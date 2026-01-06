import sys
import os
import requests
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from models.mongo_models import get_mongo_db

def verify_tenant_payments():
    print("Verifying Tenant Payment Data...")
    
    # 1. Connect to MongoDB
    try:
        db = get_mongo_db()
        payments_count = db.payments.count_documents({})
        print(f"Total payments in database: {payments_count}")
        
        if payments_count == 0:
            print("⚠️ No payments found in database!")
            # Add a sample payment for testing
            sample_payment = {
                "payment_id": "PAY_TEST_001",
                "tenant_id": "T131",  # Matches the screenshot example (Room 131)
                "tenant_name": "Test Tenant",
                "block_no": "B1",
                "room_no": "131",
                "payment_amount": 15000,
                "payment_date": datetime.now().strftime("%Y-%m-%d"),
                "payment_status": "Paid",
                "payment_method": "UPI"
            }
            db.payments.insert_one(sample_payment)
            print("✅ Added sample payment for Tenant T131")
        else:
            # Check for T131 specific payments
            t131_payments = list(db.payments.find({"tenant_id": "T131"}))
            print(f"Payments for T131: {len(t131_payments)}")
            if len(t131_payments) == 0:
                 print("⚠️ No payments for T131. Adding one...")
                 sample_payment = {
                    "payment_id": "PAY_TEST_T131",
                    "tenant_id": "T131",
                    "tenant_name": "Kiaan Kapoor",
                    "block_no": "B1",
                    "room_no": "131",
                    "payment_amount": 12500,
                    "payment_date": datetime.now().strftime("%Y-%m-%d"),
                    "payment_status": "Pending",
                    "payment_method": "Bank Transfer"
                }
                 db.payments.insert_one(sample_payment)
                 print("✅ Added sample payment for Tenant T131")

    except Exception as e:
        print(f"❌ Database error: {e}")
        return

if __name__ == "__main__":
    verify_tenant_payments()
