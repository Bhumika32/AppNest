"""
app/tools/moodfix/service.py

MoodFix Ultimate Service (Roast + Motivation + Action Plan)

✅ Fresh output every time (session seed)
✅ Mood + intensity + target support
✅ Output format:
   - 3-4 savage lines
   - Action plan bullets (3)
   - ONE task (5 mins)
✅ Mandatory name for personal roast
✅ Optional Gemini personalized chat reply (fallback works)
✅ Streak intro lines for addictiveness
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import md5
import os
import time
from random import choice

from app.tools.moodfix.gemini_client import GeminiClient


@dataclass
class MoodFixResult:
    name: str
    mood: str
    mood_label: str
    pack_text: str
    questions: list[str]


class MoodFixService:
    MOODS = {
        "sad": "😭 Sad",
        "angry": "😡 Angry",
        "lazy": "😴 Lazy",
        "stress": "😵 Stress",
        "motivation": "💪 Motivation",
        "confidence": "😎 Confidence",
    }

    INTENSITIES = {
        "soft": "😇 Soft Roast (friendly)",
        "medium": "😈 Medium Roast (spicy)",
        "savage": "💀 Savage Roast (no mercy)",
    }

    QUESTIONS = {
        "sad": [
            "What made you sad today?",
            "Do you want comfort 😭 or solution ✅?",
        ],
        "angry": [
            "Who triggered you? 😈",
            "You want revenge 😈 or peace 🧘?",
        ],
        "lazy": [
            "What task are you avoiding right now?",
            "What’s the REAL reason: fear 😬 or distraction 📱?",
        ],
        "stress": [
            "What’s stressing you the most?",
            "Deadline 🕒 or overthinking 🧠?",
        ],
        "motivation": [
            "What goal do you want to attack today?",
            "What’s blocking you right now?",
        ],
        "confidence": [
            "Where do you want to feel confident?",
            "What’s stopping you from acting bold today?",
        ],
    }

    POOL = {
        "angry": {
            "roast": [
                "your anger is valid… your reaction is embarrassing 💀",
                "you act like a warrior but fold like a cheap chair 😭",
                "you don’t need revenge, you need self-control 😈",
                "you’re one sentence away from starting WW3 😭⚔️",
                "you’re angry like it’s a sport… and you’re still losing 💀",
            ],
            "action_plan": [
                "Don’t reply fast.",
                "Don’t act loud.",
                "Act smart.",
                "Win silently.",
            ],
            "task": [
                "Write the angry msg… then DELETE it. Power move ✅",
                "Do 20 push-ups OR 30 squats. Burn it out 🔥",
                "Take 10 deep breaths. Count slowly. Don’t rush it ✅",
            ],
        },
        "lazy": {
            "roast": [
                "your bed has more pull than your goals 😭🛌",
                "you’re tired of life… but you did nothing today 💀",
                "your motivation is missing person 🚨",
                "you say you want success but act like you want sleep 😈",
            ],
            "action_plan": [
                "Pick ONE task.",
                "Do 5 minutes only.",
                "Repeat until momentum shows up.",
            ],
            "task": [
                "Open your task list. Pick 1 thing. Do it for 5 mins only.",
                "Clean your desk for 3 mins. Reset environment = reset brain ✅",
                "Put phone away for 10 mins and start anything.",
            ],
        },
        "sad": {
            "roast": [
                "you’re sad like a WiFi signal at 1 bar 😭📶",
                "you’re not broken… you’re just dramatic today 😈",
                "you’re crying like it’s a paid internship 💀",
                "your mood is giving ‘low battery’ vibes 😭🔋",
            ],
            "action_plan": [
                "Stop scrolling pain.",
                "Do one small win.",
                "Reset your mind.",
            ],
            "task": [
                "Drink water + wash your face. Then sit straight for 60 seconds.",
                "Go outside for 5 mins. No phone. Just air + silence ✅",
                "Write 3 lines: what hurt, what you learned, what you’ll do next.",
            ],
        },
        "stress": {
            "roast": [
                "your brain is running 100 tabs and none are productive 💀",
                "you’re stressed like panic is a personality 😭",
                "you’re drowning in tasks you didn’t even start 😈",
                "your stress is loud but your execution is silent 💀",
            ],
            "action_plan": [
                "Write 3 tasks ONLY.",
                "Do the smallest first step.",
                "Stop overthinking like it’s a job.",
            ],
            "task": [
                "Write 3 tasks only: Now / Next / Later ✅",
                "Do 2 mins deep breathing: in 4, hold 2, out 6.",
                "Take a 5-min walk. No phone. Just breathing.",
            ],
        },
        "motivation": {
            "roast": [
                "motivation without action is fantasy 💀",
                "stop talking big and moving small 😈",
                "your goals don’t care about your mood 😤",
                "don’t waste this energy… it expires fast ⚡",
            ],
            "action_plan": [
                "Pick the hardest task.",
                "Start 5 mins now.",
                "Don’t negotiate with your excuses.",
            ],
            "task": [
                "Pick 1 hardest task and start for 5 mins. No negotiation ✅",
                "Set timer 10 mins and sprint one work session 🔥",
                "Write your goal in 1 line. Then do 1 action for it.",
            ],
        },
        "confidence": {
            "roast": [
                "confidence looks good… but results look better 💀",
                "stop seeking validation like it pays rent 😈",
                "your vibe is strong… now make your work stronger 😤",
                "you don’t need permission to win 😎🔥",
            ],
            "action_plan": [
                "Act before fear speaks.",
                "Show up like a pro.",
                "Prove it with reps.",
            ],
            "task": [
                "Apply to 1 opportunity today. No overthinking ✅",
                "Stand straight, fix posture, and speak one bold sentence out loud.",
                "Message someone you avoided. Be direct + polite.",
            ],
        },
    }

    @staticmethod
    def make_session_seed() -> str:
        return str(int(time.time() * 1000))

    @staticmethod
    def _stable_choice(items: list[str], seed_text: str) -> str:
        h = md5(seed_text.encode("utf-8")).hexdigest()
        idx = int(h[:8], 16) % len(items)
        return items[idx]

    @staticmethod
    def get_intro_line(streak_count: int) -> str:
        """
        ✅ Adds addictive "streak bonus" messages
        """
        if streak_count <= 1:
            return "😈 MoodFix dropped. If you ignore this, your future self will slap you 💀✅"

        # Rotating streak roasts
        streak_lines = [
            f"🔥 Streak {streak_count}… okok you’re improving 😈",
            f"🔥 Streak {streak_count}… who are you and what did you do with the old you? 💀",
            f"🔥 Streak {streak_count}… don’t stop now, hero. Keep going 😈⚡",
            f"🔥 Streak {streak_count}… discipline is loading… don’t ruin it 😭✅",
        ]
        return choice(streak_lines)

    @staticmethod
    def generate(
        *,
        mood: str,
        name: str,
        session_seed: str,
        intensity: str = "medium",
        target: str = "",
    ) -> MoodFixResult:
        mood = (mood or "").strip().lower()
        intensity = (intensity or "medium").strip().lower()

        if mood not in MoodFixService.MOODS:
            raise ValueError("Invalid mood selected.")

        if intensity not in MoodFixService.INTENSITIES:
            intensity = "medium"

        clean_name = (name or "").strip().title()
        if not clean_name:
            clean_name = "Bro"

        mood_label = MoodFixService.MOODS[mood]
        pool = MoodFixService.POOL[mood]

        seed_text = f"{clean_name}|{mood}|{intensity}|{target}|{session_seed}"

        # ✅ 3-4 savage lines
        roast_lines = []
        for i in range(4):
            roast_lines.append(
                MoodFixService._stable_choice(pool["roast"], seed_text + f"|roast{i}")
            )

        # reduce based on intensity
        if intensity == "soft":
            roast_lines = roast_lines[:3]
        elif intensity == "savage":
            roast_lines = roast_lines[:4]
        else:
            roast_lines = roast_lines[:3]

        # personalize with target
        target_text = f" (Target: {target})" if target else ""

        roast_formatted = "\n".join(
            [f"• {clean_name}… {line}{target_text if idx == 0 and target else ''}"
             for idx, line in enumerate(roast_lines)]
        )

        # ✅ Action plan (3 bullets)
        plan = pool["action_plan"]
        plan_lines = []
        for j in range(3):
            plan_lines.append(MoodFixService._stable_choice(plan, seed_text + f"|plan{j}"))

        plan_formatted = "\n".join([f"• {x}" for x in plan_lines])

        # ✅ Task
        task = MoodFixService._stable_choice(pool["task"], seed_text + "|task")

        pack_text = (
            f"😈 Savage Roast:\n"
            f"{roast_formatted}\n\n"
            f"✅ Action Plan:\n"
            f"{plan_formatted}\n\n"
            f"🎯 ONE Task (5 mins):\n"
            f"• {task}"
        )

        return MoodFixResult(
            name=clean_name,
            mood=mood,
            mood_label=mood_label,
            pack_text=pack_text,
            questions=MoodFixService.QUESTIONS.get(mood, []),
        )

    @staticmethod
    def generate_personalized_reply(
        *,
        name: str,
        mood: str,
        mood_label: str,
        qna: list[str],
        intensity: str = "medium",
        target: str = "",
    ) -> str:
        """
        ✅ Uses Gemini if API key works.
        ✅ Else fallback.
        """
        name = (name or "Bro").strip().title()
        a1 = qna[0] if len(qna) > 0 else ""
        a2 = qna[1] if len(qna) > 1 else ""

        gemini_key = os.getenv("GEMINI_API_KEY")

        prompt = f"""
You are MoodFix 😈 — the best savage but helpful roaster on Earth.
User selected mood: {mood_label}
User name: {name}
Roast intensity: {intensity}
Optional target/trigger: {target}

User answers:
1) {a1}
2) {a2}

RULES:
- Give 4 savage lines (personal, funny, not hateful).
- Then Action Plan in 3 bullets.
- Then ONE task (5 mins).
- No long paragraphs.
- Make it fresh and punchy.
"""

        if gemini_key:
            try:
                text = GeminiClient.generate_text(prompt)
                return text.strip()
            except Exception as e:
                print(f"⚠️ Gemini failed -> fallback mode. Reason: {e}")

        # ✅ fallback (local)
        return (
            f"😈 {name}, based on your answers:\n"
            f"• {a1}\n"
            f"• {a2}\n\n"
            f"🔥 Here’s the real fix:\n"
            f"• Stop waiting for perfect mood.\n"
            f"• Do the next right action even if you hate it.\n"
            f"• You don’t need confidence. You need reps.\n\n"
            f"🎯 ONE Task (5 mins):\n"
            f"• Start the smallest version of what you're avoiding ✅"
        )