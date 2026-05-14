"""APScheduler jobs for emotional countdown pacing."""

from __future__ import annotations

import logging
from datetime import timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telegram import Bot

from bot.birthday_letter import birthday_letter
from bot.config import BotConfig
from bot.media_manager import send_random_media
from bot.message_generator import MessageGenerator
from bot.utils import remaining_until_birthday, send_with_typing


logger = logging.getLogger(__name__)


def interval_for_remaining(remaining: timedelta) -> timedelta:
    """Translate time remaining into increasingly frequent messages."""

    if remaining.total_seconds() <= 0:
        return timedelta(hours=3)
    if remaining <= timedelta(minutes=10):
        return timedelta(minutes=1)
    if remaining <= timedelta(hours=1):
        return timedelta(minutes=10)
    if remaining <= timedelta(hours=6):
        return timedelta(hours=1)
    if remaining <= timedelta(days=1):
        return timedelta(hours=3)
    if remaining <= timedelta(days=3):
        return timedelta(hours=12)
    return timedelta(days=1)


class RomanticScheduler:
    """Owns countdown, birthday, and celebration jobs."""

    def __init__(self, bot: Bot, config: BotConfig, generator: MessageGenerator) -> None:
        self.bot = bot
        self.config = config
        self.generator = generator
        self.scheduler = AsyncIOScheduler(timezone=config.timezone)

    def start(self) -> None:
        """Start all recurring jobs."""

        self.scheduler.add_job(
            self._send_countdown_and_reschedule,
            trigger=IntervalTrigger(minutes=1, timezone=self.config.timezone),
            id="heartbeat_rescheduler",
            replace_existing=True,
            max_instances=1,
        )
        self.scheduler.add_job(
            self._send_midnight_letter,
            trigger="date",
            run_date=self.config.birthday,
            id="midnight_birthday_letter",
            replace_existing=True,
            misfire_grace_time=3600,
        )
        self.scheduler.add_job(
            self._send_celebration,
            trigger=IntervalTrigger(
                hours=4,
                start_date=self.config.birthday + timedelta(hours=2),
                end_date=self.config.birthday + timedelta(hours=23, minutes=55),
            ),
            id="birthday_day_celebrations",
            replace_existing=True,
            max_instances=1,
        )
        self.scheduler.start()
        logger.info("Romantic scheduler started.")

    async def _send_countdown_and_reschedule(self) -> None:
        """Send countdown only when the current emotional interval says it is time."""

        if self.config.target_chat_id is None:
            logger.warning("TARGET_CHAT_ID is empty; skipping scheduled message.")
            return

        remaining = remaining_until_birthday(self.config)
        if remaining < -timedelta(days=1):
            return

        interval = interval_for_remaining(remaining)
        marker = int(remaining.total_seconds() // max(60, int(interval.total_seconds())))

        state = self.generator.state
        last_marker = state.get("last_countdown_marker")
        if last_marker == marker:
            return

        state["last_countdown_marker"] = marker
        self.generator._save_state()

        text = self.generator.next_countdown_message()
        await send_with_typing(
            self.bot,
            self.config.target_chat_id,
            text,
            dry_run=self.config.dry_run,
        )
        media_chance = min(0.45, 0.12 + (self.config.romantic_intensity * 0.025))
        await send_random_media(
            self.bot,
            self.config.target_chat_id,
            self.config,
            chance=media_chance,
        )

        music_link = self.generator.random_music_link()
        if music_link and remaining <= timedelta(days=1):
            await send_with_typing(
                self.bot,
                self.config.target_chat_id,
                f"🎶 A tiny soundtrack for missing each other tonight:\n{music_link}",
                dry_run=self.config.dry_run,
            )

    async def _send_midnight_letter(self) -> None:
        if self.config.target_chat_id is None:
            return
        await send_with_typing(
            self.bot,
            self.config.target_chat_id,
            birthday_letter(self.config),
            dry_run=self.config.dry_run,
        )

    async def _send_celebration(self) -> None:
        if self.config.target_chat_id is None:
            return
        await send_with_typing(
            self.bot,
            self.config.target_chat_id,
            self.generator.celebration_message(),
            dry_run=self.config.dry_run,
        )
