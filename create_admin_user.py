"""
Create Default Admin User
Creates a default admin account for initial login
"""

import sys
import os

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

from models.mysql_models import User

def create_admin_user():
    """Create default admin user"""
    
    print("=" * 60)
    print("CREATING DEFAULT ADMIN USER")
    print("=" * 60)
    
    # Check if admin already exists
    existing_admin = User.find_by_username('admin')
    if existing_admin:
        print("\n⚠️  Admin user already exists!")
        print(f"   Username: admin")
        print(f"   User ID: {existing_admin['user_id']}")
        print("\nIf you forgot the password, please delete the user and run this script again.")
        return
    
    # Create admin user
    print("\n[1/2] Creating admin user...")
    
    # Default credentials
    username = 'admin'
    email = 'admin@apartment.com'
    password = 'Admin@123'  # Strong password
    full_name = 'System Administrator'
    role = 'Admin'
    
    try:
        # Get next admin ID
        next_num = User.get_next_sequence_number('A')
        user_id = f"A{next_num:03d}"
        
        # Create user
        User.create_user(
            user_id=user_id,
            username=username,
            email=email,
            password=password,
            role=role,
            full_name=full_name
        )
        
        print(f"   ✓ Admin user created successfully!")
        print(f"\n[2/2] Login Credentials:")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        print(f"   User ID: {user_id}")
        
        print("\n" + "=" * 60)
        print("✅ ADMIN USER CREATED!")
        print("=" * 60)
        print("\n⚠️  IMPORTANT: Please change the password after first login!")
        print()
        
    except Exception as e:
        print(f"\n❌ Error creating admin user: {e}")
        raise

if __name__ == "__main__":
    create_admin_user()
