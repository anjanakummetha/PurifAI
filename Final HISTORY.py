import sys
import requests
import json
from datetime import datetime, timedelta
from dateutil import parser, tz

# Get latitude and longitude for a city using Google Geocoding API
def get_coordinates(city_name):
    api_key = "AIzaSyDAanUpMZudipzPw2yh09be-Thru9Qk4oE"  # API key
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city_name}&key={api_key}"
    
    response = requests.get(geocode_url)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            location = results[0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None

# Get historical air quality data for a specific time and place
def get_historical_air_quality(dateTime, latitude, longitude):
    url = "https://airquality.googleapis.com/v1/history:lookup?key=AIzaSyDAanUpMZudipzPw2yh09be-Thru9Qk4oE"
    data = {
        "dateTime": dateTime,
        "location": {"latitude": latitude, "longitude": longitude}
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

# Extract relevant info (like AQI or dominant pollutant) from historical data
def extract_historical_info(query, historical_data):
    responses = []

    # Check for AQI in the query
    if any(term in query.upper() for term in ["AQI", "AIR QUALITY INDEX", "AQ_INDEX"]):
        aqi_info = historical_data.get("hoursInfo", [{}])[0].get("indexes", [])
        if aqi_info:
            aqi = aqi_info[0].get("aqi", "Unknown")
            category = aqi_info[0].get("category", "Unknown")
            responses.append(f"The Air Quality Index (AQI) at that time was {aqi}, which is considered {category}.")

    # Check for dominant pollutant in the query
    if any(term in query.upper() for term in ["DOMINANT POLLUTANT"]):
        dominant_pollutant = historical_data.get("hoursInfo", [{}])[0].get("indexes", [{}])[0].get("dominantPollutant", "Unknown")
        if dominant_pollutant != "Unknown":
            responses.append(f"The dominant pollutant at that time was {dominant_pollutant}.")
        else:
            responses.append("Sorry, I couldn't determine the dominant pollutant from the data.")

    if not responses:
        responses.append("Sorry, I couldn't figure out what you're asking for.")

    return responses

# Handle the historical data query by combining the above functions
def handle_query_historical_data(entities):
    city = entities.get("LOCATION", "Unknown Location")
    dateTime = entities.get("PAST_TIME", "Unknown Time")
    query = entities.get("QUERY", "")

    if city != "Unknown Location" and dateTime != "Unknown Time":
        latitude, longitude = get_coordinates(city)
        if not (latitude and longitude):
            return {"error": "Could not find location."}

        try:
            date_obj = parser.parse(dateTime)
            if date_obj.tzinfo is None:
                date_obj = date_obj.replace(tzinfo=tz.UTC)
        except Exception as e:
            return {"error": f"Couldn't parse the date/time. Error: {str(e)}"}

        now_utc = datetime.now(tz.UTC)
        if now_utc - date_obj > timedelta(days=30):
            return {"error": "Can only provide data for the past 30 days."}

        historical_data = get_historical_air_quality(date_obj.isoformat(), latitude, longitude)
        if not historical_data:
            return {"error": "Couldn't get historical air quality data."}
        
        responses = extract_historical_info(query, historical_data)
        return {"response": responses}
    else:
        return {"error": "Location or time not recognized"}

# Main function to handle command-line arguments
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Please provide a city, a date/time, and a query as command line arguments.")
        sys.exit(1)

    city = sys.argv[1]
    dateTime = sys.argv[2]
    query = sys.argv[3]

    response = handle_query_historical_data({"LOCATION": city, "PAST_TIME": dateTime, "QUERY": query})
    print(json.dumps(response, indent=2))
