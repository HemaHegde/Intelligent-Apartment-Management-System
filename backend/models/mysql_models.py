"""
MySQL Database Models
User authentication model
"""

import mysql.connector
import bcrypt
from config import Config


def get_mysql_connection():
    """Get MySQL database connection"""
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )


class User:
    """User model for authentication"""
    
    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM users WHERE username = %s AND is_active = TRUE"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return user
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM users WHERE email = %s AND is_active = TRUE"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return user
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID (includes managed_building for Owners)"""
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM users WHERE user_id = %s AND is_active = TRUE"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return user
    
    @staticmethod
    def get_users_by_building(building_code):
        """Get all users (tenants) in a specific building"""
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        
        # This would need to join with apartment data from MongoDB
        # For now, return owners managing this building
        query = """SELECT user_id, username, email, role, full_name, managed_building
                   FROM users 
                   WHERE managed_building = %s AND role = 'Owner' AND is_active = TRUE"""
        cursor.execute(query, (building_code,))
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return users
    
    @staticmethod
    def verify_password(stored_hash, password):
        """Verify password against hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            stored_hash.encode('utf-8')
        )
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def update_last_login(user_id):
        """Update user's last login timestamp"""
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        query = "UPDATE users SET last_login = NOW() WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
    
    @staticmethod
    def get_all_users():
        """Get all users (admin only)"""
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT user_id, username, email, role, full_name, 
                   created_at, last_login, is_active,
                   managed_building, room_no, apartment_name, department
            FROM users 
            ORDER BY created_at DESC
        """
        cursor.execute(query)
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return users
    
    @staticmethod
    def create_user(user_id, username, email, password, role, full_name, 
                   room_no=None, apartment_name=None, apartment_no=None, department=None, managed_building=None):
        """
        Create a new user
        Password will be hashed automatically
        Supports role-specific fields:
        - room_no: for Tenants
        - apartment_name, apartment_no: for Owners (deprecated, use managed_building)
        - managed_building: for Owners (B1-B8)
        - department: for Employees
        """
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        # Hash the password
        password_hash = User.hash_password(password)
        
        query = """
            INSERT INTO users (user_id, username, email, password_hash, role, full_name,
                             room_no, apartment_name, apartment_no, department, managed_building)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, username, email, password_hash, role, full_name,
                              room_no, apartment_name, apartment_no, department, managed_building))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return True
    
    @staticmethod
    def get_next_sequence_number(role_prefix):
        """
        Get the next sequence number for auto-incrementing user IDs (Admin, Employee)
        Returns the next available number for the given role prefix
        """
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT user_id FROM users 
            WHERE user_id LIKE %s 
            ORDER BY user_id DESC 
            LIMIT 1
        """
        cursor.execute(query, (f"{role_prefix}%",))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            # Extract number from user_id (e.g., "A001" -> 1)
            last_num = int(result['user_id'][1:])
            return last_num + 1
        else:
            return 1
            
    @staticmethod
    def update_password(username, new_password):
        """Update user password (hashes it first)"""
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        password_hash = User.hash_password(new_password)
        
        try:
            query = "UPDATE users SET password_hash = %s WHERE username = %s"
            cursor.execute(query, (password_hash, username))
            conn.commit()
            updated = cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
            
        return updated

    @staticmethod
    def update_user(user_id, updates):
        """
        Update user details dynamically
        updates: dict of field_name -> new_value
        """
        if not updates:
            return False
            
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        try:
            # Build query dynamically
            set_clause = []
            values = []
            
            for key, value in updates.items():
                set_clause.append(f"{key} = %s")
                values.append(value)
                
            # Add user_id for WHERE clause
            values.append(user_id)
            
            query = f"UPDATE users SET {', '.join(set_clause)} WHERE user_id = %s"
            
            cursor.execute(query, tuple(values))
            conn.commit()
            
            return cursor.rowcount > 0
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

