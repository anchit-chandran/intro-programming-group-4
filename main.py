# Python imports
import logging
import tkinter as tk
import sqlite3

# Project imports
from views import *
from constants import config
from utilities.db import setup_db


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initial setup
        self._initial_setup()
        self.GLOBAL_STATE = {}
        self.view_map = {
            "login": LoginView,
            "plan_detail": PlanDetailView,
            "all_plans": AllPlansView,
            "add_edit_plan": AddEditPlanView,
            "all_volunteers": AllVolunteersView,
            "messages": MessagesView,
            "profile": ProfileView,
            "my_camp": MyCampView,
        }

        # DEBUG HELPERS
        self.DEBUG = True
        if self.DEBUG:
            self.set_global_state(
                {
                    "user_id": 1,
                    "username": "admin",
                    "is_admin": 1,
                }
            )

        self.current_view = None
        # Start at LoginView
        self.switch_to_view("messages")

    def switch_to_view(self, new_view: str) -> None:
        "Helper method to overcome python circular import errors"

        self.switch_view(self.view_map[new_view])

    def logout_set_view_to_login(self) -> None:
        # Reset state
        self.set_global_state({})

        self.switch_view(LoginView)

    def _initial_setup(self) -> None:
        # Initial attributes
        self.title(config.TITLE)
        self.geometry(config.SIZE)

        # DB Setup
        setup_db(reset_database=True)

    def switch_to_default_view_after_login(self) -> None:
        """Based on whether is_admin, switch to default view after login"""
        if self.get_global_state().get("is_admin"):
            self.switch_to_view("all_plans")
        else:
            self.switch_to_view("my_camp")

    def switch_view(self, new_view) -> None:
        # Clear current view
        if self.current_view is not None:
            logging.debug(f"Destroying {self.current_view}")
            self.current_view.destroy()

        self.current_view = new_view(self)
        self.current_view.pack()
        logging.debug(f"Current state: {self.get_global_state()}")

    def get_global_state(self) -> dict:
        return self.GLOBAL_STATE

    def set_global_state(self, new_state: dict) -> None:
        self.GLOBAL_STATE = new_state


def main():
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
