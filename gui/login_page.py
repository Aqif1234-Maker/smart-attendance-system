import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import database


class LoginPage(ttk.Frame):
    def __init__(self, parent, on_login_success, on_goto_signup):
        super().__init__(parent)
        self.on_login_success = on_login_success
        self.on_goto_signup   = on_goto_signup
        self.pack(fill=BOTH, expand=True)
        self._build()

    def _build(self):
        # ── Center card ────────────────────────────────
        card = ttk.Frame(self, padding=48)
        card.place(relx=0.5, rely=0.5, anchor=CENTER)

        # ── Icon + Title ───────────────────────────────
        ttk.Label(card, text="🔑", font=("Helvetica", 44)).pack(pady=(0, 8))

        ttk.Label(
            card,
            text="Teacher Login",
            font=("Helvetica", 22, "bold"),
            bootstyle="info"
        ).pack(pady=(0, 4))

        ttk.Label(
            card,
            text="Sign in to access the attendance system",
            font=("Helvetica", 11),
            bootstyle="secondary"
        ).pack(pady=(0, 32))

        # ── Email field ────────────────────────────────
        ttk.Label(card, text="Email Address", font=("Helvetica", 11, "bold")).pack(anchor=W)
        self.email_var = ttk.StringVar()
        email_entry = ttk.Entry(
            card, textvariable=self.email_var,
            width=34, font=("Helvetica", 12)
        )
        email_entry.pack(pady=(4, 16), ipady=6)
        email_entry.focus()

        # ── Password field ─────────────────────────────
        ttk.Label(card, text="Password", font=("Helvetica", 11, "bold")).pack(anchor=W)
        self.pass_var = ttk.StringVar()
        pass_entry = ttk.Entry(
            card, textvariable=self.pass_var,
            show="●", width=34, font=("Helvetica", 12)
        )
        pass_entry.pack(pady=(4, 6), ipady=6)

        # ── Show/hide password toggle ──────────────────
        self.show_pass = ttk.BooleanVar(value=False)
        ttk.Checkbutton(
            card, text="Show password",
            variable=self.show_pass,
            bootstyle="info-round-toggle",
            command=lambda: pass_entry.config(
                show="" if self.show_pass.get() else "●"
            )
        ).pack(anchor=W, pady=(0, 24))

        # ── Login button ───────────────────────────────
        ttk.Button(
            card,
            text="Login  →",
            bootstyle="info",
            width=34,
            padding=(0, 12),
            command=self._login
        ).pack(pady=(0, 16))

        # Bind Enter key to login
        pass_entry.bind("<Return>", lambda e: self._login())
        email_entry.bind("<Return>", lambda e: pass_entry.focus())

        # ── Separator ──────────────────────────────────
        ttk.Separator(card).pack(fill=X, pady=(0, 16))

        # ── Go to signup ───────────────────────────────
        bottom = ttk.Frame(card)
        bottom.pack()
        ttk.Label(
            bottom,
            text="Don't have an account? ",
            font=("Helvetica", 11),
            bootstyle="secondary"
        ).pack(side=LEFT)
        signup_link = ttk.Label(
            bottom,
            text="Sign Up",
            font=("Helvetica", 11, "bold"),
            bootstyle="info",
            cursor="hand2"
        )
        signup_link.pack(side=LEFT)
        signup_link.bind("<Button-1>", lambda e: self.on_goto_signup())

        # ── Back to landing ────────────────────────────
        ttk.Button(
            card,
            text="← Back",
            bootstyle="link-secondary",
            command=self._back
        ).pack(pady=(12, 0))

    def _back(self):
        from gui.landing_page import LandingPage
        self.destroy()

    def _login(self):
        email    = self.email_var.get().strip()
        password = self.pass_var.get().strip()

        # ── Validation ─────────────────────────────────
        if not email or not password:
            messagebox.showwarning("Missing Fields", "Please enter both email and password.")
            return

        if "@" not in email or "." not in email:
            messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
            return

        # ── Check credentials ──────────────────────────
        teacher = database.login_teacher(email, password)

        if teacher:
            self.on_login_success(teacher)
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid email or password.\nPlease try again."
            )
            self.pass_var.set("")   # Clear password field on failure