import datetime

plan_data = []

locations = ["Palestine", "Ukraine", "Africa"]

for i in range(3):
    new_plan = {
        "title": f"Plan {i}",
        "description": f"This is plan {i}",
        "location": f"{locations[i]}",
        "start_date": datetime.date.today(),
        "end_date": None
        if i != 2
        else datetime.date.today() + datetime.timedelta(days=5 + i),
        "central_email": f"central_plan_email_{i}@aid.net",
    }

    plan_data.append(new_plan)
