# Python imports
import logging
import tkinter as tk

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from .base import BaseView


class AllVolunteersView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
            width=config.SCREEN_WIDTH,
        )
        self.container.pack(pady=10)

        # Header
        self.header_container = tk.Frame(self.container)
        self.header_container.pack(pady=15, fill="x", expand=True)

        self.header = tk.Label(
            master=self.header_container,
            text=f"ALL VOLUNTEERS",
            font=(60),
        )
        self.header.pack(
            side="left",
        )

        # selected volunteer buttons
        self.edit_volunteer_button = tk.Button(
            master=self.header_container,
            text="Edit Selected volunteer",
            command=lambda: print("hello"),
        )
        self.edit_volunteer_button.pack(
            side="right",
        )

        self.view_volunteer_button = tk.Button(
            master=self.header_container,
            text="View Selected volunteer",
            command=lambda: print("hello"),
        )
        self.view_volunteer_button.pack(
            side="right",
        )
        self.add_volunteer_button = tk.Button(
            master=self.header_container,
            text="+ Add volunteer",
            command=lambda: print("hello"),
        )
        self.add_volunteer_button.pack(
            side="right",
        )

        # self.render_all_volunteers()
