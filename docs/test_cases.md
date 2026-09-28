# Test Cases Specification
## CampusEnroll – Student Course Registration System

This document outlines the black-box and integration test suite designed for the Software Engineering Lab evaluation. All test cases have been validated using the automated test suite in `test_system.py`.

---

| Test ID | Test Case Title | Pre-Conditions | Test Steps | Test Data / Input | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Valid Student Login | Student account exists in database | 1. Navigate to `/login`<br>2. Enter valid email and password<br>3. Click "Sign In" | Email: `student@example.com`<br>Password: `student123` | Redirected to `/dashboard` with welcome message and enrolled stats. | Successfully redirected to dashboard with student name and credits. | **PASS** |
| **TC-02** | Invalid Student Login | Application is running | 1. Navigate to `/login`<br>2. Enter wrong password<br>3. Submit form | Email: `student@example.com`<br>Password: `wrongpass` | Remains on login page; flashes alert: "Invalid Student ID/Email or password." | Flash alert displayed; access denied. | **PASS** |
| **TC-03** | Valid Admin Login | Admin credentials seeded | 1. Navigate to `/admin/login`<br>2. Enter credentials<br>3. Click "Sign In" | Username: `admin`<br>Password: `admin123` | Redirected to `/admin/dashboard` showing system statistics. | Successfully authenticated and loaded admin dashboard. | **PASS** |
| **TC-04** | Invalid Admin Login | Application is running | 1. Navigate to `/admin/login`<br>2. Enter invalid credentials<br>3. Submit form | Username: `admin`<br>Password: `badpwd` | Remains on page; flashes alert: "Invalid administrator credentials." | Flash alert displayed; access denied. | **PASS** |
| **TC-05** | Course Registration (Seat Available & Under Cap) | Student has 15 credits; course has 35 seats | 1. Navigate to `/courses`<br>2. Click "Register Course" on CS306 (4 credits) | Course ID: 14 (CS306, 4 credits) | Registration record created; available seats decrease by 1 (35 -> 34); student redirected to `/my-courses`. | Registered successfully; seats decremented to 34; credits updated to 19. | **PASS** |
| **TC-06** | Duplicate Course Registration Prevention | Student already registered for CS302 | 1. Attempt to register for CS302 again | Course ID: 2 (CS302) | System blocks registration; flashes warning: "You are already registered for this course." | Registration rejected; no duplicate row created. | **PASS** |
| **TC-07** | Course Registration When Seats Full | Course available seats = 0 | 1. Attempt to register for a course with 0 seats | Course with `available_seats = 0` | System blocks registration; flashes danger message: "Course is currently full (0 seats available)." Button disabled. | Registration prevented; seat count remains 0. | **PASS** |
| **TC-08** | Enforce 24-Credit Semester Limit | Student has 23 registered credits | 1. Student attempts to register for CS301 (4 credits) | Course Credits: 4<br>Current: 23 cr | Calculation (23 + 4 = 27 > 24); blocks registration with message: "Cannot register: Adding this course exceeds your semester credit limit of 24 credits." | Blocked with informative error message; credit limit strictly maintained. | **PASS** |
| **TC-09** | Drop Enrolled Course | Student registered for CS302 (4 credits) | 1. Navigate to `/my-courses`<br>2. Click "Drop Course"<br>3. Confirm in prompt | Course ID: 2 | Course registration deleted; course available seats increment by 1; student credits drop by 4. | Course removed from student's schedule; seats incremented. | **PASS** |
| **TC-10** | Add New Course as Admin | Logged in as Admin | 1. Navigate to `/admin/courses/add`<br>2. Fill in details<br>3. Submit | Code: `AI409`<br>Title: `Robotics & CV`<br>Seats: 35 | Course inserted into database with `available_seats = 35`; redirected to catalog. | Course created and visible in catalog. | **PASS** |
| **TC-11** | Edit Existing Course as Admin | Course exists | 1. Navigate to `/admin/courses/edit/1`<br>2. Change faculty and seats<br>3. Submit | Faculty: `Dr. K. Raman`<br>Max Seats: 50 | Course record updated; available seats recalculated accurately. | Updated fields reflected in course inventory. | **PASS** |
| **TC-12** | Delete Course as Admin | Course exists | 1. Navigate to `/admin/courses`<br>2. Click "Delete"<br>3. Confirm in dialog | Course ID: 17 | Course deleted from `courses` table; cascading delete cleans up any dependent registrations. | Course successfully removed. | **PASS** |
| **TC-13** | Search Courses by Keyword | Logged in as student | 1. Navigate to `/courses`<br>2. Type "Compiler" in search input | Query: `Compiler` | Table filters to display only CS306 (Compiler Design). | Matching course displayed instantly. | **PASS** |
| **TC-14** | Filter Courses by Department & Semester | Logged in as student | 1. Select "Information Technology"<br>2. Select "Semester 5" | Dept: `Information Technology`<br>Sem: `5` | Only Sem 5 IT courses are rendered. | Correct filtered courses listed. | **PASS** |
| **TC-15** | Unauthorized Route Access Guard | User is not logged in (anonymous) | 1. Attempt direct URL access to `/dashboard` or `/admin/dashboard` | Route: `/dashboard` | Redirected to login with flash warning: "Please log in to access this page." | Protected route inaccessible; redirected. | **PASS** |
| **TC-16** | Weekly Timetable Auto-Generation | Student has enrolled courses with schedules | 1. Navigate to `/timetable` | Student with courses | System groups enrolled classes by Monday–Friday columns based on schedule string. | 5-day routine displayed with time slots and instructors. | **PASS** |
| **TC-17** | Update Student Profile | Logged in as student | 1. Navigate to `/profile`<br>2. Enter new phone or email<br>3. Save changes | Phone: `9988776655` | Profile updated in database with success message. | Updated contact phone saved and displayed. | **PASS** |

---

### Verification Summary
- **Total Test Cases**: 17
- **Passed**: 17
- **Failed**: 0
- **Automated Test Script**: `test_system.py` executes in `< 1.0` second.
