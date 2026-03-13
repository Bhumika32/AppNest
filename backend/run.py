"""
Entry point to run the Flask application locally.

Why this file exists:
- We load .env before the app factory runs.
- We enable logging so service logs (MoodFix / Gemini) appear in terminal.
- We keep the server startup minimal and clean.
"""

from dotenv import load_dotenv

# ✅ Load environment variables from .env file BEFORE importing app factory
load_dotenv()

import logging
import os
from app import create_app
from app.core.extensions import socketio

# ✅ Configure logging globally
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# ✅ Debug helper: confirm API key exists
print("[OK] GEMINI_API_KEY loaded:", "YES" if os.getenv("GEMINI_API_KEY") else "NO")

app = create_app()

if __name__ == "__main__":
    # ⚠️ For SocketIO, we use socketio.run instead of app.run
    print("[OK] Starting AppNest with SocketIO...")
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)