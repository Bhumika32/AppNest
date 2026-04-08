from app.core.extensions import sio
from app.core.jwt_manager import JWTManager
import logging

logger = logging.getLogger(__name__)

@sio.on('connect')
async def handle_connect(sid, environ, auth=None):
    """
    Handle new WebSocket connections.
    Clients can send a JWT token in the 'auth' object or as a query parameter.
    """
    try:
        # 1. Try token from auth object (preferred in newer clients)
        token = None
        if auth and isinstance(auth, dict):
            token = auth.get('token')
        
        # 2. Fallback to query parameters
        if not token:
            from urllib.parse import parse_qs
            query_string = environ.get('QUERY_STRING', '')
            query_params = parse_qs(query_string)
            token = query_params.get('token', [None])[0]

        if not token:
            logger.warning(f"Client {sid} connected without token")
            return False # Reject connection if desired, or keep as anonymous

        decoded = JWTManager.validate_token(token)
        if not decoded:
            logger.warning(f"Client {sid} provided invalid token")
            return False

        user_id = decoded['sub']
        room = f"user_{user_id}"
        await sio.enter_room(sid, room)
        logger.info(f"User {user_id} (sid: {sid}) joined room {room}")
        await sio.emit('connection_success', {'message': f'Connected to room {room}'}, to=sid)
    except Exception as e:
        logger.error(f"WebSocket connect error for sid {sid}: {e}")
        return False

@sio.on('disconnect')
async def handle_disconnect(sid):
    logger.info(f"Client {sid} disconnected")

@sio.on('join_profile')
async def on_join(sid, data):
    """Fallback join room if token wasn't in connection string."""
    try:
        user_id = data.get('user_id')
        if user_id:
            room = f"user_{user_id}"
            await sio.enter_room(sid, room)
            logger.info(f"User {user_id} manually joined room {room}")
    except Exception as e:
        logger.error(f"WebSocket join_profile error: {e}")

