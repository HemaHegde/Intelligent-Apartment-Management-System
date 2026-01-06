"""
MongoDB Initialization Script
Creates collections, indexes, and imports CSV data
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
import pandas as pd
import json
from datetime import datetime
import pickle


# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "apartment_management"

# Collection names
COLLECTIONS = {
    'apartments': 'apartments',
    'complaints': 'complaints',
    'payments': 'payments',
    'prediction_logs': 'prediction_logs',
    'analytics': 'analytics'
}


def init_mongodb():
    """Initialize MongoDB collections and import data"""
    
    print("=" * 60)
    print("INITIALIZING MONGODB DATABASE")
    print("=" * 60)
    
    try:
        # Connect to MongoDB
        print("\n[1/6] Connecting to MongoDB...")
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        print(f"   ✓ Connected to database: {DB_NAME}")
        
        # Drop existing collections (optional - for clean start)
        print("\n[2/6] Dropping existing collections...")
        for collection_name in COLLECTIONS.values():
            db[collection_name].drop()
        print("   ✓ Existing collections dropped")
        
        # Create collections with indexes
        print("\n[3/6] Creating collections and indexes...")
        
        # Apartments collection
        apartments = db[COLLECTIONS['apartments']]
        apartments.create_index([("block_no", ASCENDING)])
        apartments.create_index([("room_no", ASCENDING)])
        apartments.create_index([("owner_id", ASCENDING)])
        apartments.create_index([("tenant_id", ASCENDING)])
        print("   ✓ Created 'apartments' collection")
        
        # Complaints collection
        complaints = db[COLLECTIONS['complaints']]
        complaints.create_index([("complaint_id", ASCENDING)], unique=True)
        complaints.create_index([("tenant_id", ASCENDING)])
        complaints.create_index([("complaint_category", ASCENDING)])
        complaints.create_index([("complaint_status", ASCENDING)])
        complaints.create_index([("priority", ASCENDING)])
        complaints.create_index([("created_at", DESCENDING)])
        print("   ✓ Created 'complaints' collection")
        
        # Payments collection
        payments = db[COLLECTIONS['payments']]
        payments.create_index([("payment_id", ASCENDING)], unique=True)
        payments.create_index([("tenant_id", ASCENDING)])
        payments.create_index([("payment_status", ASCENDING)])
        payments.create_index([("payment_date", DESCENDING)])
        print("   ✓ Created 'payments' collection")
        
        # Prediction logs collection
        prediction_logs = db[COLLECTIONS['prediction_logs']]
        prediction_logs.create_index([("model_type", ASCENDING)])
        prediction_logs.create_index([("timestamp", DESCENDING)])
        print("   ✓ Created 'prediction_logs' collection")
        
        # Analytics collection
        analytics = db[COLLECTIONS['analytics']]
        analytics.create_index([("metric_type", ASCENDING)])
        analytics.create_index([("date", DESCENDING)])
        print("   ✓ Created 'analytics' collection")
        
        # Import CSV data
        print("\n[4/6] Importing data from CSV...")
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, 'apartment_management_dataset_realistic_v2.csv')
        df = pd.read_csv(csv_path)
        print(f"   ✓ Loaded {len(df)} records from CSV")
        
        # Import apartments data
        print("\n[5/6] Importing apartments data...")
        # Get unique apartments (drop duplicates by room_no)
        # We need to filter out rows where room_no might be NaN (though shouldn't happen)
        apt_df = df.dropna(subset=['room_no'])
        apartments_data = apt_df[[
            'block_no', 'block_name', 'room_no', 'floor', 'room_type',
            'owner_id', 'owner_name', 'tenant_id', 'tenant_name', 'monthly_rent'
        ]].drop_duplicates(subset=['room_no']).to_dict('records')
        
        if apartments_data:
            apartments.insert_many(apartments_data)
        print(f"   ✓ Imported {len(apartments_data)} apartments")
        
        # Import complaints data
        print("\n[6/6] Importing complaints data...")
        complaints_data = []
        # Filter for complaints only
        complaint_rows = df[df['type'] == 'Complaint']
        
        for _, row in complaint_rows.iterrows():
            complaint_doc = {
                'complaint_id': row['complaint_id'],
                'tenant_id': row['tenant_id'],
                'tenant_name': row['tenant_name'],
                'block_no': row['block_no'],
                'block_name': row.get('block_name'),
                'room_no': row['room_no'],
                'complaint_text': row['complaint_text'],
                'complaint_category': row['complaint_category'],
                'complaint_status': row['complaint_status'],
                'employee_id': row['employee_id'],
                'priority': None,
                'priority_confidence': None,
                'embedding': None,
                'created_at': datetime.now(), # In production we would parse row['created_date']
                'updated_at': datetime.now()
            }
            complaints_data.append(complaint_doc)
        
        if complaints_data:
            complaints.insert_many(complaints_data)
        print(f"   ✓ Imported {len(complaints_data)} complaints")
        
        # Import payments data
        payments_data = []
        # Filter for payments only
        payment_rows = df[df['type'] == 'Payment']
        
        for _, row in payment_rows.iterrows():
            payment_doc = {
                'payment_id': row['payment_id'],
                'tenant_id': row['tenant_id'],
                'tenant_name': row['tenant_name'],
                'block_no': row['block_no'],
                'block_name': row.get('block_name'),
                'room_no': row['room_no'],
                'payment_amount': float(row['payment_amount']),
                'payment_date': row['payment_date'],
                'payment_status': row['payment_status'],
                'monthly_rent': float(row['monthly_rent']),
                'delay_risk': None,
                'risk_score': None,
                'created_at': datetime.now()
            }
            payments_data.append(payment_doc)
        
        if payments_data:
            payments.insert_many(payments_data)
        print(f"   ✓ Imported {len(payments_data)} payments")
        print(f"   ✓ Imported {len(payments_data)} payments")
        
        print("\n" + "=" * 60)
        print("✅ MONGODB INITIALIZATION COMPLETE!")
        print("=" * 60)
        print(f"\nDatabase: {DB_NAME}")
        print(f"Collections created: {len(COLLECTIONS)}")
        print(f"Total documents: {apartments.count_documents({}) + complaints.count_documents({}) + payments.count_documents({})}")
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nℹ️  Make sure MongoDB is running on localhost:27017")


if __name__ == "__main__":
    init_mongodb()
