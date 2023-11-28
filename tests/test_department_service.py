import unittest
from department_service.department_service import app, db, Department

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
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
        self.assertIn(b'Welcome to Department Service backend', response.data)

    def test_get_departments(self):
        response = self.app.get('/departments')
        self.assertEqual(response.status_code, 200)

    def test_create_department(self):
        response = self.app.post('/department', json={'name': 'HR', 'description': 'we gon h/fire you'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HR', response.data)

    def test_update_department(self):
        # Add a test department first
        dept = Department(name='IT', description='Information Technology')
        with app.app_context():
            db.session.add(dept)
            db.session.commit()
            dept_id = dept.id
        response = self.app.put(f'/department/{dept.id}', json={'name': 'IT Updated'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'IT Updated', response.data)

    def test_delete_department(self):
        # Add a test department first
        dept = Department(name='Finance', description='Finance Department')
        with app.app_context():
            db.session.add(dept)
            db.session.commit()
            dept_id = dept.id
        response = self.app.delete(f'/department/{dept.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Department deleted', response.data)

if __name__ == '__main__':
    unittest.main()
