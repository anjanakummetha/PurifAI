import sys
import json
from intent_recognition import load_model, predict_intent
from NER_model import recognize_entities
from CHECK_CURRENT_CONDITIONS import handle_check_current_conditions
from HISTORY import handle_query_historical_data
from HEATMAP import handle_view_heatmaps

# Function for handling the user's query
def handle_query(query, model, vectorizer):
    # Use IR for intent
    intent = predict_intent(query, model, vectorizer)
    
    # Recognize entities 
    entities = recognize_entities(intent, query)
    
    # print the recognized entities to check
    print(f"Recognized Entities: {entities}")
    
    # Attach the original query to check
    entities['QUERY'] = query
    
    # print intent to check
    print(f"Handling intent: {intent}")

    # Handle the query based on the predicted intent
    if intent == "CHECK_CURRENT_CONDITIONS":
        # current air quality conditions
        result = handle_check_current_conditions(entities)
    elif intent == "QUERY_HISTORICAL_DATA":
        # historical air quality data
        result = handle_query_historical_data(entities)
    elif intent == "VIEW_HEATMAPS":
        # heatmaps
        result = handle_view_heatmaps(entities)
        
        # If a heatmap URL was generated, format the message to show only the filename
        heatmap_url = result.get('url', None)
        if heatmap_url:
            result['message'] = f"Here's the heatmap for {entities['LOCATION']}: {heatmap_url.split('/')[-1]}"
    else:
        # When intent wasn't recognized
        result = {"error": "Intent not recognized"}
    
    # Convert to a JSON string and return the result
    return json.dumps(result)

# Main script entry point
if __name__ == "__main__":
    # Check if a query was provided as a command-line argument
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No query provided"}))
        sys.exit(1)

    # Get the query from the command-line arguments
    query = sys.argv[1]

    # Load the intent recognition model and vectorizer
    filepath = "Intent_Data.csv"
    model, vectorizer = load_model(filepath)

    # Process the query using the combined models
    response = handle_query(query, model, vectorizer)

    # Print the response (as a JSON string) to the console
    print(response)
