from __future__ import annotations
from app.platform.module_executor import ModuleExecutor
from datetime import datetime

"""
app/services/tools/age.py

Age Calculator service with zodiac and personality insights.

Features:
- Exact age calculation (years, months, days)
- Life statistics (days, weeks, hours lived)
- Birthday countdown
- Zodiac sign calculation
- Fun and roast messaging modes
"""

from dataclasses import dataclass
from datetime import date
from random import choice


@dataclass
class AgeResult:
    """Structured age calculation result."""
    name: str
    dob: date
    years: int
    months: int
    days: int
    total_days_lived: int
    total_weeks_lived: int
    total_hours_lived: int
    days_until_birthday: int
    next_birthday_date: str
    born_day: str
    zodiac: str
    stage: str
    message: str
    fun_fact: str


class AgeService:
    """Service class for age calculations and personality insights."""

    @staticmethod
    def _calculate_exact_age(dob: date, today: date) -> tuple[int, int, int]:
        """Calculate exact age in years, months, days."""
        years = today.year - dob.year
        months = today.month - dob.month
        days = today.day - dob.day

        if days < 0:
            prev_month = today.month - 1 or 12
            prev_year = today.year if today.month != 1 else today.year - 1
            first_today_month = date(today.year, today.month, 1)
            first_prev_month = date(prev_year, prev_month, 1)
            last_day_prev_month = (first_today_month - first_prev_month).days
            days += last_day_prev_month
            months -= 1

        if months < 0:
            months += 12
            years -= 1

        return years, months, days

    @staticmethod
    def _next_birthday_date(dob: date, today: date) -> date:
        """Calculate next birthday date."""
        next_bday = date(today.year, dob.month, dob.day)
        if next_bday < today:
            next_bday = date(today.year + 1, dob.month, dob.day)
        return next_bday

    @staticmethod
    def _born_day(dob: date) -> str:
        """Get day of week for birth date."""
        return dob.strftime("%A")

    @staticmethod
    def _zodiac_sign(dob: date) -> str:
        """Calculate zodiac sign from birth date."""
        day = dob.day
        month = dob.month

        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries ♈"
        if (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Taurus ♉"
        if (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Gemini ♊"
        if (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Cancer ♋"
        if (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Leo ♌"
        if (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Virgo ♍"
        if (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Libra ♎"
        if (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Scorpio ♏"
        if (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Sagittarius ♐"
        if (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Capricorn ♑"
        if (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Aquarius ♒"
        return "Pisces ♓"

    @staticmethod
    def _birthday_hype(days_until_birthday: int) -> str:
        """Add excitement text for upcoming birthdays."""
        if days_until_birthday == 0:
            return " 🎉 HAPPY BIRTHDAY!! Today you're the main character 🥳"
        if days_until_birthday <= 7:
            return " 🎂 Birthday is super close! Party mode loading 😄"
        if days_until_birthday <= 30:
            return " 🎉 Birthday soon… start acting surprised already 😭"
        return ""

    @staticmethod
    def _fun_fact(total_days: int, total_hours: int, fun_mode: bool, roast_mode: bool) -> str:
        """Generate a fun fact about the person's age."""
        if not fun_mode:
            return "Your age stats are calculated accurately ✅"

        if roast_mode:
            roast_facts = [
                f"You've survived {total_days:,} days. Respect ✅",
                f"That's ~{total_hours:,} hours of life… and still no 'pause button' 😭",
                "Your sleep schedule deserves a documentary 😅",
            ]
            return choice(roast_facts)

        fun_facts = [
            f"You've lived ~{total_hours:,} hours. That's a LOT of scrolling 😭",
            f"You survived {total_days:,} days. Hero energy ✅",
            "You're basically a walking memory card full of experiences 😄",
        ]
        return choice(fun_facts)

    @staticmethod
    def _personal_roast_bonus(name: str, years: int) -> str:
        """Generate a personalized playful roast."""
        name = name.strip()
        patterns = [
            f"{name}, your maturity is updating slower than Windows 😭",
            f"{name}, your age says adult… your decisions say 'trial version' 😅",
            f"{name}, you're aging perfectly… like a phone battery after 2 years 💀",
        ]

        if years >= 25:
            patterns.append(f"{name}, now happiness means 8 hours sleep + no back pain 😭")
        if years >= 30:
            patterns.append(f"{name}, you don't chase dreams now… you chase discounts 😭💸")

        return choice(patterns)

    @staticmethod
    def _stage_and_message(
        *, years: int, name: str, fun_mode: bool, roast_mode: bool, days_until_birthday: int
    ) -> tuple[str, str]:
        """Generate life stage and personalized message."""
        name = name.strip()

        if roast_mode:
            fun_mode = True

        if not fun_mode:
            return "Normal ✅", f"{name}, your age details are calculated successfully ✅"

        if not roast_mode:
            if years < 13:
                stage = "Kid Mode 🧸"
                msg_pool = [
                    f"{name}, you're in Kid Mode 🧸. Enjoy life, no EMIs yet 😄",
                    f"{name}, school + snacks + sleep = perfect lifestyle 😄",
                ]
            elif 13 <= years <= 17:
                stage = "Teen Mode ⚡"
                msg_pool = [
                    f"{name}, Teen Mode ⚡ activated. Mood swings included free 😭",
                    f"{name}, teen life: full confidence, zero experience 😅",
                ]
            elif 18 <= years <= 24:
                stage = "Young Adult 🎓"
                msg_pool = [
                    f"{name}, you're grown… but still panic when phone battery hits 20% 😭",
                    f"{name}, adult on paper… still buffering mentally 😅",
                ]
            elif 25 <= years <= 30:
                stage = "Real Adult 💼"
                msg_pool = [
                    f"{name}, welcome to adulthood 💼. Fun requires planning now 😭",
                    f"{name}, now you say 'let's meet soon' and nobody meets 😭",
                ]
            elif 31 <= years <= 40:
                stage = "Senior Youth 😎"
                msg_pool = [
                    f"{name}, senior youth 😎. Responsibilities unlocked… no uninstall option.",
                    f"{name}, you now enjoy cancelled plans… that's peace 😌",
                ]
            elif 41 <= years <= 60:
                stage = "Legend Mode 🏆"
                msg_pool = [
                    f"{name}, Legend Mode 🏆. You've survived enough to give advice now 😄",
                    f"{name}, life experience level: MAX ✅",
                ]
            else:
                stage = "Ultra Legend 👑"
                msg_pool = [
                    f"{name}, Ultra Legend 👑. You're not aging… you're upgrading.",
                    f"{name}, respect 👑. You're the final boss of experience.",
                ]

            base_msg = choice(msg_pool)
            return stage, base_msg + AgeService._birthday_hype(days_until_birthday)

        # Roast Mode
        if years < 13:
            stage = "Kid Mode 🧸 (Roast)"
            msg_pool = [
                f"{name}, you're a kid 🧸… enjoy it before life adds taxes 😭",
                f"{name}, you still have free time… this is rare 😭",
            ]
        elif 13 <= years <= 17:
            stage = "Teen Mode ⚡ (Roast)"
            msg_pool = [
                f"{name}, teen mode ⚡… emotions change faster than reels 😭",
                f"{name}, confidence 100%… knowledge still downloading 😅",
            ]
        elif 18 <= years <= 24:
            stage = "Young Adult 🎓 (Roast)"
            msg_pool = [
                f"{name}, adulthood unlocked 😭… responsibilities included free.",
                f"{name}, you're adult now… but still asking 'what is my purpose?' daily 😭",
            ]
        elif 25 <= years <= 30:
            stage = "Real Adult 💼 (Roast)"
            msg_pool = [
                f"{name}, welcome to 25+ 💼… where fun needs scheduling 😭",
                f"{name}, you don't party anymore… you calculate recovery time 💀",
            ]
        elif 31 <= years <= 40:
            stage = "Senior Youth 😎 (Roast)"
            msg_pool = [
                f"{name}, you now make sounds while sitting down 😭 welcome.",
                f"{name}, hobbies now: sleep + comfort 😅",
            ]
        elif 41 <= years <= 60:
            stage = "Legend Mode 🏆 (Roast)"
            msg_pool = [
                f"{name}, you've seen enough life updates to ignore new ones 🏆😄",
                f"{name}, you're the reason the word 'experience' exists 😌",
            ]
        else:
            stage = "Ultra Legend 👑 (Roast)"
            msg_pool = [
                f"{name}, Ultra Legend 👑… age is scared of you 😭👑",
                f"{name}, you're basically WiFi for wisdom now 😄",
            ]

        base_msg = choice(msg_pool)
        personal_bonus = AgeService._personal_roast_bonus(name, years)
        full_msg = base_msg + " | " + personal_bonus + AgeService._birthday_hype(days_until_birthday)

        return stage, full_msg

    @staticmethod
    def calculate(
        name: str, dob: date, fun_mode: bool = True, roast_mode: bool = False
    ) -> AgeResult:
        """
        Calculate age and generate personality insights.

        Args:
            name: Person's name
            dob: Date of birth
            fun_mode: Enable fun personality messaging
            roast_mode: Enable playful roast messages

        Returns:
            AgeResult with all calculated values
        """
        today = date.today()

        if dob > today:
            raise ValueError("Date of birth cannot be in the future")

        years, months, days = AgeService._calculate_exact_age(dob, today)
        total_days_lived = (today - dob).days
        total_weeks_lived = total_days_lived // 7
        total_hours_lived = total_days_lived * 24

        next_bday = AgeService._next_birthday_date(dob, today)
        days_until_birthday = (next_bday - today).days

        stage, message = AgeService._stage_and_message(
            years=years,
            name=name,
            fun_mode=fun_mode,
            roast_mode=roast_mode,
            days_until_birthday=days_until_birthday,
        )

        fun_fact = AgeService._fun_fact(
            total_days=total_days_lived,
            total_hours=total_hours_lived,
            fun_mode=fun_mode,
            roast_mode=roast_mode,
        )

        return AgeResult(
            name=name.strip(),
            dob=dob,
            years=years,
            months=months,
            days=days,
            total_days_lived=total_days_lived,
            total_weeks_lived=total_weeks_lived,
            total_hours_lived=total_hours_lived,
            days_until_birthday=days_until_birthday,
            next_birthday_date=next_bday.strftime("%d %b %Y"),
            born_day=AgeService._born_day(dob),
            zodiac=AgeService._zodiac_sign(dob),
            stage=stage,
            message=message,
            fun_fact=fun_fact,
        )



from app.platform.module_result import ModuleResult

import logging
logger = logging.getLogger(__name__)

class AgeExecutor(ModuleExecutor):
    module_key = "AgeCalculator"

    def execute(self, payload: dict, user) -> ModuleResult:
        logger.info(f"Executing Age Calculator for user: {user.id}")
        metadata = payload.get("metadata", {})
        dob_str = payload.get("dob") or metadata.get("dob")
        name = payload.get("name") or metadata.get("name") or user.username
        
        if not dob_str:
            return ModuleResult(
                completed=False,
                status="error",
                error="INVALID_INPUT",
                message="Date of birth (dob) is required in format YYYY-MM-DD"
            )
            
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            return ModuleResult(
                completed=False,
                status="error",
                error="INVALID_INPUT",
                message="Invalid date format. Use YYYY-MM-DD"
            )
        fun_mode = payload.get("fun_mode", True)
        roast_mode = payload.get("roast_mode", False)

        try:
            result = AgeService.calculate(
                name=name, 
                dob=dob, 
                fun_mode=fun_mode, 
                roast_mode=roast_mode
            )
            return ModuleResult(
                completed=True,
                status="success",
                data={
                    "name": result.name,
                    "dob": result.dob.isoformat(),
                    "years": result.years,
                    "months": result.months,
                    "days": result.days,
                    "total_days_lived": result.total_days_lived,
                    "total_weeks_lived": result.total_weeks_lived,
                    "total_hours_lived": result.total_hours_lived,
                    "days_until_birthday": result.days_until_birthday,
                    "next_birthday_date": result.next_birthday_date,
                    "born_day": result.born_day,
                    "zodiac": result.zodiac,
                    "stage": result.stage,
                    "message": result.message,
                    "fun_fact": result.fun_fact
                }
            )
        except ValueError as e:
            return ModuleResult(
                completed=False,
                status="error",
                error="INVALID_INPUT",
                message=str(e)
            )
