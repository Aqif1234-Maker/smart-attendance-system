from config import get_connection

def add_student(name, roll_number, class_name, section, contact):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO students (name, roll_number, class, section, contact) VALUES (%s, %s, %s, %s, %s)",
                (name, roll_number, class_name, section, contact)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding student: {e}")
            return False
        finally:
            conn.close()

def get_all_students():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
        conn.close()
        return result
    return []

def get_students_by_class(class_name, section):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE class=%s AND section=%s",
            (class_name, section)
        )
        result = cursor.fetchall()
        conn.close()
        return result
    return []

def update_student(student_id, name, roll_number, class_name, section, contact):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE students SET name=%s, roll_number=%s, class=%s, section=%s, contact=%s WHERE id=%s",
                (name, roll_number, class_name, section, contact, student_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating student: {e}")
            return False
        finally:
            conn.close()

def delete_student(student_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False
        finally:
            conn.close()

def search_students(keyword):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE name LIKE %s OR roll_number LIKE %s",
            (f"%{keyword}%", f"%{keyword}%")
        )
        result = cursor.fetchall()
        conn.close()
        return result
    return []

def mark_attendance(student_id, date, status):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE status=%s",
                (student_id, date, status, status)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error marking attendance: {e}")
            return False
        finally:
            conn.close()

def get_attendance_report(class_name=None, student_name=None, start_date=None, end_date=None):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT s.name, s.roll_number, s.class, s.section, a.date, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            WHERE 1=1
        """
        params = []
        if class_name:
            query += " AND s.class = %s"
            params.append(class_name)
        if student_name:
            query += " AND s.name LIKE %s"
            params.append(f"%{student_name}%")
        if start_date:
            query += " AND a.date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND a.date <= %s"
            params.append(end_date)
        query += " ORDER BY a.date DESC"
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result
    return []

def get_total_students():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students")
        result = cursor.fetchone()[0]
        conn.close()
        return result
    return 0

def get_todays_present_count():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        from datetime import date
        cursor.execute(
            "SELECT COUNT(*) FROM attendance WHERE date=%s AND status='Present'",
            (date.today(),)
        )
        result = cursor.fetchone()[0]
        conn.close()
        return result
    return 0

def get_todays_absent_count():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        from datetime import date
        cursor.execute(
            "SELECT COUNT(*) FROM attendance WHERE date=%s AND status='Absent'",
            (date.today(),)
        )
        result = cursor.fetchone()[0]
        conn.close()
        return result
    return 0

def get_recent_attendance():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.name, s.class, s.section, a.date, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            ORDER BY a.date DESC
            LIMIT 10
        """)
        result = cursor.fetchall()
        conn.close()
        return result
    return []
def get_all_classes_sections():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT class, section FROM students ORDER BY class, section"
        )
        result = cursor.fetchall()
        conn.close()
        return result
    return []

def get_students_count_by_section(class_name, section):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM students WHERE class=%s AND section=%s",
            (class_name, section)
        )
        result = cursor.fetchone()[0]
        conn.close()
        return result
    return 0

def get_present_count_by_section(class_name, section):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        from datetime import date
        cursor.execute(
            """SELECT COUNT(*) FROM attendance a
               JOIN students s ON a.student_id = s.id
               WHERE s.class=%s AND s.section=%s
               AND a.date=%s AND a.status='Present'""",
            (class_name, section, date.today())
        )
        result = cursor.fetchone()[0]
        conn.close()
        return result
    return 0

def get_absent_count_by_section(class_name, section):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        from datetime import date
        cursor.execute(
            """SELECT COUNT(*) FROM attendance a
               JOIN students s ON a.student_id = s.id
               WHERE s.class=%s AND s.section=%s
               AND a.date=%s AND a.status='Absent'""",
            (class_name, section, date.today())
        )
        result = cursor.fetchone()[0]
        conn.close()
        return result
    return 0

def get_recent_attendance_by_section(class_name, section):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT s.name, s.class, s.section, a.date, a.status
               FROM attendance a
               JOIN students s ON a.student_id = s.id
               WHERE s.class=%s AND s.section=%s
               ORDER BY a.date DESC LIMIT 10""",
            (class_name, section)
        )
        result = cursor.fetchall()
        conn.close()
        return result
    return []