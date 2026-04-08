"""
app/utils/auth_decorators.py

Reusable decorators for authentication checks.
This prevents repeated session-check code in every route.
"""

from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(view_func):
    """
    Protect a route so it can only be accessed by logged-in users.
    If not logged in, redirect to login page.
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("loggedin"):
            flash("Please login to continue.", "error")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)

    return wrapper