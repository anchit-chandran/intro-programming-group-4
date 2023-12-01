# Python imports
import logging
import tkinter as tk

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from .base import BaseView


class AllVolunteersView(BaseView):
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
        )
        self.container.pack(pady=10)

        # Header
        self.header_container = tk.Frame(self.container)
        self.header_container.pack(pady=15, fill="x", expand=True)

        self.header = tk.Label(
            master=self.header_container,
            text=f"ALL VOLUNTEERS",
            font=(60),
        )
        self.header.pack(
            side="left",
            padx=200,
        )

        # selected volunteer buttons
        self.edit_volunteer_button = tk.Button(
            master=self.header_container,
            text="Edit Selected volunteer",
            command=lambda: self._handle_selected_action_button_click(action='edit'),
        )
        self.edit_volunteer_button.pack(
            side="right",
        )

        self.view_volunteer_button = tk.Button(
            master=self.header_container,
            text="View Selected volunteer",
            command=lambda: self._handle_selected_action_button_click(action='view'),
        )
        self.view_volunteer_button.pack(
            side="right",
        )
        self.add_volunteer_button = tk.Button(
            master=self.header_container,
            text="+ Add volunteer",
            command=lambda: self._handle_selected_action_button_click(action='add'),
        )
        self.add_volunteer_button.pack(
            side="right",
        )

        self.render_all_volunteers()

    def _handle_selected_action_button_click(self, action:str)->None:
        if action == 'add':
            self._handle_add_volunteer()
            return
        
        # Other 2 buttons must have selected volunteer
        volunteer_row = self.tree.focus()
        if not volunteer_row:
            self.render_error_popup_window(message='Please select a volunteer first!')
            
            
    def render_all_volunteers(self) -> None:
        all_volunteers = self.get_all_volunteers_plans()
        self.data_to_render = self.get_data_for_rendering_table(all_volunteers)
        self.header_cols = [
            "ID",
            "Username",
            "Account Active",
            "Camp ID",
        ]
        self.all_volunteers_container = tk.Frame(
            master=self.container,
        )
        self.all_volunteers_container.pack()

        self.render_tree_table(
            header_cols=self.header_cols,
            data=self.data_to_render,
            container=self.all_volunteers_container,
            col_widths=[
                30,
                150,
                100,
                60,
            ],
        )

    def get_data_for_rendering_table(self, sql_data: list[dict]):
        data_to_render = []
        for volunteer in sql_data:
            data_to_add = []
            data_to_add.append(volunteer["id"])
            data_to_add.append(volunteer["username"])
            data_to_add.append(volunteer["is_active"])
            data_to_add.append(volunteer["camp_id"])
            data_to_render.append(data_to_add)
        return data_to_render

    def get_all_volunteers_plans(self) -> list[dict]:
        return run_query_get_rows("SELECT * FROM User WHERE is_admin=0")

    def _handle_add_volunteer(self)->None:
        
        current_state = self.master.get_global_state()
        current_state["add_volunteer"] = True
        self.master.set_global_state(current_state)

        self.master.switch_to_view("add_edit_user_profile")