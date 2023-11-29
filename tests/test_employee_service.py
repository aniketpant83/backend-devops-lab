import unittest
from employee_service.employee_service import app, db, Employee

class EmployeeServiceTestCase(unittest.TestCase):
    # set up DB
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_employees.db'
        app.config['TESTING'] = True
        self.app = app.test_client()

        with app.app_context():
            db.create_all()
    # remove DB
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # test if home page is displaying the correct message
    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the Employee Service Backend', response.json['message'])

    # test if employees list is empty
    def test_get_employees_empty(self):
        response = self.app.get('/employees')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    # test if no employee being fetched is returning a 404
    def test_get_employee_empty(self):
        response = self.app.get('/employees/1')
        self.assertEqual(response.json['message'],'Employee not found')
        self.assertEqual(response.status_code, 404)

    # test creation of employee
    def test_create_employee(self):
        response = self.app.post('/employee', json={'name': 'Aniket Pant', 'position': 'DevOps'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'Aniket Pant')

    # test fetching of employee
    def test_get_employee(self):
        self.app.post('/employee', json={'name': 'Aniket Pant', 'position': 'DevOps'})
        response = self.app.get('/employees/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Aniket Pant')

    # test updation of employee details
    def test_update_employee(self):
        self.app.post('/employee', json={'name': 'Aniket Pant', 'position': 'DevOps'})
        response = self.app.put('/employee/1', json={'name': 'Aniket Pant', 'position': 'Developer'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Aniket Pant')

    # test deletion of employee
    def test_delete_employee(self):
        self.app.post('/employee', json={'name': 'Aniket Pant', 'position': 'DevOps'})
        response = self.app.delete('/employee/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Employee deleted', response.json['message'])

if __name__ == '__main__':
    unittest.main()
