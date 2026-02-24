"""
app/routes/realm_routes.py

Realm selection API.

IMPORTANT:
- Converted from form-based redirect to API-based design
- Frontend (React) controls navigation
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.utils.realm import set_realm, DARK_MOON, FANTASY_SHRINE

# Realm-related API routes
realm_bp = Blueprint("realm", __name__, url_prefix="/api/realm")


@realm_bp.route("/set", methods=["POST"])
@jwt_required()
def set_realm_route():
    """
    Set active realm for the authenticated user.

    Expected input (JSON):
    {
        "realm": "DARK_MOON"
    }
    """
    data = request.get_json() or {}
    realm = data.get("realm")

    if realm not in (DARK_MOON, FANTASY_SHRINE):
        return {"error": "Invalid realm"}, 400

    set_realm(realm)

    return {"success": True, "active_realm": realm}, 200
