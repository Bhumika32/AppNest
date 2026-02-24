"""
app/services/roast_service.py

Handles logic for AI Roast System.
"""

import random

class RoastService:
    ROASTS = [
        "Your code compiles? I'm surprised.",
        "That's a nice button, did you find it on StackOverflow?",
        "I've seen better CSS on a Geocities page.",
        "Is this a feature or a bug? Yes.",
        "Your commit messages are as empty as your promises."
    ]

    @staticmethod
    def generate_roast(context=None):
        """
        Generate a roast based on context (e.g., losing a game, bad code).
        """
        # In a real expanded version, this could call an LLM.
        # For now, return a classic predefined roast.
        return random.choice(RoastService.ROASTS)
