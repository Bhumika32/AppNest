"""
app/__init__.py

Initialization file for the AppNest backend package.
"""
# Expose core objects for easier importing if needed
from app.core.database import Base
from app.core.extensions import sio

