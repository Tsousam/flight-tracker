import json
import os
from functools import lru_cache


# Load from JSON file at startup
@lru_cache()
def load_json(file_name):
    path = os.path.dirname(__file__)
    file_path = os.path.join(path, "..", "data", f"{file_name}.json")
    file_path = os.path.abspath(file_path)
    
    with open(file_path) as file:
        return json.load(file)

    
def get_airline_name(airline_code):
    airlines = load_json("airlines_data")
    return airlines.get(airline_code, {}).get("name", airline_code)

    
def get_airline_url(airline_code):
    airlines = load_json("airlines_data")
    return airlines.get(airline_code, {}).get("url", None)