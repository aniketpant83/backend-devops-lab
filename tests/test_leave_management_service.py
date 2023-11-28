import unittest
from leave_management_service.leave_management_service import app, db, LeaveRequest
from unittest.mock import patch
from datetime import datetime

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
        self.assertIn('Welcome to leave management service backend', response.get_json()['message'])

    @patch('leave_management_service.leave_management_service.verify_employee', return_value=True)
    def test_create_leave_request(self, mock_verify):
        response = self.app.post('/leave-request', json={
            'employee_id': 1,
            'start_date': '2023-01-01',
            'end_date': '2023-01-10'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_get_leave_requests(self):
        # Create test data
        with app.app_context():
            leave1 = LeaveRequest(employee_id=1, start_date=datetime(2023, 1, 1), end_date=datetime(2023, 1, 10), status='pending')
            leave2 = LeaveRequest(employee_id=2, start_date=datetime(2023, 2, 1), end_date=datetime(2023, 2, 10), status='approved')
            db.session.add(leave1)
            db.session.add(leave2)
            db.session.commit()
        # Test GET request
        response = self.app.get('/leave-requests')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 2)

    def test_update_leave_request(self):
        # Create test data
        with app.app_context():
            leave = LeaveRequest(employee_id=1, start_date=datetime(2023, 1, 1), end_date=datetime(2023, 1, 10), status='pending')
            db.session.add(leave)
            db.session.commit()
            leave_id = leave.id
        # Test PUT request
        response = self.app.put(f'/leave-request/{leave_id}', json={'status': 'approved'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('approved', response.get_json()['status'])

    def test_delete_leave_request(self):
        # Create test data
        with app.app_context():
            leave = LeaveRequest(employee_id=3, start_date=datetime(2023, 3, 1), end_date=datetime(2023, 3, 10), status='pending')
            db.session.add(leave)
            db.session.commit()
            leave_id = leave.id
        # Test DELETE request
        response = self.app.delete(f'/leave-request/{leave_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Leave request deleted', response.get_json()['message'])



if __name__ == '__main__':
    unittest.main()
