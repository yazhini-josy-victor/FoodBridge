

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import User, Institution
from app.utils.validators import normalize_email, validate_password


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = normalize_email(request.form.get("email", ""))
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "").strip().lower()

        # Only these roles can be selected during public registration.
        if role not in {"donor", "recipient"}:
            flash("Please select a valid account type.", "error")
            return redirect(url_for("auth.register"))

        if not full_name or len(full_name) > 120:
            flash("Enter your name (maximum 120 characters).", "error")
            return redirect(url_for("auth.register"))

        if not email or len(email) > 255 or "@" not in email:
            flash("Enter a valid email address.", "error")
            return redirect(url_for("auth.register"))

        valid, message = validate_password(password)
        if not valid:
            flash(message, "error")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("auth.register"))

        # Recipient accounts must also provide an institution profile.
        institution_data = None
        if role == "recipient":
            institution_data = {
                "name": request.form.get("institution_name", "").strip(),
                "institution_type": request.form.get(
                    "institution_type", ""
                ).strip(),
                "address": request.form.get("address", "").strip(),
                "maps_url": request.form.get("maps_url", "").strip(),
                "contact_person": request.form.get(
                    "contact_person", ""
                ).strip(),
                "contact_number": request.form.get(
                    "contact_number", ""
                ).strip(),
            }

            allowed_types = {
                "old_age_home",
                "orphanage",
                "hospital",
                "shelter",
                "community_kitchen",
                "general_ngo",
                "other",
            }

            if (
                not institution_data["name"]
                or not institution_data["address"]
                or not institution_data["contact_person"]
                or not institution_data["contact_number"]
                or institution_data["institution_type"] not in allowed_types
            ):
                flash(
                    "Complete all required institution details.",
                    "error",
                )
                return redirect(url_for("auth.register"))

            if len(institution_data["name"]) > 180:
                flash("Institution name is too long.", "error")
                return redirect(url_for("auth.register"))

            if len(institution_data["address"]) > 300:
                flash("Institution address is too long.", "error")
                return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "error")
            return redirect(url_for("auth.register"))

        user = User(
            full_name=full_name,
            email=email,
            role=role,
        )
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.flush()

            if institution_data is not None:
                institution = Institution(
                    user_id=user.id,
                    **institution_data,
                )
                db.session.add(institution)

            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            flash(
                "This email may already be registered. Please try another.",
                "error",
            )
            return redirect(url_for("auth.register"))

        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

    
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = normalize_email(request.form.get("email", ""))
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash("Invalid email or password.", "error")
            return redirect(url_for("auth.login"))

        if not user.is_active:
            flash(
                "This account is inactive. Contact the administrator.",
                "error",
            )
            return redirect(url_for("auth.login"))

        login_user(user)
        flash("You have logged in successfully.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("login.html")

@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully.", "success")
    return redirect(url_for("main.home"))

