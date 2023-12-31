from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Employee Service Backend'})

# fetching all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{'id': emp.id, 'name': emp.name, 'position': emp.position} for emp in employees])

# fetching a particular employee
@app.route('/employees/<int:emp_id>')
def get_employee(emp_id):
    employee = Employee.query.get(emp_id)
    if employee is None:
        return jsonify({'message': 'Employee not found'}), 404
    return jsonify({'id':employee.id, 'name': employee.name, 'position': employee.position})

# creating an employee
@app.route('/employee', methods=['POST'])
def create_employee():
    data = request.get_json()
    new_employee = Employee(name=data['name'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'id': new_employee.id, 'name': new_employee.name, 'position': new_employee.position}), 201

# updating an employee
@app.route('/employee/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    employee = Employee.query.get(emp_id)

    # first checking if particular employee even exists
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404
    # updating
    data = request.get_json()
    employee.name = data.get('name', employee.name)
    employee.position = data.get('position', employee.position)
    db.session.commit()
    return jsonify({'id': employee.id, 'name': employee.name, 'position': employee.position})

# deleteing an employee
@app.route('/employee/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    employee = Employee.query.get(emp_id)

    #first checking if particular employee even exists
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host = '0.0.0.0', debug=True, port = 5001)
