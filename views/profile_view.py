# Python imports
import logging
import tkinter as tk

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from views.base import BaseView
from constants import config


class ProfileView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        logging.debug(self.master.get_global_state())
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
        status_profile = ""
        firstname = ""
        lastname = ""
        sex = ""
        phone = ""
        languages = ""
        skills = ""
        emergency_contact_name = ""
        emergency_contact_number = ""
        campID = ""
        DOB = ""
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
                DOB,
            ) = self._get_user_profile_text(user_profile)

        # Section : User details (userID, campID, username, status)
        self.user_details_label_container = tk.LabelFrame(
            master=self.container,
            text="User Details",
            width=400,
            height=50,
        )

        # Section: Personal info (firstname, lastname, DOB, sex, phone...)
        self.personal_info_label_container = tk.LabelFrame(
            master=self.container,
            text="Personal information",
            width=400,
            height=100,
        )

        # Section: Emergency contact
        self.emergency_label_container = tk.LabelFrame(
            master=self.container,
            text="Emergency contact",
            width=400,
            height=50,
        )

        # Section: Button to edit
        self.button_container = tk.Frame(
            master=self.container,
            width=50,
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

        self.userID_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state=state,
            textvariable=tk.StringVar(value=user_id),
        )

        self.username_label = tk.Label(
            master=self.user_details_label_container,
            text="Username",
            width=10,
        )

        self.username_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state=state,
            textvariable=tk.StringVar(value=username),
        )

        self.campID_label = tk.Label(
            master=self.user_details_label_container,
            text="Camp ID",
            width=10,
        )

        self.campID_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state=state,
            text=tk.StringVar(value=campID),
        )

        self.status_label = tk.Label(
            master=self.user_details_label_container,
            text="Status",
            width=10,
        )

        self.status_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state=state,
            text=tk.StringVar(value=status_profile),
        )

        self.firstname_label = tk.Label(
            master=self.personal_info_label_container,
            text="First name",
            width=20,
            anchor="w",
        )

        self.firstname_entry = tk.Entry(
            master=self.personal_info_label_container,
            width=70,
            state=state,
            text=tk.StringVar(value=firstname),
        )

        self.lastname_label = tk.Label(
            master=self.personal_info_label_container,
            text="Last name",
            width=20,
            anchor="w",
        )

        self.lastname_entry = tk.Entry(
            master=self.personal_info_label_container,
            width=70,
            state=state,
            text=tk.StringVar(value=lastname),
        )

        self.dob_label = tk.Label(
            master=self.personal_info_label_container,
            text="Date of birth",
            width=20,
            anchor="w",
        )

        self.dob_entry = tk.Entry(
            master=self.personal_info_label_container,
            width=70,
            state=state,
            text=tk.StringVar(value=DOB),
        )

        self.sex_label = tk.Label(
            master=self.personal_info_label_container,
            text="Gender",
            width=20,
            anchor="w",
        )

        self.sex_entry = tk.Entry(
            master=self.personal_info_label_container,
            width=70,
            state=state,
            text=tk.StringVar(value=sex),
        )

        self.phone_label = tk.Label(
            master=self.personal_info_label_container,
            text="Phone number",
            width=20,
            anchor="w",
        )

        self.phone_entry = tk.Entry(
            master=self.personal_info_label_container,
            width=70,
            state=state,
            text=tk.StringVar(value=phone),
        )

        self.other_languages_label = tk.Label(
            master=self.personal_info_label_container,
            text="Languages spoken",
            width=20,
            anchor="w",
        )

        self.other_languages_entry = tk.Entry(
            master=self.personal_info_label_container,
            width=70,
            state=state,
            text=tk.StringVar(value=languages),
        )

        self.other_skills_label = tk.Label(
            master=self.personal_info_label_container,
            text="Skills",
            width=20,
            anchor="w",
        )

        self.other_skills_entry = tk.Entry(
            master=self.personal_info_label_container,
            width=70,
            state=state,
            text=tk.StringVar(value=skills),
        )

        self.emergency_contact_name_label = tk.Label(
            master=self.emergency_label_container,
            text="Contact name",
            width=20,
            anchor="w",
        )

        self.emergency_contact_name_entry = tk.Entry(
            master=self.emergency_label_container,
            width=70,
            state=state,
            text=tk.StringVar(value=emergency_contact_name),
        )

        self.emergency_contact_number_label = tk.Label(
            master=self.emergency_label_container,
            text="Contact phone number",
            width=20,
            anchor="w",
        )

        self.emergency_contact_number_entry = tk.Entry(
            master=self.emergency_label_container,
            width=70,
            state=state,
            text=tk.StringVar(value=emergency_contact_number),
        )

        self.edit_button = tk.Button(
            master=self.button_container,
            width=30,
            text="Edit",
            fg="white",
            bg="blue",
            command=self.handle_edit_click,
        )

        # Add to grid
        self.user_details_label_container.pack(pady=(10, 20))
        self.personal_info_label_container.pack(pady=(10, 20))
        self.emergency_label_container.pack(pady=(10, 20))
        self.button_container.pack(pady=(0, 20))

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
        self.dob_entry.grid(
            row=2,
            column=1,
        )

        self.sex_label.grid(
            row=3,
            column=0,
        )
        self.sex_entry.grid(
            row=3,
            column=1,
        )

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

        self.edit_button.grid(
            row=0,
            column=0,
        )

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
        print("editing with ", self.master.get_global_state())

    def _get_user_id_and_username_for_form(self) -> tuple[int,str]:
        """Returns user id & username or None if adding"""
        # Must handle:
        #     "own_profile"
        #     "edit_volunteer"
        #     "view_volunteer"
        #     "add_volunteer"

        if self.should_render == "own_profile":
            current_state = self.master.get_global_state()
            return current_state["user_id"], current_state['username']

        # Everything else will be stored in instance variable, except add_volunteer
        if getattr(self, "volunteer_id", None):
            return self.volunteer_id, self.volunteer_data['username']
        else:
            return None, None

    def _should_entries_disable(self) -> str:
        # Must handle:
        #     "own_profile"
        #     "edit_volunteer"
        #     "view_volunteer"
        #     "add_volunteer"
        if self.should_render in ['add_volunteer','edit_volunteer']:
            return 'normal'
        else:
            return 'disabled'
    
    def _get_user_profile_text(self, user_profile) -> tuple:
        is_active = user_profile.get("is_active")
        if is_active == 1:
            status_profile = "Active"
        elif is_active == 0:
            status_profile = "Deactivated"
        firstname = user_profile.get("first_name")
        if firstname is None:
            firstname = "No information provided"
        lastname = user_profile.get("last_name")
        if lastname is None:
            lastname = "No information provided"
        sex = user_profile.get("sex")
        if sex is None:
            sex = "No information provided"
        elif sex == "F":
            sex = "Female"
        elif sex == "M":
            sex = "Male"
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
        DOB = user_profile.get("dob")
        if DOB is None:
            DOB = "No information provided"
        else:
            DOB, DOB_time = DOB.split(" ")

        return (
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
            DOB,
        )
