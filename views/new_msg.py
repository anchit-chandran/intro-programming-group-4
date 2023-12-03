"""TEMPLATE FILE FOR MAKING NEW VIEW"""
# Python imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import logging
import datetime

# Project imports
from views.base import BaseView
from constants import config
from constants.message_priorities import Priority
from utilities.db import run_query_get_rows, insert_query_with_values


class NewMessageView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # sets the self.camp_title and self.plan_title variables
        self.set_current_user_plan_and_camp()
        self.render_widgets()
        self.update()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
            width=config.SCREEN_WIDTH,
            height=500,
        )
        self.container.pack(
            fill="both",
            padx=30,
            pady=100,
        )
        
        # Instructions label
        self.instructions_container = ttk.LabelFrame(
            master=self.container,
            text="Instructions",
        )
        self.instructions_container.pack()
        self.instructions_label = tk.Label(
            master=self.instructions_container,
            text="Please select to whom you would like to send the message and the urgency.\n\nMessages should be succinct, at most 40 characters.",
            anchor="w",
            justify="left",
        )
        self.instructions_label.pack()

        self.main_container = tk.LabelFrame(
            self.container, text="New Message", width=500, height=100
        )
        self.main_container.pack(pady=15, fill="x", expand=True)

        # ADD FORM BOXES

        LABEL_WIDTH = 12
        BOX_WIDTH = 40

        self.plan_label = tk.Label(self.main_container, text="Plan", width=LABEL_WIDTH)
        self.plan_box = tk.Entry(
            self.main_container,
            state="disabled",
            width=BOX_WIDTH,
            textvariable=tk.StringVar(value=self.plan_title),
        )

        self.camp_label = tk.Label(self.main_container, text="Camp", width=LABEL_WIDTH)
        self.camp_box = tk.Entry(
            self.main_container,
            state="disabled",
            width=BOX_WIDTH,
            textvariable=tk.StringVar(value=self.camp_title),
        )

        self.from_label = tk.Label(self.main_container, text="From", width=LABEL_WIDTH)
        self.from_box = tk.Entry(
            self.main_container,
            state="disabled",
            width=BOX_WIDTH,
            textvariable=tk.StringVar(
                value=self.master.get_global_state().get("username")
            ),
        )

        AVAILABLE_OPTIONS_SEND_TO = self.get_available_options_send_to()
        self.selected_option_send_to = tk.StringVar(value=AVAILABLE_OPTIONS_SEND_TO[0])
        self.to_label = tk.Label(self.main_container, text="To", width=LABEL_WIDTH)
        self.to_option_box = tk.OptionMenu(
            self.main_container,
            self.selected_option_send_to,
            *AVAILABLE_OPTIONS_SEND_TO,
            command=self.handle_to_select_change_send_to,
        )
        self.to_option_box.config(width=BOX_WIDTH - 4)

        self.message_content_string_var = tk.StringVar()
        self.message_content_label = tk.Label(
            self.main_container, text="Message\n(max: 40 chars)", width=LABEL_WIDTH
        )
        self.message_content_box = tk.Entry(
            self.main_container,
            width=BOX_WIDTH,
            textvariable=self.message_content_string_var,
        )
        # Set char limit of 50
        self.message_content_string_var.trace(
            "w", lambda *args: self.set_character_limit(self.message_content_string_var)
        )

        AVAILABLE_OPTIONS_URGENCY = [priority.value for priority in Priority]
        self.selected_option_urgency = tk.StringVar(value=AVAILABLE_OPTIONS_URGENCY[0])
        self.urgency_label = tk.Label(
            self.main_container, text="Urgency", width=LABEL_WIDTH
        )
        self.urgency_option_box = tk.OptionMenu(
            self.main_container,
            self.selected_option_urgency,
            *AVAILABLE_OPTIONS_URGENCY,
            command=self.handle_to_select_change_urgency,
        )
        self.urgency_option_box.config(width=BOX_WIDTH - 4)

        self.send_button = tk.Button(
            self.main_container, text="Send", width=10, command=self.handle_send_message
        )

        self.plan_label.grid(row=0, column=0)
        self.plan_box.grid(row=0, column=1, sticky="e")

        self.camp_label.grid(row=1, column=0, sticky="e")
        self.camp_box.grid(row=1, column=1, sticky="e")

        self.from_label.grid(row=2, column=0, sticky="e")
        self.from_box.grid(row=2, column=1, sticky="e")

        self.to_label.grid(row=3, column=0, sticky="e")
        self.to_option_box.grid(row=3, column=1, sticky="e")

        self.urgency_label.grid(row=4, column=0, sticky="e")
        self.urgency_option_box.grid(row=4, column=1, sticky="e")

        self.message_content_label.grid(row=5, column=0, sticky="e")
        self.message_content_box.grid(row=5, column=1, sticky="e")

        self.send_button.grid(row=6, column=1, sticky="w", padx=30, pady=10)

    def get_all_data_for_msg(self) -> dict:
        # Ensure message content is not empty
        message = self.message_content_string_var.get()
        if not message:
            self.render_error_popup_window(message="Message content can't be empty")
            return

        sent_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        urgency = self.selected_option_urgency.get()
        is_resolved = False
        sender_id = self.master.get_global_state().get("user_id")
        receiver_id = self.get_id_from_username(self.selected_option_send_to.get())

        return {
            "message": message,
            "sent_at": sent_at,
            "urgency": urgency,
            "is_resolved": is_resolved,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
        }

    def get_id_from_username(self, username: str) -> int:
        return run_query_get_rows(f"SELECT id FROM User WHERE username = '{username}'")[
            0
        ]["id"]

    def handle_send_message(self):
        data = self.get_all_data_for_msg()

        if data is None:
            return

        logging.info(f"Sending message: {data}")
        insert_query_with_values(
            query="""INSERT INTO Messages 
                  (
                    "message",
                    "sent_at",
                    "urgency",
                    "is_resolved",
                    "sender_id",
                    "receiver_id"
                      ) VALUES (
 
                        :message,
                        :sent_at,
                        :urgency,
                        :is_resolved,
                        :sender_id,
                        :receiver_id
                  );
                  """,
            values={
                "message": data["message"],
                "sent_at": data["sent_at"],
                "urgency": data["urgency"],
                "is_resolved": data["is_resolved"],
                "sender_id": data["sender_id"],
                "receiver_id": data["receiver_id"],
            },
        )
        self.handle_successful_msg_sent()

    def handle_successful_msg_sent(self, message=""):
        messagebox.showinfo(title="📨 Success", message=f"Message sent!")
        self.master.switch_to_view("messages")

    def handle_to_select_change_send_to(self, value):
        return

    def handle_to_select_change_urgency(self, value):
        return

    def get_available_options_send_to(self) -> list[str]:
        # admin
        all_users = run_query_get_rows(
            f"SELECT username FROM User WHERE id != {self.master.get_global_state().get('user_id')}"
        )
        all_users_list = [user["username"] for user in all_users]
        return all_users_list

    def set_current_user_plan_and_camp(self):
        # ADMINS NOT ASSIGNED TO CAMP / PLAN
        if self.master.get_global_state().get("is_admin"):
            self.camp_title = "-"
            self.plan_title = "-"
            return

        camp_id = run_query_get_rows(
            f"SELECT camp_id FROM User WHERE id = {self.master.get_global_state().get('user_id')}"
        )[0]["camp_id"]
        camp_data = run_query_get_rows(f"SELECT * FROM Camp WHERE id = {camp_id}")[0]
        camp_name = camp_data["name"]
        camp_id = camp_data["id"]

        self.camp_title = f"{camp_name} (ID: {camp_id})"

        plan_id = run_query_get_rows(f"SELECT plan_id FROM Camp WHERE id = {camp_id}")[
            0
        ]["plan_id"]
        plan_data = run_query_get_rows(f"SELECT * FROM Plan WHERE id = {plan_id}")[0]
        plan_name = plan_data["title"]
        plan_id = plan_data["id"]

        self.plan_title = f"{plan_name} (ID: {plan_id})"

    def set_character_limit(self, entry_text):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:40])
