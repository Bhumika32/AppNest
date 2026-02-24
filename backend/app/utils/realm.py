"""
app/utils/realm.py

Realm management utilities for AppNest.
Realms define different game and tool categories/themes.
"""

from flask import session, g

# Realm constants
DARK_MOON = "DARK_MOON"
FANTASY_SHRINE = "FANTASY_SHRINE"

VALID_REALMS = [DARK_MOON, FANTASY_SHRINE]


def set_realm(realm: str) -> None:
    """Set the active realm for the user session."""
    if realm not in VALID_REALMS:
        raise ValueError(f"Invalid realm: {realm}")
    session['active_realm'] = realm
    g.active_realm = realm


def get_active_realm() -> str:
    """Get the current active realm from session or context."""
    return g.get('active_realm', session.get('active_realm', DARK_MOON))


def realm_context_processor():
    """Provide realm context to all templates and responses."""
    return {
        'active_realm': get_active_realm(),
        'available_realms': VALID_REALMS,
    }
