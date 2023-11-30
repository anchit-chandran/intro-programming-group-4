# Python imports
import logging
import tkinter as tk
from tkinter import messagebox
import datetime
import re

# Project imports
from constants import config
from utilities.db import run_query_get_rows, insert_query_with_values
from utilities.validators import is_valid_email
from .base import BaseView


class EditResourcesView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.new_resources_click = 0 # To keep track of how many times add new resource button is clicked
    
        
        self.camp_id = self.master.get_global_state().get("camp_id_for_resources")
        if not self.camp_id:
            raise ValueError("camp_id_for_resources not in global state")
        
        self.render_widgets()
    
    def handle_add_resources_click(self, new_resources_click, camp_resources_length):
        self.new_resources_click += 1
        if self.new_resources_click == 1:
            label_name = tk.Label(
                    master=self.resources_container,
                    text="New resource name:",)
            label_name.grid(
                    row=camp_resources_length + 1 + new_resources_click,
                    column=0,)
            label_amount = tk.Label(
                    master=self.resources_container,
                    text="Amount:",)
            label_amount.grid(
                    row=camp_resources_length + 1 + new_resources_click,
                    column=1,)
        entry_new_resource_name = tk.Entry(
                master=self.resources_container,
                width=20,)
        entry_new_resource_name.grid(
                row=camp_resources_length + 2 + new_resources_click,
                column=0,)
        entry_new_resource_amount = tk.Entry(
                master=self.resources_container,
                width=20,)
        entry_new_resource_amount.grid(
                row=camp_resources_length + 2 + new_resources_click,
                column=1,)
        
    
    def handle_back_click(self):
        self.master.switch_to_view("plan_detail")
    
    
    def handle_submit_edit_click(self):
        """Handles submit edit button click
        Checks if all inputs are integers and updates database"""
        updated_values = {}
        for resource, amount in self.edited_resources.items():
            try:
                updated_values[resource] = int(amount.get())
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
            pady=100,
        )

        # Header
        self.header_container = tk.Frame(self.container)
        self.header_container.pack(pady=15, fill="x", expand=True)

        self.header = tk.Label(
            master=self.header_container,
            text=f"Edit resources for Camp {self.camp_id}",
            font=(60),
        )
        self.header.pack(
            side="left",
        )
        
        # Gets resources for camp in form [(resource_name, resource_amount)] via SQL query
        camp_resources = run_query_get_rows(
            f"SELECT name, amount FROM CampResources WHERE camp_id = '{self.camp_id}'")
        self.camp_resources_length = len(camp_resources)
        
        # Section: display resources
        self.resources_container = tk.Frame(
            master=self.container,
        )

        # Section: Button to submit edit
        self.button_container = tk.Frame(
             master=self.container,
             width = 50,
             height = 50,
         )           
        
        # Display resources
        self.edited_resources = {}
        if self.camp_resources_length == 0 and self.new_resources_click == 0:
            label_no_resources = tk.Label(
                master=self.resources_container,
                text="No resources found for this camp. Add resources",)
            label_no_resources.grid(
                row=0,
                column=0,
                sticky="w",
            )
        else:
            for i in range(self.camp_resources_length):
                label_resource = tk.Label(
                    master=self.resources_container,
                    text=camp_resources[i]["name"],)
                label_resource.grid(
                    row=i,
                    column=0,
                    sticky="w",
                )

                entry_resource = tk.Entry(
                    master=self.resources_container,
                    width=8,
                    textvariable=tk.StringVar(
                        value=camp_resources[i]["amount"],),)
                entry_resource.grid(
                    row=i,
                    column=1,
                    sticky="w",)
                self.edited_resources[camp_resources[i]["name"]]=entry_resource
                
        # Button to submit edit
        self.submit_edit_button = tk.Button(
            master=self.button_container,
            width=20,
            text="Submit changes",
            command=self.handle_submit_edit_click,
        )
        
        # Button to add new type of resource
        self.add_resource_button = tk.Button(
            master=self.button_container,
            width=20,
            text="Add new resource type",
            command=lambda: self.handle_add_resources_click(self.new_resources_click, self.camp_resources_length),
        ) 
                
        # Button to go back
        self.back_button = tk.Button(
            master=self.button_container,
            width=20,
            text="Back",
            command=self.handle_back_click,
        ) 
 
            
        #Add to grid
        self.resources_container.pack(pady=15, fill="both", expand=True, side="top")
        self.button_container.pack(pady=15, fill="both", expand=True, side="bottom") 
        
        self.add_resource_button.grid(row=0, column=0,)
        self.submit_edit_button.grid(row=0, column=1,)
        self.back_button.grid(row=0, column=2,)

            
##       resources_length = len(camp_resources)
#        resource_name = [resource["name"] for resource in camp_resources]
#        resource_amount = [resource["amount"] for resource in camp_resources]
