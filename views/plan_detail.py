# Python imports
import logging
import tkinter as tk
from tkinter import ttk

# Project imports
from constants import config, instructions
from utilities.db import run_query_get_rows
from utilities.formatting import add_border
from .base import BaseView


class PlanDetailView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.plan_id = self.master.get_global_state().get("plan_id_to_view")
        if not self.plan_id:
            logging.error("No plan id in global state!")
            raise ValueError("No plan id in global state")

        # Get all plan details
        self.get_plan_details()

        self.render_widgets()

        self.update()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
        )
        self.container.pack(
            fill="both",
        )

        # Instructions label
        self.instructions_container = ttk.LabelFrame(
            master=self.container,
            text="Instructions for Plan Detail View",
            width=300,
        )
        self.instructions_container.grid(row=0, column=0, sticky="n", padx=10)

        self.instructions_label = tk.Label(
            master=self.instructions_container,
            text=instructions.INSTRUCTIONS['plan_detail'],
            anchor="w",
            justify="left",
        )
        self.instructions_label.pack()

        # PLAN INFORMATION
        self.info_container = tk.Frame(
            master=self.container,
        )
        self.info_frame = tk.LabelFrame(
            master=self.info_container,
            text="Information",
            padx=10,
        )
        self.total_resources_frame = tk.LabelFrame(
            master=self.info_container,
            text="Total Plan Resources",
            padx=10,
        )

        # PLAN INFORMATION
        self.info_container.grid(
            row=1,
            column=0,
        )
        self.info_frame.pack(
            side="left",
        )
        self.render_plan_information(
            container=self.info_frame,
        )

        self.total_resources_frame.pack(
            side="top",
            padx=30,
        )
        self.render_total_resources(
            container=self.total_resources_frame,
        )


        self.all_camps_container = tk.Frame(
            master=self.container,
        )
        self.all_camps_container.grid(row=3, column=0, pady=5, columnspan=1)
        
        self.action_buttons = tk.Frame(
            master=self.all_camps_container,
        )
        self.action_buttons.pack(side='top')
        
        self.render_camp_action_buttons(container=self.action_buttons)
        self.render_all_camps(container=self.all_camps_container)

    def render_camp_action_buttons(self, container) -> None:
        self.add_camp_button = tk.Button(
            master=container,
            text="+ Add Camp",
            command=lambda: self._handle_add_camp_click(),
        )
        self.add_camp_button.pack(side="right", padx=30)

        self.selected_camp_actions_frame = tk.LabelFrame(
            container, text="Selected Camp Actions"
        )
        self.selected_camp_actions_frame.pack(side="left", padx=10)

        

        self.view_camp_button = tk.Button(
            master=self.selected_camp_actions_frame,
            text="🔍 View Camp",
            command=lambda: self._handle_selected_camp_actions_click("view"),
        )
        self.view_camp_button.pack(side="left", pady=5, padx=5)
        
        self.edit_camp_button = tk.Button(
            master=self.selected_camp_actions_frame,
            text="📝 Edit Camp",
            command=lambda: self._handle_selected_camp_actions_click("edit"),
        )
        self.edit_camp_button.pack(side="left", pady=5, padx=5)

        self.resources_camp_button = tk.Button(
            master=self.selected_camp_actions_frame,
            text="📝 Edit Resources for Camp",
            command=lambda: self._handle_selected_camp_actions_click("resources"),
        )
        self.resources_camp_button.pack(side="left", pady=5, padx=5)

    def _handle_add_camp_click(self) -> None:
        current_state = self.master.get_global_state()
        current_state["plan_id_for_camp"] = self.plan_id
        self.master.set_global_state(current_state)

        self.master.switch_to_view("add_edit_camp")

    def render_all_camps(self, container) -> None:
        self.all_camps = self.get_all_camps()

        self.data_to_render = []

        # Get data
        for camp in self.all_camps:
            data_to_add = self.get_data_to_render_from_camp(camp)
            self.data_to_render.append(data_to_add)
        logging.debug(f'{self.data_to_render=}')
        # Render resource string
        for item in self.data_to_render:
            resources = int(item[-1])
            if not resources:
                label = '❌'
            else:
                label = f"{resources} allocated"
            item[6] = label
                

        self.header_cols = [
            "ID",
            "Camp",
            "Location",
            "Current Capacity (n)",
            "Volunteers (n)",
            "Refugee Families (n)",
            "Resource Types (n)",
        ]

        # TODO: dynamically choose Rowheight mostly determined by n resources, each separated by \n

        self.render_tree_table(
            header_cols=self.header_cols,
            data=self.data_to_render,
            container=container,
            col_widths=[
                30,
                100,
                100,
                150,
                100,
                120,
                120,
            ],
            rowheight=75,
            max_rows=4,
        )

    def _handle_selected_camp_actions_click(self, action: str):
        camp_row = self.tree.focus()
        if not camp_row:
            self.render_error_popup_window(message="Please select a camp first!")
            return

        # Get selected row data
        camp_data = self.tree.item(camp_row, "values")
        camp_id = camp_data[0]
        if action == "edit":
            self._handle_edit_click(camp_id=camp_id)
        elif action == "view":
            self._handle_view_click(camp_id=camp_id)
        else:
            self._handle_edit_resources_click(camp_id=camp_id)

    def _handle_edit_resources_click(self, camp_id: int) -> None:
        current_state = self.master.get_global_state()
        current_state["camp_id_for_resources"] = camp_id
        self.master.set_global_state(current_state)

        self.master.switch_to_view("edit_resources")

    def _handle_edit_click(self, camp_id: int) -> None:
        current_state = self.master.get_global_state()
        current_state["camp_id_to_edit"] = camp_id
        self.master.set_global_state(current_state)

        self.master.switch_to_view("add_edit_camp")

    def _handle_view_click(self, camp_id: int) -> None:
        current_state = self.master.get_global_state()
        current_state["camp_id_to_view"] = camp_id
        self.master.set_global_state(current_state)

        self.master.switch_to_view("camp_detail")

    def get_data_to_render_from_camp(self, camp: dict) -> list:
        """Gets data to render from camp"""
        data_to_render = []

        data_to_render.append(camp["id"])

        # Get camp name
        data_to_render.append(camp["name"])

        # Get camp location
        data_to_render.append(camp["location"])

        # Get current capacity
        current_capacity = self.get_current_capacity_for_camp(camp)
        data_to_render.append(current_capacity)

        # Get volunteers
        volunteers = self.get_volunteers_for_camp(camp)
        data_to_render.append(volunteers)

        # Get refugee families
        refugee_families = self.get_refugee_familes_for_camp(camp)
        data_to_render.append(refugee_families)

        # Get resources
        resources = self.get_resources_for_camp(camp)
        data_to_render.append(resources)

        return data_to_render

    def get_resources_for_camp(self, camp: dict) -> list[tuple]:
        """Gets resources for camp in form [(resource_name, resource_amount)]"""
        resources = run_query_get_rows(
            f"""
            SELECT
                COUNT(name)
            FROM
                CampResources
            WHERE
                camp_id = '{camp["id"]}'
        """
        )
        return resources[0]['COUNT(name)']

    def get_refugee_familes_for_camp(self, camp: dict) -> int:
        """Gets refugee families for camp"""
        refugee_families = run_query_get_rows(
            f"""
            SELECT
                COUNT(*) as n_refugee_families
            FROM
                RefugeeFamily
            WHERE
                camp_id = '{camp["id"]}'
                AND is_in_camp = 1
        """
        )[0]["n_refugee_families"]

        return refugee_families

    def get_volunteers_for_camp(self, camp: dict) -> int:
        """Gets volunteers for camp"""
        volunteers = run_query_get_rows(
            f"""
            SELECT
                COUNT(*) as n_volunteers
            FROM
                User
            WHERE
                camp_id = '{camp["id"]}'
        """
        )[0]["n_volunteers"]

        return volunteers

    def get_current_capacity_for_camp(self, camp: dict) -> int:
        """Gets current capacity for camp"""
        max_capacity = camp["maxCapacity"]

        total_refugees = run_query_get_rows(
            f"""
            SELECT
                COUNT(*) as current_capacity
            FROM
                RefugeeFamily
            WHERE
                camp_id = '{camp["id"]}'
                AND is_in_camp = 1
        """
        )[0]["current_capacity"]

        current_capacity = max_capacity - total_refugees

        return f"{current_capacity} (MAX: {max_capacity})"

    def render_total_resources(self, container) -> None:
        """Renders total resources for this plan"""

        camp_resources = run_query_get_rows(
            f"""
            SELECT
                name, SUM(amount) as amount
            FROM
                CampResources
            WHERE
                id IN {self.camp_resource_ids}
            GROUP BY
                name
        """
        )

        labels = [resource["name"] for resource in camp_resources]
        values = [resource["amount"] for resource in camp_resources]

        for ix, label in enumerate(labels):
            tk.Label(
                master=container,
                text=label,
            ).grid(
                row=ix,
                column=0,
                sticky="w",
            )

            tk.Entry(
                master=container,
                state="disabled",
                width=8,
                textvariable=tk.StringVar(
                    value=values[ix],
                ),
            ).grid(
                row=ix,
                column=1,
                sticky="w",
            )

    def render_plan_information(self, container) -> None:
        """Renders all plan information with disabled entry boxes inside container"""
        labels = [
            "ID",
            "Title",
            "Description",
            "Location",
            "Start Date",
            "End Date",
            "Central Email",
            "Affected Estimate",
        ]
        values = [
            self.plan_id,
            self.plan_title,
            self.plan_description,
            self.plan_location,
            self.plan_start_date,
            self.plan_end_date,
            self.plan_central_email,
            self.affected_estimate,
        ]

        for ix, label in enumerate(labels):
            tk.Label(
                master=container,
                text=label,
            ).grid(
                row=ix,
                column=0,
                sticky="w",
            )

            # If end date is null, set to ongoing
            value = values[ix]
            if label == "End Date":
                value = value if value else "ONGOING"
            elif label == "Affected Estimate":
                value = value if value else "-"

            tk.Entry(
                master=container,
                state="disabled",
                width=50,
                textvariable=tk.StringVar(
                    value=value,
                ),
            ).grid(
                row=ix,
                column=1,
                sticky="w",
            )

    def get_plan_details(self) -> None:
        """Gets plan details from db"""

        plan_details = run_query_get_rows(
            f"""
            SELECT
                *
            FROM
                Plan
            WHERE
                id = '{self.plan_id}'
        """
        )[0]

        self.plan_title = plan_details["title"]
        self.plan_description = plan_details["description"]
        self.plan_location = plan_details["location"]
        self.plan_start_date = plan_details["start_date"]
        self.plan_end_date = plan_details["end_date"]
        self.plan_central_email = plan_details["central_email"]
        self.affected_estimate = plan_details["affected_estimate"]

        self.camp_ids = self.get_camp_ids()
        self.camp_resource_ids = self.get_all_camp_resource_ids()

    def get_all_camp_resource_ids(self) -> tuple:
        """Gets all camp resources for this plan"""

        camp_resources = run_query_get_rows(
            f"""
            SELECT
                *
            FROM
                CampResources
            WHERE
                camp_id IN {self.camp_ids}
        """
        )

        return tuple([camp_resource["id"] for camp_resource in camp_resources])

    def get_camp_ids(self) -> tuple:
        """Gets all camp ids for this plan"""

        camps = run_query_get_rows(
            f"""
            SELECT
                id
            FROM
                Camp
            WHERE
                plan_id = '{self.plan_id}'
        """
        )

        return tuple([camp["id"] for camp in camps])

    def get_all_camps(self) -> list:
        """Gets all camps for this plan"""

        camps = run_query_get_rows(
            f"""
            SELECT
                *
            FROM
                Camp
            WHERE
                plan_id = '{self.plan_id}'
        """
        )

        return camps
