import re



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

    flights = []
    for flight in flights_fetch_response:
        departure = flight["itineraries"][0]["segments"][0]
        destination = flight["itineraries"][0]["segments"][-1]
        departure_datetime_split = departure["departure"]["at"].split("T")
        destination_datetime_split = departure["arrival"]["at"].split("T")
        duration_split = flight["itineraries"][0]["duration"].split("T")
        #price = f'{flight["price"]["total"]} {flight["price"]["currency"]}'

        flights.append({
            "airline": flight["validatingAirlineCodes"][0],
            "departure": departure["departure"]["iataCode"],
            "destination": destination["arrival"]["iataCode"],
            "departure_date": departure_datetime_split[0],
            "departure_arrival_time": f'{departure_datetime_split[1]} - {destination_datetime_split[1]}',
            "duration": duration_split[1],
            "price": f'{flight["price"]["total"]} {flight["price"]["currency"]}',
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