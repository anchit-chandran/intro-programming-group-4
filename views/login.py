# Python imports
import logging
import tkinter as tk

# Project imports
from .base import BaseView
from utilities.db import run_query_get_rows
from constants.config import TITLE


class LoginView(BaseView):
    def __init__(self, master=None):
        super().__init__(master, render_nav=False)
        self.master = master
        self.render_widgets()
        self.master.update()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.LabelFrame(
            master=self,
            text=f"Welcome to {TITLE} 👋",
            width=500,
            height=300,
        )
        self.container.pack(
            fill="both",
            pady=100,
        )

        # Header
        self.logo = tk.PhotoImage(file="assets/logo.png")
        self.logo_label = tk.Label(
            master=self.container,
            image=self.logo,
        )
        self.logo_label.pack()

        # Username
        self.username_frame = tk.Frame(
            master=self.container,
        )
        self.username_frame.pack(padx=10, pady=10)

        self.username_label = tk.Label(
            master=self.username_frame,
            text="Username",
            justify="left",
            font=(20),
        )
        self.username_label.pack(anchor="w")

        self.username = tk.StringVar()
        self.username_entry_box = tk.Entry(
            master=self.username_frame, width=50, textvariable=self.username
        )
        self.username_entry_box.pack()

        # Password
        self.password_frame = tk.Frame(
            master=self.container,
        )
        self.password_frame.pack()

        self.password_label = tk.Label(
            master=self.password_frame,
            text="Password",
            justify="left",
            font=(20),
        )
        self.password_label.pack(anchor="w")

        self.password = tk.StringVar()
        self.password_entry_box = tk.Entry(
            master=self.password_frame, show="*", width=50, textvariable=self.password
        )
        self.password_entry_box.pack()

        # Login Button
        self.login_button = tk.Button(
            master=self.password_frame,
            text="Login",
            height=1,
            width=10,
            command=self._on_login,
        )
        self.login_button.pack(pady=10, anchor="w")

    def _input_valid(self, username: str, password: str) -> bool:
        if not username or not password:
            return False

        return True

    def _on_login(self) -> None:
        """Callback fn for login button"""
        username = self.username.get().strip()
        password = self.password.get()

        if not self._input_valid(username, password):
            title = "Invalid"
            message = "Fields cannot be blank."
            self.render_error_popup_window(message=message)
            return None

        # Passes all form validation. Check username + pw correct

        # Query db
        un_pw_correct = run_query_get_rows(
            query=f"SELECT id, username, is_admin, password FROM User WHERE username='{username}' and password='{password}'"
        )

        # U/n or pw incorrect
        if not un_pw_correct:
            self.render_error_popup_window(
                message="Username or password incorrect. Please check and try again.",
            )
            return None

        # Set global state variables
        current_state = self.master.get_global_state()
        current_state.update(
            {
                "user_id": un_pw_correct[0]["id"],
                "username": username,
                "is_admin": un_pw_correct[0]["is_admin"],
            }
        )
        self.master.set_global_state(current_state)

        # Handle sucessful login logic
        self.master.switch_to_default_view_after_login()
