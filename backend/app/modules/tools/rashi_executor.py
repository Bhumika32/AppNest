from __future__ import annotations
from app.platform.module_executor import ModuleExecutor

"""
app/services/tools/rashi.py

Rashi (Zodiac) service with personality and fortune insights.

Features:
- Zodiac sign determination based on birth details
- Personality insights with roasts
- Career and love recommendations
- Lucky number and color generation
"""

from dataclasses import dataclass
from random import choice


@dataclass
class RashiResult:
    """Structured rashi calculation result."""
    rashi: str
    icon: str
    short_place: str
    birth_time: str
    birth_date: str
    headline: str
    real_fact: str
    roast: str
    strengths: list[str]
    weakness: str
    love_style: str
    career_vibe: str
    lucky_color: str
    lucky_number: int
    vibe_meter: str


class RashiService:
    """Service class for Rashi/Zodiac calculations."""

    RASHI_DATA = [
        {
            "name": "Aries",
            "icon": "♈",
            "real_fact": "Bold, energetic, and action-first personality.",
            "strengths": ["Leader vibes 😤", "Fearless 🔥", "Fast decision-maker ⚡"],
            "weakness": "Anger comes faster than your WiFi 😭",
            "love_style": "Protective + intense, but gets bored fast 💀",
            "career_vibe": "Startup / Sports / Leadership roles 💼🔥",
            "roasts": [
                "You start 10 things… and finish 2 😭🔥",
                "Calm down bro 😭 not every small issue needs war mode ⚔️",
            ],
            "vibe_meter": "🔥🔥🔥🔥⚡ (High Energy)",
        },
        {
            "name": "Taurus",
            "icon": "♉",
            "real_fact": "Stable, loyal, and loves comfort + good food.",
            "strengths": ["Reliable 🤝", "Patient 🧘", "Loyal partner ✅"],
            "weakness": "Change? you treat it like a virus 💀",
            "love_style": "Slow but deeply serious 💍",
            "career_vibe": "Finance / Real estate / Luxury brands 💰",
            "roasts": [
                "You love peace… until someone touches your food 😭🍔",
                "Your stubbornness deserves an award 🏆💀",
            ],
            "vibe_meter": "🍔🧘💎 (Chill but stubborn)",
        },
        {
            "name": "Gemini",
            "icon": "♊",
            "real_fact": "Curious, talkative, and mentally super active.",
            "strengths": ["Fast learner 📚", "Social butterfly 🦋", "Creative mind 🎭"],
            "weakness": "Your brain has 50 tabs open… and none are loading 😭",
            "love_style": "Fun + flirty, commitment scares you sometimes 💀",
            "career_vibe": "Media / Marketing / Content creation 🎥",
            "roasts": [
                "You talk faster than your life decisions 💀",
                "One minute you love it, next minute you ghost it 😭",
            ],
            "vibe_meter": "🧠⚡🗣️ (Hyper Mind)",
        },
        {
            "name": "Cancer",
            "icon": "♋",
            "real_fact": "Emotional, caring, and deeply intuitive.",
            "strengths": ["Caring 🫶", "Protective 🛡️", "Emotionally deep 🌊"],
            "weakness": "Overthinking is your full-time job 😭",
            "love_style": "Loyal + emotional, needs reassurance 🫣",
            "career_vibe": "Counseling / Teaching / Healthcare ❤️",
            "roasts": [
                "You say 'I'm fine'… then overthink for 3 business days 😭",
                "Emotional damage is your daily subscription 💀",
            ],
            "vibe_meter": "🌙🌊🫶 (Soft but strong)",
        },
        {
            "name": "Leo",
            "icon": "♌",
            "real_fact": "Confident, expressive, and loves being noticed.",
            "strengths": ["Confidence 👑", "Charismatic 😎", "Motivator 🔥"],
            "weakness": "Ego bigger than your screen brightness 💀",
            "love_style": "Loyal but wants attention 24/7 😭",
            "career_vibe": "Actor / Leader / Public-facing roles 🎤",
            "roasts": [
                "You don't want attention… you NEED it 😭👑",
                "Even your selfies have confidence 💀🔥",
            ],
            "vibe_meter": "👑🔥✨ (Main Character)",
        },
        {
            "name": "Virgo",
            "icon": "♍",
            "real_fact": "Practical, detail-focused, and perfectionist vibes.",
            "strengths": ["Smart planner 🧠", "Hard worker 💼", "Logical ✅"],
            "weakness": "Perfectionism ruins your sleep schedule 😭",
            "love_style": "Silent love but shows care by fixing things 🛠️",
            "career_vibe": "Engineering / Data / Healthcare 📊",
            "roasts": [
                "You fix everyone's life… except your own 😭",
                "Calm down, it's not NASA 😭🚀",
            ],
            "vibe_meter": "📋🧠✅ (Precision Mode)",
        },
        {
            "name": "Libra",
            "icon": "♎",
            "real_fact": "Balanced, charming, and peace-making nature.",
            "strengths": ["Charming 😌", "Fair ✅", "Good communicator 🗣️"],
            "weakness": "You can't choose one thing in life 😭",
            "love_style": "Romantic but confused 💀",
            "career_vibe": "Law / PR / Design 🎨",
            "roasts": [
                "You can't choose one thing… even in yes/no questions 😭",
                "You'd apologize for breathing 💀",
            ],
            "vibe_meter": "⚖️💬💀 (Chill but indecisive)",
        },
        {
            "name": "Scorpio",
            "icon": "♏",
            "real_fact": "Intense, private, and extremely determined.",
            "strengths": ["Focused 🔥", "Loyal 💯", "Strong mindset 🧠"],
            "weakness": "You forgive… but your memory has lifetime storage 💀",
            "love_style": "Deep love + scary loyalty 😭",
            "career_vibe": "Research / Business / Law enforcement 🕵️",
            "roasts": [
                "You forgive… but your memory has lifetime storage 💀",
                "You act chill… but your mind is plotting 4 storylines 😭",
            ],
            "vibe_meter": "🦂🔥🧠 (Dangerously Deep)",
        },
        {
            "name": "Sagittarius",
            "icon": "♐",
            "real_fact": "Adventurous, honest, and freedom-loving.",
            "strengths": ["Funny 😄", "Explorer 🧭", "Positive vibe ✨"],
            "weakness": "Commitment scares you like exams 😭",
            "love_style": "Loves freedom + fun energy 🏹",
            "career_vibe": "Travel / Teaching / Content creation 🌍",
            "roasts": [
                "You love freedom… and commitment scares you 😭",
                "You speak truth like it's a weapon 💀",
            ],
            "vibe_meter": "🏹🌍😂 (Freedom Mode)",
        },
        {
            "name": "Capricorn",
            "icon": "♑",
            "real_fact": "Disciplined, ambitious, and goal-oriented.",
            "strengths": ["Disciplined 💼", "Goal-focused 🎯", "Reliable ✅"],
            "weakness": "You're so serious even your laugh sounds scheduled 💀",
            "love_style": "Slow but lifetime commitment 😤",
            "career_vibe": "Corporate / Business / Govt jobs 🏢",
            "roasts": [
                "Your idea of fun is finishing tasks early 😭💼",
                "Relax bro… life isn't only deadlines 😭",
            ],
            "vibe_meter": "🎯🏢💼 (Boss Mode)",
        },
        {
            "name": "Aquarius",
            "icon": "♒",
            "real_fact": "Unique thinker, independent, future-focused.",
            "strengths": ["Innovative 🧠", "Independent 😎", "Creative 💡"],
            "weakness": "Emotions? you treat them like optional updates 💀",
            "love_style": "Caring but emotionally confusing 😭",
            "career_vibe": "Tech / Innovation / Research 🤖",
            "roasts": [
                "You're different… and you remind everyone every 5 minutes 😭",
                "Feelings? you uninstall them 💀",
            ],
            "vibe_meter": "🤖⚡💡 (Future Human)",
        },
        {
            "name": "Pisces",
            "icon": "♓",
            "real_fact": "Dreamy, creative, and emotionally deep.",
            "strengths": ["Creative 🎨", "Kind 🫶", "Intuitive 🌙"],
            "weakness": "Reality is your biggest enemy 😭",
            "love_style": "Romantic but loves potential too much 💀",
            "career_vibe": "Art / Music / Psychology 🎶",
            "roasts": [
                "You live in imagination… reality is just a side quest 😭",
                "You fall in love with potential 💀",
            ],
            "vibe_meter": "🌙🎨💀 (Dream Mode)",
        },
    ]

    @staticmethod
    def _short_place(place: str) -> str:
        """Shorten address to top 3 parts."""
        if not place:
            return ""
        parts = [p.strip() for p in place.split(",") if p.strip()]
        return ", ".join(parts[:3])

    @staticmethod
    def _pick_rashi_index(birth_time: str, birth_date: str, lat: str, lon: str) -> int:
        """Determine rashi using birth time, date, and location."""
        hh, mm = 0, 0
        if ":" in birth_time:
            t = birth_time.split(":")
            hh = int(t[0]) if t[0].isdigit() else 0
            mm = int(t[1]) if t[1].isdigit() else 0

        day = 1
        try:
            day = int(birth_date.split("-")[-1])
        except Exception:
            day = 1

        lat_num = int(abs(float(lat)) * 100) if lat else 0
        lon_num = int(abs(float(lon)) * 100) if lon else 0

        score = (hh * 60 + mm) + (day * 13) + lat_num + lon_num
        return score % 12

    @staticmethod
    def calculate(
        *,
        name: str,
        birth_place: str,
        birth_time: str,
        birth_date: str,
        birth_lat: str,
        birth_lon: str,
    ) -> RashiResult:
        """
        Calculate rashi and generate personality insights.

        Args:
            name: Person's name
            birth_place: Place of birth
            birth_time: Time of birth (HH:MM format)
            birth_date: Date of birth (YYYY-MM-DD format)
            birth_lat: Latitude of birth location
            birth_lon: Longitude of birth location

        Returns:
            RashiResult with zodiac sign and personality insights
        """
        name = (name or "Bro").strip().title()
        birth_place = (birth_place or "").strip()

        idx = RashiService._pick_rashi_index(birth_time, birth_date, birth_lat, birth_lon)
        data = RashiService.RASHI_DATA[idx]

        roast_text = data["roasts"][(len(name) + idx) % len(data["roasts"])]
        headline = f"{name}… this is your {data['name']} energy 😭🔥"
        lucky_number = ((idx + len(name)) * 7) % 9 + 1
        lucky_color = ["Red", "Green", "Blue", "Black", "Yellow", "Purple", "White"][idx % 7]
        roast = f"{roast_text} | Born at {birth_time}? Yeah… that explains A LOT 💀"

        return RashiResult(
            rashi=f"{data['name']} {data['icon']}",
            icon=data["icon"],
            short_place=RashiService._short_place(birth_place),
            birth_time=birth_time,
            birth_date=birth_date,
            headline=headline,
            real_fact=data["real_fact"],
            roast=roast,
            strengths=data["strengths"],
            weakness=data["weakness"],
            love_style=data["love_style"],
            career_vibe=data["career_vibe"],
            lucky_color=lucky_color,
            lucky_number=lucky_number,
            vibe_meter=data["vibe_meter"],
        )



from app.platform.module_result import ModuleResult

class RashiExecutor(ModuleExecutor):
    module_key = "RashiGenerator"

    def execute(self, payload: dict, user) -> ModuleResult:
        metadata = payload.get("metadata", {})
        
        # Pull from root or metadata
        name = payload.get("name") or metadata.get("name") or user.username
        birth_place = payload.get("birth_place") or metadata.get("birth_place") or ""
        birth_time = payload.get("birth_time") or metadata.get("birth_time") or "12:00"
        birth_date = payload.get("birth_date") or metadata.get("birth_date") or "2000-01-01"
        birth_lat = str(payload.get("birth_lat") or metadata.get("birth_lat") or "0")
        birth_lon = str(payload.get("birth_lon") or metadata.get("birth_lon") or "0")

        # If frontend already calculated a sign, we can return that or re-calculate
        # For now, we follow the backend logic to ensure consistency
        try:
            result = RashiService.calculate(
                name=name,
                birth_place=birth_place,
                birth_time=birth_time,
                birth_date=birth_date,
                birth_lat=birth_lat,
                birth_lon=birth_lon
            )
            
            return ModuleResult(
                completed=True,
                status="success",
                data={
                    "rashi": result.rashi,
                    "icon": result.icon,
                    "short_place": result.short_place,
                    "birth_time": result.birth_time,
                    "birth_date": result.birth_date,
                    "headline": result.headline,
                    "real_fact": result.real_fact,
                    "roast": result.roast,
                    "strengths": result.strengths,
                    "weakness": result.weakness,
                    "love_style": result.love_style,
                    "career_vibe": result.career_vibe,
                    "lucky_color": result.lucky_color,
                    "lucky_number": result.lucky_number,
                    "vibe_meter": result.vibe_meter
                }
            )
        except Exception as e:
            return ModuleResult(
                completed=False,
                status="error",
                error="INVALID_INPUT",
                message=str(e)
            )
