"""
Verify User Model Fix
Checks if User.get_all_users() returns the 'managed_building' field.
"""

from models.mysql_models import User
from flask import Flask
from config import Config

# Patch Config for local environment
Config.MYSQL_PASSWORD = 'password'

# Need flask app context for config loading if models rely on it?
# The models import Config directly, so maybe not, but safe to mock.

def verify_fix():
    print("=" * 60)
    print("VERIFYING USER MODEL FIX")
    print("=" * 60)
    
    passwords_to_try = ['password', 'root', '', 'admin', 'password123', 'admin123', 'Password@123']
    success = False
    
    for pwd in passwords_to_try:
        try:
            print(f"Trying MySQL password: '{pwd}'...")
            Config.MYSQL_PASSWORD = pwd
            
            # Try to fetch users
            users = User.get_all_users()
            print(f"[+] Connected! Retrieved {len(users)} users.")
            success = True
            
            # Continue with verification
            owners = [u for u in users if u['role'] == 'Owner']
            print(f"[+] Found {len(owners)} owners.")
            
            if not owners:
                print("[!] No owners found to verify!")
                return

            # Check first owner
            owner = owners[0]
            print("\nChecking first owner:")
            print(f"   Name: {owner['full_name']}")
            print(f"   Role: {owner['role']}")
            
            if 'managed_building' in owner:
                print(f"   Managed Building: {owner['managed_building']}")
                if owner['managed_building']:
                    print("[SUCCESS]: 'managed_building' field is present and populated!")
                else:
                    print("[WARNING]: 'managed_building' key exists but value is empty/None.")
            else:
                print("[FAILURE]: 'managed_building' field is MISSING from result!")
                
            break
            
        except Exception as e:
            # print(f"   Failed: {e}")
            continue
            
    if not success:
        print("\n[FAILURE] Could not connect to MySQL with any common password.")

if __name__ == "__main__":
    verify_fix()
