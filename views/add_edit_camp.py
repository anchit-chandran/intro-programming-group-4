"""TEMPLATE FILE FOR MAKING NEW VIEW"""
# Python imports
import tkinter as tk

# Project imports
from views.base import BaseView
from constants import config
from utilities.db import run_query_get_rows
from utilities.formatting import add_border, calculate_max_col_width
from .base import BaseView


class AddEditCampView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()
        # message button function

    def handle_send_message(self):
        # self.master.switch_to_view("add_message")
        return

    def get_volunteers(self) -> list[dict]:
        return run_query_get_rows(
            "SELECT * FROM User WHERE camp_id = 1 AND is_admin = 0"
        )

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
            width=config.SCREEN_WIDTH,
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
        self.header.pack(
            side="left",
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

        # ------------------------ Volunteers list ------------------------------
        self.render_camp_volunteers()

    def render_camp_volunteers(self) -> None:
        self.all_volunteers = self.get_volunteers()

        # headers list
        self.header_cols = [
            "Id",
            "First Name",
            "Last Name",
            "Phone number",
            "Age",
            "Languages",
        ]
        self.data_to_render = [self.header_cols]

        for volunteer in self.all_volunteers:
            data_to_add = []
            data_to_add.append(volunteer["id"])
            data_to_add.append(volunteer["first_name"])
            data_to_add.append(volunteer["last_name"])
            data_to_add.append(volunteer["phone_number"])

            # TO DO: change to age instead of DOB
            data_to_add.append(volunteer["dob"])

            # TO DO: create a list and iterate through it to display in a column?
            data_to_add.append(volunteer["languages_spoken"])

            # TO DO: filter out the logged in volunteer?

            self.data_to_render.append(data_to_add)

        self.all_volunteers_container = tk.Frame(
            master=self.container,
        )
        self.all_volunteers_container.grid(row=3, column=0)
        # table title
        self.volunteers_header_header = tk.Label(
            master=self.all_volunteers_container,
            text="VOLUNTEERS",
            font=42,
        )
        self.volunteers_header_header.grid(row=0, column=0, pady=5, sticky="w")

        # table
        self.table_container = tk.Frame(
            master=self.all_volunteers_container,
        )
        self.table_container.grid(row=1, column=0)

        # Find the max col width
        self.max_col_width = calculate_max_col_width(self.data_to_render)

        for ix, row in enumerate(self.data_to_render):
            self._render_row(
                container=self.table_container,
                items=row,
                column_width=self.max_col_width,
                header=ix == 0,  # True if first row, else False
            )

    def _render_row(
        self,
        container: tk.Frame,
        items: list[str],
        column_width=15,
        header=False,
    ) -> None:
        self.row_container = tk.Frame(
            master=container,
        )
        self.row_container.pack()

        # Add more space for col width
        column_width += 10

        for ix, label in enumerate(items):
            self.cell_frame = tk.Frame(
                master=self.row_container,
                width=200,
                height=25,
            )
            self.cell_frame.grid(
                row=0,
                column=ix,
            )
            add_border(self.cell_frame)

            self.cell_content = tk.Label(
                master=self.cell_frame,
                text=label,
                width=column_width,
                background="black" if header else None,
                fg="white" if header else "black",
            )

            self.cell_content.pack(
                fill="both",
                expand=True,
            )
