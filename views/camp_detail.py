# Python imports
import logging
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Project imports
# from constants import config
from utilities.db import run_query_get_rows
from utilities.formatting import add_border, calculate_max_col_width
from .base import BaseView

# Project imports
from views.base import BaseView
from constants import config


class CampDetailView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()

    def handle_send_message(self):
        """navigates to new message form view"""
        self.master.switch_to_view("new_msg")
        return

    # TO DO: add actual links
    def handle_edit_click(self, refugee_id: int):
        """Navigates to edit refugee from view"""
        current_global_state = self.master.get_global_state()
        current_global_state["refugee_id_to_edit"] = refugee_id
        self.master.set_global_state(current_global_state)
        # self.master.switch_to_view("add_edit_refugee")
        return

    # TO DO: add actual links
    def handle_view_click(self, refugee_id: int):
        """navigates to refugee profile view"""
        current_global_state = self.master.get_global_state()
        current_global_state["refugee_id_to_edit"] = refugee_id
        self.master.set_global_state(current_global_state)
        # self.master.switch_to_view("refugee_profile")
        return

    # to do: add actual link
    def handle_view_departed_click(self):
        """navigates to departed refugee list view"""
        # self.master.switch_to_view("departed_refugee_list")
        return

    # TO DO: add actual links
    def _handle_add_refugee_click(self):
        """navigates to add refugee form view"""
        current_state = self.master.get_global_state()
        current_state.pop("refugee_id_to_edit", None)
        self.master.set_global_state(current_state)
        # self.master.switch_to_view("add_edit_refugee")
        return

    def is_volunteer(self):
        """checks if the user is admin for access control"""
        is_volunteer = int({self.master.get_global_state().get("is_admin")}.pop())
        if is_volunteer == 1:
            return False
        else:
            return True

    def get_camp_id(self):
        """gets camp id from state"""
        camp_id = {self.master.get_global_state().get("camp_id_to_view")}.pop()
        return camp_id

    def get_volunteers(self) -> list[dict]:
        """queries all volunteers in the camp"""
        camp_id = self.get_camp_id()
        return run_query_get_rows(
            f"SELECT * FROM User WHERE camp_id = '{camp_id}' AND is_admin = '0'"
        )

    def get_age(self, dob_str):
        """calculates volunteers age"""
        current_date = datetime.now()
        dob = datetime.strptime(dob_str, "%Y-%m-%d %H:%M:%S")
        age = (
            current_date.year
            - dob.year
            - ((current_date.month, current_date.day) < (dob.month, dob.day))
        )
        return age

    def get_refugees(self) -> list[dict]:
        """queries all refugees in the camp"""
        camp_id = self.get_camp_id()
        return run_query_get_rows(
            f"SELECT * FROM RefugeeFamily WHERE camp_id = {camp_id} AND is_in_camp=1"
        )

    def get_camp_info(self) -> list[dict]:
        """queries general info for the camp - top bit"""
        camp_id = self.get_camp_id()
        result = run_query_get_rows(
            f"SELECT name, location, maxCapacity FROM Camp WHERE id='{camp_id}'"
        )
        return result[0]

    def get_camp_resources(self) -> list[dict]:
        """queries resources for the camp"""
        camp_id = self.get_camp_id()
        resources_result = run_query_get_rows(
            f"SELECT name, amount FROM CampResources WHERE camp_id='{camp_id}'"
        )
        return resources_result

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # get camp info to display from the db
        camp_info = self.get_camp_info()

        # get resources details from db
        camp_resources = self.get_camp_resources()

        # Create container
        self.container = ttk.Frame(
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
        self.header_container = ttk.Frame(
            master=self.container,
            width=500,
            height=100,
        )
        self.header_container.grid(
            row=0,
            column=0,
        )

        self.header = ttk.Label(
            master=self.header_container,
            text=f"WELLCOME {self.master.get_global_state().get('username')}! 👋",
            font=(60),
        )
        self.header.grid(
            row=0,
            column=0,
        )

        # ------------------------ Top container------------------------------

        self.top_container = ttk.Frame(
            master=self.container,
            width=700,
            height=600,
        )
        self.top_container.grid(row=1, column=0, padx=50, pady=20, sticky="nsew")

        # info container
        self.info_container = ttk.LabelFrame(
            master=self.top_container,
            text="INFORMATION",
            width=300,
            height=600,
        )
        self.info_container.grid(row=0, column=0, padx=30, pady=20, sticky="nsew")

        # left label
        self.location_label = ttk.Label(
            master=self.info_container,
            text="Location:",
        )
        self.location_label.grid(row=4, column=0, sticky="w", pady=10, padx=10)

        self.max_capacity_label = ttk.Label(
            master=self.info_container,
            text="Max Capacity:",
        )
        self.max_capacity_label.grid(row=5, column=0, sticky="w", pady=10, padx=10)

        # right info
        self.location_info = tk.Entry(
            master=self.info_container,
            state="disabled",
            textvariable=tk.StringVar(value=camp_info["location"]),
        )
        self.location_info.grid(row=4, column=1, sticky="w", pady=10, padx=10)

        self.max_capacity_info = tk.Entry(
            master=self.info_container,
            state="disabled",
            textvariable=tk.StringVar(value=camp_info["maxCapacity"]),
        )
        self.max_capacity_info.grid(row=5, column=1, sticky="w", pady=10, padx=10)

        # resources container
        self.resources_container = ttk.LabelFrame(
            master=self.top_container,
            text="RESOURCES",
            width=300,
        )
        self.resources_container.grid(row=0, column=1, padx=30, pady=10, sticky="n")

        self.resources_num_container = ttk.Frame(
            master=self.resources_container,
            width=300,
            height=700,
        )
        self.resources_num_container.grid(row=4, column=1, pady=5, padx=10, sticky="w")

        # map through the resources to create a lable with values
        row_number = 4
        for resource in camp_resources:
            # left label
            # get from db and map over
            self.resources_label = ttk.Label(
                master=self.resources_num_container,
                text=f"{resource['name']}: ",
            )
            self.resources_label.grid(
                row=row_number, column=1, sticky="w", pady=2, padx=10
            )

            # right info
            self.resources_info = tk.Entry(
                master=self.resources_num_container,
                state="disabled",
                textvariable=tk.IntVar(value=resource["amount"]),
            )
            self.resources_info.grid(
                row=row_number, column=2, sticky="w", pady=2, padx=10
            )
            row_number += 1

        # if volunteer - show message button, if not - hide
        if self.is_volunteer():
            # button
            self.send_message_button = ttk.Button(
                master=self.top_container,
                text="MESSAGE ADMIN",
                command=self.handle_send_message,
            )
            self.send_message_button.grid(
                row=0, column=2, padx=30, pady=20, sticky="ne"
            )

        # render tables
        self.render_camp_volunteers()
        self.render_camp_refugees()

    # ------------------------ Volunteers list ------------------------------
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

            volunteer_age = self.get_age(volunteer["dob"])
            data_to_add.append(volunteer_age)

            data_to_add.append(volunteer["languages_spoken"])

            self.data_to_render.append(data_to_add)

        self.all_volunteers_container = ttk.Frame(
            master=self.container,
        )
        self.all_volunteers_container.grid(row=3, column=0, sticky="w")
        # table title
        self.volunteers_header = ttk.Label(
            master=self.all_volunteers_container,
            text="VOLUNTEERS",
            font=42,
        )
        self.volunteers_header.grid(row=0, column=0, pady=5, sticky="w")

        # table
        self.table_container = ttk.Frame(
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

    # ------------------------ Refugees list ------------------------------
    def render_camp_refugees(self) -> None:
        self.all_refugees = self.get_refugees()

        # headers list
        self.header_cols = [
            "Id",
            "Representative Name",
            "Medical Conditions",
            "Adults",
            "Children",
            "Missing members",
        ]
        self.data_to_render = [self.header_cols]

        for refugee in self.all_refugees:
            data_to_add = []
            data_to_add.append(refugee["id"])
            data_to_add.append(refugee["main_rep_name"])
            data_to_add.append(refugee["medical_conditions"])
            data_to_add.append(refugee["n_adults"])
            data_to_add.append(refugee["n_children"])
            data_to_add.append(refugee["n_missing_members"])

            self.data_to_render.append(data_to_add)

        self.all_refugees_container = ttk.Frame(
            master=self.container,
        )
        self.all_refugees_container.grid(row=4, column=0, pady=10, sticky="w")

        # table title
        self.refugees_header = ttk.Label(
            master=self.all_refugees_container,
            text="REFUGEE FAMILIES",
            font=42,
        )
        self.refugees_header.grid(row=0, column=0, pady=5, sticky="w")

        # View refugees who left the camp button
        self.add_refugee_button = ttk.Button(
            master=self.all_refugees_container,
            text="View Departed Refugees",
            command=self.handle_view_departed_click,
        )
        self.add_refugee_button.grid(row=0, column=1, pady=5, padx=10, sticky="e")

        # Add refugee button
        self.add_refugee_button = ttk.Button(
            master=self.all_refugees_container,
            text="+ Add Regugee Family",
            command=self._handle_add_refugee_click,
        )
        self.add_refugee_button.grid(row=0, column=2, pady=5, sticky="e")

        # MAKE THE TABLE SCROLLABLE
        # canvas container
        self.refugee_table_canvas = tk.Canvas(
            master=self.all_refugees_container, width=980, height=300
        )
        self.refugee_table_canvas.grid(row=1, column=0, sticky="nsew", columnspan=2)

        # table
        self.table_container = ttk.Frame(
            master=self.refugee_table_canvas,
        )
        self.table_container.grid(row=1, column=0)

        # create scrollable window
        self.refugee_table_canvas.create_window(
            (0, 0), window=self.table_container, anchor="nw"
        )

        # create scrollbar
        self.refugee_scrollbar = ttk.Scrollbar(
            master=self.all_refugees_container,
            orient="vertical",
            command=self.refugee_table_canvas.yview,
        )
        self.refugee_scrollbar.grid(row=1, column=2, sticky="ns")

        self.refugee_table_canvas.configure(yscrollcommand=self.refugee_scrollbar.set)

        # Find the max col width
        self.max_col_width = calculate_max_col_width(self.data_to_render)

        for ix, row in enumerate(self.data_to_render):
            self._render_row(
                container=self.table_container,
                items=row,
                column_width=self.max_col_width,
                header=ix == 0,  # True if first row, else False
                is_refugee_table=True,
            )

        # updating scroll area
        self.refugee_table_canvas.update_idletasks()  # to checck everything is rendered
        self.refugee_table_canvas.configure(
            scrollregion=self.refugee_table_canvas.bbox("all")
        )  # setting the area scrolled with all the items inside

    def _render_row(
        self,
        container: ttk.Frame,
        items: list[str],
        column_width=15,
        header=False,
        is_refugee_table=False,
    ) -> None:
        self.row_container = ttk.Frame(
            master=container,
        )
        self.row_container.grid(row=container.grid_size()[1], sticky="w")

        # Add more space for col width
        column_width += 10

        for ix, label in enumerate(items):
            self.cell_frame = ttk.Frame(
                master=self.row_container,
                width=200,
                height=25,
            )
            self.cell_frame.grid(row=0, column=ix, pady=5)
            add_border(self.cell_frame)

            self.cell_content = ttk.Label(
                master=self.cell_frame,
                text=label,
                width=column_width,
            )

            self.cell_content.pack(
                fill="both",
                expand=True,
            )

            # Add edit buttons
            if not header and is_refugee_table:
                # edit btn
                self.edit_refugees_btn = ttk.Button(
                    master=self.row_container,
                    text="EDIT",
                    command=lambda: self.handle_edit_click(items[0]),
                    width=column_width - 3,
                )
                self.edit_refugees_btn.grid(row=0, column=len(items) + 1, padx=5)

                # view btn
                self.edit_refugees_btn = ttk.Button(
                    master=self.row_container,
                    text="VIEW",
                    command=lambda: self.handle_view_click(items[0]),
                    width=column_width - 3,
                )
                self.edit_refugees_btn.grid(row=0, column=len(items) + 2, padx=5)
