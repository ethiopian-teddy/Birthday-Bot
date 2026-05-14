"""Entry point for the romantic Telegram birthday countdown bot."""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from bot.config import load_config
from bot.message_generator import MessageGenerator
from bot.scheduler import RomanticScheduler
from bot.utils import countdown_line, send_with_typing


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


config = load_config()
message_generator = MessageGenerator(config)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome message and chat id helper."""

    chat_id = update.effective_chat.id if update.effective_chat else None
    text = (
        "Hi love ❤️\n\n"
        "This little countdown was made with a very real heart behind it.\n\n"
        f"{countdown_line(config)}\n\n"
        f"Setup note for {config.boyfriend_name}: this chat id is <code>{chat_id}</code>."
    )
    await update.message.reply_html(text)


async def countdown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the current exact countdown on demand."""

    await update.message.reply_html(countdown_line(config))


async def surprise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a romantic surprise message whenever she asks."""

    text = message_generator.next_countdown_message()
    await update.message.reply_html(text)


async def post_init(application: Application) -> None:
    """Start scheduling after Telegram's asyncio loop is ready."""

    if config.target_chat_id is None:
        logger.info("TARGET_CHAT_ID is empty. Send /start to the bot to discover it.")
    else:
        await send_with_typing(
            application.bot,
            config.target_chat_id,
            "The countdown bot is awake now ❤️",
            dry_run=config.dry_run,
        )

    RomanticScheduler(application.bot, config, message_generator).start()


def main() -> None:
    """Build the Telegram app, attach handlers, and run forever."""

    if not config.bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing. Copy .env.example to .env and fill it in.")

    application = Application.builder().token(config.bot_token).post_init(post_init).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("countdown", countdown))
    application.add_handler(CommandHandler("surprise", surprise))

    logger.info("Bot is running. Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
