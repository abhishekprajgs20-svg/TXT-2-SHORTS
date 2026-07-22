# ðŸŽ¬ TXT 2 SHORTS â€” Telegram Bot

Send a `.txt` MCQ file âž” Get YouTube Shorts videos for every question, automatically!

## Features
- 30 Gamified Dark Themes (random per question)
- Live countdown timer with ticking sound
- Animated option reveals
- Answer reveal with explanation
- "Follow for Daily Quiz" ending

## Setup

### 1. Create Telegram Bot
- Open [@BotFather](https://t.me/BotFather) on Telegram
- Send `/newbot` âž” follow steps âž” copy your **BOT_TOKEN**

### 2. Deploy on Render.com (Free)
1. Fork this repo to your GitHub
2. Go to [render.com](https://render.com) âž” **New** âž” **Web Service**
3. Connect your GitHub repo
4. Set environment variable:
   - `BOT_TOKEN` = your Telegram bot token
5. Render will auto-detect `render.yaml` and deploy!

### 3. Use the Bot
1. Open your bot on Telegram
2. Send `/start`
3. Send your `.txt` MCQ file
4. Receive videos one by one ðŸš€

## MCQ File Format
```
Q1. What is the capital of India?
a) Mumbai
b) Delhi âœ…
c) Kolkata
d) Chennai
Ex: Delhi has been the capital of India since 1911...

Q2. ...
```

âœ… = correct answer
Ex: = explanation (optional)

## Tech Stack
- `python-telegram-bot` v20 (async)
- `FastAPI` + `uvicorn` (webhook server)
- `edge-tts` (Microsoft free TTS)
- `Pillow` (slide rendering, no browser)
- `FFmpeg` (video assembly)
- Host: **Render.com** (Free tier)