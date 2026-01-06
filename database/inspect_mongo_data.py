"""
Inspect MongoDB Data
Checks the data types and values in MongoDB to debug dashboard issues.
"""

from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "apartment_management"

def inspect_data():
    print("=" * 60)
    print("INSPECTING MONGODB DATA")
    print("=" * 60)
    
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        # 1. Check Counts
        print("\n[1] Collection Counts:")
        print(f"   Apartments: {db.apartments.count_documents({})}")
        print(f"   Complaints: {db.complaints.count_documents({})}")
        print(f"   Payments:   {db.payments.count_documents({})}")
        
        # 2. Check Payment Data (Revenue Issue)
        print("\n[2] Payment Data Sample (First 3 Paid):")
        paid_payments = list(db.payments.find({"payment_status": "Paid"}).limit(3))
        
        if not paid_payments:
            print("   No 'Paid' payments found!")
            # Check distinct statuses
            print(f"   Distinct Payment Statuses: {db.payments.distinct('payment_status')}")
        else:
            for p in paid_payments:
                print(f"   ID: {p.get('payment_id')}, Amount: {p.get('payment_amount')}, Block: {p.get('block_no')} (Type: {type(p.get('payment_amount'))})")
                
        # 3. Check Complaint Data
        print("\n[3] Complaint Data Sample:")
        complaints = list(db.complaints.find().limit(3))
        for c in complaints:
            print(f"   ID: {c.get('complaint_id')}, Status: {c.get('complaint_status')}, Priority: {c.get('priority')}")
            
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inspect_data()
