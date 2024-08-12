import spacy
from spacy.training import Example
import NER_train_data 

# Convert the data to SpaCy's required format
def convert_training_data(data):
    converted_data = []
    for text, annotations in data:
        entities = []
        for entity in annotations["entities"]:
            entity_text, label = entity
            start_idx = text.find(entity_text)
            end_idx = start_idx + len(entity_text)
            entities.append((start_idx, end_idx, label))
        converted_data.append((text, {"entities": entities}))
    return converted_data

TRAIN_DATA = convert_training_data(NER_train_data.TRAIN_DATA)

# Load a pre-existing model
nlp = spacy.load("en_core_web_sm")

# Get the NER component
ner = nlp.get_pipe("ner")

# Add new labels to the NER component
labels = [
    "LOCATION", "DOMINANT_POLLUTANT", 
    "HEALTH_RECOMMENDATIONS", "ELDERLY", 
    "LUNG_DISEASES", "HEART_DISEASES", "ATHLETES", 
    "PREGNANT_WOMEN", "CHILDREN", "AQ_INDEX", "PAST_TIME"
]
for label in labels:
    ner.add_label(label)

# Disable other pipeline components to only train NER
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    # Initialize the training process
    nlp.initialize()
    for i in range(20):  # Number of iterations
        print(f"Iteration {i}")
        losses = {}
        for text, annotations in TRAIN_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], losses=losses)
        print(losses)

# Save the model
nlp.to_disk("air_quality_ner_model")
