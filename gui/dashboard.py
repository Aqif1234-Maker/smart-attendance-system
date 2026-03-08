import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import database

class Dashboard(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.sections = []
        self.build_ui()

    def build_ui(self):
        # Header
        header = ttk.Frame(self, bootstyle="dark")
        header.pack(fill=X)
        ttk.Label(header, text="🏠  Dashboard",
                  font=("Helvetica", 18, "bold"),
                  bootstyle="inverse-dark").pack(side=LEFT, padx=20, pady=15)
        ttk.Button(header, text="🔄  Refresh",
                   bootstyle="secondary-outline",
                   command=self.refresh).pack(side=RIGHT, padx=20, pady=15)

        # ── Overall Summary Cards ──────────────────────
        overall_frame = ttk.LabelFrame(self, text="  📊 Overall Summary — All Sections  ")
        overall_frame.pack(fill=X, padx=20, pady=10)

        overall_cards = ttk.Frame(overall_frame)
        overall_cards.pack(fill=X, padx=10, pady=10)

        self.overall_total   = ttk.StringVar(value="0")
        self.overall_present = ttk.StringVar(value="0")
        self.overall_absent  = ttk.StringVar(value="0")
        self.overall_percent = ttk.StringVar(value="0%")

        self.make_card(overall_cards, "👨‍🎓 Total Students", self.overall_total,   "primary", 0)
        self.make_card(overall_cards, "✅ Today Present",   self.overall_present, "success", 1)
        self.make_card(overall_cards, "❌ Today Absent",    self.overall_absent,  "danger",  2)
        self.make_card(overall_cards, "📊 Attendance %",    self.overall_percent, "info",    3)

        # ── Section Filter Dropdown ────────────────────
        filter_frame = ttk.LabelFrame(self, text="  🔍 Filter by Section  ")
        filter_frame.pack(fill=X, padx=20, pady=5)

        inner = ttk.Frame(filter_frame)
        inner.pack(padx=10, pady=10, anchor=W)

        ttk.Label(inner, text="Select Class & Section:",
                  font=("Helvetica", 11)).pack(side=LEFT, padx=(0, 10))

        self.section_var = ttk.StringVar(value="All Sections")
        self.section_combo = ttk.Combobox(
            inner,
            textvariable=self.section_var,
            state="readonly",
            width=25,
            font=("Helvetica", 11)
        )
        self.section_combo.pack(side=LEFT, padx=5)
        # EVENT: when user selects from dropdown, update section stats
        self.section_combo.bind("<<ComboboxSelected>>", self.on_section_change)

        # ── Section Stats Cards ────────────────────────
        self.section_stats_frame = ttk.LabelFrame(self, text="  📋 Section Stats  ")
        self.section_stats_frame.pack(fill=X, padx=20, pady=5)

        section_cards = ttk.Frame(self.section_stats_frame)
        section_cards.pack(fill=X, padx=10, pady=10)

        self.sec_total   = ttk.StringVar(value="—")
        self.sec_present = ttk.StringVar(value="—")
        self.sec_absent  = ttk.StringVar(value="—")
        self.sec_percent = ttk.StringVar(value="—")

        self.make_card(section_cards, "👨‍🎓 Total Students", self.sec_total,   "primary", 0)
        self.make_card(section_cards, "✅ Today Present",   self.sec_present, "success", 1)
        self.make_card(section_cards, "❌ Today Absent",    self.sec_absent,  "danger",  2)
        self.make_card(section_cards, "📊 Attendance %",    self.sec_percent, "info",    3)

        # ── Recent Attendance Table ────────────────────
        ttk.Label(self, text="  📋 Recent Attendance",
                  font=("Helvetica", 12, "bold")).pack(padx=20, anchor=W, pady=(10, 0))

        table_frame = ttk.Frame(self)
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=5)

        columns = ("Name", "Class", "Section", "Date", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns,
                                  show="headings", height=7, bootstyle="dark")
        col_widths = [200, 100, 100, 150, 120]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL,
                                   command=self.tree.yview, bootstyle="dark-round")
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.pack(fill=BOTH, expand=True)

        # Load everything on startup
        self.load_all_data()

    def make_card(self, parent, title, variable, style, col):
        frame = ttk.Frame(parent, bootstyle=style, padding=18)
        frame.grid(row=0, column=col, padx=8, pady=5, sticky=NSEW)
        parent.columnconfigure(col, weight=1)
        ttk.Label(frame, text=title, font=("Helvetica", 10),
                  bootstyle=f"inverse-{style}").pack(anchor=W)
        ttk.Label(frame, textvariable=variable, font=("Helvetica", 24, "bold"),
                  bootstyle=f"inverse-{style}").pack(anchor=W, pady=4)

    def load_all_data(self):
        # Fetch all class+section combos from DB
        self.sections = database.get_all_classes_sections()

        # Build dropdown values
        dropdown_values = ["All Sections"]
        for cls, sec in self.sections:
            dropdown_values.append(f"Class {cls}  —  Section {sec}")

        self.section_combo["values"] = dropdown_values
        self.section_var.set("All Sections")

        # Load overall stats
        self.update_overall_stats()

        # Show all sections in table by default
        self.update_table_all()

        # Reset section stats to dashes
        self.sec_total.set("—")
        self.sec_present.set("—")
        self.sec_absent.set("—")
        self.sec_percent.set("—")

    def update_overall_stats(self):
        total   = database.get_total_students()
        present = database.get_todays_present_count()
        absent  = database.get_todays_absent_count()
        percent = f"{round((present / total) * 100)}%" if total > 0 else "0%"

        self.overall_total.set(total)
        self.overall_present.set(present)
        self.overall_absent.set(absent)
        self.overall_percent.set(percent)

    def on_section_change(self, event):
        # EVENT DRIVEN — called when dropdown selection changes
        selected = self.section_var.get()

        if selected == "All Sections":
            # Reset section cards
            self.sec_total.set("—")
            self.sec_present.set("—")
            self.sec_absent.set("—")
            self.sec_percent.set("—")
            self.update_table_all()
            return

        # Parse class and section from selected string
        # Format is "Class SE  —  Section A"
        parts = selected.replace("Class ", "").replace("Section ", "").split("  —  ")
        cls = parts[0].strip()
        sec = parts[1].strip()

        # Update section stat cards
        total   = database.get_students_count_by_section(cls, sec)
        present = database.get_present_count_by_section(cls, sec)
        absent  = database.get_absent_count_by_section(cls, sec)
        percent = f"{round((present / total) * 100)}%" if total > 0 else "0%"

        self.sec_total.set(total)
        self.sec_present.set(present)
        self.sec_absent.set(absent)
        self.sec_percent.set(percent)

        # Update LabelFrame title to show which section
        self.section_stats_frame.config(
            text=f"  📋 Section Stats — Class {cls}, Section {sec}  "
        )

        # Update table for this section only
        self.update_table_section(cls, sec)

    def update_table_all(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in database.get_recent_attendance():
            self.tree.insert("", END, values=row)

    def update_table_section(self, cls, sec):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in database.get_recent_attendance_by_section(cls, sec):
            self.tree.insert("", END, values=row)

    def refresh(self):
        self.load_all_data()