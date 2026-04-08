import secrets
from typing import Optional, Union, Dict
from app.platform.module_result import ModuleResult

class RoastService:

    GENERIC_ROASTS = [
        "Is this your first time using a computer, baka? 😭",
        "Error 404: Skill not found 🚫",
        "Recalibrating my expectations... to absolute zero 📉",
        "Your gameplay makes me want to uninstall myself 💀",
    ]

    ULTRA_ROASTS = [
        "You didn't just fail, you invented a new category of failure! 💀🔥",
        "Even my training data is cringing at that performance 🤮",
        "Scientists will study this tragic display for decades 💀",
    ]

    MID_ROASTS = [
        "Not terrible… but thoroughly unimpressive. 😬",
        "You're getting there… at the speed of an incapacitated turtle 🐢",
        "So mediocre is your comfort zone huh? 😭",
    ]

    PRO_ROASTS = [
        "Okay… that was actually decent. Don't let it go to your head 👀",
        "You're improving. Still a rookie to me though 😏",
        "Respectable. Barely. 😤",
    ]

    GAME_ROASTS = {
        "tic-tac-toe": [
            "Lost to a basic algorithm? Even a slime could do better! 🤖😭",
            "The AI knew you'd do that three turns ago. Predictable much? ⚔️",
        ],
        "hungry-snake": [
            "Your snake died faster than my patience! 🐍💀",
            "Snake difficulty: Easy. Your performance: tragic 😭",
        ],
        "flappy-bird": [
            "Flappy Bird claims another victim. PATHETIC! 💀",
            "You died to a bird. literally a 2D bird. 😭",
        ]
    }

    @staticmethod
    def _safe_choice(items):
        return items[secrets.randbelow(len(items))]

    @staticmethod
    def _normalize_result(result: Optional[Union[ModuleResult, Dict]]) -> Dict:
        if isinstance(result, ModuleResult):
            return {"score": getattr(result, "score", 0) or 0}
        if isinstance(result, dict):
            return {"score": int(result.get("score", 0))}
        return {"score": 0}

    @staticmethod
    def get_roast(module_id: int, result: Optional[Union[ModuleResult, Dict]] = None, user: Optional[object] = None) -> str:
        score = RoastService._normalize_result(result)["score"]
        module_id = (module_id or "").strip().lower()

        if module_id in RoastService.GAME_ROASTS and score < 50:
            return RoastService._safe_choice(RoastService.GAME_ROASTS[module_id])

        if score == 0: return RoastService._safe_choice(RoastService.ULTRA_ROASTS)
        if score < 40: return RoastService._safe_choice(RoastService.GENERIC_ROASTS)
        if score < 70: return RoastService._safe_choice(RoastService.MID_ROASTS)
        return RoastService._safe_choice(RoastService.PRO_ROASTS)

    @staticmethod
    def get_normal_roast() -> str:
        return RoastService._safe_choice(RoastService.GENERIC_ROASTS)

    @staticmethod
    def get_ultra_roast() -> str:
        return RoastService._safe_choice(RoastService.ULTRA_ROASTS)

    @staticmethod
    def get_personal_roast(name: Optional[str]) -> str:
        name = (name or "Dev").strip().title()
        templates = [
            "Hey {name}, your skills are like your excuses — pitiful 😭",
            "{name}, playing like that might summon ancient bugs 💀",
            "{name}, your strategy: hope and vibes. Shameful! 🔥"
        ]
        return RoastService._safe_choice(templates).format(name=name)
