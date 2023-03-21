#!/usr/bin/python
# coding:utf-8
import asyncio
import math
import random
import re
import traceback
import wave
from datetime import datetime
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
import openai
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

from bot import config
from .log import logger


def render_msg_with_code(msg):
    """给bot渲染返回的消息
    <b>text</b>：加粗文本
    <i>text</i>：斜体文本
    <u>text</u>：下划线文本
    <s>text</s>：删除线文本
    <a href="URL">text</a>：超链接文本
    <code>text</code>：等宽文本
    <pre>text</pre>：预格式化文本
    message = '''
    <pre>
    <code>
    def greet(name):
        print(f"Hello, {name}!")

    greet("World")
    </code>
    </pre>
    '''
    """
    if '`' not in msg:
        return msg
    import re
    p2 = re.compile(r'```.*?```', re.S)
    r2 = re.findall(p2, msg)
    for r in r2:
        lang = r.split('\n')[0].split('```')[1]
        msg = re.sub(f'```{lang}(.*?)```', rf'<pre><code>\1</code></pre>', msg, flags=re.S)
    return msg


async def send_like_tying(update, context, text):
    """
    send msg like typing
    :param update: bot update object
    :param context: bot context
    :param text:  msg text to send
    """
    msg = await context.bot.send_message(chat_id=update.effective_chat.id, text='God:  ', parse_mode=ParseMode.HTML)
    code_index = [(m.start(), m.end()) for m in re.finditer(r'<pre><code>(.+?)</code></pre>', text, re.S)]
    i = 0
    length = len(text)
    while i < length:
        num_chars = random.randint(1, 20) if length < 50 else random.randint(1, 50)

        if not code_index:
            current_text = text[:i + num_chars]
            full_text = msg.text + current_text
            await context.bot.edit_message_text(chat_id=msg.chat_id, message_id=msg.message_id, text=full_text,
                                                parse_mode=ParseMode.HTML)
            i += num_chars
        else:
            start, end = code_index[0]
            # expand to end of code block
            if i + num_chars > start:
                full_text = msg.text + text[:end + 1]
                await context.bot.edit_message_text(chat_id=msg.chat_id, message_id=msg.message_id, text=full_text,
                                                    parse_mode=ParseMode.HTML)
                i = end + 1
                code_index.pop(0)
            else:
                current_text = text[:i + num_chars]
                full_text = msg.text + current_text
                await context.bot.edit_message_text(chat_id=msg.chat_id, message_id=msg.message_id, text=full_text,
                                                    parse_mode=ParseMode.HTML)
                i += num_chars
        await asyncio.sleep(random.uniform(0.01, 0.15))


def text_to_speech(key: str, region: str, speech_lang: str, speech_voice: str, msg_id: int, text: str):
    """
    translate text to speech
    :param key: azure_speech_key
    :param region:  azure_speech_region
    :param speech_lang: language of the voice that speaks
    :param speech_voice:  voice name eg: zh-CN-XiaoxiaoNeural
    :param msg_id:  telegram message id
    :param text : text to speech
    """
    logger.info('text_to_speech:')
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    file_name = f"./{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"
    logger.info(f'file_name:{file_name}')
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_name)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_language = speech_lang
    speech_config.speech_synthesis_voice_name = speech_voice
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    try:
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
        logger.info(speech_synthesis_result)
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            with wave.open(file_name, 'rb') as f:
                frame_rate, num_frames = f.getframerate(), f.getnframes()
                audio_duration = float(num_frames) / float(frame_rate)
                if audio_duration >= 1:
                    return file_name
                return None
        else:
            logger.error(f'text to speech not completed : {speech_synthesis_result.reason}')
            return None
    except Exception as ex:
        logger.error(f"text to speech except: {ex}")
        logger.error(f"traceback: {traceback.format_exc()}")
        return None


def speech_to_text(key: str, region: str, filename: str):
    """azure 语音识别"""

    logger.info('speech to text:')


    try:
        with open(filename, 'rb') as f:
            transaction = openai.Audio.transcribe('whisper-1', file=f)
            logger.info(f'whisper transcribe text: {transaction.text}')
        if transaction.text:
            return transaction.text
        else:
            langs = ["en-US", "zh-CN"]
            auto_detect_source_language_config = \
                speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=langs)
            speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
            audio_config = speechsdk.audio.AudioConfig(filename=filename)
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                auto_detect_source_language_config=auto_detect_source_language_config,
                audio_config=audio_config)

            result = speech_recognizer.recognize_once_async().get()
            auto_detect_source_language_result = speechsdk.AutoDetectSourceLanguageResult(result)
            detected_language = auto_detect_source_language_result.language
            logger.info(f'detected language:{detected_language}')
            if detected_language in langs:
                logger.info(f'result: {result}')
                if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    logger.info("Recognized: {}".format(result.text))
                    return result.text

    except Exception as e:
        logger.error(f"recognize except: {e}")
        logger.error(f"traceback: {traceback.format_exc()}")
    return None


def check_contain_ch(check_str):
    """
    check if the str contains English char
    """
    flag = False
    for ch in check_str:
        if re.match(u'[\u4E00-\u9FFF]', ch):
            flag = True
            break
    return flag


async def reply_voice(update, context, answer):
    """
     check if it's only single language if it's then reply with voice
    """
    if check_contain_ch(answer):
        return
    audio_file = text_to_speech(config.azure_speech_key,
                                config.azure_speech_region,
                                config.azure_speech_lang,
                                config.azure_speech_voice,
                                update.message.chat_id,
                                answer)
    if audio_file and Path(audio_file).exists():
        await reply_multi_voice(update, context, audio_file)
        Path(audio_file).unlink()
    else:
        await update.message.reply_text("Text to speech failed")


async def reply_multi_voice(update: Update, context: CallbackContext, audio_file: str):
    logger.info('reply multi voice:')
    try:
        with wave.open(audio_file, 'rb') as f:
            # Get the audio file parameters
            sample_width = f.getsampwidth()
            frame_rate = f.getframerate()
            num_frames = f.getnframes()

            # Calculate the audio duration
            audio_duration = float(num_frames) / float(frame_rate)
            logger.info(f'audio duration: {audio_duration}')

            # Split the audio into segments of maximum duration (in seconds)
            max_duration = 59.0  # Telegram maximum audio duration is 1 minute
            num_segments = int(math.ceil(audio_duration / max_duration))
            logger.info(f'audio segments num: {num_segments}')
            for i in range(num_segments):
                # Calculate the start and end frames of the segment
                start_frame = int(i * max_duration * frame_rate)
                end_frame = int(min((i + 1) * max_duration * frame_rate, num_frames))

                # Read the segment data from the audio file
                f.setpos(start_frame)
                segment_data = f.readframes(end_frame - start_frame)

                # Write the segment data to a temporary file
                # fixme this file name can be overwrite by other
                segment_filename = 'audio_file_segment_{}.wav'.format(i)
                with wave.open(segment_filename, 'wb') as segment_file:
                    segment_file.setparams(f.getparams())
                    segment_file.writeframes(segment_data)

                # Send the segment as a Telegram audio message
                with open(segment_filename, 'rb') as segment_file:
                    await context.bot.send_voice(chat_id=update.effective_chat.id, voice=segment_file)

                # Delete the temporary file
                Path(segment_filename).unlink()
                logger.info(f'reply multi voice done!')
    except Exception as e:
        logger.error(f'error in reply_multi_voice: {e}')
        logger.error(f"error stack: {traceback.format_exc()}")
