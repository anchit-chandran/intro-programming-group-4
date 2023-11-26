"""TEMPLATE FILE FOR MAKING NEW VIEW"""
import logging as lg
import tkinter as tk

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from utilities.formatting import add_border, calculate_max_col_width
from utilities.sqlite3_date_formatter import get_date

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
            text=f"ALL VOLUNTEERS",
            font=(60),
        )
        self.header.pack(
            side="left",
        )

        # Add plan button
        self.add_volunteer_button = tk.Button(
            master=self.header_container,
            text="+ Add Volunteer",
            command=self._handle_add_volunteer_click,
        )
        self.add_plan_button.pack(
            side="right",
        )

        self.render_all_volunteers()

    def render_all_volunteers(self) -> None:
        self.all_volunteers = self.get_volunteers()

        # Get the data as simple list[str], starting with col headers
        self.header_cols = [
            "ID",
            "Username",
            "First Name",
            "Last Name",
            "Sex",
            "Phone Number",
            "Camp Name"
        ]
        self.data_to_render = [self.header_cols]
        for volunteer in self.all_plans:
            data_to_add = []
            data_to_add.append(volunteer["id"])
            data_to_add.append(volunteer["username"])
            data_to_add.append(volunteer["first_name"])
            data_to_add.append(volunteer["last_name"])
            data_to_add.append(volunteer["sex"])
            data_to_add.append(volunteer["phone_number"])
            data_to_add.append(volunteer["camp_id"])

            self.data_to_render.append(data_to_add)

        self.all_volunteers_container = tk.Frame(
            master=self.container,
        )
        self.all_volunteers_container.pack()

        self.table_container = tk.Frame(
            master=self.all_volunteers_container,
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

    def get_volunteers(self) -> list[dict]:
        return run_query_get_rows("SELECT * FROM User WHERE is_admin == 0")

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

    def _handle_view_click(self, volunteer_name: str):  # is this needed?
        
        # ADD TO STATE
        current_state = self.master.get_global_state()
        current_state["volunteer_name"] = volunteer_name
        self.master.set_global_state(current_state)
        
        # Change to view plan view
        self.master.switch_to_view("plan_detail")   #change this to a volunteer detail view
        
    
    def _handle_mouse_hover_enter(self, event):
        event.widget.config(background=config.LIGHTGREY)

    def _handle_mouse_hover_exit(self, event):
        event.widget.config(background=self.master.cget("bg"))

# change this to volunteer version
    def _handle_add_volunteer_click(self):
        
        # Clean EDIT PLAN global vars
        current_state = self.master.get_global_state()
        current_state.pop("plan_name_to_edit", None)
        self.master.set_global_state(current_state)
        
        self.master.switch_to_view("add_volunteer")   # this is a new view, to be added

    def _handle_edit_click(self, volunteer_name: str):   # need to change this???
        # Add plan name to global state for edit view
        current_global_state = self.master.get_global_state()
        current_global_state["_name_to_edit"] = volunteer_name
        self.master.set_global_state(current_global_state)

        self.master.switch_to_view("add_edit_volunteer")   # this is a new view, to be added

    