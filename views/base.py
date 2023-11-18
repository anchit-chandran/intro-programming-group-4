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

    def _handle_home_click(self) -> None:
        self.master.switch_to_view("dashboard")
    
    def _handle_my_camp_click(self) -> None:
        self.master.switch_to_view("my_camp")
    
    def _handle_profile(self) -> None:
        self.master.switch_to_view("profile")

    def render_nav(self) -> None:
        # Create Navbar
        
        self.nav_container = tk.Frame(
            master=self,
            width=800,
            height=20,
            bg='black',
        )
        self.nav_container.pack(
            pady=10,
        )

        if self.master.get_global_state().get("is_admin"):
            self.volunteer_list_button = tk.Button(
                master=self.nav_container,
                text="Home",
                command=self._handle_home_click,
            )
            self.volunteer_list_button.grid(
                row=0,
                column=0,
                sticky="w",
            )

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

            self.messages_button = tk.Button(
                master=self.nav_container,
                text="Messages",
                command=self._handle_messages_click,
            )
            self.messages_button.grid(
                row=0,
                column=3,
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
            column=4,
            sticky="e",
        )
        self.logout_button = tk.Button(
            master=self.nav_container,
            text="Logout",
            command=self._handle_logout,
        )
        self.logout_button.grid(
            row=0,
            column=5,
            sticky="e",
        )
