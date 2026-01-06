"""
Check Admin Login
Tries to login as admin with common passwords to find the correct one.
"""

import requests

API_URL = "http://localhost:5000/api/auth/login"

def check_login():
    print("=" * 60)
    print("CHECKING ADMIN LOGIN PASSWORD")
    print("=" * 60)
    
    passwords_to_try = [
        'password123', 
        'Admin@123', 
        'Password@123', 
        'admin', 
        'root', 
        'admin123'
    ]
    
    found = False
    
    with open("admin_login_result.txt", "w") as f:
        for pwd in passwords_to_try:
            print(f"Trying password: '{pwd}'...", end=" ")
            try:
                response = requests.post(API_URL, json={
                    "username": "admin",
                    "password": pwd
                })
                
                if response.status_code == 200:
                    print("✅ SUCCESS!")
                    f.write(f"SUCCESS: {pwd}\n")
                    found = True
                    break
                else:
                    print(f"Failed ({response.status_code})")
                    f.write(f"FAILED: {pwd} ({response.status_code})\n")
                    
            except Exception as e:
                print(f"Error: {e}")
                f.write(f"ERROR: {e}\n")
                
        if not found:
            f.write("FAILURE: No password worked\n")

if __name__ == "__main__":
    check_login()
