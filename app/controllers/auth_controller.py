"""
app/controllers/auth_controller.py

Auth Controller:
- Login
- Register (creates unverified account + sends OTP)
- OTP verification page
- Resend OTP
- Logout
"""

from flask import render_template, request, redirect, url_for, session, flash

from app.services.auth_service import AuthService
from app.services.otp_service import OTPService


class AuthController:
    """Controller for authentication routes."""

    @staticmethod
    def login():
        """Login controller (only verified users allowed)."""
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()

            if not username or not password:
                flash("Username and password are required.", "error")
                return redirect(url_for("auth.login"))

            success, message, user = AuthService.login_user(username, password)

            if not success:
                flash(message, "error")
                return redirect(url_for("auth.login"))

            session["loggedin"] = True
            session["user_id"] = user.id
            session["username"] = user.username

            flash(message, "success")
            return redirect(url_for("main.dashboard"))

        return render_template("auth/login.html")

    @staticmethod
    def register():
        """
        Register controller:
        - Creates user (unverified)
        - Sends OTP
        - Redirects to verify OTP page
        """
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()
            confirm_password = request.form.get("confirm_password", "").strip()

            if not username or not email or not password or not confirm_password:
                flash("All fields are required.", "error")
                return redirect(url_for("auth.register"))

            if password != confirm_password:
                flash("Passwords do not match.", "error")
                return redirect(url_for("auth.register"))

            success, message, user = AuthService.register_user(username, email, password)

            if not success:
                flash(message, "error")
                return redirect(url_for("auth.register"))

            # Store pending user id in session for OTP verification step
            session["pending_user_id"] = user.id

            # Generate OTP and send email
            otp = OTPService.create_and_store_otp(email=email, purpose="Email Verification")
            OTPService.send_otp_email(to_email=email, otp=otp, purpose="Email Verification")

            flash("OTP sent to your email. Please verify.", "success")
            return redirect(url_for("auth.verify_otp"))

        return render_template("auth/register.html")

    @staticmethod
    def verify_otp():
        """
        OTP verification page:
        - Verifies OTP entered by user
        - Decides which flow is running:
            1) Email verification after registration (pending_user_id)
            2) Password reset flow (reset_user_id)
        """
        if request.method == "POST":
            submitted_otp = request.form.get("otp", "").strip()

            if not submitted_otp:
                flash("OTP is required.", "error")
                return redirect(url_for("auth.verify_otp"))

            # Validate OTP using OTPService (expiry + attempts handled there)
            otp_ok, otp_msg = OTPService.verify_otp(submitted_otp)

            if not otp_ok:
                flash(otp_msg, "error")
                return redirect(url_for("auth.verify_otp"))

            # OTP verified: decide which flow is active
            if session.get("pending_user_id"):
                pending_user_id = session.get("pending_user_id")

                ok, msg = AuthService.verify_user_email(pending_user_id)

                # Cleanup OTP + pending session
                OTPService.clear_otp_session()
                session.pop("pending_user_id", None)

                if not ok:
                    flash(msg, "error")
                    return redirect(url_for("auth.register"))

                flash(msg, "success")
                return redirect(url_for("auth.login"))

            if session.get("reset_user_id"):
                #  Mark reset OTP as verified (required for security)
                session["reset_otp_verified"] = True

                OTPService.clear_otp_session()
                flash("OTP verified. You can now reset your password.", "success")
                return redirect(url_for("auth.reset_password"))

            # If no flow is active, something is wrong (session cleared or user opened link directly)
            OTPService.clear_otp_session()
            flash("Invalid OTP flow state. Please try again.", "error")
            return redirect(url_for("auth.login"))

        # GET request -> show OTP entry page
        return render_template("auth/verify_otp.html")
    @staticmethod
    def resend_otp():
        """
        Resend OTP endpoint with cooldown + resend limit protection.
        """
        success, message = OTPService.resend_otp()

        flash(message, "success" if success else "error")
        return redirect(url_for("auth.verify_otp"))

    @staticmethod
    def forgot_password():
        """
        Forgot Password flow:
        - User enters email
        - OTP sent to that email
        - Redirect to OTP verification page
        """
        from app.models.user import User

        if request.method == "POST":
            email = request.form.get("email", "").strip()

            if not email:
                flash("Email is required.", "error")
                return redirect(url_for("auth.forgot_password"))

            # Check if email exists
            user = User.query.filter_by(email=email).first()
            if not user:
                flash("No account found with this email.", "error")
                return redirect(url_for("auth.forgot_password"))

            OTPService.clear_otp_session()
            # Store reset user id in session
            session["reset_user_id"] = user.id
            # Generate OTP and send email
            otp = OTPService.create_and_store_otp(email=email, purpose="Password Reset")
            OTPService.send_otp_email(to_email=email, otp=otp, purpose="Password Reset")

            flash("OTP sent to your email for password reset.", "success")
            return redirect(url_for("auth.verify_otp"))

        return render_template("auth/forgot_password.html")

    @staticmethod
    def reset_password():
        """
        Reset Password page:
        - Allows user to set a new password after OTP verification.
        """
        from app.models.user import User
        from app.extensions import db

        reset_user_id = session.get("reset_user_id")
        reset_otp_verified = session.get("reset_otp_verified")

        # User must come through OTP verification
        if not reset_user_id or not reset_otp_verified:
            flash("OTP verification required. Please try again.", "error")
            return redirect(url_for("auth.forgot_password"))

        if request.method == "POST":
            new_password = request.form.get("new_password", "").strip()
            confirm_password = request.form.get("confirm_password", "").strip()

            if not new_password or not confirm_password:
                flash("All fields are required.", "error")
                return redirect(url_for("auth.reset_password"))

            if new_password != confirm_password:
                flash("Passwords do not match.", "error")
                return redirect(url_for("auth.reset_password"))

            user = User.query.get(reset_user_id)
            if not user:
                flash("User not found.", "error")
                return redirect(url_for("auth.forgot_password"))

            user.set_password(new_password)
            db.session.commit()

            # Cleanup session after successful reset
            session.pop("reset_user_id", None)
            session.pop("reset_otp_verified", None)
            flash("Password updated successfully. Please login.", "success")
            return redirect(url_for("auth.login"))

        return render_template("auth/reset_password.html")

    @staticmethod
    def logout():
        """Logout controller."""
        session.clear()
        flash("Logged out successfully!", "success")
        return redirect(url_for("main.welcome"))