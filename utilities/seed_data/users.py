from datetime import date
from constants.config import SEX_VALUES

user_data = [
    {
        "username": "admin",
        "password": "111",
        "dob": date(1997, 10, 18),
        "sex": SEX_VALUES[0],
        "phone_number": "07777777777",
        "is_active": 1,
        "is_admin": 1,
        "first_name": "Admin",
        "last_name": "McAdminFace",
        "languages_spoken": "English,Farsi",
        "skills": None,
        "emergency_contact_name": "Andrew",
        "emergency_contact_number": "+447986756453",
        "camp_id": None,
    },
    {
        "username": "volunteer1",
        "password": "111",
        "dob": date(1997, 10, 18),
        "sex": SEX_VALUES[1],
        "phone_number": "07777777777",
        "is_active": 1,
        "is_admin": 0,
        "first_name": "volunteer1",
        "last_name": "Lastname",
        "languages_spoken": "English,Spanish,German,French",
        "skills": "Doctor",
        "emergency_contact_name": "Andrew",
        "emergency_contact_number": "+447986756453",
        "camp_id": 1,
    },
    {
        "username": "volunteer2",
        "password": "111",
        "dob": date(1997, 10, 18),
        "sex": SEX_VALUES[1],
        "phone_number": "07777777777",
        "is_active": 1,
        "is_admin": 0,
        "first_name": "volunteer2",
        "last_name": "Lastname",
        "languages_spoken": "English,Chinese",
        "skills": "Art Therapy",
        "emergency_contact_name": "Andrew",
        "emergency_contact_number": "+447986756453",
        "camp_id": 1,
    },
    {
        "username": "volunteer3",
        "password": "111",
        "dob": date(1997, 10, 18),
        "sex": SEX_VALUES[1],
        "phone_number": "07777777777",
        "is_active": 1,
        "is_admin": 0,
        "first_name": "Volunteer3",
        "last_name": "Lastname",
        "languages_spoken": "English,Hindi,Lebanese",
        "skills": "Teacher",
        "emergency_contact_name": "Andrew",
        "emergency_contact_number": "+447986756453",
        "camp_id": 2,
        
    },
    {
        "username": "deactivatedVolunteer",
        "password": "111",
        "dob": date(1997, 10, 18),
        "sex": SEX_VALUES[2],
        "phone_number": "07777777777",
        "is_active": 0,
        "is_admin": 0,
        "first_name": "Volunteer3",
        "last_name": "Lastname",
        "languages_spoken": "English,Hindi,Lebanese",
        "skills": "Teacher",
        "emergency_contact_name": "Andrew",
        "emergency_contact_number": "+447986756453",
        "camp_id": 2,
    },
]
