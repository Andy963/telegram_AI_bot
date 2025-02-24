## Telegram AI Bot:

This repo a Telegram AI Bot(with chatgpt,azure-openai, palm2 etc.). **And it works great.**

You can deploy your own bot

### Features

- List of allowed Telegram users
- use `chatgpt-3.5-turbo` default
- reply with voice message (use azure text to speech)
- multi language voice message support (azure TTS)
- picture ocr and translate, summary, tell story joke etc.
- parse a url link(only summary the text for now)
- paLM2 support(use azure translate to en and ask palm2, palm2 translate is so weak)
- azure openai support
- Anthropic claude support
- user management
- set stream response by user(for low speed response)

### Bot commands

- `/retry` – Regenerate last bot answer
- `/new` – Start new dialog
- `/mode` – Select chat mode
- `/help` – Show help
- `/model` - List all ai model (chatgpt, palm2, azure_openai etc. admin required)
- `/stream` - enable stream response or disable

### Setup

1. Get your [OpenAI API](https://openai.com/api/) , paLM2 key, , azure openai key or claude key.

2. Get your Telegram bot token from [@BotFather](https://t.me/BotFather)

3. Get your azure free trial account and get your azure key(text,speech,computer vision)

4. Docker

for docker user:

```shell

docker run -d  --name chatgpt -v /etc/gpt:/etc/gpt andy963/telegram_ai_bot:latest
```

TODO:

- [x] support voice message. (use azure text to speech)
- [x] reply with multiple language voice (contains En & Zh, need azure)
- [x] picture ocr and translate, summary, tell story joke etc.
- [x] prompt list
- [x] get content from url and summary the content(weak)
- [x] paLM2 support
- [x] export history(only text for now).
- [x] multi model support (support chatgpt, palm2, azure_openai etc.)
- [x] azure openai support
- [x] Anthropic claude support
- [x] user management
- [x] set stream response (claude only for now)
- [ ] user list page by page
- [ ] model select by user
- [ ] get the latest new and summarize and send to user on schedule (maybe with voice)

if you are using ubuntu 22.04, you need to install the latest libssl1.1 either as a binary package, or by compiling it
from sources.
```shell

## References
1. [*Build ChatGPT from GPT-3*](https://learnprompting.org/docs/applied_prompting/build_chatgpt)
2. [install libssl1.1](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstarts/setup-platform?pivots=programming-language-python&tabs=linux%2Cubuntu%2Cdotnet%2Cjre%2Cmaven%2Cnodejs%2Cmac%2Cpypi)