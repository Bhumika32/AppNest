"""
app/core/extensions.py
Core database and extension setup for AppNest.
"""
import socketio

from app.core.config import settings

# ---------------------------------------------------------------------
# Socket.IO
# ---------------------------------------------------------------------
# app/core/extensions.py

mrg = socketio.AsyncRedisManager(settings.REDIS_URL, channel="appnest-socketio")

sio = socketio.AsyncServer(
    async_mode="asgi",
    client_manager=mrg,
    cors_allowed_origins=settings.CORS_ORIGINS,
)

socketio_app = socketio.ASGIApp(sio)