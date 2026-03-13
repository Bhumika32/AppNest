from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.domain.module_service import ModuleService
from app.domain.lifecycle_service import LifecycleService
from app.core.auth import admin_required

module_bp = Blueprint("modules", __name__, url_prefix="/api/modules")

@module_bp.route("", methods=["GET"])
@jwt_required(optional=True)
def get_modules():
    type_filter = request.args.get('type')
    modules = ModuleService.get_all_modules(type_filter)
    return jsonify([m.to_dict() for m in modules]), 200

@module_bp.route("/<slug>", methods=["GET"])
@jwt_required(optional=True)
def get_module_by_slug(slug):
    module = ModuleService.get_module_by_slug(slug)
    if not module:
        return jsonify(error="Module not found"), 404
    return jsonify(module.to_dict()), 200

@module_bp.route("/leaderboard", methods=["GET"])
@jwt_required(optional=True)
def get_global_leaderboard():
    from app.domain.leaderboard_service import LeaderboardService
    limit = request.args.get('limit', default=10, type=int)
    rankings = LeaderboardService.get_global_rankings(limit)
    return jsonify(rankings), 200

# Analytics Endpoints
@module_bp.route("/analytics/start", methods=["POST"])
@jwt_required()
def track_start():
    user_id = get_jwt_identity()
    data = request.get_json()
    module_id = data.get('module_id')
    
    if not module_id:
        return jsonify(error="module_id required"), 400
        
    entry = ModuleService.track_module_start(user_id, module_id)
    return jsonify(message="Launch tracked", entry_id=entry.id), 201

@module_bp.route("/analytics/end", methods=["POST"])
@jwt_required()
def track_end():
    user_id = get_jwt_identity()
    data = request.get_json()
    entry_id = data.get('entry_id')
    duration = data.get('duration', 0)
    
    if not entry_id:
        return jsonify(error="entry_id required"), 400
        
    success, message = ModuleService.track_module_end(user_id, entry_id, duration)
    if success:
        return jsonify(message=message), 200
    return jsonify(error=message), 404

@module_bp.route("/execute/<slug>", methods=["POST"])
@jwt_required()
def execute_module(slug):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        entry_id = data.get('entry_id')
        result = LifecycleService.execute_module(user_id, slug, data, entry_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify(error=str(e)), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify(error=str(e)), 500

# Admin Routes
admin_module_bp = Blueprint("admin_modules", __name__, url_prefix="/api/admin/modules")

@admin_module_bp.route("", methods=["POST"])
@jwt_required()
@admin_required()
def create_module():
    data = request.get_json()
    new_module = ModuleService.create_module(data)
    return jsonify(new_module.to_dict()), 201

@admin_module_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
@admin_required()
def update_module(id):
    data = request.get_json()
    module = ModuleService.update_module(id, data)
    if not module:
        return jsonify(error="Module not found"), 404
    return jsonify(module.to_dict()), 200

@admin_module_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_required()
def delete_module(id):
    if ModuleService.delete_module(id):
        return jsonify(message="Module purged"), 200
    return jsonify(error="Module not found"), 404

@admin_module_bp.route("/seed", methods=["POST"])
@jwt_required()
@admin_required()
def seed_modules():
    result = ModuleService.seed_modules()
    return jsonify(message="Modules seeded successfully", data=result), 200
