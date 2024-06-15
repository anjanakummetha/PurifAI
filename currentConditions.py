import requests
import json

def get_coordinates(city):
    #Use Google Maps Geocoding 
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"

    # parameters for geocoding request
    params = {
        "address": city,
        "key": "API_KEY"
    }

    # send a request to geocoding API
    geocode_response = requests.get(geocode_url, params=params)

    # get info
    if geocode_response.status_code == 200:
        results = geocode_response.json()["results"]
        if results:
            location = results[0]["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            return latitude, longitude
    else:
        print(f"Error. Status code: {geocode_response.status_code}, Message: {geocode_response.text}")
        return None, None

def get_air_quality(latitude, longitude):
    # API endpoint url
    url = "https://airquality.googleapis.com/v1/currentConditions:lookup?key=API_KEY"

    # request information
    data = {
        "universalAqi": True,
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "extraComputations": [
            "HEALTH_RECOMMENDATIONS",
            "DOMINANT_POLLUTANT_CONCENTRATION",
            "POLLUTANT_CONCENTRATION",
            "LOCAL_AQI",
            "POLLUTANT_ADDITIONAL_INFO"
        ],
        "languageCode": "en"
    }

    # set headers
    headers = {'Content-Type': 'application/json'}

    # send POST request
    response = requests.post(url, data=json.dumps(data), headers=headers)

    # print results
    if response.status_code == 200:
        print("Requested data::", response.json())
    else:
        print(f"Request failed. Status code: {response.status_code}, Message: {response.text}")

# test by requesting information from Albany
city = "Albany"
latitude, longitude = get_coordinates(city)

if latitude and longitude:
    get_air_quality(latitude, longitude)
else:
    print("Error")

