# Python imports
# import tkinter as tk
# from tkinter import ttk

import logging
import tkinter as tk
from tkinter import ttk

# Project imports
from views.base import BaseView
from constants import config
from utilities.db import (
    run_query_get_rows,
    insert_query_with_values,
)
from .base import BaseView


class AddEditCampView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.plan_id_for_camp = self.master.get_global_state().get("plan_id_to_view")
        self.camp_id = self.master.get_global_state().get("camp_id_to_edit", None)
        if self.camp_id:
            self.edit_camp_details = run_query_get_rows(
                f"SELECT * FROM Camp WHERE id = '{self.camp_id}'"
            )[0]

        self.render_widgets()
        self.master.update()

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
            pady=20,
        )

        # Header
        self.header_container = tk.Frame(self.container)
        self.header_container.pack(pady=5, fill="x", expand=True)

        self.header_text = "Edit Camp" if self.camp_id else "Add Camp"
        self.header = tk.Label(
            master=self.header_container, text=self.header_text, font=(30)
        )
        self.header.pack(
            side="top",
        )
        
        # Instructions label
        self.instructions_container = ttk.LabelFrame(
            master=self.header_container,
            text="Instructions",
        )
        self.instructions_container.pack(side='bottom')
        
        # editing
        if self.camp_id:
            text = "You can edit details for this Camp below.\n\nNOTE: max capacity cannot be set to lower than the current capacity."
        # adding new camp
        else:
            text = "You can create a Camp below by filling in all fields and pressing 'Add Camp'."

        self.instructions_label = ttk.Label(
            master=self.instructions_container,
            text=text,
            anchor="w",
            justify="left",
        )
        self.instructions_label.pack()

        # Making a form within self.container through ttk.Frame
        self.form_container = tk.Frame(
            master=self.container,
        )

        self.form_container.pack(
            pady=15,
            fill="both",
            expand=True,
        )

        self._render_plan_id(
            self.form_container,
            on_row=0,
        )
        self._render_camp_id(
            self.form_container,
            on_row=1,
        )
        self._render_camp_name(
            self.form_container,
            on_row=2,
        )
        self._render_location(
            self.form_container,
            on_row=3,
        )
        self._render_maxCapacity(
            self.form_container,
            on_row=4,
        )
        self._render_action_buttons(
            self.form_container,
            on_row=5,
        )

    def _render_action_buttons(self, form_container, on_row: int) -> None:
        self.action_buttons_container = tk.Frame(
            master=form_container,
        )
        self.action_buttons_container.grid(
            row=on_row,
            column=0,
        )

        self.submit_button = tk.Button(
            master=self.action_buttons_container,
            text="Add Camp" if not self.camp_id else "Update Camp",
            command=self._handle_submit,
            fg="green",
        )
        self.submit_button.pack(
            side="right",
        )

        self.cancel_button = tk.Button(
            master=self.action_buttons_container,
            text="Cancel",
            command=lambda: self.handle_cancel_click(),
        )
        self.cancel_button.pack(
            side="left",
        )

        if self.camp_id:
            self.delete_button = tk.Button(
                master=self.action_buttons_container,
                text="Delete",
                fg="red",
                command=self._render_delete_confirm_popup_window,
            )
            self.delete_button.pack(
                side="left",
            )

    def handle_cancel_click(self)->None:
        
        # Clean pstate
        self.master.get_global_state().pop("camp_id_to_edit", None)
        
        self.master.switch_to_view('plan_detail')
    
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

        self.plan_id_text = tk.StringVar(value=self.plan_id_for_camp)

        self.plan_id_entry = tk.Entry(
            master=self.plan_id_entry_container,
            width=50,
            state="disabled",
            textvariable=self.plan_id_text,
        )
        self.plan_id_entry.pack()

    def _get_latest_camp_id(self) -> int:
        latest_camp_id = run_query_get_rows(
            "SELECT MAX(id) AS latest_camp_id FROM Camp"
        )[0].get("latest_camp_id")
        return latest_camp_id

    def _render_camp_id(self, form_container, on_row: int) -> None:
        self.camp_id_container = tk.Frame(
            master=form_container,
        )
        self.camp_id_container.grid(
            row=on_row,
            column=0,
        )

        self.camp_id_label_container = tk.Frame(
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
        if self.camp_id:
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

    # Function to fill out camp name in form
    def _render_camp_name(self, form_container, on_row: int) -> None:
        # Container for camp name
        self.camp_name_container = tk.Frame(
            master=form_container,
        )
        self.camp_name_container.grid(
            row=on_row,
            column=0,
        )

        # Container for text into container for camp name
        self.camp_name_label_container = tk.Frame(
            master=self.camp_name_container,
        )
        self.camp_name_label_container.pack(
            expand=True,
            fill="x",
        )

        # Label for text into container for camp name
        self.camp_name_label = tk.Label(
            master=self.camp_name_label_container,
            text="Name",
        )
        self.camp_name_label.pack(side="left")

        # Container for camp name entry
        self.camp_name_entry_container = tk.Frame(
            master=self.camp_name_container,
        )
        self.camp_name_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.camp_name_text = tk.StringVar()

        if self.camp_id:
            self.camp_name_text.set(self.edit_camp_details["name"])

        # Get camp name entry
        self.camp_name_entry = tk.Entry(
            master=self.camp_name_entry_container,
            width=50,
            textvariable=self.camp_name_text if self.camp_id else None,
        )
        self.camp_name_entry.pack()

    def _render_location(self, form_container, on_row: int) -> None:
        self.location_container = tk.Frame(
            master=form_container,
        )
        self.location_container.grid(
            row=on_row,
            column=0,
        )

        self.location_label_container = tk.Frame(
            master=self.location_container,
        )
        self.location_label_container.pack(
            expand=True,
            fill="x",
        )

        self.location_label = tk.Label(
            master=self.location_label_container,
            text="Location",
        )
        self.location_label.pack(side="left")

        self.location_entry_container = tk.Frame(
            master=self.location_container,
        )
        self.location_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.location_text = tk.StringVar()
        if self.camp_id:
            self.location_text.set(self.edit_camp_details["location"])

        self.location_entry = tk.Entry(
            master=self.location_entry_container,
            width=50,
            textvariable=self.location_text if self.camp_id else None,
        )
        self.location_entry.pack()

    def _render_maxCapacity(self, form_container, on_row: int) -> None:
        self.maxCapacity_container = tk.Frame(
            master=form_container,
        )
        self.maxCapacity_container.grid(
            row=on_row,
            column=0,
        )

        self.maxCapacity_label_container = tk.Frame(
            master=self.maxCapacity_container,
        )
        self.maxCapacity_label_container.pack(
            expand=True,
            fill="x",
        )

        self.maxCapacity_label = tk.Label(
            master=self.maxCapacity_label_container,
            text="Max Capacity",
        )
        self.maxCapacity_label.pack(side="left")

        self.maxCapacity_entry_container = tk.Frame(
            master=self.maxCapacity_container,
        )
        self.maxCapacity_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.maxCapacity_text = tk.StringVar()
        if self.camp_id:
            self.maxCapacity_text.set(self.edit_camp_details["maxCapacity"])

        self.maxCapacity_entry = tk.Entry(
            master=self.maxCapacity_entry_container,
            width=50,
            textvariable=self.maxCapacity_text if self.camp_id else None,
        )
        self.maxCapacity_entry.pack()

    def _render_field_label_from_key(self, field_key: str) -> str:
        key_name_map = {
            "camp_name": "Camp Name",
            "location": "Location",
            "maxCapacity": "Max Capacity",
        }

        return key_name_map[field_key]

    def _handle_submit(self) -> None:
        plan_id = self.plan_id_entry.get()
        camp_id = self.camp_id_entry.get()
        camp_name = self.camp_name_entry.get()
        location = self.location_entry.get()
        maxCapacity = self.maxCapacity_entry.get()

        # Perform form validation
        self.form_is_valid = True
        # {field: [errors]}
        errors = {
            "camp_name": [],
            "location": [],
            "maxCapacity": [],
        }

        # Ensure all fields have values
        if not camp_name.strip():
            self.form_is_valid = False
            errors["camp_name"].append("This field is required.")
        if not location.strip():
            self.form_is_valid = False
            errors["location"].append("This field is required.")
        if not maxCapacity.strip():
            self.form_is_valid = False
            errors["description"].append("This field is required.")

        # DATA VALIDATION

        if not self.form_is_valid:
            error_msg = ""
            for field, field_errors in errors.items():
                if field_errors:
                    error_msg += (
                        "**" + self._render_field_label_from_key(field).upper() + "**\n"
                    )
                    for field_error in field_errors:
                        error_msg += f"{field_error}\n"
                    error_msg += "\n\n"
            self.render_error_popup_window(message=error_msg)

            logging.debug(
                f"INVALID FORM: {errors=}\n\{plan_id=}, {camp_name=}, {camp_id=}, {location=}, {maxCapacity=}"
            )
            return

        if self.camp_id:
            insert_query_with_values(
                query=f"""UPDATE Camp
                                     SET
                                        plan_id = :plan_id,                                   
                                        name = :name,                                        
                                        location = :location,
                                        maxCapacity = :maxCapacity
                                     WHERE
                                        id = :id
                                     """,
                values={
                    "id" : camp_id,
                    "plan_id": plan_id,
                    "name": camp_name,
                    "location": location,
                    "maxCapacity": maxCapacity,
                },
            )
            logging.info(
                f"Updated plan: {plan_id=}, {camp_name=}, {camp_id=}, {location=}, {maxCapacity=}"
            )
        else:
            insert_query_with_values(
                query="""INSERT INTO Camp 
                    (
                        plan_id,
                        name,
                        location,
                        maxCapacity
                        ) VALUES (
                        :plan_id, 
                        :name, 
                        :location, 
                        :maxCapacity
                    );
                    """,
                values={
                    "plan_id": plan_id,
                    "name": camp_name,
                    "location": location,
                    "maxCapacity": maxCapacity,
                },
            )
            logging.info(
                f"Inserted plan: {plan_id=}, {camp_name=}, {camp_id=}, {location=}, {maxCapacity=}"
            )
        self.master.switch_to_view("plan_detail")

    def _render_delete_confirm_popup_window(self) -> None:
        self.error_popup_window = tk.Toplevel(self.master)
        self.error_popup_window.title("🚨 Delete Camp")
        tk.Label(
            master=self.error_popup_window,
            text="Are you sure you want to delete this camp?",
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

        # Disable main window
        self.error_popup_window.grab_set()
