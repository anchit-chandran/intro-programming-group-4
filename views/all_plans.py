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
        self.header_container.pack()
        self.header = tk.Label(
            master=self.header_container,
            text=f"ALL PLANS VIEW",
            font=(60),
        )
        self.header.pack(side="left", fill="x")

        # Add plan
        self.add_plan_button = tk.Button(
            master=self.header_container,
            text="+ Add Plan",
        )
        self.add_plan_button.pack(side="right", fill="x")

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
        ]
        self.data_to_render = [self.header_cols]
        for plan in self.all_plans:
            data_to_add = []
            data_to_add.append(plan["title"])
            data_to_add.append(plan["location"])
            data_to_add.append(get_date(plan["start_datetime"]))
            data_to_add.append(plan["end_datetime"])

            # Find total camps
            data_to_add.append("CAMPS")
            # Find total volunteers
            data_to_add.append("VOL")
            # Find total refugees
            data_to_add.append("REFU")

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
                header=ix == 0, # True if first row, else False
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
        column_width += 6

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

            self.cell_label = tk.Label(
                master=self.cell_frame,
                text=label,
                width=column_width,
                background="black" if header else None,
            )
            self.cell_label.pack(
                fill="both",
                expand=True,
            )
