# Python imports
import logging
import tkinter as tk

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from .base import BaseView


class MyCampView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()
        # message button function

    def handle_send_message(self):
        # self.master.switch_to_view("add_message")
        return

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
            pady=20,
        )

        # Header
        self.header_container = tk.Frame(
            master=self.container,
            width=500,
            height=100,
        )
        self.header_container.grid(
            row=0,
            column=0,
        )

        self.header = tk.Label(
            master=self.header_container,
            text=f"WELLCOME {self.master.get_global_state().get('username')}! 👋",
            font=(60),
        )
        self.header.grid(
            row=0,
            column=0,
        )

        # ------------------------ Top container------------------------------
        # TO DO: get volunteer ID to get camp id from db
        # TO DO: retrieve camp info from db and put instead of placeholder
        # TO DO: get resources list from db and map over them to display data
        # TO DO: edit handle_send_message to redirect correctly - look up

        self.top_container = tk.Frame(
            master=self.container,
            width=700,
            height=600,
        )
        self.top_container.grid(row=1, column=0, padx=30, pady=20, sticky="nsew")

        # info container
        self.info_container = tk.Frame(
            master=self.top_container, width=300, height=600, bg="lightgrey"
        )
        self.info_container.grid(row=0, column=0, padx=30, pady=20, sticky="nsew")

        # header span 2 columns
        self.info_header = tk.Label(
            master=self.info_container, text="INFORMATION", font=42, bg="lightgrey"
        )
        self.info_header.grid(
            row=3, column=0, columnspan=2, pady=20, padx=10, sticky="w"
        )

        # left label
        self.location_label = tk.Label(
            master=self.info_container, text="LOCATION:", font=32, bg="lightgrey"
        )
        self.location_label.grid(row=4, column=0, sticky="w", pady=10, padx=10)

        self.max_capacity_label = tk.Label(
            master=self.info_container, text="MAX CAPACITY:", font=32, bg="lightgrey"
        )
        self.max_capacity_label.grid(row=5, column=0, sticky="w", pady=10, padx=10)

        # right info
        self.location_info = tk.Label(
            master=self.info_container, text="Placeholder", font=24, bg="lightgrey"
        )
        self.location_info.grid(row=4, column=1, sticky="w", pady=10, padx=10)

        self.max_capacity_info = tk.Label(
            master=self.info_container, text="Placeholder", font=24, bg="lightgrey"
        )
        self.max_capacity_info.grid(row=5, column=1, sticky="w", pady=10, padx=10)

        # resources container
        self.resources_container = tk.Frame(
            master=self.top_container, width=300, height=600, bg="lightgrey"
        )
        self.resources_container.grid(row=0, column=1, padx=30, pady=20, sticky="nsew")

        # header span 2 columns
        self.resources_header = tk.Label(
            master=self.resources_container, text="RESOURCES", font=42, bg="lightgrey"
        )
        self.resources_header.grid(
            row=3, column=1, columnspan=2, pady=20, padx=10, sticky="w"
        )

        # left label
        # get from db and map over
        self.resources_label = tk.Label(
            master=self.resources_container, text="Resource 1:", font=24, bg="lightgrey"
        )
        self.resources_label.grid(row=4, column=1, sticky="w", pady=10, padx=10)

        # right info
        self.resources_info = tk.Label(
            master=self.resources_container, text="Placeholder", font=16, bg="lightgrey"
        )
        self.resources_info.grid(row=4, column=2, sticky="w", pady=10, padx=10)

        # button
        self.send_message_button = tk.Button(
            master=self.top_container,
            text="MESSAGE ADMIN",
            command=self.handle_send_message,
            bg="red",
            fg="white",
        )
        self.send_message_button.grid(row=0, column=2, padx=30, pady=20, sticky="ne")
