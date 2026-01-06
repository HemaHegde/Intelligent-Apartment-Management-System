from pymongo import MongoClient
from datetime import datetime, timedelta

db = MongoClient('mongodb://localhost:27017/')['apartment_management']

# Add apartment for T1679
apartment_data = {
    'block_no': 'B1',
    'block_name': 'Maple Heights',
    'room_no': 1679,
    'room_type': '2BHK',
    'owner_id': 'O1001',
    'owner_name': 'Rajesh Kumar',
    'tenant_id': 'T1679',
    'tenant_name': 'hema'
}

# Check if apartment already exists
existing_apt = db.apartments.find_one({'tenant_id': 'T1679'})
if not existing_apt:
    db.apartments.insert_one(apartment_data)
    print("✓ Added apartment for T1679")
else:
    print("✓ Apartment already exists for T1679")

# Add payment history for T1679 (last 6 months)
payment_statuses = ['Paid', 'Paid', 'Paid', 'Paid', 'Pending', 'Paid']
base_amount = 18500

payments_to_add = []
for i in range(6):
    payment_date = (datetime.now() - timedelta(days=30*(5-i))).strftime('%d-%m-%Y')
    payment_data = {
        'payment_id': f'P{20000 + i}',
        'tenant_id': 'T1679',
        'tenant_name': 'hema',
        'room_no': 1679,
        'block_no': 'B1',
        'payment_amount': base_amount + (i * 50),
        'payment_date': payment_date,
        'payment_status': payment_statuses[i],
        'delay_risk_score': 0.2 if payment_statuses[i] == 'Paid' else 0.6
    }
    payments_to_add.append(payment_data)

# Insert payments
db.payments.insert_many(payments_to_add)
print(f"✓ Added {len(payments_to_add)} payment records for T1679")

# Verify
payment_count = db.payments.count_documents({'tenant_id': 'T1679'})
print(f"\nTotal payments for T1679: {payment_count}")
