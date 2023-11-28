from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///departments.db'
db = SQLAlchemy(app)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))

@app.route('/')
def home():
    return jsonify({'message':'Welcome to Department Service backend'})

@app.route('/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    return jsonify([{'id': dept.id, 'name': dept.name, 'description': dept.description} for dept in departments])

@app.route('/department', methods=['POST'])
def create_department():
    data = request.get_json()
    new_dept = Department(name=data['name'], description=data.get('description', ''))
    db.session.add(new_dept)
    db.session.commit()
    return jsonify({'id': new_dept.id, 'name': new_dept.name, 'description': new_dept.description})
    
@app.route('/department/<int:dept_id>', methods=['PUT'])
def update_department(dept_id):
    department = Department.query.get(dept_id)
    if not department:
        return jsonify({'message': 'Department not found'}), 404

    data = request.get_json()
    department.name = data.get('name', department.name)
    department.description = data.get('description', department.description)
    db.session.commit()
    return jsonify({'id': department.id, 'name': department.name, 'description': department.description})

@app.route('/department/<int:dept_id>', methods=['DELETE'])
def delete_department(dept_id):
    department = Department.query.get(dept_id)
    if not department:
        return jsonify({'message': 'Department not found'}), 404

    db.session.delete(department)
    db.session.commit()
    return jsonify({'message': 'Department deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host = '0.0.0.0', debug=True, port = 5001)
