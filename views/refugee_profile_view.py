# Python imports)
import logging
import tkinter as tk

# Project imports
from utilities.db import run_query_get_rows
from constants.console_color_codes import PrintColor
from .base import BaseView

class RefugeeProfileView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()
        self.master.update()

    def handle_view_click(self, camp_id: int):
        """navigates to camp detail view"""
        current_global_state = self.master.get_global_state()
        current_global_state["camp_id_to_view"] = camp_id
        self.master.set_global_state(current_global_state)
        self.master.switch_to_view("camp_detail")

    def handle_edit_click(self, refugee_id: int):
        """Navigates to edit refugee from view"""
        current_global_state = self.master.get_global_state()
        current_global_state["refugee_id_to_edit"] = refugee_id
        self.master.set_global_state(current_global_state)
        self.master.switch_to_view("add_edit_refugee")
 

    def render_widgets(self) -> None:
        """Renders widgets for refugee profile view"""
        
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
            text=f"REFUGEE PROFILE",
            font=(60),
        )
        self.header.grid(
            row=0,
            column=5,
            pady=10,
        )

       # Refugee profile variables
        
        refugee_family_id = self.master.get_global_state().get("refugee_id_to_view")  
        refugee_family_data = run_query_get_rows(f"SELECT * FROM RefugeeFamily WHERE id = '{refugee_family_id}'")[0]

        main_rep_name = refugee_family_data.get("main_rep_name")
        if main_rep_name is None:
            main_rep_name = "No information provided"

        medical_conditions = refugee_family_data.get("medical_conditions")
        if medical_conditions is None:
            medical_conditions = "No information provided"

        n_adults = refugee_family_data.get("n_adults")
        if n_adults is None:
            n_adults = "No information provided"

        n_children = refugee_family_data.get("n_children")
        if n_children is None:
            n_children = "No information provided"

        main_rep_home_town = refugee_family_data.get("main_rep_home_town")
        if main_rep_home_town is None:
            main_rep_home_town = "No information provided"

        main_rep_age = refugee_family_data.get("main_rep_age")
        if main_rep_age is None:
            main_rep_age = "No information provided"

        main_rep_sex = refugee_family_data.get("main_rep_sex")
        if main_rep_sex is None:
            main_rep_sex = "No information provided"
        elif main_rep_sex == "F":
            main_rep_sex = "Female"
        elif main_rep_sex == "M":
            main_rep_sex = "Male"

        n_missing_members = refugee_family_data.get("n_missing_members")
        if n_missing_members is None:
            n_missing_members = "No information provided"

        is_in_camp = refugee_family_data.get("is_in_camp")
        if is_in_camp == 1:
            is_in_camp_value = "YES"
        elif is_in_camp == 0:
            is_in_camp_value = "NO"

        # Camp details variables
        camp_id = refugee_family_data.get("camp_id")
        camp_data = run_query_get_rows(f"SELECT * FROM Camp WHERE id = '{camp_id}'")[0]
        camp_location = camp_data.get("location")
        if camp_location is None:
            camp_location = "No information provided"
        

        # Section: Refugee family details
        self.refugee_details_label_container = tk.LabelFrame(
            master=self.container,
            text="Refugee Family Details",
            width=500,
            height=300,
        )

        # Section: Edit Button
        self.button_container = tk.Frame(
            master=self.container,
            width = 50,
            height = 50,
        )  

        # Section: Back Button
        self.back_button_container = tk.Frame(
            master=self.container,
            width = 10,
            height = 50,
        )

        # Set up - labels and entries:

        self.refugee_family_id_label = tk.Label(
            master=self.refugee_details_label_container,
            text=f"Refugee Family ID:",
            width=20,
            anchor="w",
        )

        self.refugee_family_id_entry = tk.Entry(
            master=self.refugee_details_label_container,
            width=70,
            state="disabled",
            text=tk.StringVar(value=refugee_family_id),
        )

        self.location_label = tk.Label(
            master=self.refugee_details_label_container,
            text="Camp Location",
            width=20,
            anchor="w",
        )

        self.location_entry = tk.Entry(
            master=self.refugee_details_label_container,
            width=70,
            state="disabled",
            text=tk.StringVar(value=camp_location),
        )
        
        # Main rep name
        self.main_rep_name_label = tk.Label(
            master=self.refugee_details_label_container,
            text="Main Rep Name",
            width=20,
            anchor="w",
        )

        self.main_rep_name_entry = tk.Entry(
            master=self.refugee_details_label_container,
            width=70,
            state="disabled",
            text=tk.StringVar(value=main_rep_name),
        )

        # Main rep age
        self.main_rep_age_label = tk.Label(
            master=self.refugee_details_label_container,
            text="Main Rep Age",
            width=20,
            anchor="w",
        )

        self.main_rep_age_entry = tk.Entry(
            master=self.refugee_details_label_container,
            width=70,
            state="disabled",
            text=tk.StringVar(value=main_rep_age),
        )

        # Main Rep Home Town
        self.main_rep_home_town_label = tk.Label(
            master=self.refugee_details_label_container,
            text="Main Rep Home Town",
            width=20,
            anchor="w",
        )

        self.main_rep_home_town_entry = tk.Entry(
            master=self.refugee_details_label_container,
            width=70,
            state="disabled",
            text=tk.StringVar(value=main_rep_home_town),
        )

        # Number of Adults
        self.n_adults_label = tk.Label(
            master=self.refugee_details_label_container,
            text="No. of Adults",
            width=20,
            anchor="w",
        )

        self.n_adults_entry = tk.Entry(
            master=self.refugee_details_label_container,
            width=70,
            state="disabled",
            text=tk.StringVar(value=n_adults),
        )

        # Number of Children
        self.n_children_label = tk.Label(
            master=self.refugee_details_label_container,
            text="No. of Children",
            width=20,
            anchor="w",
        )

        self.n_children_entry = tk.Entry(
            master=self.refugee_details_label_container,
            width=70,
            state="disabled",
            text=tk.StringVar(value=n_children),
        )

        # Number of Missing Members
        self.n_missing_members_label = tk.Label(
            master=self.refugee_details_label_container,
            text="No. of Missing Members",
            width=20,
            anchor="w",
        )

        self.n_missing_members_entry = tk.Entry(
            master=self.refugee_details_label_container,
            width=70,
            state="disabled",
            text=tk.StringVar(value=n_missing_members),
        )

        # Medical Conditions
        self.medical_conditions_label = tk.Label(
            master=self.refugee_details_label_container,
            text="Medical Conditions",
            width=20,
            anchor="w",
        )

        self.medical_conditions_entry = tk.Entry(
            master=self.refugee_details_label_container,
            width=70,
            state="disabled",
            text=tk.StringVar(value=medical_conditions),
        )

        # Is in Camp
        self.is_in_camp_label = tk.Label(
            master=self.refugee_details_label_container,
            text="Residing in Camp",
            width=20,
            anchor="w",
        )

        # Assuming 1 means 'YES' and 0 means 'NO'
        is_in_camp_value = "YES" if is_in_camp == 1 else "NO"

        self.is_in_camp_entry = tk.Entry(
            master=self.refugee_details_label_container,
            width=70,
            state="disabled",
            text=tk.StringVar(value=is_in_camp_value),
        )

        # Edit button
        self.edit_button = tk.Button(
            master=self.button_container,
            width=30,
            text="Edit",
            command=lambda: self.handle_edit_click(refugee_family_data.get("id")),
            fg="white",
            bg="blue",
        )

        # Back button
        self.back_button = tk.Button(
            master=self.back_button_container,
            command=lambda: self.handle_view_click(camp_id),
            width=10,
            text="BACK",
            fg="white",
            bg="black",
        )

        
        

        # Add to grid
        self.refugee_details_label_container.pack(pady=(10, 20))
        self.button_container.pack(pady=(0, 20))
        self.back_button_container.pack(pady=(0,20))

        self.refugee_family_id_label.grid(row=0, column=0)
        self.refugee_family_id_entry.grid(row=0, column=1)

        self.main_rep_name_label.grid(row=1, column=0)
        self.main_rep_name_entry.grid(row=1, column=1)

        self.main_rep_age_label.grid(row=2, column=0)
        self.main_rep_age_entry.grid(row=2, column=1)

        self.main_rep_home_town_label.grid(row=3, column=0)
        self.main_rep_home_town_entry.grid(row=3, column=1)

        self.n_adults_label.grid(row=4, column=0)
        self.n_adults_entry.grid(row=4, column=1)

        self.n_children_label.grid(row=5, column=0)
        self.n_children_entry.grid(row=5, column=1)

        self.n_missing_members_label.grid(row=6, column=0)
        self.n_missing_members_entry.grid(row=6, column=1)

        self.medical_conditions_label.grid(row=7, column=0)
        self.medical_conditions_entry.grid(row=7, column=1)

        self.is_in_camp_label.grid(row=8, column=0)
        self.is_in_camp_entry.grid(row=8, column=1)

        self.location_label.grid(row=9, column=0)
        self.location_entry.grid(row=9, column=1)
    

        self.edit_button.grid(row=0, column=0,)
        self.back_button.grid(row=0, column=0,)

        
        

        # Add to grid
        self.refugee_details_label_container.pack(pady=(10, 20))
        self.button_container.pack(pady=(0, 20))
        self.back_button_container.pack(pady=(0,20))

        self.refugee_family_id_label.grid(row=0, column=0)
        self.refugee_family_id_entry.grid(row=0, column=1)

        self.main_rep_name_label.grid(row=1, column=0)
        self.main_rep_name_entry.grid(row=1, column=1)

        self.main_rep_age_label.grid(row=2, column=0)
        self.main_rep_age_entry.grid(row=2, column=1)

        self.main_rep_home_town_label.grid(row=3, column=0)
        self.main_rep_home_town_entry.grid(row=3, column=1)

        self.n_adults_label.grid(row=4, column=0)
        self.n_adults_entry.grid(row=4, column=1)

        self.n_children_label.grid(row=5, column=0)
        self.n_children_entry.grid(row=5, column=1)

        self.n_missing_members_label.grid(row=6, column=0)
        self.n_missing_members_entry.grid(row=6, column=1)

        self.medical_conditions_label.grid(row=7, column=0)
        self.medical_conditions_entry.grid(row=7, column=1)

        self.is_in_camp_label.grid(row=8, column=0)
        self.is_in_camp_entry.grid(row=8, column=1)

        self.location_label.grid(row=9, column=0)
        self.location_entry.grid(row=9, column=1)
    

        self.edit_button.grid(row=0, column=0,)
        self.back_button.grid(row=0, column=0,)

    
