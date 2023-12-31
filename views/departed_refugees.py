import logging
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Project imports
from constants import config, instructions
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
        self.container = tk.Frame(
            master=self,
            width=config.SCREEN_WIDTH,
            height=300,
        )
        self.container.pack(
            fill="both",
            padx=30,
            pady=50,
        )

        # Header
        self.header_container = tk.Frame(
            master=self.container,
            width=500,
            height=100,
        )
        self.header_container.pack()

        # back button
        self.go_back_button = ttk.Button(
            master=self.header_container,
            text="GO BACK TO CAMP",
            command=self.handle_back_button,
        )
        self.go_back_button.grid(row=0, column=0, padx=0, pady=15, sticky="n")

        camp_name = self.get_camp_name()

        self.header = ttk.Label(
            master=self.header_container,
            text=f"Departed refugees from {camp_name}",
            font=(60),
        )
        self.header.grid(row=1, column=0, padx=0, pady=0, sticky="new")

        # Instructions label
        self.instructions_container = ttk.LabelFrame(
            master=self.container,
            text="Instructions",
        )
        self.instructions_container.pack()
        self.instructions_label = tk.Label(
            master=self.instructions_container,
            text=instructions.INSTRUCTIONS["departed_refugees"],
            anchor="w",
            justify="left",
        )
        self.instructions_label.pack()
        
        self.all_refugees_container = ttk.Frame(
            master=self.container,
            width=1000,
        )
        
        self.all_refugees_container.pack(pady=10)
        
        self.selected_actions_container = tk.LabelFrame(
            master= self.all_refugees_container,
            text='Selected Refugee Actions'
        )
        self.selected_actions_container.pack()
        
        
        self.render_selected_refugee_actions(container=self.all_refugees_container)
        self.render_camp_refugees(container=self.all_refugees_container)
    
    def render_selected_refugee_actions(self, container) -> None:
        action_frame = tk.LabelFrame(
            master=container, text="Selected Refugee Family Actions"
        )
        action_frame.pack(side="top", padx=10)

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
        refugee_row = self.tree.focus()
        if not refugee_row:
            self.render_error_popup_window(
                message="Please select a Refugee Family first!"
            )
            return

        # Get selected row data
        refugee_data = self.tree.item(refugee_row, "values")
        refugee_id = refugee_data[0]

        if action == "view":
            self.handle_view_click(refugee_id=refugee_id)
        elif action == "edit":
            self.handle_edit_click(refugee_id=refugee_id)

    def render_camp_refugees(self, container) -> None:
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

        

        # headers list
        self.header_cols = [
            "ID",
            "Main Rep Name",
            "Med Conditions",
            "Adults",
            "Children",
            "Missing members",
        ]
        
        self.render_tree_table(
            header_cols=self.header_cols,
            container=container,
            data=self.data_to_render
        )
        

    