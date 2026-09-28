# Software Requirements Specification (SRS)
## CampusEnroll – Student Course Registration System

### 1. Introduction
#### 1.1 Purpose
The purpose of this document is to specify the complete functional and non-functional requirements for **CampusEnroll**, an academic web application designed for university course registrations. It serves as an educational showcase of core Software Engineering principles including requirement analysis, database normalization, relational integrity, business rules enforcement, and role-based access control.

#### 1.2 Intended Audience
- Lab Evaluators & Viva Examiners
- Undergraduate Students & Instructors (B.Tech CS / AI & ML)
- Academic Coordinators & System Administrators

#### 1.3 Project Scope
The system provides a self-service portal for enrolled undergraduate/graduate students to browse catalog offerings, register for semester courses, enforce academic credit caps (max 24 credits), review weekly timetables, and drop courses. In addition, an administrative module allows academic registrars to manage course inventory, allocate seat capacities, inspect student enrollment loads, and audit registration logs.

---

### 2. User Classes and Characteristics
1. **Student**:
   - Authorized undergraduate/postgraduate student.
   - Enrolled in a specific academic department (e.g., Computer Science, AI & ML, IT) and semester.
   - Allowed to register, view schedule, and drop courses within credit and seat limits.
2. **Administrator / Academic Registrar**:
   - Institutional authority overseeing curriculum and catalog entries.
   - Privileges to create, update, delete courses, adjust capacities, and monitor student enrollments.

---

### 3. Functional Requirements

#### 3.1 Authentication & Session Management
- **FR-01 (Student Login)**: The system shall authenticate students using their unique Student ID or Registered Email and password.
- **FR-02 (Admin Login)**: The system shall provide an isolated administrator login route using username and password credentials.
- **FR-03 (Session Enforcement)**: The system shall protect student-only and admin-only routes using server-side Flask sessions and reject unauthorized requests with friendly redirect messages.
- **FR-04 (Logout)**: The system shall clear session tokens upon logout and return users to the login screen.

#### 3.2 Student Module
- **FR-05 (Dashboard Overview)**: The system shall display the student's name, ID, department, semester, total registered courses count, total credits, remaining credit balance, and recently registered courses.
- **FR-06 (Credit Limit Bar)**: The system shall visually display a progress bar reflecting current credit utilization against the maximum 24 credits cap.
- **FR-07 (Course Catalog Browsing)**: The system shall display available courses with code, course name, department, semester, credits, instructor name, remaining seats, and schedule.
- **FR-08 (Course Search & Multi-Filter)**: The system shall allow searching by course code/name, and filtering by department, semester, and credits.
- **FR-09 (Single Course Registration)**: The system shall register a student into an eligible course when clicked.
- **FR-10 (Duplicate Registration Prevention)**: The system shall reject registration if the student is already registered for that course.
- **FR-11 (Seat Availability Validation)**: The system shall reject registration if the course has zero remaining seats (`available_seats <= 0`).
- **FR-12 (Credit Limit Validation)**: The system shall reject registration if the course credit weight would cause total registered credits to exceed 24.
- **FR-13 (Atomic Seat Decrement)**: The system shall atomically decrease `available_seats` by 1 upon successful registration.
- **FR-14 (My Courses List)**: The system shall display all courses currently registered by the logged-in student.
- **FR-15 (Drop Course)**: The system shall allow students to drop a registered course after confirmation, decrementing registered credit load and incrementing available course seats by 1.
- **FR-16 (Weekly Timetable)**: The system shall automatically aggregate schedules of registered courses into a Monday-to-Friday schedule grid.
- **FR-17 (Student Profile & Update)**: The system shall permit students to view their academic records and update their contact telephone number, email, or password.

#### 3.3 Administrator Module
- **FR-18 (Admin Metrics)**: The admin dashboard shall display real-time counts for total students, total courses, total registrations, and remaining seat capacity.
- **FR-19 (Popular Course Analytics)**: The system shall compute and display top courses ranked by enrollment counts.
- **FR-20 (Add Course)**: The administrator shall be able to publish a new course by providing course code, name, department, semester, credits, faculty, maximum seats, and schedule.
- **FR-21 (Edit Course)**: The administrator shall be able to edit course title, department, semester, credits, faculty, capacity, and schedule.
- **FR-22 (Delete Course)**: The administrator shall be able to delete a course with foreign-key cascade removal of related registrations after confirmation.
- **FR-23 (Student Directory)**: The administrator shall be able to inspect all enrolled students, their registered course counts, and credit totals with search capability.
- **FR-24 (Registration Audit Logs)**: The administrator shall be able to view and search all historical course registrations.

---

### 4. Non-Functional Requirements

#### 4.1 Usability
- Modern, clean, and distraction-free user interface utilizing Bootstrap 5 and customized modern typography.
- Mobile-responsive layout compatible with smartphones, tablets, and desktop displays.
- Descriptive flash notifications for all user actions (success, warning, danger).

#### 4.2 Performance
- Page load latency under 200 milliseconds in local deployment.
- Database query execution with indexed primary keys and unique constraints in SQLite.

#### 4.3 Reliability & Data Integrity
- Enforced Foreign Key constraints (`PRAGMA foreign_keys = ON`).
- Atomic transactions ensuring seat count changes and registration inserts/deletions commit together.
- Database CHECK constraints preventing negative available seats or negative credits.

#### 4.4 Security
- Parameterized SQL queries to eliminate SQL Injection (SQLi) vulnerabilities.
- Flask server-side session cookies with secure signing key.
- Separation of Student and Admin privileges via Python function decorators.

---

### 5. Constraints & Assumptions
- Standard semester credit cap is fixed at 24 credits per student.
- Course schedule strings follow consistent weekday abbreviation patterns (`Mon`, `Tue`, `Wed`, `Thu`, `Fri`).
- Single-instance local SQLite database without requiring external cloud database services.
