# Python imports
import logging
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import re

# Project imports
from constants import config
from utilities.db import run_query_get_rows, insert_query_with_values
from utilities.validators import is_valid_email
from .base import BaseView


class AddEditRefugeeView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # check the user role
        self.is_volunteer = not self.master.get_global_state().get("is_admin")

        # SET INSTANCE VARIABLES
        self.MAX_CHAR_LEN = 20
        self.plan_title_text = self.master.GLOBAL_STATE.get("plan_name")
        self.camp_id = self.master.GLOBAL_STATE.get("camp_id_to_view")

        self.edit_refugee_id = self.master.GLOBAL_STATE.get("refugee_id_to_edit")
        self.is_edit = bool(self.edit_refugee_id)
        if self.is_edit:
            self.edit_refugee_details = run_query_get_rows(
                f"SELECT * FROM RefugeeFamily WHERE id = '{self.edit_refugee_id}'"
            )[0]

        self.render_widgets()
        self.master.update()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
            width=config.SCREEN_WIDTH,
            height=400,
        )
        self.container.pack(
            fill="both",
            padx=40,
            pady=(50, 100),
        )

        # Header
        self.header_container = tk.Frame(self.container)
        self.header_container.pack(pady=5, fill="x", expand=True)

        self.header_text = (
            "Edit Refugee Family" if self.is_edit else "Add Refugee Family"
        )
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
        self.instructions_container.pack(side="bottom")
        self.instructions_label = tk.Label(
            master=self.instructions_container,
            text="All fields are mandatory.\n\nNumber of adults, number of children, age of main representative and number of missing people must be a valid positive integer",
            anchor="w",
            justify="left",
        )
        self.instructions_label.pack()

        # ----------------------- FORM ----------------------------
        self.form_container = tk.Frame(
            master=self.container,
        )
        self.form_container.pack(
            pady=15,
            fill="both",
            expand=True,
            padx=40,
        )
        # display plan - can't change
        self._render_plan_name(self.form_container, on_row=0, on_col=0),
        # display camp - question - can change or not?
        self._render_camp_name(self.form_container, on_row=0, on_col=1)

        # id
        self._render_refugee_id(self.form_container, on_row=1, on_col=0, stick_side="w")

        # rep name
        self._render_main_rep_name(
            self.form_container, on_row=1, on_col=1, stick_side="e"
        )

        # main_rep_age
        self._render_rep_age(self.form_container, on_row=2, on_col=0, stick_side="w")

        # main_rep_sex
        self._render_sex(self.form_container, on_row=2, on_col=1, stick_side="e")

        # main_rep_home_towm
        self._render_hometown(self.form_container, on_row=3, on_col=0, stick_side="w")

        # medical condition
        self._render_med_condition_name(
            self.form_container, on_row=3, on_col=1, stick_side="e"
        )

        # number of adults
        self._render_num_adults(self.form_container, on_row=4, on_col=0, stick_side="w")

        # number of children
        self._render_num_children(
            self.form_container, on_row=4, on_col=1, stick_side="e"
        )

        # number of missing people
        self._render_num_miss_members(
            self.form_container, on_row=5, on_col=0, stick_side="w"
        )

        # Status
        self._render_status(self.form_container, on_row=5, on_col=1, stick_side="e")

        # Buttons
        self._render_action_buttons(
            self.form_container, on_row=6, on_col=0, stick_side="nsew"
        )

    # -------------- Rendering functions for inputs ------------

    # render plan name
    def _render_plan_name(self, form_container, on_row: int, on_col: int) -> None:
        self.plan_name_container = tk.Frame(
            master=form_container,
        )
        self.plan_name_container.grid(row=on_row, column=on_col, padx=30, pady=10)

        self.plan_name_label_container = tk.Frame(
            master=self.plan_name_container,
        )
        self.plan_name_label_container.pack(
            expand=True,
            fill="x",
        )
        self.plan_name_label = tk.Label(
            master=self.plan_name_label_container,
            text="Plan Name",
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

        self.plan_name_str_text = tk.StringVar()
        if not self.is_volunteer:
            self.plan_name_str_text.set(self.master.GLOBAL_STATE.get("plan_name"))
        else:
            self.plan_name = self._get_plan_name()
            self.plan_name_str_text.set(self.plan_name)

        self.plan_name_entry = tk.Entry(
            master=self.plan_name_entry_container,
            width=40,
            state="disabled",
            textvariable=self.plan_name_str_text,
        )
        self.plan_name_entry.pack()

    # render camp name
    def _render_camp_name(self, form_container, on_row: int, on_col: int) -> None:
        self.camp_name_container = tk.Frame(
            master=form_container,
        )
        self.camp_name_container.grid(row=on_row, column=on_col, padx=30, pady=10)

        self.camp_name_label_container = tk.Frame(
            master=self.camp_name_container,
        )
        self.camp_name_label_container.pack(
            expand=True,
            fill="x",
        )
        self.camp_name_label = tk.Label(
            master=self.camp_name_label_container,
            text="Camp Name",
        )
        self.camp_name_label.pack(
            side="left",
        )

        self.camp_name_entry_container = tk.Frame(
            master=self.camp_name_container,
        )
        self.camp_name_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.camp_name_str_text = tk.StringVar()
        self.camp_name = self._get_camp_name()
        self.camp_name_str_text.set(self.camp_name)

        self.camp_name_entry = tk.Entry(
            master=self.camp_name_entry_container,
            width=40,
            state="disabled",
            textvariable=self.camp_name_str_text,
        )
        self.camp_name_entry.pack()

    #  Refugee ID
    def _render_refugee_id(
        self, form_container, on_row: int, on_col: int, stick_side: str
    ) -> None:
        """Renders refugee ID if exists or new refugee ID if adding"""
        self.refugee_id_container = tk.Frame(
            master=form_container,
        )
        self.refugee_id_container.grid(
            row=on_row, column=on_col, padx=30, pady=10, sticky=stick_side
        )

        self.refugee_id_label_container = tk.Frame(
            master=self.refugee_id_container,
        )
        self.refugee_id_label_container.pack(
            expand=True,
            fill="x",
        )
        self.refugee_id_label = tk.Label(
            master=self.refugee_id_label_container,
            text="Refugee ID",
        )
        self.refugee_id_label.pack(
            side="left",
        )

        self.refugee_id_entry_container = tk.Frame(
            master=self.refugee_id_container,
        )
        self.refugee_id_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.refugee_id_text = tk.StringVar()
        if self.is_edit:
            self.refugee_id_text.set(self.edit_refugee_details["id"])
        else:
            # Get latest refugee id
            self.refugee_id_text.set(self._get_latest_refugee_id() + 1)

        self.refugee_id_entry = tk.Entry(
            master=self.refugee_id_entry_container,
            width=40,
            state="disabled",
            textvariable=self.refugee_id_text,
        )
        self.refugee_id_entry.pack()

    # Refugee main rep namme
    def _render_main_rep_name(
        self, form_container, on_row: int, on_col: int, stick_side: str
    ) -> None:
        self.rep_name_container = tk.Frame(
            master=form_container,
        )
        self.rep_name_container.grid(
            row=on_row, column=on_col, padx=30, pady=10, sticky=stick_side
        )

        self.rep_name_label_container = tk.Frame(
            master=self.rep_name_container,
        )
        self.rep_name_label_container.pack(
            expand=True,
            fill="x",
        )
        self.rep_name_label = tk.Label(
            master=self.rep_name_label_container,
            text="Main Rep Name (max 40 chars)",
        )
        self.rep_name_label.pack(
            side="left",
        )

        self.rep_name_entry_container = tk.Frame(
            master=self.rep_name_container,
        )
        self.rep_name_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.main_rep_text = tk.StringVar()
        if self.is_edit:
            self.main_rep_text.set(self.edit_refugee_details["main_rep_name"])
        # Set char length limit
        self.main_rep_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=self.main_rep_text, char_limit=self.MAX_CHAR_LEN
            ),
        )
        self.rep_name_entry = tk.Entry(
            master=self.rep_name_entry_container,
            width=40,
            textvariable=self.main_rep_text,
        )
        self.rep_name_entry.pack()

    # Medical conition
    def _render_med_condition_name(
        self, form_container, on_row: int, on_col: int, stick_side: str
    ) -> None:
        self.med_condition_container = tk.Frame(
            master=form_container,
        )
        self.med_condition_container.grid(
            row=on_row, column=on_col, padx=30, pady=10, sticky=stick_side
        )

        self.med_condition_label_container = tk.Frame(
            master=self.med_condition_container,
        )
        self.med_condition_label_container.pack(
            expand=True,
            fill="x",
        )
        self.med_condition_label = tk.Label(
            master=self.med_condition_label_container,
            text="Medical Condition (max 40 chars)",
        )
        self.med_condition_label.pack(
            side="left",
        )

        self.med_condition_entry_container = tk.Frame(
            master=self.med_condition_container,
        )
        self.med_condition_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.main_rep_text = tk.StringVar()
        if self.is_edit:
            self.main_rep_text.set(self.edit_refugee_details["medical_conditions"])
        # Set char length limit
        self.main_rep_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=self.main_rep_text, char_limit=self.MAX_CHAR_LEN
            ),
        )
        self.med_condition_entry = tk.Entry(
            master=self.med_condition_entry_container,
            width=40,
            textvariable=self.main_rep_text,
        )
        self.med_condition_entry.pack()

    # Number of adults
    def _render_num_adults(
        self, form_container, on_row: int, on_col: int, stick_side: str
    ) -> None:
        self.num_adults_container = tk.Frame(
            master=form_container,
        )
        self.num_adults_container.grid(
            row=on_row, column=on_col, padx=30, pady=10, sticky=stick_side
        )

        self.num_adults_label_container = tk.Frame(
            master=self.num_adults_container,
        )
        self.num_adults_label_container.pack(
            expand=True,
            fill="x",
        )
        self.num_adults_label = tk.Label(
            master=self.num_adults_label_container,
            text="Number of adults",
        )
        self.num_adults_label.pack(
            side="left",
        )

        self.num_adults_entry_container = tk.Frame(
            master=self.num_adults_container,
        )
        self.num_adults_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.main_rep_text = tk.IntVar()
        if self.is_edit:
            self.main_rep_text.set(self.edit_refugee_details["n_adults"])

        self.num_adults_entry = tk.Entry(
            master=self.num_adults_entry_container,
            width=40,
            textvariable=self.main_rep_text,
        )
        self.num_adults_entry.pack()

    # Number of children
    def _render_num_children(
        self, form_container, on_row: int, on_col: int, stick_side: str
    ) -> None:
        self.num_children_container = tk.Frame(
            master=form_container,
        )
        self.num_children_container.grid(
            row=on_row, column=on_col, padx=30, pady=10, sticky=stick_side
        )

        self.num_children_label_container = tk.Frame(
            master=self.num_children_container,
        )
        self.num_children_label_container.pack(
            expand=True,
            fill="x",
        )
        self.num_children_label = tk.Label(
            master=self.num_children_label_container,
            text="Number of children",
        )
        self.num_children_label.pack(
            side="left",
        )

        self.num_children_entry_container = tk.Frame(
            master=self.num_children_container,
        )
        self.num_children_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.main_rep_text = tk.IntVar()
        if self.is_edit:
            self.main_rep_text.set(self.edit_refugee_details["n_children"])

        self.num_children_entry = tk.Entry(
            master=self.num_children_entry_container,
            width=40,
            textvariable=self.main_rep_text,
        )
        self.num_children_entry.pack()

    # Hometown
    def _render_hometown(
        self, form_container, on_row: int, on_col: int, stick_side: str
    ) -> None:
        self.rep_hometown_container = tk.Frame(
            master=form_container,
        )
        self.rep_hometown_container.grid(
            row=on_row, column=on_col, padx=30, pady=10, sticky=stick_side
        )

        self.rep_hometown_label_container = tk.Frame(
            master=self.rep_hometown_container,
        )
        self.rep_hometown_label_container.pack(
            expand=True,
            fill="x",
        )
        self.rep_hometown_label = tk.Label(
            master=self.rep_hometown_label_container,
            text="Main rep hometown (max 40 chars)",
        )
        self.rep_hometown_label.pack(
            side="left",
        )

        self.rep_hometown_entry_container = tk.Frame(
            master=self.rep_hometown_container,
        )
        self.rep_hometown_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.main_rep_text = tk.StringVar()
        if self.is_edit:
            self.main_rep_text.set(self.edit_refugee_details["main_rep_home_town"])
        # Set char length limit
        self.main_rep_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=self.main_rep_text, char_limit=self.MAX_CHAR_LEN
            ),
        )
        self.rep_hometown_entry = tk.Entry(
            master=self.rep_hometown_entry_container,
            width=40,
            textvariable=self.main_rep_text,
        )
        self.rep_hometown_entry.pack()

    # Main rep age
    def _render_rep_age(
        self, form_container, on_row: int, on_col: int, stick_side: str
    ) -> None:
        self.rep_age_container = tk.Frame(
            master=form_container,
        )
        self.rep_age_container.grid(
            row=on_row, column=on_col, padx=30, pady=10, sticky=stick_side
        )

        self.rep_age_label_container = tk.Frame(
            master=self.rep_age_container,
        )
        self.rep_age_label_container.pack(
            expand=True,
            fill="x",
        )
        self.rep_age_label = tk.Label(
            master=self.rep_age_label_container,
            text="Main rep age",
        )
        self.rep_age_label.pack(
            side="left",
        )

        self.rep_age_entry_container = tk.Frame(
            master=self.rep_age_container,
        )
        self.rep_age_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.main_rep_num = tk.IntVar()
        if self.is_edit:
            self.main_rep_num.set(self.edit_refugee_details["main_rep_age"])

        self.rep_age_entry = tk.Entry(
            master=self.rep_age_entry_container,
            width=40,
            textvariable=self.main_rep_num,
        )
        self.rep_age_entry.pack()

    # Main rep sex - wierd stuff in db??

    # Number of missing people
    def _render_num_miss_members(
        self, form_container, on_row: int, on_col: int, stick_side: str
    ) -> None:
        self.num_miss_members_container = tk.Frame(
            master=form_container,
        )
        self.num_miss_members_container.grid(
            row=on_row, column=on_col, padx=30, pady=10, sticky=stick_side
        )

        self.num_miss_members_label_container = tk.Frame(
            master=self.num_miss_members_container,
        )
        self.num_miss_members_label_container.pack(
            expand=True,
            fill="x",
        )
        self.num_miss_members_label = tk.Label(
            master=self.num_miss_members_label_container,
            text="Number of missing members",
        )
        self.num_miss_members_label.pack(
            side="left",
        )

        self.num_miss_members_entry_container = tk.Frame(
            master=self.num_miss_members_container,
        )
        self.num_miss_members_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.main_rep_text = tk.IntVar()
        if self.is_edit:
            self.main_rep_text.set(self.edit_refugee_details["n_missing_members"])

        self.num_miss_members_entry = tk.Entry(
            master=self.num_miss_members_entry_container,
            width=40,
            textvariable=self.main_rep_text,
        )
        self.num_miss_members_entry.pack()

    # Status
    def _render_status(
        self, form_container, on_row: int, on_col: int, stick_side: str
    ) -> None:
        self.status_container = tk.Frame(
            master=form_container,
        )
        self.status_container.grid(
            row=on_row, column=on_col, padx=(20, 50), pady=10, sticky=stick_side
        )

        self.status_label_container = tk.Frame(
            master=self.status_container,
        )
        self.status_label_container.pack(
            expand=True,
            fill="x",
        )
        self.status_label = tk.Label(
            master=self.status_label_container,
            text="Status",
        )
        self.status_label.pack(
            side="left",
        )

        self.status_entry_container = tk.Frame(
            master=self.status_container,
        )
        self.status_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.status_text = tk.StringVar()
        if self.is_edit:
            if self.edit_refugee_details["is_in_camp"] == 1:
                self.status_text.set("In camp")
            else:
                self.status_text.set("Left camp")
        else:
            self.status_text.set("In camp")

        self.options = ["In camp", "Left camp"]
        self.status_entry = tk.OptionMenu(
            self.status_entry_container, self.status_text, *self.options
        )
        self.status_entry.config(
            width=30, state="normal" if self.is_edit else "disabled"
        )

        self.status_entry.pack()

    # Main rep sex
    def _render_sex(
        self, form_container, on_row: int, on_col: int, stick_side: str
    ) -> None:
        self.sex_container = tk.Frame(
            master=form_container,
        )
        self.sex_container.grid(
            row=on_row, column=on_col, padx=(20, 50), pady=10, sticky=stick_side
        )

        self.sex_label_container = tk.Frame(
            master=self.sex_container,
        )
        self.sex_label_container.pack(
            expand=True,
            fill="x",
        )
        self.sex_label = tk.Label(
            master=self.sex_label_container,
            text="Main Rep Sex",
        )
        self.sex_label.pack(
            side="left",
        )

        self.sex_entry_container = tk.Frame(
            master=self.sex_container,
        )
        self.sex_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.sex_text = tk.StringVar()
        if self.is_edit:
            if self.edit_refugee_details["main_rep_sex"] == "F":
                self.sex_text.set("Female")
            if self.edit_refugee_details["main_rep_sex"] == "M":
                self.sex_text.set("Male")
            else:
                self.sex_text.set("Other")
        else:
            self.sex_text.set("Other")

        self.options = ["Female", "Male", "Other"]
        self.sex_entry = tk.OptionMenu(
            self.sex_entry_container, self.sex_text, *self.options
        )
        self.sex_entry.config(width=30)

        self.sex_entry.pack()

    # Buttons
    def _render_action_buttons(
        self, form_container, on_row: int, on_col: int, stick_side: str
    ) -> None:
        self.action_buttons_container = tk.Frame(
            master=form_container,
        )
        self.action_buttons_container.grid(
            row=on_row,
            column=on_col,
            padx=30,
            sticky=stick_side,
            pady=20,
            columnspan=2,
        )

        self.submit_button = tk.Button(
            master=self.action_buttons_container,
            text="Add Refugee" if not self.is_edit else "Update Refugee Info",
            command=self._handle_submit,
            fg="green",
        )
        self.submit_button.pack(side="right", padx=(10, 0))

        self.cancel_button = tk.Button(
            master=self.action_buttons_container,
            text="Back",
            command=lambda: self.master.switch_to_view("camp_detail"),
        )
        self.cancel_button.pack(side="left", padx=(0, 10))

        if self.is_edit:
            self.delete_button = tk.Button(
                master=self.action_buttons_container,
                text="Delete",
                fg="red",
                command=self._render_delete_confirm_popup_window,
            )
            self.delete_button.pack(side="left", padx=10)

    # ------------------- HELPER FUNCTIONS ----------------------
    def _get_latest_refugee_id(self) -> int:
        latest_refugee_id = run_query_get_rows(
            "SELECT MAX(id) AS latest_refugee_id FROM RefugeeFamily"
        )[0].get("latest_refugee_id")
        return latest_refugee_id

    def _get_plan_name(self):
        plan_name = run_query_get_rows(
            f"SELECT title FROM Plan AS p INNER JOIN Camp AS c ON p.id = c.plan_id WHERE c.id = {self.camp_id}"
        )[0].get("title")
        return plan_name

    def _get_camp_name(self) -> list[dict]:
        """queries name of the camp"""
        camp_name = run_query_get_rows(
            f"SELECT name FROM Camp WHERE id='{self.camp_id}'"
        )[0].get("name")
        return camp_name

    def _handle_submit(self):
        # values from entries
        refugee_id = self.refugee_id_entry.get()
        main_rep_name = self.rep_name_entry.get()
        med_condition = self.med_condition_entry.get()
        num_adults = self.num_adults_entry.get()
        num_children = self.num_children_entry.get()
        hometown = self.rep_hometown_entry.get()
        rep_age = self.rep_age_entry.get()
        missing_members = self.num_miss_members_entry.get()
        status = self.status_text.get()
        sex = self.sex_text.get()

        # change to db format status and sex
        if status == "In camp":
            status = 1
        elif status == "Left camp":
            status = 0

        if sex == "Female":
            sex = "F"
        elif sex == "Male":
            sex = "M"
        else:
            sex = "Other"

        # form validation
        self.form_is_valid = True

        errors = {
            "main_rep_name": [],
            "med_condition": [],
            "num_adults": [],
            "num_children": [],
            "hometown": [],
            "rep_age": [],
            "missing_members": [],
            "status": [],
            "main_rep_sex": [],
            "num_members": [],
        }

        # empty fields check
        if not main_rep_name.strip():
            self.form_is_valid = False
            errors["main_rep_name"].append("This field is required.")
        if not med_condition.strip():
            self.form_is_valid = False
            errors["med_condition"].append("This field is required.")
        if not num_adults.strip():
            self.form_is_valid = False
            errors["num_adults"].append("This field is required.")
        if not num_children.strip():
            self.form_is_valid = False
            errors["num_children"].append("This field is required.")
        if not hometown.strip():
            self.form_is_valid = False
            errors["hometown"].append("This field is required.")
        if not rep_age.strip():
            self.form_is_valid = False
            errors["rep_age"].append("This field is required.")
        if not missing_members.strip():
            self.form_is_valid = False
            errors["missing_members"].append("This field is required.")

        # DATA VALIDATION
        # if the numbers are valid input (type and not negative)

        if num_adults and not self.is_valid_number(num_adults.strip()):
            self.form_is_valid = False
            errors["num_adults"].append("Invalid number of adults")
        if num_children and not self.is_valid_number(num_children.strip()):
            self.form_is_valid = False
            errors["num_children"].append("Invalid number of children")
        if missing_members and not self.is_valid_number(missing_members.strip()):
            self.form_is_valid = False
            errors["missing_members"].append("Invalid number of missing memebers")
        if (
            rep_age
            and not self.is_valid_number(rep_age.strip())
            or (int(rep_age) > 105 or int(rep_age) <= 0)
        ):
            self.form_is_valid = False
            errors["rep_age"].append("Invalid age")

        # at least one family member in the camp
        if (self.is_valid_number(num_adults) and int(num_adults) == 0) and (
            self.is_valid_number(num_children) and int(num_children) == 0
        ):
            self.form_is_valid = False
            errors["num_members"].append(
                "The family has to consist of at least one member"
            )

        # error message if from is not valid
        if not self.form_is_valid:
            error_msg = ""
            for field, field_errors in errors.items():
                if field_errors:
                    error_msg += self._render_field_label_from_key(field).upper()
                    for field_error in field_errors:
                        error_msg += f"\t{field_error}\n"
                    error_msg += "\n\n"
            self.render_error_popup_window(message=error_msg)
            return

        # INSERT VALUES INTO DB
        if self.is_edit:
            insert_query_with_values(
                query=f"""UPDATE RefugeeFamily
                                     SET
                                        main_rep_name = :main_rep_name,
                                        medical_conditions = :med_condition,
                                        n_adults = :num_adults,
                                        n_children = :num_children,
                                        main_rep_home_town = :hometown,
                                        main_rep_age = :rep_age,
                                        n_missing_members = :missing_members,
                                        is_in_camp = :status,
                                        main_rep_sex = :sex
                                     WHERE
                                        id = :refugee_id
                                     """,
                values={
                    "refugee_id": refugee_id,
                    "main_rep_name": main_rep_name,
                    "med_condition": med_condition,
                    "num_adults": num_adults,
                    "num_children": num_children,
                    "hometown": hometown,
                    "rep_age": rep_age,
                    "missing_members": missing_members,
                    "status": status,
                    "sex": sex,
                },
            )
            logging.info(
                f"Updated refugee family: {refugee_id=}, {main_rep_name=}, {num_adults=}, {num_children=}, {hometown=}, {rep_age=}, {missing_members=}, {status=},  {sex=}"
            )
        else:
            insert_query_with_values(
                query="""INSERT INTO RefugeeFamily 
                    (
                                        main_rep_name,
                                        medical_conditions,
                                        n_adults,
                                        n_children,
                                        main_rep_home_town,
                                        main_rep_age,
                                        n_missing_members,
                                        is_in_camp,
                                        camp_id,
                                        main_rep_sex
                        ) VALUES (
                                        :main_rep_name,
                                        :med_condition,
                                        :num_adults,
                                        :num_children,
                                        :hometown,
                                        :rep_age,
                                        :missing_members,
                                        :status,
                                        :camp_id,
                                        :sex
                    );
                    """,
                values={
                    "main_rep_name": main_rep_name,
                    "med_condition": med_condition,
                    "num_adults": num_adults,
                    "num_children": num_children,
                    "hometown": hometown,
                    "rep_age": rep_age,
                    "missing_members": missing_members,
                    "status": status,
                    "camp_id": self.camp_id,
                    "sex": sex,
                },
            )
            logging.info(
                f"Inserted refugee family:{main_rep_name=}, {num_adults=}, {num_children=}, {hometown=}, {rep_age=}, {missing_members=}, {status=}, {sex=}"
            )
        self.master.switch_to_view("camp_detail")

    def _render_delete_confirm_popup_window(self) -> None:
        title = "🚨 Delete Refugee Record"
        message = "Are you sure you want to delete this refugee family record?"
        confirm = messagebox.askokcancel(title=title, message=message)
        if confirm:
            logging.debug(f"Deleting {self.edit_refugee_details['id']=}")

            # Perform deletion
            insert_query_with_values(
                query="""DELETE 
                                    FROM RefugeeFamily
                                    WHERE id = :id
                                    """,
                values={"id": self.edit_refugee_details["id"]},
            )

            self.master.switch_to_view("camp_detail")

    def is_valid_number(self, entry) -> bool:
        try:
            int_value = int(entry)
            if int_value >= 0:
                return True
        except ValueError:
            return False

    def _render_field_label_from_key(self, field_key: str) -> str:
        key_name_map = {
            "main_rep_name": "Main Representative Name",
            "med_condition": "Medical Condition",
            "num_adults": "Number of Adults",
            "num_children": "Number of Children",
            "hometown": "Hometown",
            "rep_age": "Representative's Age",
            "missing_members": "Number of Missing Members",
            "status": "Status",
            "sex": "Sex",
            "num_members": "Family Members",
        }

        return key_name_map[field_key]
