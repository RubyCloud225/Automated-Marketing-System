from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from subscriber_endpoints import SubscriberManager

app = Flask(__name__)
CORS(app)
DATABASE_URL = 'mysql+pymysql://username:password@localhost/db_name'
subscriber_manager = SubscriberManager(DATABASE_URL)

@app.route('/api/subscribers', methods=['GET'])
def get_subscribers():
    """Endpoint to get all active subscribers."""
    subscribers = subscriber_manager.get_subscribers()
    return jsonify(subscribers)

@app.route('/api/subscribers', methods=['POST'])
def add_subscriber():
    """Endpoint to add a new subscriber"""
    data = request.get_json()
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not email:
        return jsonify({"message": 'Email is required'}), 400
    
    try:
        new_subscriber = subscriber_manager.add_subscriber(email, first_name, last_name)
        return jsonify({'id': new_subscriber.id, 'email': new_subscriber.email}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/subscribers/<int:subscriber_id>', methods=['Delete'])
def delete_subscriber(subscriber_id):
    """Endpoint to delete"""
    if subscriber_manager.delete_subscriber(subscriber_id):
        return jsonify({'message': 'Subscriber deleted successfully'})
    return jsonify({'Message': 'Subscriber not found'})

@app.route('/api/subscribers/close', methods=['POST'])
def close_session():
    """Endpoint to close the database session"""
    subscriber_manager.close()
    return jsonify({'message': 'Session closed successfully'}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)