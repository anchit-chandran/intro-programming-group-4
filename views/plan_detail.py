# Python imports
import logging
import tkinter as tk

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from utilities.formatting import add_border
from .base import BaseView


class PlanDetailView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        self.plan_name = self.master.get_global_state().get("plan_name")
        if not self.plan_name:
            logging.error("No plan name in global state. Returning to all plans")
            self.master.switch_to_view("all_plans")

        # Get all plan details
        self.get_plan_details()

        self.render_widgets()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
            width=1200,
            height=300,
        )
        self.container.pack(
            fill="both",
            padx=10,
            pady=100,
        )
        
        self.header_label = tk.Label(
            master=self.container,
            text=f"DETAILS FOR {self.plan_name.upper()}",
            font=(60),
        )
        self.header_label.grid(row=0, column=0, columnspan=2)

        # PLAN INFORMATION
        self.info_container = tk.Frame(
            master=self.container,
            width=1000,
            height=300,
        )
        self.info_frame = tk.LabelFrame(
            master=self.info_container,
            text="Information",
            padx=10,
            pady=10,
        )
        self.total_resources_frame = tk.LabelFrame(
            master=self.info_container,
            text="Primary Resources",
            padx=10,
            pady=10,
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
            width=1200,
            height=300,
        )
        self.all_camps_container.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=40,
            
        )
        self.render_all_camps(container=self.all_camps_container)
    
    def render_all_camps(self, container) -> None:
        self.all_camps = self.get_all_camps()
        
        self.header_cols = [
            "Camp",
            "Location",
            "Current Capacity (n)",
            "Volunteers (n)",
            "Refugee Familes (n)",
            "Resources",
            "Actions",
        ]
        self.data_to_render = [self.header_cols]
        
        # Get data
        for camp in self.all_camps:
            data_to_add = self.get_data_to_render_from_camp(camp)
            self.data_to_render.append(data_to_add)
        
        # Render table
        for ix, row in enumerate(self.data_to_render):
            self._render_row(
                container=container,
                items=row,
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
            if not header: add_border(self.cell_frame)
            
            # Extra work to render resource col as it's in the form of [('Food', '100'), ('Water', '200'), ('Medicine', '300')]
            if ix == 5:
                column_width += 20 # MAKE RESOURCE COLUMN WIDER
                
                if not header: 
                    new_label = [f"{resource[0]}: {resource[1]}" for resource in label]
                    print(", ".join(new_label))
                    label = "\n".join(new_label)

            # Make action col thinner
            if ix == 6:
                column_width -= 25
                
            self.cell_content = tk.Label(
                master=self.cell_frame,
                text=label,
                width=column_width,
                height=5 if not header else 1,
            )

            self.cell_content.pack(
            )
        
        # Add action buttons
        if not header:
            BUTTON_WIDTH = (column_width - 30)
            
            self.buttons_frame = tk.Frame(
                master=self.row_container,
            )
            self.buttons_frame.grid(
                row=0,
                column=len(items),
                padx=5,
            )
            
            tk.Button(
                master=self.buttons_frame,
                text="Edit",
                width=BUTTON_WIDTH,
                command = lambda: self._handle_edit_click(items[0])
            ).pack(fill="both")
            tk.Button(
                master=self.buttons_frame,
                text="View",
                width=BUTTON_WIDTH,
                command = lambda: self._handle_view_click(items[0])
            ).pack(fill="both")
    
    def get_camp_id_from_name(self, camp_name:str) -> int:
        """Gets plan name from plan id"""
        camp_id = run_query_get_rows(
            f"""
            SELECT
                id
            FROM
                Camp
            WHERE
                name = '{camp_name}'
        """
        )[0]["id"]
        
        return camp_id
    
    def _handle_edit_click(self, camp_name:str) -> None:
        camp_id = self.get_camp_id_from_name(camp_name)
        
        current_state = self.master.get_global_state() 
        current_state['camp_id_to_edit'] = camp_id
        self.master.set_global_state(current_state)
        
        self.master.switch_to_view("add_edit_camp")
    
    def _handle_view_click(self, camp_name:str) -> None:
        camp_id = self.get_camp_id_from_name(camp_name)
        
        current_state = self.master.get_global_state() 
        current_state['camp_id_to_view'] = camp_id
        self.master.set_global_state(current_state)
        
        self.master.switch_to_view("camp_detail")
        
    def get_data_to_render_from_camp(self, camp:dict) -> list:
        """Gets data to render from camp"""
        data_to_render = []
        
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

    def get_resources_for_camp(self, camp:dict) -> list[tuple]:
        """Gets resources for camp in form [(resource_name, resource_amount)]"""
        resources = run_query_get_rows(
            f"""
            SELECT
                name, amount
            FROM
                CampResources
            WHERE
                camp_id = '{camp["id"]}'
        """
        )
        return [(resource["name"], resource["amount"]) for resource in resources]
    
    def get_refugee_familes_for_camp(self, camp:dict) -> int:
        """Gets refugee families for camp"""
        refugee_families = run_query_get_rows(
            f"""
            SELECT
                SUM(n_adults + n_children) AS n_refugee_families
            FROM
                RefugeeFamily
            WHERE
                camp_id = '{camp["id"]}'
                AND is_in_camp = 1
        """
        )[0]["n_refugee_families"]
        
        return refugee_families
    
    def get_volunteers_for_camp(self, camp:dict) -> int:
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
    
    def get_current_capacity_for_camp(self, camp:dict) -> int:
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
        """
        )[0]["current_capacity"]
        
        current_capacity = max_capacity - total_refugees
        
        return f"{current_capacity}\n(MAX: {max_capacity})"
    
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
                title = '{self.plan_name}'
        """
        )[0]

        self.plan_id = plan_details["id"]
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