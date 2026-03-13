# -----------------------------------------------------------------------------
# File: backend/app/domain/roast_service.py
#
# Description:
# Service responsible for generating roast messages after module execution.
#
# Design Principles:
# - Gemini AI calls handled centrally by ExperienceEngine
# - This service provides fallback roasts only
# - Maintains backward compatibility with older calls
# - Supports both ModuleResult objects and dictionaries
#
# Stability Improvements:
# - Removed duplicate Gemini calls
# - Safe attribute access
# - Supports dict and ModuleResult
# -----------------------------------------------------------------------------

import random
from typing import Optional, Union
from app.platform.module_result import ModuleResult


class RoastService:

    GENERIC_ROASTS = [
        "Is this your first time using a computer? 😭",
        "My grandma plays better than this, and she's a literal cloud now ☁️",
        "Error 404: Skill not found 🚫",
        "Recalibrating expectations... to zero 📉",
        "Your code makes debugging feel like archaeology 💀",
    ]

    ULTRA_ROASTS = [
        "You didn't just fail, you invented a new category of failure 💀🔥",
        "Even my training data is cringing at that performance 🤮",
        "Scientists will study this failure for decades 💀",
    ]

    GAME_ROASTS = {

        "tictactoe": [
            "Lost to an AI that's literally just doing math 😭",
            "The AI saw that mistake three moves ago 💀",
        ],

        "snake": [
            "Your snake crashed into itself faster than your code 💀",
            "Snake difficulty: Easy. Your performance: impossible 😭",
        ],

        "flappybird": [
            "Flappy Bird claims another victim 💀",
            "You died to a bird. THE BIRD 😭",
        ]
    }

    # -------------------------------------------------------------------------
    # MAIN ROAST GENERATOR
    # -------------------------------------------------------------------------
    @staticmethod
    def get_roast(
        module_key: str,
        result: Optional[Union[ModuleResult, dict]] = None,
        module_result: Optional[Union[ModuleResult, dict]] = None,
        user=None
    ) -> str:

        """
        Generate roast after module completion.

        Backward compatibility:
        - Supports `result`
        - Supports `module_result`
        """

        if module_result is not None:
            result = module_result

        score = 0
        status = "complete"

        if isinstance(result, dict):

            score = result.get("score", 0)
            status = result.get("status", "complete")

        elif isinstance(result, ModuleResult):

            score = result.score
            status = result.status

        username = "Player"

        if user and getattr(user, "username", None):
            username = user.username

        # Game-specific roast
        if module_key in RoastService.GAME_ROASTS:

            return random.choice(
                RoastService.GAME_ROASTS[module_key]
            )

        # Score based roast
        if score == 0:

            return random.choice(RoastService.ULTRA_ROASTS)

        return random.choice(RoastService.GENERIC_ROASTS)

    # -------------------------------------------------------------------------
    # NORMAL ROAST
    # -------------------------------------------------------------------------
    @staticmethod
    def get_normal_roast():

        return random.choice(
            RoastService.GENERIC_ROASTS
        )

    # -------------------------------------------------------------------------
    # ULTRA ROAST
    # -------------------------------------------------------------------------
    @staticmethod
    def get_ultra_roast():

        return random.choice(
            RoastService.ULTRA_ROASTS
        )

    # -------------------------------------------------------------------------
    # PERSONAL ROAST
    # -------------------------------------------------------------------------
    @staticmethod
    def get_personal_roast(name: str):

        name = (name or "Dev").strip().title()

        templates = [

            "Hey {name}, your code is like your deadlines — always late 😭",

            "{name}, debugging like that might summon ancient bugs 💀",

            "{name}, your strategy: hope and vibes 🔥"
        ]

        return random.choice(templates).format(name=name)
# import random
# from typing import Optional
# from app.platform.module_result import ModuleResult
# from app.domain.gemini_service import gemini_ai


# class RoastService:
#     """
#     Handles generation of roasts using Gemini AI with rule-based fallbacks.
#     """

#     GENERIC_ROASTS = [
#         "Is this your first time using a computer? 😭",
#         "My grandma plays better than this, and she's a literal cloud now ☁️",
#         "Error 404: Skill not found 🚫",
#         "Recalibrating expectations... to zero. 📉",
#         "Your code makes debugging feel like archaeology 💀",
#         "You're the reason 'technical debt' is an understatement 😭",
#         "Your error handling: just let it crash 🔥",
#         "Legend has it, your first attempt is still loading. ⏳",
#         "Even the AI is embarrassed for you. 🤖",
#     ]

#     ULTRA_ROASTS = [
#         "You didn't just fail, you invented a new category of failure 💀🔥",
#         "Even my training data is cringing at that performance 🤮",
#         "That was so bad, it looped back around to impressive. Nope. Still bad. 😭",
#         "I've seen better performance from a 1990 screensaver 👾",
#         "Your strategy: exist. Your execution: also just existing. 💀",
#         "The AI cried. I didn't think that was possible. It wasn't. You broke it. 🤖💔",
#         "Scientists will study this failure for decades. In a bad museum. 🔬💀",
#     ]

#     GAME_ROASTS = {
#         'tictactoe': [
#             "Lost to an AI that's literally just doing math. Ouch 😭",
#             "TicTacToe AI: 1, Your strategy: 'just wing it' 💀",
#         ],
#         'snake': [
#             "Your snake crashed into itself faster than your code 💀",
#             "Snake difficulty: Easy. Your performance: Legendary fail 😭",
#         ],
#         'flappybird': [
#             "Flappy Bird has defeated another victim. RIP 💀",
#             "You died to a bird. THE BIRD. DIED. 😭",
#         ]
#     }

#     @staticmethod
#     def get_roast(module_key: str, result: Optional[ModuleResult] = None, user=None) -> str:
#         """
#         Main entry point for generating dynamic roasts.
#         """
#         status = result.status if result else "complete"
#         score = result.score if result else 0

#         # 1. Try AI-powered Roast
#         context = f"User {user.username if user else 'Player'} finished {module_key} with score {score}. Status: {status}."
#         ai_roast = gemini_ai.generate_roast(context)
#         if ai_roast:
#             return ai_roast

#         # 2. Fallback to category-specific hardcoded roasts
#         if module_key in RoastService.GAME_ROASTS:
#             return random.choice(RoastService.GAME_ROASTS[module_key])

#         # 3. Final generic fallback
#         return random.choice(RoastService.GENERIC_ROASTS)

#     @staticmethod
#     def get_normal_roast() -> str:
#         """Get a normal (friendly/generic) roast. No AI, immediate response."""
#         return random.choice(RoastService.GENERIC_ROASTS)

#     @staticmethod
#     def get_ultra_roast() -> str:
#         """Get a maximum-intensity roast."""
#         return random.choice(RoastService.ULTRA_ROASTS)

#     @staticmethod
#     def get_personal_roast(name: str) -> str:
#         name = (name or "Dev").strip().title()
#         templates = [
#             "Hey {name}, your code is like your project timelines - consistently late 😭",
#             "{name}, you debug like you're trying to solve world hunger 💀",
#             "{name}, you're a living example of 'it works on my machine' 🔥"
#         ]
#         return random.choice(templates).format(name=name)
