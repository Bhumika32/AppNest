"""
Entry point to run the FastAPI application locally.
"""

from dotenv import load_dotenv
import uvicorn
import logging
import os

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Configure logging globally
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ✅ Debug helper: confirm API key exists
print("[OK] GEMINI_API_KEY loaded:", "YES" if os.getenv("GEMINI_API_KEY") else "NO")

if __name__ == "__main__":
    print("[OK] Starting AppNest with Uvicorn (FastAPI + SocketIO)...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)