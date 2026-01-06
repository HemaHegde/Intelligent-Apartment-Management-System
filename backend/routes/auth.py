"""
Authentication Routes
Login, logout, token verification, user registration
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.mysql_models import User
import re


auth_bp = Blueprint('auth', __name__)


def validate_password(password):
    """
    Validate password strength
    Returns: (is_valid: bool, errors: list)
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one number")
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        errors.append("Password must contain at least one special character")
    
    return (len(errors) == 0, errors)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    Body: {"username": "admin", "password": "password123"}
    Returns: JWT token and user info
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'error': 'Missing credentials',
                'message': 'Please provide username and password'
            }), 400
        
        username = data['username']
        password = data['password']
        
        # Find user
        user = User.find_by_username(username)
        
        if not user:
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'Username or password is incorrect'
            }), 401
        
        # Verify password
        if not User.verify_password(user['password_hash'], password):
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'Username or password is incorrect'
            }), 401
        
        # Update last login
        User.update_last_login(user['user_id'])
        
        # Create JWT token
        access_token = create_access_token(
            identity=user['user_id'],
            additional_claims={
                'role': user['role'],
                'username': user['username']
            }
        )
        
        # Prepare user data response
        user_data = {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'full_name': user['full_name']
        }
        
        # Add role-specific fields
        if user['role'] == 'Tenant':
            user_data['apartment_name'] = user.get('apartment_name')
            user_data['room_no'] = user.get('room_no')
        elif user['role'] == 'Owner':
            user_data['managed_building'] = user.get('managed_building')
            
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Login failed',
            'message': str(e)
        }), 500


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User registration endpoint (for all roles: Admin, Owner, Tenant, Employee)
    Body: {
        "username": "newuser",
        "email": "user@example.com",
        "password": "SecurePass123!",
        "full_name": "John Doe",
        "role": "Tenant|Owner|Employee|Admin",
        
        # Role-specific fields:
        "room_no": "101",              # Required for Tenant
        "apartment_name": "Sunrise",   # Required for Owner
        "apartment_no": "101",         # Required for Owner
        "department": "Maintenance"    # Required for Employee
    }
    Returns: Success message
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'full_name', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'error': 'Missing field',
                    'message': f'{field} is required'
                }), 400
        
        username = data['username']
        email = data['email']
        password = data['password']
        full_name = data['full_name']
        role = data['role']
        
        # Validate role
        valid_roles = ['Admin', 'Owner', 'Tenant', 'Employee']
        if role not in valid_roles:
            return jsonify({
                'error': 'Invalid role',
                'message': f'Role must be one of: {", ".join(valid_roles)}'
            }), 400
        
        # Validate role-specific fields
        room_no = None
        apartment_name = None
        apartment_no = None
        department = None
        managed_building = None
        
        if role == 'Tenant':
            room_no = data.get('room_no')
            apartment_name = data.get('apartment_name')
            if not room_no or not apartment_name:
                return jsonify({
                    'error': 'Missing field',
                    'message': 'Room number and apartment name are required for Tenant registration'
                }), 400
        
        elif role == 'Owner':
            apartment_name = data.get('apartment_name')
            apartment_no = data.get('apartment_no')
            managed_building = data.get('managed_building')  # B1-B8
            
            if not apartment_name or not apartment_no:
                return jsonify({
                    'error': 'Missing field',
                    'message': 'Apartment name and number are required for Owner registration'
                }), 400
            
            # Validate managed_building if provided
            if managed_building:
                valid_buildings = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']
                if managed_building not in valid_buildings:
                    return jsonify({
                        'error': 'Invalid building',
                        'message': f'Building must be one of: {", ".join(valid_buildings)}'
                    }), 400
        
        elif role == 'Employee':
            department = data.get('department')
            if not department:
                return jsonify({
                    'error': 'Missing field',
                    'message': 'Department is required for Employee registration'
                }), 400
        
        # Admin doesn't need additional fields
        
        # Validate password strength
        is_valid, errors = validate_password(password)
        if not is_valid:
            return jsonify({
                'error': 'Password validation failed',
                'message': 'Password does not meet security requirements',
                'errors': errors
            }), 400
        
        # Check if username already exists
        existing_user = User.find_by_username(username)
        if existing_user:
            return jsonify({
                'error': 'Username taken',
                'message': 'This username is already registered'
            }), 409
        
        # Check if email already exists
        existing_email = User.find_by_email(email)
        if existing_email:
            return jsonify({
                'error': 'Email taken',
                'message': 'This email is already registered'
            }), 409
        
        # Generate user_id based on role
        if role == 'Tenant':
            user_id = f"T{room_no}"
        elif role == 'Owner':
            user_id = f"O{apartment_no}"
        elif role == 'Admin':
            next_num = User.get_next_sequence_number('A')
            user_id = f"A{next_num:03d}"  # Format as A001, A002, etc.
        elif role == 'Employee':
            next_num = User.get_next_sequence_number('E')
            user_id = f"E{next_num:03d}"  # Format as E001, E002, etc.
        
        # Check if user_id already exists (for Tenant and Owner)
        if User.find_by_id(user_id):
            return jsonify({
                'error': 'ID conflict',
                'message': f'A user with ID {user_id} already exists. Please use a different {role.lower()}-specific identifier.'
            }), 409
        
        # Create new user
        User.create_user(
            user_id=user_id,
            username=username,
            email=email,
            password=password,  # Will be hashed in the model
            role=role,
            full_name=full_name,
            room_no=room_no,
            apartment_name=apartment_name,
            apartment_no=apartment_no,
            department=department,
            managed_building=managed_building
        )
        
        return jsonify({
            'message': 'Registration successful',
            'user': {
                'user_id': user_id,
                'username': username,
                'email': email,
                'role': role,
                'full_name': full_name,
                'managed_building': managed_building if role == 'Owner' else None
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Registration failed',
            'message': str(e)
        }), 500



@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """
    Verify JWT token validity
    Headers: Authorization: Bearer <token>
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'Invalid token'
            }), 401
        
        # Prepare user data response
        user_data = {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'full_name': user['full_name']
        }
        
        # Add role-specific fields
        if user['role'] == 'Tenant':
            user_data['apartment_name'] = user.get('apartment_name')
            user_data['room_no'] = user.get('room_no')
        elif user['role'] == 'Owner':
            user_data['managed_building'] = user.get('managed_building')
            
        return jsonify({
            'valid': True,
            'user': user_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Verification failed',
            'message': str(e)
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout endpoint (client-side token removal)
    """
    return jsonify({
        'message': 'Logout successful',
        'info': 'Please remove the token from client storage'
    }), 200


@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """
    Get all users (Admin only)
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.find_by_id(current_user_id)
        
        if current_user['role'] != 'Admin':
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Admin access required'
            }), 403
        
        users = User.get_all_users()
        
        return jsonify({
            'users': users,
            'count': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch users',
            'message': str(e)
        }), 500


@auth_bp.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    """
    Get all employees (for Owner/Admin to assign complaints)
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.find_by_id(current_user_id)
        
        # Only Owners and Admins can access this
        if current_user['role'] not in ['Owner', 'Admin']:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Owner or Admin access required'
            }), 403
        
        # Get all users with Employee role
        all_users = User.get_all_users()
        employees = [u for u in all_users if u['role'] == 'Employee']
        
        # Return simplified employee data
        employee_list = [{
            'user_id': emp['user_id'],
            'full_name': emp['full_name'],
            'department': emp.get('department', 'General')
        } for emp in employees]
        
        return jsonify({
            'employees': employee_list,
            'count': len(employee_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch employees',
            'message': str(e)
        }), 500


@auth_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Update user details (Admin only)
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.find_by_id(current_user_id)
        
        if current_user['role'] != 'Admin':
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Admin access required'
            }), 403
            
        data = request.get_json()
        
        # Only allow updating certain fields
        allowed_fields = ['full_name', 'email', 'managed_building', 'department', 'room_no', 'apartment_name', 'apartment_no', 'role']
        updates = {k: v for k, v in data.items() if k in allowed_fields}
        
        if not updates:
            return jsonify({
                'error': 'No valid fields',
                'message': 'No valid fields provided for update'
            }), 400
            
        # Update user in database
        # Note: We need to implement update_user in the User model if it doesn't exist
        # But assuming we use direct SQL or helper method
        User.update_user(user_id, updates)
        
        return jsonify({
            'message': 'User updated successfully',
            'updates': updates
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to update user',
            'message': str(e)
        }), 500


@auth_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    Delete user (Admin only)
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.find_by_id(current_user_id)
        
        if current_user['role'] != 'Admin':
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Admin access required'
            }), 403
            
        # Prevent self-deletion
        if user_id == current_user_id:
            return jsonify({
                'error': 'Operation denied',
                'message': 'Cannot delete your own account'
            }), 400
            
        # Delete user
        User.delete_user(user_id)
        
        return jsonify({
            'message': 'User deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to delete user',
            'message': str(e)
        }), 500
@auth_bp.route('/debug/reset-password', methods=['POST'])
def debug_reset_password():
    """
    Debug: Force reset password for a user
    """
    try:
        data = request.get_json()
        username = data.get('username')
        new_password = data.get('password')
        
        if not username or not new_password:
            return jsonify({'error': 'Missing fields'}), 400
            
        success = User.update_password(username, new_password)
        
        if success:
            return jsonify({'message': f'Password reset for {username}'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/debug/list-users', methods=['GET'])
def debug_list_users():
    """
    Debug: List all users to verify existence
    """
    try:
        users = User.get_all_users()
        # Sanitize for output
        safe_users = []
        for u in users:
            safe = {
                'user_id': u['user_id'],
                'username': u['username'],
                'role': u['role'],
                'email': u['email']
            }
            if 'managed_building' in u:
                safe['managed_building'] = u['managed_building']
            safe_users.append(safe)
            
        return jsonify(safe_users), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
