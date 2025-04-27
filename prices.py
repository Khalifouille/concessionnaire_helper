import tkinter as tk
import json

with open('all_vehicles_data.json', 'r', encoding='utf-8') as f:
    vehicle_data = json.load(f)

def search_vehicle(vehicle_name, category=None, min_price=None, max_price=None):
    results = []
    for vehicle in vehicle_data:
        if vehicle_name.lower() in vehicle['Nom véhicule'].lower():
            if category and vehicle['Catégorie'].lower() != category.lower():
                continue
            if min_price and vehicle['Prix'] < min_price:
                continue
            if max_price and vehicle['Prix'] > max_price:
                continue
            results.append(vehicle)
    return results

def on_search(event=None):
    vehicle_name = entry_name.get().strip()
    category = entry_category.get().strip()
    
    try:
        min_price = float(entry_min_price.get().strip()) if entry_min_price.get().strip() else None
        max_price = float(entry_max_price.get().strip()) if entry_max_price.get().strip() else None
    except ValueError:
        result_label.config(text="❌ Prix invalide.")
        return

    if not vehicle_name:  
        result_label.config(text="Veuillez entrer un nom de véhicule.")
        return

    results = search_vehicle(vehicle_name, category, min_price, max_price)
    
    if results:
        result_text = ""
        for vehicle in results:
            result_text += f"Nom : {vehicle['Nom véhicule']}\nCatégorie : {vehicle['Catégorie']}\nPrix : {vehicle['Prix']}$\n\n"
        result_label.config(text=result_text)
    else:
        result_label.config(text="Non trouvée")

root = tk.Tk()
root.title("Recherche de Véhicule")

label_name = tk.Label(root, text="Entrez le nom du véhicule :")
label_name.pack(pady=5)

entry_name = tk.Entry(root, width=30)
entry_name.pack(pady=5)

label_category = tk.Label(root, text="Catégorie de véhicule (optionnelle) :")
label_category.pack(pady=5)

entry_category = tk.Entry(root, width=30)
entry_category.pack(pady=5)

label_min_price = tk.Label(root, text="Prix minimum (optionnel) :")
label_min_price.pack(pady=5)

entry_min_price = tk.Entry(root, width=30)
entry_min_price.pack(pady=5)

label_max_price = tk.Label(root, text="Prix maximum (optionnel) :")
label_max_price.pack(pady=5)

entry_max_price = tk.Entry(root, width=30)
entry_max_price.pack(pady=5)

entry_name.bind("<Return>", on_search)

search_button = tk.Button(root, text="Rechercher", command=on_search)
search_button.pack(pady=20)

result_label = tk.Label(root, text="", font=('Arial', 12), justify='left')
result_label.pack(pady=20)

root.mainloop()
