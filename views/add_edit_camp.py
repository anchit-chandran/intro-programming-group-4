"""TEMPLATE FILE FOR MAKING NEW VIEW"""
# Python imports
import tkinter as tk

# Project imports
from views.base import BaseView
from constants import config


class AddEditCampView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()
        # message button function

    def handle_send_message(self):
        # self.master.switch_to_view("add_message")
        return

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
            pady=20,
        )

        # Header
        self.header_container = tk.Frame(
            master=self.container,
            width=500,
            height=100,
        )
        self.header_container.grid(
            row=0,
            column=0,
        )

        self.header = tk.Label(
            master=self.header_container,
            text=f"WELLCOME {self.master.get_global_state().get('username')}! 👋",
            font=(60),
        )
        self.header.pack(
            side="left",
        )

