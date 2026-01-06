"""
Complaint Priority Classification Model
Classifies complaint text into High, Medium, or Low priority
Uses TF-IDF vectorization + Random Forest + Rule-based logic
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import re

# Priority keywords for rule-based classification
HIGH_PRIORITY_KEYWORDS = [
    'sparking', 'smoking', 'fire', 'electric shock', 'gas leak', 'flooding',
    'broken', 'emergency', 'urgent', 'danger', 'hazard', 'safety',
    'short circuit', 'short-circuit', 'circuit breaker', 'power outage',
    'no power', 'electrical fault', 'wire exposed', 'burning smell'
]

MEDIUM_PRIORITY_KEYWORDS = [
    'leaking', 'leak', 'dripping', 'clogged', 'not working', 'broken',
    'flickering', 'buzzing', 'jammed', 'stuck'
]

# High priority categories
HIGH_PRIORITY_CATEGORIES = ['Electricity']
MEDIUM_PRIORITY_CATEGORIES = ['Plumbing', 'Water']
LOW_PRIORITY_CATEGORIES = ['Housekeeping']


def assign_priority_label(row):
    """
    Rule-based priority assignment based on complaint text and category
    """
    text = str(row['complaint_text']).lower()
    category = str(row['complaint_category'])
    
    # Check for high priority keywords
    for keyword in HIGH_PRIORITY_KEYWORDS:
        if keyword in text:
            return 'High'
    
    # Check category-based priority
    if category in HIGH_PRIORITY_CATEGORIES:
        # Electricity issues are generally high priority
        if any(word in text for word in ['sparking', 'smoking', 'shock', 'panel', 'tripped', 
                                          'short circuit', 'short-circuit', 'circuit breaker',
                                          'power outage', 'no power', 'burning smell', 'wire exposed']):
            return 'High'
        else:
            return 'Medium'
    
    if category in MEDIUM_PRIORITY_CATEGORIES:
        # Water/Plumbing issues
        if any(word in text for word in ['ceiling', 'flooding', 'overflow', 'seepage']):
            return 'High'
        elif any(word in text for word in MEDIUM_PRIORITY_KEYWORDS):
            return 'Medium'
        else:
            return 'Low'
    
    if category in LOW_PRIORITY_CATEGORIES:
        # Housekeeping is generally low priority
        if any(word in text for word in ['garbage', 'dirty', 'cleaning']):
            return 'Low'
        else:
            return 'Low'
    
    # Default to Medium if unclear
    return 'Medium'


def preprocess_text(text):
    """Clean and preprocess complaint text"""
    text = str(text).lower()
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text


def train_complaint_classifier():
    """Train the complaint priority classification model"""
    
    print("=" * 60)
    print("COMPLAINT PRIORITY CLASSIFICATION MODEL TRAINING")
    print("=" * 60)
    
    # Load dataset
    print("\n[1/7] Loading dataset...")
    df = pd.read_csv('../apartment_management_dataset_realistic.csv')
    print(f"   ✓ Loaded {len(df)} records")
    
    # Assign priority labels
    print("\n[2/7] Assigning priority labels...")
    df['priority'] = df.apply(assign_priority_label, axis=1)
    print(f"   ✓ Priority distribution:")
    print(df['priority'].value_counts().to_string(header=False).replace('\n', '\n     '))
    
    # Preprocess text
    print("\n[3/7] Preprocessing complaint texts...")
    df['complaint_text_clean'] = df['complaint_text'].apply(preprocess_text)
    print(f"   ✓ Preprocessed {len(df)} complaint texts")
    
    # Prepare features and labels
    X = df['complaint_text_clean']
    y = df['priority']
    
    # Split data
    print("\n[4/7] Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   ✓ Training set: {len(X_train)} samples")
    print(f"   ✓ Test set: {len(X_test)} samples")
    
    # TF-IDF Vectorization
    print("\n[5/7] Creating TF-IDF features...")
    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.8
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    print(f"   ✓ Created {X_train_tfidf.shape[1]} TF-IDF features")
    
    # Train Random Forest Classifier
    print("\n[6/7] Training Random Forest classifier...")
    classifier = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    classifier.fit(X_train_tfidf, y_train)
    print("   ✓ Model trained successfully")
    
    # Evaluate model
    print("\n[7/7] Evaluating model performance...")
    y_pred = classifier.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n   📊 Accuracy: {accuracy:.2%}")
    print("\n   Classification Report:")
    report = classification_report(y_test, y_pred, zero_division=0)
    for line in report.split('\n'):
        if line.strip():
            print(f"      {line}")
    
    print("\n   Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=['High', 'Medium', 'Low'])
    print(f"      Predicted:  High  Medium  Low")
    for i, label in enumerate(['High', 'Medium', 'Low']):
        print(f"      {label:8s}  {cm[i][0]:4d}  {cm[i][1]:6d}  {cm[i][2]:3d}")
    
    # Save models
    print("\n[SAVING] Saving trained models...")
    with open('complaint_classifier.pkl', 'wb') as f:
        pickle.dump(classifier, f)
    print("   ✓ Saved: complaint_classifier.pkl")
    
    with open('tfidf_vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    print("   ✓ Saved: tfidf_vectorizer.pkl")
    
    # Save sample predictions for testing
    sample_complaints = [
        "Electric socket sparking near bed",
        "Water leaking from ceiling",
        "Garbage not collected today",
        "Power backup not working",
        "Floor not mopped properly"
    ]
    
    print("\n[TESTING] Sample predictions:")
    for complaint in sample_complaints:
        clean_text = preprocess_text(complaint)
        tfidf = vectorizer.transform([clean_text])
        prediction = classifier.predict(tfidf)[0]
        confidence = classifier.predict_proba(tfidf).max()
        print(f"   '{complaint}'")
        print(f"   → Priority: {prediction} (confidence: {confidence:.2%})")
    
    print("\n" + "=" * 60)
    print("✅ COMPLAINT CLASSIFIER TRAINING COMPLETE!")
    print("=" * 60)
    
    return classifier, vectorizer, accuracy


if __name__ == "__main__":
    train_complaint_classifier()
