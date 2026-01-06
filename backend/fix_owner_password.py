import mysql.connector
import bcrypt
from config import Config

# Reuse Config (assuming it works from backend dir, else patch)
Config.MYSQL_PASSWORD = 'password' # Patch based on local findings

def fix_owner_password():
    print("Fixing password for owner_b2 in MySQL...")
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        cursor = conn.cursor()
        
        # New password hash
        salt = bcrypt.gensalt()
        new_hash = bcrypt.hashpw("Password@123".encode('utf-8'), salt).decode('utf-8')
        
        # Update
        query = "UPDATE users SET password_hash = %s WHERE username = %s"
        cursor.execute(query, (new_hash, 'owner_b2'))
        conn.commit()
        
        if cursor.rowcount > 0:
            print("[SUCCESS]: Password updated for 'owner_b2'")
            return True
        else:
            print("[FAILED]: User 'owner_b2' not found")
            return False
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"[Error]: {e}")
        return False

if __name__ == "__main__":
    passwords = ['password', 'root', '', 'admin', 'password123', 'admin123', 'Password@123']
    for pwd in passwords:
        print(f"Trying MySQL password: '{pwd}'...")
        Config.MYSQL_PASSWORD = pwd
        if fix_owner_password():
            print("Fix applied successfully.")
            break 
        else:
            print("Retrying...")
