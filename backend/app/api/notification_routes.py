"""
app/api/notification_routes.py

API Endpoints for user notification management.
Provides notification retrieval, read status updates, and deletion.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.notification_service import NotificationService

notification_bp = Blueprint("notifications", __name__, url_prefix="/api/notifications")


@notification_bp.route("", methods=["GET"])
@jwt_required()
def get_notifications():
    """
    Get user's notifications.
    
    Query params:
      - limit: Maximum notifications to retrieve (default: 50)
      - unread_only: If 'true', only return unread notifications
    """
    try:
        user_id = int(get_jwt_identity())
        limit = request.args.get("limit", 50, type=int)
        unread_only = request.args.get("unread_only", "false").lower() == "true"
        
        notifications = NotificationService.get_user_notifications(
            user_id=user_id,
            limit=limit,
            unread_only=unread_only
        )
        unread_count = NotificationService.get_unread_count(user_id)
        
        return jsonify(
            notifications=notifications,
            unread_count=unread_count,
            total=len(notifications),
        ), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@notification_bp.route("/unread", methods=["GET"])
@jwt_required()
def get_unread_count():
    """Get count of unread notifications."""
    try:
        user_id = int(get_jwt_identity())
        count = NotificationService.get_unread_count(user_id)
        return jsonify(unread_count=count), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@notification_bp.route("/<int:notification_id>/read", methods=["PATCH"])
@jwt_required()
def mark_as_read(notification_id):
    """Mark a notification as read."""
    try:
        user_id = int(get_jwt_identity())
        success = NotificationService.mark_as_read(user_id, notification_id)
        
        if not success:
            return jsonify(error="Notification not found"), 404
        
        unread_count = NotificationService.get_unread_count(user_id)
        return jsonify(success=True, unread_count=unread_count), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@notification_bp.route("/read-all", methods=["PATCH"])
@jwt_required()
def mark_all_as_read():
    """Mark all notifications as read."""
    try:
        user_id = int(get_jwt_identity())
        marked_count = NotificationService.mark_all_as_read(user_id)
        
        return jsonify(
            success=True,
            marked_count=marked_count,
            unread_count=0
        ), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@notification_bp.route("/<int:notification_id>", methods=["DELETE"])
@jwt_required()
def delete_notification(notification_id):
    """Delete a notification."""
    try:
        user_id = int(get_jwt_identity())
        success = NotificationService.delete_notification(user_id, notification_id)
        
        if not success:
            return jsonify(error="Notification not found"), 404
        
        return jsonify(success=True), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@notification_bp.route("/clear-all", methods=["DELETE"])
@jwt_required()
def clear_all():
    """Delete all notifications for the user."""
    try:
        user_id = int(get_jwt_identity())
        deleted_count = NotificationService.clear_all_notifications(user_id)
        
        return jsonify(success=True, deleted_count=deleted_count), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
