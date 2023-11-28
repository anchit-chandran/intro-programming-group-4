# Python imports
import tkinter as tk
from tkinter import ttk

# Project imports
from views.base import BaseView
from constants import config
from utilities.db import run_query_get_rows, \
    insert_query_with_values  # from utilities.db means “from the utilities module, find the db.py file”
from .base import BaseView


class AddEditCampView(BaseView):
    def __init__(self,
                 master=None):  # so when the add/edit camp button is pressed, the following under __init__ has to run
        super().__init__(master)
        self.master = master  # self.master is just a variable name

        self.camp_name_to_edit = self.master.GLOBAL_STATE.get("camp_name_to_edit")
        self.camp_name_is_edit = bool(self.camp_name_to_edit)
        if self.camp_name_is_edit:
            self.edit_camp_details = run_query_get_rows(
                f"SELECT * FROM Camp WHERE name = '{self.camp_name_to_edit}'"
                # select all columns from camp table for this camp name
            )[0]  # not sure what [0] is for (?)

        self.render_widgets()

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
            pady=20,
        )

        # Header
        self.header_container = ttk.Frame(self.container)
        self.header_container.pack(pady=5, fill="x", expand=True)

        self.header_text = "Edit Camp" if self.camp_name_is_edit else "Add Plan"
        self.header = ttk.Label(
            master=self.header_container,
            text=self.header_text,
            font=(30)
        )
        self.header.pack(
            side="left",
        )

        # Making a form within self.container through ttk.Frame
        self.form_container = ttk.Frame(
            master=self.container,
        )

        self.form_container.pack(
            pady=15,
            fill="both",
            expand=True,
        )

        self._render_camp_name(
            self.form_container,
            on_row=1,
        )

    # need to do the buttons section (?)
    def _render_plan_id(self, form_container, on_row: int) -> None:
        # PLAN ID
        self.plan_id_container = tk.Frame(
            master=form_container,
        )
        self.plan_id_container.grid(
            row=on_row,
            column=0,
        )

        self.plan_id_label_container = tk.Frame(
            master=self.plan_id_container,
        )
        self.plan_id_label_container.pack(
            expand=True,
            fill="x",
        )
        self.plan_id_label = tk.Label(
            master=self.plan_id_label_container,
            text="Plan ID",
        )
        self.plan_id_label.pack(
            side="left",
        )

        self.plan_id_entry_container = tk.Frame(
            master=self.plan_id_container,
        )
        self.plan_id_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.plan_id_text = tk.StringVar()
        if self.camp_name_is_edit:
            self.plan_id_text.set(self.edit_camp_details["id"])

            self.plan_id_entry = tk.Entry(
                master=self.plan_id_entry_container,
                width=50,
                state="disabled",
                textvariable=self.plan_id_text,
            )
            self.plan_id_entry.pack()
        else:
            self.plan_id_entry = tk.Entry(
                master=self.plan_id_entry_container,
                width=50,
                textvariable=self.plan_id_text,
            )
            self.plan_id_entry.pack()

    def _render_camp_id(self, form_container, on_row: int) -> None:
        self.camp_id_container = ttk.Frame(
            master=form_container,
        )
        self.camp_id_container.grid(
            row=on_row,
            column=0,
        )

        self.camp_id_label_container = ttk.Frame(
            master=self.camp_id_container,
        )
        self.camp_id_label_container.pack(
            expand=True,
            fill="x",
        )
        self.camp_id_label = tk.Label(
            master=self.camp_id_label_container,
            text="Camp ID",
        )
        self.camp_id_label.pack(
            side="left",
        )

        self.camp_id_entry_container = tk.Frame(
            master=self.camp_id_container,
        )
        self.camp_id_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.camp_id_text = tk.StringVar()
        if self.camp_name_is_edit:
            self.camp_id_text.set(self.edit_camp_details["id"])
        else:  # If adding new camp
            # Get latest camp id (plus 1 because you need this camp id to be increment from the last camp id)
            self.camp_id_text.set(self._get_latest_camp_id() + 1)
        self.camp_id_entry = tk.Entry(
            master=self.camp_id_entry_container,
            width=50,
            state="disabled",
            textvariable=self.camp_id_text,
        )
        self.camp_id_entry.pack()

    def _get_latest_camp_id(self) -> int:
        latest_camp_id = run_query_get_rows(
            "SELECT MAX(id) AS latest_camp_id FROM Plan"
        )[0].get("latest_plan_id")
        return latest_camp_id

    # Function to fill out camp name in form
    def _render_camp_name(self, form_container, on_row: int) -> None:
        # Container for camp name
        self.camp_name_container = ttk.Frame(
            master=form_container,
        )
        self.camp_name_container.grid(
            row=on_row,
            column=0,
        )

        # Container for text into container for camp name
        self.camp_name_label_container = ttk.Frame(
            master=self.camp_name_container,
        )
        self.camp_name_label_container.pack(
            expand=True,
            fill="x",
        )

        # Label for text into container for camp name
        self.camp_name_label = ttk.Label(
            master=self.camp_name_label_container,
            text="Name",
        )
        self.camp_name_label.pack(
            side="left"
        )

        # Container for camp name entry
        self.camp_name_entry_container = tk.Frame(
            master=self.camp_name_container,
        )
        self.camp_name_entry_container.pack(
            expand=True,
            fill="x",
        )

        # Whatever the camp name entry is, set that as the name (relate to the table in db.py for camp)
        # there will later be a _handle_submit function to get the camp name entry (?)
        self.camp_name_text = ttk.StringVar()
        # If editing, change the previously filled name to new name
        if self.camp_name_is_edit:
            self.camp_name_text.set(self.edit_camp_details["name"])

        # Get camp name entry
        self.camp_name_entry = ttk.Entry(
            master=self.camp_name_entry_container,
            width=50,
            textvariable=self.camp_name_text if self.camp_name_is_edit else None,
        )
        self.camp_name_entry.pack()

    def _render_location(self, form_container, on_row: int) -> None:
        self.location_container = ttk.Frame(
            master=form_container,
        )
        self.location_container.grid(
            row=on_row,
            column=0,
        )

        self.location_label_container = ttk.Frame(
            master=self.location_container,
        )
        self.location_label_container.pack(
            expand=True,
            fill="x",
        )

        self.location_label = ttk.Label(
            master=self.location_label_container,
            text="Location",
        )
        self.location_label.pack(
            side="left"
        )

        self.location_entry_container = tk.Frame(
            master=self.location_container,
        )
        self.location_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.location_text = ttk.StringVar()
        if self.camp_name_is_edit:
            self.location_text.set(self.edit_camp_details["location"])

        self.location_entry = ttk.Entry(
            master=self.location_entry_container,
            width=50,
            textvariable=self.location_text if self.camp_name_is_edit else None,
        )
        self.location_entry.pack()

    def _render_maxCapacity(self, form_container, on_row: int) -> None:
        self.maxCapacity_container = ttk.Frame(
            master=form_container,
        )
        self.maxCapacity_container.grid(
            row=on_row,
            column=0,
        )

        self.maxCapacity_label_container = ttk.Frame(
            master=self.maxCapacity_container,
        )
        self.maxCapacity_label_container.pack(
            expand=True,
            fill="x",
        )

        self.maxCapacity_label = ttk.Label(
            master=self.maxCapacity_label_container,
            text="Location",
        )
        self.maxCapacity_label.pack(
            side="left"
        )

        self.maxCapacity_entry_container = tk.Frame(
            master=self.maxCapacity_container,
        )
        self.maxCapacity_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.maxCapacity_text = ttk.StringVar()
        if self.camp_name_is_edit:
            self.maxCapacity_text.set(self.edit_camp_details["maxCapacity"])

        self.maxCapacity_entry = ttk.Entry(
            master=self.maxCapacity_entry_container,
            width=50,
            textvariable=self.maxCapacity_text if self.camp_name_is_edit else None,
        )
        self.maxCapacity_entry.pack()







