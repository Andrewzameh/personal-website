import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("rememberMe")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                if remember:
                    login_user(user, remember=True)
                else:
                    login_user(user, remember=False)
                return redirect(url_for("views.home"))

            else:
                flash("Invalid password", category="error")
        else:
            flash(
                "Invalid email or no account created for this email", category="error"
            )
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category="error")
        elif len(email) < 4:
            flash("Email is too short", category="error")
        elif (
            len(password1) < 8
            or not re.search("[a-z]", password1)
            or not re.search("[A-Z]", password1)
            or not re.search("[0-9]", password1)
        ):
            flash(
                "Password must be at least 8 characters long and contain only small and capital letters and numbers",
                category="error",
            )
        elif password1 != password2:
            flash("Passwords do not match", category="error")
        else:
            newUser = User(
                email=email,
                firstName=firstName,
                lastName=lastName,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            flash("Account created successfully!", category="success")
            return redirect(url_for("views.home"))
    return render_template("signup.html", user=current_user)
