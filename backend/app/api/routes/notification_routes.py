from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.services.notification_service import NotificationService
from app.api.deps.auth import get_current_user
from app.models.user import User
from sqlalchemy.orm import Session
from app.core.database import get_db

notification_router = APIRouter()

@notification_router.get("")
async def get_notifications(
    limit: int = Query(50, ge=1, le=100),
    unread_only: bool = Query(False),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's notifications.
    """
    stats = NotificationService.get_notification_stats(db, user.id)
    user_id = user.id
    
    notifications = NotificationService.get_user_notifications(
        db,
        user_id=user_id,
        limit=limit,
        unread_only=unread_only
    )
    unread_count = NotificationService.get_unread_count(db, user_id)
    
    return {
        "notifications": notifications,
        "unread_count": unread_count,
        "total": len(notifications),
    }

@notification_router.get("/unread")
async def get_unread_count(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get count of unread notifications."""
    count = NotificationService.get_unread_count(db, user.id)
    return {"unread_count": count}

@notification_router.patch("/{notification_id}/read")
async def mark_as_read(notification_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Mark a notification as read."""
    stats = NotificationService.get_notification_stats(db, user.id)
    if stats.get("unread_count", 0) == 0:
        raise HTTPException(status_code=400, detail="No unread notifications")          
    user_id = user.id
    success = NotificationService.mark_as_read(db, user_id, notification_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    unread_count = NotificationService.get_unread_count(db, user_id)
    return {"success": True, "unread_count": unread_count}

@notification_router.patch("/read-all")
async def mark_all_as_read(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Mark all notifications as read."""
    marked_count = NotificationService.mark_all_as_read(db, user.id)
    return {
        "success": True,
        "marked_count": marked_count,
        "unread_count": 0
    }

@notification_router.delete("/{notification_id}")
async def delete_notification(notification_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete a notification."""
    success = NotificationService.delete_notification(db, user.id, notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"success": True}

@notification_router.delete("/clear-all")
async def clear_all(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete all notifications for the user."""
    deleted_count = NotificationService.clear_all_notifications(db, user.id)
    return {"success": True, "deleted_count": deleted_count}
