"""
app/services/roast/personal_roast.py

Personal roast service with name-based roasts.
"""

import random
from dataclasses import dataclass


@dataclass
class PersonalRoastResult:
    """Result of a personal roast."""
    name: str
    roast_text: str
    intensity: str
    category: str


class PersonalRoastService:
    """Service for generating personalized roasts."""

    ROAST_TEMPLATES = [
        "Hey {name}, your code is like your project timelines - consistently late 😭",
        "{name}, you debug like you're trying to solve world hunger 💀",
        "{name}, your error messages are more confusing than your life choices 😅",
        "{name}, you're a living example of 'it works on my machine' 🔥",
        "{name}, your code structure is as organized as your desktop 💀",
        "{name}, you comment your code? Wow, you're optimistic 😭",
        "{name}, your mental model is the only thing more broken than your code 😭",
        "{name}, you variable name choices are... creative? 💀",
        "{name}, your coding speed: fast. Your code quality: questionable 😅",
        "{name}, you're living proof that Stack Overflow doesn't teach best practices 🔥",
    ]

    @staticmethod
    def generate(name: str) -> PersonalRoastResult:
        """
        Generate a personalized roast.

        Args:
            name: Person's name

        Returns:
            PersonalRoastResult with customized roast
        """
        name = (name or "Dev").strip().title()
        template = random.choice(PersonalRoastService.ROAST_TEMPLATES)
        roast_text = template.format(name=name)

        return PersonalRoastResult(
            name=name,
            roast_text=roast_text,
            intensity="Personal",
            category="Personal",
        )
