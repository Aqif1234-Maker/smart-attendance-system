import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import date
import database

class ReportPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.report_data = []
        self.build_ui()

    def build_ui(self):
        # Header
        header = ttk.Frame(self, bootstyle="dark")
        header.pack(fill=X)
        ttk.Label(header, text="📊  Attendance Reports", font=("Helvetica", 18, "bold"),
                  bootstyle="inverse-dark").pack(side=LEFT, padx=20, pady=15)

        # Filter Frame
        filter_frame = ttk.LabelFrame(self, text="  🔍 Filter Options  ")
        filter_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(filter_frame, text="Student Name:", font=("Helvetica", 10)).grid(
            row=0, column=0, padx=10, pady=12)
        self.name_var = ttk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.name_var,
                  width=15, bootstyle="dark").grid(row=0, column=1, padx=5, pady=12)

        ttk.Label(filter_frame, text="Class:", font=("Helvetica", 10)).grid(
            row=0, column=2, padx=10, pady=12)
        self.class_var = ttk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.class_var,
                  width=8, bootstyle="dark").grid(row=0, column=3, padx=5, pady=12)

        ttk.Label(filter_frame, text="From (YYYY-MM-DD):", font=("Helvetica", 10)).grid(
            row=0, column=4, padx=10, pady=12)
        self.start_var = ttk.StringVar(value=str(date.today()))
        ttk.Entry(filter_frame, textvariable=self.start_var,
                  width=14, bootstyle="dark").grid(row=0, column=5, padx=5, pady=12)

        ttk.Label(filter_frame, text="To (YYYY-MM-DD):", font=("Helvetica", 10)).grid(
            row=0, column=6, padx=10, pady=12)
        self.end_var = ttk.StringVar(value=str(date.today()))
        ttk.Entry(filter_frame, textvariable=self.end_var,
                  width=14, bootstyle="dark").grid(row=0, column=7, padx=5, pady=12)

        ttk.Button(filter_frame, text="📊  Generate", bootstyle="primary",
                   command=self.generate_report,
                   width=15).grid(row=0, column=8, padx=10, pady=12)

        # Table
        columns = ("Name", "Roll No", "Class", "Section", "Date", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings",
                                  height=12, bootstyle="dark")
        col_widths = [180, 100, 80, 80, 130, 110]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=CENTER)

        scrollbar = ttk.Scrollbar(self, orient=VERTICAL,
                                   command=self.tree.yview, bootstyle="dark-round")
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y, padx=(0, 5))
        self.tree.pack(fill=BOTH, padx=20, pady=5)

        # Action Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=12)
        ttk.Button(btn_frame, text="📥  Export to Excel", bootstyle="success",
                   command=self.export_excel, width=20).pack(side=LEFT, padx=10)
        ttk.Button(btn_frame, text="📊  Show Chart", bootstyle="info",
                   command=self.show_chart, width=18).pack(side=LEFT, padx=10)

    def generate_report(self):
        name = self.name_var.get() or None
        cls = self.class_var.get() or None
        start = self.start_var.get() or None
        end = self.end_var.get() or None

        self.report_data = database.get_attendance_report(cls, name, start, end)

        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.report_data:
            self.tree.insert("", END, values=row)

        if not self.report_data:
            messagebox.showinfo("Info", "No records found for selected filters.")

    def export_excel(self):
        if not self.report_data:
            messagebox.showwarning("Warning", "No data to export. Generate a report first!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Report"
        )
        if file_path:
            df = pd.DataFrame(self.report_data,
                              columns=["Name", "Roll No", "Class", "Section", "Date", "Status"])
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"✅ Report exported to {file_path}")

    def show_chart(self):
        if not self.report_data:
            messagebox.showwarning("Warning", "No data to chart. Generate a report first!")
            return

        statuses = [row[5] for row in self.report_data]
        present = statuses.count("Present")
        absent = statuses.count("Absent")
        late = statuses.count("Late")

        plt.style.use("dark_background")
        labels = ["Present", "Absent", "Late"]
        values = [present, absent, late]
        colors = ["#28a745", "#dc3545", "#ffc107"]

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(labels, values, color=colors, width=0.5, edgecolor="white")
        ax.set_title("Attendance Summary", fontsize=14, fontweight="bold")
        ax.set_ylabel("Count")
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(val), ha="center", fontweight="bold")

        chart_win = ttk.Toplevel(self)
        chart_win.title("📊 Attendance Chart")
        chart_win.geometry("600x450")
        canvas = FigureCanvasTkAgg(fig, master=chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)