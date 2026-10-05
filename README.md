# Student Attendance Management System

A simple web-based Student Attendance Management System developed using Python, Flask, HTML, CSS/Bootstrap, and SQLite.

The system allows users to manage student records, mark daily attendance, view attendance records, and generate attendance reports.

## Features

- Add new students
- Edit student details
- Delete students
- Search students by name or roll number
- Mark daily attendance
- Quick attendance marking using Attendance ID
- Automatically mark remaining students as Absent
- View attendance records
- Search attendance records
- Generate attendance reports
- Calculate attendance percentage
- Flash messages for successful and failed operations
- SQLite database for storing student and attendance data
- Responsive web interface using Bootstrap

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- Jinja2
- JavaScript

## Project Structure

student_attendance/
│
├── app.py
├── requirements.txt
├── README.md
├── test_app.py
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── students.html
    ├── add_student.html
    ├── edit_student.html
    ├── mark_attendance.html
    ├── view_attendance.html
    └── report.html

## Main Modules

### 1. Dashboard

Provides an overview of the attendance management system and quick access to major features.

### 2. Student Management

Allows users to:

- Add students
- Edit student information
- Delete students
- Search students
- View registered students

### 3. Attendance Management

Allows users to:

- Select an attendance date
- Search students
- Mark students as Present
- Automatically mark remaining students as Absent
- Prevent duplicate attendance records for the same student and date

### 4. Attendance Records

Displays attendance records for students with options to search and review attendance history.

### 5. Attendance Reports

Generates student-wise attendance information including:

- Total Attendance Days
- Present Days
- Absent Days
- Attendance Percentage

Attendance percentage is calculated using:

Attendance Percentage = (Present Days / Total Attendance Days) × 100

## Database

The application uses SQLite as its database.

The database contains two main tables:

### Students

Stores:

- Student ID
- Roll Number
- Name
- Email
- Course
- Semester

### Attendance

Stores:

- Attendance ID
- Student ID
- Attendance Date
- Attendance Status

Each student can have only one attendance record for a particular date.

## Installation

### 1. Clone the repository

git clone https://github.com/YOUR_USERNAME/student-attendance-system.git

### 2. Open the project directory

cd student-attendance-system

### 3. Create a virtual environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

### 4. Install dependencies

pip install -r requirements.txt

### 5. Run the application

python app.py

Open the local Flask URL shown in the terminal, typically:

http://127.0.0.1:5000/

## Usage Workflow

Start Application
        ↓
    Dashboard
        ↓
 ┌──────┼───────────────┐
 ↓      ↓               ↓
Manage  Mark          View
Students Attendance   Attendance
          ↓
    Select Date
          ↓
 Mark Present Students
          ↓
Remaining Students
      → Absent
          ↓
 Attendance Report
          ↓
Attendance Percentage

## Testing

The project includes a basic test file.

Run:

python test_app.py

## Important Note

The SQLite database file (database.db) is intentionally excluded from Git using .gitignore.

The database is generated and maintained locally by the application.

## Future Enhancements

- User authentication and login
- Admin and teacher roles
- Export attendance reports to Excel/PDF
- Monthly and semester-wise reports
- Attendance charts and visual analytics
- Email notifications for low attendance
- Student login portal
- Cloud database integration

## Project Purpose

The project demonstrates the development of a basic web-based attendance management system using Flask and SQLite. It focuses on CRUD operations, database management, attendance processing, search functionality, and report generation.

## Author

Ankit Sahu# Student Attendance Management System

A simple web-based Student Attendance Management System developed using Python, Flask, HTML, CSS/Bootstrap, and SQLite.

The system allows users to manage student records, mark daily attendance, view attendance records, and generate attendance reports.

## Features

- Add new students
- Edit student details
- Delete students
- Search students by name or roll number
- Mark daily attendance
- Quick attendance marking using Attendance ID
- Automatically mark remaining students as Absent
- View attendance records
- Search attendance records
- Generate attendance reports
- Calculate attendance percentage
- Flash messages for successful and failed operations
- SQLite database for storing student and attendance data
- Responsive web interface using Bootstrap

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- Jinja2
- JavaScript

## Project Structure

student_attendance/
│
├── app.py
├── requirements.txt
├── README.md
├── test_app.py
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── students.html
    ├── add_student.html
    ├── edit_student.html
    ├── mark_attendance.html
    ├── view_attendance.html
    └── report.html

## Main Modules

### 1. Dashboard

Provides an overview of the attendance management system and quick access to major features.

### 2. Student Management

Allows users to:

- Add students
- Edit student information
- Delete students
- Search students
- View registered students

### 3. Attendance Management

Allows users to:

- Select an attendance date
- Search students
- Mark students as Present
- Automatically mark remaining students as Absent
- Prevent duplicate attendance records for the same student and date

### 4. Attendance Records

Displays attendance records for students with options to search and review attendance history.

### 5. Attendance Reports

Generates student-wise attendance information including:

- Total Attendance Days
- Present Days
- Absent Days
- Attendance Percentage

Attendance percentage is calculated using:

Attendance Percentage = (Present Days / Total Attendance Days) × 100

## Database

The application uses SQLite as its database.

The database contains two main tables:

### Students

Stores:

- Student ID
- Roll Number
- Name
- Email
- Course
- Semester

### Attendance

Stores:

- Attendance ID
- Student ID
- Attendance Date
- Attendance Status

Each student can have only one attendance record for a particular date.

## Installation

### 1. Clone the repository

git clone https://github.com/YOUR_USERNAME/student-attendance-system.git

### 2. Open the project directory

cd student-attendance-system

### 3. Create a virtual environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

### 4. Install dependencies

pip install -r requirements.txt

### 5. Run the application

python app.py

Open the local Flask URL shown in the terminal, typically:

http://127.0.0.1:5000/

## Usage Workflow

Start Application
        ↓
    Dashboard
        ↓
 ┌──────┼───────────────┐
 ↓      ↓               ↓
Manage  Mark          View
Students Attendance   Attendance
          ↓
    Select Date
          ↓
 Mark Present Students
          ↓
Remaining Students
      → Absent
          ↓
 Attendance Report
          ↓
Attendance Percentage

## Testing

The project includes a basic test file.

Run:

python test_app.py

## Important Note

The SQLite database file (database.db) is intentionally excluded from Git using .gitignore.

The database is generated and maintained locally by the application.

## Future Enhancements

- User authentication and login
- Admin and teacher roles
- Export attendance reports to Excel/PDF
- Monthly and semester-wise reports
- Attendance charts and visual analytics
- Email notifications for low attendance
- Student login portal
- Cloud database integration

## Project Purpose

The project demonstrates the development of a basic web-based attendance management system using Flask and SQLite. It focuses on CRUD operations, database management, attendance processing, search functionality, and report generation.

