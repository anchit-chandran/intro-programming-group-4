import logging
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Project imports
# from constants import config
from utilities.db import run_query_get_rows
from utilities.formatting import add_border, calculate_max_col_width
from .base import BaseView
from constants import config


class DepartedRefugeesView(BaseView):
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
            fill="both",
            padx=30,
            pady=100,
        )

        # Header
        self.header_container = tk.Frame(self.container)
        self.header_container.pack(pady=15, fill="x", expand=True)

        self.header = tk.Label(
            master=self.header_container,
            text=f"TEMPLATE",
            font=(60),
        )
        self.header.pack(
            side="left",
        )

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
