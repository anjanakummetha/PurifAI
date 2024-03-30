import requests
import json

# variables for time and city
city = "Albany"
# This time is March 26th, 2024 3pm UTC
dateTime = "2024-03-26T15:00:00Z" 

def get_coordinates(city):
    # use Google Maps Geocoding 
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    # parameters for geocoding request
    params = {
        "address": city,
        "key": "AIzaSyDAanUpMZudipzPw2yh09be-Thru9Qk4oE"
    }
    
    # send request to geocoding API
    geocode_response = requests.get(geocode_url, params=params)
    
    # get the information
    if geocode_response.status_code == 200:
        results = geocode_response.json()["results"]
        if results:
            location = results[0]["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            return latitude, longitude
    else:
        print(f"Error Status code: {geocode_response.status_code}, Message: {geocode_response.text}")
        return None, None

def get_historical_air_quality(dateTime, latitude, longitude):
    # url for history endpoint
    url = "https://airquality.googleapis.com/v1/history:lookup?key=AIzaSyDAanUpMZudipzPw2yh09be-Thru9Qk4oE"
    
    # requested information 
    data = {
        "dateTime": dateTime,
        "location": {
            "latitude": latitude,
            "longitude": longitude
        }
    }
    
    # headers for request
    headers = {'Content-Type': 'application/json'}
    
    # send the POST request
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # check if the request was successful
    if response.status_code == 200:
        print("Response data:", response.json())
    else:
        print(f"Request failed. Status code: {response.status_code}, Message: {response.text}")

# get longitude and latitude of the city
latitude, longitude = get_coordinates(city)

# request historical air quality once you have the coordinates
if latitude and longitude:
    get_historical_air_quality(dateTime, latitude, longitude)
else:
    print("Error")

