# File: app/api/routes/auth_routes.py

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, BackgroundTasks
from sqlalchemy.orm import Session
import hmac
import hashlib
from app.services.auth_service import AuthService
from app.services.otp_service import OTPService
from app.core.jwt_manager import JWTManager
from app.core.config import settings
from app.api.deps.auth import get_current_user, get_token_payload
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth_schema import (
    LoginRequest,
    RegisterRequest,
    OTPVerifyRequest,
    ResendOTPRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

auth_router = APIRouter()

def sign_cookie(session_id, token):
    raw = f"{session_id}.{token}"
    signature = hmac.new(
        settings.JWT_SECRET_KEY.encode(),
        raw.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"{raw}.{signature}"
# -----------------------------------------------------
# COOKIE HELPER
# -----------------------------------------------------
def set_auth_cookie(response: Response, session_id: str, refresh_token: str):

    response.set_cookie(
        key="refresh_token",
        value=sign_cookie(session_id, refresh_token),
        httponly=True,
        secure=False,  # ⚠️ change to True in production
        samesite="lax",
        max_age=30 * 24 * 60 * 60,
        path="/",
    )


# -----------------------------------------------------
# REGISTER
# -----------------------------------------------------
@auth_router.post("/register", status_code=201)
def register(payload: RegisterRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    success, message, user = AuthService.register_user(
        db,
        payload.username,
        payload.email,
        payload.password,
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    # ---- CREATE OTP ----
    try:
        otp = OTPService.create_and_store_otp(
            db,
            payload.email,
            "VERIFY_EMAIL"
        )

        background_tasks.add_task(
            OTPService.send_otp_email,
            payload.email,
            otp,
            "Email Verification"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OTP sending failed: {str(e)}"
        )

    return {
        "message": "OTP sent successfully to your registered email",
        "status": "success"
    }


# -----------------------------------------------------
# VERIFY OTP (MANDATORY BEFORE LOGIN)
# -----------------------------------------------------
@auth_router.post("/verify-otp")
def verify_otp(payload: OTPVerifyRequest, db: Session = Depends(get_db)):

    success, message = OTPService.verify_otp(
        db,
        payload.email,
        payload.otp,
        "VERIFY_EMAIL"
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    AuthService.verify_user(db, payload.email)

    return {
        "message": "Account verified successfully",
        "status": "verified"
    }


# -----------------------------------------------------
# RESEND OTP
# -----------------------------------------------------
@auth_router.post("/resend-otp")
def resend_otp(payload: ResendOTPRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    allowed, msg = OTPService.can_resend(
        db,
        payload.email,
        "VERIFY_EMAIL"
    )

    if not allowed:
        raise HTTPException(status_code=429, detail=msg)

    try:
        otp = OTPService.create_and_store_otp(
            db,
            payload.email,
            "VERIFY_EMAIL"
        )

        background_tasks.add_task(
            OTPService.send_otp_email,
            payload.email,
            otp,
            "Email Verification"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"OTP resend failed: {str(e)}"
        )

    return {
        "message": "OTP resent successfully",
        "status": "success"
    }


# -----------------------------------------------------
# LOGIN (ONLY AFTER OTP VERIFIED)
# -----------------------------------------------------
@auth_router.post("/login")
def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):

    success, message, user, session, refresh_token = AuthService.login_user(
        db,
        email=payload.email,
        password=payload.password,
        device_info=request.headers.get("user-agent"),
        ip_address=request.client.host,
    )

    if not success:
        raise HTTPException(status_code=401, detail=message)

    access_token = JWTManager.issue_access_token(
        user_id=user.id,
        role=user.role.name,
        session_id=str(session.id),
    )

    set_auth_cookie(response, session.id, refresh_token)

    return {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role.name if user.role else "user",
            "avatar_url": user.avatar_url,
            "is_verified": user.is_verified,
        }
    }


# -----------------------------------------------------
# REFRESH TOKEN
# -----------------------------------------------------
@auth_router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):

    refresh_cookie = request.cookies.get("refresh_token")

    if not refresh_cookie:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    parts = refresh_cookie.split(".", 2)

    if len(parts) != 3:
        raise HTTPException(status_code=401, detail="Invalid cookie format")

    session_id, refresh_token, signature = parts
    
    expected_signature = hmac.new(
        settings.JWT_SECRET_KEY.encode(),
        f"{session_id}.{refresh_token}".encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid cookie signature")
    
    success, message, user, session, new_refresh = AuthService.refresh_session(
        db,
        session_id,
        refresh_token,
    )

    if not success:
        response.delete_cookie(key="refresh_token", path="/")
        raise HTTPException(status_code=401, detail=message)

    new_access = JWTManager.issue_access_token(
        user.id,
        user.role.name,
        session.id,
    )

    set_auth_cookie(response, session.id, new_refresh)

    return {"access_token": new_access}


# -----------------------------------------------------
# LOGOUT
# -----------------------------------------------------
@auth_router.post("/logout")
def logout(
    payload: dict = Depends(get_token_payload),
    response: Response = None,
    db: Session = Depends(get_db),
):
    session_id = payload.get("session_id")

    if not session_id:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    AuthService.logout_session(db, session_id)

    response.delete_cookie(key="refresh_token", path="/")

    return {"message": "Logged out"}


# -----------------------------------------------------
# CURRENT USER
# -----------------------------------------------------
@auth_router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "role": user.role.name if user.role else "user",
        "avatar_url": user.avatar_url,
        "bio": user.bio,
        "is_verified": user.is_verified,
    }