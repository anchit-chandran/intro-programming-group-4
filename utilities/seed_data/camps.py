from ..sqlite3_date_formatter import convert_to_sqlite3_date


camp_data = []

# for each plan 1 - 3
for plan_id in range(1,4):
    
    # create 3 camps
    for j in range(3):
        new_camp = {
            "name": f"Camp {j}",
            "location": f"Location {j}",
            "maxCapacity": (j * 10) + 30,
            "plan_id": plan_id
        }
        
        camp_data.append(new_camp)