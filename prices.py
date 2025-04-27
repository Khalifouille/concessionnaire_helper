import tkinter as tk
import json

with open('all_vehicles_data.json', 'r', encoding='utf-8') as f:
    vehicle_data = json.load(f)

def search_vehicle(name=None, category=None, min_price=None, max_price=None):
    results = []
    for vehicle in vehicle_data:
        if name and name.lower() not in vehicle['Nom véhicule'].lower():
            continue
        
        if category and vehicle['Catégorie'].lower() != category.lower():
            continue
        
        try:
            price = float(vehicle['Prix'].replace('$', '').replace(' ', '').strip())
        except ValueError:
            price = 0 

        if min_price and price < min_price:
            continue
        if max_price and price > max_price:
            continue

        results.append(vehicle)
    return results

def on_search(event=None): 
    name = name_entry.get().strip()
    category = category_entry.get().strip()

    try:
        min_price = float(min_price_entry.get().strip()) if min_price_entry.get().strip() else None
        max_price = float(max_price_entry.get().strip()) if max_price_entry.get().strip() else None
    except ValueError:
        result_text.delete(1.0, tk.END) 
        result_text.insert(tk.END, "Veuillez entrer des prix valides.")
        return

    if not name and not category and not min_price and not max_price:
        result_text.delete(1.0, tk.END) 
        result_text.insert(tk.END, "Veuillez entrer au moins un critère de recherche.")
        return

    results = search_vehicle(name, category, min_price, max_price)
    
    result_text.delete(1.0, tk.END) 
    
    if results:
        result_text.insert(tk.END, "\n\n".join([f"Nom : {vehicle['Nom véhicule']}\nCatégorie : {vehicle['Catégorie']}\nPrix : {vehicle['Prix']}\n" for vehicle in results]))
    else:
        result_text.insert(tk.END, "Aucun véhicule trouvé.")

root = tk.Tk()
root.title("Recherche de Véhicule")

tk.Label(root, text="Nom du véhicule :").pack(pady=10)
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=10)

tk.Label(root, text="Catégorie de véhicule :").pack(pady=10)
category_entry = tk.Entry(root, width=30)
category_entry.pack(pady=10)

tk.Label(root, text="Prix minimum :").pack(pady=10)
min_price_entry = tk.Entry(root, width=30)
min_price_entry.pack(pady=10)

tk.Label(root, text="Prix maximum :").pack(pady=10)
max_price_entry = tk.Entry(root, width=30)
max_price_entry.pack(pady=10)

search_button = tk.Button(root, text="Rechercher", command=on_search)
search_button.pack(pady=20)

result_frame = tk.Frame(root)
result_frame.pack(pady=20)

result_text = tk.Text(result_frame, width=50, height=10, wrap=tk.WORD)
result_text.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
