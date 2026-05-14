"""Message selection, pacing, and anti-repetition logic."""

from __future__ import annotations

import json
import random
from datetime import timedelta
from pathlib import Path

from bot.config import BotConfig
from bot.utils import countdown_line, remaining_until_birthday


STATE_FILE = "sent_messages.json"


class MessageGenerator:
    """Loads romantic message datasets and returns fresh messages."""

    def __init__(self, config: BotConfig) -> None:
        self.config = config
        self.config.state_dir.mkdir(exist_ok=True)
        self.state_path = self.config.state_dir / STATE_FILE
        self.datasets = self._load_datasets()
        self.state = self._load_state()

    def _load_datasets(self) -> dict[str, list[str]]:
        datasets: dict[str, list[str]] = {}
        for path in self.config.messages_dir.glob("*.json"):
            with path.open("r", encoding="utf-8") as file:
                datasets[path.stem] = json.load(file)
        return datasets

    def _load_state(self) -> dict[str, list[str]]:
        if not self.state_path.exists():
            return {"sent": []}
        with self.state_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _save_state(self) -> None:
        with self.state_path.open("w", encoding="utf-8") as file:
            json.dump(self.state, file, ensure_ascii=False, indent=2)

    def _remember(self, message: str) -> None:
        sent = self.state.setdefault("sent", [])
        sent.append(message)
        self.state["sent"] = sent[-220:]
        self._save_state()

    def _choose(self, keys: list[str]) -> str:
        pool: list[str] = []
        for key in keys:
            pool.extend(self.datasets.get(key, []))

        sent = set(self.state.get("sent", []))
        fresh = [message for message in pool if message not in sent]
        if not fresh:
            self.state["sent"] = []
            fresh = pool

        message = random.choice(fresh)
        self._remember(message)
        return self._personalize(message)

    def _personalize(self, message: str) -> str:
        return (
            message
            .replace("{her}", self.config.girlfriend_name)
            .replace("{him}", self.config.boyfriend_name)
        )

    def category_for_now(self) -> str:
        """Return the emotional stage based on remaining time."""

        remaining = remaining_until_birthday(self.config)
        if remaining.total_seconds() <= 0:
            return "celebration"
        if remaining <= timedelta(minutes=10):
            return "final_10_minutes"
        if remaining <= timedelta(hours=1):
            return "final_hour"
        if remaining <= timedelta(hours=6):
            return "final_6_hours"
        if remaining <= timedelta(days=1):
            return "one_day"
        if remaining <= timedelta(days=3):
            return "three_days"
        return "daily"

    def next_countdown_message(self) -> str:
        """Create a complete countdown message with a fresh romantic note."""

        category = self.category_for_now()
        keys_by_category = {
            "daily": ["daily", "memories", "reasons", "future"],
            "three_days": ["daily", "three_days", "miss_you", "future"],
            "one_day": ["one_day", "miss_you", "late_night", "reasons"],
            "final_6_hours": ["final_6_hours", "reasons", "virtual_hugs"],
            "final_hour": ["final_hour", "final_10_minutes"],
            "final_10_minutes": ["final_10_minutes"],
            "celebration": ["celebration"],
        }
        note = self._choose(keys_by_category[category])
        return f"{countdown_line(self.config)}\n\n{note}"

    def celebration_message(self) -> str:
        return self._choose(["celebration", "birthday_day"])

    def random_music_link(self) -> str | None:
        return random.choice(self.config.music_links) if self.config.music_links else None
