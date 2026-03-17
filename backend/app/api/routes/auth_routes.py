from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.domain.auth_service import AuthService
from app.domain.otp_service import OTPService
from app.core.jwt_manager import JWTManager
from app.utils.auth_decorators import get_current_user
from app.core.database import get_db
from app.models.user import User

auth_router = APIRouter()


# -----------------------------------------------------
# Pydantic Request Schemas
# -----------------------------------------------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str


class ResendOTPRequest(BaseModel):
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str


# -----------------------------------------------------
# Helper: Set Refresh Cookie
# -----------------------------------------------------

def set_auth_cookie(response: Response, session_id: int, refresh_token: str):
    cookie_value = f"{session_id}.{refresh_token}"

    response.set_cookie(
        key="refresh_token",
        value=cookie_value,
        httponly=True,
        secure=False,  # change to True in production (HTTPS)
        samesite="lax",
        max_age=30 * 24 * 60 * 60,
        path="/api/auth"
    )


# -----------------------------------------------------
# Login
# -----------------------------------------------------

@auth_router.post("/login")
async def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):

    success, message, user, session, refresh_token = AuthService.login_user(
        db,
        email=payload.email,
        password=payload.password,
        device_info=request.headers.get("user-agent"),
        ip_address=request.client.host
    )

    if not success:
        raise HTTPException(status_code=401, detail=message)

    access_token = JWTManager.issue_access_token(
        user_id=user.id,
        role=user.role.name,
        session_id=session.id
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
            "is_verified": user.is_verified
        }
    }


# -----------------------------------------------------
# Register
# -----------------------------------------------------

@auth_router.post("/register", status_code=201)
async def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):

    success, message, user = AuthService.register_user(
        db,
        payload.username,
        payload.email,
        payload.password
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    try:
        otp = OTPService.create_and_store_otp(db, payload.email, "VERIFY_EMAIL")

        OTPService.send_otp_email(
            to_email=payload.email,
            otp=otp,
            purpose="Email Verification"
        )

    except Exception as e:
        return {
            "message": f"Registration successful but OTP failed: {str(e)}"
        }

    return {"message": "Verification code sent to email."}


# -----------------------------------------------------
# Verify OTP
# -----------------------------------------------------

@auth_router.post("/verify-otp")
async def verify_otp(
    payload: OTPVerifyRequest,
    db: Session = Depends(get_db)
):

    success, message = OTPService.verify_otp(
        db,
        payload.email,
        payload.otp
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    AuthService.verify_user(db, payload.email)

    return {"message": "Account verified successfully."}


# -----------------------------------------------------
# Resend OTP
# -----------------------------------------------------

@auth_router.post("/resend-otp")
async def resend_otp(
    payload: ResendOTPRequest,
    db: Session = Depends(get_db)
):

    allowed, msg = OTPService.can_resend(db, payload.email)

    if not allowed:
        raise HTTPException(status_code=429, detail=msg)

    otp = OTPService.create_and_store_otp(
        db,
        payload.email,
        "VERIFY_EMAIL"
    )

    OTPService.send_otp_email(
        to_email=payload.email,
        otp=otp,
        purpose="Email Verification"
    )

    return {"message": "OTP resent."}


# -----------------------------------------------------
# Refresh Access Token
# -----------------------------------------------------

@auth_router.post("/refresh")
async def refresh(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):

    refresh_cookie = request.cookies.get("refresh_token")

    if not refresh_cookie or "." not in refresh_cookie:
        raise HTTPException(status_code=401, detail="No valid refresh token provided")

    session_id, refresh_token = refresh_cookie.split(".", 1)

    success, message, user, session, new_refresh = AuthService.refresh_session(
        db,
        session_id,
        refresh_token
    )

    if not success:
        response.delete_cookie(key="refresh_token", path="/api/auth")
        raise HTTPException(status_code=401, detail=message)

    new_access = JWTManager.issue_access_token(
        user.id,
        user.role.name,
        session.id
    )

    set_auth_cookie(response, session.id, new_refresh)

    return {"access_token": new_access}


# -----------------------------------------------------
# Logout
# -----------------------------------------------------

@auth_router.post("/logout")
async def logout(
    response: Response,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    session_id = user.get("session_id")

    if session_id:
        AuthService.logout_session(db, session_id)

    response.delete_cookie(key="refresh_token", path="/api/auth")

    return {"message": "Logged out"}


# -----------------------------------------------------
# Current User Profile
# -----------------------------------------------------

@auth_router.get("/me")
async def me(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_id = user.id

    user = db.query(User).filter_by(id=user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "role": user.role.name if user.role else "user",
        "avatar_url": user.avatar_url,
        "bio": user.bio,
        "is_verified": user.is_verified
    }


# -----------------------------------------------------
# Forgot Password
# -----------------------------------------------------

@auth_router.post("/forgot-password")
async def forgot_password(
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter_by(email=payload.email).first()

    if user:
        otp = OTPService.create_and_store_otp(
            db,
            payload.email,
            "RESET_PASSWORD"
        )

        OTPService.send_otp_email(
            to_email=payload.email,
            otp=otp,
            purpose="Password Reset"
        )

    return {"message": "If an account exists, instructions were sent."}


# -----------------------------------------------------
# Reset Password
# -----------------------------------------------------

@auth_router.post("/reset-password")
async def reset_password(
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    success, message = OTPService.verify_otp(
        db,
        payload.email,
        payload.otp
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    AuthService.reset_password(db, payload.email, payload.new_password)

    return {"message": "Password reset successfully. Please login again."}



# from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Body
# from typing import Optional
# from app.domain.auth_service import AuthService
# from app.domain.otp_service import OTPService
# from app.core.jwt_manager import JWTManager
# from app.utils.auth_decorators import get_current_user_claims, security
# from sqlalchemy.orm import Session
# from app.core.database import get_db

# from app.models.user import User

# auth_router = APIRouter()

# def set_auth_cookie(response: Response, session_id: int, refresh_token: str):
#     cookie_value = f"{session_id}.{refresh_token}"
#     response.set_cookie(
#         key="refresh_token",
#         value=cookie_value,
#         httponly=True,
#         secure=False,  # Set to True in production
#         samesite="lax",
#         max_age=30 * 24 * 60 * 60,
#         path="/api/auth"
#     )

# @auth_router.post("/login")
# async def login(
#     response: Response,
#     request: Request,
#     payload: dict = Body(...),
#     db: Session = Depends(get_db)
# ):
#     email = payload.get("email")
#     password = payload.get("password")
    
#     if not email or not password:
#         raise HTTPException(status_code=400, detail="Email and password are required")
        
#     success, message, user, session, refresh_token = AuthService.login_user(
#         db,
#         email=email,
#         password=password,
#         device_info=request.headers.get("user-agent"),
#         ip_address=request.client.host
#     )
    
#     if not success:
#         raise HTTPException(status_code=401, detail=message)
        
#     access_token = JWTManager.issue_access_token(
#         user_id=user.id,
#         role=user.role.name,
#         session_id=session.id
#     )
    
#     set_auth_cookie(response, session.id, refresh_token)
    
#     return {
#         "access_token": access_token,
#         "user": {
#             "id": user.id,
#             "email": user.email,
#             "username": user.username,
#             "role": user.role.name if user.role else "user",
#             "avatar_url": user.avatar_url,
#             "is_verified": user.is_verified
#         }
#     }

# @auth_router.post("/register", status_code=201)
# async def register(
#     payload: dict = Body(...),
#     db: Session = Depends(get_db)
# ):
#     username = payload.get("username")
#     email = payload.get("email")
#     password = payload.get("password")
    
#     if not username or not email or not password:
#         raise HTTPException(status_code=400, detail="All fields are required")
        
#     success, message, user = AuthService.register_user(
#         db,
#         username,
#         email,
#         password
#     )
#     if not success:
#         raise HTTPException(status_code=400, detail=message)
        
#     try:
#         otp = OTPService.create_and_store_otp(db, email, "VERIFY_EMAIL")
#         OTPService.send_otp_email(to_email=email, otp=otp, purpose="Email Verification")
#     except Exception as e:
#         # Registration succeeded but OTP failed to send
#         return {"message": f"Registration successful, but failed to send verification code: {str(e)}"}
        
#     return {"message": "Verification code sent to email."}

# @auth_router.post("/verify-otp")
# async def verify_otp(payload: dict = Body(...), db: Session = Depends(get_db)):
#     email = payload.get("email")
#     otp = payload.get("otp")
    
#     if not email or not otp:
#         raise HTTPException(status_code=400, detail="Email and OTP are required")
        
#     success, message = OTPService.verify_otp(db, email, otp)
#     if not success:
#         raise HTTPException(status_code=400, detail=message)
        
#     AuthService.verify_user(email)
#     return {"message": "Account verified successfully."}

# @auth_router.post("/resend-otp")
# async def resend_otp(payload: dict = Body(...), db: Session = Depends(get_db)):
#     email = payload.get("email")
#     if not email:
#         raise HTTPException(status_code=400, detail="Email required")
        
#     allowed, msg = OTPService.can_resend(db, email)
#     if not allowed:
#         raise HTTPException(status_code=429, detail=msg)
        
#     otp = OTPService.create_and_store_otp(db, email, "VERIFY_EMAIL")
#     OTPService.send_otp_email(to_email=email, otp=otp, purpose="Email Verification")
#     return {"message": "OTP resent."}

# @auth_router.post("/refresh")
# async def refresh(
#     request: Request,
#     response: Response,
#     db: Session = Depends(get_db)
# ):
#     refresh_cookie = request.cookies.get("refresh_token")
#     if not refresh_cookie or "." not in refresh_cookie:
#         raise HTTPException(status_code=401, detail="No valid refresh token provided")
        
#     session_id, refresh_token = refresh_cookie.split(".", 1)
    
#     success, message, user, session, new_refresh = AuthService.refresh_session(db,session_id, refresh_token)
#     if not success:
#         response.delete_cookie(key="refresh_token", path="/api/auth")
#         raise HTTPException(status_code=401, detail=message)
        
#     new_access = JWTManager.issue_access_token(user.id, user.role.name, session.id)
#     set_auth_cookie(response, session.id, new_refresh)
    
#     return {"access_token": new_access}

# async def logout(
#     response: Response,
#     claims: dict = Depends(get_current_user_claims),
#     db: Session = Depends(get_db)
# ):
#     session_id = claims.get("session_id")
#     if session_id:
#         AuthService.logout_session(db, session_id)
        
#     response.delete_cookie(key="refresh_token", path="/api/auth")
#     return {"message": "Logged out"}

# @auth_router.get("/me")
# async def me(
#     claims: dict = Depends(get_current_user_claims),
#     db: Session = Depends(get_db)
# ):
#     user_id = claims.get("sub")

#     user = db.query(User).filter_by(id=user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
        
#     return {
#         "id": user.id,
#         "email": user.email,
#         "username": user.username,
#         "role": user.role.name if user.role else "user",
#         "avatar_url": user.avatar_url,
#         "bio": user.bio,
#         "is_verified": user.is_verified
#     }

# async def forgot_password(payload: dict = Body(...), db: Session = Depends(get_db)):
#     email = payload.get("email")
#     if email:
#         user = db.query(User).filter_by(email=email).first()
#         if user:
#             otp = OTPService.create_and_store_otp(db, email, "RESET_PASSWORD")
#             OTPService.send_otp_email(to_email=email, otp=otp, purpose="Password Reset")
            
#     return {"message": "If an account exists, instructions were sent."}

# @auth_router.post("/reset-password")
# async def reset_password(payload: dict = Body(...), db: Session = Depends(get_db)):
#     email = payload.get("email")
#     otp = payload.get("otp")
#     new_password = payload.get("new_password")
    
#     if not email or not otp or not new_password:
#         raise HTTPException(status_code=400, detail="Missing fields")
        
#     success, message = OTPService.verify_otp(db, email, otp)
#     if not success:
#         raise HTTPException(status_code=400, detail=message)
        
#     AuthService.reset_password(email, new_password)
#     return {"message": "Password reset successfully. Please login again."}
