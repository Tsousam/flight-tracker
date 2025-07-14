import re
from amadeus import ResponseError
from services.amadeus_client import amadeus
import airportsdata


airports = airportsdata.load('IATA')


def arrange_flights_data(flights_fetch_response):
    # KEY EXAMPLE VALUES:
    # airline: "TP"
    # departure: "LIS"
    # destination: "FCO"
    # at: "2025-06-10T09:15:00"
    # duration: "PT22H15M"
    # price: "152.95"
    # currency: "EUR"
    # bookable_seats: 3

    from utils.load_airlines_data import get_airline_name, get_airline_url

    flights = []
    for flight in flights_fetch_response:
        flight_code = flight["validatingAirlineCodes"][0]
        airline_url = get_airline_url(flight_code)
        airline_name = get_airline_name(flight_code)
        departure_airport = get_airport_name(flight["itineraries"][0]["segments"][0]["departure"]["iataCode"])
        destination_airport = get_airport_name(flight["itineraries"][0]["segments"][-1]["arrival"]["iataCode"])
        departure_datetime_split = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")
        departure_date = departure_datetime_split[0]
        departure_hours = departure_datetime_split[1]
        arrival_datetime_split = flight["itineraries"][0]["segments"][-1]["arrival"]["at"].split("T")
        arrival_hours = arrival_datetime_split[1]
        duration_split = flight["itineraries"][0]["duration"].split("T")

        ############################# Temporary fix #############################
        if flight["price"]["currency"] == "EUR":
            flight["price"]["currency"] = "€"

        ############################# Temporary fix #############################
        if flight["price"]["currency"] == "DOL":
            flight["price"]["currency"] = "$"

        if "." in flight["price"]["total"]:
            flight_total = flight["price"]["total"].split(".")
            flight["price"]["total"] = flight_total[0]

        if len(departure_hours) > 5:
            departure_hours = departure_hours[:5]

        if len(arrival_hours) > 5:
            arrival_hours = arrival_hours[:5]

        print(f'{departure_hours} - {arrival_hours}')


        flights.append({"id": flight["id"],
                        "url": airline_url,
                        "airline": airline_name,
                        "departure": departure_airport,
                        "destination": destination_airport,
                        "departure_date": departure_date,
                        "departure_arrival_time": f'{departure_hours} - {arrival_hours}',
                        "duration": duration_split[1],
                        "price": f'{flight["price"]["total"]}{flight["price"]["currency"]}',
                        "bookable_seats": flight["numberOfBookableSeats"]
                        })
    return flights


def extract_airport_shorten(airport):
    if not airport:
        return None

    match = re.search(r"\((\w{3})\)", airport)
    if match:
        return match.group(1)
    return None

""" def get_airline_name(airline_code):
    try:
        response = amadeus.reference_data.airlines.get(airlineCodes=airline_code)
        return response.data[0]['businessName'].title()
    except Exception:
        return airline_code """


def get_airport_name(airport_code):
    data = airports.get(airport_code.strip().upper())
    if data:
        return f'{data["city"]} ({airport_code}) – {data["name"]}'
    return airport_code


def save_flight(flight_id):
    return None



def search_flight_offers(departure, destination, departure_date, adults, max_results):
    try:
        # Flight Offers Search to search for flights from X to Y
        flight_search = amadeus.shopping.flight_offers_search.get(originLocationCode="LIS",
                                                                destinationLocationCode="FCO",
                                                                departureDate="2025-07-17",
                                                                # If round trip
                                                                #returnDate="2025-06-17", 
                                                                adults=adults,
                                                                max=max_results
                                                                )

        #print(flight_search.data)
        return flight_search.data

    except ResponseError as error:
        print(error)