# Python imports
import logging
import tkinter as tk

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from utilities.formatting import add_border
from .base import BaseView


class VolunteerDetailView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.volunteer_name = self.master.get_global_state().get("volunteer_name")
        if not self.volunteer_name:
            logging.error("No volunteer name in global state. Returning to all plans")
            raise ValueError("No volunteer name in global state")

        # Get all plan details
        self.get_volunteer_details()

        self.render_volunteer_widgets()

    def render_volunteer_widgets(self) -> None:
        self.volunteer_detail = self.get_volunteers()

        # Get the data as simple list[str], starting with col headers
        self.header_cols = [
            "ID",
            "Username",
            "Password"
            "Date of Birth"
            "First Name",
            "Last Name",
            "Sex",
            "Phone Number",
            "Camp Name",
            "Status",
            "Languages Spoken",
            "Skills",
            "Emergency Contact",
            "Emergency Contact Number"
        ]
        self.data_to_render = [self.header_cols]
        for volunteer in self.volunteer_detail:
            data_to_add = []
            data_to_add.append(volunteer["id"])
            data_to_add.append(volunteer["username"])
            data_to_add.append(volunteer["password"])
            data_to_add.append(volunteer["first_name"])
            data_to_add.append(volunteer["last_name"])
            data_to_add.append(volunteer["sex"])
            data_to_add.append(volunteer["phone_number"])
            data_to_add.append(volunteer["camp_id"])
            # status
            status = volunteer["is_active"]
            if status == 1:
                data_to_add.append("Active")
            else:
                data_to_add.append("Deactivated")

            data_to_add.append(volunteer["languages_spoken"])
            data_to_add.append(volunteer["skills"])
            data_to_add.append(volunteer["emergency_contact_name"])
            data_to_add.append(volunteer["emergency_contact_number"])

            self.data_to_render.append(data_to_add)

        self.volunteer_detail_container = tk.Frame(
            master=self.container,
        )
        self.volunteer_detail_container.pack()

        self.table_container = tk.Frame(
            master=self.volunteer_detail_container,
        )
        self.table_container.pack()

        # Find the max col width
        self.max_col_width = calculate_max_col_width(self.data_to_render)

        for ix, row in enumerate(self.data_to_render):
            self._render_row(
                container=self.table_container,
                items=row,
                column_width=self.max_col_width,
                header=ix == 0,  # True if first row, else False
            )

   