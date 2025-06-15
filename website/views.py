from flask import current_app, Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website.models import User, TrackedFlights, db
from utils.flight_utils import arrange_flights_data



views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":

        return render_template("index.html")
    
    user_flights = TrackedFlights.query.filter_by(user_id=current_user.id).all()

    print(user_flights)
    
    return render_template("index.html", flights=user_flights)

@views.route("/results")
@login_required
def results():
    from amadeus import ResponseError
    from services.amadeus_client import amadeus

    departure = request.args.get("departure")
    destination = request.args.get("destination")
    departure_date = request.args.get("departure_date")

    flights=[]
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode="LIS",
            destinationLocationCode="FCO",
            departureDate="2025-06-17",
            # If round trip
            #returnDate="2025-06-17", 
            adults=1,
            max=20)

        arranged_flights = arrange_flights_data(response.data)
        print(arranged_flights)
    except ResponseError as error:
        print(error)
        print(arranged_flights)

    return render_template("results.html", flights=arranged_flights)



@views.route("/search", methods=["GET", "POST"])
@login_required
def search_flights():
    from datetime import datetime, timedelta
    from utils.flight_utils import extract_airport_shorten

    airport_list = ["Lisbon (LIS)", "Porto (OPO)", "Madrid (MAD)", "Barcelona (BCN)",
                    "Paris (CDG)", "London (LHR)", "Frankfurt (FRA)", "Amsterdam (AMS)",
                    "Rome (FCO)", "New York (JFK)"]

    if request.method == "POST":
        departure = request.form.get("departure")
        destination = request.form.get("destination")
        only_direct_flights = request.form.get("only_direct")
        departure_date = request.form.get("departure_date")
        print(departure_date)
        departure_range = request.form.get("departure_range")


        if departure not in airport_list: 
            flash("Please select a valid Airport for Departure.", "error")
            return redirect(request.url)
        
        if destination not in airport_list: 
            flash("Please select a valid Airport for Destination.", "error")
            return redirect(request.url)
        
        if departure == destination:
            flash("Departure and Destination cannot be the same.", "error")
            return redirect(request.url)
        
        if not departure_date and not departure_range:
            flash("Please select a Date of Departure.", "error")
            return redirect(request.url)
        
        today = datetime.now().date()
        max_date = today + timedelta(days=365)

        if departure_date:
            try:
                parsed_departure = datetime.strptime(departure_date, "%Y/%m/%d").date()
            except ValueError:
                flash("Invalid Departure Date format.", "error")
                return redirect(request.url)

            if parsed_departure < today:
                flash("Selected date cannot be in the past.", "error")
                return redirect(request.url)

            if parsed_departure > max_date:
                flash("Selected date must be within 1 year.", "error")
                return redirect(request.url)
            
        if departure_range:
            try:
                split_dates = departure_range.split(" to ")
                if len(split_dates) != 2:
                    raise ValueError("Invalid range format.")
                user_min_date = datetime.strptime(split_dates[0], "%Y/%m/%d").date()
                user_max_date = datetime.strptime(split_dates[1], "%Y/%m/%d").date()

                if user_min_date < today or user_max_date < today:
                    flash("Selected range cannot include past dates.", "error")
                    return redirect(request.url)

                if user_max_date > max_date:
                    flash("Selected range must be within 1 year.", "error")
                    return redirect(request.url)
            
                if user_min_date > user_max_date:
                    temp = user_min_date
                    user_min_date = user_max_date
                    user_max_date = temp

            except ValueError:
                flash("Please select both a Start and an End Date in the correct format.", "error")
                return redirect(request.url)
            
        departure_shorten = extract_airport_shorten(departure)
        destination_shorten = extract_airport_shorten(destination)
        departure_date= departure_date.replace("/", "-")
            
        #flash("Searching for your future flight.", "success")
        return redirect(url_for("views.results", departure=departure_shorten,
                        destination=destination_shorten, departure_date=departure_date))

    return render_template("search.html", airport_list=airport_list)

@views.route("/account", methods=["GET", "POST"])
@login_required
def user_account():
    return render_template("account.html")