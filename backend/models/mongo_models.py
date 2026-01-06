"""
MongoDB Database Models
Collections for complaints, payments, predictions, analytics
"""

from pymongo import MongoClient
from datetime import datetime
from config import Config


def get_mongo_db():
    """Get MongoDB database connection"""
    client = MongoClient(Config.MONGO_URI)
    return client[Config.MONGO_DB]


class Complaint:
    """Complaint model"""
    
    @staticmethod
    def get_all(filters=None, limit=100, skip=0):
        """Get all complaints with optional filters"""
        db = get_mongo_db()
        query = filters or {}
        
        complaints = list(db.complaints.find(query)
                         .sort('created_at', -1)
                         .skip(skip)
                         .limit(limit))
        
        # Convert ObjectId to string
        for complaint in complaints:
            complaint['_id'] = str(complaint['_id'])
        
        return complaints
    
    @staticmethod
    def get_by_id(complaint_id):
        """Get complaint by ID"""
        db = get_mongo_db()
        complaint = db.complaints.find_one({'complaint_id': complaint_id})
        
        if complaint:
            complaint['_id'] = str(complaint['_id'])
        
        return complaint
    
    @staticmethod
    def create(complaint_data):
        """Create new complaint"""
        db = get_mongo_db()
        complaint_data['created_at'] = datetime.now()
        complaint_data['updated_at'] = datetime.now()
        
        result = db.complaints.insert_one(complaint_data)
        return str(result.inserted_id)
    
    @staticmethod
    def update(complaint_id, update_data):
        """Update complaint"""
        db = get_mongo_db()
        update_data['updated_at'] = datetime.now()
        
        result = db.complaints.update_one(
            {'complaint_id': complaint_id},
            {'$set': update_data}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def get_trends(days=30):
        """Get complaint trends"""
        db = get_mongo_db()
        
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'category': '$complaint_category',
                        'status': '$complaint_status'
                    },
                    'count': {'$sum': 1}
                }
            }
        ]
        
        trends = list(db.complaints.aggregate(pipeline))
        return trends


class Payment:
    """Payment model"""
    
    @staticmethod
    def get_all(filters=None, limit=100, skip=0):
        """Get all payments with optional filters"""
        db = get_mongo_db()
        query = filters or {}
        
        payments = list(db.payments.find(query)
                       .sort('payment_date', -1)
                       .skip(skip)
                       .limit(limit))
        
        for payment in payments:
            payment['_id'] = str(payment['_id'])
        
        return payments
    
    @staticmethod
    def get_by_tenant(tenant_id):
        """Get payments by tenant ID"""
        db = get_mongo_db()
        payments = list(db.payments.find({'tenant_id': tenant_id})
                       .sort('payment_date', -1))
        
        for payment in payments:
            payment['_id'] = str(payment['_id'])
        
        return payments
    
    @staticmethod
    def get_risk_alerts(threshold=0.5):
        """Get tenants at risk of payment delay"""
        db = get_mongo_db()
        
        at_risk = list(db.payments.find({
            'risk_score': {'$gte': threshold}
        }).sort('risk_score', -1))
        
        for payment in at_risk:
            payment['_id'] = str(payment['_id'])
        
        return at_risk
    
    @staticmethod
    def update_risk_score(payment_id, risk_score, delay_risk):
        """Update payment risk score"""
        db = get_mongo_db()
        
        result = db.payments.update_one(
            {'payment_id': payment_id},
            {'$set': {
                'risk_score': risk_score,
                'delay_risk': delay_risk
            }}
        )
        
        return result.modified_count > 0


class PredictionLog:
    """Prediction log model"""
    
    @staticmethod
    def create(log_data):
        """Create prediction log"""
        db = get_mongo_db()
        log_data['timestamp'] = datetime.now()
        
        result = db.prediction_logs.insert_one(log_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_recent(model_type=None, limit=50):
        """Get recent predictions"""
        db = get_mongo_db()
        
        query = {'model_type': model_type} if model_type else {}
        logs = list(db.prediction_logs.find(query)
                   .sort('timestamp', -1)
                   .limit(limit))
        
        for log in logs:
            log['_id'] = str(log['_id'])
        
        return logs


class Analytics:
    """Analytics model"""
    
    @staticmethod
    def get_summary_stats():
        """Get summary statistics for dashboard"""
        db = get_mongo_db()
        
        stats = {
            'total_apartments': db.apartments.count_documents({}),
            'total_complaints': db.complaints.count_documents({}),
            'total_payments': db.payments.count_documents({}),
            'pending_complaints': db.complaints.count_documents({'complaint_status': 'Pending'}),
            'overdue_payments': db.payments.count_documents({'payment_status': 'Overdue'}),
            'high_priority_complaints': db.complaints.count_documents({'priority': 'High'}),
        }
        
        return stats
