"""
app/api/routes/roast_routes.py

API Endpoints for Roast Service.

Provides various roast types: normal, personal, ultra, game-specific, and tool-specific.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.domain.roast_service import RoastService
from app.platform.module_result import ModuleResult

roast_bp = Blueprint("roast", __name__, url_prefix="/api/roast")


@roast_bp.route("/normal", methods=["GET"])
@jwt_required()
def get_normal_roast():
    """Get a normal (friendly) roast."""
    try:
        roast = RoastService.get_normal_roast()
        return jsonify(roast=roast, intensity="low", type="normal"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@roast_bp.route("/personal", methods=["POST"])
@jwt_required()
def get_personal_roast():
    """
    Get a personalized roast.

    Input: { "name": "John" }
    """
    try:
        data = request.get_json() or {}
        name = data.get("name", "Dev")
        roast = RoastService.get_personal_roast(name)
        return jsonify(name=name, roast=roast, intensity="medium", type="personal"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@roast_bp.route("/ultra", methods=["GET"])
@jwt_required()
def get_ultra_roast():
    """Get an ultra (maximum intensity) roast."""
    try:
        roast = RoastService.get_ultra_roast()
        return jsonify(roast=roast, intensity="high", type="ultra"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@roast_bp.route("/game/<game_name>", methods=["GET"])
@jwt_required()
def get_game_roast(game_name):
    """Get a game-specific roast."""
    try:
        mock_result = ModuleResult(completed=False, status="lose", score=0)
        roast = RoastService.get_roast(game_name, mock_result)
        return jsonify(roast=roast, intensity="medium", game=game_name, type="game"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@roast_bp.route("/tool/<tool_name>", methods=["GET"])
@jwt_required()
def get_tool_roast(tool_name):
    """Get a tool-specific roast."""
    try:
        mock_result = ModuleResult(completed=True, status="success", score=0)
        roast = RoastService.get_roast(tool_name, mock_result)
        return jsonify(roast=roast, intensity="low", tool=tool_name, type="tool"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@roast_bp.route("/random", methods=["GET"])
@jwt_required()
def get_random_roast():
    """Get a random roast."""
    try:
        roast = RoastService.get_normal_roast()
        return jsonify(roast=roast, intensity="medium", type="random"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
