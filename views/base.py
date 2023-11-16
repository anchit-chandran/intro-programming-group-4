# Python imports
import logging
import tkinter as tk

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

    def render_nav(self) -> None:
        # Create Navbar
        self.nav_container = tk.Frame(
            master=self,
            width=config.SCREEN_WIDTH,
            height=20,
            relief=tk.FLAT,
            bg="black",
            borderwidth=1,
        )
        self.nav_container.pack(
            pady=10,
        )

        self.nav_items_left_container = tk.Frame(
            master=self.nav_container,
        )
        self.nav_items_left_container.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.all_plans_button = tk.Button(
            master=self.nav_items_left_container,
            text="All Plans",
            command=self._handle_all_plans_click,
        )
        self.all_plans_button.grid(row=0, column=0, sticky="w")

        self.volunteer_list_button = tk.Button(
            master=self.nav_items_left_container,
            text="Volunteer List",
            command=self._handle_volunteers_list_click,
        )
        self.volunteer_list_button.grid(
            row=0,
            column=1,
            sticky="w",
        )

        self.messages_button = tk.Button(
            master=self.nav_items_left_container,
            text="Messages",
            command=self._handle_messages_click,
        )
        self.messages_button.grid(row=0, column=2, sticky="w")

        self.nav_items_right_container = tk.Frame(
            master=self.nav_container,
        )
        self.nav_items_right_container.grid(
            row=0,
            column=1,
            sticky="e",
        )
        self.logout_button = tk.Button(
            master=self.nav_items_right_container,
            text="Logout",
            command=self._handle_logout,
            relief=tk.FLAT,
        )
        self.logout_button.pack(
            side="right",
            anchor="e",
        )
