# Python imports
import logging
import tkinter as tk
import datetime
import re

# Project imports
from constants import config
from utilities.db import run_query_get_rows, insert_query_with_values
from utilities.validators import is_valid_email
from .base import BaseView


class AddEditRefugeeView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # check the user role
        self.is_volunteer = not self.master.get_global_state().get("is_admin")

        # SET INSTANCE VARIABLES
        self.MAX_CHAR_LEN = 20
        self.plan_title_text = self.master.GLOBAL_STATE.get("plan_name")
        self.camp_id = self.master.GLOBAL_STATE.get("camp_id_to_view")

        self.edit_refugee_id = self.master.GLOBAL_STATE.get("refugee_id_to_edit")
        self.is_edit = bool(self.edit_refugee_id)
        if self.is_edit:
            self.edit_refugee_details = run_query_get_rows(
                f"SELECT * FROM RefugeeFamily WHERE id = '{self.edit_refugee_id}'"
            )[0]

        self.render_widgets()
        self.master.update()

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
            text=f"Add edit refugee view",
            font=(60),
        )
        self.header.pack(
            side="left",
        )

        # ----------------------- FORM ----------------------------
        self.form_container = tk.Frame(
            master=self.container,
        )
        self.form_container.pack(
            pady=15,
            fill="both",
            expand=True,
        )
        # display plan - can't change
        self._render_plan_name(
            self.form_container,
            on_row=0,
        )
        # display camp - question - can change or not?
        self._render_camp_name(
            self.form_container,
            on_row=0,
        )

        # id
        self._render_refugee_id(
            self.form_container,
            on_row=1,
        )

        # rep name
        self._render_main_rep_name(
            self.form_container,
            on_row=2,
        )

        # medical condition
        self._render_med_condition_name(
            self.form_container,
            on_row=3,
        )

        # number of adults
        self._render_num_adults_name(
            self.form_container,
            on_row=4,
        )

        # number of children

        # main_rep_home_towm

        # main_rep_age

        # main_rep_sex

        # number of missing people

        # Status

    # -------------- Rendering functions for inputs ------------

    # render plan name
    def _render_plan_name(self, form_container, on_row: int) -> None:
        self.plan_name_container = tk.Frame(
            master=form_container,
        )
        self.plan_name_container.grid(row=on_row, column=0, sticky="w")

        self.plan_name_label_container = tk.Frame(
            master=self.plan_name_container,
        )
        self.plan_name_label_container.pack(
            expand=True,
            fill="x",
        )
        self.plan_name_label = tk.Label(
            master=self.plan_name_label_container,
            text="Plan Name",
        )
        self.plan_name_label.pack(
            side="left",
        )

        self.plan_name_entry_container = tk.Frame(
            master=self.plan_name_container,
        )
        self.plan_name_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.plan_name_str_text = tk.StringVar()
        if not self.is_volunteer:
            self.plan_name_str_text.set(self.master.GLOBAL_STATE.get("plan_name"))
        else:
            self.plan_name = self._get_plan_name()
            self.plan_name_str_text.set(self.plan_name)

        self.plan_name_entry = tk.Entry(
            master=self.plan_name_entry_container,
            width=20,
            state="disabled",
            textvariable=self.plan_name_str_text,
        )
        self.plan_name_entry.pack()

    # render camp name
    def _render_camp_name(self, form_container, on_row: int) -> None:
        self.camp_name_container = tk.Frame(
            master=form_container,
        )
        self.camp_name_container.grid(row=on_row, column=1, sticky="e")

        self.camp_name_label_container = tk.Frame(
            master=self.camp_name_container,
        )
        self.camp_name_label_container.pack(
            expand=True,
            fill="x",
        )
        self.camp_name_label = tk.Label(
            master=self.camp_name_label_container,
            text="Camp Name",
        )
        self.camp_name_label.pack(
            side="left",
        )

        self.camp_name_entry_container = tk.Frame(
            master=self.camp_name_container,
        )
        self.camp_name_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.camp_name_str_text = tk.StringVar()
        self.camp_name = self._get_camp_name()
        self.camp_name_str_text.set(self.camp_name)

        self.camp_name_entry = tk.Entry(
            master=self.camp_name_entry_container,
            width=20,
            state="disabled",
            textvariable=self.camp_name_str_text,
        )
        self.camp_name_entry.pack()

    #  Refugee ID
    def _render_refugee_id(self, form_container, on_row: int) -> None:
        """Renders refugee ID if exists or new refugee ID if adding"""
        self.refugee_id_container = tk.Frame(
            master=form_container,
        )
        self.refugee_id_container.grid(
            row=on_row,
            column=0,
            columnspan=2,
        )

        self.refugee_id_label_container = tk.Frame(
            master=self.refugee_id_container,
        )
        self.refugee_id_label_container.pack(
            expand=True,
            fill="x",
        )
        self.refugee_id_label = tk.Label(
            master=self.refugee_id_label_container,
            text="Refugee ID",
        )
        self.refugee_id_label.pack(
            side="left",
        )

        self.refugee_id_entry_container = tk.Frame(
            master=self.refugee_id_container,
        )
        self.refugee_id_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.refugee_id_text = tk.StringVar()
        if self.is_edit:
            self.refugee_id_text.set(self.edit_refugee_details["id"])
        else:
            # Get latest refugee id
            self.refugee_id_text.set(self._get_latest_refugee_id() + 1)

        self.refugee_id_entry = tk.Entry(
            master=self.refugee_id_entry_container,
            width=50,
            state="disabled",
            textvariable=self.refugee_id_text,
        )
        self.refugee_id_entry.pack()

    # Refugee main rep namme
    def _render_main_rep_name(self, form_container, on_row: int) -> None:
        self.rep_name_container = tk.Frame(
            master=form_container,
        )
        self.rep_name_container.grid(
            row=on_row,
            column=0,
            columnspan=2,
        )

        self.rep_name_label_container = tk.Frame(
            master=self.rep_name_container,
        )
        self.rep_name_label_container.pack(
            expand=True,
            fill="x",
        )
        self.rep_name_label = tk.Label(
            master=self.rep_name_label_container,
            text="Name (max 40 chars)",
        )
        self.rep_name_label.pack(
            side="left",
        )

        self.rep_name_entry_container = tk.Frame(
            master=self.rep_name_container,
        )
        self.rep_name_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.main_rep_text = tk.StringVar()
        if self.is_edit:
            self.main_rep_text.set(self.edit_refugee_details["main_rep_name"])
        # Set char length limit
        self.main_rep_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=self.main_rep_text, char_limit=self.MAX_CHAR_LEN
            ),
        )
        self.rep_name_entry = tk.Entry(
            master=self.rep_name_entry_container,
            width=50,
            textvariable=self.main_rep_text,
        )
        self.rep_name_entry.pack()

    # Medical conition
    def _render_med_condition_name(self, form_container, on_row: int) -> None:
        self.med_condition_container = tk.Frame(
            master=form_container,
        )
        self.med_condition_container.grid(
            row=on_row,
            column=0,
            columnspan=2,
        )

        self.med_condition_label_container = tk.Frame(
            master=self.med_condition_container,
        )
        self.med_condition_label_container.pack(
            expand=True,
            fill="x",
        )
        self.med_condition_label = tk.Label(
            master=self.med_condition_label_container,
            text="Medical Condition (max 40 chars)",
        )
        self.med_condition_label.pack(
            side="left",
        )

        self.med_condition_entry_container = tk.Frame(
            master=self.med_condition_container,
        )
        self.med_condition_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.main_rep_text = tk.StringVar()
        if self.is_edit:
            self.main_rep_text.set(self.edit_refugee_details["medical_conditions"])
        # Set char length limit
        self.main_rep_text.trace(
            "w",
            lambda *args: self.set_character_limit(
                entry_text=self.main_rep_text, char_limit=self.MAX_CHAR_LEN
            ),
        )
        self.med_condition_entry = tk.Entry(
            master=self.med_condition_entry_container,
            width=50,
            textvariable=self.main_rep_text,
        )
        self.med_condition_entry.pack()

    # Number of adults
    def _render_num_adults_name(self, form_container, on_row: int) -> None:
        self.num_adults_container = tk.Frame(
            master=form_container,
        )
        self.num_adults_container.grid(
            row=on_row,
            column=0,
            columnspan=2,
        )

        self.num_adults_label_container = tk.Frame(
            master=self.num_adults_container,
        )
        self.num_adults_label_container.pack(
            expand=True,
            fill="x",
        )
        self.num_adults_label = tk.Label(
            master=self.num_adults_label_container,
            text="Number of adults",
        )
        self.num_adults_label.pack(
            side="left",
        )

        self.num_adults_entry_container = tk.Frame(
            master=self.num_adults_container,
        )
        self.num_adults_entry_container.pack(
            expand=True,
            fill="x",
        )

        self.main_rep_text = tk.IntVar()
        if self.is_edit:
            self.main_rep_text.set(self.edit_refugee_details["n_adults"])
        # TO DO: Check if it is a valid number???
        # # Set char length limit
        # self.main_rep_text.trace(
        #     "w",
        #     lambda *args: self.set_character_limit(
        #         entry_text=self.main_rep_text, char_limit=self.MAX_CHAR_LEN
        #     ),
        # )
        self.num_adults_entry = tk.Entry(
            master=self.num_adults_entry_container,
            width=50,
            textvariable=self.main_rep_text,
        )
        self.num_adults_entry.pack()

    # ------------------- HELPER FUNCTIONS ----------------------
    def _get_latest_refugee_id(self) -> int:
        latest_refugee_id = run_query_get_rows(
            "SELECT MAX(id) AS latest_refugee_id FROM RefugeeFamily"
        )[0].get("latest_refugee_id")
        return latest_refugee_id

    def _get_plan_name(self):
        plan_name = run_query_get_rows(
            f"SELECT title FROM Plan AS p INNER JOIN Camp AS c ON p.id = c.plan_id WHERE c.id = {self.camp_id}"
        )[0].get("title")
        return plan_name

    def _get_camp_name(self) -> list[dict]:
        """queries name of the camp"""
        camp_name = run_query_get_rows(
            f"SELECT name FROM Camp WHERE id='{self.camp_id}'"
        )[0].get("name")
        return camp_name
