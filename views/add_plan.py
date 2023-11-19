# Python imports
import logging
import tkinter as tk
import datetime

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from .base import BaseView


class AddPlanView(BaseView):
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
            fill="both",
            padx=30,
            pady=20,
        )

        # Header
        self.header_container = tk.Frame(self.container)
        self.header_container.pack(pady=5, fill="x", expand=True)

        self.header = tk.Label(
            master=self.header_container,
            text=f"Add Plan",
            font=(20),
        )
        self.header.pack(
            side="left",
        )

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

        self.submit_button = tk.Button(
            master=self.form_container,
            text="Submit",
            command=self._handle_submit,
        )
        self.submit_button.grid(row=10, column=0)

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

        # Get latest plan id
        self.plan_id_text = tk.StringVar()
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
            text="Name",
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

        self.plan_name_entry = tk.Entry(
            master=self.plan_name_entry_container,
            width=50,
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

        self.start_date_year_entry = tk.Entry(
            master=self.start_date_entry_container,
            width=50 // 3,
        )
        self.start_date_year_entry.pack(
            side="left",
        )
        self.start_date_year_entry.insert(0, "YYYY")
        self.start_date_month_entry = tk.Entry(
            master=self.start_date_entry_container,
            width=50 // 3,
        )
        self.start_date_month_entry.pack(
            side="left",
        )
        self.start_date_month_entry.insert(0, "MM")
        self.start_date_day_entry = tk.Entry(
            master=self.start_date_entry_container,
            width=50 // 3,
        )
        self.start_date_day_entry.pack(
            side="left",
        )
        self.start_date_day_entry.insert(0, "DD")

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
            text="Location",
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

        self.plan_location_entry = tk.Entry(
            master=self.plan_location_entry_container,
            width=50,
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
        self.end_date_year_entry.insert(0, "YYYY")
        self.end_date_month_entry = tk.Entry(
            master=self.end_date_entry_container,
            width=50 // 3,
        )
        self.end_date_month_entry.pack(
            side="left",
        )
        self.end_date_month_entry.insert(0, "MM")
        self.end_date_day_entry = tk.Entry(
            master=self.end_date_entry_container,
            width=50 // 3,
        )
        self.end_date_day_entry.pack(
            side="left",
        )
        self.end_date_day_entry.insert(0, "DD")

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
            text="Description",
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

        self.description_entry = tk.Entry(
            master=self.description_entry_container,
            width=50,
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

        self.central_email_entry = tk.Entry(
            master=self.central_email_entry_container,
            width=50,
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
            if start_date < datetime.date.today():
                return None
            return start_date
        except Exception as e:
            logging.debug(f"Invalid start date: {e}")
            return None

    def _render_field_label_from_key(self, field_key: str) -> str:
        key_name_map = {
            
            "plan_name" : 'Plan Name',
            "start_date" : 'Start Date',
            "location" : 'Location',
            "description" : 'Description',
            "central_email" : 'Central Email',
        
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
        if not ''.join(start_date.split('-')).strip():
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
        
        # DATA VALIDATION
        # Ensure start date valid
        start_date = self.validate_start_date(start_date)
        if start_date is None:
            self.form_is_valid = False
            errors["start_date"].append("Invalid date.")

        if not self.form_is_valid:
            error_msg = ''
            for field, field_errors in errors.items():
                if field_errors:
                    error_msg += self._render_field_label_from_key(field).upper() + '\n'
                    for field_error in field_errors:
                        error_msg += f'\t{field_error}\n'
                    error_msg += '\n\n'
            self.render_error_popup_window(message=error_msg)
            
            logging.debug(
                f"INVALID FORM: {errors=}\n\{plan_id=}, {plan_name=}, {start_date=}, {location=}, {description=}, {central_email=}"
            )
            return

        logging.info(
            f"Adding plan: {plan_id=}, {plan_name=}, {start_date=}, {location=}, {description=}, {central_email=}"
        )

    def get_entry_date(self) -> str:
        """Returns date in YYYY-MM-DD format. Also performs validation"""
        year = self.start_date_year_entry.get()
        month = self.start_date_month_entry.get()
        day = self.start_date_day_entry.get()

        return f"{year}-{month}-{day}"
