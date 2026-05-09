from __future__ import annotations

import random


ACHIEVEMENTS: tuple[str, ...] = (
    "Professional yapper",
    "Touched grass not found",
    "Keyboard philosopher",
    "Certified chat main character",
    "Won an argument with a wall",
    "Speedran confusion any%",
    "Suspiciously online",
    "NPC dialogue collector",
    "Overthinking grandmaster",
    "Local legend in a three-message radius",
    "Quantum nonsense generator",
    "Emotionally attached to the send button",
)


class AchievementService:
    def __init__(self, achievements: tuple[str, ...] = ACHIEVEMENTS) -> None:
        self._achievements = achievements

    def random_achievement(self) -> str:
        return f'\U0001f3c6 Achievement unlocked:\n"{random.choice(self._achievements)}"'
