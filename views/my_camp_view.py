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


class MyCampView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()

    # message button function
    # TO DO: add actual links
    def handle_send_message(self):
        self.master.switch_to_view("new_msg")
        return

    # Edit refugee button
    # TO DO: add actual links
    def handle_edit_click(self, refugee_id: int):
        # Add refugee id to global state for edit view
        current_global_state = self.master.get_global_state()
        current_global_state["refugee_id_to_edit"] = refugee_id
        self.master.set_global_state(current_global_state)

        self.master.switch_to_view("add_edit_refugee")

    # View refugee profile function
    # TO DO: add actual links
    def handle_view_click(self, refugee_id: int):
        current_global_state = self.master.get_global_state()
        current_global_state["refugee_id_to_edit"] = refugee_id
        self.master.set_global_state(current_global_state)

        self.master.switch_to_view("refugee_profile")

    # redirect to departed refugee list view
    def handle_view_departed_click(self):
        self.master.switch_to_view("departed_refugee_list")

    # add refugees function
    # TO DO: add actual links
    def _handle_add_refugee_click(self, refugee_id: int):
        # Clean EDIT PLAN global vars
        current_state = self.master.get_global_state()
        current_state.pop("refugee_id_to_edit", None)
        self.master.set_global_state(current_state)

        self.master.switch_to_view("add_edit_refugee")

    # check if admin for access control
    def is_volunteer(self):
        volunteer_id = int({self.master.get_global_state().get("is_admin")}.pop())
        if volunteer_id == 1:
            return False
        else:
            return True

    # get and set camp id
    def get_camp_id(self):
        volunteer_id = int({self.master.get_global_state().get("user_id")}.pop())
        camp_query = run_query_get_rows(
            f"SELECT camp_id FROM User WHERE id = '{volunteer_id}'"
        )
        camp_id = camp_query[0]["camp_id"]
        current_global_state = self.master.get_global_state()
        current_global_state["camp_id"] = camp_id
        self.master.set_global_state(current_global_state)

    # query all volunteers in the camp
    def get_volunteers(self) -> list[dict]:
        # get volunteer ID to get camp id from db
        camp_id = int({self.master.get_global_state().get("camp_id")}.pop())

        # get all volunteers in the camp
        return run_query_get_rows(
            f"SELECT * FROM User WHERE camp_id = '{camp_id}' AND is_admin = '0'"
        )

    # calculate volunteers age
    def get_age(self, dob_str):
        current_date = datetime.now()
        dob = datetime.strptime(dob_str, "%Y-%m-%d %H:%M:%S")
        age = (
            current_date.year
            - dob.year
            - ((current_date.month, current_date.day) < (dob.month, dob.day))
        )
        return age

    # query all refugees in the camp
    def get_refugees(self) -> list[dict]:
        camp_id = int({self.master.get_global_state().get("camp_id")}.pop())
        return run_query_get_rows(
            # ????? QUESTION - DO WE DISPLAY THOSE WHO ARE NOT IN CAMP AS WELL???
            f"SELECT * FROM RefugeeFamily WHERE camp_id = {camp_id} AND is_in_camp=1"
        )

    # query general info for the camp - top bit
    def get_camp_info(self) -> list[dict]:
        camp_id = int({self.master.get_global_state().get("camp_id")}.pop())
        result = run_query_get_rows(
            f"SELECT name, location, maxCapacity FROM Camp WHERE id='{camp_id}'"
        )
        return result[0]

    # query resources for the camp
    def get_camp_resources(self) -> list[dict]:
        camp_id = int({self.master.get_global_state().get("camp_id")}.pop())
        resources_result = run_query_get_rows(
            f"SELECT name, amount FROM CampResources WHERE camp_id='{camp_id}'"
        )
        return resources_result

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # set camp_id into state to retireve for queries in later functions
        self.get_camp_id()

        # get camp info to display from the db
        camp_info = self.get_camp_info()

        # get resources details from db
        camp_resources = self.get_camp_resources()

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

        self.top_container = tk.Frame(
            master=self.container,
            width=700,
            height=600,
        )
        self.top_container.grid(row=1, column=0, padx=50, pady=20, sticky="nsew")

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
            master=self.info_container,
            text=camp_info["location"],
            font=24,
            bg="lightgrey",
        )
        self.location_info.grid(row=4, column=1, sticky="w", pady=10, padx=10)

        self.max_capacity_info = tk.Label(
            master=self.info_container,
            text=camp_info["maxCapacity"],
            font=24,
            bg="lightgrey",
        )
        self.max_capacity_info.grid(row=5, column=1, sticky="w", pady=10, padx=10)

        # resources container
        self.resources_container = tk.Frame(
            master=self.top_container, width=300, bg="lightgrey"
        )
        self.resources_container.grid(row=0, column=1, padx=30, pady=10, sticky="nsew")

        # header span 2 columns
        self.resources_header = tk.Label(
            master=self.resources_container, text="RESOURCES", font=42, bg="lightgrey"
        )
        self.resources_header.grid(
            row=3, column=1, columnspan=2, pady=20, padx=10, sticky="w"
        )

        self.resources_num_container = tk.Frame(
            master=self.resources_container, width=300, height=700, bg="lightgrey"
        )
        self.resources_num_container.grid(row=4, column=1, pady=5, padx=10, sticky="w")

        # map through the resources to create a lable with values
        row_number = 4
        for resource in camp_resources:
            # left label
            # get from db and map over
            self.resources_label = tk.Label(
                master=self.resources_num_container,
                text=resource["name"],
                font=14,
                bg="lightgrey",
            )
            self.resources_label.grid(
                row=row_number, column=1, sticky="w", pady=2, padx=10
            )

            # right info
            self.resources_info = tk.Label(
                master=self.resources_num_container,
                text=resource["amount"],
                font=14,
                bg="lightgrey",
            )
            self.resources_info.grid(
                row=row_number, column=2, sticky="w", pady=2, padx=10
            )
            row_number += 1

        # if volunteer - show message button, if not - hide
        if self.is_volunteer():
            # button
            self.send_message_button = tk.Button(
                master=self.top_container,
                text="MESSAGE ADMIN",
                command=self.handle_send_message,
                bg="red",
                fg="white",
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

        self.all_volunteers_container = tk.Frame(
            master=self.container,
        )
        self.all_volunteers_container.grid(row=3, column=0, sticky="w")
        # table title
        self.volunteers_header = tk.Label(
            master=self.all_volunteers_container,
            text="VOLUNTEERS",
            font=42,
        )
        self.volunteers_header.grid(row=0, column=0, pady=5, sticky="w")

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

        self.all_refugees_container = tk.Frame(
            master=self.container,
        )
        self.all_refugees_container.grid(row=4, column=0, pady=10, sticky="w")

        # table title
        self.refugees_header = tk.Label(
            master=self.all_refugees_container,
            text="REFUGEE FAMILIES",
            font=42,
        )
        self.refugees_header.grid(row=0, column=0, pady=5, sticky="w")

        # View refugees who left the camp button
        self.add_refugee_button = tk.Button(
            master=self.all_refugees_container,
            text="View Departed Refugees",
            command=self.handle_view_departed_click,
            bg="blue",
        )
        self.add_refugee_button.grid(row=0, column=1, pady=5, padx=10, sticky="e")

        # Add refugee button
        self.add_refugee_button = tk.Button(
            master=self.all_refugees_container,
            text="+ Add Regugee Family",
            command=self._handle_add_refugee_click,
            bg="green",
        )
        self.add_refugee_button.grid(row=0, column=2, pady=5, sticky="e")

        # MAKE THE TABLE SCROLLABLE
        # canvas container
        self.refugee_table_canvas = tk.Canvas(
            master=self.all_refugees_container, width=1150, height=200
        )
        self.refugee_table_canvas.grid(row=1, column=0, sticky="nsew", columnspan=2)

        # table
        self.table_container = tk.Frame(
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
        container: tk.Frame,
        items: list[str],
        column_width=15,
        header=False,
        is_refugee_table=False,
    ) -> None:
        self.row_container = tk.Frame(
            master=container,
        )
        self.row_container.grid(row=container.grid_size()[1], sticky="w")

        # Add more space for col width
        column_width += 10

        for ix, label in enumerate(items):
            self.cell_frame = tk.Frame(
                master=self.row_container,
                width=200,
                height=25,
            )
            self.cell_frame.grid(row=0, column=ix, pady=5)
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

        # Add edit buttons
        if not header and is_refugee_table:
            # edit btn
            self.edit_refugees_btn = tk.Button(
                master=self.row_container,
                text="EDIT",
                command=lambda: self.handle_edit_click(items[0]),
                width=column_width - 3,
                bg="grey",
            )
            self.edit_refugees_btn.grid(row=0, column=len(items) + 1, padx=5)

            # view btn
            self.edit_refugees_btn = tk.Button(
                master=self.row_container,
                text="VIEW",
                command=lambda: self.handle_view_click(items[0]),
                width=column_width - 3,
                bg="lightblue",
            )
            self.edit_refugees_btn.grid(row=0, column=len(items) + 2, padx=5)
