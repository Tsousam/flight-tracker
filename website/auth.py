from flask import Flask, Blueprint, render_template, request


auth = Blueprint('auth', __name__)


@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

    return render_template("login.html")

@auth.route("/logout")
def logout():
    return render_template("logout.html")

@auth.route("/password", methods=["GET", "POST"])
def password():
    if request.method == "GET":
        return render_template("password.html")

@auth.route("/register")
def register():
    return render_template("register.html")

