import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import date
import database

class AttendancePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.attendance_vars = {}
        self.build_ui()

    def build_ui(self):
        # Header
        header = ttk.Frame(self, bootstyle="dark")
        header.pack(fill=X)
        ttk.Label(header, text="📋  Mark Attendance", font=("Helvetica", 18, "bold"),
                  bootstyle="inverse-dark").pack(side=LEFT, padx=20, pady=15)

        # Filter Frame
        filter_frame = ttk.LabelFrame(self, text="  🔍 Select Class & Date  ")
        filter_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(filter_frame, text="Class:", font=("Helvetica", 10)).grid(
            row=0, column=0, padx=15, pady=12)
        self.class_var = ttk.StringVar()
        ttk.Combobox(filter_frame, textvariable=self.class_var, bootstyle="dark",
                     values=["1","2","3","4","5","6","7","8","9","10"],
                     width=10).grid(row=0, column=1, padx=10, pady=12)

        ttk.Label(filter_frame, text="Section:", font=("Helvetica", 10)).grid(
            row=0, column=2, padx=15, pady=12)
        self.section_var = ttk.StringVar()
        ttk.Combobox(filter_frame, textvariable=self.section_var, bootstyle="dark",
                     values=["A","B","C","D"],
                     width=10).grid(row=0, column=3, padx=10, pady=12)

        ttk.Label(filter_frame, text="Date (YYYY-MM-DD):", font=("Helvetica", 10)).grid(
            row=0, column=4, padx=15, pady=12)
        self.date_var = ttk.StringVar(value=str(date.today()))
        ttk.Entry(filter_frame, textvariable=self.date_var,
                  width=14, bootstyle="dark").grid(row=0, column=5, padx=10, pady=12)

        ttk.Button(filter_frame, text="🔍  Load Students", bootstyle="primary",
                   command=self.load_students,
                   width=18).grid(row=0, column=6, padx=15, pady=12)

        # Students Area
        self.scroll_frame = ttk.Frame(self)
        self.scroll_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Submit Button
        ttk.Button(self, text="✅  Submit Attendance", bootstyle="success",
                   command=self.submit_attendance, width=22).pack(pady=12)

    def load_students(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.attendance_vars.clear()

        cls = self.class_var.get()
        sec = self.section_var.get()

        if not cls or not sec:
            messagebox.showwarning("Warning", "Please select class and section!")
            return

        students = database.get_students_by_class(cls, sec)

        if not students:
            ttk.Label(self.scroll_frame,
                      text="⚠️ No students found for this class/section.",
                      font=("Helvetica", 11)).pack(pady=20)
            return

        # Header Row
        header = ttk.Frame(self.scroll_frame, bootstyle="secondary")
        header.pack(fill=X, pady=2)
        ttk.Label(header, text="Roll No", width=12, font=("Helvetica", 10, "bold"),
                  bootstyle="inverse-secondary").pack(side=LEFT, padx=10, pady=8)
        ttk.Label(header, text="Student Name", width=22, font=("Helvetica", 10, "bold"),
                  bootstyle="inverse-secondary").pack(side=LEFT, padx=10, pady=8)
        ttk.Label(header, text="Mark Status", width=35, font=("Helvetica", 10, "bold"),
                  bootstyle="inverse-secondary").pack(side=LEFT, padx=10, pady=8)

        for i, student in enumerate(students):
            student_id, name, roll, cls_, sec_, contact = student
            bg = "dark" if i % 2 == 0 else "secondary"
            row = ttk.Frame(self.scroll_frame)
            row.pack(fill=X, pady=1)

            ttk.Label(row, text=roll, width=12,
                      font=("Helvetica", 10)).pack(side=LEFT, padx=10, pady=6)
            ttk.Label(row, text=name, width=22,
                      font=("Helvetica", 10)).pack(side=LEFT, padx=10, pady=6)

            status_var = ttk.StringVar(value="Present")
            self.attendance_vars[student_id] = status_var

            for status in ["Present", "Absent", "Late"]:
                color = "success" if status == "Present" else "danger" if status == "Absent" else "warning"
                ttk.Radiobutton(row, text=status, variable=status_var,
                                value=status, bootstyle=color).pack(side=LEFT, padx=10)

    def submit_attendance(self):
        if not self.attendance_vars:
            messagebox.showwarning("Warning", "Please load students first!")
            return

        selected_date = self.date_var.get()
        if not selected_date:
            messagebox.showwarning("Warning", "Please enter a date!")
            return

        success_count = 0
        for student_id, status_var in self.attendance_vars.items():
            success = database.mark_attendance(student_id, selected_date, status_var.get())
            if success:
                success_count += 1

        messagebox.showinfo("Success", f"✅ Attendance submitted for {success_count} students!")