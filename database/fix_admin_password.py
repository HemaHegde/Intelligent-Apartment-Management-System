"""
Fix Admin Password
Directly updates the admin password in MySQL to ensure it matches the documentation: Password@123
"""

import mysql.connector
import bcrypt
import getpass

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password', 
    'database': 'apartment_management'
}

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def fix_password():
    print("=" * 60)
    print("FIXING ADMIN PASSWORD")
    print("=" * 60)
    
    conn = None
    passwords_to_try = ['password', 'root', '', 'admin', 'password123', 'admin123']
    
    # 1. Connect to MySQL with retry logic
    for pwd in passwords_to_try:
        try:
            current_config = DB_CONFIG.copy()
            if pwd == '':
                del current_config['password']
            else:
                current_config['password'] = pwd
                
            print(f"   Attempting connection with password: '{pwd}'...")
            conn = mysql.connector.connect(**current_config)
            if conn.is_connected():
                print(f"✓ Connected to MySQL with password: '{pwd}'")
                break
        except mysql.connector.Error:
            continue
            
    if not conn or not conn.is_connected():
        print("\n❌ Could not connect to MySQL. Cannot fix password.")
        return

    try:
        cursor = conn.cursor()
        
        # 2. Hash new password
        new_password = "Password@123"
        new_hash = hash_password(new_password)
        
        # 3. Update Admin user
        print(f"Updating password for user 'admin' to '{new_password}'...")
        update_query = "UPDATE users SET password_hash = %s WHERE username = 'admin'"
        cursor.execute(update_query, (new_hash,))
        
        if cursor.rowcount > 0:
            conn.commit()
            print("✅ Admin password updated successfully!")
        else:
            print("⚠️ User 'admin' not found!")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error updating password: {e}")

if __name__ == "__main__":
    fix_password()
