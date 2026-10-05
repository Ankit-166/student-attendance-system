import sqlite3
import requests
import sys

BASE_URL = "http://localhost:5000"
DB_PATH = "database.db"

def reset_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM attendance")
    conn.execute("DELETE FROM students")
    conn.commit()
    conn.close()

def run_tests():
    reset_db()
    session = requests.Session()
    
    print("1,2. Adding students with Attendance ID...")
    res = session.post(f"{BASE_URL}/students/add", data={
        "roll_no": "2505112120001",
        "attendance_id": "001",
        "name": "Ankit Kumar Sahu",
        "email": "ankit@test.com",
        "course": "CS",
        "semester": "1"
    })
    res = session.post(f"{BASE_URL}/students/add", data={
        "roll_no": "2505112120002",
        "attendance_id": "002",
        "name": "Rahul Verma",
        "email": "rahul@test.com",
        "course": "CS",
        "semester": "1"
    })
    
    print("3,4,5. Searching on Students Page...")
    res = session.get(f"{BASE_URL}/students?search=ankit")
    assert b"2505112120001" in res.content
    res = session.get(f"{BASE_URL}/students?search=2505112120002")
    assert b"Rahul Verma" in res.content
    res = session.get(f"{BASE_URL}/students?search=001")
    assert b"Ankit Kumar Sahu" in res.content
    
    print("6. Duplicate Attendance ID...")
    res = session.post(f"{BASE_URL}/students/add", data={
        "roll_no": "2505112120003",
        "attendance_id": "001",
        "name": "Duplicate Student",
        "email": "",
        "course": "",
        "semester": "1"
    })
    assert b"already exists" in res.content
    
    print("7,8. Edit & Delete Student...")
    session.post(f"{BASE_URL}/students/add", data={"roll_no": "TEMP", "attendance_id": "999", "name": "Temp"})
    conn = sqlite3.connect(DB_PATH)
    temp_id = conn.execute("SELECT id FROM students WHERE attendance_id='999'").fetchone()[0]
    session.post(f"{BASE_URL}/students/edit/{temp_id}", data={"roll_no": "TEMP2", "attendance_id": "998", "name": "Temp Edit"})
    assert conn.execute("SELECT name FROM students WHERE id=?", (temp_id,)).fetchone()[0] == "Temp Edit"
    session.post(f"{BASE_URL}/students/delete/{temp_id}")
    assert conn.execute("SELECT COUNT(*) FROM students WHERE attendance_id='998'").fetchone()[0] == 0
    
    print("9,10,11,12,13. Quick Mark Present (Classroom Mode)...")
    # Mark Ankit and Rahul Present via comma separated string
    # Add a third student to test the 'Absent' fallback
    session.post(f"{BASE_URL}/students/add", data={"roll_no": "2505112120004", "attendance_id": "004", "name": "Priya", "email": "", "course": "", "semester": "1"})
    
    res = session.post(f"{BASE_URL}/attendance/quick_mark", data={"date": "2023-10-01", "identifier": "001, 2505112120002, 999"})
    assert b"Student not found" in res.content # 999 is invalid
    
    # Check that Priya (004) is Absent, Ankit & Rahul are Present
    priya_id = conn.execute("SELECT id FROM students WHERE attendance_id='004'").fetchone()[0]
    priya_status = conn.execute("SELECT status FROM attendance WHERE student_id=? AND date='2023-10-01'", (priya_id,)).fetchone()[0]
    assert priya_status == "Absent", f"Priya should be Absent, got {priya_status}"
    
    ankit_id = conn.execute("SELECT id FROM students WHERE attendance_id='001'").fetchone()[0]
    ankit_status = conn.execute("SELECT status FROM attendance WHERE student_id=? AND date='2023-10-01'", (ankit_id,)).fetchone()[0]
    assert ankit_status == "Present", "Ankit should be Present"
    
    # Empty input marks all absent
    res = session.post(f"{BASE_URL}/attendance/quick_mark", data={"date": "2023-10-02", "identifier": ""})
    status_count = conn.execute("SELECT COUNT(*) FROM attendance WHERE date='2023-10-02' AND status='Absent'").fetchone()[0]
    assert status_count == 3, f"Expected 3 Absent records, got {status_count}"
    
    print("14,15. Invalid ID/Roll Number...")
    res = session.post(f"{BASE_URL}/attendance/quick_mark", data={"date": "2023-10-01", "identifier": "INVALID123"})
    assert b"not found" in res.content
    
    print("16-22. View Attendance & Search...")
    res = session.get(f"{BASE_URL}/attendance/view?date=2023-10-01&search=ankit")
    assert b"Ankit Kumar Sahu" in res.content and b"Rahul Verma" not in res.content
    res = session.get(f"{BASE_URL}/attendance/view?date=2023-10-01&search=002")
    assert b"Rahul Verma" in res.content and b"Ankit Kumar" not in res.content
    
    print("23-28. Reports & Database Safety...")
    res = session.get(f"{BASE_URL}/attendance/report?search=ankit")
    assert b"50.0%" in res.content
    count = conn.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND date='2023-10-01'", (ankit_id,)).fetchone()[0]
    assert count == 1, "Duplicate attendance record created!"
    
    # Delete cascade
    session.post(f"{BASE_URL}/students/delete/{ankit_id}")
    count = conn.execute("SELECT COUNT(*) FROM attendance WHERE student_id=?", (ankit_id,)).fetchone()[0]
    assert count == 0, "Cascade delete failed!"
    
    print("ALL TESTS PASSED SUCCESSFULLY.")

if __name__ == '__main__':
    run_tests()
