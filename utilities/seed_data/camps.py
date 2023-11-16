camp_data = []
camp_resource_data = []

# for each plan 1 - 3
for plan_id in range(1, 4):
    # create 3 camps
    for j in range(3):
        new_camp = {
            "name": f"Camp {j}",
            "location": f"Location {j}",
            "maxCapacity": (j * 10) + 30,
            "plan_id": plan_id,
        }

        camp_data.append(new_camp)

RESOURCE_NAMES = ["Food", "Water", "Medicine"]
# add resources for each camp
for camp_id in range(1, len(camp_data) + 1):
    # create 3 resources, per camp
    for resource in range(1, 4):
        new_resource = {
            "name": f"{RESOURCE_NAMES[resource-1]}",
            "amount": 100 * resource,
            "camp_id": camp_id,
        }

        camp_resource_data.append(new_resource)
