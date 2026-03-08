import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import database

class StudentForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_id = None
        self.build_ui()

    def build_ui(self):
        # Header
        header = ttk.Frame(self, bootstyle="dark")
        header.pack(fill=X)
        ttk.Label(header, text="👨‍🎓  Student Management", font=("Helvetica", 18, "bold"),
                  bootstyle="inverse-dark").pack(side=LEFT, padx=20, pady=15)

        # Form
        form = ttk.LabelFrame(self, text="  📝 Student Details  ")
        form.pack(fill=X, padx=20, pady=10)

        fields = ["Name", "Roll Number", "Class", "Section", "Contact"]
        self.entries = {}

        for i, field in enumerate(fields):
            ttk.Label(form, text=field, font=("Helvetica", 10)).grid(
                row=i, column=0, padx=20, pady=8, sticky=W)
            entry = ttk.Entry(form, width=35, bootstyle="dark")
            entry.grid(row=i, column=1, padx=20, pady=8, sticky=W)
            self.entries[field] = entry

        # Buttons
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=15, padx=20, sticky=W)

        ttk.Button(btn_frame, text="➕  Add Student", bootstyle="success",
                   command=self.add_student, width=18).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="✏️  Update", bootstyle="warning",
                   command=self.update_student, width=15).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️  Clear", bootstyle="secondary-outline",
                   command=self.clear_form, width=12).pack(side=LEFT, padx=5)

        # Search
        search_frame = ttk.Frame(self)
        search_frame.pack(fill=X, padx=20, pady=8)
        ttk.Label(search_frame, text="🔍  Search:", font=("Helvetica", 10)).pack(side=LEFT)
        self.search_var = ttk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var,
                                  width=35, bootstyle="dark")
        search_entry.pack(side=LEFT, padx=10)
        search_entry.bind("<KeyRelease>", self.search_students)

        ttk.Button(search_frame, text="🗑️  Delete Selected", bootstyle="danger-outline",
                   command=self.delete_student).pack(side=RIGHT, padx=5)

        # Table
        columns = ("ID", "Name", "Roll No", "Class", "Section", "Contact")
        self.tree = ttk.Treeview(self, columns=columns, show="headings",
                                  height=12, bootstyle="dark")
        col_widths = [60, 180, 100, 80, 80, 130]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=CENTER)

        scrollbar = ttk.Scrollbar(self, orient=VERTICAL,
                                   command=self.tree.yview, bootstyle="dark-round")
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y, padx=(0, 5))
        self.tree.pack(fill=BOTH, padx=20, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        self.load_students()

    def load_students(self, students=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data = students if students else database.get_all_students()
        for row in data:
            self.tree.insert("", END, values=row)

    def search_students(self, event):
        keyword = self.search_var.get()
        results = database.search_students(keyword)
        self.load_students(results)

    def on_row_select(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            self.selected_id = values[0]
            keys = ["Name", "Roll Number", "Class", "Section", "Contact"]
            for i, key in enumerate(keys):
                self.entries[key].delete(0, END)
                self.entries[key].insert(0, values[i + 1])

    def add_student(self):
        name = self.entries["Name"].get()
        roll = self.entries["Roll Number"].get()
        cls = self.entries["Class"].get()
        sec = self.entries["Section"].get()
        contact = self.entries["Contact"].get()

        if not all([name, roll, cls, sec]):
            messagebox.showwarning("Validation", "Please fill all required fields!")
            return

        success = database.add_student(name, roll, cls, sec, contact)
        if success:
            messagebox.showinfo("Success", "✅ Student added successfully!")
            self.clear_form()
            self.load_students()
        else:
            messagebox.showerror("Error", "❌ Failed! This roll number already exists in the same class and section.")

    def update_student(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Please select a student to update!")
            return
        name = self.entries["Name"].get()
        roll = self.entries["Roll Number"].get()
        cls = self.entries["Class"].get()
        sec = self.entries["Section"].get()
        contact = self.entries["Contact"].get()
        success = database.update_student(self.selected_id, name, roll, cls, sec, contact)
        if success:
            messagebox.showinfo("Success", "✅ Student updated successfully!")
            self.clear_form()
            self.load_students()

    def delete_student(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Please select a student to delete!")
            return
        confirm = messagebox.askyesno("Confirm Delete", "⚠️ Are you sure you want to delete this student?")
        if confirm:
            database.delete_student(self.selected_id)
            messagebox.showinfo("Success", "🗑️ Student deleted successfully!")
            self.clear_form()
            self.load_students()

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, END)
        self.selected_id = None