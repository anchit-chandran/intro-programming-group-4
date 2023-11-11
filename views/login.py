# Python imports
import logging
import tkinter as tk

# Project imports
from constants import config
from .dashboard import DashboardView
from utilities.db import run_query_get_rows


class LoginView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        logging.debug("LoginView created")
        self.master = master
        self.render_widgets()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
            width=500,
            height=300,
        )
        self.container.pack(
            fill="both",
            padx=30,
            pady=100,
        )

        # Header
        self.header = tk.Label(
            master=self.container,
            text="LOGIN",
            font=(60),
        )
        self.header.pack()

        # Username
        self.username_frame = tk.Frame(
            master=self.container,
        )
        self.username_frame.pack()

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
            master=self.password_frame, width=50, textvariable=self.password
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

    def _delete_window(self, window: tk.Toplevel) -> None:
        window.destroy()

    def _render_error_popup_window(self, message: str) -> None:
        self.error_popup_window = tk.Toplevel(self.master)
        self.error_popup_window.title("❌ Error")
        tk.Label(
            master=self.error_popup_window,
            text=message,
        ).pack(
            padx=10,
            pady=2,
        )
        tk.Button(
            master=self.error_popup_window,
            text="Ok",
            command=lambda: self._delete_window(self.error_popup_window),
        ).pack(
            padx=5,
            pady=2,
        )

        # Disable main window
        self.error_popup_window.grab_set()

    def _on_login(self) -> None:
        """Callback fn for login button"""
        username = self.username.get()
        password = self.password.get()

        if not self._input_valid(username, password):
            self._render_error_popup_window(message="Fields cannot be blank.")
            return None

        # Passes all frontend validation. Check username + pw correct

        # Query db
        un_pw_correct = run_query_get_rows(
                query=f"SELECT username, password FROM User WHERE username='{username}' and password='{password}'"
            )

        # U/n or pw incorrect
        if not un_pw_correct:
            self._render_error_popup_window(
                message="Username or password incorrect. Please check and try again."
            )
            return None

        # Handle sucessful login logic
        self.master.switch_view(DashboardView)
