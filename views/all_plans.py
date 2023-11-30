# Python imports
import logging
import tkinter as tk

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

        self.render_all_plans()

    def render_all_plans(self) -> None:
        self.all_plans = self.get_plans()

        # Get the data as simple list[str], starting with col headers
        self.header_cols = [
            "Plan",
            "Location",
            "Start Date",
            "End Date",
            "Camps (n)",
            "Volunteers (n)",
            "Refugee Familes (n)",
            "Edit",
        ]
        self.data_to_render = [self.header_cols]
        for plan in self.all_plans:
            data_to_add = []
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

        self.all_plans_container = tk.Frame(
            master=self.container,
        )
        self.all_plans_container.pack()

        self.table_container = tk.Frame(
            master=self.all_plans_container,
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

    def get_plans(self) -> list[dict]:
        return run_query_get_rows("SELECT * FROM Plan")

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

            # Get color
            if label == "Ongoing":
                fg = "green"
            else:
                fg = None

            self.cell_content = tk.Label(
                master=self.cell_frame,
                text=label,
                width=column_width,
                fg=fg,
            )

            self.cell_content.pack(
                fill="both",
                expand=True,
            )

            if not header:
                self.cell_content.bind("<Enter>", self._handle_mouse_hover_enter)
                self.cell_content.bind("<Leave>", self._handle_mouse_hover_exit)

        # Add action buttons
        if not header:
            BUTTON_WIDTH = (column_width - 6)//2
            tk.Button(
                master=self.row_container,
                text="Edit",
                command=lambda: self._handle_edit_click(items[0]),
                width=BUTTON_WIDTH
            ).grid(row=0, column=len(items))
            tk.Button(
                master=self.row_container,
                text="View",
                command=lambda: self._handle_view_click(items[0]),
                width=BUTTON_WIDTH
            ).grid(row=0, column=len(items)+1)

    def _handle_view_click(self, plan_name: str):
        
        # ADD TO STATE
        current_state = self.master.get_global_state()
        current_state["plan_name"] = plan_name
        self.master.set_global_state(current_state)
        
        # Change to view plan view
        self.master.switch_to_view("plan_detail")
        
    
    def _handle_mouse_hover_enter(self, event):
        event.widget.config(background=config.LIGHTGREY)

    def _handle_mouse_hover_exit(self, event):
        event.widget.config(background=self.master.cget("bg"))

    def _handle_add_plan_click(self):
        
        # Clean EDIT PLAN global vars
        current_state = self.master.get_global_state()
        current_state.pop("plan_name_to_edit", None)
        self.master.set_global_state(current_state)
        
        self.master.switch_to_view("add_edit_plan")

    def _handle_edit_click(self, plan_name: str):
        # Add plan name to global state for edit view
        current_global_state = self.master.get_global_state()
        current_global_state["plan_name_to_edit"] = plan_name
        self.master.set_global_state(current_global_state)

        self.master.switch_to_view("add_edit_plan")

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
            f"SELECT COUNT(*) AS n_volunteers FROM RefugeeFamily WHERE camp_id IN {camp_ids}"
        )[0].get("n_volunteers")

        return n_refugees
