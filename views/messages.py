# Python imports
import logging
import tkinter as tk

# Project imports
from constants import config
from utilities.db import run_query_get_rows
from utilities.formatting import add_border, calculate_max_col_width
from .base import BaseView


class MessagesView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()

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
            text=f"Messages 📧",
            font=(60),
        )
        self.header.grid(
            row=0,
            column=5,
            pady=10,
        )

        self.render_unresolved_messages()

        logging.debug(
            f"{self.get_messages()=} {self.master.get_global_state()['user_id']}"
        )

    def get_messages(self):
        """Returns messages for this user from db"""
        return run_query_get_rows(
            f"SELECT * FROM Messages WHERE receiver_id = {self.master.get_global_state()['user_id']}"
        )

    def render_unresolved_messages(self):
        self.unresolved_messages = self.get_messages()

        # Get the data as simple list[str], starting with col headers
        self.header_cols = [
            "Received At",
            "Sender",
            "Priority",
            "Message",
            "Resolve?",
        ]
        self.data_to_render = [self.header_cols]

        for message in self.unresolved_messages:
            data_to_add = []
            data_to_add.append(message["sent_at"])
            data_to_add.append(message["sender_id"])
            data_to_add.append(message["urgency"])
            data_to_add.append(message["message"])

            self.data_to_render.append(data_to_add)

        self.unresolved_messages_container = tk.Frame(
            master=self.container,
        )
        self.unresolved_messages_container.pack()

        self.table_container = tk.LabelFrame(
            master=self.unresolved_messages_container,
            text="Unresolved Messages",
            padx=10,
            pady=10,
        )
        self.table_container.pack(padx=10, pady=10)

        for ix, row in enumerate(self.data_to_render):
            self._render_row(
                container=self.table_container,
                items=row,
                header=ix == 0,  # True if first row, else False
            )

    def _render_row(
        self,
        container: tk.Frame,
        items: list[str],
        column_width=15,
        header=False,
    ) -> None:
        self.row_container = tk.Frame(
            master=container,
        )
        self.row_container.pack()

        for ix, label in enumerate(items):
            self.cell_frame = tk.Frame(
                master=self.row_container,
                width=200,
                height=25,
            )
            self.cell_frame.grid(
                row=0,
                column=ix,
            )
            add_border(self.cell_frame)

            self.cell_content = tk.Label(
                master=self.cell_frame,
                text=label,
                width=column_width if ix != 3 else 100,
            )

            self.cell_content.pack(
                fill="both",
                expand=True,
            )



        # Add edit buttons
        if not header:
            tk.Button(
                master=self.row_container,
                text="Resolve",
                width=15,
            ).grid(row=0, column=len(items))


