import tkinter as tk
from tkinter import messagebox
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
        messagebox.showinfo("Résultat", f"Le véhicule '{vehicle_name}' se trouve dans la catégorie '{category}' et coûte {price}.")
    else:
        messagebox.showwarning("Non trouvé", f"Le véhicule '{vehicle_name}' n'a pas été trouvé.")

root = tk.Tk()
root.title("Recherche de Véhicule")

label = tk.Label(root, text="Entrez le nom du véhicule :")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

search_button = tk.Button(root, text="Rechercher", command=on_search)
search_button.pack(pady=20)

root.mainloop()
