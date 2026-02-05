from flask import Blueprint, render_template, session, redirect, url_for

from app.utils.auth_decorators import login_required
from app.services.tools_registry import ToolsRegistry

# Main blueprint: handles public pages and dashboard
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def welcome():
    """
    Welcome page route.
    Redirects user to dashboard if already logged in.
    """
    if session.get("loggedin"):
        return redirect(url_for("main.dashboard"))
    return render_template("main/welcome.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    """
    Dashboard route:
    - Shows tool cards dynamically from ToolsRegistry
    """
    tools = ToolsRegistry.get_tools()
    return render_template(
        "main/dashboard.html",
        username=session.get("username"),
        tools=tools
    )