from flask import Blueprint, jsonify, request
from app.services.analytics_service import AnalyticsService
from flask_jwt_extended import jwt_required, get_jwt
from app.models.module import Module
from app.core.extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route("/modules", methods=["GET"])
@jwt_required()
def get_admin_modules():
    """Get all registered modules for admin management."""
    modules = Module.query.all()
    return jsonify([m.to_dict() for m in modules]), 200


@admin_bp.route("/modules/<int:id>", methods=["PATCH"])
@jwt_required()
def update_module_status(id):
    """Enable/disable or update module metadata."""
    module = db.session.get(Module, id)
    if not module:
        return jsonify(error="Module not found"), 404

    data = request.get_json()
    if 'is_active' in data:
        module.is_active = data['is_active']
    
    db.session.commit()
    return jsonify(module.to_dict()), 200

@admin_bp.route('/analytics/overview', methods=['GET'])
@jwt_required()
def get_overview():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"msg": "Admin access required"}), 403
        
    stats = AnalyticsService.get_platform_stats()
    return jsonify(stats), 200

@admin_bp.route('/analytics/users', methods=['GET'])
@jwt_required()
def get_user_analytics():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"msg": "Admin access required"}), 403
        
    user_data = AnalyticsService.get_user_growth_data()
    return jsonify(user_data), 200
@admin_bp.route('/analytics/games', methods=['GET'])
@jwt_required()
def get_game_analytics():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"msg": "Admin access required"}), 403
        
    game_data = AnalyticsService.get_game_popularity()
    return jsonify(game_data), 200

@admin_bp.route('/analytics/tools', methods=['GET'])
@jwt_required()
def get_tool_analytics():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"msg": "Admin access required"}), 403
        
    tool_data = AnalyticsService.get_tool_usage()
    return jsonify(tool_data), 200
