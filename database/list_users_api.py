import requests
import json

def list_users():
    url = "http://localhost:5000/api/auth/debug/list-users"
    print(f"Fetching users from {url}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            users = response.json()
            print(f"Found {len(users)} users.")
            
            # Filter for owners
            owners = [u for u in users if u['role'] == 'Owner']
            print(f"Found {len(owners)} owners:")
            for o in owners:
                print(f" - {o['username']} (ID: {o['user_id']}, Bldg: {o.get('managed_building')}, Email: {o['email']})")
                
            # Check for owner_b2 username
            target = next((u for u in users if u['username'] == 'owner_b2'), None)
            if target:
                print(f"\n[FOUND USERNAME]: {target}")
            else:
                print("\n[MISSING USERNAME] 'owner_b2' not found.")

            # Check for owner_b2 email
            target_email = next((u for u in users if u['email'] == 'owner_b2@apartment.com'), None)
            if target_email:
                print(f"[FOUND EMAIL]: {target_email}")
            else:
                print("[MISSING EMAIL] 'owner_b2@apartment.com' not found.")
        else:
            print(f"Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_users()
