# Python imports
# import tkinter as tk
# from tkinter import ttk

import logging
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


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

        self.is_admin = self.master.get_global_state().get("is_admin")

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
        self.instructions_container.pack(side="bottom")

        # editing
        if self.camp_id:
            current_capacity = self.calculate_current_capacity(camp_id=self.camp_id)
            text = f"You can edit details for this Camp below.\n\nMax Capacity must be a positive integer.\n\nNOTE: max capacity cannot be set to lower than the current capacity, which is currently: {current_capacity}."
        # adding new camp
        else:
            text = "You can create a Camp below by filling in all fields and pressing 'Add Camp'.\n\nMax Capacity must be a positive integer."

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

    def calculate_current_capacity(self, camp_id: int) -> int:
        current_capacity = run_query_get_rows(
            f"SELECT COUNT(id) FROM RefugeeFamily WHERE is_in_camp=1 AND camp_id={camp_id}"
        )[0]["COUNT(id)"]

        return int(current_capacity)

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
            command=self.handle_cancel_click,
        )
        self.cancel_button.pack(
            side="left",
        )

        if self.camp_id and self.is_admin:
            self.delete_button = tk.Button(
                master=self.action_buttons_container,
                text="Delete",
                fg="red",
                command=self._render_delete_confirm_popup_window,
            )
            self.delete_button.pack(
                side="left",
            )

    def handle_cancel_click(self) -> None:
        # Clean state
        self.master.get_global_state().pop("camp_id_to_edit", None)

        if self.is_admin:
            self.master.switch_to_view("plan_detail")
        else:
            current_global_state = self.master.get_global_state()
            current_global_state["camp_id_to_view"] = self.camp_id
            self.master.set_global_state(current_global_state)
            self.master.switch_to_view("camp_detail")

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
        # unique name
        else:
            # self.camp_id is None if adding,
            if self.camp_id is None:
                duplicate_camps = run_query_get_rows(
                    f"SELECT name FROM Camp WHERE name='{camp_name}' AND plan_id={plan_id}"
                )

                if len(duplicate_camps):
                    self.form_is_valid = False
                    errors["camp_name"].append("Camp name must be unique!")
            else:
                # editing camp id -> exclude current camp name
                current_camp_name = run_query_get_rows(
                    f"SELECT name FROM Camp WHERE id = {camp_id}"
                )[0]["name"]
                duplicate_camps = run_query_get_rows(
                    f"SELECT name FROM Camp WHERE name='{camp_name}' AND name != '{current_camp_name}' AND plan_id={plan_id}"
                )

                if len(duplicate_camps):
                    self.form_is_valid = False
                    errors["camp_name"].append("Camp name must be unique!")

        if not location.strip():
            self.form_is_valid = False
            errors["location"].append("This field is required.")
        if not maxCapacity.strip():
            self.form_is_valid = False
            errors["maxCapacity"].append("This field is required.")
        else:
            # maxCap has a value -> check it's an integer
            try:
                if not maxCapacity.isnumeric():
                    self.form_is_valid = False
                    errors["maxCapacity"].append(
                        "Invalid input! Must be a positive integer"
                    )
                else:
                    # Num IS an integer
                    if int(maxCapacity) < 0:
                        raise Exception

                    current_capacity = self.calculate_current_capacity(camp_id=camp_id)

                    if int(maxCapacity) < current_capacity:
                        self.form_is_valid = False
                        errors["maxCapacity"].append(
                            f"Invalid input! Cannot be less than current capacity ({current_capacity})"
                        )
            except Exception as e:
                logging.debug(f"Invalid input for maxCapacity")

        # VALIDATE
        if not self.form_is_valid:
            error_msg = ""
            for field, field_errors in errors.items():
                if field_errors:
                    error_msg += (
                        "" + self._render_field_label_from_key(field).upper() + "\n"
                    )
                    for field_error in field_errors:
                        error_msg += f"\t{field_error}\n"
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
                    "id": camp_id,
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

        # Clean state
        self.master.get_global_state().pop("camp_id_to_edit", None)

        if self.is_admin:
            self.master.switch_to_view("plan_detail")
        else:
            current_global_state = self.master.get_global_state()
            current_global_state["camp_id_to_view"] = self.camp_id
            self.master.set_global_state(current_global_state)
            self.master.switch_to_view("camp_detail")

    def _render_delete_confirm_popup_window(self) -> None:
        title = "🚨 Delete Camp"
        
        assoc_refugee_ids_raw = run_query_get_rows(f'SELECT id FROM RefugeeFamily WHERE camp_id = {self.camp_id}')
        assoc_refugee_ids = tuple([item['id'] for item in assoc_refugee_ids_raw])
        
        assoc_volunteer_ids_raw = run_query_get_rows(f'SELECT id FROM User WHERE camp_id = {self.camp_id}')
        assoc_volunteer_ids = tuple([item['id'] for item in assoc_volunteer_ids_raw])
        
        message = f"Are you sure you want to delete this camp?\n\nNOTE: this will delete all associated data, unless re-assigned, including:\n\n\t {len(assoc_volunteer_ids)} Volunteers\n\t {len(assoc_refugee_ids)} RefugeeFamilies"
        confirm = messagebox.askokcancel(title=title, message=message)
        if confirm:
            logging.debug(f"Deleting {self.edit_camp_details['id']=}")

            # Perform deletion
            insert_query_with_values(
                query="""DELETE 
                                    FROM Camp
                                    WHERE id = :id
                                    """,
                values={"id": self.edit_camp_details["id"]},
            )
            current_global_state = self.master.get_global_state()
            camp_id_to_view = current_global_state.pop("camp_id_to_edit")

            self.master.switch_to_view("plan_detail")
