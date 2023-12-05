# Python imports
import logging
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime

# Project imports
from constants import config
from utilities.db import run_query_get_rows, insert_query_with_values
from utilities.validators import is_valid_email
from .base import BaseView


class AddEditPlanView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # SET INSTANCE VARIABLES
        self.MAX_CHAR_LEN = 20

        self.edit_plan_id = self.master.GLOBAL_STATE.get("plan_id_to_edit")
        self.is_edit = bool(self.edit_plan_id)
        if self.is_edit:
            self.edit_plan_details = run_query_get_rows(
                f"SELECT * FROM Plan WHERE id = {self.edit_plan_id}"
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

        self.header_text = "Edit Plan" if self.is_edit else "Add Plan"
        self.header = tk.Label(
            master=self.header_container,
            text=self.header_text,
            font=(20),
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
        self.instructions_label = tk.Label(
            master=self.instructions_container,
            text="All fields are mandatory.\n\nStart Date must be a valid date, and in the future.\n\nCentral email must be a valid email in the general format: example@domain.com.",
            anchor="w",
            justify="left",
        )
        self.instructions_label.pack()

        # FORM
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
        self._render_plan_name(
            self.form_container,
            on_row=1,
        )
        self._render_plan_location(
            self.form_container,
            on_row=2,
        )
        self._render_start_date(
            self.form_container,
            on_row=3,
        )
        self._render_description(
            self.form_container,
            on_row=4,
        )
        self._render_central_email(
            self.form_container,
            on_row=5,
        )

        self._render_action_buttons(
            self.form_container,
            on_row=6,
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
            text="Add Plan" if not self.is_edit else "Update Plan",
            command=self._handle_submit,
            fg="green",
        )
        self.submit_button.pack(
            side="right",
        )

        self.cancel_button = tk.Button(
            master=self.action_buttons_container,
            text="Back",
            command=lambda: self.master.switch_to_view("all_plans"),
        )
        self.cancel_button.pack(
            side="left",
        )

        if self.is_edit:
            self.delete_button = tk.Button(
                master=self.action_buttons_container,
                text="Delete",
                fg="red",
                command=self._render_delete_confirm_popup_window,
            )
            self.delete_button.pack(
                side="left",
            )

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
        if self.is_edit:
            self.plan_id_text.set(self.edit_plan_details["id"])
        else:
            # Get latest plan id
            self.plan_id_text.set(self._get_latest_plan_id() + 1)
        self.plan_id_entry = tk.Entry(
            master=self.plan_id_entry_container,
            width=50,
            state="disabled",
            textvariable=self.plan_id_text,
        )
        self.plan_id_entry.pack()

    def _render_plan_name(self, form_container, on_row: int) -> None:
        # PLAN NAME
        self.plan_name_container = tk.Frame(
            master=form_container,
        )
        self.plan_name_container.grid(
            row=on_row,
            column=0,
        )

        self.plan_name_label_container = tk.Frame(
            master=self.plan_name_container,
        )
        self.plan_name_label_container.pack(
            expand=True,
            fill="x",
        )
        self.plan_name_label = tk.Label(
            master=self.plan_name_label_container,
            text="Name (max 40 chars)",
        )
        self.plan_name_label.pack(
            side="left",
        )

        self.plan_name_entry_container = tk.Frame(
            master=self.plan_name_container,
        )
        self.plan_name_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.plan_title_text = tk.StringVar()
        if self.is_edit:
            self.plan_title_text.set(self.edit_plan_details["title"])
        # Set char length limit
        self.plan_title_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=self.plan_title_text, char_limit=self.MAX_CHAR_LEN
            ),
        )
        self.plan_name_entry = tk.Entry(
            master=self.plan_name_entry_container,
            width=50,
            textvariable=self.plan_title_text,
        )
        self.plan_name_entry.pack()

    def _render_start_date(self, form_container, on_row: int) -> None:
        # DATE
        self.start_date_container = tk.Frame(
            master=form_container,
        )
        self.start_date_container.grid(
            row=on_row,
            column=0,
        )

        self.start_date_label_container = tk.Frame(
            master=self.start_date_container,
        )
        self.start_date_label_container.pack(
            expand=True,
            fill="x",
        )
        self.start_date_label = tk.Label(
            master=self.start_date_label_container,
            text="Start Date (YYYY-MM-DD)",
        )
        self.start_date_label.pack(
            side="left",
        )
        self.start_date_entry_container = tk.Frame(
            master=self.start_date_container,
        )
        self.start_date_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.plan_start_date_year_text = tk.StringVar()
        if self.is_edit:
            self.edit_year, self.edit_month, self.edit_day = self.edit_plan_details[
                "start_date"
            ].split("-")
            self.plan_start_date_year_text.set(self.edit_year)
        # Set char length limit
        self.plan_start_date_year_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=self.plan_start_date_year_text, char_limit=4
            ),
        )
        self.start_date_year_entry = tk.Entry(
            master=self.start_date_entry_container,
            width=50 // 3,
            textvariable=self.plan_start_date_year_text,
            state="disabled" if self.is_edit else None,
        )
        self.start_date_year_entry.pack(
            side="left",
        )
        if not self.is_edit:
            self.start_date_year_entry.insert(0, "1912")

        self.plan_start_date_month_text = tk.StringVar()
        if self.is_edit:
            self.plan_start_date_month_text.set(self.edit_month)
        # Set char length limit
        self.plan_start_date_month_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=self.plan_start_date_month_text, char_limit=2
            ),
        )
        self.start_date_month_entry = tk.Entry(
            master=self.start_date_entry_container,
            width=50 // 3,
            textvariable=self.plan_start_date_month_text,
            state="disabled" if self.is_edit else None,
        )
        self.start_date_month_entry.pack(
            side="left",
        )
        if not self.is_edit:
            self.start_date_month_entry.insert(0, "06")

        self.plan_start_date_day_text = tk.StringVar()
        if self.is_edit:
            self.plan_start_date_day_text.set(self.edit_day)
        # Set char length limit
        self.plan_start_date_day_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=self.plan_start_date_day_text, char_limit=2
            ),
        )
        self.start_date_day_entry = tk.Entry(
            master=self.start_date_entry_container,
            width=50 // 3,
            textvariable=self.plan_start_date_day_text,
            state="disabled" if self.is_edit else None,
        )
        self.start_date_day_entry.pack(
            side="left",
        )
        if not self.is_edit:
            self.start_date_day_entry.insert(0, "23")

    def _render_plan_location(self, form_container, on_row: int) -> None:
        # PLAN location
        self.plan_location_container = tk.Frame(
            master=form_container,
        )
        self.plan_location_container.grid(
            row=on_row,
            column=0,
        )

        self.plan_location_label_container = tk.Frame(
            master=self.plan_location_container,
        )
        self.plan_location_label_container.pack(
            expand=True,
            fill="x",
        )
        self.plan_location_label = tk.Label(
            master=self.plan_location_label_container,
            text="Location (max 40 chars)",
        )
        self.plan_location_label.pack(
            side="left",
        )

        self.plan_location_entry_container = tk.Frame(
            master=self.plan_location_container,
        )
        self.plan_location_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.plan_location_text = tk.StringVar()
        if self.is_edit:
            self.plan_location_text.set(self.edit_plan_details["location"])

        # Set char length limit
        self.plan_location_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=self.plan_location_text, char_limit=self.MAX_CHAR_LEN
            ),
        )

        self.plan_location_entry = tk.Entry(
            master=self.plan_location_entry_container,
            width=50,
            textvariable=self.plan_location_text,
        )
        self.plan_location_entry.pack()

    def _render_end_date(self, form_container, on_row: int) -> None:
        # DATE
        self.end_date_container = tk.Frame(
            master=form_container,
        )
        self.end_date_container.grid(
            row=on_row,
            column=0,
        )

        self.end_date_label_container = tk.Frame(
            master=self.end_date_container,
        )
        self.end_date_label_container.pack(
            expand=True,
            fill="x",
        )
        self.end_date_label = tk.Label(
            master=self.end_date_label_container,
            text="End Date (YYYY-MM-DD) (optional)",
        )
        self.end_date_label.pack(
            side="left",
        )
        self.end_date_entry_container = tk.Frame(
            master=self.end_date_container,
        )
        self.end_date_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.end_date_year_entry = tk.Entry(
            master=self.end_date_entry_container,
            width=50 // 3,
        )
        self.end_date_year_entry.pack(
            side="left",
        )
        self.end_date_year_entry.insert(0, "1912")
        self.end_date_month_entry = tk.Entry(
            master=self.end_date_entry_container,
            width=50 // 3,
        )
        self.end_date_month_entry.pack(
            side="left",
        )
        self.end_date_month_entry.insert(0, "06")
        self.end_date_day_entry = tk.Entry(
            master=self.end_date_entry_container,
            width=50 // 3,
        )
        self.end_date_day_entry.pack(
            side="left",
        )
        self.end_date_day_entry.insert(0, "23")

    def _render_description(self, form_container, on_row: int) -> None:
        # PLAN description
        self.description_container = tk.Frame(
            master=form_container,
        )
        self.description_container.grid(
            row=on_row,
            column=0,
        )

        self.description_label_container = tk.Frame(
            master=self.description_container,
        )
        self.description_label_container.pack(
            expand=True,
            fill="x",
        )
        self.description_label = tk.Label(
            master=self.description_label_container,
            text="Description (max 40 chars)",
        )
        self.description_label.pack(
            side="left",
        )

        self.description_entry_container = tk.Frame(
            master=self.description_container,
        )
        self.description_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.description_text = tk.StringVar()
        if self.is_edit:
            self.description_text.set(self.edit_plan_details["description"])

        # Set char length limit
        self.description_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=self.description_text, char_limit=self.MAX_CHAR_LEN
            ),
        )

        self.description_entry = tk.Entry(
            master=self.description_entry_container,
            width=50,
            textvariable=self.description_text,
        )
        self.description_entry.pack()

    def _render_central_email(self, form_container, on_row: int) -> None:
        # PLAN central_email
        self.central_email_container = tk.Frame(
            master=form_container,
        )
        self.central_email_container.grid(
            row=on_row,
            column=0,
        )

        self.central_email_label_container = tk.Frame(
            master=self.central_email_container,
        )
        self.central_email_label_container.pack(
            expand=True,
            fill="x",
        )
        self.central_email_label = tk.Label(
            master=self.central_email_label_container,
            text="Central Email",
        )
        self.central_email_label.pack(
            side="left",
        )

        self.central_email_entry_container = tk.Frame(
            master=self.central_email_container,
        )
        self.central_email_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.central_email_text = tk.StringVar()
        if self.is_edit:
            self.central_email_text.set(self.edit_plan_details["central_email"])

        self.central_email_entry = tk.Entry(
            master=self.central_email_entry_container,
            width=50,
            textvariable=self.central_email_text,
        )
        self.central_email_entry.pack()

    def _get_latest_plan_id(self) -> int:
        latest_plan_id = run_query_get_rows(
            "SELECT MAX(id) AS latest_plan_id FROM Plan"
        )[0].get("latest_plan_id")
        return latest_plan_id

    def validate_start_date(self, start_date: str) -> datetime.date:
        """Try to turn start date into Date object and ensure it is not in future"""
        try:
            year, month, day = start_date.split("-")
            start_date = datetime.date(year=int(year), month=int(month), day=int(day))

            # If editing, start date can be in the past
            if start_date < datetime.date.today() and (not self.is_edit):
                return None, "Start date cannot be in the past."
            return start_date, ""
        except Exception as e:
            logging.debug(f"Invalid start date: {e}")
            return None, "Invalid start date."

    def _render_field_label_from_key(self, field_key: str) -> str:
        key_name_map = {
            "plan_name": "Plan Name",
            "start_date": "Start Date",
            "location": "Location",
            "description": "Description",
            "central_email": "Central Email",
        }

        return key_name_map[field_key]

    def _handle_submit(self) -> None:
        plan_id = self.plan_id_entry.get()
        plan_name = self.plan_name_entry.get()
        start_date = self.get_entry_date()
        location = self.plan_location_entry.get()
        description = self.description_entry.get()
        central_email = self.central_email_entry.get()

        # Perform form validation
        self.form_is_valid = True
        # {field: [errors]}
        errors = {
            "plan_name": [],
            "start_date": [],
            "location": [],
            "description": [],
            "central_email": [],
        }

        # Ensure all fields have values
        if not plan_name.strip():
            self.form_is_valid = False
            errors["plan_name"].append("This field is required.")
        else:
            # Ensure unique name
            if self.is_edit:
                # Get current plan name
                current_plan_name = run_query_get_rows(f"SELECT title FROM Plan WHERE id={plan_id}")[0]['title']
                
                # Check duplicates
                n_duplicate_plans = run_query_get_rows(f"SELECT COUNT(*) FROM Plan WHERE title='{plan_name}' AND title != '{current_plan_name}'")[0]['COUNT(*)']
                logging.debug(f'{self.is_edit=} and {n_duplicate_plans=}')
                
                if n_duplicate_plans: # bc this current plan will already show
                    self.form_is_valid = False
                    errors["plan_name"].append(f"Plan Name must be unique!")
            else:
                # Check duplicates
                n_duplicate_plans = run_query_get_rows(f"SELECT COUNT(*) FROM Plan WHERE title='{plan_name}'")[0]['COUNT(*)']
                if n_duplicate_plans:
                    self.form_is_valid = False
                    errors["plan_name"].append(f"Plan Name must be unique!")
        if not "".join(start_date.split("-")).strip():
            self.form_is_valid = False
            errors["start_date"].append("This field is required.")
        if not location.strip():
            self.form_is_valid = False
            errors["location"].append("This field is required.")
        if not description.strip():
            self.form_is_valid = False
            errors["description"].append("This field is required.")
        if not central_email.strip():
            self.form_is_valid = False
            errors["central_email"].append("This field is required.")

        # DATA VALIDATION
        # Ensure start date valid
        start_date, date_error_msg = self.validate_start_date(start_date)
        if start_date is None:
            self.form_is_valid = False
            errors["start_date"].append(date_error_msg)

        # EMAIL VALIDATION
        if central_email and not is_valid_email(central_email):
            self.form_is_valid = False
            errors["central_email"].append("Invalid email.")

        if not self.form_is_valid:
            error_msg = ""
            for field, field_errors in errors.items():
                if field_errors:
                    error_msg += self._render_field_label_from_key(field).upper()
                    for field_error in field_errors:
                        error_msg += f"\n\t{field_error}\n"
                    error_msg += "\n\n"
            self.render_error_popup_window(message=error_msg)

            logging.debug(
                f"INVALID FORM: {errors=}\n\{plan_id=}, {plan_name=}, {start_date=}, {location=}, {description=}, {central_email=}"
            )
            return

        if self.is_edit:
            insert_query_with_values(
                query=f"""UPDATE Plan
                                     SET
                                        title = :title,
                                        description = :description,
                                        location = :location,
                                        start_date = :start_date,
                                        central_email = :central_email
                                     WHERE
                                        id = :id
                                     """,
                values={
                    "id": plan_id,
                    "title": plan_name,
                    "description": description,
                    "location": location,
                    "start_date": start_date,
                    "end_date": None,
                    "central_email": central_email,
                },
            )
            logging.info(
                f"Updated plan: {plan_id=}, {plan_name=}, {start_date=}, {location=}, {description=}, {central_email=}"
            )
        else:
            insert_query_with_values(
                query="""INSERT INTO Plan 
                    (
                        title,
                        description,
                        location,
                        start_date,
                        end_date,
                        central_email
                        ) VALUES (
                        :title, 
                        :description, 
                        :location, 
                        :start_date, 
                        :end_date, 
                        :central_email
                    );
                    """,
                values={
                    "title": plan_name,
                    "description": description,
                    "location": location,
                    "start_date": start_date,
                    "end_date": None,
                    "central_email": central_email,
                },
            )
            logging.info(
                f"Inserted plan: {plan_id=}, {plan_name=}, {start_date=}, {location=}, {description=}, {central_email=}"
            )
        self.master.switch_to_view("all_plans")

    def get_entry_date(self) -> str:
        """Returns date in YYYY-MM-DD format. Also performs validation"""
        year = self.start_date_year_entry.get()
        month = self.start_date_month_entry.get()
        day = self.start_date_day_entry.get()

        return f"{year}-{month}-{day}"

    def _render_delete_confirm_popup_window(self) -> None:
        title = "🚨 Delete Plan"
        message = "Are you sure you want to delete this plan?"
        confirm = messagebox.askokcancel(title=title, message=message)
        if confirm:
            logging.debug(f"Deleting {self.edit_plan_details['id']=}")

        # Perform deletion
        insert_query_with_values(
            query="""DELETE 
                                 FROM Plan
                                 WHERE id = :id
                                 """,
            values={"id": self.edit_plan_details["id"]},
        )

        self.master.switch_to_view("all_plans")
