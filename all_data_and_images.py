import json
import re
import os
from difflib import get_close_matches

def normalize_name(name):
    name = name.lower()
    name = re.sub(r'\(.*?\)', '', name)  
    name = re.sub(r'[^a-z0-9]', '', name)  
    return name.strip()

def find_image_for_vehicle(vehicle_name, image_dir="vehicle_images"):
    normalized = normalize_name(vehicle_name)
    
    for filename in os.listdir(image_dir):
        if normalize_name(filename.split('.')[0]) == normalized:
            return os.path.join(image_dir, filename)
    
    all_images = [f.split('.')[0] for f in os.listdir(image_dir)]
    close_matches = get_close_matches(normalized, all_images, n=1, cutoff=0.85)
    if close_matches:
        return os.path.join(image_dir, close_matches[0] + '.png')
    
    return None

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
    
    image_path = find_image_for_vehicle(nom_vehicule)
    
    v["MaxOccupants"] = max_occupants if max_occupants else "Inconnu"
    v["Image"] = image_path if image_path else "Non disponible"
    result.append(v)

with open("vehicules_avec_images.json", "w", encoding="utf-8") as out:
    json.dump(result, out, indent=4, ensure_ascii=False)

print("✅ Fichier 'vehicules_avec_images.json' généré avec succès!")
print(f"🔢 Statistiques:")
print(f"- Véhicules traités: {len(result)}")
print(f"- Images associées: {len([v for v in result if v['Image'] != 'Non disponible'])}")