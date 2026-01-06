"""
ML Model Loader Utility
Loads trained ML models on startup
"""

import pickle
import os
from config import Config


class MLModels:
    """Singleton class to load and store ML models"""
    
    _instance = None
    _models_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLModels, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._models_loaded:
            self.load_models()
            MLModels._models_loaded = True
    
    def load_models(self):
        """Load all ML models"""
        models_path = Config.ML_MODELS_PATH
        
        print("\n" + "=" * 60)
        print("LOADING ML MODELS")
        print("=" * 60)
        
        try:
            # Load complaint classifier
            print("\n[1/5] Loading complaint classifier...")
            with open(os.path.join(models_path, 'complaint_classifier.pkl'), 'rb') as f:
                self.complaint_classifier = pickle.load(f)
            print("   ✓ Complaint classifier loaded")
            
            # Load TF-IDF vectorizer
            print("\n[2/5] Loading TF-IDF vectorizer...")
            with open(os.path.join(models_path, 'tfidf_vectorizer.pkl'), 'rb') as f:
                self.tfidf_vectorizer = pickle.load(f)
            print("   ✓ TF-IDF vectorizer loaded")
            
            # Load payment predictor
            print("\n[3/5] Loading payment predictor...")
            with open(os.path.join(models_path, 'payment_predictor.pkl'), 'rb') as f:
                self.payment_predictor = pickle.load(f)
            print("   ✓ Payment predictor loaded")
            
            # Load feature scaler
            print("\n[4/5] Loading feature scaler...")
            with open(os.path.join(models_path, 'feature_scaler.pkl'), 'rb') as f:
                self.feature_scaler = pickle.load(f)
            print("   ✓ Feature scaler loaded")
            
            # Load label encoders and feature columns
            print("\n[5/5] Loading label encoders and feature columns...")
            with open(os.path.join(models_path, 'label_encoders.pkl'), 'rb') as f:
                self.label_encoders = pickle.load(f)
            
            with open(os.path.join(models_path, 'feature_columns.pkl'), 'rb') as f:
                self.feature_columns = pickle.load(f)
            
            print("   ✓ Label encoders and feature columns loaded")
            
            print("\n" + "=" * 60)
            print("✅ ALL ML MODELS LOADED SUCCESSFULLY!")
            print("=" * 60 + "\n")
            
        except FileNotFoundError as e:
            print(f"\n❌ Error: Model file not found - {e}")
            print("   Please train the models first by running:")
            print("   cd ml_models && python train_complaint_classifier.py")
            print("   cd ml_models && python train_payment_predictor.py")
            raise
        except Exception as e:
            print(f"\n❌ Error loading models: {e}")
            raise
    
    def predict_complaint_priority(self, complaint_text):
        """Predict complaint priority with safety keyword override"""
        import re
        
        # Critical safety keywords that should ALWAYS be HIGH priority
        CRITICAL_KEYWORDS = [
            'spark', 'sparking', 'fire', 'smoking', 'smoke', 'burning',
            'shock', 'electric shock', 'electrocuted', 'gas leak', 'flooding',
            'short circuit', 'short-circuit', 'exposed wire', 'wire exposed',
            'circuit breaker', 'power outage', 'no power', 'burning smell'
        ]
        
        # Check for critical keywords first (rule-based override)
        text_lower = str(complaint_text).lower()
        for keyword in CRITICAL_KEYWORDS:
            if keyword in text_lower:
                return {
                    'priority': 'High',
                    'confidence': 0.95  # High confidence for safety issues
                }
        
        # Preprocess text for ML model
        text = str(complaint_text).lower()
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = ' '.join(text.split())
        
        # Vectorize
        tfidf = self.tfidf_vectorizer.transform([text])
        
        # Predict using ML model
        prediction = self.complaint_classifier.predict(tfidf)[0]
        confidence = self.complaint_classifier.predict_proba(tfidf).max()
        
        return {
            'priority': prediction,
            'confidence': float(confidence)
        }
    
    def predict_payment_delay(self, features):
        """Predict payment delay risk"""
        import pandas as pd
        import numpy as np
        
        # Create feature vector
        feature_dict = {}
        
        for col in self.feature_columns:
            if col in features:
                feature_dict[col] = features[col]
            else:
                feature_dict[col] = 0
        
        # Create DataFrame
        X = pd.DataFrame([feature_dict])
        
        # Scale features
        X_scaled = self.feature_scaler.transform(X)
        
        # Predict
        prediction = self.payment_predictor.predict(X_scaled)[0]
        risk_score = self.payment_predictor.predict_proba(X_scaled)[0][1]
        
        return {
            'will_delay': bool(prediction),
            'risk_score': float(risk_score)
        }


# Global instance
ml_models = MLModels()
