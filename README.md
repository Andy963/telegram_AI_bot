# ChatGPT Telegram Bot: **Fast. No daily limits. Special chat modes**

<div align="center">
<img src="https://raw.githubusercontent.com/karfly/chatgpt_telegram_bot/main/static/header.png" align="center" style="width: 100%" />
</div>

<p align="center">
<a href="https://t.me/chatgpt_karfly_bot" alt="Run Telegram Bot shield"><img src="https://img.shields.io/badge/RUN-Telegram%20Bot-blue" /></a>
</p>

We all love [chat.openai.com](https://chat.openai.com), but... It's TERRIBLY laggy, has daily limits, and is only accessible through an archaic web interface.

This repo is ChatGPT re-created with GPT-3.5 LLM as Telegram Bot. **And it works great.**

You can deploy your own bot, or use mine: [@chatgpt_karfly_bot](https://t.me/chatgpt_karfly_bot)

if you want to use 'text-davinci-003' set the `use_chatgpt_api: false` in config.yml

## Features
- Low latency replies (it usually takes about 3-5 seconds) 
- No request limits
- Code highlighting
- Special chat modes: 👩🏼‍🎓 Assistant, 👩🏼‍💻 Code Assistant, 🎬 Movie Expert. More soon
- List of allowed Telegram users
- Track $ balance spent on OpenAI API
- user `chatgpt-3.5-turbo` default

## Bot commands
- `/retry` – Regenerate last bot answer
- `/new` – Start new dialog
- `/mode` – Select chat mode
- `/balance` – Show balance
- `/help` – Show help

## Setup
1. Get your [OpenAI API](https://openai.com/api/) key

2. Get your Telegram bot token from [@BotFather](https://t.me/BotFather)

3. Edit `config/config.example.yml` to set your tokens and run 2 commands below (*if you're advanced user, you can also edit* `config/config.example.env`):
```bash
mv config/config.yml config/config.yml
```

🔥 And now **run**:
you can generate the init database or use mine:

```bash 
python bot/models.py
```

```bash
docker-compose up --build
```


TODO:
- [x] support voice message.
- [ ] voice reply
- [x] code block

## References
1. [*Build ChatGPT from GPT-3*](https://learnprompting.org/docs/applied_prompting/build_chatgpt)
