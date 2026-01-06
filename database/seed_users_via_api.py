"""
Seed users via Backend API
Bypasses direct MySQL connection issues by using the public /register endpoint
"""

import requests
import json
import os
import time

API_URL = "http://localhost:5000/api/auth/register"

def seed_via_api():
    print("=" * 60)
    print("SEEDING USERS VIA API")
    print("=" * 60)
    
    # Load users
    json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users_to_seed.json')
    try:
        with open(json_path, 'r') as f:
            users = json.load(f)
    except Exception as e:
        print(f"❌ Error reading JSON: {e}")
        return

    print(f"Loaded {len(users)} users to register...")
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    # Login as Admin to enable deletions
    admin_token = None
    try:
        login_resp = requests.post("http://localhost:5000/api/auth/login", json={
            "username": "admin",
            "password": "Admin@123" # We confirmed this is the admin password
        })
        if login_resp.status_code == 200:
            admin_token = login_resp.json().get('access_token')
            print(" [✓] Admin authentication successful")
        else:
            print(" [!] Admin login failed. Cannot delete existing users.")
    except:
        print(" [!] Admin login error")

    for i, user in enumerate(users):
        # Prepare payload
        payload = {
            "username": user['username'],
            "email": user['email'],
            "password": "Password@123", 
            "full_name": user['full_name'],
            "role": user['role']
        }
        
        # Add role-specific fields
        if user['role'] == 'Owner':
            payload["apartment_name"] = "Office"
            payload["apartment_no"] = "OFF"
            if user.get('managed_building'):
                payload["managed_building"] = user['managed_building']
        elif user['role'] == 'Tenant':
            payload["room_no"] = user['room_no']
            payload["apartment_name"] = user['apartment_name']
        elif user['role'] == 'Employee':
            payload["department"] = user['department']

        try:
            # Attempt Register
            response = requests.post(API_URL, json=payload)
            
            if response.status_code in [200, 201]:
                print(f" [✓] Registered: {user['username']}")
                success_count += 1
                
            elif response.status_code == 409: # Conflict
                # Try to delete and re-register if we have admin token
                if admin_token and user['user_id']:
                    del_url = f"http://localhost:5000/api/auth/users/{user['user_id']}"
                    del_headers = {"Authorization": f"Bearer {admin_token}"}
                    
                    # Delete
                    del_resp = requests.delete(del_url, headers=del_headers)
                    
                    if del_resp.status_code in [200, 204]:
                        print(f" [R] Re-registering: {user['username']} (Deleted old)")
                        # Retry Register
                        retry_resp = requests.post(API_URL, json=payload)
                        if retry_resp.status_code in [200, 201]:
                            success_count += 1
                        else:
                            print(f" [X] Failed retry: {retry_resp.text}")
                            fail_count += 1
                    else:
                        print(f" [-] Skipped: {user['username']} (Exists & Delete failed)")
                        skip_count += 1
                else:
                    print(f" [-] Skipped: {user['username']} (Exists)")
                    skip_count += 1
            else:
                print(f" [X] Failed: {user['username']} - {response.text}")
                fail_count += 1
                
        except requests.exceptions.ConnectionError:
            return
        except Exception as e:
            print(f" [X] Error: {e}")
            fail_count += 1
            
        if i % 10 == 0: time.sleep(0.1)

    print("\n" + "=" * 60)
    print(f"SEEDING COMPLETE")
    print(f"Success: {success_count}")
    print(f"Skipped: {skip_count}")
    print(f"Failed:  {fail_count}")
    print("=" * 60)

if __name__ == "__main__":
    seed_via_api()
