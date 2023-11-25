# Python imports
import logging
import tkinter as tk

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from .base import BaseView


class PlanDetailView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.plan_name = self.master.get_global_state().get("plan_name")

        # Get all plan details
        self.get_plan_details()

        self.render_widgets()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
            width=1000,
            height=300,
        )
        self.container.pack(
            fill="both",
            padx=10,
            pady=100,
        )

        self.header = tk.Label(
            master=self.container,
            text=f"Plan Detail: {self.plan_name}",
            font=(60),
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="w",
        )

        # PLAN INFORMATION
        self.info_container = tk.Frame(
            master=self.container,
            width=1000,
            height=300,
        )
        self.info_frame = tk.LabelFrame(
            master=self.info_container,
            text="Information",
        )
        self.total_resources_frame = tk.LabelFrame(
            master=self.info_container,
            text="Information",
        )

        # PLAN INFORMATION
        self.info_container.grid(
            row=1,
            column=0,
        )
        self.info_frame.pack(
            side="left",
            fill="both",
            pady=10,
        )
        self.render_plan_information(
            container=self.info_frame,
        )

        self.total_resources_frame.pack(
            side="top",
            padx=30,
            pady=10,
        )
        self.render_total_resources(
            container=self.total_resources_frame,
        )

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
        
        labels = [resource['name'] for resource in camp_resources]
        values = [resource['amount'] for resource in camp_resources]
        
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
