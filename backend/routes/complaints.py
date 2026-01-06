"""
Complaint Routes
Complaint management and trend endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.mongo_models import Complaint, get_mongo_db
from models.mysql_models import User
from utils.ml_loader import ml_models
from datetime import datetime


complaints_bp = Blueprint('complaints', __name__)


@complaints_bp.route('/', methods=['GET'])
@jwt_required()
def get_complaints():
    """
    Get all complaints with role-based filtering
    - Admin: See ALL complaints
    - Owner: See complaints from their managed building only
    - Employee: See complaints assigned to them only
    - Tenant: See their own complaints only
    
    Query params: ?status=Pending&priority=High&category=Electricity
    """
    try:
        current_user_id = get_jwt_identity()
        current_user = User.find_by_id(current_user_id)
        
        # Build query based on role and filters
        query = {}
        
        # Role-based filtering
        if current_user['role'] == 'Tenant':
            # Tenants see only their own complaints
            query['tenant_id'] = current_user_id
        elif current_user['role'] == 'Employee':
            # Employees see only complaints assigned to them
            query['employee_id'] = current_user_id
        elif current_user['role'] == 'Owner':
            # Owners see complaints from their managed building only
            if current_user.get('managed_building'):
                query['block_no'] = current_user['managed_building']
        # Admin sees all complaints (no filter)
        
        # Add filters from query params
        if request.args.get('status'):
            query['complaint_status'] = request.args.get('status')
        if request.args.get('priority'):
            query['priority'] = request.args.get('priority')
        if request.args.get('category'):
            query['complaint_category'] = request.args.get('category')
        
        limit = int(request.args.get('limit', 100))
        skip = int(request.args.get('skip', 0))
        
        complaints = Complaint.get_all(query, limit, skip)
        
        return jsonify({
            'complaints': complaints,
            'count': len(complaints)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch complaints',
            'message': str(e)
        }), 500


@complaints_bp.route('/', methods=['POST'])
@jwt_required()
def create_complaint():
    """
    Create new complaint with auto-priority prediction
    Body: {
        "complaint_text": "Electric socket sparking",
        "complaint_category": "Electricity",
        "room_no": 126
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('complaint_text'):
            return jsonify({
                'error': 'Missing data',
                'message': 'Please provide complaint_text'
            }), 400
        
        current_user_id = get_jwt_identity()
        current_user = User.find_by_id(current_user_id)
        
        # Auto-predict priority
        prediction = ml_models.predict_complaint_priority(data['complaint_text'])
        
        # Generate complaint ID
        db = get_mongo_db()
        last_complaint = db.complaints.find_one(sort=[('complaint_id', -1)])
        new_id_num = int(last_complaint['complaint_id'][1:]) + 1 if last_complaint else 1001
        complaint_id = f'C{new_id_num}'
        
        # Create complaint document
        complaint_data = {
            'complaint_id': complaint_id,
            'tenant_id': current_user_id,
            'tenant_name': current_user['full_name'],
            'room_no': data.get('room_no'),
            'complaint_text': data['complaint_text'],
            'complaint_category': data.get('complaint_category', 'Other'),
            'complaint_status': 'Pending',
            'employee_id': None,
            'priority': prediction['priority'],
            'priority_confidence': prediction['confidence']
        }
        
        complaint_id = Complaint.create(complaint_data)
        
        return jsonify({
            'success': True,
            'message': 'Complaint created successfully',
            'complaint_id': complaint_data['complaint_id'],
            'priority': prediction['priority']
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to create complaint',
            'message': str(e)
        }), 500


@complaints_bp.route('/<complaint_id>', methods=['PUT'])
@jwt_required()
def update_complaint(complaint_id):
    """
    Update complaint status
    Body: {"complaint_status": "In Progress", "employee_id": "E104"}
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Missing data',
                'message': 'Please provide update data'
            }), 400
        
        success = Complaint.update(complaint_id, data)
        
        if not success:
            return jsonify({
                'error': 'Update failed',
                'message': 'Complaint not found or no changes made'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Complaint updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to update complaint',
            'message': str(e)
        }), 500


@complaints_bp.route('/trends', methods=['GET'])
@jwt_required()
def get_complaint_trends():
    """
    Get complaint trends for graphs
    Returns data grouped by category and status
    """
    try:
        db = get_mongo_db()
        
        # Trend by category
        category_pipeline = [
            {'$group': {
                '_id': '$complaint_category',
                'count': {'$sum': 1}
            }},
            {'$sort': {'count': -1}}
        ]
        category_trends = list(db.complaints.aggregate(category_pipeline))
        
        # Trend by status
        status_pipeline = [
            {'$group': {
                '_id': '$complaint_status',
                'count': {'$sum': 1}
            }}
        ]
        status_trends = list(db.complaints.aggregate(status_pipeline))
        
        # Trend by priority
        priority_pipeline = [
            {'$group': {
                '_id': '$priority',
                'count': {'$sum': 1}
            }}
        ]
        priority_trends = list(db.complaints.aggregate(priority_pipeline))
        
        return jsonify({
            'by_category': category_trends,
            'by_status': status_trends,
            'by_priority': priority_trends
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch trends',
            'message': str(e)
        }), 500
