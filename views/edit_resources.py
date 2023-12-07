# Python imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Project imports
from utilities.db import run_query_get_rows, insert_query_with_values
from .base import BaseView
from constants import instructions


class EditResourcesView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.new_resources_click = 0 # To keep track of how many times add new resource button is clicked
    
        
        self.camp_id = self.master.get_global_state().get("camp_id_for_resources")
        if not self.camp_id:
            raise ValueError("camp_id_for_resources not in global state")
        
        self.render_widgets()
        
    # Add new resource button action
    def handle_add_new_resource_click(self):
        self.master.switch_to_view("new_resource")
    
    
    # Back button action
    def handle_back_click(self):
        self.master.switch_to_view("plan_detail")
        
    # Submit changes button action
    def handle_submit_edit_click(self):
        """Handles submit edit button click
        Checks if all inputs are positive integers and updates database"""
        updated_values = {}
        for resource, amount in self.edited_resources.items():
            try:
                updated_values[resource] = int(amount.get())
                if updated_values[resource] < 0:
                    messagebox.showerror("Error", "Invalid input. Please enter a positive unit.")
                    break
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter an integer.")
                break
        resourse_name_values = list(updated_values.keys())
        resourse_entry_values = list(updated_values.values())  
        # In case all values are integers, all values are taken in updated_values 
        if len(updated_values) == len(self.edited_resources):
            for i in range(len(updated_values)):
                insert_query_with_values(query = f"UPDATE CampResources SET amount = ? WHERE camp_id = ? AND name = ?",
                                values = (resourse_entry_values[i], self.camp_id, resourse_name_values[i],))
            messagebox.showinfo("Information", "Resources updated successfully.")
            self.master.switch_to_view("edit_resources")

    
    # delete resource button action        
    def handle_delete_resource_click(self, resource_id):
        # Confirm with user deletion of resource
        user_input = messagebox.askyesno("Delete resource", "Are you sure you want to delete this resource?")
        # If user confirms deletion, delete resource from database
        if user_input == True:
            insert_query_with_values(
                query="""DELETE FROM CampResources WHERE id = ?
                                    """,
                values=(resource_id,),
            )
            messagebox.showinfo("Resource deleted", "Resources deleted successfully.")
            self.master.switch_to_view("edit_resources")

        
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
            text=f"Edit resources for Camp {self.camp_id}",
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

        # Section: Resource change form
        self.resource_change_form_container = tk.LabelFrame(
             master=self.container,
             text = "Resource change form",
             width = 400,
             height = 100,
         )        
        
        self.resource_change_form_container.pack(pady=(10, 20))
        
        # Section: Buttons
        self.button_container = tk.Frame(
             master=self.container,
             width = 50,
             height = 50,
         )
        
        self.button_container.pack(pady=(0, 20)) 
        
        # Button to submit edit
        self.submit_edit_button = tk.Button(
            master=self.button_container,
            width=20,
            text="Submit changes",
            command=self.handle_submit_edit_click,
        )
        
        self.submit_edit_button.grid(row=0, column=1,)
           
        # Button to go back
        self.back_button = tk.Button(
            master=self.button_container,
            width=20,
            text="Back",
            command=self.handle_back_click,
        )
        
        self.back_button.grid(row=0, column=0,)
        
        # Gets resources for camp in form via SQL query
        camp_resources = run_query_get_rows(
            f"SELECT name, amount, id FROM CampResources WHERE camp_id = '{self.camp_id}'")
        self.camp_resources_length = len(camp_resources)      
        
        # Instructions label
        self.instructions_label = tk.Label(
            master=self.instructions_container,
            text=instructions.INSTRUCTIONS['edit_resources'],
    
            anchor = "w",
            justify = "left",
        )
        self.instructions_label.grid(
            row=0,
            column=0,
            sticky="w",
        )
        
        # Display resources
        self.edited_resources = {}
        
        self.add_resources_button = tk.Button(
            master=self.resource_change_form_container,
            width=15,
            text="+ New resource",
            anchor="w",
            command=self.handle_add_new_resource_click,
        )
        self.add_resources_button.grid(
            row=0, 
            column=0, 
            sticky = "w", 
            pady=(0, 10))
        
        
        
        if self.camp_resources_length == 0 and self.new_resources_click == 0:
            label_no_resources = tk.Label(
                master=self.resource_change_form_container,
                text="No resources found for this camp. Add resources",
                width=70,
                anchor="w",)
            label_no_resources.grid(
                row=1,
                column=0,
                sticky="w",
            )
        else:
            for i in range(self.camp_resources_length):
                label_resource = tk.Label(
                    master=self.resource_change_form_container,
                    text=camp_resources[i]["name"],
                    anchor="w",
                    width = 20,)
                label_resource.grid(
                    row=i+1,
                    column=0,
                    sticky="w",
                )

                entry_resource = tk.Entry(
                    master=self.resource_change_form_container,
                    textvariable=tk.StringVar(
                        value=camp_resources[i]["amount"],),
                    width = 50,)
                    
                entry_resource.grid(
                    row=i+1,
                    column=1,
                    )
                
                delete_resource_button = tk.Button(
                    master=self.resource_change_form_container,
                    text="Delete",
                    width = 10,
                    command=lambda resource_id=camp_resources[i]["id"]: self.handle_delete_resource_click(resource_id),
                )
                delete_resource_button.grid(
                    row=i+1,
                    column=2,
                    padx=(10, 0),
                    )
                self.edited_resources[camp_resources[i]["name"]]=entry_resource    
        
    
        
          
        
        
        
        
        
        



