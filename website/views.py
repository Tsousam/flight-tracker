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
    if request.method == "POST":
        departure = request.form.get("departure")
        destination = request.form.get("destination")
        only_direct_flights = request.form.get("only_direct")
        departure_date = request.form.get("departure_date")
        departure_range = request.form.get("departure_range")


        
    airport_list = ["Ada", "Java", "JavaScript", "Brainfuck", "LOLCODE", "Node.js", "Ruby on Rails"]

    return render_template("search.html", airport_list=airport_list)

@views.route("/account", methods=["GET", "POST"])
@login_required
def user_account():
    return render_template("account.html")


@views.route("/results", methods=["GET", "POST"])
@login_required
def results():
    return render_template("results.html")
