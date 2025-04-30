import json
import re
from difflib import get_close_matches

def normalize_name(name):
    name = name.lower()
    name = re.sub(r'\(.*?\)', '', name)  
    name = re.sub(r'[^a-z0-9]', '', name)  
    return name.strip()

# Charger les deux fichiers
with open("all_vehicles_data.json", "r", encoding="utf-8") as f1:
    all_vehicles = json.load(f1)

with open("nom_vehicules_occupants.json", "r", encoding="utf-8") as f2:
    seats_data = json.load(f2)

seats_dict = {
    normalize_name(vehicle["DisplayName"]): vehicle["MaxOccupants"]
    for vehicle in seats_data
}

result = []
for v in all_vehicles:
    nom_vehicule = v.get("Nom véhicule", "")
    normalized = normalize_name(nom_vehicule)
    max_occupants = seats_dict.get(normalized)

    if not max_occupants:
        close = get_close_matches(normalized, seats_dict.keys(), n=1, cutoff=0.85)
        if close:
            max_occupants = seats_dict[close[0]]

    v["MaxOccupants"] = max_occupants if max_occupants else "Inconnu"
    result.append(v)

with open("vehicules_avec_occupants.json", "w", encoding="utf-8") as out:
    json.dump(result, out, indent=4, ensure_ascii=False)

print("✅ Fichier 'vehicules_avec_occupants.json' généré.")
