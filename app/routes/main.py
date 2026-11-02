
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    return render_template("index.html")


@bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.role == "donor":
        return render_template("donor_dashboard.html")

    elif current_user.role == "recipient":
        return render_template("recipient_dashboard.html")

    elif current_user.role == "admin":
        return render_template("admin_dashboard.html")

    return redirect(url_for("main.home"))
