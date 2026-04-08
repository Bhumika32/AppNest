"""
File: backend/app/main.py

Clean FastAPI + Socket.IO integration for AppNest
"""

import uuid
import time
import logging

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.extensions import sio
from app.core.database import Base, engine, SessionLocal
from app.platform.module_registry import ModuleRegistry

from app.api.routes.auth_routes import auth_router

import socketio

# ---------------------------------------------------------------------

# CREATE FASTAPI APP (PRIMARY HTTP APP)

# ---------------------------------------------------------------------

fastapi_app = FastAPI(
title="AppNest API",
version="2.0.0",
docs_url="/docs",
redoc_url="/redoc"
)

# ---------------------------------------------------------------------

# SOCKET.IO SERVER (REAL-TIME LAYER)

# ---------------------------------------------------------------------

from app.api.routes.ws_events import sio

# Wrap FastAPI inside Socket.IO ASGI app

app = socketio.ASGIApp(
sio,
other_asgi_app=fastapi_app
)

# ---------------------------------------------------------------------

# ROOT ENDPOINT (DEBUG PURPOSE)

# ---------------------------------------------------------------------

@fastapi_app.get("/")
def root():
    return {"status": "FastAPI is working properly"}

# ---------------------------------------------------------------------

# STARTUP EVENT

# ---------------------------------------------------------------------

@fastapi_app.on_event("startup")
async def startup_event():
    
    logging.info("Starting AppNest server...")


    # Create DB tables
    Base.metadata.create_all(bind=engine)

    # Discover modules
    logging.info("Discovering modules...")
    ModuleRegistry._discover_modules()

    logging.info("Seeding modules...")

    from app.services.module_service import ModuleService

    session = SessionLocal()
    try:
        # ModuleService.seed_modules(session)
        pass

    finally:
        session.close()

    from app.services.notification_handlers import register_notification_handlers
    register_notification_handlers()

    logging.info("Startup initialization completed.")


# ---------------------------------------------------------------------

# REQUEST MIDDLEWARE (LOGGING + TRACE)

# ---------------------------------------------------------------------

@fastapi_app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    start_time = time.time()


    response: Response = await call_next(request)

    process_time = time.time() - start_time

    response.headers["X-Request-Id"] = request_id
    response.headers["X-Process-Time"] = str(round(process_time, 4))

    return response

# ---------------------------------------------------------------------

# CORS CONFIGURATION

# ---------------------------------------------------------------------

fastapi_app.add_middleware(
CORSMiddleware,
allow_origins=settings.CORS_ORIGINS if hasattr(settings, "CORS_ORIGINS") else ["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# ---------------------------------------------------------------------

# ROUTER REGISTRATION (IMPORTANT: USE fastapi_app)

# ---------------------------------------------------------------------

from app.api.routes.auth_routes import auth_router
from app.api.routes.profile_routes import profile_router
from app.api.routes.module_routes import module_router
from app.api.routes.admin_routes import admin_router
from app.api.routes.main_routes import main_router
from app.api.routes.notification_routes import notification_router
from app.api.routes.roast_routes import roast_router

fastapi_app.include_router(auth_router, prefix="/api/auth")
fastapi_app.include_router(profile_router, prefix="/api/profile")
fastapi_app.include_router(module_router, prefix="/api/modules")
fastapi_app.include_router(admin_router, prefix="/api/admin")
fastapi_app.include_router(main_router, prefix="/api")
fastapi_app.include_router(notification_router, prefix="/api/notifications")
fastapi_app.include_router(roast_router, prefix="/api/roasts")