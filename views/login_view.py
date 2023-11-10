# Python imports
import tkinter as tk

# Project imports
from constants import config


class LoginView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self.master,
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
        self.username_label.pack(anchor='w')
        
        self.username_entry_box = tk.Entry(master=self.username_frame, width=50)
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
        self.password_label.pack(anchor='w')
        
        self.password_entry_box = tk.Entry(master=self.password_frame, width=50)
        self.password_entry_box.pack()
