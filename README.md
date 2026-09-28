# CampusEnroll – Student Course Registration System
### Academic Software Engineering Lab Showcase Project

![CampusEnroll Banner](https://img.shields.io/badge/Project-CampusEnroll-4f46e5?style=for-the-badge&logo=mortarboard)
![Python Flask](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Database](https://img.shields.io/badge/Database-SQLite3-003B57?style=for-the-badge&logo=sqlite)
![UI](https://img.shields.io/badge/Frontend-HTML5%20%2F%20CSS3%20%2F%20Bootstrap5-7952B3?style=for-the-badge&logo=bootstrap)

---

## 1. Project Title
**CampusEnroll – Student Course Registration System**  
An academic, role-based university portal built with Python Flask, SQLite, Jinja2, Bootstrap 5, and Vanilla JavaScript.

---

## 2. Problem Statement
In traditional university administration, manual course enrollment and uncoordinated registration systems suffer from critical bottlenecks:
- Students frequently register beyond the permissible semester credit ceiling, leading to academic overloads.
- Classroom seating capacities are exceeded due to race conditions or lack of real-time seat decrement.
- Duplicate registrations across identical courses cause administrative overhead.
- Generating a personalized weekly timetable requires cumbersome manual cross-referencing of disjointed timetables.

**CampusEnroll** solves these issues through a centralized, automated web portal with strict business constraints and intuitive self-service interfaces for both students and academic administrators.

---

## 3. Objectives
1. Provide a modern, clean web interface for students to browse, search, and register for courses.
2. Enforce academic integrity rules:
   - **Maximum Credit Limit** (fixed ceiling of 24 credits per semester).
   - **Seat Capacity Protection** (atomic decrement on registration; zero negative seats).
   - **Zero Duplicate Enrollments** (composite relational uniqueness).
3. Generate a personalized **5-day weekly class timetable** (Monday to Friday) from registered course schedules.
4. Provide comprehensive **administrative controls** to manage course catalogs, monitor seat capacities, and audit registrations.
5. Demonstrate core **Software Engineering concepts** (SRS, Use Cases, ER Modeling, Normalization, Layered MVC/MTV, Automated Testing).

---

## 4. Scope
- **Student Scope**: Registration, catalog search and multi-parameter filtering, credit usage monitoring, course dropping with instant seat restoration, weekly timetable generation, and personal contact management.
- **Admin Scope**: Course catalog CRUD (Create, Read, Update, Delete), capacity allocation, student credit tracking, popular course analytics, and historical registration logs audit.
- **Academic Environment**: Built for local demonstration in software engineering labs, project exhibitions, and viva examinations without reliance on paid third-party APIs.

---

## 5. Functional Requirements
- **FR-01**: Student authentication via unique Student ID or registered email and password.
- **FR-02**: Separate administrator authentication portal.
- **FR-03**: Role-based access control (RBAC) via session-checking Python decorators (`@student_required`, `@admin_required`).
- **FR-04**: Interactive student dashboard displaying student info, total enrolled courses, registered credits, remaining credit balance, and a visual progress bar.
- **FR-05**: Dynamic course catalog with real-time keyword search and multi-filtering (Department, Semester, Credits).
- **FR-06**: Atomic course registration with real-time seat decrement (`available_seats - 1`).
- **FR-07**: Strict rejection of duplicate registrations for the same course.
- **FR-08**: Strict rejection of registrations exceeding the 24-credit ceiling.
- **FR-09**: Rejection of registrations when available seats equal zero.
- **FR-10**: Course dropping with confirmation dialog, credit subtraction, and seat restoration (`available_seats + 1`).
- **FR-11**: Dynamic 5-day weekly class schedule (Monday–Friday).
- **FR-12**: Student profile viewer and editor for contact phone, email, and password.
- **FR-13**: Admin dashboard with real-time statistics (total students, total courses, total registrations, remaining seats, and top popular courses).
- **FR-14**: Full course lifecycle management for admins (Add, Edit, Delete with cascade).
- **FR-15**: Searchable student directory and registration audit trail.

---

## 6. Non-Functional Requirements
- **Usability**: Professional university aesthetic with indigo/blue color accents, responsive Bootstrap 5 cards, and clear flash messages for all user actions.
- **Performance**: High-speed local execution (< 50ms average route response time) utilizing local SQLite.
- **Reliability & Data Integrity**: Transactional atomic operations (`commit()` and `rollback()`), foreign keys enabled (`PRAGMA foreign_keys = ON`), and database check constraints.
- **Security**: Parameterized SQL queries preventing SQL Injection (SQLi), Jinja2 auto-escaping preventing XSS, and server-side session management.

---

## 7. User Roles
1. **Student**: Undergraduate or postgraduate student enrolling in courses for the current semester.
2. **Administrator**: University registrar or academic coordinator overseeing curriculum, courses, and capacity.

---

## 8. Technology Stack
| Layer | Technology | Justification |
| :--- | :--- | :--- |
| **Backend Framework** | Python Flask (v3.1+) | Minimalist, lightweight, beginner-friendly, and easy to explain in a viva. |
| **Database** | SQLite 3 | Serverless, zero-configuration relational database with native Python support. |
| **Templating Engine** | Jinja2 | Clean server-side HTML rendering with inheritance and context processors. |
| **Frontend Styling** | CSS3 & Bootstrap 5 (via CDN) | Modern, responsive grid system and aesthetic UI components without heavy build tools. |
| **Client-Side Logic**| Vanilla JavaScript | Lightweight real-time search, confirmation dialogs, and alert auto-dismissal. |
| **Icons** | Bootstrap Icons CDN | Crisp vector iconography for metrics and action buttons. |

---

## 9. System Architecture
CampusEnroll follows the classic **Layered Model-Template-View (MTV / MVC)** architecture:
- **Presentation Layer**: Jinja2 templates (`templates/*.html`), custom stylesheet (`static/css/style.css`), and JavaScript helpers (`static/js/script.js`).
- **Controller / Routing Layer**: Flask application (`app.py`) handling HTTP requests, route authentication decorators, session tokens, and business logic.
- **Persistence Layer**: SQLite database (`database.db`) interacted with via standard parameterized queries and database helper functions.

Detailed architecture diagrams and sequence flows are documented in [`docs/system_architecture.md`](docs/system_architecture.md).

---

## 10. Database Design
The relational schema comprises four primary tables:
1. `students`: Stores student profiles, roll numbers, credentials, departments, and semesters.
2. `admins`: Stores administrative user accounts.
3. `courses`: Stores course codes, titles, departments, credit weights, faculty, max seats, available seats, and schedule strings.
4. `registrations`: Associative table linking students and courses with unique composite constraint `UNIQUE(student_id, course_id)` and cascade deletion.

Full ER diagrams and 3NF normalization proofs are documented in [`docs/database_design.md`](docs/database_design.md).

---

## 11. Modules
- **Authentication Module**: Login, logout, session storage, and unauthorized route interception.
- **Student Dashboard Module**: Profile highlights, credit utilization gauge, and enrolled course summaries.
- **Course Catalog Module**: Multi-attribute filtering, live search, capacity status badges, and registration triggers.
- **Enrollment & Dropping Engine**: Atomic credit verification, duplicate checking, seat decrement/increment transactions.
- **Timetable Module**: Weekday routine parser and grid organizer.
- **Admin Management Module**: Complete course CRUD, capacity monitoring, and system metrics calculation.
- **Audit & Analytics Module**: Popular courses query and chronological enrollment audit log.

---

## 12. Use Cases
11 formal use cases have been specified, covering primary success flows and alternate error flows. See [`docs/use_cases.md`](docs/use_cases.md) for complete specifications.

---

## 13. Installation Steps

### Prerequisites
- Python 3.8 or higher installed on your computer.

### Step 1: Clone or Open the Project Directory
```bash
cd "d:/Student Course Registration System"
```

### Step 2: Install Required Dependencies
```bash
pip install -r requirements.txt
```
*(Dependencies are lightweight: Flask, Werkzeug, Jinja2. SQLite is built into Python.)*

### Step 3: Initialize the Database with Sample Data
```bash
python database/init_db.py
```
This automatically creates `database.db` pre-populated with:
- 1 Administrator account
- 8 Sample Engineering Students across CSE, AI & ML, and IT
- 18 Realistic University Courses
- Initial sample registrations

---

## 14. How to Run

### Run the Flask Application:
```bash
python app.py
```

### Access in your Web Browser:
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 15. Demo Credentials

### Primary Student Account:
- **Student ID:** `BWU/BTA/23/576` *(or Email: `student@example.com`)*
- **Password:** `student123`
- *Student Details:* **Arvind Kumar Yadav** (`B.Tech CSE (AI & ML)`, Semester 5)

### Sample Peer Student Accounts (Password: `student123`):
- `BWU/BTA/23/577` / `suman@example.com` – **Suman Giri** (`B.Tech CSE (AI & ML)`)
- `BWU/BTA/23/578` / `rajkamal@example.com` – **Rajkamal** (`B.Tech Computer Science & Engineering`)
- `BWU/BTA/23/579` / `ranjan@example.com` – **Ranjan** (`B.Tech Information Technology`)
- `BWU/BTA/23/580` / `priya@example.com` – **Priya Patel** (`B.Tech Computer Science & Engineering`)
- `BWU/BTA/23/581` / `sneha@example.com` – **Sneha Reddy** (`B.Tech CSE (AI & ML)`)

### Admin Demo Login:
- **Username:** `admin`
- **Password:** `admin123`
- *Access: Full administrative dashboard, course CRUD, student directory, registration audit*

---

## 16. 3-Tier Architecture & System Design
CampusEnroll strictly implements the decoupled **3-Tier Software Architecture**:
1. **Tier 1 (Presentation Layer)**: HTML5, CSS3 with Light/Dark/System themes, Bootstrap 5, Jinja2 template inheritance, and Vanilla JavaScript.
2. **Tier 2 (Application / Business Logic Layer)**: Python Flask route controllers, session role-based access control (`@student_required`, `@admin_required`), 4-tier validation engine (duplicate rejection, 24-credit ceiling, seat capacity protection, schedule conflict detection).
3. **Tier 3 (Data Layer)**: Normalized SQLite database (`database.db`), foreign keys (`PRAGMA foreign_keys = ON`), check constraints, and atomic multi-table transactions.

*Full architectural diagram & specification:* See [**docs/architecture.md**](docs/architecture.md).

---

## 17. Local Storage Persistence Features
The application utilizes browser `localStorage` for responsive client-side persistence:
- **Theme Preference**: Persists Light, Dark, or System mode across page reloads.
- **Remembered Student ID**: Optional "Remember Student ID" checkbox saves `BWU/BTA/23/576` on login.
- **Course Wishlist / Starred Offerings**: Students can star/bookmark courses directly in the course catalog. Starred courses are persisted in `localStorage` and can be toggled using the *"Saved Offerings"* filter button.

---

## 18. Smart Environment Safeguards
Built-in resilience for effortless deployment and zero-crash execution:
- **Native `.env` Loader**: Safely reads environment variables without crashing if `.env` is absent.
- **Self-Healing Database**: If `database.db` is missing (e.g. when cloned fresh from GitHub), `app.py` automatically initializes the schema and seeds sample data on first launch.
- **HTTP Security Headers**: Injects `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, and `X-XSS-Protection: 1; mode=block`.
- **Environment Template**: Pre-configured [`.env.example`](.env.example) and clean [`.gitignore`](.gitignore).

---

## 19. How to Push to GitHub
When you are ready to publish the project to your GitHub account:

```bash
# 1. Initialize Git repository (if not already done)
git init

# 2. Stage all files (respects .gitignore)
git add .

# 3. Create your initial commit
git commit -m "feat: CampusEnroll 3-tier student course registration system"

# 4. Rename main branch
git branch -M main

# 5. Connect to your GitHub repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/Student-Course-Registration-System.git

# 6. Push code to GitHub
git push -u origin main
```

---

## 20. Software Engineering Documentation Index
All software engineering lab artifacts are available in the `docs/` folder:
- **[3-Tier Architecture Specification](docs/architecture.md)**
- **[Requirements Specification (SRS)](docs/requirements.md)**
- **[Use Case Specifications](docs/use_cases.md)**
- **[Database Design & ER Diagram](docs/database_design.md)**
- **[System Architecture](docs/system_architecture.md)**
- **[Test Cases & Verification Matrix](docs/test_cases.md)** (16 automated unit test cases)
- **[Cloud & Docker Deployment Guide](docs/deployment.md)**

