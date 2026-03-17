"""
backend/app/main.py
Main FastAPI entrypoint for AppNest.
"""

import uuid
import time
import logging

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from sqlalchemy.orm import Session
from typing import Generator

import socketio
import app.core.database as get_db
from app.core.extensions import engine, Base, SessionLocal
from app.platform.module_registry import ModuleRegistry
from app.api.routes.ws_events import sio

# ---------------------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------------------

app = FastAPI(
    title="AppNest API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ---------------------------------------------------------------------
# DB Dependency (for FastAPI style endpoints if needed)
# ---------------------------------------------------------------------

def get_db() -> Generator[Session, None, None]:

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


# ---------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------

@app.on_event("startup")
async def startup_event():

    logging.info("Starting AppNest server...")

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Discover platform modules
    logging.info("Discovering modules...")
    ModuleRegistry._discover_modules()

    logging.info("Seeding modules...")

    from app.domain.module_service import ModuleService

    session = SessionLocal()

    try:
        ModuleService.seed_modules(session)
    finally:
        session.close()

    logging.info("Startup initialization completed.")


# ---------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------

@app.middleware("http")
async def request_context_middleware(request: Request, call_next):

    request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    start_time = time.time()

    request.state.request_id = request_id

    # ------------------------------------------------
    # CREATE REQUEST SCOPED DB SESSION
    # ------------------------------------------------

    session = SessionLocal()
    #db.session = session

    try:

        response: Response = await call_next(request)

    finally:
        # Always close DB session
        session.close()

    process_time = time.time() - start_time

    response.headers["X-Request-Id"] = request_id
    response.headers["X-Process-Time"] = str(round(process_time, 4))

    return response


# ---------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if hasattr(settings, "CORS_ORIGINS") else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------

from app.api.routes.auth_routes import auth_router
from app.api.routes.profile_routes import profile_router
from app.api.routes.module_routes import module_router
from app.api.routes.admin_routes import admin_router
from app.api.routes.main_routes import main_router
from app.api.routes.notification_routes import notification_router
from app.api.routes.roast_routes import roast_router

app.include_router(auth_router, prefix="/api/auth")
app.include_router(profile_router, prefix="/api/profile")
app.include_router(module_router, prefix="/api/modules")
app.include_router(admin_router, prefix="/api/admin")
app.include_router(main_router, prefix="/api")
app.include_router(notification_router, prefix="/api/notifications")
app.include_router(roast_router, prefix="/api/roasts")

# ---------------------------------------------------------------------
# Socket.IO Integration
# ---------------------------------------------------------------------

fastapi_app = app

app = socketio.ASGIApp(
    sio,
    other_asgi_app=fastapi_app
)