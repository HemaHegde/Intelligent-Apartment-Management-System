import requests
import json

API_URL = "http://localhost:5000/api/auth/login"

def check_owner_login():
    username = "owner_b2"
    passwords = ["Password@123", "password123", "admin123", "owner123"]
    
    print(f"Checking login for: {username}")
    
    for pwd in passwords:
        print(f"Trying '{pwd}'...", end=" ")
        try:
            response = requests.post(API_URL, json={
                "username": username,
                "password": pwd
            })
            
            if response.status_code == 200:
                print("✅ SUCCESS!")
                token = response.json().get('access_token')
                print(f"Token received: {token[:20]}...")
                return
            else:
                print(f"Failed ({response.status_code})")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    check_owner_login()
