"""
app/services/roast/ultra_roast.py

Ultra roast service with maximum intensity roasts.
"""

import random
from dataclasses import dataclass


@dataclass
class UltraRoastResult:
    """Result of an ultra roast."""
    roast_text: str
    intensity: str
    category: str


class UltraRoastService:
    """Service for generating ultra (maximum intensity) roasts."""

    ROASTS = [
        "Your code makes debugging feel like archaeology 💀",
        "You're the reason 'technical debt' is an understatement 😭",
        "Your error handling: just let it crash 🔥",
        "You code like stackoverflow is your IDE 💀",
        "Copy-paste programming? More like copy-paste disasters 😭",
        "Your function names are as clear as mud 🔥",
        "You're a walking security vulnerability 💀",
        "Your code review notes should have trigger warnings 😭",
        "You think comments are for other people 🔥",
        "Your architecture would make developers cry 💀",
        "You're the reason code reviews take 3 hours 😭",
        "Your refactoring is... optimistic 🔥",
        "You hardcode like it's going out of style 💀",
    ]

    @staticmethod
    def generate() -> UltraRoastResult:
        """Generate an ultra (maximum intensity) roast."""
        roast_text = random.choice(UltraRoastService.ROASTS)
        return UltraRoastResult(
            roast_text=roast_text,
            intensity="Ultra",
            category="Ultra",
        )
