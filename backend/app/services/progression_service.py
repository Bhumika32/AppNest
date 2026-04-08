# app/services/progression_service.py

from typing import Dict
import logging

from sqlalchemy.orm import Session

from app.domain.xp_domain import XPDomain
from app.domain.event_bus import EventBus, Events

logger = logging.getLogger(__name__)


class ProgressionService:

    def __init__(self, progression_repo, xp_repo):
        self.progression_repo = progression_repo
        self.xp_repo = xp_repo

    def award_xp(
        self,
        db: Session,
        user_id: int,
        module_id: int,
        base_xp: int,
        unique_hash: str,
    ) -> Dict:

        try:

        # -----------------------------
        # TRANSACTION
        # -----------------------------
        # with db.begin():

            # -----------------------------
            # 1. DUPLICATE CHECK
            # -----------------------------
            if self.xp_repo.exists_hash(db, unique_hash):
                return {
                    "status": "blocked",
                    "reason": "duplicate_attempt"
                }

            # -----------------------------
            # 2. DAILY LIMIT
            # -----------------------------
            today_xp = self.xp_repo.get_today_xp(db, user_id)

            if today_xp >= 200:
                return {
                    "status": "blocked",
                    "reason": "daily_limit_reached"
                }

            # -----------------------------
            # 3. MODULE LIMIT
            # -----------------------------
            module_xp = self.xp_repo.get_module_xp_today(
                db,
                user_id,
                module_id
            )

            if module_xp >= 50:
                return {
                    "status": "blocked",
                    "reason": "module_limit_reached"
                }

            # -----------------------------
            # 4. LOAD PROGRESSION
            # -----------------------------
            progression = self.progression_repo.get_by_user_id(db, user_id)

            if not progression:
                progression = self.progression_repo.create(
                    db,
                    {
                        "user_id": user_id,
                        "total_xp": 0,
                        "level": 1,
                        "rank_title": "Rookie"
                    }
                )

            prev_level = progression.level
            prev_rank = progression.rank_title

            # -----------------------------
            # 5. DOMAIN XP CALCULATION
            # -----------------------------
            xp = XPDomain.calculate_final_xp(base_xp)

            # -----------------------------
            # 6. CREATE XP TRANSACTION
            # -----------------------------
            self.xp_repo.create(
                db,
                {
                    "user_id": user_id,
                    "module_id": module_id,
                    "xp_awarded": xp,
                    "unique_hash": unique_hash,
                    "source": "module",
                    "reason": "module_completion"
                }
            )

            # -----------------------------
            # 7. UPDATE PROGRESSION
            # -----------------------------
            new_total = progression.total_xp + xp

            new_level = XPDomain.calculate_level(new_total)
            new_rank = XPDomain.calculate_rank(new_total)

            self.progression_repo.update(
                db,
                progression,
                {
                    "total_xp": new_total,
                    "level": new_level,
                    "rank_title": new_rank
                }
            )

        # -------------------------------------------------
        # IMPORTANT: EVENTS MUST FIRE AFTER TRANSACTION
        # -------------------------------------------------

            # XP GRANTED EVENT
            EventBus.publish(
                Events.XP_GRANTED,
                {
                    "db": db,
                    "user_id": user_id,
                    "xp_awarded": xp,
                    "module_id": module_id
                }
            )

            # LEVEL UP EVENT
            if new_level > prev_level:
                EventBus.publish(
                    Events.LEVEL_UP,
                    {
                        "db": db,
                        "user_id": user_id,
                        "new_level": new_level
                    }
                )

            # -----------------------------
            # RETURN RESULT
            # -----------------------------
            return {
                "status": "success",
                "xp_awarded": xp,
                "total_xp": new_total,
                "level": new_level,
                "leveled_up": new_level > prev_level,
                "rank_changed": new_rank != prev_rank,
                "rank_title": new_rank
            }

        except Exception:
            logger.exception("XP award failed")
            raise
# # app/services/progression_service.py
# from typing import Optional, Dict
# import logging

# from sqlalchemy.orm import Session

# from app.domain.xp_domain import XPDomain

# logger = logging.getLogger(__name__)

# class ProgressionService:

#     def __init__(self, progression_repo, xp_repo):
#         self.progression_repo = progression_repo
#         self.xp_repo = xp_repo

#     def award_xp(
#         self,
#         db: Session,
#         user_id: int,
#         module_key: str,
#         base_xp: int,
#         unique_hash: str,
#     ) -> Dict:

#         try:
#             with db.begin():

#                 # -----------------------------
#                 # 1. DUPLICATE CHECK
#                 # -----------------------------
#                 if self.xp_repo.exists_hash(db, unique_hash):
#                     return {
#                         "status": "blocked",
#                         "reason": "duplicate_attempt"
#                     }

#                 # -----------------------------
#                 # 2. DAILY LIMIT
#                 # -----------------------------
#                 today_xp = self.xp_repo.get_today_xp(db, user_id)
#                 if today_xp >= 200:
#                     return {
#                         "status": "blocked",
#                         "reason": "daily_limit_reached"
#                     }

#                 # -----------------------------
#                 # 3. MODULE LIMIT
#                 # -----------------------------
#                 module_xp = self.xp_repo.get_module_xp_today(
#                     db, user_id, module_key
#                 )

#                 if module_xp >= 50:
#                     return {
#                         "status": "blocked",
#                         "reason": "module_limit_reached"
#                     }

#                 # -----------------------------
#                 # 4. LOAD PROGRESSION
#                 # -----------------------------
#                 progression = self.progression_repo.get_by_user_id(db, user_id)

#                 if not progression:
#                     progression = self.progression_repo.create(db, {
#                         "user_id": user_id,
#                         "total_xp": 0,
#                         "level": 1,
#                         "rank_title": "Rookie"
#                     })

#                 prev_level = progression.level
#                 prev_rank = progression.rank_title

#                 # -----------------------------
#                 # 5. DOMAIN CALCULATION
#                 # -----------------------------
#                 xp = XPDomain.calculate_final_xp(base_xp)

#                 # -----------------------------
#                 # 6. CREATE TRANSACTION
#                 # -----------------------------
#                 self.xp_repo.create(db, {
#                     "user_id": user_id,
#                     "module_key": module_key,
#                     "xp_awarded": xp,
#                     "unique_hash": unique_hash,
#                 })

#                 # -----------------------------
#                 # 7. UPDATE PROGRESSION
#                 # -----------------------------
#                 new_total = progression.total_xp + xp

#                 new_level = XPDomain.calculate_level(new_total)
#                 new_rank = XPDomain.calculate_rank(new_total)

#                 self.progression_repo.update(db, progression, {
#                     "total_xp": new_total,
#                     "level": new_level,
#                     "rank_title": new_rank
#                 })

#             # -----------------------------
#             # 8. EVENT OUTPUT (IMPORTANT)
#             # -----------------------------
#             return {
#                 "status": "success",
#                 "xp_awarded": xp,
#                 "total_xp": new_total,
#                 "level": new_level,
#                 "leveled_up": new_level > prev_level,
#                 "rank_changed": new_rank != prev_rank,
#                 "rank_title": new_rank,

#                 # FUTURE PIPELINE HOOKS
#                 "events": {
#                     "level_up": new_level > prev_level,
#                     "rank_up": new_rank != prev_rank,
#                 }
#             }

#         except Exception:
#             logger.exception("XP award failed")
#             raise