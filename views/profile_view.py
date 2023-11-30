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
        self.render_widgets()
        self.master.update()

       # Edit button click
    def handle_edit_click(self):
        """Handles edit profile button click"""
        self.master.switch_to_view("add_edit_user_profile")

            
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
        
        self.header = tk.Label(
            master=self.header_container,
            text=f"PROFILE VIEW {self.master.get_global_state().get('username')}! 👋",
            font=(60),
        )
        self.header.grid(
            row=0,
            column=5,
            pady=10,
            )

        # User profile variables
        userID = self.master.get_global_state().get('user_id')
        username = self.master.get_global_state().get('username')
        user_profile = run_query_get_rows(f"SELECT * FROM User WHERE id = '{userID}'")[0]
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
                      
        # Section : User details (userID, campID, username, status)
        self.user_details_label_container = tk.LabelFrame(
             master=self.container,
             text = "User Details",
             width = 400,
             height = 50,
         )
   
        
        # Section: Personal info (firstname, lastname, DOB, sex, phone...)
        self.personal_info_label_container = tk.LabelFrame(
             master=self.container,
             text = "Personal information",
             width = 400,
             height = 100,
         )

        # Section: Emergency contact
        self.emergency_label_container = tk.LabelFrame(
             master=self.container,
             text = "Emergency contact",
             width = 400,
             height = 50,
         )        
        
        # Section: Button to edit
        self.button_container = tk.Frame(
             master=self.container,
             width = 50,
             height = 50,
         )         
        
              
        # Set up - labels and entries
        self.userID_label = tk.Label(
            master=self.user_details_label_container,
            text="User ID",
            width=10,
            )
        
        self.userID_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state="disabled",
            textvariable=tk.StringVar(value=userID),
            )
        
        self.username_label = tk.Label(
            master=self.user_details_label_container,
            text="Username",
            width=10,
            )
        
        self.username_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state="disabled",
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
            state="disabled",
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
            state="disabled",
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
            state="disabled",
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
            state="disabled",
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
            state="disabled",
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
            state="disabled",
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
            state="disabled",
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
            state="disabled",
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
            state="disabled",
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
            state="disabled",
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
            state="disabled",
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
        
        self.userID_label.grid(row=0, column=0,)
        self.userID_entry.grid(row=0, column=1,)

        self.username_label.grid(row=0, column=2,)
        self.username_entry.grid(row=0, column=3,)

        self.campID_label.grid(row=0, column=4,)
        self.campID_entry.grid(row=0, column=5,)
        
        self.status_label.grid(row=0, column=6,)
        self.status_entry.grid(row=0, column=7,)
        
        self.firstname_label.grid(row=0, column=0,)
        self.firstname_entry.grid(row=0, column=1,)
        
        self.lastname_label.grid(row=1, column=0,)
        self.lastname_entry.grid(row=1, column=1,)

        self.dob_label.grid(row=2, column=0,)
        self.dob_entry.grid(row=2, column=1,)

        self.sex_label.grid(row=3, column=0,)
        self.sex_entry.grid(row=3, column=1,)

        self.phone_label.grid(row=4, column=0,)
        self.phone_entry.grid(row=4, column=1,)
        
        self.other_languages_label.grid(row=5, column=0,)
        self.other_languages_entry.grid(row=5, column=1,)
        
        self.other_skills_label.grid(row=6, column=0,)
        self.other_skills_entry.grid(row=6, column=1,)
        
        self.emergency_contact_name_label.grid(row=0, column=0,)
        self.emergency_contact_name_entry.grid(row=0, column=1,)
        
        self.emergency_contact_number_label.grid(row=1, column=0,)
        self.emergency_contact_number_entry.grid(row=1, column=1,)
        
        self.edit_button.grid(row=0, column=0,)
    
    
    

