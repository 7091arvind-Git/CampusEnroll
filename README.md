# CampusEnroll – Student Course Registration System

[![Live Demo](https://img.shields.io/badge/Live%20Demo-campusenroll.onrender.com-success?style=for-the-badge&logo=render)](https://campusenroll.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> A modern, responsive, 3-tier university course registration portal designed for academic software engineering labs and viva presentations.

---

## 🌐 Live Demo & Repository

* **Live Website:** [https://campusenroll.onrender.com](https://campusenroll.onrender.com)
* **GitHub Repository:** [https://github.com/7091arvind-Git/CampusEnroll](https://github.com/7091arvind-Git/CampusEnroll)

*(Note: On Render's free tier, if the site hasn't been visited recently, it may take 30–40 seconds to wake up on the first load.)*

---

## 🔑 Demo Login Credentials

### 1. Student Portal
* **Student ID / Roll:** `BWU/BTA/23/576` *(or email: `student@example.com`)*
* **Password:** `student123`
* **Student Name:** Arvind Kumar Yadav
* **Department:** B.Tech CSE (AI & ML) — Semester 5

### 2. Admin Portal
* **Username:** `admin`
* **Password:** `admin123`
* **Access:** Course management (Add/Edit/Delete), student directory, seat capacities, and registration logs.

---

## ✨ Key Features

### 🎓 For Students
* **Course Catalog:** Browse university courses with real-time keyword search and filters (Department, Semester, Credits).
* **Smart Validations:** 
  * Prevents duplicate course enrollment.
  * Enforces maximum credit limit (24 credits per semester).
  * Blocks registration when seats are full.
* **One-Click Drop:** Drop courses with instant credit adjustment and automatic seat restoration.
* **Weekly Timetable:** Generates a personalized 5-day class routine (Monday–Friday).
* **Course Wishlist / Saved Courses:** Star your favorite courses to save them in your browser via `localStorage`.

### 🛡️ For Administrators
* **Course Management (CRUD):** Add new offerings, modify seat capacities, and remove obsolete courses.
* **Student Directory:** View student credit loads and contact info.
* **Audit Trail:** Track enrollment history with timestamps.

### 🎨 User Experience & Themes
* **Theme Switcher:** Seamless toggle between **Light Mode**, **Dark Mode**, and **System Default**.
* **Zero-Flicker:** Instant theme detection in `<head>` so dark mode never flashes white on reload.
* **Local Storage Persistence:** Remembers your theme, saved courses, and student ID.
* **Mobile-First Design:** Fully responsive layout for smartphones, tablets, laptops, and desktop screens.

---

## 🏗️ 3-Tier Architecture

CampusEnroll is built on the classic **3-Tier Software Architecture**:

```
+-------------------------------------------------------------+
|                  1. PRESENTATION TIER                       |
|   HTML5, Vanilla CSS3, Bootstrap 5, Jinja2, Vanilla JS      |
|   (Responsive UI, Dark/Light Themes, LocalStorage State)    |
+-------------------------------------------------------------+
                              |
                              v  HTTP Requests (GET / POST)
+-------------------------------------------------------------+
|                2. APPLICATION / LOGIC TIER                  |
|                      Python Flask (app.py)                  |
|   - Authentication & Role-Based Access Control (RBAC)       |
|   - Credit Limit & Duplicate Enrollment Checks              |
|   - Real-time Seat Allocation & Schedule Conflict Check     |
|   - Smart Environment Safeguards & Security Headers         |
+-------------------------------------------------------------+
                              |
                              v  Parameterized SQL & Transactions
+-------------------------------------------------------------+
|                      3. DATA TIER                           |
|                 SQLite Database (database.db)               |
|   - Normalized Relational Tables (students, courses, etc.)  |
|   - Foreign Keys (PRAGMA foreign_keys = ON) & Constraints   |
|   - ACID Transactions with commit & rollback safety         |
+-------------------------------------------------------------+
```

---

## 💻 Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Bootstrap Icons |
| **Backend** | Python 3.11+, Flask |
| **Database** | SQLite3 (Zero setup required, self-healing) |
| **WSGI Server** | Gunicorn (Linux/Production), Waitress (Windows) |
| **Deployment** | Render ([render.yaml](render.yaml), Docker ready) |

---

## 🚀 How to Run Locally

### Step 1: Clone the repository
```bash
git clone https://github.com/7091arvind-Git/CampusEnroll.git
cd CampusEnroll
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the application
```bash
python app.py
```
Open your browser and visit: **`http://127.0.0.1:5000`**

*(Note: The database automatically initializes itself with sample data on first run! No manual SQL commands required.)*

---

## 🧪 Automated Testing

CampusEnroll includes an automated test suite verifying all routes, constraints, and authentication rules:

```bash
python test_system.py
```
*Result: 16 out of 16 tests passing.*

---

## 📁 Project Structure

```text
Student Course Registration System/
├── app.py                  # Main Flask application & business logic
├── wsgi.py                 # WSGI production server entry point
├── requirements.txt        # Python package dependencies
├── render.yaml             # Render cloud deployment blueprint
├── Procfile                # Production process declaration
├── database.db             # SQLite relational database
├── database/
│   ├── schema.sql          # Relational SQL table definitions
│   └── init_db.py          # Database seeding script
├── static/
│   ├── css/style.css       # Custom design system & dark mode tokens
│   └── js/script.js        # Theme switcher & local storage helpers
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Master layout with responsive navbar
│   ├── index.html          # Public landing page
│   ├── login.html          # Student login portal
│   ├── dashboard.html      # Student dashboard & credit metrics
│   ├── courses.html        # Course catalog with wishlist
│   ├── my_courses.html     # Enrolled courses & drop manager
│   ├── timetable.html      # Weekly class routine
│   └── profile.html        # Student account profile
├── docs/                   # Software Engineering Lab documentation
│   ├── architecture.md     # 3-Tier Architecture specification
│   ├── requirements.md     # Software Requirements Specification (SRS)
│   ├── use_cases.md        # Use case descriptions
│   ├── database_design.md  # Database schema & ER details
│   ├── test_cases.md       # Test verification matrix
│   └── deployment.md       # Cloud deployment instructions
└── test_system.py          # Automated unit test suite
```

---

## 👨‍💻 Project Developer

* **Name:** Arvind Kumar Yadav
* **Degree:** B.Tech in Computer Science & Engineering (AI & ML)
* **Student ID:** `BWU/BTA/23/576`
* **Semester:** 5th Semester
* **Institution:** Brainware University
