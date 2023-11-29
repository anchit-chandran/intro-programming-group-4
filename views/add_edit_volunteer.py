import tkinter as tk
from tkinter import messagebox
from views.base import BaseView
from constants import config

class AddEditUserView(BaseView):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.render_widgets()

    def render_widgets(self) -> None:
        """Renders widgets for view"""

        # Create container
        self.container = tk.Frame(
            master=self,
            width=config.SCREEN_WIDTH,
            height=300,
        )
        self.container.pack(
            fill="both",
            padx=30,
            pady=100,
        )

        # Header
        self.header_container = tk.Frame(self.container)
        self.header_container.pack(pady=15, fill="x", expand=True)

        self.header = tk.Label(
            master=self.header_container,
            text="Add edit user view",
            font=('Arial', 16, 'bold'),  
        )
        self.header.pack(
            side="left",
        )

    def render_error_popup_window(self, message='YOUR MESSAGE'):
        messagebox.showerror("Error", message)

def validate_age(age):
    try:
        age = int(age)
        if age < 0:
            raise ValueError("Age cannot be negative.")
        return True
    except ValueError:
        return False

def validate_email(email):
    return '@' in email

def validate_phone_number(phone_number):
    return len(phone_number) >= 10 and phone_number.isdigit()

def submit(entries, fields, view):
    for field in fields:
        for name, validation_func in zip(field, [None, None, None, None, validate_age, None, None, None]):
            if name != '':
                value = entries[name].get()
                if validation_func and not validation_func(value):
                    view.render_error_popup_window(f"Invalid {name}: {value}")
                    return
                print(f"{name}: {value}")

def makeform(root, fields, view):
    entries = {}
    for field_set in fields:
        row = tk.Frame(root)
        for name in field_set:
            if name != '':
                lab = tk.Label(row, width=22, text=name+": ", anchor='w')
                ent = tk.Entry(row)
                lab.pack(side=tk.LEFT)
                ent.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
                entries[name] = ent
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    return entries

if __name__ == '__main__':
    root = tk.Tk()
    add_edit_view = AddEditUserView(root) 
    fields = [
        ('Camp Name', ''),
        ('Plan Name', 'First Name'),
        ('Last Name', 'Middle Name'),
        ('Nationality', 'Sex'),
        ('Age', 'Email'),
        ('Address', 'Phone Number'),
        ('Emergency Contact Relation', 'Emergency Contact Number')
    ]
    ents = makeform(root, fields, add_edit_view)
    root.bind('<Return>', (lambda event, e=ents: submit(e, fields, add_edit_view)))
    b1 = tk.Button(root, text='Submit', command=(lambda e=ents: submit(e, fields, add_edit_view)))
    b1.pack(side=tk.RIGHT, anchor='se', padx=5, pady=5)
    root.mainloop()

