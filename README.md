# 🎓 Smart Attendance System

A desktop GUI application for managing student attendance built with Python, MySQL, and ttkbootstrap.

## 🚀 Features
- Modern Dark themed GUI (ttkbootstrap)
- Add, edit, search and delete students
- Mark attendance as Present, Absent or Late
- Dashboard with per-section stats and dropdown filter
- Generate reports with date/class/name filters
- Export reports to Excel (.xlsx)
- Attendance charts with matplotlib

## 🛠️ Tech Stack
- **Language:** Python 3.13
- **GUI:** ttkbootstrap (Modern tkinter)
- **Database:** MySQL 8.0
- **Libraries:** pandas, matplotlib, openpyxl

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/smart-attendance-system.git
cd smart-attendance-system
```

### 2. Install dependencies
```bash
pip install ttkbootstrap pillow pandas openpyxl matplotlib mysql-connector-python
```

### 3. Setup MySQL Database
Run this SQL in MySQL Workbench:
```sql
CREATE DATABASE attendance_db;
USE attendance_db;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(20) NOT NULL,
    class VARCHAR(20) NOT NULL,
    section VARCHAR(10) NOT NULL,
    contact VARCHAR(15),
    UNIQUE KEY unique_roll_per_class (roll_number, class, section)
);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    date DATE NOT NULL,
    status ENUM('Present', 'Absent', 'Late') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    UNIQUE KEY unique_attendance (student_id, date)
);
```

### 4. Configure database connection
```bash
cp config.example.py config.py
```
Edit `config.py` and fill in your MySQL username and password.

### 5. Run the app
```bash
python main.py
```

## 📁 Project Structure
```
SmartAttendance/
├── main.py                 # Entry point + navigation
├── config.py               # MySQL connection (not in repo)
├── config.example.py       # Template for config.py
├── database.py             # All database operations
├── gui/
│   ├── dashboard.py        # Dashboard with section stats
│   ├── student_form.py     # Student management
│   ├── attendance_page.py  # Mark attendance
│   └── report_page.py      # Reports + export
└── README.md
```

## 👨‍💻 Built By
Aqif Shaikh — Event-Driven Programming Project