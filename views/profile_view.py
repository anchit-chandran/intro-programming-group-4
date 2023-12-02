# Python imports
import logging
import tkinter as tk
from tkinter import ttk
from datetime import date

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from views.base import BaseView
from constants import config


class ProfileView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.MAX_CHAR_LEN = 30
        self.MAX_CHAR_LEN_IDs = 3
        self.should_render = self.decide_what_to_render()
        # above may set:
        # self.volunteer_id
        # self.volunteer_data

        self.render_widgets()
        self.master.update()

    def decide_what_to_render(self) -> str:
        """Will return one of:

        "edit_volunteer"
        "view_volunteer"
        "add_volunteer"
        "own_profile"

        """
        current_state = self.master.get_global_state()

        if current_state.get("volunteer_id_to_edit"):
            self.volunteer_id = current_state.pop("volunteer_id_to_edit")
            logging.debug(f"Editing volunteer: {self.volunteer_id}")
            self._set_volunteer_instance_data()
            return "edit_volunteer"
        elif current_state.get("volunteer_id_to_view"):
            self.volunteer_id = current_state.pop("volunteer_id_to_view")
            logging.debug(f"Viewing volunteer: {self.volunteer_id}")
            self._set_volunteer_instance_data()
            return "view_volunteer"
        elif current_state.get("add_volunteer"):
            return "add_volunteer"
        else:
            # viewing self
            return "own_profile"

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
            width=800,
            height=500,
        )
        self.container.pack(
            fill="both",
        )

        # Header
        self.header_container = tk.Frame(
            master=self.container,
            width=500,
            height=10,
        )
        self.header_container.pack()

        header_text = self.get_header_text()
        self.header = tk.Label(
            master=self.header_container,
            text=header_text,
            font=(60),
        )
        self.header.grid(
            row=0,
            column=5,
            pady=10,
        )

        # User profile variables
        status_profile = "Active"
        firstname = ""
        lastname = ""
        sex = ""
        phone = ""
        languages = ""
        skills = ""
        emergency_contact_name = ""
        emergency_contact_number = ""
        campID = ""
        dob_year = ""
        dob_month = ""
        dob_day = ""

        user_id, username = self._get_user_id_and_username_for_form()
        if user_id:
            user_profile = run_query_get_rows(
                f"SELECT * FROM User WHERE id = '{user_id}'"
            )[0]
            (
                status_profile,
                firstname,
                lastname,
                sex,
                phone,
                languages,
                skills,
                emergency_contact_name,
                emergency_contact_number,
                campID,
                dob_year,
                dob_month,
                dob_day,
            ) = self._get_user_profile_text(user_profile)

        # Section : User details (userID, campID, username, status)
        self.user_details_label_container = tk.LabelFrame(
            master=self.container,
            text="User Details*",
            width=400,
            height=50,
        )

        # Section: Personal info (firstname, lastname, DOB, sex, phone...)
        self.personal_info_label_container = tk.LabelFrame(
            master=self.container,
            text="Personal information*",
            width=400,
            height=100,
        )

        # Section: Emergency contact
        self.emergency_label_container = tk.LabelFrame(
            master=self.container,
            text="Emergency contact*",
            width=400,
            height=50,
        )

        # Set up - labels and entries
        self.userID_label = tk.Label(
            master=self.user_details_label_container,
            text="User ID",
            width=10,
        )

        # DECIDE WHETHER ENTRIES SHOULD BE DISABLED
        state = self._should_entries_disable()
        new_user_id = run_query_get_rows(f"SELECT MAX(id) FROM User")[0]["MAX(id)"] + 1
        user_id_text = tk.StringVar(value=user_id or new_user_id)
        self.userID_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state="disabled",
            textvariable=user_id_text,
        )

        self.username_label = tk.Label(
            master=self.user_details_label_container,
            text=f"Username",
            width=10,
        )

        username_text = tk.StringVar(value=username)
        # Set char length limit
        username_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=username_text, char_limit=15
            ),
        )
        self.username_entry = tk.Entry(
            master=self.user_details_label_container,
            width=20,
            state="disabled" if not self.should_render == "add_volunteer" else "normal",
            textvariable=username_text,
        )

        self.campID_label = tk.Label(
            master=self.user_details_label_container,
            text="Camp ID",
            width=10,
        )

        camp_id_text = tk.StringVar(value=campID)
        # Set char length limit
        camp_id_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=camp_id_text, char_limit=self.MAX_CHAR_LEN_IDs
            ),
        )
        self.campID_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state=state
            if not getattr(self, "volunteer_editing_self", None)
            else "disabled",  # volunteers can't edit this
            text=camp_id_text,
        )

        self.status_label = tk.Label(
            master=self.user_details_label_container,
            text="Status",
            width=10,
        )

        self.status_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state="disabled",
            text=tk.StringVar(value=status_profile),
        )

        self.firstname_label = tk.Label(
            master=self.personal_info_label_container,
            text="First name",
            width=20,
            anchor="w",
        )
        firstname_text = tk.StringVar(value=firstname)
        # Set char length limit
        firstname_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=firstname_text, char_limit=self.MAX_CHAR_LEN
            ),
        )
        self.firstname_entry = tk.Entry(
            master=self.personal_info_label_container,
            width=70,
            state=state,
            text=firstname_text,
        )

        self.lastname_label = tk.Label(
            master=self.personal_info_label_container,
            text="Last name",
            width=20,
            anchor="w",
        )

        # Set char length limit
        lastname_text = tk.StringVar(value=lastname)
        lastname_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=lastname_text, char_limit=self.MAX_CHAR_LEN
            ),
        )
        self.lastname_entry = tk.Entry(
            master=self.personal_info_label_container,
            width=70,
            state=state,
            text=lastname_text,
        )

        self.dob_container = tk.Frame(
            master=self.personal_info_label_container,
        )

        self.dob_label = tk.Label(
            master=self.personal_info_label_container,
            text="Date of Birth",
            width=20,
            anchor="w",
        )

        # Set char length limit
        dob_year_text = tk.StringVar(value=dob_year or "YYYY")
        dob_year_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=dob_year_text, char_limit=4
            ),
        )
        self.dob_year_entry = tk.Entry(
            master=self.dob_container,
            width=10,
            text=dob_year_text,
            state=state,
        )
        self.dob_year_entry.pack(anchor="w", side="left")

        # Set char length limit
        dob_month_text = tk.StringVar(value=dob_month or "MM")
        dob_month_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=dob_month_text, char_limit=2
            ),
        )
        self.dob_month_entry = tk.Entry(
            master=self.dob_container,
            width=5,
            text=dob_month_text,
            state=state,
        )
        self.dob_month_entry.pack(anchor="w", side="left", padx=5)

        # Set char length limit
        dob_day_text = tk.StringVar(value=dob_day or "DD")
        dob_day_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=dob_day_text, char_limit=2
            ),
        )
        self.dob_day_entry = tk.Entry(
            master=self.dob_container,
            width=5,
            text=dob_day_text,
            state=state,
        )
        self.dob_day_entry.pack(anchor="w", side="left", padx=5)

        self.sex_label = tk.Label(
            master=self.personal_info_label_container,
            text="Sex",
            width=20,
            anchor="w",
        )

        if self.should_render in ["view_volunteer", "own_profile"]:
            sex_text = tk.StringVar(value=sex)
            self.sex_entry = tk.Entry(
                master=self.personal_info_label_container,
                width=70,
                state=state,
                text=sex_text,
            )
        else:
            self.sex_entry = ttk.Combobox(
                master=self.personal_info_label_container,
                width=6,
                state="readonly",
            )
            self.sex_entry["values"] = config.SEX_VALUES
            if sex == "":
                sex = None
            self.sex_entry.current(
                config.SEX_VALUES.index(sex) if sex else 1
            )  # If no sex, val will be None

        self.phone_label = tk.Label(
            master=self.personal_info_label_container,
            text="Phone number",
            width=20,
            anchor="w",
        )

        # Set char length limit
        phone_text = tk.StringVar(value=phone)
        phone_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=phone_text, char_limit=15
            ),
        )
        self.phone_entry = tk.Entry(
            master=self.personal_info_label_container,
            width=70,
            state=state,
            text=phone_text,
        )

        self.other_languages_label = tk.Label(
            master=self.personal_info_label_container,
            text="Languages spoken",
            width=20,
            anchor="w",
        )

        # Set char length limit
        languages_text = tk.StringVar(value=languages)
        languages_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=languages_text, char_limit=self.MAX_CHAR_LEN
            ),
        )
        self.other_languages_entry = tk.Entry(
            master=self.personal_info_label_container,
            width=70,
            state=state,
            text=languages_text,
        )

        self.other_skills_label = tk.Label(
            master=self.personal_info_label_container,
            text="Skills",
            width=20,
            anchor="w",
        )

        # Set char length limit
        skills_text = tk.StringVar(value=skills)
        skills_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=skills_text, char_limit=self.MAX_CHAR_LEN
            ),
        )
        self.other_skills_entry = tk.Entry(
            master=self.personal_info_label_container,
            width=70,
            state=state,
            text=skills_text,
        )

        self.emergency_contact_name_label = tk.Label(
            master=self.emergency_label_container,
            text="Contact name",
            width=20,
            anchor="w",
        )

        # Set char length limit
        emergency_contact_name_text = tk.StringVar(value=emergency_contact_name)
        emergency_contact_name_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=emergency_contact_name_text, char_limit=self.MAX_CHAR_LEN
            ),
        )
        self.emergency_contact_name_entry = tk.Entry(
            master=self.emergency_label_container,
            width=70,
            state=state,
            text=emergency_contact_name_text,
        )

        self.emergency_contact_number_label = tk.Label(
            master=self.emergency_label_container,
            text="Contact phone number",
            width=20,
            anchor="w",
        )

        # Set char length limit
        emergency_contact_number_text = tk.StringVar(value=emergency_contact_number)
        emergency_contact_number_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=emergency_contact_number_text, char_limit=15
            ),
        )
        self.emergency_contact_number_entry = tk.Entry(
            master=self.emergency_label_container,
            width=70,
            state=state,
            text=emergency_contact_number_text,
        )

        # Add to grid
        self.user_details_label_container.pack(pady=(10, 20))
        self.personal_info_label_container.pack(pady=(10, 20))
        self.emergency_label_container.pack(pady=(10, 20))

        self.userID_label.grid(
            row=0,
            column=0,
        )
        self.userID_entry.grid(
            row=0,
            column=1,
        )

        self.username_label.grid(
            row=0,
            column=2,
        )
        self.username_entry.grid(
            row=0,
            column=3,
        )

        self.campID_label.grid(
            row=0,
            column=4,
        )
        self.campID_entry.grid(
            row=0,
            column=5,
        )

        self.status_label.grid(
            row=0,
            column=6,
        )
        self.status_entry.grid(
            row=0,
            column=7,
        )

        self.firstname_label.grid(
            row=0,
            column=0,
        )
        self.firstname_entry.grid(
            row=0,
            column=1,
        )

        self.lastname_label.grid(
            row=1,
            column=0,
        )
        self.lastname_entry.grid(
            row=1,
            column=1,
        )

        self.dob_label.grid(
            row=2,
            column=0,
        )
        self.dob_container.grid(row=2, column=1, sticky="w")

        self.sex_label.grid(
            row=3,
            column=0,
        )
        self.sex_entry.grid(row=3, column=1, sticky="w")

        self.phone_label.grid(
            row=4,
            column=0,
        )
        self.phone_entry.grid(
            row=4,
            column=1,
        )

        self.other_languages_label.grid(
            row=5,
            column=0,
        )
        self.other_languages_entry.grid(
            row=5,
            column=1,
        )

        self.other_skills_label.grid(
            row=6,
            column=0,
        )
        self.other_skills_entry.grid(
            row=6,
            column=1,
        )

        self.emergency_contact_name_label.grid(
            row=0,
            column=0,
        )
        self.emergency_contact_name_entry.grid(
            row=0,
            column=1,
        )

        self.emergency_contact_number_label.grid(
            row=1,
            column=0,
        )
        self.emergency_contact_number_entry.grid(
            row=1,
            column=1,
        )

        self._conditional_render_action_buttons(container=self.container)

    def get_header_text(self) -> None:
        # Must handle:
        #     "own_profile"
        #     "edit_volunteer"
        #     "view_volunteer"
        #     "add_volunteer"
        current_state = self.master.get_global_state()

        if self.should_render == "own_profile":
            return f"Hey, {current_state['username']} 👋"
        elif self.should_render == "edit_volunteer":
            return f"Editing {self.volunteer_data['username']} ✏️"
        elif self.should_render == "view_volunteer":
            return f"Viewing {self.volunteer_data['username']} 👁️"
        elif self.should_render == "add_volunteer":
            return f"Add new volunteer"

    def _set_volunteer_instance_data(self):
        self.volunteer_data = run_query_get_rows(
            f"SELECT * FROM User WHERE id = {self.volunteer_id}"
        )[0]

    # Edit button click
    def handle_edit_click(self):
        """Handles edit profile button click"""
        # Must handle:
        #     "own_profile" -> user_id
        #     "view_volunteer" -> volunteer_id_to_view

        current_state = self.master.get_global_state()

        if self.should_render == "view_volunteer":
            user_id = self.volunteer_id
        else:
            user_id = current_state["user_id"]

        current_state["volunteer_id_to_edit"] = user_id
        self.master.set_global_state(current_state)

        self.master.switch_to_view("profile")

    def _get_user_id_and_username_for_form(self) -> tuple[int, str]:
        """Returns user id & username or None if adding"""
        # Must handle:
        #     "own_profile"
        #     "edit_volunteer"
        #     "view_volunteer"
        #     "add_volunteer"

        if self.should_render == "own_profile":
            current_state = self.master.get_global_state()
            return current_state["user_id"], current_state["username"]

        # Everything else will be stored in instance variable, except add_volunteer
        if getattr(self, "volunteer_id", None):
            return self.volunteer_id, self.volunteer_data["username"]
        else:
            return None, None

    def _should_entries_disable(self) -> str:
        # Must handle:
        #     "own_profile"
        #     "edit_volunteer"
        #     "view_volunteer"
        #     "add_volunteer"
        if self.should_render in ["add_volunteer", "edit_volunteer"]:
            # Volunteer editing own profile should not be able to change User Details
            if self.should_render == "edit_volunteer" and not self._check_is_admin():
                self.volunteer_editing_self = True
            return "normal"
        else:
            return "disabled"

    def _get_user_profile_text(self, user_profile) -> tuple:
        is_active = config.ACTIVE if user_profile.get("is_active") else config.INACTIVE

        firstname = user_profile.get("first_name") or "No information provided"
        lastname = user_profile.get("last_name") or "No information provided"

        sex = user_profile.get("sex") or None

        phone = user_profile.get("phone_number")
        if phone is None:
            phone = "No information provided"
        languages = user_profile.get("languages_spoken")
        if languages is None:
            languages = "No information provided"
        skills = user_profile.get("skills")
        if skills is None:
            skills = "No information provided"
        emergency_contact_name = user_profile.get("emergency_contact_name")
        if emergency_contact_name is None:
            emergency_contact_name = "No information provided"
        emergency_contact_number = user_profile.get("emergency_contact_number")
        if emergency_contact_number is None:
            emergency_contact_number = "No information provided"
        campID = user_profile.get("camp_id")
        if campID is None:
            campID = "-"

        dob_year, dob_month, dob_day = user_profile.get("dob").split("-")

        return (
            is_active,
            firstname,
            lastname,
            sex,
            phone,
            languages,
            skills,
            emergency_contact_name,
            emergency_contact_number,
            campID,
            dob_year,
            dob_month,
            dob_day,
        )

    def _conditional_render_action_buttons(self, container) -> None:
        # Must handle:
        #     "own_profile"
        #     "edit_volunteer"
        #     "view_volunteer"
        #     "add_volunteer"
        if self.should_render in ["own_profile", "view_volunteer"]:
            # Section: Button to edit
            self.button_container = tk.Frame(
                master=container,
                width=50,
                height=50,
            )
            self.button_container.pack(pady=(0, 20))
            self.edit_button = tk.Button(
                master=self.button_container,
                text="Edit",
                command=self.handle_edit_click,
            )
            self.edit_button.grid(row=0, column=0)

        elif self.should_render in ["edit_volunteer", "add_volunteer"]:
            self.button_container = tk.Frame(
                master=container,
                width=50,
                height=50,
            )
            self.button_container.pack(pady=(0, 20))
            submit_button_text = (
                "Update" if self.should_render == "edit_volunteer" else "Add"
            )
            self.edit_add_button = tk.Button(
                master=self.button_container,
                text=submit_button_text,
                command=self.handle_edit_add_button_click,
            )
            self.edit_add_button.grid(row=0, column=0)

    def handle_edit_add_button_click(self):
        user_id_input = self.userID_entry.get()
        username_input = self.username_entry.get()
        camp_id_input = self.campID_entry.get()
        status_input = self.status_entry.get()
        firstname_input = self.firstname_entry.get()
        lastname_input = self.lastname_entry.get()
        dob_year_input, dob_month_input, dob_day_input = (
            self.dob_year_entry.get(),
            self.dob_month_entry.get(),
            self.dob_day_entry.get(),
        )
        dob_input = f"{dob_year_input}-{dob_month_input}-{dob_day_input}"
        sex_input = self.sex_entry.get()
        phone_input = self.phone_entry.get()
        other_languages_input = self.other_languages_entry.get()
        other_skills_input = self.other_skills_entry.get()
        emergency_contact_name_input = self.emergency_contact_name_entry.get()
        emergency_contact_number_input = self.emergency_contact_number_entry.get()

        # Group vals for ease of validation
        user_detail_values = [
            user_id_input,
            username_input,
            camp_id_input,
            status_input,
        ]
        personal_information_values = [
            firstname_input,
            lastname_input,
            dob_input,
            sex_input,
            phone_input,
            other_languages_input,
            other_skills_input,
            emergency_contact_name_input,
            emergency_contact_number_input,
        ]

        all_values = []
        all_values.extend(user_detail_values)
        all_values.extend(personal_information_values)

        # Error vars
        self.form_errors = {
            f"{field_name}": [] for field_name in self._get_all_field_names()
        }
        self.form_is_valid = True

        # Mandatory fields
        if not self._check_all_inputs_have_values(inputs_to_check=all_values):
            self._handle_invalid_form()
            return

        # SPECIFIC VALIDATION

        # username_input
        # if editing, username will always be valid
        if self.should_render != 'edit_volunteer':
            if not self._is_username_available(username=username_input):
                self.form_errors["username_input"].append("Username not available")
                self.form_is_valid = False

        # camp_id_input TODO

        # dob_input
        if not self._is_dob_valid(dob=dob_input):
            self.form_errors["dob_input"].append("Invalid date of birth")
            self.form_is_valid = False
        else:
            # Can assume this is a valid date
            if not self._is_dob_in_past(dob=dob_input):
                self.form_errors["dob_input"].append("Date of birth must be in past!")
                self.form_is_valid = False
        
        # sex_input
        # phone_input
        # other_languages_input
        # other_skills_input
        # emergency_contact_name_input
        # emergency_contact_number_input

        logging.debug(all_values, self.form_errors)
        if not self.form_is_valid:
            self._handle_invalid_form()
            return

    def _is_dob_valid(self, dob: str):
        """dob in YYYY-MM-DD format"""
        try:
            year, month, day = dob.split("-")
            date(year=int(year), month=int(month), day=int(day))
        except Exception as e:
            logging.debug(f"Invalid DoB: {e}")
            return False
        return True

    def _is_dob_in_past(self, dob: str):
        """dob in YYYY-MM-DD format"""
        year, month, day = dob.split("-")
        year, month, day = int(year), int(month), int(day)

        dob = date(year=year, month=month, day=day)

        return dob < date.today()

    def _is_username_available(self, username: str) -> bool:
        return not run_query_get_rows(f"SELECT * FROM User WHERE username='{username}'")

    def _render_error_msg_text(self) -> str:
        """Gets a formatted error message string from self.form_errors"""
        error_str = ""
        for field, field_errors in self.form_errors.items():
            if field_errors:
                error_str += self._render_field_label_from_field_key(field)
                for field_error in field_errors:
                    error_str += f"\n\t{field_error}\n"
                error_str += "\n\n"
        return error_str

    def _handle_invalid_form(self) -> None:
        error_string = self._render_error_msg_text()
        self.render_error_popup_window(title="Invalid Form", message=error_string)

    def _render_field_label_from_field_key(self, field_key: str) -> str:
        key_to_label_map = {
            "user_id_input": "User ID",
            "username_input": "Username",
            "camp_id_input": "Camp ID",
            "status_input": "Status",
            "firstname_input": "First Name",
            "lastname_input": "Last Name",
            "dob_input": "Date of Birth",
            "sex_input": "Sex",
            "phone_input": "Phone Number",
            "other_languages_input": "Other Languages",
            "other_skills_input": "Other Skills",
            "emergency_contact_name_input": "Emergency Contact Name",
            "emergency_contact_number_input": "Emergency Contact Number",
        }

        return key_to_label_map[field_key]

    def _check_all_inputs_have_values(self, inputs_to_check: list[str]) -> bool:
        """Returns True if every inputs_to_check has a value"""
        valid = True
        for ix, inp in enumerate(inputs_to_check):
            inp_stripped = inp.strip()
            if ix == 6:
                inp_stripped = inp_stripped.replace("-", "")  # dob

            if not inp_stripped:
                all_field_names = self._get_all_field_names()
                self.form_errors[all_field_names[ix]].append("Field must have a value!")
                valid = False
                self.form_is_valid = False
        return valid

    def _check_is_admin(self) -> bool:
        """Return true if admin"""
        return bool(self.master.get_global_state()["is_admin"])

    def _get_all_field_names(self) -> list[str]:
        return [
            "user_id_input",
            "username_input",
            "camp_id_input",
            "status_input",
            "firstname_input",
            "lastname_input",
            "dob_input",
            "sex_input",
            "phone_input",
            "other_languages_input",
            "other_skills_input",
            "emergency_contact_name_input",
            "emergency_contact_number_input",
        ]
