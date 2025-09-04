import json
import pickle
import re

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam


class CallAnalysisPredictor:
    """
    Class for making predictions on new data
    """
    def __init__(self):
        self.profanity_components = None
        self.sensitive_model = None
        self.sensitive_vectorizer = None
        
    def load_models(self):
        """
        Load trained models
        """
        # Load profanity model
        with open('ml_model/profanity_model.pkl', 'rb') as f:
            self.profanity_components = pickle.load(f)
        
        # Load sensitive data model
        self.sensitive_model = tf.keras.models.load_model('ml_model/sensitive_model.h5')
        
        with open('ml_model/sensitive_vectorizer.pkl', 'rb') as f:
            self.sensitive_vectorizer = pickle.load(f)
    
    def preprocess_json_input(self, json_string):
        """
        Preprocess JSON input for prediction
        Args:
            json_string: JSON string of conversation
        Returns:
            processed_text: Clean text for prediction
        """
        try:
            conversation_list = json.loads(json_string)
            all_text = []
            
            for item in conversation_list:
                if 'text' in item:
                    all_text.append(item['text'])
            
            combined_text = " ".join(all_text)
            combined_text = combined_text.lower()
            combined_text = re.sub(r'[^\w\s]', ' ', combined_text)
            combined_text = re.sub(r'\s+', ' ', combined_text).strip()
            
            return combined_text
        except:
            return ""
    
    def predict_profanity(self, json_string):
        """
        Predict profanity in conversation
        """
        processed_text = self.preprocess_json_input(json_string)
        
        # Transform text
        text_tfidf = self.profanity_components['vectorizer'].transform([processed_text])
        
        # Predict
        prediction = self.profanity_components['model'].predict(text_tfidf)[0]
        
        # Convert back to label
        label_classes = self.profanity_components['label_encoder'].classes_
        result = label_classes[prediction]
        
        return result
    
    def predict_sensitive_data(self, json_string):
        """
        Predict sensitive data compliance violation
        """
        processed_text = self.preprocess_json_input(json_string)
        
        # Transform text
        text_tfidf = self.sensitive_vectorizer.transform([processed_text]).toarray()
        
        # Predict
        prediction = self.sensitive_model.predict(text_tfidf)[0][0]
        
        # Convert to binary classification
        result = "found" if prediction > 0.5 else "not found"
        
        return result