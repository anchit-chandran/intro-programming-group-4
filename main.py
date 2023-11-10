# Python imports
import logging
import tkinter as tk

# Project imports
from views.login import LoginView
from constants import config


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initial setup
        self._initial_setup()

        # Start at LoginView
        self.current_view = None
        self.switch_view(LoginView)

    def _initial_setup(self) -> None:
        self.title(config.TITLE)
        self.geometry(config.SIZE)

    def switch_view(self, new_view) -> None:
        # Clear current view
        if self.current_view is not None:
            logging.debug(f'Destroying {self.current_view}')
            for frame in self.current_view.container.winfo_children():
                frame.destroy()
            self.current_view.destroy()

        self.current_view = new_view(self)
        self.current_view.pack()


def main():
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
