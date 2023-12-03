import random

from .camps import camp_data

refugee_family_data = []
NAMES = ["Aria", "Mateo", "Yuna", "Jasper", "Nia", "Emiliano", "Freya", "Kaito", "Lila", "Samir"]
MEDICAL_CONDITIONS = ["Asthma", "Diabetes", "Atherosclerosis", "Lung Cancer", "HIV/AIDS", "Mental Health", "Sciatica"]

# for each camp
for camp_id in range(1,len(camp_data)+1):
    
    # make 30 families
    for i in range(15):
        new_refugee_family = {
            "main_rep_name" : NAMES[i%len(NAMES)],
            "medical_conditions" : random.choice(MEDICAL_CONDITIONS),
            "n_adults" : random.randint(0,3),
            "n_children" : random.randint(0,5),
            "main_rep_home_town" : f"Town {camp_id}-{i}",
            "main_rep_age" : random.randint(18,90),
            "main_rep_sex" : random.randint(0,3),
            "n_missing_members" : random.randint(0,3),
            "is_in_camp" : 0 if i == 9 else 1,
            "camp_id" : camp_id,
        }
        
        refugee_family_data.append(new_refugee_family)