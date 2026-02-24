"""
app/services/roast/ai_roast.py

AI-powered roast service using contextual generation.
"""

import random
from dataclasses import dataclass


@dataclass
class AIRoastResult:
    """Result of an AI roast."""
    roast_text: str
    intensity: str
    category: str
    context: str


class AIRoastService:
    """Service for generating AI-powered roasts."""

    GAME_ROASTS = {
        'tictactoe': [
            "Lost to an AI that's literally just doing math. Ouch 😭",
            "TicTacToe AI: 1, Your strategy: 'just wing it' 💀",
            "You got destroyed at the simplest game ever. Respect 🔥",
        ],
        'snake': [
            "Your snake crashed into itself faster than your code 💀",
            "Snake difficulty: Easy. Your performance: Legendary fail 😭",
            "You made Snake look harder than calculus 🔥",
        ],
        'flappybird': [
            "Flappy Bird has defeated another victim. RIP 💀",
            "You died to a bird. THE BIRD. DIED. 😭",
            "Even the bird felt bad for you 🔥",
        ],
        'breakbreaker': [
            "You broke more bricks in your desktop than in the game 💀",
            "That paddle control was... adventurous 😭",
            "The bricks are still laughing at you 🔥",
        ],
    }

    TOOL_ROASTS = {
        'bmi': [
            "BMI Calculator: Breaking it down so you don't have to 💀",
            "At least your health stats are honest 😭",
            "Numbers don't lie... and that's the problem 🔥",
        ],
        'currency': [
            "Converting currencies better than you convert effort 💀",
            "Your wallet status: depressed 😭",
            "Money talks... and it's leaving 🔥",
        ],
        'weather': [
            "Even the weather app knows more about planning than you 💀",
            "It's raining, and your motivation is drizzling 😭",
            "The forecast: cloudy with a chance of procrastination 🔥",
        ],
        'age': [
            "Time flies when you're having fun... you're not 💀",
            "Getting older, wiser, or just tired? Asking for a friend 😭",
            "Another year older, no wiser yet 🔥",
        ],
    }

    @staticmethod
    def generate_game_roast(game_name: str) -> AIRoastResult:
        """
        Generate a game-specific roast.

        Args:
            game_name: Name of the game (tictactoe, snake, etc.)

        Returns:
            AIRoastResult with game-specific roast
        """
        game_name = game_name.lower()
        roasts = AIRoastService.GAME_ROASTS.get(game_name, AIRoastService.GAME_ROASTS['tictactoe'])
        roast_text = random.choice(roasts)

        return AIRoastResult(
            roast_text=roast_text,
            intensity="AI",
            category="Game",
            context=game_name,
        )

    @staticmethod
    def generate_tool_roast(tool_name: str) -> AIRoastResult:
        """
        Generate a tool-specific roast.

        Args:
            tool_name: Name of the tool (bmi, currency, etc.)

        Returns:
            AIRoastResult with tool-specific roast
        """
        tool_name = tool_name.lower()
        roasts = AIRoastService.TOOL_ROASTS.get(tool_name, AIRoastService.TOOL_ROASTS['bmi'])
        roast_text = random.choice(roasts)

        return AIRoastResult(
            roast_text=roast_text,
            intensity="AI",
            category="Tool",
            context=tool_name,
        )

    @staticmethod
    def generate_random() -> AIRoastResult:
        """Generate a random AI roast."""
        all_roasts = list(AIRoastService.GAME_ROASTS.values()) + list(
            AIRoastService.TOOL_ROASTS.values()
        )
        roasts = random.choice(all_roasts)
        roast_text = random.choice(roasts)

        return AIRoastResult(
            roast_text=roast_text,
            intensity="AI",
            category="Random",
            context="general",
        )
