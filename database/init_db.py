"""
Database Initialization Script for CampusEnroll
Student Course Registration System
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')

def init_database():
    print(f"Connecting to database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Execute schema
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())
    print("Database tables created successfully.")

    # 1. Insert Admin
    cursor.execute("""
        INSERT INTO admins (username, password)
        VALUES (?, ?)
    """, ('admin', 'admin123'))

    # 2. Insert Sample Students (8 students)
    students = [
        ('BWU/BTA/23/576', 'Arvind Kumar Yadav', 'student@example.com', 'student123', 'B.Tech CSE (AI & ML)', 5, '9876543210'),
        ('BWU/BTA/23/577', 'Suman Giri', 'suman@example.com', 'student123', 'B.Tech CSE (AI & ML)', 5, '9876543211'),
        ('BWU/BTA/23/578', 'Rajkamal', 'rajkamal@example.com', 'student123', 'B.Tech Computer Science & Engineering', 5, '9876543212'),
        ('BWU/BTA/23/579', 'Ranjan', 'ranjan@example.com', 'student123', 'B.Tech Information Technology', 3, '9876543213'),
        ('BWU/BTA/23/580', 'Priya Patel', 'priya@example.com', 'student123', 'B.Tech Computer Science & Engineering', 3, '9876543214'),
        ('BWU/BTA/23/581', 'Sneha Reddy', 'sneha@example.com', 'student123', 'B.Tech CSE (AI & ML)', 3, '9876543215'),
        ('BWU/BTA/23/582', 'Aditya Kumar', 'aditya@example.com', 'student123', 'B.Tech Computer Science & Engineering', 5, '9876543216'),
        ('BWU/BTA/23/583', 'Ananya Iyer', 'ananya@example.com', 'student123', 'B.Tech Information Technology', 5, '9876543217')
    ]

    cursor.executemany("""
        INSERT INTO students (student_id, name, email, password, department, semester, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, students)

    # 3. Insert Sample Courses (18 courses across CSE, AI & ML, IT)
    courses = [
        ('CS301', 'Data Structures & Algorithms', 'Computer Science & Engineering', 3, 4, 'Dr. Rajesh Raman', 40, 40, 'Mon, Wed, Fri 09:00 - 10:00 AM'),
        ('CS302', 'Database Management Systems', 'Computer Science & Engineering', 5, 4, 'Prof. Sunita Rao', 45, 45, 'Tue, Thu 10:00 - 11:30 AM'),
        ('CS303', 'Operating Systems', 'Computer Science & Engineering', 5, 4, 'Dr. Amit Joshi', 40, 40, 'Mon, Wed 11:00 AM - 12:30 PM'),
        ('CS304', 'Computer Networks', 'Computer Science & Engineering', 5, 3, 'Prof. Vikram Sen', 35, 35, 'Tue, Thu 02:00 - 03:30 PM'),
        ('CS305', 'Software Engineering', 'Computer Science & Engineering', 5, 3, 'Dr. Kavita Menon', 50, 50, 'Wed, Fri 01:30 - 03:00 PM'),
        ('AI301', 'Introduction to Machine Learning', 'AI & Machine Learning', 5, 4, 'Dr. Sanjay Bhatt', 35, 35, 'Mon, Thu 10:00 - 11:30 AM'),
        ('AI302', 'Artificial Intelligence Principles', 'AI & Machine Learning', 5, 4, 'Prof. Deepa George', 35, 35, 'Tue, Fri 09:00 - 10:30 AM'),
        ('AI303', 'Deep Learning & Neural Networks', 'AI & Machine Learning', 5, 4, 'Dr. Vivek Pillai', 30, 30, 'Wed, Fri 10:00 - 11:30 AM'),
        ('CS201', 'Object Oriented Programming (Java)', 'Computer Science & Engineering', 3, 4, 'Prof. Neha Gupta', 45, 45, 'Mon, Wed 02:00 - 03:30 PM'),
        ('CS202', 'Discrete Mathematics', 'Computer Science & Engineering', 3, 3, 'Dr. R. K. Sharma', 50, 50, 'Tue, Thu 09:00 - 10:30 AM'),
        ('IT301', 'Web Technology & Full Stack', 'Information Technology', 5, 3, 'Prof. Arindam Bose', 40, 40, 'Mon, Wed 03:30 - 05:00 PM'),
        ('IT302', 'Cloud Computing Architecture', 'Information Technology', 5, 3, 'Dr. Shalini Saxena', 35, 35, 'Tue, Thu 11:30 AM - 01:00 PM'),
        ('AI201', 'Python for Data Science', 'AI & Machine Learning', 3, 3, 'Prof. Tanvi Deshmukh', 40, 40, 'Mon, Fri 01:00 - 02:30 PM'),
        ('CS306', 'Compiler Design', 'Computer Science & Engineering', 5, 4, 'Dr. Harish Prasad', 35, 35, 'Tue, Thu 03:30 - 05:00 PM'),
        ('IT303', 'Information Security & Cryptography', 'Information Technology', 5, 3, 'Prof. Ashok Nair', 35, 35, 'Mon, Wed 10:00 - 11:30 AM'),
        ('CS307', 'Design & Analysis of Algorithms', 'Computer Science & Engineering', 5, 4, 'Dr. Preeti Sinha', 40, 40, 'Tue, Fri 01:30 - 03:00 PM'),
        ('CS203', 'Computer Organization & Architecture', 'Computer Science & Engineering', 3, 3, 'Prof. M. Swaminathan', 45, 45, 'Wed, Fri 09:00 - 10:30 AM'),
        ('AI304', 'Natural Language Processing', 'AI & Machine Learning', 5, 3, 'Dr. Archana Das', 30, 30, 'Thu, Fri 02:00 - 03:30 PM')
    ]

    cursor.executemany("""
        INSERT INTO courses (course_code, course_name, department, semester, credits, faculty, max_seats, available_seats, schedule)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, courses)

    # 4. Insert Sample Registrations
    # Student 1 (Aarav Sharma): CS302 (DBMS), CS303 (OS), CS305 (Software Eng), AI301 (Machine Learning) -> 15 credits
    # Other students registered in a few courses
    sample_registrations = [
        (1, 2), # Student 1 in Course 2 (CS302)
        (1, 3), # Student 1 in Course 3 (CS303)
        (1, 5), # Student 1 in Course 5 (CS305)
        (1, 6), # Student 1 in Course 6 (AI301)
        (2, 6), # Student 2 in Course 6 (AI301)
        (2, 7), # Student 2 in Course 7 (AI302)
        (2, 8), # Student 2 in Course 8 (AI303)
        (3, 2), # Student 3 in Course 2 (CS302)
        (3, 4), # Student 3 in Course 4 (CS304)
        (4, 1), # Student 4 in Course 1 (CS301)
        (4, 10),# Student 4 in Course 10 (CS202)
        (5, 1), # Student 5 in Course 1 (CS301)
        (5, 9), # Student 5 in Course 9 (CS201)
        (7, 2), # Student 7 in Course 2 (CS302)
        (7, 3), # Student 7 in Course 3 (CS303)
        (8, 11),# Student 8 in Course 11 (IT301)
        (8, 12) # Student 8 in Course 12 (IT302)
    ]

    for student_id, course_id in sample_registrations:
        cursor.execute("""
            INSERT INTO registrations (student_id, course_id)
            VALUES (?, ?)
        """, (student_id, course_id))
        # Decrement available seats
        cursor.execute("""
            UPDATE courses
            SET available_seats = available_seats - 1
            WHERE id = ?
        """, (course_id,))

    conn.commit()
    conn.close()
    print("Database initialized successfully with sample data!")

if __name__ == '__main__':
    init_database()
