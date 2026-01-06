from pymongo import MongoClient

db = MongoClient('mongodb://localhost:27017/')['apartment_management']

# Check T1002
payments_t1002 = list(db.payments.find({'tenant_id': 'T1002'}))
print(f"Payments for T1002: {len(payments_t1002)}")

if payments_t1002:
    print("\nSample payments:")
    for p in payments_t1002[:3]:
        print(f"  Payment ID: {p['payment_id']}, Amount: ₹{p['payment_amount']}, Status: {p['payment_status']}, Date: {p['payment_date']}")
else:
    print("No payments found for T1002")

# Check if tenant1002 user exists in MySQL
print("\n" + "="*50)
print("To login as tenant1002, you need:")
print("  Username: tenant1002 (or check MySQL users table)")
print("  Password: The password used during registration")
print("="*50)
