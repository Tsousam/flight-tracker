from flask import current_app, Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from website.models import User, TrackedFlights, asc, db
from utils.flight_utils import arrange_flights_data, search_flight_offers
import json



views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":

        return render_template("index.html")
    
    user_flights = TrackedFlights.query.filter_by(user_id=current_user.id).order_by(asc(TrackedFlights.departure_date),asc(TrackedFlights.departure_arrival_time)).all()

    print(user_flights)
    
    return render_template("index.html", flights=user_flights)

@views.route("/delete-flight", methods=["POST"])
@login_required
def delete_flight():
    departure = request.form.get("departure")
    destination = request.form.get("destination")
    departure_date = request.form.get("departure_date")
    departure_arrival_time = request.form.get("departure_arrival_time")

    print(departure)
    print(destination)
    print(departure_date)
    print(departure_arrival_time)

    flight = TrackedFlights.query.filter_by(user_id=current_user.id,
                                            departure=departure,
                                            destination=destination,
                                            departure_date=departure_date,
                                            departure_arrival_time=departure_arrival_time
                                            ).first()

    print(flight)
    
    if not flight:
        flash("There was an error while trying to delete your flight. Try again later.", "error")
        return redirect(url_for('views.index'))
    
    db.session.delete(flight)
    db.session.commit()
    flash("Flight deleted successfully.", "success")
    return redirect(url_for('views.index'))

@views.route("/results")
@login_required
def results():    
    departure = request.args.get("departure")
    departure_iata = request.args.get("departure_iata")
    destination = request.args.get("destination")
    destination_iata = request.args.get("destination_iata")
    departure_date = request.args.get("departure_date")
    #departure_data_formatted = request.args.get("departure_date_formatted")
    adults = request.args.get("adults")
    max_results = request.args.get("max_results")

    print("RESULTS FUNCTION")
    print(departure_iata)
    print(destination_iata)
    print(departure_date)
    print(adults)
    print(max_results)
    print("END RESULTS FUNCTION")

    fetch_flights = search_flight_offers(departure_iata, destination_iata, departure_date, adults, max_results)
    #print(fetch_flights)
    arranged_flights = arrange_flights_data(fetch_flights, departure, destination)
    #print(arranged_flights)
    
    session['departure'] = departure
    session['destination'] = destination
    session['departure_date'] = departure_date
    session['last_search'] = json.dumps(arranged_flights)

    return render_template("results.html", departure=departure, destination=destination, departure_date=departure_date, flights=arranged_flights, if_results="results-page")

@views.route("/save-flight")
@login_required
def save_flight():
    from datetime import datetime

    url = request.args.get('url')
    airline = request.args.get('airline')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    departure_date = datetime.strptime(request.args.get('departure_date'), "%Y-%m-%d").date()
    departure_arrival_time = request.args.get('departure_arrival_time')
    duration = request.args.get('duration')
    price = request.args.get('price')
    seats = request.args.get('seats')
    #last_checked = 

    print(url)
    print(airline)
    print(departure)
    print(destination)
    print(departure_date)
    print(departure_arrival_time)
    print(duration)
    print(price)
    print(seats)

    if not airline or not departure or not destination:
        flash("There was a problem saving your flight. Please try again later.", "error")
        return redirect(url_for('views.saved_results'))
    
    existing_flight = TrackedFlights.query.filter_by(user_id=current_user.id,
                                                     departure=departure,
                                                     destination=destination,
                                                     departure_date=departure_date,
                                                     departure_arrival_time=departure_arrival_time
                                                    ).first()

    if existing_flight:
        flash("This flight is already saved.", "info")
        return redirect(url_for('views.saved_results'))
    

    try:
        new_flight = TrackedFlights(user_id = current_user.id,
                                    url = url,
                                    airline = airline,
                                    departure=departure,
                                    destination=destination,
                                    departure_date=departure_date,
                                    departure_arrival_time = departure_arrival_time,
                                    duration=duration,
                                    price=price,
                                    bookable_seats = seats,
                                    last_checked = datetime.now()
                                    )
    
        db.session.add(new_flight)
        db.session.commit()
        flash("Flight was saved.", "success")

    except Exception as e:
        db.session.rollback()
        flash("An error has occurred while saving the flight.", "error")
        print(e)

    return redirect(url_for('views.saved_results'))



@views.route("/saved-results")
@login_required
def saved_results():
    try:
        last_search = session.get('last_search')

        if not last_search:
            flash("No previous search found.", "error")
            return redirect(url_for('views.index'))

        departure = session.get('departure')
        destination = session.get('destination')
        departure_date = session.get('departure_date')
        arranged_flights = json.loads(last_search)

        return render_template("results.html", departure=departure, destination=destination, departure_date=departure_date, flights=arranged_flights, if_results="results-page")

    except Exception as e:
        flash("Could not reload your last search results.", "error")
        print(e)
        return redirect(url_for('views.index'))



@views.route("/search", methods=["GET", "POST"])
@login_required
def search_flights():
    from datetime import datetime, timedelta
    from utils.flight_data import load_json
    from utils.flight_utils import extract_airport_shorten

    MAX_RESULTS = 25

    #airport_list = ["Lisbon (LIS)", "Porto (OPO)", "Madrid (MAD)", "Barcelona (BCN)",
                    #"Paris (CDG)", "London (LHR)", "Frankfurt (FRA)", "Amsterdam (AMS)",
                    #"Rome (FCO)", "New York (JFK)"]

    airports = load_json("airports")

    airport_list = []

    for airport in airports:
        airport_name = f"{airport['code']} - {airport['name']}"
        airport_list.append(airport_name)

    if request.method == "POST":
        departure = request.form.get("departure")
        destination = request.form.get("destination")
        departure_date = request.form.get("departure_date")
        adults = int(request.form.get("adults"))

        print(departure)
        print(destination)


        if departure not in airport_list: 
            flash("Please select a valid Airport for Departure.", "error")
            return redirect(request.url)
        
        if destination not in airport_list: 
            flash("Please select a valid Airport for Destination.", "error")
            return redirect(request.url)
        
        if departure == destination:
            flash("Departure and Destination cannot be the same.", "error")
            return redirect(request.url)
        
        if not departure_date:# and not departure_range:
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
            
        """ if departure_range:
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
                return redirect(request.url) """
        
    
        if adults < 0 or adults > 9:
            flash("Invalid Adult number.", "error")
            return redirect(request.url)
            
        departure_shorten = extract_airport_shorten(departure)
        destination_shorten = extract_airport_shorten(destination)
        departure_date= departure_date.replace("/", "-")

        print("SEARCH FUNCTION")
        print(departure_shorten)
        print(destination_shorten)
        print(departure)
        print(destination)
        print(departure_date)
        print(adults)
        print(MAX_RESULTS)
        print("END SEARCH FUNCTION")
            
        #flash("Searching for your future flight.", "success")
        return redirect(url_for("views.results", departure=departure, departure_iata=departure_shorten,
                                destination=destination, destination_iata=destination_shorten, departure_date=departure_date,
                                adults=adults, max_results=MAX_RESULTS))

    return render_template("search.html", airport_list=airport_list)


@views.route("/account", methods=["GET", "POST"])
@login_required
def user_account():
    return render_template("account.html")
