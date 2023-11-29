# Python imports
import logging
import tkinter as tk
import tkinter.ttk as ttk

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
        self.update()


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
        self.header_container = ttk.Frame(self.container)
        self.header_container.pack(pady=15, fill="x", expand=True)

        self.header = tk.Label(
            master=self.header_container,
            text=f"ALL VOLUNTEERS",
            font=(60),
        )
        self.header.pack(
            side="left",
        )

        # Add volunteer button
        self.add_volunteer_button = tk.Button(
            master=self.header_container,
            text="+ Add Volunteer",
            command=self._handle_add_volunteer_click,
        )
        self.add_volunteer_button.pack(
            side="right",
        )
        
        # render table
        self.render_all_volunteers()

        # scrollbar function
        self.canvas_volunteer.bind(
            "<Configure>", self._on_canvas_configure_volunteer_table_container
        )

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
            "Camp Name",
            "Status",
            "Date of Birth",
            "Languages",
            "Skills",
            "Emergency Contact",
            "Emergency Number",
            "Edit",
        ]
        self.data_to_render = [self.header_cols]

        for volunteer in self.all_volunteers:
            data_to_add = []
            data_to_add.append(volunteer["id"])
            data_to_add.append(volunteer["username"])
            data_to_add.append(volunteer["first_name"])
            data_to_add.append(volunteer["last_name"])
            # sex
            sex = volunteer["sex"]
            if sex == "F":
                data_to_add.append("Female")
            else:
                data_to_add.append("Male")

            data_to_add.append(volunteer["phone_number"])
            data_to_add.append(volunteer["camp_id"])

            # status
            status = volunteer["is_active"]
            if status == 1:
                data_to_add.append("Active")
            else:
                data_to_add.append("Deactivated")
    
            data_to_add.append(get_date(volunteer["dob"]))
            data_to_add.append(volunteer["languages_spoken"])
            data_to_add.append(volunteer["skills"])
            data_to_add.append(volunteer["emergency_contact_name"])
            data_to_add.append(volunteer["emergency_contact_number"])

            self.data_to_render.append(data_to_add)

        self.all_volunteers_container = tk.Frame(
            master=self.container,
            width=500,
        )
        self.all_volunteers_container.pack(fill="both", expand=True)
        

        # scroll bar 
        # scrollbar function
        self.canvas_volunteer = tk.Canvas(
            self.all_volunteers_container,
            width=2000,
            height=200,
        )

        # create a scrollbar for canvas
        scrollbar_y = ttk.Scrollbar(
            self.all_volunteers_container,
            orient=tk.VERTICAL,
            command=self.canvas_volunteer.yview,
        )
        scrollbar_y.pack(
            side=tk.RIGHT,
            fill=tk.Y,
        )

        scrollbar_x = ttk.Scrollbar(
            self.all_volunteers_container,
            orient=tk.HORIZONTAL,
            command=self.canvas_volunteer.xview,
        )
        scrollbar_x.pack(
            side=tk.BOTTOM,
            fill=tk.X,
        )

        self.canvas_volunteer.pack(side=tk.LEFT, fill="both", expand=True)

        # Configure the canvas to use the scrollbar
        self.canvas_volunteer.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

         # Create a frame inside the canvas
        table_frame = tk.Frame(
            self.canvas_volunteer,
        )
        self.canvas_volunteer.create_window((0, 0), window=table_frame, anchor=tk.NW)
        # scrollbar attempt end
        
        self.table_container = tk.LabelFrame(
            master=table_frame,
            text="Volunteers Information",
            padx=10,
            pady=10,        
        )
        self.table_container.pack(padx=10, pady=50, fill="both", expand=True)  

        # Find the max col width
        self.max_col_width = calculate_max_col_width(self.data_to_render)

        for ix, row in enumerate(self.data_to_render):
            self._render_row(
                container=self.table_container,
                items=row,
                column_width=self.max_col_width,
                header=ix == 0,  # True if first row, else False; needs to fix this
            )
        

    def get_volunteers(self) -> 'list[dict]':
        return run_query_get_rows("SELECT * FROM User WHERE is_admin == 0")

   

    def _render_row(
        self,
        container: tk.Frame,
        items: 'list[str]',
        column_width=15,
        header=False,
    ) -> None:
        self.row_container = tk.Frame(
            master=container,
        )
        self.row_container.grid(row=container.grid_size()[1], sticky="w")

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
            if label == "Active":
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
                width=5
            ).grid(row=0, column=len(items))
            tk.Button(
                master=self.row_container,
                text="Deactivate",
                command=self._render_deactivate_confirm_popup_window,
                width=5
            ).grid(row=0, column=len(items)+1)
            tk.Button(
                master=self.row_container,
                text="Delete",
                command=self._render_delete_confirm_popup_window,
                width=4
            ).grid(row=0, column=len(items)+2)

    # Bind the canvas to update the scroll region
    def _on_canvas_configure_volunteer_table_container(self, event):
        self.canvas_volunteer.configure(
            scrollregion=self.canvas_volunteer.bbox("all")
        )
    # do not need this 
    #def _handle_view_click(self, volunteer_name: str):  
    #    # ADD TO STATE
    #    current_state = self.master.get_global_state()
    #    current_state["volunteer_name"] = volunteer_name
    #    self.master.set_global_state(current_state)
        
        # Change to view plan view
    #    self.master.switch_to_view("volunteer_detail")   #change this to a volunteer detail view
        
    
    def _handle_mouse_hover_enter(self, event):
        event.widget.config(background=config.LIGHTGREY)

    def _handle_mouse_hover_exit(self, event):
        event.widget.config(background=self.master.cget("bg"))

# change this to volunteer version
    def _handle_add_volunteer_click(self):
        
        # Clean EDIT PLAN global vars
        current_state = self.master.get_global_state()
        current_state.pop("volunteer_name_to_edit", None)
        self.master.set_global_state(current_state)
        
        self.master.switch_to_view("add_edit_user")   # link to Nondu's view

    def _handle_edit_click(self, volunteer_name: str):   
        # Add plan name to global state for edit view
        current_global_state = self.master.get_global_state()
        current_global_state["_name_to_edit"] = volunteer_name
        self.master.set_global_state(current_global_state)

        self.master.switch_to_view("add_edit_user")   # link to Nondu's view


    def _render_deactivate_confirm_popup_window(self) -> None:
        self.error_popup_window = tk.Toplevel(self.master)
        self.error_popup_window.title("🚨 Deactivate Volunteer")
        tk.Label(
            master=self.error_popup_window,
            text="Are you sure you want to deactivate this volunteer?",
        ).pack(
            pady=2,
            padx=10,
            expand=True,
            fill="both",
        )

        actions_container = tk.Frame(
            master=self.error_popup_window,
        )
        actions_container.pack()
        tk.Button(
            master=actions_container,
            text="Cancel",
            command=lambda: self._delete_window(self.error_popup_window),
        ).pack(
            pady=2,
            side="left",
            fill="x",
        )
        tk.Button(
            master=actions_container,
            text="Deactivate",
            fg="red",
        ).pack(
            pady=2,
            side="right",
            fill="x",
        )

    # how to delete
    def _render_delete_confirm_popup_window(self) -> None:
        self.error_popup_window = tk.Toplevel(self.master)
        self.error_popup_window.title("🚨 Delete Volunteer")
        tk.Label(
            master=self.error_popup_window,
            text="Are you sure you want to delete this volunteer?",
        ).pack(
            pady=2,
            padx=10,
            expand=True,
            fill="both",
        )

        actions_container = tk.Frame(
            master=self.error_popup_window,
        )
        actions_container.pack()
        tk.Button(
            master=actions_container,
            text="Cancel",
            command=lambda: self._delete_window(self.error_popup_window),
        ).pack(
            pady=2,
            side="left",
            fill="x",
        )
        tk.Button(
            master=actions_container,
            text="Delete",
            fg="red",
        ).pack(
            pady=2,
            side="right",
            fill="x",
        )


