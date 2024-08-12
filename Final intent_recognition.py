import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os
import numpy as np

def add_temporal_features(df):
    # Add features to detect past tense indicators and presence of dates
    df['has_past_indicator'] = df['Query'].apply(lambda x: 1 if any(word in x.lower() for word in ['was', 'on', 'ago', 'last', 'yesterday', 'previous', 'earlier']) else 0)
    df['has_date'] = df['Query'].apply(lambda x: 1 if any(char.isdigit() for char in x) else 0)
    
    # Add features for detecting current condition indicators
    df['has_current_condition_indicator'] = df['Query'].apply(lambda x: 1 if any(phrase in x.lower() for phrase in ['health recommendations', 'health recommendation']) else 0)
    
    return df

def train_and_update_model(filepath, incremental=False):
    # Load and preprocess data
    data = pd.read_csv(filepath)
    data = add_temporal_features(data)
    
    texts = data['Query']
    labels = data['Intent']

    # Create TF-IDF vectors from the text queries
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2), stop_words='english')
    X = vectorizer.fit_transform(texts)
    
    # Combine TF-IDF features with custom temporal features
    temporal_features = data[['has_past_indicator', 'has_date', 'has_current_condition_indicator']].values
    X_combined = np.concatenate([X.toarray(), temporal_features], axis=1)

    print("Number of features during training:", X_combined.shape[1])  # Output number of features

    y = labels

    # Load existing model for incremental training or train a new one
    if incremental and os.path.exists('model.pkl'):
        model = joblib.load('model.pkl')
        model.partial_fit(X_combined, y)
    else:
        model = LogisticRegression(max_iter=1000)  # Train with more iterations for convergence
        model.fit(X_combined, y)
    
    # Save the trained model and vectorizer
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    
def load_model(filepath=None):
    # Load the trained model and vectorizer, or train a new one if not found
    if not os.path.exists('model.pkl') or not os.path.exists('vectorizer.pkl'):
        if filepath:
            train_and_update_model(filepath)
        else:
            raise FileNotFoundError("Model and vectorizer files not found; no filepath provided to train a new model.")
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    return model, vectorizer

def predict_intent(query, model, vectorizer):
    # Handle queries that match specific conditions directly
    if any(phrase in query.lower() for phrase in ['health recommendations', 'health recommendation']):
        print(f"Mandatory match for current conditions identified in query: '{query}'")
        return "CHECK_CURRENT_CONDITIONS"
    
    if 'was' in query.lower():
        print(f"Mandatory match for historical data identified in query: '{query}'")
        return "QUERY_HISTORICAL_DATA"
    
    # Vectorize the query and add custom features
    query_vec = vectorizer.transform([query]).toarray()
    past_indicator = 1 if any(word in query.lower() for word in ['was', 'on', 'ago', 'last', 'yesterday', 'previous', 'earlier']) else 0
    date_indicator = 1 if any(char.isdigit() for char in query) else 0
    current_condition_indicator = 1 if any(phrase in query.lower() for phrase in ['health recommendations', 'health recommendation']) else 0
    
    query_features = np.array([past_indicator, date_indicator, current_condition_indicator])
    query_combined = np.concatenate((query_vec, query_features.reshape(1, -1)), axis=1)

    print("Number of features during prediction:", query_combined.shape[1])  # Output number of features during prediction

    # Predict intent based on the combined features
    prediction = model.predict(query_combined)
    print(f"Predicted intent for query '{query}': {prediction[0]}")
    return prediction[0]

if __name__ == "__main__":
    filepath = "Intent_Data.csv"
    query = "What are the health recommendations for children in Chicago?"

    # Train the model if needed, then load it
    train_and_update_model(filepath, incremental=False)
    
    model, vectorizer = load_model(filepath)
    intent = predict_intent(query, model, vectorizer)
    print(intent)
