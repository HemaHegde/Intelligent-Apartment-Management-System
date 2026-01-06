"""
Tenant Payment Delay Prediction Model
Predicts whether a tenant will delay payment next month
Uses tabular features + Random Forest Classifier
"""

import pandas as pd
import numpy as np
import pickle
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_auc_score
from imblearn.over_sampling import SMOTE


def engineer_payment_features(df):
    """
    Engineer features from payment and complaint data
    """
    print("   Engineering payment features...")
    
    # Convert payment_date to datetime
    df['payment_date'] = pd.to_datetime(df['payment_date'], format='%d-%m-%Y')
    
    # Calculate days since payment
    reference_date = pd.to_datetime('2025-12-11')  # Latest date in dataset
    df['days_since_payment'] = (reference_date - df['payment_date']).dt.days
    
    # Binary target: 1 if payment is Overdue or Pending, 0 if Paid
    df['will_delay'] = df['payment_status'].apply(
        lambda x: 1 if x in ['Overdue', 'Pending'] else 0
    )
    
    # Aggregate features by tenant
    tenant_features = df.groupby('tenant_id').agg({
        'payment_amount': ['mean', 'std', 'min', 'max'],
        'monthly_rent': 'first',
        'will_delay': 'sum',  # Count of delays
        'payment_id': 'count',  # Total payments
        'complaint_id': 'count',  # Total complaints
        'days_since_payment': 'mean'
    }).reset_index()
    
    # Flatten column names
    tenant_features.columns = [
        'tenant_id', 'avg_payment', 'std_payment', 'min_payment', 'max_payment',
        'monthly_rent', 'delay_count', 'total_payments', 'total_complaints',
        'avg_days_since_payment'
    ]
    
    # Calculate delay rate
    tenant_features['delay_rate'] = (
        tenant_features['delay_count'] / tenant_features['total_payments']
    )
    
    # Payment consistency (lower std = more consistent)
    tenant_features['payment_consistency'] = (
        tenant_features['std_payment'].fillna(0) / tenant_features['avg_payment']
    )
    
    # Complaint rate
    tenant_features['complaint_rate'] = (
        tenant_features['total_complaints'] / tenant_features['total_payments']
    )
    
    # Merge back with original data to get room_type and other features
    df_merged = df.merge(tenant_features, on='tenant_id', how='left', suffixes=('', '_agg'))
    
    # Encode room_type
    le_room = LabelEncoder()
    df_merged['room_type_encoded'] = le_room.fit_transform(df_merged['room_type'])
    
    # Encode complaint_category
    le_category = LabelEncoder()
    df_merged['complaint_category_encoded'] = le_category.fit_transform(df_merged['complaint_category'])
    
    # Encode complaint_status
    le_status = LabelEncoder()
    df_merged['complaint_status_encoded'] = le_status.fit_transform(df_merged['complaint_status'])
    
    print(f"   ✓ Created {len(tenant_features)} tenant profiles")
    
    return df_merged, le_room, le_category, le_status


def train_payment_predictor():
    """Train the payment delay prediction model"""
    
    print("=" * 60)
    print("PAYMENT DELAY PREDICTION MODEL TRAINING")
    print("=" * 60)
    
    # Load dataset
    print("\n[1/7] Loading dataset...")
    df = pd.read_csv('../apartment_management_dataset_realistic.csv')
    print(f"   ✓ Loaded {len(df)} records")
    
    # Engineer features
    print("\n[2/7] Engineering features...")
    df_features, le_room, le_category, le_status = engineer_payment_features(df)
    
    # Select features for model
    feature_columns = [
        'monthly_rent',
        'avg_payment',
        'payment_consistency',
        'delay_rate',
        'total_complaints',
        'complaint_rate',
        'avg_days_since_payment',
        'room_type_encoded',
        'complaint_category_encoded',
        'complaint_status_encoded'
    ]
    
    X = df_features[feature_columns].fillna(0)
    y = df_features['will_delay']
    
    print(f"   ✓ Selected {len(feature_columns)} features")
    print(f"   ✓ Target distribution: {y.value_counts().to_dict()}")
    
    # Split data
    print("\n[3/7] Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   ✓ Training set: {len(X_train)} samples")
    print(f"   ✓ Test set: {len(X_test)} samples")
    
    # Handle class imbalance with SMOTE
    print("\n[4/7] Handling class imbalance with SMOTE...")
    smote = SMOTE(random_state=42)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    print(f"   ✓ Balanced training set: {len(X_train_balanced)} samples")
    print(f"   ✓ New distribution: {pd.Series(y_train_balanced).value_counts().to_dict()}")
    
    # Scale features
    print("\n[5/7] Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_balanced)
    X_test_scaled = scaler.transform(X_test)
    print("   ✓ Features scaled")
    
    # Train Random Forest Classifier
    print("\n[6/7] Training Random Forest classifier...")
    classifier = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    classifier.fit(X_train_scaled, y_train_balanced)
    print("   ✓ Model trained successfully")
    
    # Evaluate model
    print("\n[7/7] Evaluating model performance...")
    y_pred = classifier.predict(X_test_scaled)
    y_pred_proba = classifier.predict_proba(X_test_scaled)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\n   📊 Accuracy: {accuracy:.2%}")
    print(f"   📊 ROC-AUC Score: {roc_auc:.2%}")
    
    print("\n   Classification Report:")
    report = classification_report(
        y_test, y_pred, 
        target_names=['Will Pay On Time', 'Will Delay'],
        zero_division=0
    )
    for line in report.split('\n'):
        if line.strip():
            print(f"      {line}")
    
    print("\n   Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"      Predicted:    On Time  Delay")
    print(f"      On Time       {cm[0][0]:7d}  {cm[0][1]:5d}")
    print(f"      Delay         {cm[1][0]:7d}  {cm[1][1]:5d}")
    
    # Feature importance
    print("\n   Top 5 Most Important Features:")
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': classifier.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.head(5).iterrows():
        print(f"      {row['feature']:30s} {row['importance']:.4f}")
    
    # Save models
    print("\n[SAVING] Saving trained models...")
    with open('payment_predictor.pkl', 'wb') as f:
        pickle.dump(classifier, f)
    print("   ✓ Saved: payment_predictor.pkl")
    
    with open('feature_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print("   ✓ Saved: feature_scaler.pkl")
    
    with open('label_encoders.pkl', 'wb') as f:
        pickle.dump({
            'room_type': le_room,
            'complaint_category': le_category,
            'complaint_status': le_status
        }, f)
    print("   ✓ Saved: label_encoders.pkl")
    
    # Save feature columns
    with open('feature_columns.pkl', 'wb') as f:
        pickle.dump(feature_columns, f)
    print("   ✓ Saved: feature_columns.pkl")
    
    # Test predictions
    print("\n[TESTING] Sample predictions:")
    sample_indices = X_test.sample(5, random_state=42).index
    for idx in sample_indices:
        features = X_test.loc[idx:idx]
        scaled_features = scaler.transform(features)
        prediction = classifier.predict(scaled_features)[0]
        risk_score = classifier.predict_proba(scaled_features)[0][1]
        actual = y_test.loc[idx]
        
        print(f"   Tenant: Monthly Rent=${features['monthly_rent'].values[0]:.0f}, "
              f"Delay Rate={features['delay_rate'].values[0]:.2%}")
        print(f"   → Prediction: {'Will Delay' if prediction == 1 else 'On Time'} "
              f"(Risk: {risk_score:.2%}) | Actual: {'Delayed' if actual == 1 else 'On Time'}")
    
    print("\n" + "=" * 60)
    print("✅ PAYMENT PREDICTOR TRAINING COMPLETE!")
    print("=" * 60)
    
    return classifier, scaler, accuracy, roc_auc


if __name__ == "__main__":
    train_payment_predictor()
