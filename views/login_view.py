import tkinter as tk

class LoginView(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()
    
    def render_widgets(self)->None:
        """Renders widgets for view"""
        self.header = tk.Label(self.master, text='LOGIN VIEW')
        self.header.pack()
    
    