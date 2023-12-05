# Python imports
import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import date

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from utilities.formatting import add_border, calculate_max_col_width
from utilities.sqlite3_date_formatter import get_date
from .base import BaseView


class AllPlansView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
            width=config.SCREEN_WIDTH,
            height=300,
        )
        self.container.pack(
            pady=10,
        )

        # Instructions label
        self.instructions_container = ttk.LabelFrame(
            master=self.container,
            text="Instructions for All Plans View",
        )
        self.instructions_container.pack()
        self.instructions_label = tk.Label(
            master=self.instructions_container,
            text="New plans can be added using the '+ Add Plan' button.\n\nPlans can be viewed or modified by first selecting the plan by clicking on it, then using the appropriate action button.\n\nIf a Plan is ended, using 'Toggle Plan Status' with a selected plan, further interaction with the Plan is disabled until it is restarted.\n\nNOTE: Refugee Family count excludes those registered but not currently in the camp.",
            anchor="w",
            justify="left",
        )
        self.instructions_label.pack()

        # Header
        self.header_container = tk.Frame(self.container)
        self.header_container.pack(pady=15, fill="x", expand=True)

        self.header = tk.Label(
            master=self.header_container,
            text=f"ALL PLANS",
            font=(60),
        )
        self.header.pack(
            side="left",
        )

        # Add plan button
        self.add_plan_button = tk.Button(
            master=self.header_container,
            text="+ Add Plan",
            command=self._handle_add_plan_click,
        )
        self.add_plan_button.pack(
            side="right",
        )
        
        # Selected plan action buttons
        self.selected_plan_action_buttons_container = tk.LabelFrame(
            master=self.header_container,
            text='Selected Plan Actions'
        )
        self.selected_plan_action_buttons_container.pack(side='top')

        self.edit_plan_button = tk.Button(
            master=self.selected_plan_action_buttons_container,
            text="📝 Edit Plan",
            command=self._handle_edit_click,
        )
        self.edit_plan_button.pack(
            side="right",
            pady=5,
            padx=5,
        )

        self.toggle_status_button = tk.Button(
            master=self.selected_plan_action_buttons_container,
            text="🔚 Toggle Status",
            command=self._handle_toggle_click,
        )
        self.toggle_status_button.pack(
            side="right",
            pady=5,
            padx=5,
            
        )

        self.view_plan_button = tk.Button(
            master=self.selected_plan_action_buttons_container,
            text="🔍 View",
            command=self._handle_view_click,
        )
        self.view_plan_button.pack(
            side="right",
            pady=5,
            padx=5,
        )

        self.render_all_plans()

    def render_all_plans(self) -> None:
        self.all_plans = self.get_plans()

        # Get the data as simple list[str]
        self.data_to_render = []
        for plan in self.all_plans:
            data_to_add = []
            data_to_add.append(plan["id"])
            data_to_add.append(plan["title"])
            data_to_add.append(plan["location"])
            data_to_add.append(get_date(plan["start_date"]))

            # End date
            end_date = plan["end_date"]
            if end_date is None:
                data_to_add.append("Ongoing")
            else:
                data_to_add.append(get_date(plan["end_date"]))

            # Find total camps
            total_camps = self._calculate_total_camps_per_plan(plan["id"]).get(
                "COUNT(*)"
            )
            data_to_add.append(total_camps)

            # Find total volunteers
            total_volunteers = self._calculate_total_volunteers_per_plan(plan["id"])
            data_to_add.append(total_volunteers)

            # Find total refugees
            total_refugee_familes = self._calculate_total_refugee_families_per_plan(
                plan["id"]
            )
            data_to_add.append(total_refugee_familes)

            self.data_to_render.append(data_to_add)

        self.header_cols = [
            "ID",
            "Plan",
            "Location",
            "Start Date",
            "End Date",
            "Camps (n)",
            "Volunteers (n)",
            "Refugee Familes (n)",
        ]

        self.all_plans_container = tk.Frame(
            master=self.container,
        )
        self.all_plans_container.pack()

        self.render_tree_table(
            header_cols=self.header_cols,
            data=self.data_to_render,
            container=self.all_plans_container,
        )

    def get_plans(self) -> list[dict]:
        return run_query_get_rows("SELECT * FROM Plan")

    def _handle_view_click(self):
        plan_row = self.tree.focus()
        if plan_row:
            plan_data = self.tree.item(plan_row, "values")
            plan_id = plan_data[0]
            if self._check_plan_ended(plan_id=plan_id):
                self.render_error_popup_window(message="Plan has ended! Please re-open the Plan to go further.")
                return
            current_global_state = self.master.get_global_state()
            current_global_state["plan_id_to_view"] = plan_id
            self.master.set_global_state(current_global_state)

            self.master.switch_to_view("plan_detail")
        else:
            self.render_error_popup_window(message="Please select a plan to view!")

    def _handle_add_plan_click(self):
        # Clean EDIT PLAN global vars
        current_state = self.master.get_global_state()
        current_state.pop("plan_id_to_edit", None)
        self.master.set_global_state(current_state)

        self.master.switch_to_view("add_edit_plan")

    def _handle_toggle_click(self):
        plan_row = self.tree.focus()
        if not plan_row:
            self.render_error_popup_window(
                message="Please select a plan to toggle status!"
            )
            return

        plan_data = self.tree.item(plan_row, "values")
        plan_id = plan_data[0]
        plan_end_date = run_query_get_rows(f"SELECT end_date FROM Plan WHERE id={plan_id}")[0]['end_date']

        confirm_msg = f'Are you sure you want to {"end" if plan_end_date is None else "restart"} this plan?'
        user_input = messagebox.askyesno("Toggle Plan Status", confirm_msg)
        
        if not user_input:
            return

        # set enddate to today
        logging.debug(f'{plan_end_date=}')
        if plan_end_date is None:
            today = date.today()
            run_query_get_rows(
                f"""UPDATE Plan
                                        SET
                                            end_date = '{today}'
                                        WHERE
                                            id = {plan_id}"""
            )
        # Restart plan
        else:
            run_query_get_rows(
                f"""UPDATE Plan
                                        SET
                                            end_date = NULL
                                        WHERE
                                            id = {plan_id}"""
            )
        
        self.master.refresh_view()

    def _check_plan_ended(self, plan_id:int)->bool:
        plan_end_date = run_query_get_rows(f"SELECT end_date FROM Plan WHERE id={plan_id}")[0]['end_date']
        logging.debug(f"{plan_end_date=}")
        return bool(plan_end_date)
        
    
    def _handle_edit_click(self):
        plan_row = self.tree.focus()
        if plan_row:

            plan_data = self.tree.item(plan_row, "values")
            plan_id = plan_data[0]
            
            if self._check_plan_ended(plan_id=plan_id):
                self.render_error_popup_window(message="Plan has ended! Please re-open the Plan to go further.")
                return
            
            current_global_state = self.master.get_global_state()
            current_global_state["plan_id_to_edit"] = plan_id
            self.master.set_global_state(current_global_state)

            self.master.switch_to_view("add_edit_plan")
        else:
            self.render_error_popup_window(message="Please select a plan to edit!")

    def _calculate_total_camps_per_plan(self, plan_id: int) -> int:
        """Calculates the total number of camps for plan"""

        return run_query_get_rows(
            f"SELECT COUNT(*) FROM Camp WHERE plan_id = {plan_id}"
        )[0]

    def _calculate_total_volunteers_per_plan(self, plan_id: int) -> int:
        """Calculates the total number of volunteers for plan"""
        camp_ids = tuple(
            [
                camp["id"]
                for camp in run_query_get_rows(
                    f"SELECT DISTINCT(id) FROM Camp WHERE plan_id = {plan_id}"
                )
            ]
        )

        n_volunteers = run_query_get_rows(
            f"SELECT COUNT(*) AS n_users FROM User WHERE camp_id IN {camp_ids}"
        )[0].get("n_users")

        return n_volunteers

    def _calculate_total_refugee_families_per_plan(self, plan_id: int) -> int:
        """Calculates the total number of volunteers for plan"""
        camp_ids = tuple(
            [
                camp["id"]
                for camp in run_query_get_rows(
                    f"SELECT DISTINCT(id) FROM Camp WHERE plan_id = {plan_id}"
                )
            ]
        )

        n_refugees = run_query_get_rows(
            f"SELECT COUNT(*) AS n_families FROM RefugeeFamily WHERE camp_id IN {camp_ids} AND is_in_camp = 1"
        )[0].get("n_families")

        return n_refugees
