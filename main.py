# Python imports
import tkinter as tk

# Project imports
from views import *
from constants import config


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Initial setup
        self._initial_setup()
        
        self.current_view = None
        self.switch_view(LoginView)
        
    def _initial_setup(self)->None:
        self.title(config.TITLE)
        self.geometry(config.SIZE)

    def switch_view(self, new_view)->None:
        # Clear current view
        if self.current_view:
            self.current_view = None

        self.current_view = new_view(self)
        self.current_view.pack()


def main():
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    main()
