import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from gui.landing_page   import LandingPage
from gui.login_page     import LoginPage
from gui.signup_page    import SignupPage
from gui.dashboard      import Dashboard
from gui.student_form   import StudentForm
from gui.attendance_page import AttendancePage
from gui.report_page    import ReportPage
import database


# ══════════════════════════════════════════════════════════════
# APP — Main application window (loaded after login)
# ══════════════════════════════════════════════════════════════

class App(ttk.Frame):
    """
    Main application — only created after successful login.
    Receives teacher dict {id, full_name, email} from login.
    """
    def __init__(self, parent, teacher, on_logout):
        super().__init__(parent)
        self.teacher   = teacher       # Logged-in teacher info
        self.on_logout = on_logout     # Callback to go back to landing
        self.pack(fill=BOTH, expand=True)
        self.current_frame = None
        self._build()

    def _build(self):
        # ── Sidebar ────────────────────────────────────
        self.sidebar = ttk.Frame(self, width=220, bootstyle="dark")
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False)

        # Logo
        logo_frame = ttk.Frame(self.sidebar, bootstyle="dark", padding=(0, 20, 0, 16))
        logo_frame.pack(fill=X)
        ttk.Label(
            logo_frame, text="🎓",
            font=("Helvetica", 32), bootstyle="default"
        ).pack()
        ttk.Label(
            logo_frame, text="SMART ATTENDANCE",
            font=("Helvetica", 9, "bold"),
            bootstyle="info"
        ).pack()

        ttk.Separator(self.sidebar, orient=HORIZONTAL).pack(fill=X, padx=12, pady=4)

        # ── Teacher name badge ─────────────────────────
        teacher_frame = ttk.Frame(self.sidebar, bootstyle="dark", padding=(12, 10))
        teacher_frame.pack(fill=X)

        ttk.Label(
            teacher_frame,
            text="👤  Logged in as",
            font=("Helvetica", 9),
            bootstyle="secondary"
        ).pack(anchor=W)

        ttk.Label(
            teacher_frame,
            text=self.teacher["full_name"],
            font=("Helvetica", 11, "bold"),
            bootstyle="info",
            wraplength=180
        ).pack(anchor=W, pady=(2, 0))

        ttk.Separator(self.sidebar, orient=HORIZONTAL).pack(fill=X, padx=12, pady=8)

        # ── Navigation buttons ─────────────────────────
        nav_items = [
            ("🏠   Dashboard",  self._show_dashboard),
            ("👨‍🎓   Students",   self._show_students),
            ("📋   Attendance", self._show_attendance),
            ("📊   Reports",    self._show_reports),
        ]

        self.nav_buttons = []
        for label, cmd in nav_items:
            btn = ttk.Button(
                self.sidebar,
                text=label,
                bootstyle="dark",
                command=cmd,
                padding=(16, 10)
            )
            btn.pack(fill=X, padx=8, pady=2)
            self.nav_buttons.append(btn)

        # ── Spacer ─────────────────────────────────────
        ttk.Frame(self.sidebar, bootstyle="dark").pack(fill=Y, expand=True)

        # ── Logout button (at bottom) ──────────────────
        ttk.Separator(self.sidebar, orient=HORIZONTAL).pack(fill=X, padx=12, pady=4)

        ttk.Button(
            self.sidebar,
            text="🚪   Logout",
            bootstyle="outline-danger",
            command=self._logout,
            padding=(16, 10)
        ).pack(fill=X, padx=8, pady=(4, 16))

        ttk.Label(
            self.sidebar,
            text="v1.0",
            font=("Helvetica", 9),
            bootstyle="secondary"
        ).pack(pady=(0, 8))

        # ── Main content area ──────────────────────────
        self.content = ttk.Frame(self)
        self.content.pack(side=LEFT, fill=BOTH, expand=True)

        # Load dashboard by default
        self._show_dashboard()

    def _switch_frame(self, FrameClass):
        """Destroy current page and load new one."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = FrameClass(self.content)
        self.current_frame.pack(fill=BOTH, expand=True)

    def _show_dashboard(self):
        self._switch_frame(Dashboard)

    def _show_students(self):
        self._switch_frame(StudentForm)

    def _show_attendance(self):
        self._switch_frame(AttendancePage)

    def _show_reports(self):
        self._switch_frame(ReportPage)

    def _logout(self):
        from tkinter import messagebox
        confirmed = messagebox.askyesno(
            "Logout",
            f"Logout from {self.teacher['full_name']}'s account?"
        )
        if confirmed:
            self.on_logout()


# ══════════════════════════════════════════════════════════════
# ROOT CONTROLLER — manages which screen is visible
# ══════════════════════════════════════════════════════════════

class RootController:
    """
    Controls which page is shown:
    LandingPage → LoginPage / SignupPage → App (main)
    Logout → back to LandingPage
    """
    def __init__(self):
        # Create main window
        self.root = ttk.Window(
            title="Smart Attendance System",
            themename="darkly",
            size=(1200, 720),
            minsize=(900, 600)
        )
        self._center_window()

        # Auto-create teachers table if not exists
        database.create_teachers_table()

        # Current visible frame
        self.current = None

        # Start with landing page
        self.show_landing()

        self.root.mainloop()

    def _center_window(self):
        """Center the window on screen."""
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"+{x}+{y}")

    def _clear(self):
        """Destroy whatever is currently shown."""
        if self.current:
            self.current.destroy()
            self.current = None

    # ── Navigation methods ─────────────────────────────

    def show_landing(self):
        self._clear()
        self.current = LandingPage(
            self.root,
            on_login=self.show_login,
            on_signup=self.show_signup
        )

    def show_login(self):
        self._clear()
        self.current = LoginPage(
            self.root,
            on_login_success=self.show_main_app,
            on_goto_signup=self.show_signup
        )

    def show_signup(self):
        self._clear()
        self.current = SignupPage(
            self.root,
            on_signup_success=self.show_login,  # After signup → go to login
            on_goto_login=self.show_login
        )

    def show_main_app(self, teacher):
        """Called after successful login. teacher = {id, full_name, email}"""
        self._clear()
        self.current = App(
            self.root,
            teacher=teacher,
            on_logout=self.show_landing   # Logout → back to landing
        )


# ══════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    RootController()