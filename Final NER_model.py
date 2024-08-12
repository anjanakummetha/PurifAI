import sys
import spacy
import json

# Load the custom NER model trained for air quality data
nlp_ner = spacy.load("air_quality_ner_model")

def recognize_entities(intent, text):
    # Process the text using the NER model
    doc = nlp_ner(text)
    
    # Define which entities to extract based on the specific intent
    intent_entities = {
        "CHECK_CURRENT_CONDITIONS": ["AQ_INDEX", "DOMINANT_POLLUTANT", "HEALTH_RECOMMENDATIONS", "ELDERLY", "LUNG_DISEASES", "HEART_DISEASES", "ATHLETES", "PREGNANT_WOMEN", "CHILDREN", "LOCATION"],
        "QUERY_HISTORICAL_DATA": ["LOCATION", "PAST_TIME", "DOMINANT_POLLUTANT", "AQ_INDEX"],
        "VIEW_HEATMAPS": ["LOCATION"]
    }

    # Extract entities that match the intent's list
    entities = {ent.label_: ent.text for ent in doc.ents if ent.label_ in intent_entities.get(intent, [])}
    return entities

if __name__ == "__main__":
    # Expecting an intent and a query as command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python script.py <intent> <query>")
        sys.exit(1)
    
    intent = sys.argv[1]
    query = sys.argv[2]

    # Recognize and print the entities from the query
    entities = recognize_entities(intent, query)
    print(json.dumps(entities, indent=2))
