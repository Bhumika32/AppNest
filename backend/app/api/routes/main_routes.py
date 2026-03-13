"""
app/routes/main_routes.py

Core non-auth API routes.

NOTE:
- React handles welcome/dashboard UI
- Backend exposes only utility endpoints
"""

from flask import Blueprint

# Core API routes grouped under /api
main_bp = Blueprint("main", __name__, url_prefix="/api")


@main_bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.

    Used by:
    - Frontend to verify backend availability
    - DevOps / monitoring tools

    Response:
    {
        "status": "ok"
    }
    """
    return {"status": "ok"}, 200
