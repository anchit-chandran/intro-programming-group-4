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

    def get_refugees(self) -> list[dict]:
        """queries all refugees in the camp"""
        camp_id = {self.master.get_global_state().get("camp_id_to_view")}.pop()
        return run_query_get_rows(
            f"SELECT * FROM RefugeeFamily WHERE camp_id = {camp_id} AND is_in_camp=0"
        )

    def get_camp_name(self):
        """retrieves camp name by camp id from db"""
        camp_id = {self.master.get_global_state().get("camp_id_to_view")}.pop()
        return run_query_get_rows(f"SELECT name FROM camp WHERE id = {camp_id}")[0][
            "name"
        ]

    def handle_view_click(self, refugee_id: int):
        """navigates to refugee profile view"""
        current_global_state = self.master.get_global_state()
        current_global_state["refugee_id_to_view"] = refugee_id
        self.master.set_global_state(current_global_state)
        self.master.switch_to_view("refugee_profile")

    def handle_edit_click(self, refugee_id: int):
        """Navigates to edit refugee from view"""
        current_global_state = self.master.get_global_state()
        current_global_state["refugee_id_to_edit"] = refugee_id
        self.master.set_global_state(current_global_state)
        self.master.switch_to_view("add_edit_refugee")

    def handle_back_button(self):
        self.master.switch_to_view("camp_detail")

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = ttk.Frame(
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
        self.header_container = ttk.Frame(
            master=self.container,
            width=500,
            height=100,
        )
        self.header_container.grid(
            row=0,
            column=0,
        )

        # back button
        self.send_message_button = ttk.Button(
            master=self.header_container,
            text="GO BACK TO PLAN",
            command=self.handle_back_button,
        )
        self.send_message_button.grid(
            row=0, column=0, padx=(0, 30), pady=20, sticky="ne"
        )

        camp_name = self.get_camp_name()
        print(camp_name)

        self.header = ttk.Label(
            master=self.header_container,
            text=f"Departed refugees from {camp_name}",
            font=(60),
        )
        self.header.grid(row=0, column=1, padx=(0, 30), pady=20, sticky="nw")

        self.render_camp_refugees()

    def render_camp_refugees(self) -> None:
        self.all_refugees = self.get_refugees()

        # headers list
        self.header_cols = [
            "Id",
            "Main Rep Name",
            "Med Conditions",
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
            width=1000,
        )
        self.all_refugees_container.grid(
            row=4, column=0, columnspan=10, pady=10, sticky="w"
        )

        # MAKE THE TABLE SCROLLABLE
        # canvas container
        self.refugee_table_canvas = tk.Canvas(
            master=self.all_refugees_container, width=1000, height=500
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
        self.refugee_scrollbar.grid(row=1, column=1, sticky="nse", padx=1)

        self.refugee_table_canvas.configure(yscrollcommand=self.refugee_scrollbar.set)

        # Find the max col width
        self.max_col_width = 15

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

        for ix, label in enumerate(items):
            column_width = 15
            self.cell_frame = ttk.Frame(
                master=self.row_container,
                width=300,
                height=25,
            )
            self.cell_frame.grid(row=0, column=ix, pady=5)
            add_border(self.cell_frame)

            # Decrease width for id column
            if ix == 0:
                column_width = 3

            # ADD SPACE FOR LANGUAGES FOR VOLUNTEERS
            if not is_refugee_table and ix == 5:
                column_width += 15

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
            BUTTON_WIDTH = 5
            # edit btn
            self.edit_refugees_btn = ttk.Button(
                master=self.row_container,
                text="EDIT",
                command=lambda: self.handle_edit_click(items[0]),
                width=BUTTON_WIDTH,
            )
            self.edit_refugees_btn.grid(row=0, column=len(items) + 1, padx=5)

            # view btn
            self.edit_refugees_btn = ttk.Button(
                master=self.row_container,
                text="VIEW",
                command=lambda: self.handle_view_click(items[0]),
                width=BUTTON_WIDTH,
            )
            self.edit_refugees_btn.grid(row=0, column=len(items) + 2, padx=5)
