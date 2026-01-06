"""
Seed MySQL database with demo users
Creates users for all 4 roles with hashed passwords
"""

import mysql.connector
import bcrypt
from datetime import datetime
import getpass


# Database configuration (password will be prompted)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change as needed
    'database': 'apartment_management'
}

# Demo users (password: 'password123' for all)
DEMO_USERS = [
    {
        'user_id': 'A001',
        'username': 'admin',
        'email': 'admin@apartment.com',
        'password': 'Admin@123',
        'role': 'Admin',
        'full_name': 'System Administrator'
    },
    {
        'user_id': 'O101',
        'username': 'owner1',
        'email': 'owner1@apartment.com',
        'password': 'Owner@123',
        'role': 'Owner',
        'full_name': 'John Owner'
    },
    {
        'user_id': 'T126',
        'username': 'tenant1',
        'email': 'tenant1@apartment.com',
        'password': 'Tenant@123',
        'role': 'Tenant',
        'full_name': 'Jane Tenant'
    },
    {
        'user_id': 'E104',
        'username': 'employee1',
        'email': 'employee1@apartment.com',
        'password': 'Employee@123',
        'role': 'Employee',
        'full_name': 'Mike Employee'
    }
]


def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def seed_users():
    """Seed database with demo users"""
    
    print("=" * 60)
    print("SEEDING MYSQL DATABASE WITH DEMO USERS")
    print("=" * 60)
    
    try:
        # Prompt for MySQL password
        print("\n[1/4] Enter MySQL root password:")
        mysql_password = getpass.getpass("Password: ")
        
        # Add password to config
        db_config = DB_CONFIG.copy()
        db_config['password'] = mysql_password
        
        # Connect to database
        print("\n[2/4] Connecting to MySQL database...")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("   ✓ Connected successfully")
        
        # Clear existing users (optional)
        print("\n[3/4] Clearing existing demo users...")
        cursor.execute("DELETE FROM users WHERE user_id IN ('ADMIN001', 'O1001', 'T1001', 'E104')")
        conn.commit()
        print("   ✓ Cleared existing users")
        
        # Insert demo users
        print("\n[4/4] Inserting demo users...")
        insert_query = """
            INSERT INTO users (user_id, username, email, password_hash, role, full_name)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        for user in DEMO_USERS:
            password_hash = hash_password(user['password'])
            cursor.execute(insert_query, (
                user['user_id'],
                user['username'],
                user['email'],
                password_hash,
                user['role'],
                user['full_name']
            ))
            print(f"   ✓ Created user: {user['username']} ({user['role']})")
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ DEMO USERS CREATED SUCCESSFULLY!")
        print("=" * 60)
        print("\nLogin Credentials (all passwords: 'password123'):")
        print("-" * 60)
        for user in DEMO_USERS:
            print(f"  {user['role']:10s} | {user['email']:25s} | {user['username']}")
        print("-" * 60)
        
        # Close connection
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"\n❌ Error: {err}")
        print("\nℹ️  Make sure MySQL is running and database 'apartment_management' exists")
        print("   Run: mysql -u root -p < mysql_schema.sql")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    seed_users()
