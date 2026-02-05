"""
app/tools/moodfix/routes.py

MoodFix Tool Routes (Ultimate Roast Chat)

✅ Step-1: Start mood roast (local pack + optional Gemini later)
✅ Step-2: Chat continues (2 answers)
✅ Step-3: Personalized roast reply
✅ Mood stays selected
✅ Name mandatory
✅ Intensity + Target supported
✅ Streak system with daily tracking (count + date)
✅ Streak bonus roast message (fun + addictive)
✅ Terminal logs for Gemini fallback/debug
"""

from datetime import date
from flask import Blueprint, render_template, request, flash, session, redirect, url_for

from app.utils.auth_decorators import login_required
from app.tools.moodfix.service import MoodFixService

moodfix_bp = Blueprint("moodfix", __name__, url_prefix="/tools/moodfix")


@moodfix_bp.route("/", methods=["GET", "POST"])
@login_required
def moodfix_home():
    # ---------------------------
    # ✅ Streak system (safe dict)
    # ---------------------------
    today = str(date.today())

    streak_obj = session.get("moodfix_streak", {"count": 0, "date": today})

    # Safety checks (so it never crashes)
    if not isinstance(streak_obj, dict):
        streak_obj = {"count": 0, "date": today}

    if "count" not in streak_obj:
        streak_obj["count"] = 0
    if "date" not in streak_obj:
        streak_obj["date"] = today

    # ---------------------------
    # ✅ Reset chat if page opened fresh (optional)
    # NOTE: Don't wipe on GET anymore, because you want mood + name to stay.
    # If you want wipe on refresh, uncomment next 2 lines.
    # ---------------------------
    # if request.method == "GET":
    #     pass

    if request.method == "POST":
        user_message = request.form.get("user_message", "").strip()
        action = request.form.get("action", "").strip()

        # ---------------------------
        # ✅ Step-1 Start MoodFix
        # ---------------------------
        if action == "start":
            entered_name = request.form.get("name", "").strip()
            selected_mood = request.form.get("mood", "").strip()
            selected_intensity = request.form.get("intensity", "medium").strip()
            target = request.form.get("target", "").strip()

            if not entered_name:
                flash("Name is mandatory 😈 I need a target 🎯", "danger")
                return redirect(url_for("moodfix.moodfix_home"))

            if not selected_mood:
                flash("Pick a mood first 😭", "danger")
                return redirect(url_for("moodfix.moodfix_home"))

            # ✅ Update streak (once per start action)
            if streak_obj["date"] == today:
                streak_obj["count"] += 1
            else:
                streak_obj["count"] = 1
                streak_obj["date"] = today

            session["moodfix_streak"] = streak_obj

            # ✅ Generate session seed so output stays fresh
            session_seed = MoodFixService.make_session_seed()

            result = MoodFixService.generate(
                mood=selected_mood,
                name=entered_name,
                session_seed=session_seed,
                intensity=selected_intensity,
                target=target,
            )

            # ✅ Build chat history
            chat = []

            # 🔥 Funny roast popup message
            chat.append({"role": "bot", "text": MoodFixService.get_intro_line(streak_obj["count"])})

            chat.append({"role": "bot", "text": result.pack_text})

            # Ask 2 mood questions
            for q in result.questions:
                chat.append({"role": "bot", "text": f"🧠 {q}"})

            session["moodfix_chat"] = chat
            session["moodfix_context"] = {
                "name": result.name,
                "mood": result.mood,
                "mood_label": result.mood_label,
                "seed": session_seed,
                "answers": [],
                "questions": result.questions,
                "intensity": selected_intensity,
                "target": target,
            }

            # Save fields so UI stays filled
            session["moodfix_form"] = {
                "entered_name": entered_name,
                "selected_mood": selected_mood,
                "selected_intensity": selected_intensity,
                "target": target,
            }

            flash("😈 MoodFix dropped. Try ignoring it now.", "success")
            return redirect(url_for("moodfix.moodfix_home"))

        # ---------------------------
        # ✅ Step-2 User chat answers
        # ---------------------------
        if user_message:
            chat = session.get("moodfix_chat", [])
            ctx = session.get("moodfix_context", None)

            if not ctx:
                flash("MoodFix session expired. Hit Reset and start again 😭", "warning")
                return redirect(url_for("moodfix.moodfix_home"))

            chat.append({"role": "user", "text": user_message})
            ctx["answers"].append(user_message)

            # ✅ After 2 answers -> personalized fix (Gemini optional)
            if len(ctx["answers"]) >= 2:
                response = MoodFixService.generate_personalized_reply(
                    name=ctx["name"],
                    mood=ctx["mood"],
                    mood_label=ctx["mood_label"],
                    qna=ctx["answers"][:2],
                    intensity=ctx.get("intensity", "medium"),
                    target=ctx.get("target", ""),
                )
                chat.append({"role": "bot", "text": response})
                chat.append({"role": "bot", "text": "✅ Done. Want another MoodFix? Hit Reset 😈"})

            else:
                chat.append({"role": "bot", "text": "Good ✅ one more answer and I’ll roast-fix you properly 😈"})

            session["moodfix_chat"] = chat
            session["moodfix_context"] = ctx

            return redirect(url_for("moodfix.moodfix_home"))

    # ---------------------------
    # ✅ Render page with sticky fields
    # ---------------------------
    form = session.get("moodfix_form", {})
    entered_name = form.get("entered_name", "")
    selected_mood = form.get("selected_mood", "")
    selected_intensity = form.get("selected_intensity", "medium")
    target = form.get("target", "")

    return render_template(
        "tools/moodfix_chat.html",
        chat=session.get("moodfix_chat", []),
        moods=MoodFixService.MOODS,
        intensities=MoodFixService.INTENSITIES,
        entered_name=entered_name,
        selected_mood=selected_mood,
        selected_intensity=selected_intensity,
        target=target,
        streak_count=streak_obj.get("count", 0),
    )


@moodfix_bp.route("/reset", methods=["POST"])
@login_required
def moodfix_reset():
    session.pop("moodfix_chat", None)
    session.pop("moodfix_context", None)
    session.pop("moodfix_form", None)
    flash("Reset done ✅ Now pick a mood again 😈", "info")
    return redirect(url_for("moodfix.moodfix_home"))