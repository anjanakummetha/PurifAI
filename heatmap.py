#api_key = os.getenv('API_KEY')
import requests

api_key = "API_KEY"
type_heatmap = "US_AQI"
zoom_level = "2"
x_coordinate = "0"
y_coordinate = "1"
api_base_url = "https://airquality.googleapis.com/v1/mapTypes"

# url with required parameters
url = f"{api_base_url}/{type_heatmap}/heatmapTiles/{zoom_level}/{x_coordinate}/{y_coordinate}?key={api_key}"
#https://airquality.googleapis.com/v1/mapTypes/US_AQI/heatmapTiles/2/0/1?key=API_KEY


# request to retrieve url
response = requests.get(url)

# save the heat map as a file
if response.status_code == 200:
    with open('heatmap_Test.png', 'wb') as file:
        file.write(response.content)
    print("Heatmap tile saved")
else:
    # If the request failed, print the below statement
    print(f"Error Status code: {response.status_code}")
