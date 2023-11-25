"""TEMPLATE FILE FOR MAKING NEW VIEW"""
# Python imports
import tkinter as tk

# Project imports
# from constants import config
from utilities.db import run_query_get_rows
from utilities.formatting import add_border, calculate_max_col_width
from .base import BaseView


class AddEditCampView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()

    # message button function
    # TO DO: add actual functionality
    def handle_send_message(self):
        # self.master.switch_to_view("add_message")
        return

    # Edit refugee button
    def handle_edit_click(self, refugee_id: int):
        # Add refugee id to global state for edit view
        current_global_state = self.master.get_global_state()
        current_global_state["refugee_id_to_edit"] = refugee_id
        self.master.set_global_state(current_global_state)

        self.master.switch_to_view("add_edit_refugee")

    # View refugee profile function
    def handle_view_click(self, refugee_id: int):
        current_global_state = self.master.get_global_state()
        current_global_state["refugee_id_to_edit"] = refugee_id
        self.master.set_global_state(current_global_state)

        self.master.switch_to_view("add_edit_refugee")

    # add refugees function
    def _handle_add_refugee_click(self, refugee_id: int):
        # Clean EDIT PLAN global vars
        current_state = self.master.get_global_state()
        current_state.pop("refugee_id_to_edit", None)
        self.master.set_global_state(current_state)

        self.master.switch_to_view("add_edit_refugee")

    # query all volunteers in the camp
    def get_volunteers(self) -> list[dict]:
        # TO DO: get volunteer ID to get camp id from db
        volunteer_id = int({self.master.get_global_state().get("user_id")}.pop())
        camp_query = run_query_get_rows(
            f"SELECT camp_id FROM User WHERE id = '{volunteer_id}'"
        )
        camp_id = camp_query[0]["camp_id"]
        print(volunteer_id, camp_id)
        current_global_state = self.master.get_global_state()
        current_global_state["camp_id"] = camp_id
        self.master.set_global_state(current_global_state)

        return run_query_get_rows(
            f"SELECT * FROM User WHERE camp_id = '{camp_id}' AND is_admin = '0'"
        )

    # query all refugees in the camp
    def get_refugees(self) -> list[dict]:
        return run_query_get_rows(
            # ????? QUESTION - DO WE DISPLAY THOSE WHO ARE NOT IN CAMP AS WELL???
            # TO DO: change camp id to retrieved one
            "SELECT * FROM RefugeeFamily WHERE camp_id = 1 AND is_in_camp=1"
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
        volunteer_id = {self.master.get_global_state().get("user_id")}
        # TO DO: retrieve camp info from db and put instead of placeholder
        # TO DO: get resources list from db and map over them to display data
        # TO DO: edit handle_send_message to redirect correctly - look up
        # TO DO: make the container scrollable with Canva

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

            # TO DO: change to age instead of DOB
            data_to_add.append(volunteer["dob"])

            # TO DO: create a list and iterate through it to display in a column?
            data_to_add.append(volunteer["languages_spoken"])

            # TO DO: filter out the logged in volunteer?

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

        # Add refugee button
        self.add_refugee_button = tk.Button(
            master=self.all_refugees_container,
            text="+ Add Regugee Family",
            command=self._handle_add_refugee_click,
            bg="green",
        )
        self.add_refugee_button.grid(row=0, column=1, pady=5, sticky="e")

        # table
        self.table_container = tk.Frame(
            master=self.all_refugees_container,
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
                is_refugee_table=True,
            )

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
