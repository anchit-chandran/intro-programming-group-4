# Python imports
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

       

        # Assuming you have a way to identify the refugee family, for example, the family ID
        refugee_family_id = 1  # Replace with the actual family ID
        
        # Fetch data from the database based on the family ID
        refugee_family_data = run_query_get_rows(
            f"SELECT * FROM RefugeeFamily WHERE id = {refugee_family_id}"
        )

        if refugee_family_data:
            refugee_family_data = refugee_family_data[0]

            # Extract relevant information from the fetched data
            main_rep_name = refugee_family_data.get("main_rep_name", "No information provided")
            medical_conditions = refugee_family_data.get("medical_conditions", "No information provided")
            n_adults = refugee_family_data.get("n_adults", "No information provided")
            n_children = refugee_family_data.get("n_children", "No information provided")
            main_rep_home_town = refugee_family_data.get("main_rep_home_town", "No information provided")
            main_rep_age = refugee_family_data.get("main_rep_age", "No information provided")
            main_rep_sex = refugee_family_data.get("main_rep_sex", "No information provided")
            n_missing_members = refugee_family_data.get("n_missing_members", "No information provided")
            is_in_camp = refugee_family_data.get("is_in_camp", "No information provided")



             # Camp Details Frame (newly added)
            self.camp_details_label_container = tk.LabelFrame(
                master=self.container,
                text="Camp Details",
                width=400,
                height=50,
            )

             # Fetch camp details based on the camp ID from refugee family data
            camp_id = refugee_family_data.get("camp_id", None)
            camp_data = run_query_get_rows(
                f"SELECT * FROM Camp WHERE id = {camp_id}"
            )

        if camp_data:
            camp_data = camp_data[0]

            # Extract relevant information from the fetched camp data
            refugee_family_id_label = tk.Label(
                master=self.camp_details_label_container,
                text=f"Refugee Family ID: {refugee_family_id}",
                width=20,
                anchor="w",
            )

            camp_id_label = tk.Label(
                master=self.camp_details_label_container,
                text=f"Camp ID: {camp_id}",
                width=10,
                anchor="w",
            )

            location_label = tk.Label(
                master=self.camp_details_label_container,
                text=f"Location: {camp_data.get('location', 'No information provided')}",
                width=20,
                anchor="w",
            )

            # Section: Display refugee family details
            self.refugee_details_label_container = tk.LabelFrame(
                master=self.container,
                text="Refugee Family Details",
                width=400,
                height=300,
            )

             # Section: Button to edit
            self.button_container = tk.Frame(
                master=self.container,
                width = 50,
                height = 50,
            )  

            # Set up - labels and entries:
            # main rep name
            self.main_rep_name_label = tk.Label(
                master=self.refugee_details_label_container,
                text="Main Representative Name",
                width=20,
                anchor="w",
            )

            self.main_rep_name_entry = tk.Entry(
                master=self.refugee_details_label_container,
                width=70,
                state="disabled",
                text=tk.StringVar(value=main_rep_name),
            )

            # main rep age
            self.main_rep_age_label = tk.Label(
                master=self.refugee_details_label_container,
                text="Main Representative Age",
                width=20,
                anchor="w",
            )

            self.main_rep_age_entry = tk.Entry(
                master=self.refugee_details_label_container,
                width=70,
                state="disabled",
                text=tk.StringVar(value=main_rep_age),
            )

            # Main Representative Home Town
            self.main_rep_home_town_label = tk.Label(
                master=self.refugee_details_label_container,
                text="Main Representative Home Town",
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
                text="Number of Adults",
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
                text="Number of Children",
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
                text="Number of Missing Members",
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
                text="Is in Camp",
                width=20,
                anchor="w",
            )

            self.is_in_camp_entry = tk.Entry(
                master=self.refugee_details_label_container,
                width=70,
                state="disabled",
                text=tk.StringVar(value=is_in_camp),
            )

            self.edit_button = tk.Button(
                master=self.button_container,
                width=30,
                text="Edit",
                fg="white",
                bg="blue",
            )

            # Add to grid
            self.camp_details_label_container.pack(pady=(10, 20))
            self.refugee_details_label_container.pack(pady=(10, 20))
            self.button_container.pack(pady=(0, 20))

            self.main_rep_name_label.grid(row=0, column=0)
            self.main_rep_name_entry.grid(row=0, column=1)

            self.main_rep_age_label.grid(row=1, column=0)
            self.main_rep_age_entry.grid(row=1, column=1)

            self.main_rep_home_town_label.grid(row=2, column=0)
            self.main_rep_home_town_entry.grid(row=2, column=1)

            self.n_adults_label.grid(row=3, column=0)
            self.n_adults_entry.grid(row=3, column=1)

            self.n_children_label.grid(row=4, column=0)
            self.n_children_entry.grid(row=4, column=1)

            self.n_missing_members_label.grid(row=5, column=0)
            self.n_missing_members_entry.grid(row=5, column=1)

            self.medical_conditions_label.grid(row=6, column=0)
            self.medical_conditions_entry.grid(row=6, column=1)

            self.is_in_camp_label.grid(row=7, column=0)
            self.is_in_camp_entry.grid(row=7, column=1)

            self.edit_button.grid(row=0, column=0,)

            refugee_family_id_label.grid(row=0, column=0)
            camp_id_label.grid(row=0, column=1)
            location_label.grid(row=0, column=2)

        

        else:
            # Display a message if no data is found
            no_data_label = tk.Label(
                master=self.container,
                text="No information available for this refugee family.",
                font=(14),
                fg="red",
            )
            no_data_label.pack(pady=20)