"""Small reusable helpers for dates, formatting, and Telegram sending."""

from __future__ import annotations

import asyncio
import logging
import random
from datetime import datetime, timedelta
from html import escape

from telegram import Bot
from telegram.constants import ChatAction, ParseMode

from bot.config import BotConfig


logger = logging.getLogger(__name__)


def now_in_her_timezone(config: BotConfig) -> datetime:
    """Return the current time in the birthday timezone."""

    return datetime.now(config.timezone)


def remaining_until_birthday(config: BotConfig) -> timedelta:
    """Return time left until midnight on her birthday."""

    return config.birthday - now_in_her_timezone(config)


def format_countdown(delta: timedelta) -> str:
    """Format a timedelta as days, hours, minutes, and seconds."""

    total_seconds = max(0, int(delta.total_seconds()))
    days, rem = divmod(total_seconds, 86_400)
    hours, rem = divmod(rem, 3_600)
    minutes, seconds = divmod(rem, 60)
    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"


def countdown_line(config: BotConfig) -> str:
    """Create a romantic live countdown line."""

    return f"⏳ <b>{format_countdown(remaining_until_birthday(config))}</b> until your day, {escape(config.girlfriend_name)}."


async def send_with_typing(
    bot: Bot,
    chat_id: int,
    text: str,
    *,
    dry_run: bool = False,
    parse_mode: str = ParseMode.HTML,
) -> None:
    """Simulate a real typing pause, then send a Telegram message."""

    if dry_run:
        logger.info("DRY RUN message to %s: %s", chat_id, text)
        return

    await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    await asyncio.sleep(random.uniform(1.4, 4.2))
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=parse_mode,
        disable_web_page_preview=False,
    )
