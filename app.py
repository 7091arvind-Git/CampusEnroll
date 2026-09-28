"""
CampusEnroll – Student Course Registration System
Main Flask Application

Developed for Academic Software Engineering Lab Showcase.
Stack: Python Flask, SQLite, Jinja2, Bootstrap 5, Vanilla JS.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from functools import wraps

# ==============================================================================
# SMART ENVIRONMENT SAFEGUARDS
# ==============================================================================
def _load_env_safeguards():
    """
    Smart Environment Loader:
    Reads .env file safely without requiring third-party libraries if not installed.
    Provides bulletproof fallbacks for all critical application settings.
    """
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        os.environ.setdefault(k.strip(), v.strip().strip("'\""))
        except Exception as e:
            print(f"[Smart Safeguard] Notice: Could not read .env ({e}), using safe defaults.")

_load_env_safeguards()

app = Flask(__name__)

# Smart Session Secret Key Safeguard (Environment variable with secure fallback)
app.secret_key = os.environ.get('SECRET_KEY', 'campusenroll-academic-lab-secret-key-bwu-2024')

# Maximum allowed credits per semester (configurable via environment, default 24)
try:
    MAX_CREDIT_LIMIT = int(os.environ.get('MAX_CREDIT_LIMIT', 24))
except ValueError:
    MAX_CREDIT_LIMIT = 24

# Database Path Configuration
DB_PATH = os.environ.get('DATABASE_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db'))

def _ensure_database_safeguard():
    """
    Self-Healing Database Safeguard:
    Checks if database.db exists and has the required schema.
    If database is missing or empty when cloned from GitHub, it auto-initializes seamlessly!
    """
    needs_init = False
    if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) == 0:
        needs_init = True
    else:
        try:
            conn = sqlite3.connect(DB_PATH)
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'").fetchone()
            conn.close()
            if not tables:
                needs_init = True
        except Exception:
            needs_init = True

    if needs_init:
        print("[Smart Safeguard] Database missing or empty. Auto-initializing schema & seed data...")
        try:
            from database.init_db import init_database
            init_database()
            print("[Smart Safeguard] Database successfully auto-initialized.")
        except Exception as e:
            print(f"[Smart Safeguard] Error during database auto-init: {e}")

_ensure_database_safeguard()

# HTTP Security Headers Safeguard
@app.after_request
def apply_security_headers(response):
    """Injects essential security headers protecting against sniffing, clickjacking, and XSS."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


# ==============================================================================
# DATABASE CONNECTION HELPER
# ==============================================================================
def get_db():
    """
    Establish a connection to the SQLite database.
    Row factory is set to sqlite3.Row so columns can be accessed by name.
    Foreign key enforcement is enabled.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ==============================================================================
# AUTHENTICATION DECORATORS
# ==============================================================================
def student_required(f):
    """Decorator to protect student-only routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'student':
            flash('Please log in as a student to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to protect admin-only routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Please log in as an administrator to access this area.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# ==============================================================================
# CONTEXT PROCESSOR (Inject common variables into all templates)
# ==============================================================================
@app.context_processor
def inject_global_data():
    """Makes max credit limit and up-to-date user info accessible to all Jinja2 templates."""
    role = session.get('role')
    user_id = session.get('user_id')
    user_name = session.get('name')
    student_id = session.get('student_id')
    department = session.get('department')

    # If student is logged in, query database to guarantee fresh name & branch
    if user_id and role == 'student':
        try:
            conn = get_db()
            row = conn.execute(
                "SELECT name, student_id, department FROM students WHERE id = ?",
                (user_id,)
            ).fetchone()
            conn.close()
            if row:
                user_name = row['name']
                student_id = row['student_id']
                department = row['department']
                # Sync session cookie so changes are immediately reflected
                session['name'] = user_name
                session['student_id'] = student_id
                session['department'] = department
        except Exception:
            pass
    elif user_id and role == 'admin':
        user_name = 'Administrator'

    return {
        'MAX_CREDIT_LIMIT': MAX_CREDIT_LIMIT,
        'current_user': {
            'is_logged_in': user_id is not None,
            'role': role,
            'name': user_name,
            'student_id': student_id,
            'department': department
        }
    }


# ==============================================================================
# PUBLIC ROUTES
# ==============================================================================
@app.route('/')
def index():
    """Landing Page: Overview of CampusEnroll, quick stats, and login options."""
    conn = get_db()
    total_courses = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    total_registrations = conn.execute("SELECT COUNT(*) FROM registrations").fetchone()[0]
    conn.close()

    return render_template('index.html',
                           total_courses=total_courses,
                           total_students=total_students,
                           total_registrations=total_registrations)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Student Login: Authenticates by Student ID or Email and Password."""
    if 'user_id' in session and session.get('role') == 'student':
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '').strip()

        if not identifier or not password:
            flash('Please enter both Student ID/Email and password.', 'danger')
            return render_template('login.html')

        conn = get_db()
        # Look up student by student_id or email
        student = conn.execute("""
            SELECT * FROM students 
            WHERE (student_id = ? OR email = ?) AND password = ?
        """, (identifier, identifier, password)).fetchone()
        conn.close()

        if student:
            # Set session variables
            session['user_id'] = student['id']
            session['role'] = 'student'
            session['name'] = student['name']
            session['student_id'] = student['student_id']
            session['department'] = student['department']
            session['semester'] = student['semester']
            flash(f"Welcome back, {student['name']}!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Student ID/Email or password. Please try again.', 'danger')

    return render_template('login.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin Login: Authenticates administrator by username and password."""
    if 'user_id' in session and session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Please enter both username and password.', 'danger')
            return render_template('admin_login.html')

        conn = get_db()
        admin = conn.execute("""
            SELECT * FROM admins 
            WHERE username = ? AND password = ?
        """, (username, password)).fetchone()
        conn.close()

        if admin:
            session['user_id'] = admin['id']
            session['role'] = 'admin'
            session['name'] = 'Administrator'
            flash('Logged in successfully as Administrator.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid administrator credentials.', 'danger')

    return render_template('admin_login.html')


@app.route('/logout')
def logout():
    """Logs out current user and clears session."""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


# ==============================================================================
# STUDENT ROUTES
# ==============================================================================
@app.route('/dashboard')
@student_required
def dashboard():
    """Student Dashboard: Profile highlights, credit summary, and enrolled courses."""
    student_id = session['user_id']
    conn = get_db()

    # Get student profile
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    # Get registered courses for this student
    registered_courses = conn.execute("""
        SELECT c.*, r.registration_date 
        FROM courses c
        JOIN registrations r ON c.id = r.course_id
        WHERE r.student_id = ?
        ORDER BY r.registration_date DESC
    """, (student_id,)).fetchall()

    # Calculate total registered credits
    total_credits = sum(c['credits'] for c in registered_courses)
    total_courses_count = len(registered_courses)

    # Remaining credits allowed
    remaining_credits = MAX_CREDIT_LIMIT - total_credits
    credit_percent = min(100, int((total_credits / MAX_CREDIT_LIMIT) * 100))

    conn.close()

    return render_template('dashboard.html',
                           student=student,
                           registered_courses=registered_courses,
                           total_credits=total_credits,
                           total_courses_count=total_courses_count,
                           remaining_credits=remaining_credits,
                           credit_percent=credit_percent)


@app.route('/courses')
@student_required
def browse_courses():
    """
    Browse Courses:
    Lists courses with search by name/code and filters by department, semester, credits.
    Highlights already-registered courses.
    """
    student_id = session['user_id']
    search_query = request.args.get('search', '').strip()
    selected_dept = request.args.get('department', '').strip()
    selected_sem = request.args.get('semester', '').strip()
    selected_credits = request.args.get('credits', '').strip()

    conn = get_db()

    # Fetch IDs of courses the student is already registered for
    reg_rows = conn.execute("SELECT course_id FROM registrations WHERE student_id = ?", (student_id,)).fetchall()
    registered_course_ids = {row['course_id'] for row in reg_rows}

    # Calculate current student credits
    current_credits_row = conn.execute("""
        SELECT SUM(c.credits) as total
        FROM courses c
        JOIN registrations r ON c.id = r.course_id
        WHERE r.student_id = ?
    """, (student_id,)).fetchone()
    current_credits = current_credits_row['total'] or 0

    # Build dynamic query for filtering courses
    query = "SELECT * FROM courses WHERE 1=1"
    params = []

    if search_query:
        query += " AND (course_code LIKE ? OR course_name LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    if selected_dept:
        query += " AND department = ?"
        params.append(selected_dept)

    if selected_sem:
        query += " AND semester = ?"
        params.append(int(selected_sem))

    if selected_credits:
        query += " AND credits = ?"
        params.append(int(selected_credits))

    query += " ORDER BY department, semester, course_code"
    courses = conn.execute(query, params).fetchall()

    # Get distinct departments for filter dropdown
    departments = [row['department'] for row in conn.execute("SELECT DISTINCT department FROM courses ORDER BY department").fetchall()]

    conn.close()

    return render_template('courses.html',
                           courses=courses,
                           registered_course_ids=registered_course_ids,
                           current_credits=current_credits,
                           departments=departments,
                           search_query=search_query,
                           selected_dept=selected_dept,
                           selected_sem=selected_sem,
                           selected_credits=selected_credits)


@app.route('/register/<int:course_id>', methods=['POST'])
@student_required
def register_course(course_id):
    """
    Course Registration Logic:
    1. Check if course exists
    2. Check duplicate registration
    3. Check seat availability
    4. Check maximum credit limit (24 credits)
    5. Safely decrement available seats and record registration
    """
    student_id = session['user_id']
    conn = get_db()

    # 1. Fetch course details
    course = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    if not course:
        conn.close()
        flash('Course not found.', 'danger')
        return redirect(url_for('browse_courses'))

    # 2. Check if already registered
    already_registered = conn.execute("""
        SELECT id FROM registrations 
        WHERE student_id = ? AND course_id = ?
    """, (student_id, course_id)).fetchone()

    if already_registered:
        conn.close()
        flash(f"You are already registered for {course['course_code']} - {course['course_name']}.", 'warning')
        return redirect(url_for('browse_courses'))

    # 3. Check seat availability
    if course['available_seats'] <= 0:
        conn.close()
        flash(f"Registration failed: {course['course_code']} is currently full (0 seats available).", 'danger')
        return redirect(url_for('browse_courses'))

    # 4. Check maximum credit limit
    credits_sum_row = conn.execute("""
        SELECT SUM(c.credits) as total 
        FROM courses c
        JOIN registrations r ON c.id = r.course_id
        WHERE r.student_id = ?
    """, (student_id,)).fetchone()
    current_credits = credits_sum_row['total'] or 0

    if current_credits + course['credits'] > MAX_CREDIT_LIMIT:
        conn.close()
        flash(f"Cannot register: Adding this course ({course['credits']} credits) exceeds your semester credit limit of {MAX_CREDIT_LIMIT} credits. You currently have {current_credits} credits.", 'danger')
        return redirect(url_for('browse_courses'))

    # 5. Perform registration inside a transaction
    try:
        conn.execute("""
            INSERT INTO registrations (student_id, course_id)
            VALUES (?, ?)
        """, (student_id, course_id))

        conn.execute("""
            UPDATE courses 
            SET available_seats = available_seats - 1 
            WHERE id = ? AND available_seats > 0
        """, (course_id,))

        conn.commit()
        flash(f"Successfully registered for {course['course_code']} - {course['course_name']} ({course['credits']} credits)!", 'success')
    except sqlite3.Error as e:
        conn.rollback()
        flash(f"Registration failed due to a system error: {str(e)}", 'danger')
    finally:
        conn.close()

    return redirect(url_for('my_courses'))


@app.route('/my-courses')
@student_required
def my_courses():
    """My Courses: Lists all courses the student is currently enrolled in with option to drop."""
    student_id = session['user_id']
    conn = get_db()

    registered_courses = conn.execute("""
        SELECT c.*, r.id as reg_id, r.registration_date 
        FROM courses c
        JOIN registrations r ON c.id = r.course_id
        WHERE r.student_id = ?
        ORDER BY c.course_code
    """, (student_id,)).fetchall()

    total_credits = sum(c['credits'] for c in registered_courses)
    remaining_credits = MAX_CREDIT_LIMIT - total_credits

    conn.close()

    return render_template('my_courses.html',
                           registered_courses=registered_courses,
                           total_credits=total_credits,
                           remaining_credits=remaining_credits)


@app.route('/drop/<int:course_id>', methods=['POST'])
@student_required
def drop_course(course_id):
    """
    Drop Course:
    1. Checks if student is registered
    2. Removes registration
    3. Increases available seats in the course
    """
    student_id = session['user_id']
    conn = get_db()

    course = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    if not course:
        conn.close()
        flash('Course not found.', 'danger')
        return redirect(url_for('my_courses'))

    reg = conn.execute("""
        SELECT * FROM registrations 
        WHERE student_id = ? AND course_id = ?
    """, (student_id, course_id)).fetchone()

    if not reg:
        conn.close()
        flash('You are not registered for this course.', 'warning')
        return redirect(url_for('my_courses'))

    try:
        # Delete registration record
        conn.execute("DELETE FROM registrations WHERE student_id = ? AND course_id = ?", (student_id, course_id))

        # Safely increment available seats (not exceeding max_seats)
        conn.execute("""
            UPDATE courses 
            SET available_seats = MIN(max_seats, available_seats + 1)
            WHERE id = ?
        """, (course_id,))

        conn.commit()
        flash(f"Successfully dropped course: {course['course_code']} - {course['course_name']}.", 'success')
    except sqlite3.Error as e:
        conn.rollback()
        flash(f"Error dropping course: {str(e)}", 'danger')
    finally:
        conn.close()

    return redirect(url_for('my_courses'))


@app.route('/timetable')
@student_required
def timetable():
    """
    Weekly Timetable:
    Displays registered courses organized by weekday (Monday - Friday).
    """
    student_id = session['user_id']
    conn = get_db()

    courses = conn.execute("""
        SELECT c.* 
        FROM courses c
        JOIN registrations r ON c.id = r.course_id
        WHERE r.student_id = ?
        ORDER BY c.schedule
    """, (student_id,)).fetchall()
    conn.close()

    # Organize timetable by day
    # Days mapped to their short name patterns in schedule
    days_map = {
        'Monday': ['Mon', 'Monday'],
        'Tuesday': ['Tue', 'Tuesday'],
        'Wednesday': ['Wed', 'Wednesday'],
        'Thursday': ['Thu', 'Thursday'],
        'Friday': ['Fri', 'Friday']
    }

    weekly_schedule = {day: [] for day in days_map}

    for course in courses:
        schedule_text = course['schedule']
        for day, keywords in days_map.items():
            if any(k in schedule_text for k in keywords):
                # Extract time part if available (after day initials)
                time_slot = schedule_text
                # Simple time extraction for display
                weekly_schedule[day].append({
                    'code': course['course_code'],
                    'name': course['course_name'],
                    'faculty': course['faculty'],
                    'credits': course['credits'],
                    'time': time_slot
                })

    return render_template('timetable.html', weekly_schedule=weekly_schedule, courses_count=len(courses))


@app.route('/profile', methods=['GET', 'POST'])
@student_required
def profile():
    """Student Profile: View personal & academic details, update contact and password."""
    student_id = session['user_id']
    conn = get_db()

    if request.method == 'POST':
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        new_password = request.form.get('password', '').strip()

        if not email:
            flash('Email cannot be empty.', 'danger')
        else:
            # Check if email is already taken by another student
            existing = conn.execute("SELECT id FROM students WHERE email = ? AND id != ?", (email, student_id)).fetchone()
            if existing:
                flash('This email address is already in use by another student.', 'danger')
            else:
                if new_password:
                    conn.execute("""
                        UPDATE students 
                        SET email = ?, phone = ?, password = ? 
                        WHERE id = ?
                    """, (email, phone, new_password, student_id))
                else:
                    conn.execute("""
                        UPDATE students 
                        SET email = ?, phone = ? 
                        WHERE id = ?
                    """, (email, phone, student_id))
                conn.commit()
                flash('Profile updated successfully!', 'success')

    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    
    # Calculate statistics for profile page
    stats = conn.execute("""
        SELECT COUNT(r.id) as course_count, COALESCE(SUM(c.credits), 0) as total_credits
        FROM registrations r
        JOIN courses c ON r.course_id = c.id
        WHERE r.student_id = ?
    """, (student_id,)).fetchone()

    conn.close()

    return render_template('profile.html', student=student, stats=stats)


# ==============================================================================
# ADMIN ROUTES
# ==============================================================================
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin Dashboard: Metrics, popular courses, and latest registrations."""
    conn = get_db()

    total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    total_courses = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    total_registrations = conn.execute("SELECT COUNT(*) FROM registrations").fetchone()[0]
    total_available_seats = conn.execute("SELECT COALESCE(SUM(available_seats), 0) FROM courses").fetchone()[0]

    # Top popular courses by registration count
    popular_courses = conn.execute("""
        SELECT c.course_code, c.course_name, c.department, c.credits, c.max_seats, c.available_seats,
               COUNT(r.id) as reg_count
        FROM courses c
        LEFT JOIN registrations r ON c.id = r.course_id
        GROUP BY c.id
        ORDER BY reg_count DESC, c.course_code ASC
        LIMIT 5
    """).fetchall()

    # Recent registrations
    recent_registrations = conn.execute("""
        SELECT s.student_id, s.name as student_name, c.course_code, c.course_name, r.registration_date
        FROM registrations r
        JOIN students s ON r.student_id = s.id
        JOIN courses c ON r.course_id = c.id
        ORDER BY r.id DESC
        LIMIT 6
    """).fetchall()

    conn.close()

    return render_template('admin_dashboard.html',
                           total_students=total_students,
                           total_courses=total_courses,
                           total_registrations=total_registrations,
                           total_available_seats=total_available_seats,
                           popular_courses=popular_courses,
                           recent_registrations=recent_registrations)


@app.route('/admin/courses')
@admin_required
def manage_courses():
    """Manage Courses: View all courses with edit, delete, and add controls."""
    search = request.args.get('search', '').strip()
    dept = request.args.get('department', '').strip()

    conn = get_db()
    query = """
        SELECT c.*, COUNT(r.id) as reg_count
        FROM courses c
        LEFT JOIN registrations r ON c.id = r.course_id
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND (c.course_code LIKE ? OR c.course_name LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    if dept:
        query += " AND c.department = ?"
        params.append(dept)

    query += " GROUP BY c.id ORDER BY c.department, c.course_code"
    courses = conn.execute(query, params).fetchall()

    departments = [row['department'] for row in conn.execute("SELECT DISTINCT department FROM courses ORDER BY department").fetchall()]
    conn.close()

    return render_template('manage_courses.html',
                           courses=courses,
                           departments=departments,
                           search=search,
                           dept=dept)


@app.route('/admin/courses/add', methods=['GET', 'POST'])
@admin_required
def add_course():
    """Add Course: Create a new academic course with validation."""
    if request.method == 'POST':
        course_code = request.form.get('course_code', '').strip().upper()
        course_name = request.form.get('course_name', '').strip()
        department = request.form.get('department', '').strip()
        semester = request.form.get('semester', '').strip()
        credits = request.form.get('credits', '').strip()
        faculty = request.form.get('faculty', '').strip()
        max_seats = request.form.get('max_seats', '').strip()
        schedule = request.form.get('schedule', '').strip()

        # Validation
        if not all([course_code, course_name, department, semester, credits, faculty, max_seats, schedule]):
            flash('All fields are required.', 'danger')
            return render_template('add_course.html')

        try:
            sem_int = int(semester)
            credits_int = int(credits)
            seats_int = int(max_seats)

            if sem_int <= 0 or credits_int <= 0 or seats_int <= 0:
                flash('Semester, credits, and maximum seats must be positive numbers.', 'danger')
                return render_template('add_course.html')
        except ValueError:
            flash('Please enter valid numeric values for semester, credits, and seats.', 'danger')
            return render_template('add_course.html')

        conn = get_db()
        existing = conn.execute("SELECT id FROM courses WHERE course_code = ?", (course_code,)).fetchone()
        if existing:
            conn.close()
            flash(f"A course with code '{course_code}' already exists.", 'danger')
            return render_template('add_course.html')

        # Insert new course (available_seats initially equals max_seats)
        conn.execute("""
            INSERT INTO courses (course_code, course_name, department, semester, credits, faculty, max_seats, available_seats, schedule)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (course_code, course_name, department, sem_int, credits_int, faculty, seats_int, seats_int, schedule))
        conn.commit()
        conn.close()

        flash(f"Course '{course_code} - {course_name}' added successfully!", 'success')
        return redirect(url_for('manage_courses'))

    return render_template('add_course.html')


@app.route('/admin/courses/edit/<int:course_id>', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    """Edit Course: Update details of an existing course."""
    conn = get_db()
    course = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()

    if not course:
        conn.close()
        flash('Course not found.', 'danger')
        return redirect(url_for('manage_courses'))

    # Calculate current registered count
    registered_count = conn.execute("SELECT COUNT(*) FROM registrations WHERE course_id = ?", (course_id,)).fetchone()[0]

    if request.method == 'POST':
        course_name = request.form.get('course_name', '').strip()
        department = request.form.get('department', '').strip()
        semester = request.form.get('semester', '').strip()
        credits = request.form.get('credits', '').strip()
        faculty = request.form.get('faculty', '').strip()
        max_seats = request.form.get('max_seats', '').strip()
        schedule = request.form.get('schedule', '').strip()

        if not all([course_name, department, semester, credits, faculty, max_seats, schedule]):
            flash('All fields are required.', 'danger')
            return render_template('edit_course.html', course=course, registered_count=registered_count)

        try:
            sem_int = int(semester)
            credits_int = int(credits)
            seats_int = int(max_seats)

            if sem_int <= 0 or credits_int <= 0 or seats_int <= 0:
                flash('Semester, credits, and seats must be positive numbers.', 'danger')
                return render_template('edit_course.html', course=course, registered_count=registered_count)

            if seats_int < registered_count:
                flash(f"Maximum seats cannot be less than currently registered students ({registered_count}).", 'danger')
                return render_template('edit_course.html', course=course, registered_count=registered_count)

        except ValueError:
            flash('Invalid numeric inputs.', 'danger')
            return render_template('edit_course.html', course=course, registered_count=registered_count)

        # Calculate new available seats
        new_available = seats_int - registered_count

        conn.execute("""
            UPDATE courses 
            SET course_name = ?, department = ?, semester = ?, credits = ?, faculty = ?, 
                max_seats = ?, available_seats = ?, schedule = ?
            WHERE id = ?
        """, (course_name, department, sem_int, credits_int, faculty, seats_int, new_available, schedule, course_id))
        conn.commit()
        conn.close()

        flash(f"Course {course['course_code']} updated successfully!", 'success')
        return redirect(url_for('manage_courses'))

    conn.close()
    return render_template('edit_course.html', course=course, registered_count=registered_count)


@app.route('/admin/courses/delete/<int:course_id>', methods=['POST'])
@admin_required
def delete_course(course_id):
    """Delete Course: Removes course and cascades to registered entries."""
    conn = get_db()
    course = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()

    if not course:
        conn.close()
        flash('Course not found.', 'danger')
        return redirect(url_for('manage_courses'))

    conn.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    conn.commit()
    conn.close()

    flash(f"Course {course['course_code']} has been deleted successfully.", 'success')
    return redirect(url_for('manage_courses'))


@app.route('/admin/students')
@admin_required
def view_students():
    """View Students: Lists all enrolled students with registered course and credit count."""
    search = request.args.get('search', '').strip()
    conn = get_db()

    query = """
        SELECT s.*, 
               COUNT(r.id) as registered_count,
               COALESCE(SUM(c.credits), 0) as total_credits
        FROM students s
        LEFT JOIN registrations r ON s.id = r.student_id
        LEFT JOIN courses c ON r.course_id = c.id
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND (s.student_id LIKE ? OR s.name LIKE ? OR s.email LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    query += " GROUP BY s.id ORDER BY s.student_id"
    students = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('students.html', students=students, search=search)


@app.route('/admin/registrations')
@admin_required
def view_registrations():
    """View Registrations: Searchable list of all course registrations."""
    search = request.args.get('search', '').strip()
    conn = get_db()

    query = """
        SELECT r.id as reg_id, r.registration_date,
               s.student_id, s.name as student_name, s.department as student_dept,
               c.course_code, c.course_name, c.credits, c.semester
        FROM registrations r
        JOIN students s ON r.student_id = s.id
        JOIN courses c ON r.course_id = c.id
        WHERE 1=1
    """
    params = []

    if search:
        query += """ AND (s.student_id LIKE ? OR s.name LIKE ? OR c.course_code LIKE ? OR c.course_name LIKE ?)"""
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"])

    query += " ORDER BY r.registration_date DESC, r.id DESC"
    registrations = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('registrations.html', registrations=registrations, search=search)


# ==============================================================================
# ERROR HANDLERS
# ==============================================================================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', content_error="404 - Page Not Found"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('base.html', content_error="500 - Internal Server Error"), 500


# ==============================================================================
# APPLICATION ENTRY POINT
# ==============================================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']

    print("=" * 60)
    print(" CampusEnroll – Student Course Registration System")
    print(f" Running on http://127.0.0.1:{port}")
    print(" Demo Student Login: BWU/BTA/23/576 (or student@example.com) / student123")
    print(" Demo Admin Login:   admin / admin123")
    print("=" * 60)
    app.run(debug=debug, host='0.0.0.0', port=port)
