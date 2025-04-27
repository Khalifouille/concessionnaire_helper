import tkinter as tk
import json

with open('all_vehicles_data.json', 'r', encoding='utf-8') as f:
    vehicle_data = json.load(f)

def search_vehicle(vehicle_name):
    for vehicle in vehicle_data:
        if vehicle_name.lower() in vehicle['Nom véhicule'].lower():
            return vehicle['Catégorie'], vehicle['Prix']
    return None

def on_search():
    vehicle_name = entry.get()
    result = search_vehicle(vehicle_name)
    
    if result:
        category, price = result
        result_label.config(text=f"Catégorie : {category}\nPrix : {price}")
    else:
        result_label.config(text="Non trouvée")

root = tk.Tk()
root.title("Recherche de Véhicule")

label = tk.Label(root, text="Entrez le nom du véhicule :")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

search_button = tk.Button(root, text="Rechercher", command=on_search)
search_button.pack(pady=20)

result_label = tk.Label(root, text="", font=('Arial', 12), justify='left')
result_label.pack(pady=20)

root.mainloop()
