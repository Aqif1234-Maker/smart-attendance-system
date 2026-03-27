import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class LandingPage(ttk.Frame):
    def __init__(self, parent, on_login, on_signup):
        super().__init__(parent)
        self.on_login = on_login
        self.on_signup = on_signup
        self.pack(fill=BOTH, expand=True)
        self._build()

    def _build(self):
        # ── Background canvas ──────────────────────────
        self.configure(style="dark.TFrame")

        # ── Center container ───────────────────────────
        center = ttk.Frame(self, padding=0)
        center.place(relx=0.5, rely=0.5, anchor=CENTER)

        # ── Logo / Icon ────────────────────────────────
        ttk.Label(
            center,
            text="🎓",
            font=("Helvetica", 72),
            bootstyle="default"
        ).pack(pady=(0, 10))

        # ── App Title ──────────────────────────────────
        ttk.Label(
            center,
            text="Smart Attendance System",
            font=("Helvetica", 28, "bold"),
            bootstyle="info"
        ).pack(pady=(0, 6))

        # ── Subtitle ───────────────────────────────────
        ttk.Label(
            center,
            text="Manage student attendance the smart way",
            font=("Helvetica", 13),
            bootstyle="secondary"
        ).pack(pady=(0, 50))

        # ── Divider line ───────────────────────────────
        ttk.Separator(center, orient=HORIZONTAL).pack(fill=X, pady=(0, 40))

        # ── Buttons container ──────────────────────────
        btn_frame = ttk.Frame(center)
        btn_frame.pack()

        # Login button
        ttk.Button(
            btn_frame,
            text="🔑   Login",
            bootstyle="info",
            width=22,
            padding=(0, 14),
            command=self.on_login
        ).pack(pady=(0, 14))

        # Sign Up button
        ttk.Button(
            btn_frame,
            text="✏️   Create Account",
            bootstyle="outline-info",
            width=22,
            padding=(0, 14),
            command=self.on_signup
        ).pack()

        # ── Footer ─────────────────────────────────────
        ttk.Label(
            center,
            text="v1.0  ·  Teacher Portal",
            font=("Helvetica", 10),
            bootstyle="secondary"
        ).pack(pady=(50, 0))