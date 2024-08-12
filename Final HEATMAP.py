import requests
import sys
import os  # Import os module for file paths and directories
from NER_model import recognize_entities
from intent_recognition import load_model, predict_intent

# This function returns the map details for a given location
def get_location_data(location):
    location_data = {
        "world": {"map_type": "US_AQI", "zoom_level": 0, "x_tile": 0, "y_tile": 0},
        "europe": {"map_type": "US_AQI", "zoom_level": 2, "x_tile": 2, "y_tile": 1},
        "asia": {"map_type": "US_AQI", "zoom_level": 2, "x_tile": 3, "y_tile": 1},
        "north america": {"map_type": "US_AQI", "zoom_level": 1, "x_tile": 0, "y_tile": 0},
        "south america": {"map_type": "US_AQI", "zoom_level": 2, "x_tile": 1, "y_tile": 2},
        "oceania": {"map_type": "US_AQI", "zoom_level": 2, "x_tile": 3, "y_tile": 2},
        "australia": {"map_type": "US_AQI", "zoom_level": 2, "x_tile": 3, "y_tile": 2},
        "africa": {"map_type": "US_AQI", "zoom_level": 2, "x_tile": 2, "y_tile": 1},
    }
    # Return the map details for the location, or none if invalid location
    return location_data.get(location.lower(), None)

# Creating a heatmap image for the specified location
def generate_heatmap(api_key, map_type, zoom_level, x_tile, y_tile, location):
    api_base_url = "https://airquality.googleapis.com/v1/mapTypes"
    url = f"{api_base_url}/{map_type}/heatmapTiles/{zoom_level}/{x_tile}/{y_tile}?key={api_key}"

    # SSending a request to get the heatmap image
    response = requests.get(url)
    if response.status_code == 200:
        filename = f'heatmap_{map_type}_{zoom_level}_{x_tile}_{y_tile}.png'
        file_path = os.path.join('heatmaps', filename)  # Set the path to save the heatmap image

        # Create the heatmaps directory
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save the heatmap image to the specified path
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        # Generate the URL to access the saved heatmap image
        heatmap_url = f"http://localhost:3003/heatmaps/{filename}"
        return {"status": "success", "message": f"Here's the heatmap for {location}:", "url": heatmap_url}
    else:
        # Print an error if it doesn't work
        print(f"Error generating heatmap: {response.content}")
        return {"status": "error", "message": "Could not generate heatmap."}
    
# This function handles the intent to view heatmaps based on the user query
def handle_view_heatmaps(entities):
    # Get location from recognized entities in the user query
    location = entities.get("LOCATION", "").strip()
    
    if location:
        # Map details for the specified location
        location_data = get_location_data(location)
        
        if location_data:
            # Get map details
            map_type = location_data["map_type"]
            zoom_level = location_data["zoom_level"]
            x_tile = location_data["x_tile"]
            y_tile = location_data["y_tile"]
            
            # Generate the heatmap and return it
            return generate_heatmap("AIzaSyDAanUpMZudipzPw2yh09be-Thru9Qk4oE", map_type, zoom_level, x_tile, y_tile, location)
        else:
            # Return an error if the location isn't right
            return {"status": "error", "message": "Invalid location provided."}
    else:
        # Return an error if the location is missing
        return {"status": "error", "message": "Could not determine location from the query."}
