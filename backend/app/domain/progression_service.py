# File: backend/app/domain/progression_service.py
# -----------------------------------------------------------------------------
# Handles XP rewards, leveling, and player progression logic for AppNest.
#
# Responsibilities:
# - Calculate XP rewards
# - Record XP transactions (ledger)
# - Update user progression
# - Determine level-ups
# - Assign rank titles
#
# Architecture Notes:
# - XPTransaction acts as an immutable XP ledger
# - UserProgression stores the current progression state
# - Level thresholds are absolute total XP values
# -----------------------------------------------------------------------------

from sqlalchemy.orm import Session
from app.models.user_progression import UserProgression
from app.models.xp_transaction import XPTransaction


class ProgressionService:

    # -------------------------------------------------------------------------
    # RANK SYSTEM
    # -------------------------------------------------------------------------
    RANKS = [
        (1, "Apprentice"),
        (5, "Arcane Player"),
        (10, "Battle Adept"),
        (25, "Neon Warrior"),
        (50, "Realm Guardian"),
        (100, "Anime Legend")
    ]

    # -------------------------------------------------------------------------
    # DIFFICULTY MULTIPLIERS
    # -------------------------------------------------------------------------
    DIFFICULTY_MULTIPLIER = {
        "EASY": 1.0,
        "MEDIUM": 1.5,
        "HARD": 2.2
    }

    # -------------------------------------------------------------------------
    # GET USER PROGRESSION
    # -------------------------------------------------------------------------
    @staticmethod
    def get_user_progression(db: Session, user_id: int) -> UserProgression:
        progression = db.query(UserProgression).filter_by(user_id=user_id).first()
        if not progression:
            progression = UserProgression(user_id=user_id)
            db.add(progression)
            db.commit()

        return progression

    # -------------------------------------------------------------------------
    # TOTAL XP REQUIRED FOR A LEVEL
    # -------------------------------------------------------------------------
    @staticmethod
    def calculate_total_xp_for_level(level: int) -> int:
        """
        Returns cumulative XP required to reach a given level from level 1.
        Formula: level takes (100 + current_level * 20) XP to complete.
        """
        if level <= 1:
            return 0
        total = 0
        for i in range(1, level):
            total += 100 + (i * 20)
        return total

    # -------------------------------------------------------------------------
    # RANK TITLE
    # -------------------------------------------------------------------------
    @staticmethod
    def get_rank_title(level: int) -> str:

        current_rank = "Apprentice"

        for rank_level, title in sorted(ProgressionService.RANKS):
            if level >= rank_level:
                current_rank = title
            else:
                break

        return current_rank

    # -------------------------------------------------------------------------
    # AWARD XP
    # -------------------------------------------------------------------------
    @staticmethod
    def award_xp(
        db: Session,
        user_id: int,
        module_id: int,
        base_reward: int,
        difficulty: str = "EASY",
        performance_bonus: int = 0,
        streak_bonus: int = 0,
        reason: str = "Module Completed"
    ) -> dict:

        multiplier = ProgressionService.DIFFICULTY_MULTIPLIER.get(
            difficulty.upper(),
            1.0
        )

        total_xp_awarded = int(
            (base_reward * multiplier) +
            performance_bonus +
            streak_bonus
        )

        progression = ProgressionService.get_user_progression(user_id)

        # -------------------------------------------------------------
        # RECORD XP TRANSACTION (ledger)
        # -------------------------------------------------------------
        transaction = XPTransaction(
            user_id=user_id,
            module_id=module_id,
            xp_awarded=total_xp_awarded,
            difficulty=difficulty,
            reason=reason
        )

        db.add(transaction)

        # -------------------------------------------------------------
        # UPDATE TOTAL XP
        # -------------------------------------------------------------
        progression.total_xp += total_xp_awarded

        old_level = progression.level
        leveled_up = False

        # -------------------------------------------------------------
        # LEVEL CALCULATION
        # -------------------------------------------------------------
        while progression.total_xp >= ProgressionService.calculate_total_xp_for_level(
            progression.level + 1
        ):
            progression.level += 1
            leveled_up = True

        if leveled_up:
            progression.rank_title = ProgressionService.get_rank_title(
                progression.level
            )

        db.commit()
        
        # Calculate full stats for frontend
        xp_required_for_next = 100 + (progression.level * 20)
        base_xp_for_current_level = ProgressionService.calculate_total_xp_for_level(progression.level)
        xp_in_current_level = progression.total_xp - base_xp_for_current_level
        
        # ensure progress percent does not exceed 100% (it shouldn't but just in case)
        progress_percent = int((xp_in_current_level / xp_required_for_next) * 100)
        progress_percent = min(100, max(0, progress_percent))

        # Emit milestone event if applicable
        if leveled_up and progression.level in [10, 25, 50, 100]:
            from app.domain.event_bus import EventBus
            EventBus.publish("LEVEL_MILESTONE", {
                "user_id": user_id,
                "level": progression.level,
                "rank": progression.rank_title
            })

        return {
            "xp_awarded": total_xp_awarded,
            "total_xp": progression.total_xp,
            "level": progression.level,
            "xp_in_current_level": xp_in_current_level,
            "xp_required_for_next_level": xp_required_for_next,
            "progress_percent": progress_percent,
            "leveled_up": leveled_up,
            "rank_title": progression.rank_title
        }

# from app.core.extensions import db
# from app.models.user_progression import UserProgression
# from app.models.xp_transaction import XPTransaction
# import math

# class ProgressionService:
#     RANKS = [
#         (1, "Apprentice"),
#         (5, "Arcane Player"),
#         (10, "Battle Adept"),
#         (25, "Neon Warrior"),
#         (50, "Realm Guardian"),
#         (100, "Anime Legend")
#     ]

#     DIFFICULTY_MULTIPLIER = {
#         'EASY': 1.0,
#         'MEDIUM': 1.5,
#         'HARD': 2.2
#     }

#     @staticmethod
#     def get_user_progression(user_id: int) -> UserProgression:
#         progression = UserProgression.query.filter_by(user_id=user_id).first()
#         if not progression:
#             progression = UserProgression(user_id=user_id)
#             db.session.add(progression)
#             db.session.commit()
#         return progression

#     @staticmethod
#     def calculate_xp_required(level: int) -> int:
#         return int(100 + (level ** 1.5) * 40)

#     @staticmethod
#     def get_rank_title(level: int) -> str:
#         current_rank = "Apprentice"
#         for rank_level, title in sorted(ProgressionService.RANKS, key=lambda x: x[0]):
#             if level >= rank_level:
#                 current_rank = title
#             else:
#                 break
#         return current_rank

#     @staticmethod
#     def award_xp(user_id: int, module_id: int, base_reward: int, difficulty: str = 'EASY', performance_bonus: int = 0, streak_bonus: int = 0, reason: str = 'Module Completed') -> dict:
#         multiplier = ProgressionService.DIFFICULTY_MULTIPLIER.get(difficulty.upper(), 1.0)
#         total_xp_awarded = int((base_reward * multiplier) + performance_bonus + streak_bonus)

#         progression = ProgressionService.get_user_progression(user_id)
        
#         # Create XP Transaction
#         transaction = XPTransaction(
#             user_id=user_id,
#             module_id=module_id,
#             xp_awarded=total_xp_awarded,
#             difficulty=difficulty,
#             reason=reason
#         )
#         db.session.add(transaction)

#         # Update progression
#         progression.total_xp += total_xp_awarded
        
#         # Fix: Level up calculation should be purely deterministic based on absolute total_xp
#         # We determine the maximum level achievable with current total_xp.
#         leveled_up = False
#         old_level = progression.level
        
#         while True:
#             xp_required = ProgressionService.calculate_xp_required(progression.level)
#             # Level requirement typically refers to the total accumulated XP needed for the next level,
#             # but if it was meant to be relative to the previous level, we sum up requirements or treat requirement as absolute threshold.
#             # Assuming `xp_required` returned from calculate_xp_required is the ABSOLUTE total XP needed to reach next level:
#             if progression.total_xp >= xp_required:
#                 leveled_up = True
#                 progression.level += 1
#             else:
#                 break

#         if leveled_up:
#             progression.rank_title = ProgressionService.get_rank_title(progression.level)
            
#         db.session.commit()

#         return {
#             "xp_awarded": total_xp_awarded,
#             "new_total": progression.total_xp,
#             "level": progression.level,
#             "leveled_up": leveled_up,
#             "rank_title": progression.rank_title,
#             "xp_required_next_level": ProgressionService.calculate_xp_required(progression.level)
#         }
