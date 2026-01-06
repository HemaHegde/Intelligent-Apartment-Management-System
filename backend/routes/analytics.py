"""
Analytics Routes
Employee performance and system analytics endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.mongo_models import get_mongo_db
from models.mysql_models import User
from datetime import datetime, timedelta


analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/employee-performance', methods=['GET'])
@jwt_required()
def get_employee_performance():
    """
    Get employee performance metrics (Admin only)
    Returns:
    - Complaints resolved per employee
    - Average resolution time
    - Current workload
    - Performance ranking
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
        
        # Get all employees
        all_users = User.get_all_users()
        employees = [u for u in all_users if u['role'] == 'Employee']
        
        performance_data = []
        
        for emp in employees:
            emp_id = emp['user_id']
            
            # Total complaints assigned
            total_assigned = db.complaints.count_documents({'employee_id': emp_id})
            
            # Resolved complaints
            resolved = db.complaints.count_documents({
                'employee_id': emp_id,
                'complaint_status': 'Resolved'
            })
            
            # In progress complaints
            in_progress = db.complaints.count_documents({
                'employee_id': emp_id,
                'complaint_status': 'In Progress'
            })
            
            # Pending complaints
            pending = db.complaints.count_documents({
                'employee_id': emp_id,
                'complaint_status': 'Pending'
            })
            
            # Calculate resolution rate
            resolution_rate = (resolved / total_assigned * 100) if total_assigned > 0 else 0
            
            performance_data.append({
                'employee_id': emp_id,
                'full_name': emp['full_name'],
                'department': emp.get('department', 'General'),
                'total_assigned': total_assigned,
                'resolved': resolved,
                'in_progress': in_progress,
                'pending': pending,
                'resolution_rate': round(resolution_rate, 1),
                'current_workload': in_progress + pending
            })
        
        # Sort by resolution rate (descending)
        performance_data.sort(key=lambda x: x['resolution_rate'], reverse=True)
        
        return jsonify({
            'employees': performance_data,
            'total_employees': len(employees)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch employee performance',
            'message': str(e)
        }), 500


@analytics_bp.route('/payment-analytics', methods=['GET'])
@jwt_required()
def get_payment_analytics():
    """
    Get detailed payment analytics (Admin only)
    Returns:
    - Collection rate
    - Revenue by building
    - Overdue trends
    - Top defaulters
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
        
        # Total payments
        total_payments = db.payments.count_documents({})
        paid_payments = db.payments.count_documents({'payment_status': 'Paid'})
        pending_payments = db.payments.count_documents({'payment_status': 'Pending'})
        overdue_payments = db.payments.count_documents({'payment_status': 'Overdue'})
        
        # Collection rate
        collection_rate = (paid_payments / total_payments * 100) if total_payments > 0 else 0
        
        # Revenue by building
        buildings = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8']
        revenue_by_building = []
        
        for building in buildings:
            pipeline = [
                {'$match': {'block_no': building, 'payment_status': 'Paid'}},
                {'$group': {'_id': None, 'total': {'$sum': '$payment_amount'}}}
            ]
            result = list(db.payments.aggregate(pipeline))
            revenue = result[0]['total'] if result else 0
            
            revenue_by_building.append({
                'building': building,
                'revenue': revenue
            })
        
        # Top defaulters (tenants with most overdue payments)
        defaulters_pipeline = [
            {'$match': {'payment_status': 'Overdue'}},
            {'$group': {
                '_id': '$tenant_id',
                'tenant_name': {'$first': '$tenant_name'},
                'block_no': {'$first': '$block_no'},
                'room_no': {'$first': '$room_no'},
                'overdue_count': {'$sum': 1},
                'total_overdue_amount': {'$sum': '$payment_amount'}
            }},
            {'$sort': {'overdue_count': -1}},
            {'$limit': 10}
        ]
        
        top_defaulters = list(db.payments.aggregate(defaulters_pipeline))
        
        return jsonify({
            'collection_rate': round(collection_rate, 1),
            'total_payments': total_payments,
            'paid_payments': paid_payments,
            'pending_payments': pending_payments,
            'overdue_payments': overdue_payments,
            'revenue_by_building': revenue_by_building,
            'top_defaulters': top_defaulters
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch payment analytics',
            'message': str(e)
        }), 500
