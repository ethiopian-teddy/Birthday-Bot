"""Configuration helpers for the romantic birthday countdown bot."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class BotConfig:
    """All user-editable settings used by the bot."""

    bot_token: str
    target_chat_id: int | None
    girlfriend_name: str
    boyfriend_name: str
    birthday: datetime
    timezone: ZoneInfo
    romantic_intensity: int
    dry_run: bool
    messages_dir: Path
    media_dir: Path
    state_dir: Path
    music_links: list[str]


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _get_int(name: str, default: int) -> int:
    raw_value = os.getenv(name, str(default)).strip()
    try:
        return int(raw_value)
    except ValueError:
        return default


def _parse_birthday(date_text: str, timezone: ZoneInfo) -> datetime:
    """Parse YYYY-MM-DD into midnight in her timezone."""

    birthday_date = datetime.strptime(date_text, "%Y-%m-%d").date()
    return datetime.combine(birthday_date, datetime.min.time(), tzinfo=timezone)


def _load_settings_file() -> dict[str, object]:
    """Load optional non-secret settings from config/settings.json."""

    settings_path = BASE_DIR / "config" / "settings.json"
    if not settings_path.exists():
        return {}
    with settings_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _setting(settings: dict[str, object], env_name: str, file_name: str, default: str) -> str:
    """Environment variables win over the friendly JSON settings file."""

    env_value = os.getenv(env_name)
    if env_value not in (None, ""):
        return env_value
    value = settings.get(file_name, default)
    return str(value)


def load_config() -> BotConfig:
    """Load .env settings and return a strongly typed config object."""

    load_dotenv(BASE_DIR / ".env")

    settings = _load_settings_file()
    timezone_name = _setting(settings, "TIMEZONE", "timezone", "Africa/Addis_Ababa")
    timezone = ZoneInfo(timezone_name)
    birthday = _parse_birthday(_setting(settings, "BIRTHDAY_DATE", "birthday_date", "2026-12-25"), timezone)

    chat_id_text = os.getenv("TARGET_CHAT_ID", "").strip()
    target_chat_id = int(chat_id_text) if chat_id_text else None

    music_links = [
        link.strip()
        for link in os.getenv("MUSIC_LINKS", "").split(",")
        if link.strip()
    ]

    return BotConfig(
        bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        target_chat_id=target_chat_id,
        girlfriend_name=_setting(settings, "GIRLFRIEND_NAME", "girlfriend_name", "my love"),
        boyfriend_name=_setting(settings, "BOYFRIEND_NAME", "boyfriend_name", "your boyfriend"),
        birthday=birthday,
        timezone=timezone,
        romantic_intensity=max(
            1,
            min(
                10,
                int(_setting(settings, "ROMANTIC_INTENSITY", "romantic_intensity", "8")),
            ),
        ),
        dry_run=_get_bool("DRY_RUN", False),
        messages_dir=BASE_DIR / "messages",
        media_dir=BASE_DIR / "media",
        state_dir=BASE_DIR / "state",
        music_links=music_links,
    )
