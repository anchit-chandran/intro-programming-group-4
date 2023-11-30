"""TEMPLATE FILE FOR MAKING NEW VIEW"""
# Python imports
import tkinter as tk

# Project imports
from views.base import BaseView
from constants import config


class EditResourcesView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        self.camp_id = self.master.get_global_state().get("camp_id_for_resources")
        if not self.camp_id:
            raise ValueError("camp_id_for_resources not in global state")
        
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
            text=f"TEMPLATE",
            font=(60),
        )
        self.header.pack(
            side="left",
        )

