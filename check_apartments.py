from pymongo import MongoClient

db = MongoClient('mongodb://localhost:27017/')['apartment_management']

# Check sample apartments
sample_apts = list(db.apartments.find().limit(5))
print("Sample apartments:")
for apt in sample_apts:
    print(f"  Tenant: {apt.get('tenant_id')}, Block: {apt.get('block_no')}, Room: {apt.get('room_no')}")

# Count by block
print("\nApartments per block:")
pipeline = [
    {'$group': {'_id': '$block_no', 'count': {'$sum': 1}}},
    {'$sort': {'_id': 1}}
]
for result in db.apartments.aggregate(pipeline):
    print(f"  {result['_id']}: {result['count']} apartments")

# Total count
total = db.apartments.count_documents({})
print(f"\nTotal apartments: {total}")

# Check if filtering by block works
b1_count = db.apartments.count_documents({'block_no': 'B1'})
print(f"Apartments in B1: {b1_count}")
