# Python imports
import logging
import tkinter as tk

# Project imports
from constants import config


class DashboardView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        logging.debug('DashboardView created')
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
            text="DASHBOARD",
            font=(60),
        )
        self.header.pack()