import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import database


class SignupPage(ttk.Frame):
    def __init__(self, parent, on_signup_success, on_goto_login):
        super().__init__(parent)
        self.on_signup_success = on_signup_success
        self.on_goto_login     = on_goto_login
        self.pack(fill=BOTH, expand=True)
        self._build()

    def _build(self):
        # ── Center card ────────────────────────────────
        card = ttk.Frame(self, padding=48)
        card.place(relx=0.5, rely=0.5, anchor=CENTER)

        # ── Icon + Title ───────────────────────────────
        ttk.Label(card, text="✏️", font=("Helvetica", 44)).pack(pady=(0, 8))

        ttk.Label(
            card,
            text="Create Teacher Account",
            font=("Helvetica", 22, "bold"),
            bootstyle="info"
        ).pack(pady=(0, 4))

        ttk.Label(
            card,
            text="Register to start managing attendance",
            font=("Helvetica", 11),
            bootstyle="secondary"
        ).pack(pady=(0, 28))

        # ── Full Name ──────────────────────────────────
        ttk.Label(card, text="Full Name", font=("Helvetica", 11, "bold")).pack(anchor=W)
        self.name_var = ttk.StringVar()
        name_entry = ttk.Entry(
            card, textvariable=self.name_var,
            width=34, font=("Helvetica", 12)
        )
        name_entry.pack(pady=(4, 14), ipady=6)
        name_entry.focus()

        # ── Email ──────────────────────────────────────
        ttk.Label(card, text="Email Address", font=("Helvetica", 11, "bold")).pack(anchor=W)
        self.email_var = ttk.StringVar()
        ttk.Entry(
            card, textvariable=self.email_var,
            width=34, font=("Helvetica", 12)
        ).pack(pady=(4, 14), ipady=6)

        # ── Password ───────────────────────────────────
        ttk.Label(card, text="Password  (min 6 characters)", font=("Helvetica", 11, "bold")).pack(anchor=W)
        self.pass_var = ttk.StringVar()
        self.pass_entry = ttk.Entry(
            card, textvariable=self.pass_var,
            show="●", width=34, font=("Helvetica", 12)
        )
        self.pass_entry.pack(pady=(4, 14), ipady=6)

        # ── Confirm Password ───────────────────────────
        ttk.Label(card, text="Confirm Password", font=("Helvetica", 11, "bold")).pack(anchor=W)
        self.confirm_var = ttk.StringVar()
        self.confirm_entry = ttk.Entry(
            card, textvariable=self.confirm_var,
            show="●", width=34, font=("Helvetica", 12)
        )
        self.confirm_entry.pack(pady=(4, 6), ipady=6)

        # ── Show/hide toggle ───────────────────────────
        self.show_pass = ttk.BooleanVar(value=False)
        ttk.Checkbutton(
            card, text="Show passwords",
            variable=self.show_pass,
            bootstyle="info-round-toggle",
            command=self._toggle_passwords
        ).pack(anchor=W, pady=(0, 22))

        # ── Sign Up button ─────────────────────────────
        ttk.Button(
            card,
            text="Create Account  →",
            bootstyle="success",
            width=34,
            padding=(0, 12),
            command=self._signup
        ).pack(pady=(0, 16))

        # Bind Enter key
        self.confirm_entry.bind("<Return>", lambda e: self._signup())

        # ── Separator ──────────────────────────────────
        ttk.Separator(card).pack(fill=X, pady=(0, 16))

        # ── Go to login ────────────────────────────────
        bottom = ttk.Frame(card)
        bottom.pack()
        ttk.Label(
            bottom,
            text="Already have an account? ",
            font=("Helvetica", 11),
            bootstyle="secondary"
        ).pack(side=LEFT)
        login_link = ttk.Label(
            bottom,
            text="Login",
            font=("Helvetica", 11, "bold"),
            bootstyle="info",
            cursor="hand2"
        )
        login_link.pack(side=LEFT)
        login_link.bind("<Button-1>", lambda e: self.on_goto_login())

        # ── Back button ────────────────────────────────
        ttk.Button(
            card,
            text="← Back",
            bootstyle="link-secondary",
            command=self.destroy
        ).pack(pady=(12, 0))

    def _toggle_passwords(self):
        show = "" if self.show_pass.get() else "●"
        self.pass_entry.config(show=show)
        self.confirm_entry.config(show=show)

    def _signup(self):
        name     = self.name_var.get().strip()
        email    = self.email_var.get().strip()
        password = self.pass_var.get().strip()
        confirm  = self.confirm_var.get().strip()

        # ── Validation ─────────────────────────────────
        if not all([name, email, password, confirm]):
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return

        if "@" not in email or "." not in email:
            messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
            return

        if len(password) < 6:
            messagebox.showwarning(
                "Weak Password",
                "Password must be at least 6 characters long."
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Password Mismatch",
                "Passwords do not match. Please try again."
            )
            self.pass_var.set("")
            self.confirm_var.set("")
            self.pass_entry.focus()
            return

        # ── Register in database ───────────────────────
        result = database.register_teacher(name, email, password)

        if result == "exists":
            messagebox.showerror(
                "Email Already Registered",
                f"An account with '{email}' already exists.\nPlease login instead."
            )
        elif result == "success":
            messagebox.showinfo(
                "Account Created! 🎉",
                f"Welcome, {name}!\nYour account has been created.\nPlease login to continue."
            )
            self.on_signup_success()   # Redirect to login page
        else:
            messagebox.showerror("Error", "Something went wrong. Please try again.")