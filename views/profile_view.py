# Python imports
import logging
import tkinter as tk

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from .base import BaseView


class ProfileView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()

    def render_widgets(self) -> None:
        """Renders widgets for view"""
        
        # Create container
        self.container = tk.Frame(
            master=self,
            width=500,
            height=300,
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
        sex = user_profile.get("last_name")
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
            campID = "No information provided" 
        DOB = user_profile.get("dob")
        if DOB is None:
            DOB = "No information provided" 
        else:
            DOB, DOB_time = DOB.split(" ")
                      
        self.user_details_label_container = tk.LabelFrame(
             master=self.container,
             text = "User Details",
             width = 200,
             height = 50,
         )
        self.user_details_label_container.pack(side="left", padx=(0, 10))

        self.userID_label = tk.Label(
            master=self.user_details_label_container,
            text="User ID",
            )
        
        self.userID_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state="disabled",
            textvariable=tk.StringVar(value=userID),
            )
        
        self.username_label = tk.Label(
            master=self.user_details_label_container,
            text="Username",)
        
        self.username_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state="disabled",
            textvariable=tk.StringVar(value=username),
            )        
        
        self.campID_label = tk.Label(
            master=self.user_details_label_container,
            text="Camp ID",)
        
        self.campID_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state="disabled",
            text=tk.StringVar(value=campID),
            )
        
        self.status_label = tk.Label(
            master=self.user_details_label_container,
            text="Status",)
        
        self.status_entry = tk.Entry(
            master=self.user_details_label_container,
            width=10,
            state="disabled",
            text=tk.StringVar(value=status_profile),
            )
                
        self.userID_label.grid(row=0, column=0,)
        self.userID_entry.grid(row=0, column=1,)

        self.username_label.grid(row=0, column=2,)
        self.username_entry.grid(row=0, column=3,)

        self.campID_label.grid(row=0, column=4,)
        self.campID_entry.grid(row=0, column=5,)
        
        self.status_label.grid(row=0, column=6,)
        self.status_entry.grid(row=0, column=7,)
        # 
        # self.user_details = tk.Label(
        #     master=self.user_details_container,
        #     text="User Details",
        #     font=(30),
        # )
        # self.user_details.grid(
        #     row=1,
        #     column=0,
        # )
        # 
# self.user_id_label = tk.Label(
#     master=self.user_details_container,
#     text="User ID",
#     font=(5),
# )
# self.user_id_label.grid(
#     row=2,
#     column=0,
# )
# 
# self.username_label = tk.Label(
#     master=self.user_details_container,
#     text="Username",
#     font=(5),
# )
# self.username_label.grid(
#     row=2,
#     column=2,
# )
# 
# self.camp_id_label = tk.Label(
#     master=self.user_details_container,
#     text="Camp ID",
#     font=(5),
# )
# self.camp_id_label.grid(
#     row=2,
#     column=4,
# )
# 

        # Personal information section
#        self.user_personal_info_container = tk.Frame(
#            master=self.container,
#            width=200,
#            height=50,
#        )
#        self.user_personal_info_container.pack(side="left", padx=(0,10))
#
#        self.user_personal_info = tk.Label(
#            master=self.user_personal_info_container,
#            text="Personal information",
#            font=(30),
#        )
#        self.user_personal_info.grid(
#            row=2,
#            column=0,
#            pady=10
#        )
        
        # Emergency Contact section
#        self.user_emerg_contact_container = tk.Frame(
#            master=self.container,
#            width=200,
#            height=50,
#        )
#        self.user_emerg_contact_container.pack(side ="right", padx=(0,10))

#        self.user_emerg_contact = tk.Label(
#            master=self.user_emerg_contact_container,
#            text="Emergency contact",
#            font=(30),
#        )
#        self.user_emerg_contact.grid(
#            row=2,
#            column=0,
#            pady = 10,
#        )
#        
        # Other
#        self.user_other_container = tk.Frame(
#            master=self.container,
#            width=200,
#            height=50,
#        )
#        self.user_other_container.pack(side ="left", padx=(0,10))

#        self.user_other = tk.Label(
#            master=self.user_emerg_contact_container,
#            text="Other information",
#            font=(30),
#        )
#        self.user_other.grid(
#            row=3,
#            column=0,
#            pady = 10,
#        )