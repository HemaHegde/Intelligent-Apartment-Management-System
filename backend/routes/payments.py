"""
Payment Routes
Payment management and risk alert endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.mongo_models import Payment, get_mongo_db
from models.mysql_models import User


payments_bp = Blueprint('payments', __name__)


@payments_bp.route('/', methods=['GET'])
@jwt_required()
def get_payments():
    """
    Get all payments with role-based filtering
    - Admin: See ALL payments
    - Owner: See payments from tenants in their managed building
    - Employee: NO ACCESS (employees don't handle payments)
    - Tenant: See their own payments only
    
    Query params: ?status=Overdue&tenant_id=T1001
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.find_by_id(current_user_id)
        
        # Employees should not access payment data
        if current_user['role'] == 'Employee':
            return jsonify({
                'error': 'Access denied',
                'message': 'Employees do not have access to payment information'
            }), 403
        
        # Build query based on role
        query = {}
        
        # Role-based filtering
        if current_user['role'] == 'Tenant':
            # Tenants see only their own payments
            query['tenant_id'] = current_user_id
        elif current_user['role'] == 'Owner':
            # Owners see payments from their managed building only
            if current_user.get('managed_building'):
                query['block_no'] = current_user['managed_building']
        # Admin sees all payments (no filter)
        
        # Add filters from query params
        if request.args.get('status'):
            query['payment_status'] = request.args.get('status')
        if request.args.get('tenant_id') and current_user['role'] in ['Admin', 'Owner']:
            query['tenant_id'] = request.args.get('tenant_id')
        
        limit = int(request.args.get('limit', 100))
        skip = int(request.args.get('skip', 0))
        
        payments = Payment.get_all(query, limit, skip)
        
        return jsonify({
            'payments': payments,
            'count': len(payments)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch payments',
            'message': str(e)
        }), 500


@payments_bp.route('/risk-alerts', methods=['GET'])
@jwt_required()
def get_risk_alerts():
    """
    Get tenants at risk of payment delay
    - Admin: See all risk alerts
    - Owner: See risk alerts for their building only
    - Employee/Tenant: NO ACCESS
    
    Query params: ?threshold=0.5
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.find_by_id(current_user_id)
        
        # Only Admin and Owner can access risk alerts
        if current_user['role'] not in ['Admin', 'Owner']:
            return jsonify({
                'error': 'Access denied',
                'message': 'Only Admin and Owner can view payment risk alerts'
            }), 403
        
        threshold = float(request.args.get('threshold', 0.5))
        
        at_risk = Payment.get_risk_alerts(threshold)
        
        # Filter by building for Owners
        if current_user['role'] == 'Owner' and current_user.get('managed_building'):
            at_risk = [p for p in at_risk if p.get('block_no') == current_user['managed_building']]
        
        return jsonify({
            'at_risk_payments': at_risk,
            'count': len(at_risk)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch risk alerts',
            'message': str(e)
        }), 500


@payments_bp.route('/trends', methods=['GET'])
@jwt_required()
def get_payment_trends():
    """
    Get payment trends for graphs
    Returns data grouped by status and month
    """
    try:
        db = get_mongo_db()
        
        # Trend by status
        status_pipeline = [
            {'$group': {
                '_id': '$payment_status',
                'count': {'$sum': 1},
                'total_amount': {'$sum': '$payment_amount'}
            }}
        ]
        status_trends = list(db.payments.aggregate(status_pipeline))
        
        # Monthly revenue trend
        monthly_pipeline = [
            {'$match': {'payment_status': 'Paid'}},
            {'$group': {
                '_id': {
                    '$substr': ['$payment_date', 3, 7]  # Extract MM-YYYY
                },
                'total_revenue': {'$sum': '$payment_amount'},
                'count': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        monthly_trends = list(db.payments.aggregate(monthly_pipeline))
        
        return jsonify({
            'by_status': status_trends,
            'by_month': monthly_trends
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch trends',
            'message': str(e)
        }), 500


@payments_bp.route('/tenant/<tenant_id>', methods=['GET'])
@jwt_required()
def get_tenant_payments(tenant_id):
    """
    Get payment history for a specific tenant
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.find_by_id(current_user_id)
        
        # Check authorization
        if current_user['role'] == 'Tenant' and current_user_id != tenant_id:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'You can only view your own payments'
            }), 403
        
        payments = Payment.get_by_tenant(tenant_id)
        
        return jsonify({
            'payments': payments,
            'count': len(payments)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch payments',
            'message': str(e)
        }), 500
