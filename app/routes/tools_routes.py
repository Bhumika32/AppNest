"""
app/routes/tools_routes.py

Tools landing page routes.
Shows all tools dynamically using ToolsRegistry.
"""

from flask import Blueprint, render_template
from app.utils.auth_decorators import login_required
from app.services.tools_registry import ToolsRegistry

tools_bp = Blueprint("tools", __name__)


@tools_bp.route("/tools/")
@login_required
def tools_home():
    """
    Tools home page:
    - Shows all available tools as cards
    """
    tools = ToolsRegistry.get_tools()
    return render_template("tools/tools_index.html", tools=tools)