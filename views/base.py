# Python imports
import logging
import tkinter as tk
from tkinter import messagebox

from utilities.db import run_query_get_rows
from constants import config
from constants.console_color_codes import PrintColor


class BaseView(tk.Frame):
    def __init__(self, master=None, render_nav: bool = True):
        super().__init__(master)
        logging.debug(
            f"{PrintColor.HEADER}{self.__class__.__name__} created {PrintColor.ENDC}"
        )
        self.master = master
        if render_nav:
            self.render_nav()

        self.current_nav_item = None

    def _handle_logout(self) -> None:
        logging.debug("Logging out")
        self.master.logout_set_view_to_login()

    def _handle_all_plans_click(self) -> None:
        self.master.switch_to_view("all_plans")

    def _handle_volunteers_list_click(self) -> None:
        self.master.switch_to_view("all_volunteers")

    def _handle_messages_click(self) -> None:
        self.master.switch_to_view("messages")

    def _handle_my_camp_click(self) -> None:
        user_id = self.master.get_global_state().get("user_id")
        camp_id = run_query_get_rows(f"""
                                     SELECT camp_id
                                     FROM User
                                     WHERE id={user_id}
                                     """)[0]['camp_id']
        
        current_state = self.master.get_global_state() 
        current_state['camp_id_to_view'] = camp_id
        self.master.set_global_state(current_state)
        
        self.master.switch_to_view("camp_detail")

    def _handle_profile(self) -> None:
        self.master.switch_to_view("profile")

    def _handle_messages(self) -> None:
        self.master.switch_to_view("messages")

    def _delete_window(self, window: tk.Toplevel) -> None:
        window.destroy()

    def render_error_popup_window(self, title='Invalid', message: str='') -> None:
        messagebox.showerror(title=title, message=message)
    

    def render_nav(self) -> None:
        # Create Navbar

        self.nav_container = tk.Frame(
            master=self,
            width=800,
            height=20,
        )
        self.nav_container.pack(
            pady=10,
        )

        if self.master.get_global_state().get("is_admin"):
            self.all_plans_button = tk.Button(
                master=self.nav_container,
                text="All Plans",
                command=self._handle_all_plans_click,
            )
            self.all_plans_button.grid(
                row=0,
                column=1,
                sticky="w",
            )

            self.volunteer_list_button = tk.Button(
                master=self.nav_container,
                text="Volunteer List",
                command=self._handle_volunteers_list_click,
            )
            self.volunteer_list_button.grid(
                row=0,
                column=2,
                sticky="w",
            )

        else:
            # volunteer buttons
            self.my_camp_button = tk.Button(
                master=self.nav_container,
                text="My Camp",
                command=self._handle_my_camp_click,
            )
            self.my_camp_button.grid(
                row=0,
                column=3,
                sticky="w",
            )



        self.profile_button = tk.Button(
            master=self.nav_container,
            text="My Profile",
            command=self._handle_profile,
        )
        self.profile_button.grid(
            row=0,
            column=5,
            sticky="e",
        )

        # Get n(messages)
        n_unresolved_messages = len(
            run_query_get_rows(
                f"SELECT * FROM messages WHERE is_resolved = 0 AND receiver_id = {self.master.get_global_state().get('user_id')}"
            )
        )

        self.messages_button = tk.Button(
            master=self.nav_container,
            text=f"Messages ({n_unresolved_messages})",
            command=self._handle_messages,
        )
        self.messages_button.grid(
            row=0,
            column=6,
            sticky="w",
        )

        self.refresh_button = tk.Button(
            master=self.nav_container,
            text="Refresh 🔁",
            command=self.master.refresh_view,
        )
        self.refresh_button.grid(
            row=0,
            column=7,
            sticky="e",
        )

        self.logout_button = tk.Button(
            master=self.nav_container,
            text="Logout",
            command=self._handle_logout,
        )
        self.logout_button.grid(
            row=0,
            column=8,
            sticky="e",
        )

        self.username_frame = tk.LabelFrame(
            master=self.nav_container,
            text="Account",
        )
        self.username_frame.grid(
            row=0,
            column=9,
            sticky="w",
        )
        self.role_text = (
            "Admin" if self.master.get_global_state().get("is_admin") else "Volunteer"
        )
        self.user_text = tk.Label(
            master=self.username_frame,
            text=f"{self.master.get_global_state().get('username')} ({self.role_text})",
            fg="green",
        )
        self.user_text.pack(padx=5, pady=5)

    def set_character_limit(self, entry_text:tk.StringVar, char_limit: int) -> None:
        """Set character limit for entry_text (exclusive)
        
        E.g.
            # Set char limit of 50
            self.message = tk.StringVar()
            self.message.trace(
                "w", lambda *args: self.set_character_limit(entry_text = self.message, char_limit=50)
            )
        """
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:char_limit])