from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from website.models import User, db
from flask_login import login_required, login_user, logout_user, current_user



auth = Blueprint("auth", __name__)

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("You have entered an invalid username or password.", "error")
            return render_template("login.html", email=email)
        else:
            flash("Welcome back, Tracker", "success")
            login_user(user)
            return redirect(url_for("views.index"))
        
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/password", methods=["GET", "POST"])
def password():
    if request.method == "GET":
        return render_template("password.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not email:
            flash("Must provide email.", "error")

        if len(email) < 4:
            flash("Email must be at least 4 characters long.")
            return redirect(request.url)
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", "error")
            return redirect(request.url)
        
        if not password:
            flash("Must provide password.", "error")
            return redirect(request.url)

        if len(password) < 8:
            flash("Password must be at least 8 character long.")
            return redirect(request.url)

        if not confirmation:
            flash("Must confirm password.", "error")
            return redirect(request.url)

        if password != confirmation:
            flash("Passwords don't match.", "error")
            return redirect(request.url)

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Account was created successfully.", "success")

        return redirect(url_for("views.index"))

    return render_template("register.html")