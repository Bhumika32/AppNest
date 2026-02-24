"""
app/services/roast/normal_roast.py

Normal roast service with friendly, playful roasts.
"""

import random
from dataclasses import dataclass


@dataclass
class NormalRoastResult:
    """Result of a normal roast."""
    roast_text: str
    intensity: str
    category: str


class NormalRoastService:
    """Service for generating normal (friendly) roasts."""

    ROASTS = [
        "Your code compiles? I'm surprised.",
        "That's a nice button, did you find it on StackOverflow?",
        "I've seen better CSS on a Geocities page.",
        "Is this a feature or a bug? Yes.",
        "Your commit messages are as empty as your promises.",
        "You're coding like you're trying to debug time itself.",
        "Your variable names are shorter than your attention span.",
        "I've seen better error handling in a toaster.",
        "Your code reviewer is probably stressed out.",
        "You're the reason the undo button exists.",
    ]

    @staticmethod
    def generate() -> NormalRoastResult:
        """Generate a normal (friendly) roast."""
        roast_text = random.choice(NormalRoastService.ROASTS)
        return NormalRoastResult(
            roast_text=roast_text,
            intensity="Friendly",
            category="Normal",
        )
