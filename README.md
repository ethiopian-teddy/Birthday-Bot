# Romantic Telegram Birthday Countdown Bot

A warm, long-distance birthday countdown bot for Telegram. It sends increasingly emotional messages as the birthday approaches, mixes English and Amharic naturally, supports photos/GIFs/voice notes/videos, and sends a long midnight birthday letter.

## What It Does

- Counts down to her birthday in days, hours, minutes, and seconds.
- Sends scheduled romantic messages automatically.
- Increases message frequency as midnight gets closer.
- Avoids repeating the same messages too soon.
- Simulates typing before sending messages.
- Supports optional photos, GIFs, videos, voice notes, and music links.
- Includes a simple romantic countdown webpage in `web/`.

## Project Structure

```text
bot/
  config.py              Loads .env and config/settings.json
  scheduler.py           Adaptive countdown scheduling
  message_generator.py   Randomized messages and anti-repetition
  media_manager.py       Optional photo/GIF/video/voice support
  birthday_letter.py     Midnight birthday letter
  utils.py               Countdown and Telegram helpers
messages/                Romantic message datasets
media/
  photos/                Add .jpg, .png, .webp files
  gifs/                  Add .gif files
  voice_notes/           Add .ogg, .oga, .mp3, .m4a files
  videos/                Add .mp4, .mov, .webm files
config/settings.json     Easy non-secret customization
web/                     Optional romantic countdown webpage
main.py                  Bot entry point
requirements.txt
.env.example
```

## Setup

1. Create a Telegram bot with [@BotFather](https://t.me/BotFather).
2. Copy `.env.example` to `.env`.
3. Put your bot token in `TELEGRAM_BOT_TOKEN`.
4. Edit `config/settings.json`:

```json
{
  "birthday_date": "2026-12-25",
  "girlfriend_name": "Her Name",
  "boyfriend_name": "Your Name",
  "timezone": "Africa/Addis_Ababa",
  "romantic_intensity": 8
}
```

5. Install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

6. Start the bot:

```bash
python main.py
```

7. Open Telegram, message your bot, and send `/start`.
8. Copy the chat id shown by the bot into `.env` as `TARGET_CHAT_ID`.
9. Restart the bot.

## Commands

- `/start` shows a welcome message and the chat id.
- `/countdown` shows the exact current countdown.
- `/surprise` sends a romantic surprise message.

## Scheduling Behavior

The bot checks once per minute and sends only when the current emotional stage says it should:

- 7+ days away: about once per day
- 3 days away: morning/evening style pacing
- 1 day away: every few hours
- Final 6 hours: hourly
- Final hour: every 10 minutes
- Final 10 minutes: every minute
- Midnight: long birthday letter
- Birthday day: celebration messages every few hours

The anti-repetition state is saved in `state/sent_messages.json`.

## Customizing Messages

Edit the JSON files in `messages/`. You can add as many messages as you want.

Supported placeholders:

- `{her}` becomes her name
- `{him}` becomes your name

Example:

```json
"{her}, I miss you softly today. I cannot wait until distance becomes just a story we tell."
```

## Adding Media

Drop files into these folders:

- `media/photos/`
- `media/gifs/`
- `media/voice_notes/`
- `media/videos/`

The bot will occasionally send a random file after a romantic message. For best Telegram voice-note behavior, use `.ogg` or `.oga`.

## Music Links

Add comma-separated links in `.env`:

```text
MUSIC_LINKS=https://youtu.be/your-song,https://open.spotify.com/track/your-song
```

The bot may share a music link during the final day.

## Optional Web Countdown

Open `web/index.html` in a browser for the romantic countdown page.

Edit `web/config.js`:

```js
window.LOVE_COUNTDOWN_CONFIG = {
  girlfriendName: "Her Name",
  boyfriendName: "Your Name",
  birthdayIso: "2026-12-25T00:00:00+03:00",
  musicUrl: "https://youtu.be/your-song"
};
```

Add images:

- `web/assets/hero.jpg`
- `web/assets/photo1.jpg`
- `web/assets/photo2.jpg`
- `web/assets/photo3.jpg`

For local hosting:

```bash
python -m http.server 8080 --directory web
```

Then open `http://localhost:8080`.

## Railway Deployment

1. Push this project to GitHub.
2. Create a new Railway project from the repo.
3. Add environment variables from `.env.example`.
4. Use this start command:

```bash
python main.py
```

5. Make sure the service type is a worker, not a web server.

## Render Deployment

This repo includes `render.yaml`.

1. Push to GitHub.
2. In Render, create a new Blueprint or Background Worker.
3. Add environment variables.
4. Build command:

```bash
pip install -r requirements.txt
```

5. Start command:

```bash
python main.py
```

## VPS Deployment

```bash
git clone your-repo-url
cd your-repo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python main.py
```

For 24/7 reliability, run it with `systemd`, `supervisor`, or `tmux`.

Example `systemd` service:

```ini
[Unit]
Description=Romantic Telegram Birthday Countdown Bot
After=network.target

[Service]
WorkingDirectory=/home/ubuntu/romantic-birthday-bot
ExecStart=/home/ubuntu/romantic-birthday-bot/.venv/bin/python main.py
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

## Testing Safely

Set this in `.env`:

```text
DRY_RUN=true
```

The bot will log scheduled messages without sending them.

You can also set the birthday date to tomorrow to watch the pacing become more frequent.

## Emotional Customization Tips

- Add real memories to `messages/memories.json`.
- Add very specific reasons you love her to `messages/reasons.json`.
- Add future date plans you have actually talked about to `messages/future.json`.
- Record one or two short voice notes and place them in `media/voice_notes/`.
- Put favorite photos in `media/photos/`.

The more personal the message banks are, the more the bot will feel like you.
