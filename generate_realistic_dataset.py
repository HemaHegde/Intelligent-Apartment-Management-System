"""
Realistic Dataset Generator for Sunrise Apartments
Generates apartment management data with proper entity relationships
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# CONFIGURATION
# ============================================================================

COMPANY_NAME = "Sunrise Apartments"

# Building configuration (8 buildings across India)
BUILDINGS = [
    {"block_no": "B1", "name": "Maple Heights", "city": "Mumbai", "apartments": 30},
    {"block_no": "B2", "name": "Harmony Residency", "city": "Delhi", "apartments": 28},
    {"block_no": "B3", "name": "Sunrise Enclave", "city": "Bangalore", "apartments": 29},
    {"block_no": "B4", "name": "Lakeview Towers", "city": "Hyderabad", "apartments": 28},
    {"block_no": "B5", "name": "Green Meadows", "city": "Chennai", "apartments": 30},
    {"block_no": "B6", "name": "Silver Oaks", "city": "Pune", "apartments": 29},
    {"block_no": "B7", "name": "Crystal View", "city": "Kolkata", "apartments": 28},
    {"block_no": "B8", "name": "Riverside Park", "city": "Ahmedabad", "apartments": 28},
]

# Room type distribution
ROOM_TYPES = {
    "1BHK": {"probability": 0.40, "rent_range": (11000, 14000)},
    "2BHK": {"probability": 0.35, "rent_range": (17000, 20000)},
    "3BHK": {"probability": 0.25, "rent_range": (24000, 30000)},
}

# Complaint categories and templates
COMPLAINT_CATEGORIES = {
    "Plumbing": [
        "Water leakage in kitchen sink", "Toilet flush not working properly",
        "Shower head clogged", "Drain clogging in utility area",
        "Leaking faucet in second bathroom", "Bathroom tap handle broken",
        "Ceiling leak near water tank", "Pipe vibrating during water flow",
        "Sink trap jammed", "Leakage near washing machine outlet",
        "Water dripping from ceiling after rain", "Drain smell from kitchen",
        "Kitchen sink pipe leaking slightly"
    ],
    "Electricity": [
        "Fan not working in bedroom", "Hall light flickering frequently",
        "Power backup not working", "Switch socket cracked in hall",
        "Electric socket sparking near bed", "Geyser not starting in morning",
        "Electrical panel buzzing", "Low voltage in living room circuit",
        "Water heater not heating enough", "Light switch loose",
        "Noisy fan in kitchen", "Power tripped during evening",
        "Light bulbs in corridor fused", "Fan regulator broken", "Power socket smoking"
    ],
    "Housekeeping": [
        "Floor not mopped properly", "Garbage not collected today",
        "Cleaning missed by housekeeping staff", "Dust on balcony after cleaning",
        "Common area dirty post rain", "Sweeper absent",
        "Housekeeping skipped common corridor", "Mop left in corridor",
        "Utensil rack area not cleaned properly", "No housekeeping staff this week",
        "Overflowing garbage bin", "Cleaning incomplete in lobby area"
    ],
    "Water": [
        "Low water pressure in bathrooms", "Foul smell in water during mornings",
        "Brown water from tap", "Water supply delayed",
        "Metallic taste in water", "Rusty water from bathroom tap",
        "Tap water muddy after rain", "Water tank overflow",
        "Water filter needs replacement", "Water seepage from terrace"
    ]
}

# Indian names for variety
FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna",
    "Ishaan", "Shaurya", "Atharv", "Advait", "Aadhya", "Ananya", "Pari", "Anika",
    "Diya", "Navya", "Saanvi", "Myra", "Sara", "Ira", "Priya", "Kavya",
    "Rohan", "Kabir", "Arnav", "Vihaan", "Dhruv", "Kiaan", "Riya", "Avni"
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Kumar", "Singh", "Gupta", "Reddy", "Iyer",
    "Nair", "Menon", "Rao", "Krishnan", "Desai", "Joshi", "Mehta", "Shah",
    "Kulkarni", "Bhat", "Shetty", "Pillai", "Das", "Ghosh", "Banerjee", "Kapoor",
    "Malhotra", "Khanna", "Chopra", "Kaur", "Bhosale", "Tiwari", "Pandey", "Sinha"
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_name():
    """Generate random Indian name"""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def generate_room_type():
    """Generate room type based on probability distribution"""
    rand = random.random()
    cumulative = 0
    for room_type, config in ROOM_TYPES.items():
        cumulative += config["probability"]
        if rand <= cumulative:
            return room_type
    return "1BHK"

def generate_rent(room_type):
    """Generate monthly rent based on room type"""
    min_rent, max_rent = ROOM_TYPES[room_type]["rent_range"]
    return random.randint(min_rent, max_rent)

def generate_complaint_text(category):
    """Generate complaint text from category"""
    return random.choice(COMPLAINT_CATEGORIES[category])

def generate_date_in_range(start_date, end_date):
    """Generate random date between start and end"""
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)

# ============================================================================
# DATA GENERATION
# ============================================================================

def generate_apartments():
    """Generate 230 unique apartments across 8 buildings"""
    print("\n[1/6] Generating apartments...")
    
    apartments = []
    apartment_id = 1
    
    for building in BUILDINGS:
        num_apartments = building["apartments"]
        
        for i in range(num_apartments):
            room_no = 100 + apartment_id
            floor = (apartment_id % 6) + 1  # Floors 1-6
            room_type = generate_room_type()
            
            apartments.append({
                "apartment_id": apartment_id,
                "block_no": building["block_no"],
                "block_name": building["name"],
                "city": building["city"],
                "room_no": room_no,
                "floor": floor,
                "room_type": room_type,
            })
            
            apartment_id += 1
    
    print(f"   ✓ Generated {len(apartments)} apartments across {len(BUILDINGS)} buildings")
    return apartments

def generate_property_managers(apartments):
    """Generate 25-30 property managers (1 per building + extras)"""
    print("\n[2/6] Generating property managers...")
    
    managers = []
    manager_id = 1001
    
    # Assign one manager per building
    for building in BUILDINGS:
        managers.append({
            "owner_id": f"O{manager_id}",
            "owner_name": generate_name(),
            "managed_building": building["block_no"],
            "city": building["city"]
        })
        manager_id += 1
    
    # Add some additional managers (assistant managers)
    for i in range(random.randint(17, 22)):
        building = random.choice(BUILDINGS)
        managers.append({
            "owner_id": f"O{manager_id}",
            "owner_name": generate_name(),
            "managed_building": building["block_no"],
            "city": building["city"]
        })
        manager_id += 1
    
    print(f"   ✓ Generated {len(managers)} property managers")
    return managers

def generate_employees():
    """Generate 5 specific employees for maintenance"""
    print("\n[3/6] Generating employees...")
    
    departments = ["General", "Plumbing", "Electrical", "Housekeeping", "Security"]
    employees = [
        {"user_id": "E101", "full_name": "Mike Johnson", "department": "General", "email": "mike@apartment.com"},
        {"user_id": "E102", "full_name": "Sarah Smith", "department": "Electrical", "email": "sarah@apartment.com"},
        {"user_id": "E103", "full_name": "David Wilson", "department": "Plumbing", "email": "david@apartment.com"},
        {"user_id": "E104", "full_name": "Priya Patel", "department": "Housekeeping", "email": "priya@apartment.com"},
        {"user_id": "E105", "full_name": "Rajesh Kumar", "department": "Security", "email": "rajesh@apartment.com"},
    ]
    
    print(f"   ✓ Generated {len(employees)} employees")
    return employees

def generate_tenants(apartments, occupancy_rate=0.90):
    """Generate tenants for apartments (85-95% occupancy)"""
    print("\n[4/6] Generating tenants...")
    
    num_tenants = int(len(apartments) * occupancy_rate)
    occupied_apartments = random.sample(apartments, num_tenants)
    
    tenants = []
    tenant_id = 1001
    
    # Date range for move-in (last 2 years)
    end_date = datetime(2025, 12, 1)
    start_date = end_date - timedelta(days=730)
    
    for apt in occupied_apartments:
        move_in_date = generate_date_in_range(start_date, end_date)
        monthly_rent = generate_rent(apt["room_type"])
        
        tenants.append({
            "tenant_id": f"T{tenant_id}",
            "tenant_name": generate_name(),
            "apartment_id": apt["apartment_id"],
            "block_no": apt["block_no"],
            "block_name": apt["block_name"],
            "room_no": apt["room_no"],
            "floor": apt["floor"],
            "room_type": apt["room_type"],
            "monthly_rent": monthly_rent,
            "move_in_date": move_in_date,
            "email": f"tenant{tenant_id}@apartment.com"
        })
        tenant_id += 1
    
    print(f"   ✓ Generated {len(tenants)} tenants ({occupancy_rate*100:.0f}% occupancy)")
    return tenants

def generate_payments(tenants):
    """Generate 6-12 months of payment history per tenant"""
    print("\n[5/6] Generating payment records...")
    
    payments = []
    payment_id = 10001
    
    reference_date = datetime(2025, 12, 11)
    
    for tenant in tenants:
        # Generate 6-12 months of payments
        num_payments = random.randint(6, 12)
        
        for month_offset in range(num_payments):
            payment_date = reference_date - timedelta(days=month_offset * 30)
            
            # Payment status distribution: 70% Paid, 20% Pending, 10% Overdue
            rand = random.random()
            if rand < 0.70:
                payment_status = "Paid"
            elif rand < 0.90:
                payment_status = "Pending"
            else:
                payment_status = "Overdue"
            
            # Payment amount (usually monthly rent, sometimes varies slightly)
            payment_amount = tenant["monthly_rent"] + random.randint(-100, 100)
            
            payments.append({
                "payment_id": f"P{payment_id}",
                "tenant_id": tenant["tenant_id"],
                "tenant_name": tenant["tenant_name"],
                "block_no": tenant["block_no"],
                "room_no": tenant["room_no"],
                "monthly_rent": tenant["monthly_rent"],
                "payment_amount": payment_amount,
                "payment_date": payment_date.strftime("%d-%m-%Y"),
                "payment_status": payment_status,
            })
            payment_id += 1
    
    print(f"   ✓ Generated {len(payments)} payment records")
    return payments

def generate_complaints(tenants, employees):
    """Generate 2-5 complaints per tenant over time"""
    print("\n[6/6] Generating complaint records...")
    
    complaints = []
    complaint_id = 1001
    
    # Employee IDs for assignment
    employee_ids = [e["user_id"] for e in employees]
    
    reference_date = datetime(2025, 12, 11)
    
    for tenant in tenants:
        # Generate 2-5 complaints per tenant
        num_complaints = random.randint(2, 5)
        
        for _ in range(num_complaints):
            # Random complaint category
            category = random.choice(list(COMPLAINT_CATEGORIES.keys()))
            complaint_text = generate_complaint_text(category)
            
            # Complaint status: 50% Resolved, 30% In Progress, 20% Pending
            rand = random.random()
            if rand < 0.50:
                complaint_status = "Resolved"
            elif rand < 0.80:
                complaint_status = "In Progress"
            else:
                complaint_status = "Pending"
            
            # Assign priority based on keywords
            text_lower = complaint_text.lower()
            priority = "Medium" # Default
            
            high_keywords = ["leak", "spark", "smoke", "fire", "crack", "buzzing", "trip", "fused", "overflow"]
            low_keywords = ["dust", "dirty", "mop", "garbage", "smell", "noise", "noisy", "flicker"]
            
            if any(k in text_lower for k in high_keywords):
                priority = "High"
            elif any(k in text_lower for k in low_keywords):
                priority = "Low"
                
            # Random date in last 6 months
            complaint_date = generate_date_in_range(
                reference_date - timedelta(days=180),
                reference_date
            )
            

            complaints.append({
                "complaint_id": f"C{complaint_id}",
                "tenant_id": tenant["tenant_id"],
                "tenant_name": tenant["tenant_name"],
                "block_no": tenant["block_no"],
                "room_no": tenant["room_no"],
                "complaint_text": complaint_text,
                "complaint_category": category,
                "complaint_status": complaint_status,
                "employee_id": random.choice(employee_ids),
                "created_date": complaint_date.strftime("%d-%m-%Y"),
                "priority": priority
            })
            complaint_id += 1
    
    print(f"   ✓ Generated {len(complaints)} complaint records")
    return complaints

def export_users_for_seeding(managers, employees, tenants):
    """Export all users to JSON for MySQL seeding"""
    import json
    
    users = []
    
    # Admin
    users.append({
        "user_id": "A001",
        "username": "admin",
        "email": "admin@apartment.com",
        "role": "Admin",
        "full_name": "System Administrator",
        "password": "password123"
    })
    
    # Owners / Managers
    for m in managers:
        users.append({
            "user_id": m["owner_id"],
            "username": m["email"].split('@')[0] if "email" in m else f"owner_{m['managed_building'].lower()}",
            "email": m.get("email", f"owner_{m['managed_building'].lower()}@apartment.com"),
            "role": "Owner",
            "full_name": m["owner_name"],
            "managed_building": m["managed_building"],
            "password": "password123"
        })
        
    # Employees
    for e in employees:
        users.append({
            "user_id": e["user_id"],
            "username": e["email"].split('@')[0],
            "email": e["email"],
            "role": "Employee",
            "full_name": e["full_name"],
            "department": e["department"],
            "password": "password123"
        })
        
    # Tenants
    for t in tenants:
        users.append({
            "user_id": t["tenant_id"],
            "username": f"tenant_{t['room_no']}",
            "email": t["email"],
            "role": "Tenant",
            "full_name": t["tenant_name"],
            "room_no": t["room_no"],
            "apartment_name": t["block_name"],
            "password": "password123"
        })
        
    with open("users_to_seed.json", "w") as f:
        json.dump(users, f, indent=4)
        
    print(f"\nExample Logins (All passwords: 'password123'):")
    print("-" * 50)
    print(f"Admin:     admin / admin@apartment.com")
    print(f"Owner B1:  {users[1]['email']}")
    print(f"Employee:  {employees[0]['email']} ({employees[0]['full_name']})")
    print(f"Tenant:    {tenants[0]['email']}")
    print("-" * 50)

def merge_all_data(apartments, managers, tenants, payments, complaints, employees):
    """Merge all data into final dataset (concatenated view)"""
    print("\n[7/7] Merging all data...")
    
    records = []
    
    # helper to get apt info
    def get_apt_info(tenant_id):
        tenant = next((t for t in tenants if t["tenant_id"] == tenant_id), None)
        if not tenant: return None
        
        # Find manager
        building_managers = [m for m in managers if m["managed_building"] == tenant["block_no"]]
        manager = random.choice(building_managers) if building_managers else managers[0]
        
        return {
            "block_no": tenant["block_no"],
            "block_name": tenant["block_name"],
            "room_no": tenant["room_no"],
            "floor": tenant["floor"],
            "room_type": tenant["room_type"],
            "owner_id": manager["owner_id"],
            "owner_name": manager["owner_name"],
            "tenant_id": tenant_id,
            "tenant_name": tenant["tenant_name"],
            "monthly_rent": tenant["monthly_rent"],
        }

    # 1. Add all payments
    for payment in payments:
        info = get_apt_info(payment["tenant_id"])
        if info:
            record = info.copy()
            record.update({
                "type": "Payment",
                "payment_id": payment["payment_id"],
                "payment_amount": payment["payment_amount"],
                "payment_date": payment["payment_date"],
                "payment_status": payment["payment_status"],
                # Fill complaint fields with None
                "employee_id": None,
                "complaint_id": None,
                "complaint_text": None,
                "complaint_category": None,
                "complaint_status": None,
                "created_date": None
            })
            records.append(record)
            
    # 2. Add all complaints
    for complaint in complaints:
        info = get_apt_info(complaint["tenant_id"])
        if info:
            record = info.copy()
            record.update({
                "type": "Complaint",
                # Fill payment fields with None
                "payment_id": None,
                "payment_amount": None,
                "payment_date": None,
                "payment_status": None,
                
                "employee_id": complaint["employee_id"],
                "complaint_id": complaint["complaint_id"],
                "complaint_text": complaint["complaint_text"],
                "complaint_category": complaint["complaint_category"],
                "complaint_status": complaint["complaint_status"],
                "created_date": complaint["created_date"]
            })
            records.append(record)
    
    print(f"   ✓ Created {len(records)} combined records (Payments + Complaints)")
    return records

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("=" * 70)
    print(f"GENERATING REALISTIC DATASET FOR {COMPANY_NAME}")
    print("=" * 70)
    
    # Generate all entities
    apartments = generate_apartments()
    managers = generate_property_managers(apartments)
    employees = generate_employees()
    tenants = generate_tenants(apartments, occupancy_rate=0.90)
    payments = generate_payments(tenants)
    complaints = generate_complaints(tenants, employees)
    
    # Export for seeding
    export_users_for_seeding(managers, employees, tenants)
    
    # Merge into final dataset
    records = merge_all_data(apartments, managers, tenants, payments, complaints, employees)
    
    # Create DataFrame
    df = pd.DataFrame(records)
    
    # Save to CSV
    output_file = "apartment_management_dataset_realistic_v2.csv"
    df.to_csv(output_file, index=False)
    
    print("\n" + "=" * 70)
    print("✅ DATASET GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total Records: {len(df)}")
    print(f"   Unique Apartments: {df['room_no'].nunique()}")
    print(f"   Unique Tenants: {df['tenant_id'].nunique()}")
    print(f"   Unique Owners/Managers: {df['owner_id'].nunique()}")
    print(f"   Unique Employees: {len(employees)}")
    print(f"   Unique Buildings: {df['block_no'].nunique()}")
    print(f"   Total Payments: {df['payment_id'].nunique()}")
    print(f"   Total Complaints: {df['complaint_id'].nunique()}")
    
    print(f"\n💾 Saved to: {output_file}")
    print(f"   File size: {len(df)} rows × {len(df.columns)} columns")
    
    print("\n📈 Data Distribution:")
    print(f"   Room Types:\n{df['room_type'].value_counts()}")
    print(f"\n   Payment Status:\n{df['payment_status'].value_counts()}")
    print(f"\n   Complaint Categories:\n{df['complaint_category'].value_counts()}")
    print(f"\n   Complaint Status:\n{df['complaint_status'].value_counts()}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
