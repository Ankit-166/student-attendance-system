from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_flash_messages'
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        db.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_no TEXT UNIQUE NOT NULL,
                attendance_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                course TEXT,
                semester INTEGER
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                date DATE NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
                UNIQUE(student_id, date)
            )
        ''')
        db.commit()
        db.close()

init_db()

@app.route('/')
def dashboard():
    conn = get_db_connection()
    total_students = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    total_records = conn.execute('SELECT COUNT(*) FROM attendance').fetchone()[0]
    conn.close()
    return render_template('dashboard.html', total_students=total_students, total_records=total_records)

@app.route('/students')
def students():
    search = request.args.get('search', '')
    conn = get_db_connection()
    if search:
        query = "SELECT * FROM students WHERE name LIKE ? OR roll_no LIKE ? OR attendance_id LIKE ? ORDER BY roll_no"
        students = conn.execute(query, ('%' + search + '%', '%' + search + '%', '%' + search + '%')).fetchall()
    else:
        students = conn.execute("SELECT * FROM students ORDER BY roll_no").fetchall()
    conn.close()
    return render_template('students.html', students=students, search=search)

@app.route('/students/add', methods=('GET', 'POST'))
def add_student():
    if request.method == 'POST':
        roll_no = request.form.get('roll_no', '').strip()
        attendance_id = request.form.get('attendance_id', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()
        semester = request.form.get('semester', '').strip()

        if not roll_no or not name or not attendance_id:
            flash('Roll Number, Attendance ID, and Name are required!', 'danger')
        else:
            conn = get_db_connection()
            try:
                conn.execute(
                    'INSERT INTO students (roll_no, attendance_id, name, email, course, semester) VALUES (?, ?, ?, ?, ?, ?)',
                    (roll_no, attendance_id, name, email, course, semester)
                )
                conn.commit()
                flash('Student added successfully!', 'success')
                conn.close()
                return redirect(url_for('students'))
            except sqlite3.IntegrityError as e:
                if 'attendance_id' in str(e):
                    flash(f'Student with Attendance ID {attendance_id} already exists!', 'danger')
                else:
                    flash(f'Student with Roll Number {roll_no} already exists!', 'danger')
            finally:
                conn.close()
    return render_template('add_student.html')

@app.route('/students/edit/<int:id>', methods=('GET', 'POST'))
def edit_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    if student is None:
        conn.close()
        flash('Student not found!', 'danger')
        return redirect(url_for('students'))

    if request.method == 'POST':
        roll_no = request.form.get('roll_no', '').strip()
        attendance_id = request.form.get('attendance_id', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()
        semester = request.form.get('semester', '').strip()

        if not roll_no or not name or not attendance_id:
            flash('Roll Number, Attendance ID, and Name are required!', 'danger')
        else:
            try:
                conn.execute(
                    'UPDATE students SET roll_no = ?, attendance_id = ?, name = ?, email = ?, course = ?, semester = ? WHERE id = ?',
                    (roll_no, attendance_id, name, email, course, semester, id)
                )
                conn.commit()
                flash('Student updated successfully!', 'success')
                conn.close()
                return redirect(url_for('students'))
            except sqlite3.IntegrityError as e:
                if 'attendance_id' in str(e):
                    flash(f'Student with Attendance ID {attendance_id} already exists!', 'danger')
                else:
                    flash(f'Student with Roll Number {roll_no} already exists!', 'danger')
    conn.close()
    return render_template('edit_student.html', student=student)

@app.route('/students/delete/<int:id>', methods=('POST',))
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students'))

@app.route('/attendance/mark', methods=('GET', 'POST'))
def mark_attendance():
    date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    conn = get_db_connection()
    
    if request.method == 'POST':
        form_date = request.form.get('date')
        if not form_date:
            flash('Date is required!', 'danger')
        else:
            date = form_date
            students = conn.execute("SELECT id FROM students").fetchall()
            try:
                for student in students:
                    status = request.form.get(f'status_{student["id"]}')
                    if status:
                        conn.execute('''
                            INSERT INTO attendance (student_id, date, status) 
                            VALUES (?, ?, ?)
                            ON CONFLICT(student_id, date) 
                            DO UPDATE SET status=excluded.status
                        ''', (student['id'], date, status))
                conn.commit()
                flash('Bulk Attendance saved successfully!', 'success')
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('mark_attendance', date=date))

    query = '''
        SELECT s.*, a.status 
        FROM students s 
        LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ? 
        ORDER BY s.roll_no
    '''
    students = conn.execute(query, (date,)).fetchall()
    conn.close()
    return render_template('mark_attendance.html', students=students, date=date)

@app.route('/attendance/quick_mark', methods=('POST',))
def quick_mark_attendance():
    date = request.form.get('date')
    identifiers_raw = request.form.get('identifier', '').strip()
    
    if not date:
        flash('Date is required!', 'danger')
        return redirect(url_for('mark_attendance'))
        
    conn = get_db_connection()
    all_students = conn.execute('SELECT id, attendance_id, roll_no, name FROM students').fetchall()
    
    if not identifiers_raw:
        identifiers = []
    else:
        identifiers = [i.strip() for i in identifiers_raw.split(',') if i.strip()]
        
    present_ids = set()
    invalid_identifiers = set()
    
    for identifier in identifiers:
        found = False
        for s in all_students:
            if s['attendance_id'] == identifier or s['roll_no'] == identifier:
                present_ids.add(s['id'])
                found = True
                break
        if not found:
            invalid_identifiers.add(identifier)
            
    for invalid in invalid_identifiers:
        flash(f'⚠ {invalid} - Student not found', 'danger')
        
    present_count = 0
    absent_count = 0
    
    for s in all_students:
        status = 'Present' if s['id'] in present_ids else 'Absent'
        if status == 'Present':
            present_count += 1
        else:
            absent_count += 1
            
        conn.execute('''
            INSERT INTO attendance (student_id, date, status) 
            VALUES (?, ?, ?)
            ON CONFLICT(student_id, date) 
            DO UPDATE SET status=excluded.status
        ''', (s['id'], date, status))
        
    conn.commit()
    conn.close()
    
    flash(f'Attendance Saved Successfully! Present: {present_count} | Absent: {absent_count}', 'success')
    return redirect(url_for('mark_attendance', date=date))

@app.route('/attendance/view')
def view_attendance():
    date = request.args.get('date', '')
    search = request.args.get('search', '').strip()
    records = []
    
    if date:
        conn = get_db_connection()
        if search:
            query = '''
                SELECT s.roll_no, s.attendance_id, s.name, a.status 
                FROM attendance a 
                JOIN students s ON a.student_id = s.id 
                WHERE a.date = ? AND (s.name LIKE ? OR s.roll_no LIKE ? OR s.attendance_id LIKE ?)
                ORDER BY s.roll_no
            '''
            records = conn.execute(query, (date, f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
        else:
            query = '''
                SELECT s.roll_no, s.attendance_id, s.name, a.status 
                FROM attendance a 
                JOIN students s ON a.student_id = s.id 
                WHERE a.date = ? 
                ORDER BY s.roll_no
            '''
            records = conn.execute(query, (date,)).fetchall()
        conn.close()
    return render_template('view_attendance.html', records=records, date=date, search=search)

@app.route('/attendance/report')
def report():
    search = request.args.get('search', '').strip()
    conn = get_db_connection()
    
    query_base = '''
        SELECT s.roll_no, s.attendance_id, s.name, 
               COUNT(a.id) as total_days,
               SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_days,
               SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent_days
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
    '''
    
    if search:
        query = query_base + '''
            WHERE s.name LIKE ? OR s.roll_no LIKE ? OR s.attendance_id LIKE ?
            GROUP BY s.id
            ORDER BY s.roll_no
        '''
        report_data = conn.execute(query, (f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
    else:
        query = query_base + '''
            GROUP BY s.id
            ORDER BY s.roll_no
        '''
        report_data = conn.execute(query).fetchall()
        
    conn.close()
    return render_template('report.html', report=report_data, search=search)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
