"""
Apartment Routes
Apartment data and summary endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.mongo_models import get_mongo_db
from models.mysql_models import User


apartments_bp = Blueprint('apartments', __name__)


@apartments_bp.route('/', methods=['GET'])
@jwt_required()
def get_apartments():
    """
    Get all apartments with role-based filtering
    - Admin: See ALL apartments across all buildings
    - Owner: See apartments in their managed building only
    - Tenant: See their own apartment only
    - Employee: NO ACCESS
    
    Query params: ?block_no=B1&room_type=2BHK
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.find_by_id(current_user_id)
        
        # Employees don't need access to apartment listings
        if current_user['role'] == 'Employee':
            return jsonify({
                'error': 'Access denied',
                'message': 'Employees do not have access to apartment listings'
            }), 403
        
        db = get_mongo_db()
        
        # Build query from request args
        query = {}
        
        # Role-based filtering
        if current_user['role'] == 'Tenant':
            # Tenants see only their own apartment
            if current_user.get('room_no'):
                query['room_no'] = current_user['room_no']
        elif current_user['role'] == 'Owner':
            # Owners see apartments in their managed building only
            if current_user.get('managed_building'):
                query['block_no'] = current_user['managed_building']
        # Admin sees all apartments (no filter)
        
        # Add filters from query params (Admin and Owner only)
        if current_user['role'] in ['Admin', 'Owner']:
            if request.args.get('block_no'):
                query['block_no'] = request.args.get('block_no')
            if request.args.get('room_type'):
                query['room_type'] = request.args.get('room_type')
            if request.args.get('owner_id'):
                query['owner_id'] = request.args.get('owner_id')
            if request.args.get('tenant_id'):
                query['tenant_id'] = request.args.get('tenant_id')
        
        apartments = list(db.apartments.find(query))
        
        # Convert ObjectId to string
        for apt in apartments:
            apt['_id'] = str(apt['_id'])
        
        return jsonify({
            'apartments': apartments,
            'count': len(apartments)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch apartments',
            'message': str(e)
        }), 500


@apartments_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    """
    Get apartment summary statistics for dashboard
    """
    try:
        db = get_mongo_db()
        
        # Get current user
        current_user_id = get_jwt_identity()
        current_user = User.find_by_id(current_user_id)
        
        # Build query based on role
        apartment_query = {}
        complaint_query = {}
        payment_query = {}
        
        if current_user['role'] == 'Owner':
            # Owners see data from their managed building only
            if current_user.get('managed_building'):
                apartment_query['block_no'] = current_user['managed_building']
                complaint_query['block_no'] = current_user['managed_building']
                payment_query['block_no'] = current_user['managed_building']
        elif current_user['role'] == 'Tenant':
            apartment_query['tenant_id'] = current_user_id
            complaint_query['tenant_id'] = current_user_id
            payment_query['tenant_id'] = current_user_id
        elif current_user['role'] == 'Employee':
            complaint_query['employee_id'] = current_user_id
        
        # Get statistics
        summary = {
            'total_apartments': db.apartments.count_documents(apartment_query),
            'total_complaints': db.complaints.count_documents(complaint_query),
            'total_payments': db.payments.count_documents(payment_query),
            'pending_complaints': db.complaints.count_documents({**complaint_query, 'complaint_status': 'Pending'}),
            'in_progress_complaints': db.complaints.count_documents({**complaint_query, 'complaint_status': 'In Progress'}),
            'resolved_complaints': db.complaints.count_documents({**complaint_query, 'complaint_status': 'Resolved'}),
            'high_priority_complaints': db.complaints.count_documents({**complaint_query, 'priority': 'High'}),
            'medium_priority_complaints': db.complaints.count_documents({**complaint_query, 'priority': 'Medium'}),
            'low_priority_complaints': db.complaints.count_documents({**complaint_query, 'priority': 'Low'}),
            'paid_payments': db.payments.count_documents({**payment_query, 'payment_status': 'Paid'}),
            'pending_payments': db.payments.count_documents({**payment_query, 'payment_status': 'Pending'}),
            'overdue_payments': db.payments.count_documents({**payment_query, 'payment_status': 'Overdue'}),
        }
        
        # Calculate total revenue (for Admin and Owner)
        if current_user['role'] in ['Admin', 'Owner']:
            pipeline = [
                {'$match': {**payment_query, 'payment_status': 'Paid'}},
                {'$group': {'_id': None, 'total': {'$sum': '$payment_amount'}}}
            ]
            revenue_result = list(db.payments.aggregate(pipeline))
            summary['total_revenue'] = revenue_result[0]['total'] if revenue_result else 0
        
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch summary',
            'message': str(e)
        }), 500


@apartments_bp.route('/<room_no>', methods=['GET'])
@jwt_required()
def get_apartment_details(room_no):
    """
    Get detailed information about a specific apartment
    """
    try:
        db = get_mongo_db()
        
        apartment = db.apartments.find_one({'room_no': int(room_no)})
        
        if not apartment:
            return jsonify({
                'error': 'Apartment not found',
                'message': f'No apartment found with room number {room_no}'
            }), 404
        
        apartment['_id'] = str(apartment['_id'])
        
        # Get related complaints
        complaints = list(db.complaints.find({'room_no': int(room_no)}))
        for c in complaints:
            c['_id'] = str(c['_id'])
        
        # Get related payments
        payments = list(db.payments.find({'room_no': int(room_no)}))
        for p in payments:
            p['_id'] = str(p['_id'])
        
        return jsonify({
            'apartment': apartment,
            'complaints': complaints,
            'payments': payments
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch apartment details',
            'message': str(e)
        }), 500


@apartments_bp.route('/buildings/summary', methods=['GET'])
@jwt_required()
def get_buildings_summary():
    """
    Get summary statistics for all buildings (Admin only)
    Returns stats for each of the 8 buildings
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.find_by_id(current_user_id)
        
        # Only Admin can access this
        if current_user['role'] != 'Admin':
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Admin access required'
            }), 403
        
        db = get_mongo_db()
        
        buildings = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']
        building_names = {
            'B1': 'Maple Heights',
            'B2': 'Harmony Residency',
            'B3': 'Sunrise Enclave',
            'B4': 'Lakeview Towers',
            'B5': 'Green Meadows',
            'B6': 'Silver Oaks',
            'B7': 'Crystal View',
            'B8': 'Riverside Park'
        }
        
        building_stats = []
        
        for building_code in buildings:
            # Get stats for this building
            total_apartments = db.apartments.count_documents({'block_no': building_code})
            total_complaints = db.complaints.count_documents({'block_no': building_code})
            pending_complaints = db.complaints.count_documents({
                'block_no': building_code,
                'complaint_status': 'Pending'
            })
            
            # Calculate revenue
            revenue_pipeline = [
                {'$match': {'block_no': building_code, 'payment_status': 'Paid'}},
                {'$group': {'_id': None, 'total': {'$sum': '$payment_amount'}}}
            ]
            revenue_result = list(db.payments.aggregate(revenue_pipeline))
            total_revenue = revenue_result[0]['total'] if revenue_result else 0
            
            # Get assigned owner
            all_users = User.get_all_users()
            assigned_owner = next((u for u in all_users if u.get('managed_building') == building_code and u['role'] == 'Owner'), None)
            
            building_stats.append({
                'building_code': building_code,
                'building_name': building_names[building_code],
                'total_apartments': total_apartments,
                'total_complaints': total_complaints,
                'pending_complaints': pending_complaints,
                'total_revenue': total_revenue,
                'owner': {
                    'user_id': assigned_owner['user_id'] if assigned_owner else None,
                    'full_name': assigned_owner['full_name'] if assigned_owner else 'Unassigned'
                } if assigned_owner else None
            })
        
        return jsonify({
            'buildings': building_stats,
            'total_buildings': len(buildings)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch building summary',
            'message': str(e)
        }), 500
