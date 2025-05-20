from flask import current_app, Blueprint, render_template, request
from flask_login import login_required, current_user
from website.models import User, TrackedFlights, db

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":

        return render_template("index.html")
    
    user_flights = TrackedFlights.query.filter_by(user_id=current_user.id).all()

    print(user_flights)
    
    return render_template("index.html", flights=user_flights)

@views.route("/search", methods=["GET", "POST"])
@login_required
def search_flights():
    return render_template("search.html")

@views.route("/account", methods=["GET", "POST"])
@login_required
def user_account():
    return render_template("account.html")
