# Python imports
import logging
import tkinter as tk
from tkinter import ttk

# Project imports
from constants import config, message_priorities
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
            column=0,
            pady=10,
        )

        # Instructions label
        self.instructions_container = tk.LabelFrame(
            master=self.header_container,
            text="Instructions",
        )
        self.instructions_container.grid(
            row=1,
            column=0,
            sticky="w",
        )
        self.instructions_label = tk.Label(
            master=self.instructions_container,
            text="Below you can see your messages, separated by resolved and unresolved.\n\nYou can resolve / unresolve messages by selecting the message and pressing the appropriate button.\n\nNOTE: messages are sorted first by  Priority (highest priority at the top), then by most recently received.\n\n---Sending messages---\nYou can send message by clicking the 'New Message' button.",
            anchor="w",
            justify="left",
        )
        self.instructions_label.pack()

        self.new_msg_btn = tk.Button(
            master=self.header_container,
            text="New Message",
            command=self._handle_new_msg_click,
        )
        self.new_msg_btn.grid(row=3, column=10, padx=10, pady=10, sticky="e")

        # Unresolved messages
        self.render_unresolved_messages(
            is_resolved=False, tree_name="unresolved_tree", container=self.container
        )

        # Unresolved messages
        self.render_resolved_messages(
            is_resolved=True, tree_name="resolved_tree", container=self.container
        )

    def render_unresolved_messages(self, is_resolved: bool, tree_name: str, container):
        self.unresolved_container = tk.LabelFrame(
            master=container,
            text="Unresolved Messages",
        )
        self.unresolved_container.pack(padx=10, pady=10)

        self.unresolved_table_container = tk.Frame(
            master=self.unresolved_container, padx=10, pady=10
        )
        self.unresolved_table_container.grid(row=0, column=0)
        self.render_messages(
            is_resolved=is_resolved,
            tree_name=tree_name,
            container=self.unresolved_table_container,
        )

        self.resolve_selected_button = tk.Button(
            master=self.unresolved_container,
            text="Resolve Selected",
            padx=10,
            command=lambda: self._handle_resolve_undo_click(resolve_message=True),
        )
        self.resolve_selected_button.grid(
            row=0, column=1, sticky=tk.N, padx=10, pady=10
        )

    def render_resolved_messages(self, is_resolved: bool, tree_name: str, container):
        self.resolved_container = tk.LabelFrame(
            master=container,
            text="Resolved Messages",
        )
        self.resolved_container.pack(padx=10, pady=10)

        self.resolved_table_container = tk.Frame(
            master=self.resolved_container, padx=10, pady=10
        )
        self.resolved_table_container.grid(row=0, column=0)
        self.render_messages(
            is_resolved=is_resolved,
            tree_name=tree_name,
            container=self.resolved_table_container,
        )

        self.resolve_selected_button = tk.Button(
            master=self.resolved_container,
            text="Unresolve Selected",
            padx=10,
            command=lambda: self._handle_resolve_undo_click(resolve_message=False),
        )
        self.resolve_selected_button.grid(
            row=0, column=1, sticky=tk.N, padx=10, pady=10
        )

    def render_messages(self, is_resolved: bool, tree_name: str, container):
        messages = self.get_messages(is_resolved=is_resolved)

        # Get the data as simple list[str]

        self.data_to_render = []
        self.data_to_render.extend(self._get_data_to_render(messages))

        # No messages, just header
        if not self.data_to_render:
            no_messages_label = tk.Label(
                master=container,
                text="No unresolved messages ✅",
                font=(60),
            )
            no_messages_label.pack()
        else:
            self.header_cols = [
                "ID",
                "Received At",
                "Plan",
                "Camp",
                "Sender",
                "Priority",
                "Message",
            ]
            self.render_tree_table(
                header_cols=self.header_cols,
                data=self.data_to_render,
                container=container,
                tree_name=tree_name,
                col_widths=[
                    25,
                    100,
                    100,
                    100,
                    70,
                    60,
                    250,
                ],
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
                        WHEN urgency = '{message_priorities.Priority.LOW.value}' THEN 3
                        WHEN urgency = '{message_priorities.Priority.MID.value}' THEN 2
                        WHEN urgency = '{message_priorities.Priority.TOP.value}' THEN 1
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

    def _handle_resolve_undo_click(self, resolve_message: bool) -> None:
        """Handles resolve / undo button click"""

        try:
            if resolve_message:
                tree = self.unresolved_tree
                message_row = tree.focus()
                if not message_row:
                    self.render_error_popup_window(
                        message="Select a message to resolve first!"
                    )
                    return
            else:
                tree = self.resolved_tree
                message_row = tree.focus()
                if not message_row:
                    self.render_error_popup_window(
                        message="Select a message to unresolve first!"
                    )
                    return

            message_id = tree.item(message_row, "values")[0]
        except AttributeError as e:
            self.render_error_popup_window(message="No messages!")
            return

        # Update db
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
