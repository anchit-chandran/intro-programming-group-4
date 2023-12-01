camp_data = []
camp_resource_data = []

# for each plan 1 - 3
names = ['Alpha', 'Beta', 'Gamma']
for plan_id in range(1, 4):
    # create 3 camps
    for j in range(3):
        new_camp = {
            "name": f"Camp {names[j]}",
            "location": f"Location {j}",
            "maxCapacity": (j * 10) + 30,
            "plan_id": plan_id,
        }

        camp_data.append(new_camp)

RESOURCE_NAMES = ["Food", "Water", "Medicine", "Clothing"]
# add resources for each camp
for camp_id in range(2, len(camp_data) + 1):
    # create resources, per camp
    for j in range(len(RESOURCE_NAMES)):
        new_resource = {
            "name": f"{RESOURCE_NAMES[j]}",
            "amount": 100 * j if j else 100,
            "camp_id": camp_id,
        }

        camp_resource_data.append(new_resource)
