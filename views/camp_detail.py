# Python imports
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime

# Project imports
from views.base import BaseView
from constants import instructions
from utilities.db import run_query_get_rows
from utilities.formatting import add_border


class CampDetailView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.is_volunteer = not self.master.get_global_state().get("is_admin")
        self.render_widgets()
        self.update()

    

    def handle_view_departed_click(self):
        """navigates to departed refugee list view"""
        self.master.switch_to_view("departed_refugees")

    def _handle_add_refugee_click(self):
        """navigates to add refugee form view"""
        # get the max capacity and refugee number in the camp
        camp_id = self.get_camp_id()
        maxCapacity = run_query_get_rows(
            f"SELECT maxCapacity FROM Camp WHERE id='{camp_id}'"
        )[0]["maxCapacity"]

        n_refugees = len(
            run_query_get_rows(
                f"SELECT id FROM RefugeeFamily WHERE camp_id = {camp_id} AND is_in_camp=1"
            )
        )

        if n_refugees < maxCapacity:
            current_state = self.master.get_global_state()
            current_state.pop("refugee_id_to_edit", None)
            self.master.set_global_state(current_state)
            self.master.switch_to_view("add_edit_refugee")
        else:
            self.render_error_popup_window(
                message="The camp is at its max capacity. Cannot add more refugee families"
            )
            return

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
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
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

    def handle_back_button(self):
        current_state = self.master.get_global_state()
        current_state.pop("camp_id_to_view", None)
        self.master.set_global_state(current_state)
        self.master.switch_to_view("plan_detail")

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # get camp info to display from the db
        camp_info = self.get_camp_info()

        # get resources details from db
        camp_resources = self.get_camp_resources()

        # Create container
        self.container = tk.Frame(
            master=self,
        )
        self.container.pack(
        )

        # Header
        self.header_container = tk.Frame(
            master=self.container,
        )
        self.header_container.grid(
            row=0,
            column=0,
        )

        # if not volunteer show button
        if not self.is_volunteer:
            # back button
            self.go_back_button = ttk.Button(
                master=self.header_container,
                text="GO BACK TO PLAN",
                command=self.handle_back_button,
            )
            self.go_back_button.pack(side="top")

        self.header = ttk.Label(
            master=self.header_container,
            text=f"Camp Details",
            font=(60),
        )
        self.header.pack()

        # Instructions label
        self.instructions_container = ttk.LabelFrame(
            master=self.header_container,
            text="Instructions for Camp Detail",
        )
        self.instructions_container.pack(side="bottom")
        self.instructions_label = tk.Label(
            master=self.instructions_container,
            text=instructions.INSTRUCTIONS['camp_detail'],
            anchor="w",
            justify="left",
            wraplength=1000,
        )
        self.instructions_label.pack()

        # ------------------------ Top container------------------------------

        self.top_container = tk.Frame(
            master=self.container,
            width=700,
            height=600,
        )
        self.top_container.grid(row=1, column=0, padx=50, pady=20, sticky="nw")

        # info container
        self.info_container = tk.LabelFrame(
            master=self.top_container,
            text="Information",
            width=300,
            height=600,
        )
        self.info_container.grid(row=0, column=1, padx=30, sticky="nw")

        # left label
        self.location_label = ttk.Label(
            master=self.info_container,
            text="Camp name:",
        )
        self.location_label.grid(row=4, column=0, sticky="w", pady=10, padx=10)

        self.location_label = ttk.Label(
            master=self.info_container,
            text="Location:",
        )
        self.location_label.grid(row=5, column=0, sticky="w", pady=10, padx=10)

        self.max_capacity_label = ttk.Label(
            master=self.info_container,
            text="Max Capacity:",
        )
        self.max_capacity_label.grid(row=6, column=0, sticky="w", pady=10, padx=10)

        # right info
        self.location_info = tk.Entry(
            master=self.info_container,
            state="disabled",
            textvariable=tk.StringVar(value=camp_info["name"]),
        )
        self.location_info.grid(row=4, column=1, sticky="w", pady=10, padx=10)

        self.location_info = tk.Entry(
            master=self.info_container,
            state="disabled",
            textvariable=tk.StringVar(value=camp_info["location"]),
        )
        self.location_info.grid(row=5, column=1, sticky="w", pady=10, padx=10)

        self.max_capacity_info = tk.Entry(
            master=self.info_container,
            state="disabled",
            textvariable=tk.StringVar(value=camp_info["maxCapacity"]),
        )
        self.max_capacity_info.grid(row=6, column=1, sticky="w", pady=10, padx=10)

        # resources container
        self.resources_container = tk.LabelFrame(
            master=self.top_container,
            text="Resources",
            width=300,
        )
        self.resources_container.grid(row=0, column=2, padx=30, sticky="nw")

        self.resources_num_container = tk.Frame(
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
                textvariable=tk.StringVar(value=resource["amount"]),
            )
            self.resources_info.grid(
                row=row_number, column=2, sticky="w", pady=2, padx=10
            )
            row_number += 1

        # if volunteer - show edit buttons
        if self.is_volunteer:
            
            self.camp_action_buttons_container = tk.LabelFrame(
                master=self.top_container,
                text='Camp Actions'
            )
            self.camp_action_buttons_container.grid(row=0, column=3,  sticky="ne")
            
            self.edit_details_button = ttk.Button(
                master=self.camp_action_buttons_container,
                text="📝 Edit Details",
                command=self.handle_edit_click_volunteer,
            )
            self.edit_details_button.pack(side='top', padx=5, pady=5)


        # render tables
        self.render_camp_volunteers()
        self.render_camp_refugees()
    
    
    def handle_edit_click_volunteer(self):
    
        current_global_state = self.master.get_global_state()
        camp_id_to_view = current_global_state.pop('camp_id_to_view')
        plan_id_for_camp = run_query_get_rows(f"SELECT plan_id FROM Camp WHERE id={camp_id_to_view}")[0]['plan_id']
        
        current_global_state["camp_id_to_edit"] = camp_id_to_view
        current_global_state["plan_id_to_view"] = plan_id_for_camp
        self.master.set_global_state(current_global_state)
        self.master.switch_to_view("add_edit_camp")
        
        
    # ------------------------ Volunteers list ------------------------------
    def render_camp_volunteers(self) -> None:
        self.all_volunteers = self.get_volunteers()

        self.data_to_render = []

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
        self.volunteers_header = ttk.Label(
            master=self.all_volunteers_container,
            text="VOLUNTEERS",
            font=42,
        )
        self.volunteers_header.grid(row=0, column=0, pady=5, sticky="w")

        # table
        self.table_container = tk.Frame(
            master=self.all_volunteers_container,
        )
        self.table_container.grid(row=1, column=0, columnspan=2)

        # headers list
        self.header_cols = [
            "Id",
            "First Name",
            "Last Name",
            "Phone #",
            "Age",
            "Languages",
        ]
        self.render_tree_table(
            header_cols=self.header_cols,
            data=self.data_to_render,
            container=self.table_container,
            tree_name="volunteer_tree",
            col_widths=[
                50,
                100,
                100,
                100,
                50,
                200,
            ],
        )

    # ------------------------ Refugees list ------------------------------
    def render_camp_refugees(self) -> None:
        self.all_refugees = self.get_refugees()

        self.data_to_render = []

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
            width=1000,
        )
        self.all_refugees_container.grid(row=4, column=0, pady=10, sticky="w")

        # table title
        header_container = tk.Frame(
            master=self.all_refugees_container,
        )
        header_container.grid(row=0, column=0, pady=5, sticky="w")
        self.refugees_header = ttk.Label(
            master=header_container,
            text="REFUGEE FAMILIES",
            font=42,
        )
        self.refugees_header.pack(side="left")

        self.generic_action_buttons_container = tk.Frame(master=header_container)
        self.generic_action_buttons_container.pack()

        # View refugees who left the camp button
        self.add_refugee_button = ttk.Button(
            master=self.generic_action_buttons_container,
            text="View Departed Refugees",
            command=self.handle_view_departed_click,
        )
        self.add_refugee_button.pack(side="right")

        # Add refugee button
        self.add_refugee_button = ttk.Button(
            master=self.generic_action_buttons_container,
            text=" + Add Regugee Family",
            command=self._handle_add_refugee_click,
        )
        self.add_refugee_button.pack(side="right")

        # table
        table_container = tk.Frame(
            master=self.all_refugees_container,
        )
        table_container.grid(row=1, column=0)
        # Selected refugee action buttons
        self.render_selected_refugee_actions(container=table_container)

        # headers list
        self.header_cols = [
            "Id",
            "Main Rep Name",
            "Med Conditions",
            "Adults (n)",
            "Children (n)",
            "Missing members (n)",
        ]
        self.render_tree_table(
            header_cols=self.header_cols,
            data=self.data_to_render,
            container=table_container,
            tree_name="refugee_tree",
            col_widths=[
                50,
                150,
                150,
                150,
                150,
                150,
            ],
            rowheight=20,
        )

    def render_selected_refugee_actions(self, container) -> None:
        action_frame = tk.LabelFrame(
            master=container, text="Selected Refugee Family Actions"
        )
        action_frame.pack(side="right")

        self.view_refugee_button = ttk.Button(
            master=action_frame,
            text="👁️ View",
            command=lambda: self._handle_selected_refugee_actions_click("view"),
        )
        self.view_refugee_button.pack(side="left")

        self.edit_refugee_button = ttk.Button(
            master=action_frame,
            text="✏️ Edit",
            command=lambda: self._handle_selected_refugee_actions_click("edit"),
        )
        self.edit_refugee_button.pack(side="right")

    def _handle_selected_refugee_actions_click(self, action: str):
        refugee_row = self.refugee_tree.focus()
        if not refugee_row:
            self.render_error_popup_window(
                message="Please select a Refugee Family first!"
            )
            return

        # Get selected row data
        refugee_data = self.refugee_tree.item(refugee_row, "values")
        refugee_id = refugee_data[0]

        if action == "view":
            self.handle_view_click(refugee_id=refugee_id)
        elif action == "edit":
            self.handle_edit_click(refugee_id=refugee_id)

    def handle_edit_click(self, refugee_id: int):
        """Navigates to edit refugee from view"""
        
        
        
        current_global_state = self.master.get_global_state()
        current_global_state["refugee_id_to_edit"] = refugee_id
        self.master.set_global_state(current_global_state)
        self.master.switch_to_view("add_edit_refugee")

    def handle_view_click(self, refugee_id: int):
        """navigates to refugee profile view"""
        current_global_state = self.master.get_global_state()
        current_global_state["refugee_id_to_view"] = refugee_id
        self.master.set_global_state(current_global_state)
        self.master.switch_to_view("refugee_profile")