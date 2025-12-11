# Air Quality Chatbot
A Python-based system for interpreting natural-language queries about air quality, extracting user intent and entities, and retrieving information from the Google Air Quality API.
The project includes modules for current conditions, historical data, and heatmap generation, along with a custom NER model and a simple intent-recognition model.

## Table of Contents
* [Overview](#overview)
* [Features](#features)
* [Installation](#installation)
* [Environment Variables](#environment-variables)
* [Project Structure](#project-structure)
* [Usage](#usage)
* [Module Descriptions](#module-descriptions)
* [Limitations](#limitations)

## Overview 
The system takes a user query (e.g., “What’s the AQI in Dallas today?”), identifies:
* Intent (current conditions, historical data, heatmap)
* Entities (location, pollutant type, population group, time)
and routes the request to the correct module.

Data is retrieved using:
* Google Geocoding API → converts location to coordinates
* Google Air Quality API → retrieves air quality data

The project also includes:
* A custom spaCy NER model
* An intent recognition model
Standalone scripts for current conditions, history, and heatmaps

## Features 
### Natural Language Processing
spaCy NER trained to identify:
* Location names
* Groups (children, elderly, athletes, etc.)
* AQI-related tags (AQ_INDEX, DOMINANT_POLLUTANT, HEALTH_RECOMMENDATIONS)
Simple intent recognition model using scikit-learn

### API-Based Air Quality Retrieval
* Current conditions (AQI, dominant pollutant, health recommendations)
* Historical pollutant data
* Lat/long lookup through Google Geocoding

### Heatmap Generation
* Grid-based coordinate sampling
* Requests AQI values for each cell
* Produces a heatmap image using Pillow + Matplotlib

### Routing Logic
Combined script that:
* Loads intent model
* Runs NER
* Routes request to the correct module

## Installation
Clone the repository and install dependencies:

pip install -r requirements.txt
python -m spacy download en_core_web_sm

If you want to retrain the NER model:
python Final\ NER_model_training.py

## Environment Variables 
Add Google API keys in the code where placeholders say: ADD_API_KEY_HERE

Required keys:
* Google Geocoding API Key
* Google Air Quality API Key

## Project Structure 

Final combined.py
* Main system orchestrator
Final CHECK_CURRENT_CONDITIONS
* Current AQI and health recommendations
Final HISTORY.py
* Historical air quality queries
Final HEATMAP.py
* AQI heatmap generation
intent_recognition.py
* ML model for intent classification
NER_model.py
* spaCy NER model loading + entity extraction
NER_model_training.py
* Script for custom NER training

index.js                        
* Front-end/server integration (JavaScript)

currentConditions.py             
* Earlier version of current conditions logic
history.py
* Earlier version of history logic
heatmap.py
* Earlier version of heatmap logic
requirements.txt
* Dependencies


## Usage
Running main system:
python "Final combined.py"


## Module Descriptions

1. intent_recognition.py
* Loads a trained ML model
* Predicts high-level user intent such as:
* CHECK_CURRENT_CONDITIONS
* CHECK_HISTORY
* HEATMAP

2. NER_model.py
* Loads spaCy model
Extracts entities:
* LOCATION
* AQ_INDEX
* HEALTH_RECOMMENDATIONS
* DOMINANT_POLLUTANT
* CHILDREN, ELDERLY, ATHLETES, etc.

3. Final CHECK_CURRENT_CONDITIONS
* Takes entities from NER
* Retrieves coordinates via Google Geocoding
* Calls Google Air Quality API
Returns:
* AQI
* Health recommendations
* Dominant pollutant

4. Final HISTORY.py
* Similar structure to current conditions
* Queries historical pollutant concentration
* Requires date entity

6. Final HEATMAP.py
* Builds a lat/long grid around provided location
* Calls AQI endpoint for each coordinate
* Generates PNG heatmap

7. Final combined.py
* Central script that:
* Loads intent & NER models
* Routes query
* Formats response

## Limitations

* API keys must be manually inserted
* Basic error handling 
* No frontend UI except the placeholder index.js
* NER model accuracy depends on limited training data
* No caching of API responses


