"""
Automated Verification Test Suite for CampusEnroll
Student Course Registration System
"""
import unittest
import os
import sqlite3
from app import app, get_db, MAX_CREDIT_LIMIT
from database.init_db import init_database

class CampusEnrollTestCase(unittest.TestCase):
    def setUp(self):
        # Reset and reseed the database before test run
        init_database()
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_01_landing_page(self):
        """Test public home page."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CampusEnroll', response.data)
        self.assertIn(b'Student Portal', response.data)

    def test_02_student_login_valid(self):
        """Test valid student login."""
        response = self.client.post('/login', data={
            'identifier': 'student@example.com',
            'password': 'student123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, Arvind Kumar Yadav', response.data)
        self.assertIn(b'Semester Credit Utilization', response.data)

    def test_02b_student_login_with_bwu_code(self):
        """Test valid student login using university roll code BWU/BTA/23/576."""
        response = self.client.post('/login', data={
            'identifier': 'BWU/BTA/23/576',
            'password': 'student123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, Arvind Kumar Yadav', response.data)
        self.assertIn(b'BWU/BTA/23/576', response.data)

    def test_03_student_login_invalid(self):
        """Test invalid student credentials."""
        response = self.client.post('/login', data={
            'identifier': 'student@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid Student ID/Email or password', response.data)

    def test_04_admin_login_valid(self):
        """Test valid admin login."""
        response = self.client.post('/admin/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Administrative Overview', response.data)
        self.assertIn(b'Course Inventory', response.data)

    def test_05_admin_login_invalid(self):
        """Test invalid admin credentials."""
        response = self.client.post('/admin/login', data={
            'username': 'admin',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid administrator credentials', response.data)

    def test_06_unauthorized_student_access(self):
        """Test student route protection when not logged in."""
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Please log in as a student', response.data)

    def test_07_unauthorized_admin_access(self):
        """Test admin route protection when not logged in."""
        response = self.client.get('/admin/dashboard', follow_redirects=True)
        self.assertIn(b'Please log in as an administrator', response.data)

    def test_08_browse_and_filter_courses(self):
        """Test course catalog filtering."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['role'] = 'student'
            sess['name'] = 'Arvind Kumar Yadav'

        # Filter by department
        response = self.client.get('/courses?department=AI+%26+Machine+Learning')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Introduction to Machine Learning', response.data)

        # Search query
        response = self.client.get('/courses?search=Compiler')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CS306', response.data)

    def test_09_course_registration_and_seat_decrement(self):
        """Test successful registration and seat decrement."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['role'] = 'student'
            sess['name'] = 'Arvind Kumar Yadav'

        conn = get_db()
        # Course 14 is CS306 (Compiler Design, 4 credits)
        course_before = conn.execute("SELECT available_seats FROM courses WHERE id = 14").fetchone()
        seats_before = course_before['available_seats']
        conn.close()

        # Register for course 14
        response = self.client.post('/register/14', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully registered for CS306', response.data)

        conn = get_db()
        course_after = conn.execute("SELECT available_seats FROM courses WHERE id = 14").fetchone()
        self.assertEqual(course_after['available_seats'], seats_before - 1)
        conn.close()

    def test_10_duplicate_registration_prevention(self):
        """Test preventing registering for the same course twice."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['role'] = 'student'
            sess['name'] = 'Arvind Kumar Yadav'

        # Student 1 is already registered for course 2 (CS302) in seed data
        response = self.client.post('/register/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You are already registered for CS302', response.data)

    def test_11_credit_limit_constraint(self):
        """Test enforcing maximum 24 credits limit."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['role'] = 'student'
            sess['name'] = 'Arvind Kumar Yadav'

        # Student 1 currently has 15 credits.
        # Add course 14 (4 credits) -> 19 credits
        self.client.post('/register/14', follow_redirects=True)
        # Add course 16 (4 credits) -> 23 credits
        self.client.post('/register/16', follow_redirects=True)

        # Now trying to add another 4-credit course (Course 1 - CS301, 4 cr) would make 27 > 24!
        response = self.client.post('/register/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'exceeds your semester credit limit of 24 credits', response.data)

    def test_12_drop_course_and_seat_increment(self):
        """Test dropping a course and verifying available seats increase."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['role'] = 'student'
            sess['name'] = 'Arvind Kumar Yadav'

        conn = get_db()
        # Student 1 is in course 2 (CS302)
        course_before = conn.execute("SELECT available_seats FROM courses WHERE id = 2").fetchone()
        seats_before = course_before['available_seats']
        conn.close()

        response = self.client.post('/drop/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully dropped course: CS302', response.data)

        conn = get_db()
        course_after = conn.execute("SELECT available_seats FROM courses WHERE id = 2").fetchone()
        self.assertEqual(course_after['available_seats'], seats_before + 1)
        conn.close()

    def test_13_weekly_timetable(self):
        """Test timetable displays enrolled classes."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['role'] = 'student'
            sess['name'] = 'Arvind Kumar Yadav'

        response = self.client.get('/timetable')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Weekly Class Timetable', response.data)
        self.assertIn(b'Monday', response.data)
        self.assertIn(b'Tuesday', response.data)

    def test_14_admin_add_course(self):
        """Test admin adding a new course."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['role'] = 'admin'
            sess['name'] = 'Administrator'

        response = self.client.post('/admin/courses/add', data={
            'course_code': 'AI409',
            'course_name': 'Robotics & Computer Vision',
            'department': 'AI & Machine Learning',
            'semester': '6',
            'credits': '4',
            'faculty': 'Dr. K. S. Rao',
            'max_seats': '35',
            'schedule': 'Mon, Thu 02:00 - 03:30 PM'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AI409', response.data)

        conn = get_db()
        new_course = conn.execute("SELECT * FROM courses WHERE course_code = 'AI409'").fetchone()
        self.assertIsNotNone(new_course)
        self.assertEqual(new_course['available_seats'], 35)
        conn.close()

    def test_15_admin_delete_course(self):
        """Test admin deleting a course."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['role'] = 'admin'
            sess['name'] = 'Administrator'

        # Delete course 17
        response = self.client.post('/admin/courses/delete/17', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'deleted successfully', response.data)

        conn = get_db()
        deleted = conn.execute("SELECT * FROM courses WHERE id = 17").fetchone()
        self.assertIsNone(deleted)
        conn.close()

if __name__ == '__main__':
    unittest.main()
