import traceback
from flask import request, jsonify, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from app.services.auth_service import AuthService
from app.services.otp_service import OTPService
from app.core.jwt_manager import JWTManager
from app.models.user import User

class AuthController:
    """
    Controller for production-grade authentication API.
    """

    @staticmethod
    def _set_auth_cookie(response, refresh_token):
        """Helper to set secure HttpOnly refresh cookie."""
        # Note: secure=False and samesite='Lax' for local development compatibility
        response.set_cookie(
            'refresh_token',
            refresh_token,
            httponly=True,
            secure=False,  
            samesite='Lax',
            max_age=30 * 24 * 60 * 60  # 30 days
        )
        return response

    @staticmethod
    def login():
        try:
            data = request.get_json() or {}
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return jsonify({"error": "Email and password are required"}), 400

            # 1. Authenticate via Service
            success, message, user, session, refresh_token = AuthService.login_user(
                email=email, 
                password=password,
                device_info=request.headers.get('User-Agent'),
                ip_address=request.remote_addr
            )

            if not success:
                return jsonify({"error": message}), 401

            # 2. Issue short-lived access token
            access_token = JWTManager.issue_access_token(
                user_id=user.id,
                role=user.role.name,
                session_id=session.id
            )

            # 3. Create response and set HttpOnly refresh cookie
            resp = make_response(jsonify({
                "access_token": access_token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "role": user.role.name if user.role else "user",
                    "avatar_url": user.avatar_url,
                    "is_verified": user.is_verified
                }
            }))
            
            return AuthController._set_auth_cookie(resp, refresh_token), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "Internal Server Error"}), 500

    @staticmethod
    def register():
        try:
            data = request.get_json() or {}
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if not username or not email or not password:
                return jsonify({"error": "All fields are required"}), 400

            success, message, user = AuthService.register_user(username, email, password)
            if not success:
                return jsonify({"error": message}), 400

            # Generate and send hashed OTP
            otp = OTPService.create_and_store_otp(email=email, purpose="VERIFY_EMAIL")
            OTPService.send_otp_email(to_email=email, otp=otp, purpose="Email Verification")

            return jsonify({"message": "Verification code sent to email."}), 201
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": "Registration failed"}), 500

    @staticmethod
    def verify_otp():
        try:
            data = request.get_json() or {}
            email = data.get("email")
            otp = data.get("otp")

            if not email or not otp:
                return jsonify({"error": "Email and OTP are required"}), 400

            success, message = OTPService.verify_otp(email, otp)
            if not success:
                return jsonify({"error": message}), 400

            # Mark user as verified
            user = User.query.filter_by(email=email).first()
            if user:
                user.is_verified = True
                from app.core.extensions import db
                db.session.commit()

            return jsonify({"message": "Account verified successfully."}), 200
        except Exception as e:
            return jsonify({"error": "Verification error"}), 500

    @staticmethod
    def resend_otp():
        data = request.get_json() or {}
        email = data.get("email")
        if not email:
            return jsonify({"error": "Email required"}), 400

        allowed, msg = OTPService.can_resend(email)
        if not allowed:
            return jsonify({"error": msg}), 429

        otp = OTPService.create_and_store_otp(email, "VERIFY_EMAIL")
        OTPService.send_otp_email(email, otp, "Email Verification")
        return jsonify({"message": "OTP resent."}), 200

    @staticmethod
    def refresh():
        """Refresh rotation: uses HttpOnly cookie to issue new access + refresh tokens."""
        refresh_token = request.cookies.get('refresh_token')
        if not refresh_token:
            return jsonify({"error": "No refresh token provided"}), 401

        success, message, user, session, new_refresh = AuthService.refresh_session(refresh_token)
        if not success:
            resp = make_response(jsonify({"error": message}), 401)
            resp.set_cookie('refresh_token', '', expires=0) # Clear invalid cookie
            return resp

        # Issue new access token
        new_access = JWTManager.issue_access_token(user.id, user.role.name, session.id)

        resp = make_response(jsonify({"access_token": new_access}))
        return AuthController._set_auth_cookie(resp, new_refresh), 200

    @staticmethod
    @jwt_required()
    def logout():
        refresh_token = request.cookies.get('refresh_token')
        if refresh_token:
            AuthService.logout_session(refresh_token)
        
        resp = make_response(jsonify({"message": "Logged out"}))
        resp.set_cookie('refresh_token', '', expires=0)
        return resp, 200

    @staticmethod
    @jwt_required()
    def logout_all():
        user_id = get_jwt_identity()
        AuthService.logout_all_sessions(user_id)
        
        resp = make_response(jsonify({"message": "Logged out from all devices"}))
        resp.set_cookie('refresh_token', '', expires=0)
        return resp, 200

    @staticmethod
    @jwt_required()
    def me():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role.name if user.role else "user",  # ✅ Safely get role name
            "avatar_url": user.avatar_url,
            "bio": user.bio,
            "is_verified": user.is_verified
        }), 200

    @staticmethod
    def forgot_password():
        data = request.get_json() or {}
        email = data.get("email")
        # Secure version: always return generic success
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                otp = OTPService.create_and_store_otp(email, "RESET_PASSWORD")
                OTPService.send_otp_email(email, otp, "Password Reset")
        
        return jsonify({"message": "If an account exists, instructions were sent."}), 200

    @staticmethod
    def reset_password():
        data = request.get_json() or {}
        email = data.get("email")
        otp = data.get("otp")
        new_password = data.get("new_password")

        if not email or not otp or not new_password:
            return jsonify({"error": "Missing fields"}), 400

        success, message = OTPService.verify_otp(email, otp)
        if not success:
            return jsonify({"error": message}), 400

        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(new_password)
            # Critical Security Step: Revoke ALL sessions after password change
            AuthService.logout_all_sessions(user.id)
            from app.core.extensions import db
            db.session.commit()

        return jsonify({"message": "Password reset successfully. Please login again."}), 200
