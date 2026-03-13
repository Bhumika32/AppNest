from flask_socketio import emit, join_room, leave_room
from app.core.extensions import socketio
from flask_jwt_extended import decode_token
from flask import request

@socketio.on('connect')
def handle_connect():
    """
    Handle new WebSocket connections.
    Clients should send a JWT token in the 'auth' object or as a query parameter.
    """
    token = request.args.get('token')
    if not token:
        # For development, allow unauthenticated connection but warn
        print("Client connected without token")
        return

    try:
        # Validate JWT and join user room
        decoded = decode_token(token)
        user_id = decoded['sub']
        room = f"user_{user_id}"
        join_room(room)
        print(f"User {user_id} joined room {room}")
        emit('connection_success', {'message': f'Connected to room {room}'})
    except Exception as e:
        print(f"WebSocket auth failed: {e}")
        # Disconnect if token is invalid in production
        # return False 

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('join_profile')
def on_join(data):
    """Fallback join room if token wasn't in connection string."""
    user_id = data.get('user_id')
    if user_id:
        room = f"user_{user_id}"
        join_room(room)
        print(f"User {user_id} manually joined room {room}")
