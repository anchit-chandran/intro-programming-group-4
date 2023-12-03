import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Project imports
from constants import config
from utilities.db import run_query_get_rows, insert_query_with_values
from .base import BaseView


class NewResourceView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.new_resources_click = 0 # To keep track of how many times add new resource button is clicked
    
        
        self.camp_id = self.master.get_global_state().get("camp_id_for_resources")
        if not self.camp_id:
            raise ValueError("camp_id_for_resources not in global state")
        
        self.render_widgets()
        
    def get_resources_for_camp(self, camp_id):
        """Gets resources for camp in form [(resource_name)]"""
        resources = run_query_get_rows(
            f"""
            SELECT
                name
            FROM
                CampResources
            WHERE
                camp_id = '{camp_id}'
        """
        )
        return [resource["name"] for resource in resources]
        

    # Back button action
    def handle_back_click(self):
        self.master.switch_to_view("edit_resources")
        
    # Submit changes button action
    def handle_submit_new_resource_click(self, resource_name, resource_amount):
        """Handles submit new resource button click
        ---"""
        resource_names = self.get_resources_for_camp(self.camp_id)
        resource_name = resource_name.get()
        resource_amount = resource_amount.get()
            
        # Check amount if it is positive integer and submit query
        try:
            if resource_name == "" or resource_amount == "":
                messagebox.showerror("Error", "Please fill all entries.")
            else:            
                # Clean up resource name
                if resource_name[-1] == " ": # in case there is a space left behind
                    resource_name = resource_name[:-1]
                resource_name = resource_name[0].capitalize() + resource_name[1:].lower()
            
                # check if resource name already exists and reject entry if it does
                for resource in resource_names:
                    if resource_name == resource:
                        messagebox.showerror("Error", "Resource already exists. Please enter a new resource type.")
                        return
                    
                resource_amount = int(resource_amount)
                if resource_amount < 0:
                    messagebox.showerror("Error", "Invalid input. Please enter a positive unit.")
                elif resource_amount == 0:
                    messagebox.showerror("Error", "No need to record empty resources.")
                else:
                    insert_query_with_values(query = f"INSERT INTO CampResources (name, amount, camp_id) VALUES (?, ?, ?)",
                                        values = (resource_name, resource_amount, self.camp_id,))
                    messagebox.showinfo("Information", "Resources updated successfully.")
                    self.master.switch_to_view("edit_resources")
        except Exception as e:
            messagebox.showerror("Error", "Invalid input. Please enter an integer.")
        

        

        
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
            text=f"Add a resource for Camp {self.camp_id}",
            font=(60),
        )
        self.header.grid(
            row=0,
            column=5,
            pady=10,
            )
        
        # Section: Instructions for view
        self.instructions_container = ttk.LabelFrame(
             master=self.container,
             text = "Instructions",
             width = 400,
             height = 50,
         )
        
        self.instructions_container.pack(pady=(10, 20))

        # Section: Add resource change form
        self.resource_change_form_container = tk.LabelFrame(
             master=self.container,
             text = "Add resource form",
             width = 400,
             height = 100,
         )        
        
        self.resource_change_form_container.pack(pady=(10, 20))
        
        # Display fields to add new resources
        label_name = tk.Label(
                    master=self.resource_change_form_container,
                    text="New resource name:",
                    anchor="w",
                    width=35,
                    )
        label_name.grid(
                    row=0,
                    column=0,
                    )
        label_amount = tk.Label(
                    master=self.resource_change_form_container,
                    text="Amount:",
                    anchor="w",
                    width=35,
                    )
        label_amount.grid(
                    row=0,
                    column=1,)
        
        # Set char length limit
        resource_name = tk.StringVar()
        resource_name.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=resource_name, char_limit=20,
            ),
        )
        entry_new_resource_name = tk.Entry(
                master=self.resource_change_form_container,
                width=35,
                textvariable=resource_name
                )
        entry_new_resource_name.grid(
                row=1,
                column=0,
                padx=(2, 10),
                pady=(0, 10),
                sticky="w",
                )
        entry_new_resource_amount = tk.Entry(
                master=self.resource_change_form_container,
                width=35,
                )
        entry_new_resource_amount.grid(
                row=1,
                column=1,
                padx=(0, 2),
                pady=(0, 10),
                sticky="w",
                )
        
        
        # Section: Buttons
        self.button_container = tk.Frame(
             master=self.container,
             width = 50,
             height = 50,
         )
        
        self.button_container.pack(pady=(0, 20)) 
        
        # Button to submit new resource
        self.submit_new_resource_button = tk.Button(
            master=self.button_container,
            width=20,
            text="Submit new resource",
            command=lambda: self.handle_submit_new_resource_click(entry_new_resource_name, entry_new_resource_amount),
        )
        
        self.submit_new_resource_button.grid(row=0, column=0,)
           
        # Button to go back
        self.back_button = tk.Button(
            master=self.button_container,
            width=20,
            text="Back",
            command=self.handle_back_click,
        )
        
        self.back_button.grid(row=0, column=1,)   
        
        # Instructions label
        self.instructions_label = tk.Label(
            master=self.instructions_container,
            text="---Input---\nCreate a new resource below.\n\nThe new resource should not duplicate with resources you already have.\nResource name can be a max of 20 characters.\n\nUnits must be positive integers. \n\n ---Submit---\nClick 'Submit new resource' to create the new resource.",
            anchor = "w",
            justify = "left",
        )
        self.instructions_label.grid(
            row=0,
            column=0,
            sticky="w",
        )
        
        
        