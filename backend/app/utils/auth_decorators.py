"""
app/utils/auth_decorators.py

Custom authentication decorators for AppNest.
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User
from app.core.extensions import db


def token_required(f):
    """Decorator to verify JWT token is present and valid."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"error": "Token is missing or invalid"}), 401
        return f(*args, **kwargs)
    return decorated


def user_required(f):
    """Decorator to verify JWT token and get authenticated user."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = int(get_jwt_identity())  # Convert string ID back to int
            user = db.session.get(User, user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": "Authentication failed"}), 401
        return f(*args, user=user, **kwargs)
    return decorated


def admin_required(f):
    """Decorator to verify user has admin role."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = int(get_jwt_identity())  # Convert string ID back to int
            user = db.session.get(User, user_id)
            if not user or (user.role and user.role.name.lower()) != 'admin':
                return jsonify({"error": "Admin access required"}), 403
        except Exception as e:
            return jsonify({"error": "Authentication failed"}), 401
        return f(*args, user=user, **kwargs)
    return decorated
