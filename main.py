import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from gui.dashboard import Dashboard
from gui.student_form import StudentForm
from gui.attendance_page import AttendancePage
from gui.report_page import ReportPage

class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")  # Modern Dark Theme
        self.title("Smart Attendance System")
        self.geometry("1200x750")
        self.resizable(True, True)
        self.current_frame = None
        self.build_ui()

    def build_ui(self):
        # Sidebar
        sidebar = ttk.Frame(self, bootstyle="dark", width=220)
        sidebar.pack(side=LEFT, fill=Y)
        sidebar.pack_propagate(False)

        # Logo Area
        logo_frame = ttk.Frame(sidebar, bootstyle="dark")
        logo_frame.pack(fill=X, pady=30)
        ttk.Label(logo_frame, text="🎓", font=("Helvetica", 36),
                  bootstyle="inverse-dark").pack()
        ttk.Label(logo_frame, text="SMART", font=("Helvetica", 14, "bold"),
                  bootstyle="inverse-dark").pack()
        ttk.Label(logo_frame, text="ATTENDANCE", font=("Helvetica", 11),
                  bootstyle="inverse-dark").pack()

        # Divider
        ttk.Separator(sidebar, orient=HORIZONTAL).pack(fill=X, padx=15, pady=5)

        # Nav Buttons
        self.nav_buttons = []
        buttons = [
            ("  🏠  Dashboard", self.show_dashboard),
            ("  👨‍🎓  Students", self.show_students),
            ("  📋  Attendance", self.show_attendance),
            ("  📊  Reports", self.show_reports),
        ]

        for text, command in buttons:
            btn = ttk.Button(sidebar, text=text, bootstyle="secondary",
                             command=command, width=22)
            btn.pack(pady=6, padx=15, anchor=W)
            self.nav_buttons.append(btn)

        # Bottom info
        ttk.Separator(sidebar, orient=HORIZONTAL).pack(fill=X, padx=15, pady=5, side=BOTTOM)
        ttk.Label(sidebar, text="v1.0 Prototype", font=("Helvetica", 8),
                  bootstyle="inverse-dark").pack(side=BOTTOM, pady=10)

        # Content Area
        self.content = ttk.Frame(self)
        self.content.pack(side=LEFT, fill=BOTH, expand=True)

        self.show_dashboard()

    def switch_frame(self, frame_class):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self.content)
        self.current_frame.pack(fill=BOTH, expand=True)

    def show_dashboard(self):
        self.switch_frame(Dashboard)

    def show_students(self):
        self.switch_frame(StudentForm)

    def show_attendance(self):
        self.switch_frame(AttendancePage)

    def show_reports(self):
        self.switch_frame(ReportPage)

if __name__ == "__main__":
    app = App()
    app.mainloop()