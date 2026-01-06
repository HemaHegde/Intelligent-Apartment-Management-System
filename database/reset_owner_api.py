import requests
import json

def reset_password():
    url = "http://localhost:5000/api/auth/debug/reset-password"
    payload = {
        "username": "owner_b2",
        "password": "Password@123"
    }
    
    print(f"Calling debug reset for 'owner_b2'...")
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print("[SUCCESS] Password reset successful!")
            print(response.json())
        else:
            print(f"[FAILED] {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"[Error] {e}")

if __name__ == "__main__":
    reset_password()
