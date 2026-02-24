"""
app/api/profile_routes.py

API Endpoints for User Profile Management.

Provides profile retrieval, updates, and user statistics.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.extensions import db
from app.models.user import User
from app.services.profile.user_profile import UserProfileService
from werkzeug.utils import secure_filename
from flask import current_app, url_for
import os
import time

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@profile_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_profile():
    """Get current user's profile."""
    try:
        user_id = int(get_jwt_identity())  # Convert string ID back to int
        user = db.session.get(User, user_id)

        if not user:
            return jsonify(error="User not found"), 404

        profile = UserProfileService.format_user_profile(user)
        stats = UserProfileService.get_user_statistics(user)
        achievements = UserProfileService.get_user_achievements(user)

        return jsonify(
            profile={
                "id": profile.user_id,
                "username": profile.username,
                "email": profile.email,
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "avatar_url": profile.avatar_url,
                "bio": profile.bio,
                "joined_date": profile.joined_date,
            },
            statistics=stats,
            achievements=achievements,
        ), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@profile_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_my_profile():
    """Update current user's profile."""
    try:
        user_id = int(get_jwt_identity())  # Convert string ID back to int
        user = db.session.get(User, user_id)

        if not user:
            return jsonify(error="User not found"), 404

        data = request.get_json()

        profile = UserProfileService.update_profile(
            user,
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            bio=data.get("bio"),
            avatar_url=data.get("avatar_url"),
        )

        db.session.commit()

        return jsonify(
            message="Profile updated successfully",
            profile={
                "id": profile.user_id,
                "username": profile.username,
                "email": profile.email,
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "avatar_url": profile.avatar_url,
                "bio": profile.bio,
            },
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500


@profile_bp.route('/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """Upload user avatar image and update profile.avatar_url

    Accepts multipart/form-data with field 'avatar'. Stores file under
    static/uploads/avatars and returns absolute URL.
    """
    try:
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)
        if not user:
            return jsonify(error='User not found'), 404

        if 'avatar' not in request.files:
            return jsonify(error='No avatar file provided'), 400

        file = request.files['avatar']
        if file.filename == '':
            return jsonify(error='Empty filename'), 400

        filename = secure_filename(file.filename)
        # create uploads path
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
        os.makedirs(upload_dir, exist_ok=True)

        unique_name = f"{user_id}_{int(time.time())}_{filename}"
        save_path = os.path.join(upload_dir, unique_name)
        file.save(save_path)

        # Generate external URL
        avatar_url = url_for('static', filename=f'uploads/avatars/{unique_name}', _external=True)

        # Update user and commit
        user.avatar_url = avatar_url
        db.session.commit()

        return jsonify(success=True, avatar_url=avatar_url), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500


@profile_bp.route("/me/stats", methods=["GET"])
@jwt_required()
def get_user_statistics():
    """Get user statistics."""
    try:
        user_id = int(get_jwt_identity())  # Convert string ID back to int
        user = db.session.get(User, user_id)

        if not user:
            return jsonify(error="User not found"), 404

        stats = UserProfileService.get_user_statistics(user)

        return jsonify(statistics=stats), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@profile_bp.route("/me/achievements", methods=["GET"])
@jwt_required()
def get_user_achievements():
    """Get user achievements."""
    try:
        user_id = int(get_jwt_identity())  # Convert string ID back to int
        user = db.session.get(User, user_id)

        if not user:
            return jsonify(error="User not found"), 404

        achievements = UserProfileService.get_user_achievements(user)

        return jsonify(achievements=achievements), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
@profile_bp.route("/me/dashboard-summary", methods=["GET"])
@jwt_required()
def get_dashboard_summary():
    """Unified endpoint for user dashboard content."""
    try:
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if not user:
            return jsonify(error="User not found"), 404

        stats = UserProfileService.get_user_statistics(user) or {}
        achievements = UserProfileService.get_user_achievements(user) or []

        credits = int(stats.get("credits") or 0)
        age_days = int(stats.get('account_age_days') or 0)

        return jsonify(
            xp=credits,
            level=(credits // 1000) + 1,
            rank=f"#{max(1, 1000 - (credits // 100))}",
            title="NEON SCOUT" if credits < 5000 else "PHANTOM AGENT",
            uptime=f"{age_days * 24}h",
            performance_history=stats.get("performance_history", []),
            recent_activity=[], # Placeholder
            daily_quests=[
                {"id": 1, "task": "Complete 3 matches", "reward": "500 XP", "progress": 66, "color": "neon-blue"},
                {"id": 2, "task": "Use Forge Tools 5 times", "reward": "200 XP", "progress": 20, "color": "neon-pink"},
                {"id": 3, "task": "Participate in Roast Battle", "reward": "100 XP", "progress": 0, "color": "neon-green"},
            ],
            user={
                "username": user.username or (user.email.split('@')[0] if user.email else "user"),
                "avatar": getattr(user, 'avatar_url', None),
                "role": str(user.role.name) if (user.role and hasattr(user.role, 'name')) else "user"
            }
        ), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "details": "Check server logs"}), 500
