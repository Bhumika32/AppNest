import secrets
from typing import Optional, Union, Dict
from sqlalchemy.orm import Session
from app.platform.module_result import ModuleResult

class MentorService:

    LOW_SCORE_TIPS = [
        "Even a training dummy has better reflexes. Start slow, baka! 😤",
        "Accuracy first! Speed comes later. Did you learn nothing at the academy? 🗡️",
        "Your power level is literally dropping. Break it into smaller steps! 📉",
    ]

    MID_SCORE_TIPS = [
        "You're improving... slowly. Refining your strategy wouldn't hurt. 🐢",
        "Look for patterns in your mistakes, if you can even see them. 👀",
        "Consistency might actually make you decent. Keep pushing! 🔥",
    ]

    HIGH_SCORE_TIPS = [
        "Okay, fine. That was strong. Increase the difficulty if you dare. ⚡",
        "Optimize your approach. You might actually be a threat now. ⚔️",
        "Hmph. Push your limits—I suppose you're ready for the real deal. 🌌",
    ]

    GENERIC_TIPS = [
        "Consistency is key! Keep practicing, rookie! 📈",
        "Take a break! An overheated brain is worse than a broken blade! 🧠",
        "Every session teaches you something... hopefully. 🚀",
        "Focus! Accuracy before speed! 🎯",
    ]

    @staticmethod
    def _safe_choice(items: list) -> str:
        return items[secrets.randbelow(len(items))]

    @staticmethod
    def _normalize_result(result: Optional[Union[ModuleResult, Dict]]) -> Dict:
        if isinstance(result, ModuleResult):
            return {"score": getattr(result, "score", 0) or 0}
        if isinstance(result, dict):
            return {"score": int(result.get("score", 0))}
        return {"score": 0}

    @staticmethod
    def get_advice(db: Session, module_id: int , result: Optional[Union[ModuleResult, Dict]] = None, user: Optional[object] = None) -> str:
        score = MentorService._normalize_result(result)["score"]

        if score < 50: return MentorService._safe_choice(MentorService.LOW_SCORE_TIPS)
        if score < 80: return MentorService._safe_choice(MentorService.MID_SCORE_TIPS)
        if score >= 80: return MentorService._safe_choice(MentorService.HIGH_SCORE_TIPS)
        
        return MentorService._safe_choice(MentorService.GENERIC_TIPS)

    @staticmethod
    def fallback_tip(db: Session) -> str:
        return MentorService._safe_choice(MentorService.GENERIC_TIPS)
