# Python imports
import logging
import tkinter as tk
import sqlite3

# Project imports
from views import DashboardView, LoginView, AllPlansView
from constants import config
from utilities.db import setup_db


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initial setup
        self._initial_setup()
        self.GLOBAL_STATE = {}

        # Start at LoginView
        self.current_view = None
        self.switch_view(DashboardView)

    def switch_to_view(self, new_view:str)->None:
        "Helper method to overcome python circular import errors"
        view_map = {
            'login' : LoginView,
            'dashboard' : DashboardView,
            'all_plans': AllPlansView,
        }
        self.switch_view(view_map[new_view])
    
    def logout_set_view_to_login(self)->None:
        # Reset state
        self.set_global_state({})
        
        self.switch_view(LoginView)
    
    def _initial_setup(self) -> None:
        
        # Initial attributes
        self.title(config.TITLE)
        self.geometry(config.SIZE)
        
        # DB Setup
        setup_db(reset_database=True)

    def switch_view(self, new_view) -> None:
        # Clear current view
        if self.current_view is not None:
            logging.debug(f'Destroying {self.current_view}')
            self.current_view.destroy()

        self.current_view = new_view(self)
        self.current_view.pack()
        logging.debug(f'Current state: {self.get_global_state()}')
    
    def get_global_state(self)->dict:
        return self.GLOBAL_STATE
    
    def set_global_state(self, new_state:dict)->None:
        self.GLOBAL_STATE = new_state
    
        


def main():
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
