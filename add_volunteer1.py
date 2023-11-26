import tkinter as tk
from tkinter import messagebox 

root = tk.Tk()
root.title("Add Volunteer")

fields = [
    ('Camp Name', ''),
    ('Plan Name', 'First Name'),
    ('Last Name', 'Middle Name'),
    ('Nationality', 'Sex'),
    ('Age', 'Email'),
    ('Address', 'Phone Number'),
    ('Emergency Contact Relation', 'Emergency Contact Number')
]

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

def submit(entries):
    for field in fields:
        for name, validation_func in zip(field, [None, None, None, None, validate_age, None, None, None]):
            if name != '':
                value = entries[name].get()
                if validation_func and not validation_func(value):
                    tk.messagebox.showerror("Error", f"Invalid {name}: {value}")
                    return
                print(f"{name}: {value}")

def makeform(root, fields):
    entries = {}
    for field in fields:
        row = tk.Frame(root)
        for name in field:
            if name != '':
                lab = tk.Label(row, width=22, text=name+": ", anchor='w')
                ent = tk.Entry(row)
                lab.pack(side=tk.LEFT)
                ent.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
                entries[name] = ent
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
    return entries

if __name__ == '__main__':
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: submit(e)))
    b1 = tk.Button(root, text='Submit', command=(lambda e=ents: submit(e)))
    b1.pack(side=tk.RIGHT, anchor='se', padx=5, pady=5)
    root.mainloop()
