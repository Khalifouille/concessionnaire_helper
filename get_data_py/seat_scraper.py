import json

with open("sieges_voitures.json", "r", encoding="utf-8") as f:
    data = json.load(f)

vehicles = []
for vehicle_dict in data:
    for vehicle_id, vehicle_info in vehicle_dict.items():
        display_name = vehicle_info.get("DisplayName")
        max_occupants = vehicle_info.get("MaxOccupants")
        vehicles.append({
            "DisplayName": display_name,
            "MaxOccupants": max_occupants
        })

with open("nom_vehicules_occupants.json", "w", encoding="utf-8") as f_out:
    json.dump(vehicles, f_out, indent=4, ensure_ascii=False)

print("Fichier 'nom_vehicules_occupants.json' créé avec succès.")
