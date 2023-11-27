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
            "Edit Buttons",
        ]
        self.data_to_render = [self.header_cols]

        for volunteer in self.all_volunteers:
            data_to_add = []
            data_to_add.append(volunteer["id"])
            data_to_add.append(volunteer["username"])
            data_to_add.append(volunteer["first_name"])
            data_to_add.append(volunteer["last_name"])
            data_to_add.append(volunteer["sex"])
            data_to_add.append(volunteer["phone_number"])
            data_to_add.append(volunteer["camp_id"])
            # status
            status = volunteer["is_active"]
            if status == 1:
                data_to_add.append("Active")
            else:
                data_to_add.append("Deactivated")

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
                header=ix == 0,  # True if first row, else False; needs to fix this
            )

        # MAKE THE TABLE SCROLLABLE
        # canvas container
        #self.volunteer_table_canvas = tk.Canvas(
        #    master=self.all_volunteers_container, width=1000, height=200
        #)
        #self.volunteer_table_canvas.grid(row=1, column=0, sticky="nsew", columnspan=2)

        # table
        #self.table_container = ttk.Frame(
        #    master=self.volunteer_table_canvas,
        #)
        #self.table_container.grid(row=1, column=0)

        # create scrollable window
        #self.volunteer_table_canvas.create_window(
        #    (0, 0), window=self.table_container, anchor="nw"
        #)

        # create scrollbar
        #self.volunteer_scrollbar = ttk.Scrollbar(
        #    master=self.volunteer_table_canvas,
        #    orient="vertical",
         #   command=self.volunteer_table_canvas.yview,
        #)
        #self.volunteer_scrollbar.grid(row=1, column=1, sticky="nse", padx=1)

        #self.volunteer_table_canvas.configure(yscrollcommand=self.volunteer_scrollbar.set)

        # Find the max col width
        #self.max_col_width = 15

        #for ix, row in enumerate(self.data_to_render):
        #    self._render_row(
         #       container=self.table_container,
         #       items=row,
         #       column_width=self.max_col_width,
         #       header=ix == 0,  # True if first row, else False
         #   )

        # updating scroll area
        #self.volunteer_table_canvas.update_idletasks()  # to checck everything is rendered
        #self.volunteer_table_canvas.configure(
          #  scrollregion=self.volunteer_table_canvas.bbox("all")
        #)  # setting the area scrolled with all the items inside

    def get_volunteers(self) -> 'list[dict]':
        return run_query_get_rows("SELECT * FROM User WHERE is_admin == 0")

    #def get_volunteers_status(self, username: str) -> int:
    #    return run_query_get_rows("SELECT is_active FROM User WHERE username = {username}")

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
            BUTTON_WIDTH = (column_width)//4
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
            tk.Button(
                master=self.row_container,
                text="Disable",
                command=self._render_deactivate_confirm_popup_window,
                width=BUTTON_WIDTH
            ).grid(row=0, column=len(items)+2)
            tk.Button(
                master=self.row_container,
                text="Delete",
                command=self._render_delete_confirm_popup_window,
                width=BUTTON_WIDTH
            ).grid(row=0, column=len(items)+3)


    def _handle_view_click(self, volunteer_name: str):  
        
        # ADD TO STATE
        current_state = self.master.get_global_state()
        current_state["volunteer_name"] = volunteer_name
        self.master.set_global_state(current_state)
        
        # Change to view plan view
        self.master.switch_to_view("volunteer_detail")   #change this to a volunteer detail view
        
    
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
        
        self.master.switch_to_view("add_edit_volunteer")   # link to Nondu's view

    def _handle_edit_click(self, volunteer_name: str):   
        # Add plan name to global state for edit view
        current_global_state = self.master.get_global_state()
        current_global_state["_name_to_edit"] = volunteer_name
        self.master.set_global_state(current_global_state)

        self.master.switch_to_view("add_edit_volunteer")   # link to Nondu's view


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


