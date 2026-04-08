#app/domain/xp_domain.py
import math

class XPDomain:

    # -----------------------------
    # LEVEL SYSTEM
    # -----------------------------
    @staticmethod
    def calculate_level(total_xp: int) -> int:
        return max(1, math.floor(math.sqrt(total_xp / 100)))

    @staticmethod
    def xp_for_next_level(level: int) -> int:
        return (level + 1) ** 2 * 100

    @staticmethod
    def calculate_rank(total_xp: int) -> str:
        if total_xp >= 8000:
            return "Legend"
        elif total_xp >= 4000:
            return "Elite"
        elif total_xp >= 1500:
            return "Challenger"
        elif total_xp >= 500:
            return "Explorer"
        return "Rookie"

    # -----------------------------
    # CORE XP ENGINE (FIXED)
    # -----------------------------
    @staticmethod
    def calculate_final_xp(base_xp: int, usage_count: int = 0) -> int:
        if base_xp <= 0:
            return 0

        xp = XPDomain.apply_decay(base_xp, usage_count)
        return max(1, int(xp))

    # -----------------------------
    # EXISTING METHODS (PRESERVED)
    # -----------------------------
    @staticmethod
    def calculate_game_xp(score: int, difficulty: str) -> int:
        base = 10

        if score < 10:
            xp = base
        elif score < 30:
            xp = base * 2.5
        else:
            xp = base * 5

        difficulty_multiplier = {
            "easy": 1.0,
            "medium": 1.3,
            "hard": 1.6
        }.get(difficulty, 1.0)

        return int(xp * difficulty_multiplier)

    @staticmethod
    def calculate_tool_xp(is_first_use: bool, is_repeat: bool) -> int:
        if is_first_use:
            return 10
        if is_repeat:
            return 2
        return 5

    @staticmethod
    def apply_decay(xp: int, usage_count: int) -> int:
        if usage_count > 10:
            return int(xp * 0.2)
        if usage_count > 5:
            return int(xp * 0.5)
        return xp