import unittest
from employee_service import app, db, Employee

class EmployeeServiceTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_employees.db'
        app.config['TESTING'] = True
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the Employee Service Backend', response.json['message'])

    def test_get_employees_empty(self):
        response = self.app.get('/employees')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_employee(self):
        response = self.app.post('/employee', json={'name': 'Aniket Pant', 'position': 'DevOps'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Aniket Pant')

    def test_get_employee(self):
        # First, create an employee
        self.app.post('/employee', json={'name': 'Aniket Pant', 'position': 'DevOps'})
        response = self.app.get('/employees/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Aniket Pant')

    def test_update_employee(self):
        # First, create an employee
        self.app.post('/employee', json={'name': 'Aniket Pant', 'position': 'DevOps'})
        response = self.app.put('/employee/1', json={'name': 'Aniket Pant', 'position': 'Developer'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Aniket Pant')

    def test_delete_employee(self):
        # First, create an employee
        self.app.post('/employee', json={'name': 'Aniket Pant', 'position': 'DevOps'})
        response = self.app.delete('/employee/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Employee deleted', response.json['message'])

if __name__ == '__main__':
    unittest.main()
