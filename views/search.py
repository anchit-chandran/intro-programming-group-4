"""TEMPLATE FILE FOR MAKING NEW VIEW"""
# Python imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import logging
import re
import pandas as pd
from datetime import datetime

# Project imports
from views.base import BaseView
from constants import config
from utilities.db import run_query_get_rows


class SearchView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Initialise any vars
        self.all_field_keys = [
            "id",
            "main_rep_name",
            "main_rep_age",
            "main_rep_sex",
            "main_rep_home_town",
            "n_adults",
            "n_children",
            "n_missing_members",
            "medical_conditions",
            "is_in_camp",
            "camp_id",
        ]
        # Get empty table for now
        self.search_results = [
            ["" for _ in range(len(self.all_field_keys))],
        ]

        self.render_widgets()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
            width=config.SCREEN_WIDTH,
        )
        self.container.pack()

        # Header
        self.header_container = tk.Frame(self.container)
        self.header_container.pack(pady=15, fill="x", expand=True)

        self.header = tk.Label(
            master=self.header_container,
            text=f"Search Refugee Families",
            font=(60),
        )
        self.header.pack(
            side="top",
        )

        # Instructions label
        self.instructions_container = ttk.LabelFrame(
            master=self.header_container,
            text="Instructions for Searching Refugee Families",
        )
        self.instructions_container.pack(side="bottom")
        self.instructions_label = tk.Label(
            master=self.instructions_container,
            text="This is an open-ended utility which will perform a search across all registered Refugee Families and return matches based on as many fields inputted.\n\nSome example uses include:\n\n\t-Helping lost refugees reconnect with their family\n\t-Identifying refugees with particular medical conditions to provide medications\n\t-Identifying children to target educational and/or social aid\n\nPlease fill in as many fields as possible. At least 1 value is required. You can scroll if there are many results.\n\nNOTE: search fields labelled '(< or >)' can search on exact integers, or can be combined with the '<' / '>' symbols to search ranges e.g. for Number of Children, '>1' would return all Families with more than 2 children. These fields MUST include valid whole numbers.\n\nUse the 'Download' button to download the results.",
            anchor="w",
            justify="left",
            wraplength=1000,
        )
        self.instructions_label.pack(side="bottom")

        self.refugee_search_container = tk.LabelFrame(
            master=self.container, text="Search Fields"
        )
        self.refugee_search_container.pack()
        
        # download
        self.download_button = tk.Button(
            master=self.container, text = 'Download', command=self.handle_download_click
        )
        self.download_button.pack(side='top', pady=5)

        self._render_refugee_family_search_fields(self.refugee_search_container)

        self.results_container = tk.LabelFrame(master=self.container, text="Matches")
        self.results_container.pack()
        self._render_results_fields(self.results_container, results=self.search_results)

    def _render_refugee_family_search_fields(self, container):
        self.refugee_family_id_label = tk.Label(
            master=container,
            text=f"Refugee Family ID:",
            width=25,
            anchor="w",
        )

        self.refugee_family_id_entry = tk.Entry(
            master=container,
            width=35,
        )

        # Main rep name
        self.main_rep_name_label = tk.Label(
            master=container,
            text="Main Rep Name",
            width=25,
            anchor="w",
        )

        self.main_rep_name_entry = tk.Entry(
            master=container,
            width=35,
        )

        # Main rep age
        self.main_rep_age_label = tk.Label(
            master=container,
            text="Main Rep Age",
            width=25,
            anchor="w",
        )

        self.main_rep_age_entry = tk.Entry(
            master=container,
            width=35,
        )

        # Main rep sex
        self.main_rep_sex_label = tk.Label(
            master=container,
            text="Main Rep Sex",
            width=25,
            anchor="w",
        )

        self.main_rep_sex_entry = ttk.Combobox(
            master=container,
            width=6,
            state="readonly",
        )
        sex_values = ['']
        sex_values.extend(list(config.SEX_VALUES))
        self.main_rep_sex_entry["values"] = sex_values
        self.main_rep_sex_entry.current(None) 

        # Main Rep Home Town
        self.main_rep_home_town_label = tk.Label(
            master=container,
            text="Main Rep Home Town",
            width=25,
            anchor="w",
        )

        self.main_rep_home_town_entry = tk.Entry(
            master=container,
            width=35,
        )

        # Number of Adults
        self.n_adults_label = tk.Label(
            master=container,
            text="No. of Adults (< or >)",
            width=25,
            anchor="w",
        )

        self.n_adults_entry = tk.Entry(
            master=container,
            width=35,
        )

        # Number of Children
        self.n_children_label = tk.Label(
            master=container,
            text="No. of Children (< or >)",
            width=25,
            anchor="w",
        )

        self.n_children_entry = tk.Entry(
            master=container,
            width=35,
        )

        # Number of Missing Members
        self.n_missing_members_label = tk.Label(
            master=container,
            text="No. of Missing Members (< or >)",
            width=25,
            anchor="w",
        )

        self.n_missing_members_entry = tk.Entry(
            master=container,
            width=35,
        )

        # Medical Conditions
        self.medical_conditions_label = tk.Label(
            master=container,
            text="Medical Conditions",
            width=25,
            anchor="w",
        )

        self.medical_conditions_entry = tk.Entry(
            master=container,
            width=35,
        )

        # Is in Camp
        self.is_in_camp_label = tk.Label(
            master=container,
            text="Residing in Camp",
            width=25,
            anchor="w",
        )

        self.is_in_camp_entry = tk.Entry(
            master=container,
            width=35,
        )

        self.camp_label = tk.Label(
            master=container,
            text="Camp",
            width=25,
            anchor="w",
        )

        # CAMP DROPDOWN
        self.camp_entry = ttk.Combobox(
            master=container,
            width=25,
            state="readonly",
        )
        self.camp_entry["values"] = self.get_all_camp_labels()
        self.camp_entry.current(0)

        self.plan_label = tk.Label(
            master=container,
            text="Plan",
            width=25,
            anchor="w",
        )

        self.plan_entry = tk.Entry(
            master=container,
            width=35,
        )

        # Search
        self.search_button = tk.Button(
            master=container, text="Search", command=self._handle_search_click
        )
        
        

        # PLACE WIDGETS ON SCREEN
        self.refugee_family_id_label.grid(row=0, column=0)
        self.refugee_family_id_entry.grid(row=0, column=1)

        self.main_rep_name_label.grid(row=0, column=2)
        self.main_rep_name_entry.grid(row=0, column=3)

        self.main_rep_age_label.grid(row=1, column=0)
        self.main_rep_age_entry.grid(row=1, column=1)

        self.main_rep_sex_label.grid(row=1, column=2)
        self.main_rep_sex_entry.grid(row=1, column=3, sticky='w')

        self.main_rep_home_town_label.grid(row=2, column=0)
        self.main_rep_home_town_entry.grid(row=2, column=1)

        self.n_adults_label.grid(row=2, column=2)
        self.n_adults_entry.grid(row=2, column=3)

        self.n_children_label.grid(row=3, column=0)
        self.n_children_entry.grid(row=3, column=1)

        self.n_missing_members_label.grid(row=3, column=2)
        self.n_missing_members_entry.grid(row=3, column=3)

        self.medical_conditions_label.grid(row=4, column=0)
        self.medical_conditions_entry.grid(row=4, column=1)

        self.is_in_camp_label.grid(row=4, column=2)
        self.is_in_camp_entry.grid(row=4, column=3)

        self.camp_label.grid(row=10, column=0)
        self.camp_entry.grid(row=10, column=1, sticky="w")

        self.search_button.grid(row=20, column=0, columnspan=4, pady=5)
        
    def handle_download_click(self)->None:
        if self.is_table_empty():
            self.render_error_popup_window(message="No results to download!")
            return
        
        logging.debug(f'downloading...')
        df = pd.DataFrame(columns=self.header_cols, data=self.search_results)
        
        filename = f"{str(datetime.now()).replace('-','').replace(' ','').replace(':','').replace('.','')}-search-results.csv"

        df.to_csv(filename)
        
        messagebox.showinfo(title='Success 📩', message=f'Your file has been downloaded with the name: {filename}')
        

    def is_table_empty(self)->int:
        rows = getattr(self, 'search_results', None)
        if rows[0] == ['', '', '', '', '', '', '', '', '', '', '']:
            return True
        return False
        
    
    def _convert_camp_id_to_label(self, camp_id: int) -> str:
        """Converts Camp id to form '`Name`' (ID:`id`)"""
        name = run_query_get_rows(f"""SELECT name FROM Camp WHERE id={camp_id}""")[0][
            "name"
        ]

        return f"{name} (ID:{camp_id})"

    def get_all_camp_labels(self) -> list[str]:
        """Returns all camp labels in form ['Camp `ID` (PlanID: `id`)', ...,]"""
        camp_data = run_query_get_rows(f"SELECT id, plan_id FROM Camp")

        labels = [""]  # start with empty label
        for camp in camp_data:
            labels.append(f"CampID: {camp['id']} (PlanID: {camp['plan_id']})")

        return labels

    def _render_results_fields(self, container, results: list[list[str]]):
        self.header_cols = [
            "RefugeeFamID",
            "Main Rep Name",
            "Main Rep Age",
            "Main Rep Sex",
            "Main Rep Home Town",
            "Adults (n)",
            "Children (n)",
            "Missing Members (n)",
            "Medical Conditions",
            "Residing in Camp",
            "Camp",
        ]
        
        

        self.render_tree_table(
            container=container,
            header_cols=self.header_cols,
            data=results,
            max_rows=5,
            treeheight=5,
            col_widths=[
                80,
                100,
                80,
                80,
                125,
                80,
                125,
                100,
                125,
                100,
                100,
            ],
        )
        

    def _construct_where_clauses_from(self, fields_and_values: dict) -> str:
        """Returns valid SQL WHERE clauses joined using ANDs"""

        where_clauses = []

        for field, val in fields_and_values.items():
            if val:
                if field == "camp_id":
                    val = self._get_camp_id_from_label(val)

                # Numeric fields
                if field in ["n_adults", "n_children", "n_missing_members"]:
                    # Look for carets
                    carets = re.findall(pattern=r">|<", string=val)
                    if carets:
                        # If there are carets, then change value to WHERE FIELD > val
                        where_clauses.append(
                            f"{field} {carets[0]} {val.replace(carets[0], '')}"
                        )
                        continue

                where_clauses.append(f"{field} LIKE '%{val}%'")

        where_joined = "\n AND ".join(where_clauses)

        return where_joined

    def perform_search(self, all_field_values):
        fields_and_values = {
            key: val for key, val in zip(self.all_field_keys, all_field_values)
        }

        where_clauses = self._construct_where_clauses_from(fields_and_values)

        if not where_clauses:
            self.render_error_popup_window(message="Please enter at least 1 value!")
            return

        search_query = f"""SELECT *
            FROM RefugeeFamily
            WHERE 
                {where_clauses if where_clauses else ''}
        """
        logging.debug(f"RAW QUERY: {search_query}")

        search_results_raw = run_query_get_rows(search_query)
        self.search_results = [list(result.values()) for result in search_results_raw]
        logging.debug(f"RESULTS: {self.search_results}")

        # Convert campid to label
        for row in self.search_results:
            row[-1] = self._convert_camp_id_to_label(row[-1])

        # Delete current tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        for result in self.search_results:
            self.tree.insert("", "end", values=result)

        

    def _handle_search_click(self) -> None:
        errors = f"Invalid input!"
        try:
            refugee_family_id_input = self.refugee_family_id_entry.get()
            main_rep_name_input = self.main_rep_name_entry.get()
            main_rep_age_input = self.main_rep_age_entry.get()
            main_rep_sex_input = self.main_rep_sex_entry.get()
            main_rep_home_town_input = self.main_rep_home_town_entry.get()

            n_adults_input = self.n_adults_entry.get()
            if n_adults_input:
                num = n_adults_input.replace("<", "").replace(">", "")
                if not num.isnumeric():
                    errors += " Are the number fields correct?"
                    raise Exception("Nums must be ints")
            n_children_input = self.n_children_entry.get()
            if n_children_input:
                num = n_children_input.replace("<", "").replace(">", "")
                if not num.isnumeric():
                    raise Exception("Nums must be ints")
            n_missing_members_input = self.n_missing_members_entry.get()
            if n_missing_members_input:
                num = n_missing_members_input.replace("<", "").replace(">", "")
                if not num.isnumeric():
                    errors += " Are the number fields correct?"
                    raise Exception("Nums must be ints")

            medical_conditions_input = self.medical_conditions_entry.get()
            is_in_camp_input = self.is_in_camp_entry.get()
            camp_input = self.camp_entry.get()

            all_field_values = [
                refugee_family_id_input,
                main_rep_name_input,
                main_rep_age_input,
                main_rep_sex_input,
                main_rep_home_town_input,
                n_adults_input,
                n_children_input,
                n_missing_members_input,
                medical_conditions_input,
                is_in_camp_input,
                camp_input,
            ]

            self.perform_search(all_field_values=all_field_values)
        except Exception as e:
            logging.debug(f"Something went wrong: {e}")
            self.render_error_popup_window(message=errors)

    def _get_camp_id_from_label(self, label: str) -> int:
        """Returns camp id int from label, which is in format 'CampID: 2 (PlanID: 1)'"""
        camp_id_str = re.search(pattern=r"(?<=CampID: )\d+", string=label).group(0)
        return int(camp_id_str)
