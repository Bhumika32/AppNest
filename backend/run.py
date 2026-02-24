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

# ✅ Configure logging globally so our logger.info() actually prints in terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# ✅ Debug helper: confirm API key exists (do NOT print the key)
print("[OK] GEMINI_API_KEY loaded:", "YES" if os.getenv("GEMINI_API_KEY") else "NO")

app = create_app()

if __name__ == "__main__":
    # ⚠️ Debug server is for local development only
    app.run(debug=True, host='127.0.0.1', port=5000)