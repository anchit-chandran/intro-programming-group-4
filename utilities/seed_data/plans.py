import datetime

from ..sqlite3_date_formatter import convert_to_sqlite3_date


plan_data = []

for i in range(3):
    new_plan = {
        "title": f"Plan {i}",
        "description": f"This is plan {i}",
        "location": f"Location {i}",
        "start_datetime": convert_to_sqlite3_date(datetime.datetime.now()),
        "end_datetime": None
        if i != 2
        else convert_to_sqlite3_date(
            datetime.datetime.now() + datetime.timedelta(days=5 + i)
        ),
        "central_email": f"central_plan_email_{i}@aid.net",
    }
    
    plan_data.append(new_plan)