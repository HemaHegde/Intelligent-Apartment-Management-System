"""
ML Prediction Routes
Complaint priority and payment delay prediction endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.ml_loader import ml_models
from models.mongo_models import PredictionLog, Complaint, Payment


ml_bp = Blueprint('ml', __name__)


@ml_bp.route('/predict-complaint-priority', methods=['POST'])
@jwt_required()
def predict_complaint_priority():
    """
    Predict complaint priority from text
    Body: {"complaint_text": "Electric socket sparking"}
    Returns: {"priority": "High", "confidence": 0.95}
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('complaint_text'):
            return jsonify({
                'error': 'Missing complaint text',
                'message': 'Please provide complaint_text in request body'
            }), 400
        
        complaint_text = data['complaint_text']
        
        # Get prediction
        result = ml_models.predict_complaint_priority(complaint_text)
        
        # Log prediction
        log_data = {
            'model_type': 'complaint_priority',
            'input_data': {'complaint_text': complaint_text},
            'output': result,
            'user_id': get_jwt_identity()
        }
        PredictionLog.create(log_data)
        
        return jsonify({
            'success': True,
            'prediction': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e)
        }), 500


@ml_bp.route('/predict-payment-delay', methods=['POST'])
@jwt_required()
def predict_payment_delay():
    """
    Predict payment delay risk
    Body: {
        "monthly_rent": 18503,
        "avg_payment": 18500,
        "payment_consistency": 0.01,
        "delay_rate": 0.2,
        "total_complaints": 5,
        "complaint_rate": 0.5,
        "avg_days_since_payment": 10,
        "room_type_encoded": 1,
        "complaint_category_encoded": 2,
        "complaint_status_encoded": 1
    }
    Returns: {"will_delay": true, "risk_score": 0.78}
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Missing data',
                'message': 'Please provide feature data in request body'
            }), 400
        
        # Get prediction
        result = ml_models.predict_payment_delay(data)
        
        # Log prediction
        log_data = {
            'model_type': 'payment_delay',
            'input_data': data,
            'output': result,
            'user_id': get_jwt_identity()
        }
        PredictionLog.create(log_data)
        
        return jsonify({
            'success': True,
            'prediction': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e)
        }), 500


@ml_bp.route('/prediction-logs', methods=['GET'])
@jwt_required()
def get_prediction_logs():
    """
    Get recent prediction logs
    Query params: ?model_type=complaint_priority&limit=50
    """
    try:
        model_type = request.args.get('model_type')
        limit = int(request.args.get('limit', 50))
        
        logs = PredictionLog.get_recent(model_type, limit)
        
        return jsonify({
            'logs': logs,
            'count': len(logs)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch logs',
            'message': str(e)
        }), 500


@ml_bp.route('/batch-predict-complaints', methods=['POST'])
@jwt_required()
def batch_predict_complaints():
    """
    Batch predict priorities for all complaints without priority
    Updates MongoDB with predictions
    """
    try:
        # Get complaints without priority
        complaints = Complaint.get_all({'priority': None})
        
        updated_count = 0
        
        for complaint in complaints:
            # Predict priority
            result = ml_models.predict_complaint_priority(complaint['complaint_text'])
            
            # Update complaint
            Complaint.update(complaint['complaint_id'], {
                'priority': result['priority'],
                'priority_confidence': result['confidence']
            })
            
            updated_count += 1
        
        return jsonify({
            'success': True,
            'message': f'Updated {updated_count} complaints with priority predictions'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Batch prediction failed',
            'message': str(e)
        }), 500
