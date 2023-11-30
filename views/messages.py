# Python imports
import logging
import tkinter as tk
from tkinter import ttk

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

        self.header = ttk.Label(
            master=self.header_container,
            text=f"Messages 📧",
            font=(60),
        )
        self.header.grid(
            row=0,
            column=5,
            pady=10,
        )

        self.new_msg_btn = tk.Button(
            master=self.header_container,
            text="New Message",
            command=self._handle_new_msg_click,
        )
        self.new_msg_btn.grid(row=0, column=10, padx=10, pady=10, sticky="e")

        self.render_unresolved_messages()
        self.render_resolved_messages()

        self.canvas_unresolved.bind(
            "<Configure>", self._on_canvas_configure_unresolved_table_container
        )
        self.canvas_resolved.bind(
            "<Configure>", self._on_canvas_configure_resolved_table_container
        )

    def get_messages(self, is_resolved: bool):
        """Returns messages for this user from db"""
        return run_query_get_rows(
            f"""SELECT * 
                FROM Messages 
                WHERE receiver_id = {self.master.get_global_state()['user_id']} 
                AND is_resolved = {is_resolved}
                ORDER BY 
                    CASE
                        WHEN urgency = 'LOW' THEN 1
                        WHEN urgency = 'MID' THEN 2
                        WHEN urgency = 'HIGH' THEN 3
                    END
                    ASC, sent_at DESC
                """
        )

    def _get_camp_plan_name_from_sender_id(
        self,
        sender_id: int,
    ) -> str:
        """Returns names from sender id"""
        sender_name = run_query_get_rows(
            f"SELECT username FROM User WHERE id = {sender_id}"
        )[0]["username"]

        camp_id_query = f"SELECT camp_id FROM User WHERE id = {sender_id}"

        camp_id = run_query_get_rows(camp_id_query)[0]["camp_id"]

        # admins don't have plans / camps
        if not camp_id:
            return "-", "-", sender_name

        camp = run_query_get_rows(
            f"SELECT name, plan_id FROM Camp WHERE id = {camp_id}"
        )[0]
        camp_name, plan_id = camp.get("name"), camp.get("plan_id")

        plan_name = run_query_get_rows(f"SELECT title FROM Plan WHERE id = {plan_id}")[
            0
        ]["title"]

        return camp_name, plan_name, sender_name

    def _get_data_to_render(self, data) -> list[list[str]]:
        """Returns data to render in table"""
        data_to_render = []
        for message in data:
            data_to_add = []
            data_to_add.append(message["id"])

            # Just get date and time HH:MM
            data_to_add.append(message["sent_at"][:-3])

            # Get Plan & CAMP & Sender name
            camp_name, plan_name, sender_name = self._get_camp_plan_name_from_sender_id(
                sender_id=message["sender_id"]
            )
            data_to_add.append(plan_name)
            data_to_add.append(camp_name)
            data_to_add.append(sender_name)

            data_to_add.append(message["urgency"])
            data_to_add.append(message["message"])

            data_to_render.append(data_to_add)
        return data_to_render

    def render_unresolved_messages(self):
        self.unresolved_messages = self.get_messages(is_resolved=False)

        # Get the data as simple list[str], starting with col headers
        self.header_cols = [
            "Msg ID",
            "Received At",
            "Plan",
            "Camp",
            "Sender",
            "Priority",
            "Message",
            "Resolve?",
        ]
        self.data_to_render = [self.header_cols]

        self.data_to_render.extend(self._get_data_to_render(self.unresolved_messages))

        self.unresolved_messages_container = tk.Frame(
            master=self.container,
            width=1400,
        )
        self.unresolved_messages_container.pack(fill="both", expand=True)

        # SCROLL BAR - THANK YOU https://www.pythontutorial.net/tkinter/tkinter-scrollbar/
        # Create a canvas widget
        self.canvas_unresolved = tk.Canvas(
            self.unresolved_messages_container,
            width=1400,
            height=400,  # clamp height
        )
        self.canvas_unresolved.pack(side=tk.LEFT, fill="both", expand=True)

        # Create a scrollbar for the canvas
        scrollbar = ttk.Scrollbar(
            self.unresolved_messages_container,
            orient=tk.VERTICAL,
            command=self.canvas_unresolved.yview,
        )
        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y,
        )

        # Configure the canvas to use the scrollbar
        self.canvas_unresolved.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        table_frame = tk.Frame(
            self.canvas_unresolved,
        )
        self.canvas_unresolved.create_window((0, 0), window=table_frame, anchor=tk.NW)

        self.unresolved_table_container = tk.LabelFrame(
            master=table_frame,
            text="Unresolved Messages",
            padx=10,
            pady=10,
            width=1400,
        )
        self.unresolved_table_container.pack(
            padx=10,
            pady=50,
            fill="both",
            expand=True,
        )

        for ix, row in enumerate(self.data_to_render):
            self._render_row(
                container=self.unresolved_table_container,
                items=row,
                header=ix == 0,  # True if first row, else False
                resolved_messages=False,
            )

        # No messages, just header
        if len(self.data_to_render) == 1:
            no_messages_label = tk.Label(
                master=self.unresolved_table_container,
                text="No unresolved messages ✅",
                font=(60),
            )
            no_messages_label.pack()

    def render_resolved_messages(self):
        self.resolved_messages = self.get_messages(is_resolved=True)

        # Get the data as simple list[str], starting with col headers
        self.header_cols = [
            "Msg ID",
            "Received At",
            "Plan",
            "Camp",
            "Sender",
            "Priority",
            "Message",
            "Undo?",
        ]
        self.data_to_render = [self.header_cols]

        self.data_to_render.extend(self._get_data_to_render(self.resolved_messages))

        self.resolved_messages_container = tk.Frame(
            master=self.container,
            # width=500,
            pady=50,
        )
        self.resolved_messages_container.pack(fill="both", expand=True)

        # SCROLL BAR - THANK YOU https://www.pythontutorial.net/tkinter/tkinter-scrollbar/
        # Create a canvas widget
        self.canvas_resolved = tk.Canvas(
            self.resolved_messages_container,
            # width=1400,
        )
        self.canvas_resolved.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
        )

        # Create a scrollbar for the canvas
        scrollbar = ttk.Scrollbar(
            self.resolved_messages_container,
            orient=tk.VERTICAL,
            command=self.canvas_resolved.yview,
        )
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configure the canvas to use the scrollbar
        self.canvas_resolved.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        table_frame = tk.Frame(self.canvas_resolved)
        self.canvas_resolved.create_window((0, 0), window=table_frame, anchor=tk.NW)

        self.table_container = tk.LabelFrame(
            master=table_frame,
            text="Resolved Messages",
            padx=10,
            pady=10,
            width=1500,
        )
        self.table_container.pack(expand=True)

        for ix, row in enumerate(self.data_to_render):
            self._render_row(
                container=self.table_container,
                items=row,
                header=ix == 0,  # True if first row, else False
                resolved_messages=True,
            )

        # No messages, just header
        if len(self.data_to_render) == 1:
            no_messages_label = tk.Label(
                master=self.table_container,
                text="No resolved messages",
                font=(60),
            )
            no_messages_label.pack()

    # Bind the canvas to update the scroll region
    def _on_canvas_configure_unresolved_table_container(self, event):
        self.canvas_unresolved.configure(
            scrollregion=self.canvas_unresolved.bbox("all")
        )

    def _on_canvas_configure_resolved_table_container(self, event):
        self.canvas_resolved.configure(scrollregion=self.canvas_resolved.bbox("all"))

    def _render_row(
        self,
        container: tk.Frame,
        items: list[str],
        column_width=18,
        header=False,
        resolved_messages=True,
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
            if not header:
                add_border(self.cell_frame)

            self.cell_content = tk.Label(
                master=self.cell_frame,
                text=label,
                width=column_width if ix != 6 else 55,
                justify="left",
            )

            self.cell_content.pack(
                anchor="e",
                fill="both",
                expand=True,
            )

        # Add action buttons
        if not header:
            tk.Button(
                master=self.row_container,
                text="Undo" if resolved_messages else "Resolve",
                width=column_width,
                command=lambda: self._handle_resolve_undo_click(message_id=items[0]),
            ).grid(row=0, column=len(items))

    def _handle_resolve_undo_click(self, message_id: int) -> None:
        """Handles resolve / undo button click"""

        # Update db
        logging.debug(f"Resolving / undoing message {message_id}")
        run_query_get_rows(
            f"""UPDATE Messages
                SET is_resolved = 
                    CASE
                        WHEN is_resolved = 1 THEN 0
                    ELSE 1
                END
                WHERE id = {message_id}
            """
        )

        # Reload view
        self.master.switch_to_view("messages")

    def _handle_new_msg_click(self) -> None:
        """Handles new message button click"""
        self.master.switch_to_view("new_msg")
