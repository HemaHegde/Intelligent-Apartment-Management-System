"""
Load Realistic Dataset to MongoDB
Loads apartment, payment, and complaint data from CSV to MongoDB
"""

import pandas as pd
import pymongo
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.config import Config

def get_mongo_connection():
    """Get MongoDB connection"""
    client = pymongo.MongoClient(Config.MONGO_URI)
    return client[Config.MONGO_DB]

def load_data_to_mongodb():
    """Load data from CSV to MongoDB"""
    
    print("=" * 60)
    print("LOADING REALISTIC DATASET TO MONGODB")
    print("=" * 60)
    
    # Load CSV
    print("\n[1/4] Loading CSV file...")
    df = pd.read_csv('apartment_management_dataset_realistic.csv')
    print(f"   ✓ Loaded {len(df)} records")
    
    # Connect to MongoDB
    print("\n[2/4] Connecting to MongoDB...")
    db = get_mongo_connection()
    print("   ✓ Connected to MongoDB")
    
    # Clear existing data
    print("\n[3/4] Clearing existing data...")
    db.apartments.delete_many({})
    db.payments.delete_many({})
    db.complaints.delete_many({})
    print("   ✓ Cleared existing collections")
    
    # Load apartments
    print("\n[4/4] Loading data to MongoDB...")
    
    # Get unique apartments
    apartments_df = df[['block_no', 'block_name', 'room_no', 'room_type', 
                        'owner_id', 'owner_name', 'tenant_id', 'tenant_name']].drop_duplicates()
    
    apartments_data = []
    for _, row in apartments_df.iterrows():
        apartments_data.append({
            'block_no': row['block_no'],
            'block_name': row['block_name'],
            'room_no': int(row['room_no']),
            'room_type': row['room_type'],
            'owner_id': row['owner_id'],
            'owner_name': row['owner_name'],
            'tenant_id': row['tenant_id'] if pd.notna(row['tenant_id']) else None,
            'tenant_name': row['tenant_name'] if pd.notna(row['tenant_name']) else None
        })
    
    if apartments_data:
        db.apartments.insert_many(apartments_data)
        print(f"   ✓ Loaded {len(apartments_data)} apartments")
    
    # Load payments
    payments_df = df[df['payment_id'].notna()][['payment_id', 'tenant_id', 'tenant_name', 
                                                   'room_no', 'block_no', 'payment_amount', 
                                                   'payment_date', 'payment_status']].drop_duplicates()
    
    payments_data = []
    for _, row in payments_df.iterrows():
        payments_data.append({
            'payment_id': row['payment_id'],
            'tenant_id': row['tenant_id'],
            'tenant_name': row['tenant_name'],
            'room_no': int(row['room_no']),
            'block_no': row['block_no'],
            'payment_amount': float(row['payment_amount']),
            'payment_date': row['payment_date'],
            'payment_status': row['payment_status'],
            'delay_risk_score': 0.0  # Default value
        })
    
    if payments_data:
        db.payments.insert_many(payments_data)
        print(f"   ✓ Loaded {len(payments_data)} payments")
    
    # Load complaints
    complaints_df = df[df['complaint_id'].notna()][['complaint_id', 'tenant_id', 'tenant_name',
                                                       'room_no', 'block_no', 'complaint_text',
                                                       'complaint_category', 'complaint_status',
                                                       'employee_id']].drop_duplicates()
    
    complaints_data = []
    for _, row in complaints_df.iterrows():
        # Generate priority based on complaint text (simple rule-based)
        text_lower = str(row['complaint_text']).lower()
        if any(word in text_lower for word in ['spark', 'fire', 'shock', 'emergency', 'urgent', 'danger']):
            priority = 'High'
        elif any(word in text_lower for word in ['leak', 'broken', 'not working']):
            priority = 'Medium'
        else:
            priority = 'Low'
        
        complaints_data.append({
            'complaint_id': row['complaint_id'],
            'tenant_id': row['tenant_id'],
            'tenant_name': row['tenant_name'],
            'room_no': int(row['room_no']),
            'block_no': row['block_no'],
            'complaint_text': row['complaint_text'],
            'complaint_category': row['complaint_category'],
            'complaint_status': row['complaint_status'],
            'employee_id': row['employee_id'] if pd.notna(row['employee_id']) else None,
            'priority': priority,
            'priority_confidence': 0.85  # Default value
        })
    
    if complaints_data:
        db.complaints.insert_many(complaints_data)
        print(f"   ✓ Loaded {len(complaints_data)} complaints")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ DATA LOADING COMPLETE!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  • Apartments: {db.apartments.count_documents({})}")
    print(f"  • Payments: {db.payments.count_documents({})}")
    print(f"  • Complaints: {db.complaints.count_documents({})}")
    print()

if __name__ == "__main__":
    load_data_to_mongodb()
