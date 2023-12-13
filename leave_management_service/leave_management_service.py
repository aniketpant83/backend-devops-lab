from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaves.db'
db = SQLAlchemy(app)

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')  # pending, approved, denied

# Function to check if employee exists in the database
def verify_employee(employee_id):
    response = requests.get(f'http://employee-service:5000/employee/{employee_id}')
    return response.status_code == 200

@app.route('/')
def home():
    return jsonify({'message':'Welcome to leave management service backend'})

@app.route('/leave-requests', methods=['GET'])
def get_leave_requests():
    leave_requests = LeaveRequest.query.all()
    return jsonify([{
        'id': leave.id, 
        'employee_id': leave.employee_id,
        'start_date': leave.start_date.strftime('%Y-%m-%d'),
        'end_date': leave.end_date.strftime('%Y-%m-%d'),
        'status': leave.status
    } for leave in leave_requests])

@app.route('/leave-request', methods=['POST'])
def create_leave_request():
    data = request.get_json()

    # Check for employee in db
    if not verify_employee(data['employee_id']):
        return jsonify({'message': 'Employee not found'}), 404

    new_leave = LeaveRequest(
        employee_id=data['employee_id'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d')
    )
    db.session.add(new_leave)
    db.session.commit()
    return jsonify({'id': new_leave.id}), 201

@app.route('/leave-request/<int:request_id>', methods=['PUT'])
def update_leave_request(request_id):
    leave_request = LeaveRequest.query.get(request_id)
    if not leave_request:
        return jsonify({'message': 'Leave request not found'}), 404

    data = request.get_json()
    leave_request.status = data.get('status', leave_request.status)
    db.session.commit()
    return jsonify({
        'id': leave_request.id,
        'status': leave_request.status
    })

@app.route('/leave-request/<int:request_id>', methods=['DELETE'])
def delete_leave_request(request_id):
    leave_request = LeaveRequest.query.get(request_id)
    if not leave_request:
        return jsonify({'message': 'Leave request not found'}), 404

    db.session.delete(leave_request)
    db.session.commit()
    return jsonify({'message': 'Leave request deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host = '0.0.0.0', debug=True, port = 5003)
