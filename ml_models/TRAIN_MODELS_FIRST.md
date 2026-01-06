# 🚨 URGENT FIX: Train ML Models

## The Problem

You're getting "Network Error" because the **ML models haven't been trained yet**!

When you submit a complaint, the backend tries to predict priority using ML models, but the model files don't exist, causing the backend to crash.

---

## The Solution - Train the Models

### Step 1: Open Command Prompt

Navigate to the ML models folder:

```cmd
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\ml_models"
```

### Step 2: Install Dependencies (if not done)

```cmd
pip install -r requirements.txt
```

**Wait for this to complete** (may take a few minutes)

### Step 3: Train Complaint Classifier

```cmd
python train_complaint_classifier.py
```

**Expected output:**
```
Training Complaint Priority Classifier...
✓ Model trained successfully
✓ Saved: complaint_classifier.pkl
✓ Saved: tfidf_vectorizer.pkl
```

### Step 4: Train Payment Predictor

```cmd
python train_payment_predictor.py
```

**Expected output:**
```
Training Payment Delay Predictor...
✓ Model trained successfully
✓ Saved: payment_predictor.pkl
✓ Saved: feature_scaler.pkl
```

### Step 5: Restart Backend

1. Go to your backend terminal
2. Press `Ctrl+C` to stop it
3. Run `python app.py` again

**Expected output:**
```
==========================================================
LOADING ML MODELS
==========================================================

[1/5] Loading complaint classifier...
   ✓ Complaint classifier loaded

[2/5] Loading TF-IDF vectorizer...
   ✓ TF-IDF vectorizer loaded

[3/5] Loading payment predictor...
   ✓ Payment predictor loaded

[4/5] Loading feature scaler...
   ✓ Feature scaler loaded

[5/5] Loading label encoders and feature columns...
   ✓ Label encoders and feature columns loaded

==========================================================
✅ ALL ML MODELS LOADED SUCCESSFULLY!
==========================================================
```

---

## Step 6: Test Complaint Submission

1. Go back to your browser (`http://localhost:5173`)
2. Login as tenant
3. Submit a complaint
4. **Should work now!** ✅

---

## Quick Command Summary

```cmd
# All in one:
cd "c:\Users\hemah\Desktop\APARTMENT SYSTEM\ml_models"
pip install -r requirements.txt
python train_complaint_classifier.py
python train_payment_predictor.py

# Then restart backend:
cd ..\backend
python app.py
```

---

## Why This Happened

The ML models need to be **trained before the backend can use them**. The backend tries to load these files on startup:

- `complaint_classifier.pkl` - Predicts complaint priority
- `tfidf_vectorizer.pkl` - Converts text to numbers
- `payment_predictor.pkl` - Predicts payment delays
- `feature_scaler.pkl` - Normalizes payment features
- `label_encoders.pkl` - Encodes categorical data
- `feature_columns.pkl` - Stores feature names

Without these files, the backend crashes when trying to predict priority!

---

## Troubleshooting

### If training fails with Python 3.13 errors:

The requirements have already been updated for Python 3.13 compatibility. If you still get errors, try:

```cmd
pip install numpy pandas scikit-learn imbalanced-learn sentence-transformers
```

### If you see "No module named 'sklearn'":

```cmd
pip install scikit-learn
```

---

**Run the training commands now, then restart your backend!** 🚀
