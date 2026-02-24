"""
app/api/roast_routes.py

API Endpoints for Roast Service.

Provides various roast types: normal, personal, ultra, and AI-generated.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.roast.normal_roast import NormalRoastService
from app.services.roast.personal_roast import PersonalRoastService
from app.services.roast.ultra_roast import UltraRoastService
from app.services.roast.ai_roast import AIRoastService

roast_bp = Blueprint("roast", __name__, url_prefix="/api/roast")


@roast_bp.route("/normal", methods=["GET"])
@jwt_required()
def get_normal_roast():
    """Get a normal (friendly) roast."""
    try:
        result = NormalRoastService.generate()
        return jsonify(
            roast=result.roast_text,
            intensity=result.intensity,
            type="normal",
        ), 200
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
        data = request.get_json()
        name = data.get("name", "Dev")

        result = PersonalRoastService.generate(name)

        return jsonify(
            name=result.name,
            roast=result.roast_text,
            intensity=result.intensity,
            type="personal",
        ), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@roast_bp.route("/ultra", methods=["GET"])
@jwt_required()
def get_ultra_roast():
    """Get an ultra (maximum intensity) roast."""
    try:
        result = UltraRoastService.generate()

        return jsonify(
            roast=result.roast_text,
            intensity=result.intensity,
            type="ultra",
        ), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@roast_bp.route("/game/<game_name>", methods=["GET"])
@jwt_required()
def get_game_roast(game_name):
    """Get a game-specific roast."""
    try:
        result = AIRoastService.generate_game_roast(game_name)

        return jsonify(
            roast=result.roast_text,
            intensity=result.intensity,
            game=result.context,
            type="game",
        ), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@roast_bp.route("/tool/<tool_name>", methods=["GET"])
@jwt_required()
def get_tool_roast(tool_name):
    """Get a tool-specific roast."""
    try:
        result = AIRoastService.generate_tool_roast(tool_name)

        return jsonify(
            roast=result.roast_text,
            intensity=result.intensity,
            tool=result.context,
            type="tool",
        ), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@roast_bp.route("/random", methods=["GET"])
@jwt_required()
def get_random_roast():
    """Get a random roast."""
    try:
        result = AIRoastService.generate_random()

        return jsonify(
            roast=result.roast_text,
            intensity=result.intensity,
            type="random",
        ), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
