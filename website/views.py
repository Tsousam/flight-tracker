from datetime import date, datetime
from flask import current_app, Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from sqlalchemy import update
from utils.flight_utils import arrange_flights_data, search_flight_offers
from website.models import User, TrackedFlights, asc, db
import json


views = Blueprint("views", __name__)

MAX_RESULTS = 25



@views.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":

        return render_template("index.html")
    
    # Delete outdated saved flights before calling the landing page.
    db.session.query(TrackedFlights).filter(TrackedFlights.departure_date < date.today()).delete()
    db.session.commit()
    
    # Fetch all saved flights and sort them into user_flights.
    user_flights = TrackedFlights.query.filter_by(user_id=current_user.id).order_by(asc(TrackedFlights.departure_date),asc(TrackedFlights.departure_arrival_time)).all()
    
    return render_template("index.html", flights=user_flights)



@views.route("/delete-flight", methods=["POST"])
@login_required
def delete_flight():
    carrier_code = request.form.get("carrier_code")
    flight_number = request.form.get("flight_number")

    flight = TrackedFlights.query.filter_by(user_id = current_user.id,
                                            carrier_code = carrier_code,
                                            flight_number = flight_number
                                            ).first()

    #print(flight)
    
    if not flight:
        flash("There was an error while trying to delete your flight.", "error")
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

    """ print(departure_iata)
    print(destination_iata)
    print(departure_date)
    print(adults)
    print(max_results) """

    fetch_flights = search_flight_offers(departure_iata, destination_iata, departure_date, adults, MAX_RESULTS)
    #print(fetch_flights)
    arranged_flights = arrange_flights_data(fetch_flights, departure, destination, adults)
    #print(arranged_flights)
    
    session['departure'] = departure
    session['destination'] = destination
    session['departure_date'] = departure_date
    session['last_search'] = json.dumps(arranged_flights)

    return render_template("results.html", departure=departure, destination=destination, departure_date=departure_date, flights=arranged_flights, if_results="results-page")



@views.route("/save-flight")
@login_required
def save_flight():
    url = request.args.get('url')
    carrier_code = request.args.get('carrier_code')
    flight_number = request.args.get('flight_number')
    airline = request.args.get('airline')
    departure_iata = request.args.get('departure_iata')
    destination_iata = request.args.get('destination_iata')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    departure_date = datetime.strptime(request.args.get('departure_date'), "%Y-%m-%d").date()
    departure_arrival_time = request.args.get('departure_arrival_time')
    duration = request.args.get('duration')
    price = request.args.get('price')
    adults = request.args.get('adults')
    seats = request.args.get('seats')

    """ print(url)
    print(airline)
    print(departure)
    print(destination)
    print(departure_date)
    print(departure_arrival_time)
    print(duration)
    print(price)
    print(seats) """

    if not airline or not departure or not destination:
        flash("There was a problem saving your flight. Missing data.", "error")
        return redirect(url_for('views.saved_results'))
    
    existing_flight = TrackedFlights.query.filter_by(user_id = current_user.id,
                                                     carrier_code = carrier_code,
                                                     flight_number = flight_number,
                                                    ).first()

    if existing_flight:
        flash("The flight was already saved.", "info")
        return redirect(url_for('views.saved_results'))
    

    try:
        new_flight = TrackedFlights(user_id = current_user.id,
                                    carrier_code = carrier_code,
                                    flight_number = flight_number,
                                    url = url,
                                    airline = airline,
                                    departure_iata = departure_iata,
                                    destination_iata = destination_iata,
                                    departure = departure,
                                    destination = destination,
                                    departure_date = departure_date,
                                    departure_arrival_time = departure_arrival_time,
                                    duration = duration,
                                    price = price,
                                    adults = adults,
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

        #print(departure)
        #print(destination)


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

        """ print(departure_shorten)
        print(destination_shorten)
        print(departure)
        print(destination)
        print(departure_date)
        print(adults)
        print(MAX_RESULTS) """
            
        #flash("Searching for your future flight.", "success")
        return redirect(url_for("views.results", departure=departure, departure_iata=departure_shorten,
                                destination=destination, destination_iata=destination_shorten, departure_date=departure_date,
                                adults=adults, max_results=MAX_RESULTS))

    return render_template("search.html", airport_list=airport_list)



@views.route("/update-flight", methods=["POST"])
@login_required
def update_flight():
    carrier_code = request.form.get("carrier_code")
    flight_number = request.form.get("flight_number")
    departure_iata = request.form.get("departure_iata")
    destination_iata = request.form.get("destination_iata")
    departure_date = request.form.get("departure_date")
    adults = request.form.get("adults")

    """print(carrier_code)
    print(flight_number)
    print(departure_iata)
    print(destination_iata)
    print(departure_date)
    print(adults)"""


    flight = TrackedFlights.query.filter(TrackedFlights.user_id == current_user.id,
                                         TrackedFlights.carrier_code == carrier_code,
                                         TrackedFlights.flight_number == flight_number,
                                         TrackedFlights.departure_date < date.today()
                                        ).first()

    if flight:
        flash("Flight was already departed.", "error")
        return redirect(url_for('views.saved_results'))
    

    fetch_flights = search_flight_offers(departure_iata, destination_iata, departure_date, adults, MAX_RESULTS)


    for flight in fetch_flights:
        if carrier_code == flight["itineraries"][0]["segments"][0]["carrierCode"] and flight_number == flight["itineraries"][0]["segments"][0]["number"]:

            ############################# Temporary fix #############################
            if flight["price"]["currency"] == "EUR":
                flight["price"]["currency"] = "€"

            ############################# Temporary fix #############################
            if flight["price"]["currency"] == "DOL":
                flight["price"]["currency"] = "$"

            if "." in flight["price"]["total"]:
                flight_total = flight["price"]["total"].split(".")
                flight["price"]["total"] = flight_total[0]

            try:
                update_flight = update(TrackedFlights).where(TrackedFlights.user_id == current_user.id,
                                                            TrackedFlights.carrier_code == carrier_code,
                                                            TrackedFlights.flight_number == flight_number
                                                            ).values(
                                                                price = f'{flight["price"]["total"]}{flight["price"]["currency"]}',
                                                                bookable_seats = flight["numberOfBookableSeats"],
                                                                last_checked = datetime.now()
                                                            )
                db.session.execute(update_flight)
                db.session.commit()
            
                flash("Flight was updated.", "success")
                return redirect(url_for('views.index'))

            except Exception as e:
                db.session.rollback()
                flash("An error has occurred while updating the flight.", "error")
                print(e)
                return redirect(url_for('views.index'))

    flash("There was a problem updating the flight.", "error")
    return redirect(url_for('views.index'))



@views.route("/account", methods=["GET", "POST"])
@login_required
def user_account():
    return render_template("account.html")
