"""Optional media support for photos, GIFs, videos, and voice notes."""

from __future__ import annotations

import logging
import random
from pathlib import Path

from telegram import Bot

from bot.config import BotConfig


logger = logging.getLogger(__name__)

MEDIA_FOLDERS = {
    "photo": ("photos", {".jpg", ".jpeg", ".png", ".webp"}),
    "animation": ("gifs", {".gif"}),
    "voice": ("voice_notes", {".ogg", ".oga", ".mp3", ".m4a"}),
    "video": ("videos", {".mp4", ".mov", ".webm"}),
}


def _pick_file(folder: Path, extensions: set[str]) -> Path | None:
    if not folder.exists():
        return None
    candidates = [
        path for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in extensions
    ]
    return random.choice(candidates) if candidates else None


async def send_random_media(
    bot: Bot,
    chat_id: int,
    config: BotConfig,
    *,
    chance: float = 0.22,
) -> None:
    """Sometimes send one media file from the media folders."""

    if config.dry_run or random.random() > chance:
        return

    media_type = random.choice(list(MEDIA_FOLDERS))
    folder_name, extensions = MEDIA_FOLDERS[media_type]
    file_path = _pick_file(config.media_dir / folder_name, extensions)
    if file_path is None:
        return

    logger.info("Sending %s media: %s", media_type, file_path)
    with file_path.open("rb") as media_file:
        if media_type == "photo":
            await bot.send_photo(chat_id=chat_id, photo=media_file)
        elif media_type == "animation":
            await bot.send_animation(chat_id=chat_id, animation=media_file)
        elif media_type == "voice":
            await bot.send_voice(chat_id=chat_id, voice=media_file)
        elif media_type == "video":
            await bot.send_video(chat_id=chat_id, video=media_file)
