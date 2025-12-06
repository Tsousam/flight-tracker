# ✈️ Flight Tracker  

A Flask-based web application to search, track, and update flight offers. The app integrates with external flight API - Amadeus - and provides users with the ability to save, monitor, and update flight prices and availability over time.  


## Features  

- **User Authentication** (Flask-Login)  
- **Flight search & results** via Amadeus API (JSON responses parsed into structured results)  
- **Save tracked flights** to a local database (SQLite / any SQLAlchemy-supported DB)  
- **Automatic departure validation** (flights past departure date are filtered or removed)  
- **Update tracked flights**: refresh price, bookable seats, and last-checked timestamp  
- **Session management** with Flask-Session (store last search, departure/destination info, etc.)  
- **Search parameters**: departure, destination, date, adults (1–9)  
- **Database schema** with SQLAlchemy (TrackedFlights, User, etc.)  


## Tech Stack  

- **Backend**: Flask 3.1, Flask-Login, Flask-SQLAlchemy  
- **Frontend**: HTML, Bootstrap 5, JavaScript  
- **Database**: SQLite
- **APIs**: Amadeus (flight search & availability)
- **Libraries**: airportsdata (IATA metadata lookup) 
- **Caching & Session**: Flask-Session, Redis
- **Data Format**: REST/JSON  
- **Environment**: Python 3.13 + dotenv for API keys  


## Clean Flask MVC structure

- **Models**: SQLAlchemy models (User, TrackedFlights)
- **Views**: HTML templates rendered with Jinja2
- **Controllers**: Flask route functions handling form submissions, session logic, and DB operations


## Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/Tsousam/flight-tracker.git
   cd flight-tracker
   ```

2. Create and activate a virtual environment:  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:  
   First, copy the example file and rename it:  
   ```bash
   cp .env.example .env
   ```
   Then open .env and fill in your own values:
   ```ini
   SECRET_KEY=your_secret_key
   AMADEUS_API_KEY=your_api_key
   AMADEUS_API_SECRET=your_api_secret
   ```

5. Run the app:  
   ```bash
   flask run
   ```


## Models Overview  

### `TrackedFlights`  
Stores all saved flights for each user.  
```python
id                      # Primary key
user_id                 # Foreign key to User
carrier_code            # Airline code (e.g., DL)
flight_number           # Flight number (e.g., 2307)
airline                 # Full airline name
departure_iata          # Origin airport code (e.g., OPO)
destination_iata        # Destination airport code (e.g., LIS)
departure               # Full departure name
destination             # Full destination name
departure_date          # Date of flight
departure_arrival_time  # String "HH:MM - HH:MM"
duration                # Flight duration
price                   # Stored as string "123€"
adults                  # Number of passengers (1–9)
bookable_seats          # Seats available
last_checked            # Last updated timestamp
```

---

## Example Workflow  

1. **Search for flights** by entering departure, destination, date, and number of adults.  
2. **Results page** displays offers (`LIS - Humberto Delgado Airport -> Warsaw Chopin Airport` etc.).  
3. **Save a flight** → stored in DB with full details.  
4. **Update a flight** → checks if still available, refreshes price/seats.  
5. If flight’s **departure date < today**, app prevents updates and alerts the user.  

---

## Requirements  

`requirements.txt`  
```
Flask~=3.1
Flask-SQLAlchemy~=3.1
python-dotenv~=1.1
Flask_Session~=0.8
Flask-Login~=0.6
redis~=6.1
amadeus~=12.0
airportsdata~=20250622
```

---

## API Notes  

- **Amadeus API** provides itineraries, segments, carrier codes, IATA codes, and price/seat info.  
- JSON parsing extracts:  
  - `carrierCode` -> airline code  
  - `number` -> flight number  
  - `departure.iataCode` -> origin  
  - `arrival.iataCode` -> destination  
  - `price.total` + `price.currency` -> formatted string  
  - `numberOfBookableSeats`

---

## Future Improvements  

- Automated email alerts (SendGrid/Mailgun)  
- Background task scheduling with Celery + Redis  
- User preferences (price alerts)  

---

## Author  

Tiago Martins  
- [GitHub](https://github.com/Tsousam)  