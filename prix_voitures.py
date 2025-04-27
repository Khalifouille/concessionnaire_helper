import json

with open('all_vehicles_data.json', 'r', encoding='utf-8') as f:
    vehicle_data = json.load(f)

def search_vehicle(vehicle_name):
    for vehicle in vehicle_data:
        if vehicle_name.lower() in vehicle['Nom véhicule'].lower():
            return vehicle['Catégorie'], vehicle['Prix']
    return None

vehicle_name = input("Entrez le nom du véhicule que vous cherchez : ")

result = search_vehicle(vehicle_name)

if result:
    category, price = result
    print(f"Le véhicule '{vehicle_name}' se trouve dans la catégorie '{category}' et coûte {price}.")
else:
    print(f"Le véhicule '{vehicle_name}' n'a pas été trouvé.")
