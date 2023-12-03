"""TEMPLATE FILE FOR MAKING NEW VIEW"""
# Python imports
import tkinter as tk
from tkinter import ttk

# Project imports
from views.base import BaseView
from constants import config


class MissingPeopleView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()

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
            text="If a refugee is looking to find their family across registered Refugee Families, a search across fields can be attempted below.\n\nPlease fill in as many fields as known.",
            anchor="w",
            justify="left",
            wraplength=1000,
        )
        self.instructions_label.pack(side="bottom")

        self.refugee_search_container = tk.LabelFrame(
            master=self.container, text="Search Fields"
        )
        self.refugee_search_container.pack()

        self._render_refugee_family_search_fields(self.refugee_search_container)

        self.results_container = tk.LabelFrame(master=self.container, text="Matches")
        self.results_container.pack()
        self._render_results_fields(self.results_container)

    def _render_refugee_family_search_fields(self, container):
        self.refugee_family_id_label = tk.Label(
            master=container,
            text=f"Refugee Family ID:",
            width=20,
            anchor="w",
        )

        self.refugee_family_id_entry = tk.Entry(
            master=container,
            width=70,
        )

        self.location_label = tk.Label(
            master=container,
            text="Camp Location",
            width=20,
            anchor="w",
        )

        self.location_entry = tk.Entry(
            master=container,
            width=70,
        )

        # Main rep name
        self.main_rep_name_label = tk.Label(
            master=container,
            text="Main Rep Name",
            width=20,
            anchor="w",
        )

        self.main_rep_name_entry = tk.Entry(
            master=container,
            width=70,
        )

        # Main rep age
        self.main_rep_age_label = tk.Label(
            master=container,
            text="Main Rep Age",
            width=20,
            anchor="w",
        )

        self.main_rep_age_entry = tk.Entry(
            master=container,
            width=70,
        )

        # Main Rep Home Town
        self.main_rep_home_town_label = tk.Label(
            master=container,
            text="Main Rep Home Town",
            width=20,
            anchor="w",
        )

        self.main_rep_home_town_entry = tk.Entry(
            master=container,
            width=70,
        )

        # Number of Adults
        self.n_adults_label = tk.Label(
            master=container,
            text="No. of Adults",
            width=20,
            anchor="w",
        )

        self.n_adults_entry = tk.Entry(
            master=container,
            width=70,
        )

        # Number of Children
        self.n_children_label = tk.Label(
            master=container,
            text="No. of Children",
            width=20,
            anchor="w",
        )

        self.n_children_entry = tk.Entry(
            master=container,
            width=70,
        )

        # Number of Missing Members
        self.n_missing_members_label = tk.Label(
            master=container,
            text="No. of Missing Members",
            width=20,
            anchor="w",
        )

        self.n_missing_members_entry = tk.Entry(
            master=container,
            width=70,
        )

        # Medical Conditions
        self.medical_conditions_label = tk.Label(
            master=container,
            text="Medical Conditions",
            width=20,
            anchor="w",
        )

        self.medical_conditions_entry = tk.Entry(
            master=container,
            width=70,
        )

        # Is in Camp
        self.is_in_camp_label = tk.Label(
            master=container,
            text="Residing in Camp",
            width=20,
            anchor="w",
        )

        self.is_in_camp_entry = tk.Entry(
            master=container,
            width=70,
        )

        # Search
        self.search_button = tk.Button(
            master=container,
            text="Search",
        )

        # PLACE WIDGETS ON SCREEN
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

        self.search_button.grid(row=10, column=0, columnspan=2)

    def _render_results_fields(self, container):
        header_cols = [
            "Refugee Family ID",
            "Main Rep Name",
            "Main Rep Age",
            "Main Rep Home Town",
            "Adults (N)",
            "Children (N)",
            "Missing Members (N)",
            "Medical Conditions",
            "Residing in Camp",
            "Camp Location",
        ]

        self.render_tree_table(
            container=container,
            header_cols=header_cols,
            data=[["-" for _ in range(len(header_cols))]],
            max_rows=5
        )
