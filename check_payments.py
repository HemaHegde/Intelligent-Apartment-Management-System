from pymongo import MongoClient

db = MongoClient('mongodb://localhost:27017/')['apartment_management']

# Check payments for T1679
payments_t1679 = list(db.payments.find({'tenant_id': 'T1679'}))
print(f"Payments for T1679 (hema): {len(payments_t1679)}")

# Check sample payments
sample_payments = list(db.payments.find().limit(5))
print(f"\nSample payments in database:")
for p in sample_payments:
    print(f"  tenant_id: {p.get('tenant_id')}, room_no: {p.get('room_no')}, amount: {p.get('payment_amount')}")

# Check which tenants have payments
tenant_ids = db.payments.distinct('tenant_id')
print(f"\nTotal unique tenants with payments: {len(tenant_ids)}")
print(f"Sample tenant IDs: {tenant_ids[:10]}")

# Check if T1679 exists in apartments
apartment = db.apartments.find_one({'tenant_id': 'T1679'})
if apartment:
    print(f"\nT1679 apartment found: Room {apartment.get('room_no')}")
else:
    print("\nT1679 not found in apartments!")
