"""
app/core/extensions.py
Core database and extension setup for AppNest.
"""

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime,
    Text, ForeignKey, Float, JSON, Enum, Numeric, SmallInteger,
    Index, UniqueConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref

from contextvars import ContextVar
import socketio

from app.core.config import settings


# ---------------------------------------------------------------------
# Database Engine
# ---------------------------------------------------------------------

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ---------------------------------------------------------------------
# Context session storage
# ---------------------------------------------------------------------

_session_var: ContextVar = ContextVar("db_session", default=None)


class DBShim:
    """
    Compatibility layer that mimics Flask-SQLAlchemy style access (temporery).
    """

    def __init__(self):

        self.Model = Base
        self.Column = Column
        self.Integer = Integer
        self.String = String
        self.Boolean = Boolean
        self.DateTime = DateTime
        self.Text = Text
        self.ForeignKey = ForeignKey
        self.Float = Float
        self.JSON = JSON
        self.Enum = Enum
        self.Numeric = Numeric
        self.SmallInteger = SmallInteger
        self.Index = Index
        self.UniqueConstraint = UniqueConstraint
        self.func = func
        self.relationship = relationship
        self.backref = backref

    @property
    def session(self):
        return _session_var.get()

    @session.setter
    def session(self, value):
        _session_var.set(value)


db = DBShim()

# ---------------------------------------------------------------------
# Socket.IO
# ---------------------------------------------------------------------
mrg = socketio.AsyncRedisManager(settings.REDIS_URL, channel="appnest-socketio")
sio = socketio.AsyncServer(
    async_mode="asgi",
    client_manager=mrg,
    cors_allowed_origins=settings.CORS_ORIGINS
)

socketio_app = socketio.ASGIApp(sio)
# """
# app/core/extensions.py

# Core database and extension setup for AppNest.
# """

# from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import sessionmaker, scoped_session
# from sqlalchemy import (
#     create_engine, Column, Integer, String, Boolean, DateTime,
#     Text, ForeignKey, Float, JSON, Enum, Numeric, SmallInteger,
#     Index, UniqueConstraint
# )
# from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship, backref

# from contextvars import ContextVar
# import socketio

# from app.core.config import Config

# # ---------------------------------------------------------------------
# # Database Engine
# # ---------------------------------------------------------------------

# engine = create_engine(
#     Config.SQLALCHEMY_DATABASE_URI,
#     pool_pre_ping=True,      # prevents stale MySQL connections
#     pool_recycle=3600        # recycle connections every hour
# )

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )

# # db_session = scoped_session(SessionLocal)

# Base = declarative_base()

# # ---------------------------------------------------------------------
# # Context session storage
# # ---------------------------------------------------------------------

# _session_var: ContextVar = ContextVar("db_session", default=None)


# class DBShim:
#     """
#     Compatibility layer that mimics Flask-SQLAlchemy style access.
#     """

#     def __init__(self):
#         self.Model = Base
#         self.Column = Column
#         self.Integer = Integer
#         self.String = String
#         self.Boolean = Boolean
#         self.DateTime = DateTime
#         self.Text = Text
#         self.ForeignKey = ForeignKey
#         self.Float = Float
#         self.JSON = JSON
#         self.Enum = Enum
#         self.Numeric = Numeric
#         self.SmallInteger = SmallInteger
#         self.Index = Index
#         self.UniqueConstraint = UniqueConstraint
#         self.func = func
#         self.relationship = relationship
#         self.backref = backref

#     @property
#     def session(self):
#         return _session_var.get()

#     @session.setter
#     def session(self, value):
#         _session_var.set(value)


# db = DBShim()

# # ---------------------------------------------------------------------
# # Socket.IO
# # ---------------------------------------------------------------------

# sio = socketio.AsyncServer(
#     async_mode="asgi",
#     cors_allowed_origins="*"
# )

# socketio_app = socketio.ASGIApp(sio)
# # """
# # app/core/extensions.py

# # This module defines core generic extensions and database configurations.
# # """

# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker, scoped_session
# # from sqlalchemy import (
# #     create_engine, Column, Integer, String, Boolean, DateTime, 
# #     Text, ForeignKey, Float, JSON, Enum, Numeric, SmallInteger,
# #     Index, UniqueConstraint
# # )
# # from sqlalchemy.sql import func
# # from sqlalchemy.orm import relationship, backref
# # import os
# # from app.core.config import Config

# # # Create Engine
# # engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
# # # Session Factory
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # # Scoped session for background tasks/non-request flows
# # db_session = scoped_session(SessionLocal)

# # from contextvars import ContextVar

# # Base = declarative_base()

# # # ContextVar to hold session per-request
# # _session_var: ContextVar = ContextVar("db_session", default=None)

# # class DBShim:
# #     """A minimal shim to emulate Flask-SQLAlchemy for backwards compatibility."""
# #     def __init__(self):
# #         self.Model = Base
# #         self.Column = Column
# #         self.Integer = Integer
# #         self.String = String
# #         self.Boolean = Boolean
# #         self.DateTime = DateTime
# #         self.Text = Text
# #         self.ForeignKey = ForeignKey
# #         self.Float = Float
# #         self.JSON = JSON
# #         self.Enum = Enum
# #         self.Numeric = Numeric
# #         self.SmallInteger = SmallInteger
# #         self.Index = Index
# #         self.UniqueConstraint = UniqueConstraint
# #         self.func = func
# #         self.relationship = relationship
# #         self.backref = backref


# #     @property
# #     def session(self):
# #         return _session_var.get()

# #     @session.setter
# #     def session(self, value):
# #         _session_var.set(value)

# # db = DBShim()

# # import socketio
# # # ASGI SocketIO App
# # sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
# # socketio_app = socketio.ASGIApp(sio)
