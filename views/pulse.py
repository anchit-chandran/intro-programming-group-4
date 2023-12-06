"""TEMPLATE FILE FOR MAKING NEW VIEW"""
# Python imports
import logging
import tkinter as tk
from tkinter import ttk
import pandas as pd

# Project imports
from constants import config, instructions
from utilities.db import run_query_get_rows
from .base import BaseView


class PulseView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        # Init any required vars
        self.plan_id = self.master.get_global_state().get('plan_id_to_view')
        
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

        self.instructions_container = ttk.LabelFrame(
            master=self.header_container,
            text=f"Pulse Dashboard for Plan ID {self.plan_id}",
            width=300,
        )
        self.instructions_container.grid(row=0, column=0, sticky="n", padx=10)

        self.instructions_label = tk.Label(
            master=self.instructions_container,
            text=f"Here you can see an overview of metrics related to this Plan.",
            anchor="w",
            justify="left",
        )
        self.instructions_label.pack()
        
        self.dashboard_container = tk.LabelFrame(master=self.container, text='Dashboard')
        self.dashboard_container.pack()
        self.render_dashboard(container=self.dashboard_container)
    
    def render_dashboard(self, container)->None:
        
        self.render_male_female_viz(container=container)

    def render_male_female_viz(self, container)->None:
        
        refugee_data = self.get_refugee_data_for_plan()
        
        df = (
            pd.DataFrame(refugee_data)
            [['camp_id','main_rep_sex']]
            .groupby(by=['camp_id'])
            .value_counts()
            .reset_index(name='count')
            .plot()
            )
        
        logging.debug(df)
        
    
    def get_refugee_data_for_plan(self)->list[dict]:
        camp_ids_raw = run_query_get_rows(f"SELECT id FROM Camp WHERE plan_id={self.plan_id}")
        
        camp_ids = tuple(result['id'] for result in camp_ids_raw)
        
        refugee_query = f"SELECT * FROM RefugeeFamily WHERE camp_id IN {camp_ids}"
        
        refugee_data = run_query_get_rows(refugee_query)
        
        return refugee_data