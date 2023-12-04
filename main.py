# Python imports
import logging
import tkinter as tk
import sqlite3

# Project imports
from views import *
from constants import config
from utilities.db import setup_db, run_query_get_rows


class MainApplication(tk.Tk):
    def __init__(self, testing: bool = False):
        super().__init__()
        self.testing = testing
        # Initial setup
        self._initial_setup()
        self.GLOBAL_STATE = {}
        self.view_map = {
            "login": LoginView,
            "plan_detail": PlanDetailView,  # Needs plan_id_to_view in global state
            "all_plans": AllPlansView,
            "add_edit_plan": AddEditPlanView,  # Needs plan_id_to_edit if edit in global state
            "add_edit_camp": AddEditCampView,  # Needs plan_id_for_camp if adding; camp_id_to_edit if edit
            "camp_detail": CampDetailView,  # Needs camp_id_to_view in global state
            "all_volunteers": AllVolunteersView,
            "messages": MessagesView,
            "profile": ProfileView,  # gets user_id from global state if editing self, volunteer_id_to_edit if editing volunteer, add_volunteer if adding volunteer, volunteer_id_to_view if viewing volunteer
            "new_msg": NewMessageView,
            "edit_resources": EditResourcesView,  # Needs camp_id_for_resources in global state,
            "new_resource": NewResourceView,  # Needs camp_id_for_resources in global state,
            "add_edit_refugee": AddEditRefugeeView,  # Needs refugee_id_to_edit if edit and camp_id_to_view from state if add
            "departed_refugees": DepartedRefugeesView,  # Needs camp_id_to_view from state
            "refugee_profile": RefugeeProfileView,  # Needs refugee_id_to_view in global state
            "search":SearchView,
        }
        # Create the reverse map
        self.reverse_view_map = {}
        for view_name, view in self.view_map.items():
            self.reverse_view_map.update({view: view_name})

        # DEBUG HELPERS
        self.DEBUG = True or testing
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
        self.switch_to_view("search")

    def switch_to_view(self, new_view: str) -> None:
        "Helper method to overcome python circular import errors"

        self._render_new_view(self.view_map[new_view])

    def logout_set_view_to_login(self) -> None:
        # Reset state
        self.set_global_state({})

        self._render_new_view(LoginView)

    def _initial_setup(self) -> None:
        # Initial attributes
        self.title(config.TITLE)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}") # thanks https://stackoverflow.com/questions/54296506/how-to-show-minimize-and-maximize-buttons-tkinter
        if not self.testing: self.iconbitmap(config.LOGOICO) # doesnt run on github actions
        # self.attributes('-fullscreen', True)

        # DB Setup
        setup_db(reset_database=True)

    def switch_to_default_view_after_login(self) -> None:
        """Based on whether is_admin, switch to default view after login"""
        if self.get_global_state().get("is_admin"):
            self.switch_to_view("all_plans")
        else:
            user_id = self.get_global_state().get("user_id")
            camp_id = run_query_get_rows(
                f"""
                                        SELECT camp_id
                                        FROM User
                                        WHERE id={user_id}
                                        """
            )[0]["camp_id"]

            current_state = self.get_global_state()
            current_state["camp_id_to_view"] = camp_id
            self.set_global_state(current_state)
            self.switch_to_view("camp_detail")

    def _render_new_view(self, new_view) -> None:
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

    def refresh_view(self) -> None:
        """Reloads the current view"""
        logging.info(
            f"Refreshing view: {self.current_view}. Current_state: {self.get_global_state()}"
        )
        self.switch_to_view(self.reverse_view_map[self.current_view.__class__])


def main():
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
