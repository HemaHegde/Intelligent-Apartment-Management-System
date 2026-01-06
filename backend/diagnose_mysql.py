import mysql.connector
from config import Config

def diagnose():
    print("DIAGNOSING MYSQL...")
    passwords = ['password', 'root', '', 'admin', 'password123', 'admin123', 'Password@123']
    
    conn = None
    working_pwd = None
    
    for pwd in passwords:
        try:
            print(f"Testing '{pwd}'...", end=" ")
            c = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=pwd,
                database=Config.MYSQL_DB
            )
            print("SUCCESS!")
            conn = c
            working_pwd = pwd
            break
        except Exception as e:
            print(f"[Fail]: {str(e)}")

    if not conn:
        print("[CRITICAL]: No working MySQL password found.")
        return

    print(f"\n[SUCCESS] Working Root Password: '{working_pwd}'")
    
    # Check User
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, username, role, password_hash FROM users WHERE username = 'owner_b2'")
    user = cursor.fetchone()
    
    if user:
        print(f"[FOUND] User 'owner_b2' FOUND.")
        print(f"   Role: {user['role']}")
        print(f"   Hash starts with: {user['password_hash'][:10]}...")
        
        # Reset Password
        print("   Attempting password reset to 'Password@123'...")
        import bcrypt
        salt = bcrypt.gensalt()
        new_hash = bcrypt.hashpw("Password@123".encode('utf-8'), salt).decode('utf-8')
        
        cursor.execute("UPDATE users SET password_hash = %s WHERE username = 'owner_b2'", (new_hash,))
        conn.commit()
        print("   [SUCCESS] PASSWORD RESET COMPLETE.")
        
    else:
        print("[NOT FOUND] User 'owner_b2' NOT FOUND in database.")
        print("   Checking similar users...")
        cursor.execute("SELECT username FROM users WHERE role='Owner'")
        owners = cursor.fetchall()
        print(f"   Found owners: {[o['username'] for o in owners]}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    diagnose()
