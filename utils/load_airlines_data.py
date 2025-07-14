import json
import os
from functools import lru_cache


# Load Airline URLs from JSON file at startup
@lru_cache()
def load_airlines_data():
    path = os.path.dirname(__file__)
    file_path = os.path.join(path, '..', 'data', 'airlines_data.json')
    file_path = os.path.abspath(file_path)
    
    with open(file_path) as file:
        return json.load(file)
    
def get_airline_name(airline_code):
    airlines = load_airlines_data()
    return airlines.get(airline_code, {}).get('name', airline_code)

    
def get_airline_url(airline_code):
    airlines = load_airlines_data()
    return airlines.get(airline_code, {}).get('url', None)