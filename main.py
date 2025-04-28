import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

with open('all_vehicles_data.json', 'r', encoding='utf-8') as f:
    vehicle_data = json.load(f)

trunk_space_by_category = {
    "Boats": 1500,
    "Commercial": 1000,
    "Compact": 15,
    "Coupés": 20,
    "Moto-Vélo": 0,
    "Emergency": 500,
    "Helicopters": 1000,
    "Industrial": 2000,
    "Military": 500,
    "Moto-Vélo": 10,
    "Muscles": 25,
    "Tout Terrain": 50,
    "Open Wheel": 50,
    "Planes": 2000,
    "SUV": 75,
    "Sedans": 25,
    "Service": 2000,
    "Sportive": 20,
    "Sportive Classique": 20,
    "Super Sportive": 10,
    "Trains": 2000,
    "Utility": 2000,
    "Vans": 500
}

def search_vehicle(name=None, category=None, min_price=None, max_price=None):
    results = []
    for vehicle in vehicle_data:
        if name and name.lower() not in vehicle['Nom véhicule'].lower():
            continue
        if category and category != "Tous" and vehicle['Catégorie'].lower() != category.lower():
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

def get_vehicle_price_clean(vehicle_name):
    for vehicle in vehicle_data:
        if vehicle.get('Nom véhicule', '').upper() == vehicle_name.upper():
            prix = vehicle.get('Prix', '')
            if isinstance(prix, str):
                prix = prix.replace('$', '').replace(' ', '').strip()
            return prix
    return '0'

def send_to_webhook(data):
    embed = {
        "title": "📝 Nouvelle Vente Enregistrée",
        "color": 5814783,
        "fields": [
            {"name": "Vendeur", "value": data['vendeur'], "inline": True},
            {"name": "Grade", "value": data['grade'], "inline": True},
            {"name": "Type de Vente", "value": data['type_vente'], "inline": True},
            {"name": "Quantité", "value": data['quantite'], "inline": True},
            {"name": "Date", "value": data['date_vente'], "inline": True},
            {"name": "Nom du Véhicule", "value": data['nom_vehicule'], "inline": True},
            {"name": "Facture Employé", "value": data['prix_facture'] + " $", "inline": True},
            {"name": "Coût Usine", "value": data['cout_usine'], "inline": True},
            {"name": "Salaire Variable", "value": str(data['salaire_variable']) + " $", "inline": True},
            {"name": "Ancien Propriétaire", "value": data['ancien_proprio'], "inline": True},
            {"name": "Nouveau Propriétaire", "value": data['nouveau_proprio'], "inline": True},
            {"name": "Téléphone", "value": data['telephone'], "inline": True},
            {"name": "Immatriculation", "value": data['immatriculation'], "inline": True},
        ],
        "footer": {"text": "LS MOTOR - Système de Vente"},
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    payload = {"embeds": [embed]}
    response = requests.post(WEBHOOK_URL, json=payload)
    return response.status_code == 204

def on_submit():
    vendeur = "Yazid Brown"
    grade = "Apprenti"
    type_vente = type_vente_var.get()
    quantite = quantite_entry.get()
    date_vente = date_entry.get()
    nom_vehicule = vehicule_entry.get()
    ancien_proprio = ancien_proprio_entry.get()
    nouveau_proprio = nouveau_proprio_entry.get()
    telephone = telephone_entry.get()
    immatriculation = immatriculation_entry.get()

    try:
        quantite_int = int(quantite)
    except ValueError:
        messagebox.showerror("Erreur", "Quantité invalide.")
        return

    result = search_vehicle(nom_vehicule)
    if result:
        name, price = result[0]['Nom véhicule'], result[0]['Prix']
        cout_usine = price
        salaire_variable = int(price.replace(" ", "").replace("$", "")) // 10
    else:
        cout_usine = salaire_variable = ""

    if type_vente.lower() == "double des clés":
        prix_facture = str(500 * quantite_int)
    else:
        prix_facture = get_vehicle_price_clean(nom_vehicule)

    vente_data = {
        "vendeur": vendeur,
        "grade": grade,
        "type_vente": type_vente,
        "quantite": quantite,
        "date_vente": date_vente,
        "nom_vehicule": nom_vehicule,
        "prix_facture": prix_facture,
        "cout_usine": cout_usine,
        "salaire_variable": salaire_variable,
        "ancien_proprio": ancien_proprio,
        "nouveau_proprio": nouveau_proprio,
        "telephone": telephone,
        "immatriculation": immatriculation
    }

    if send_to_webhook(vente_data):
        messagebox.showinfo("Succès", "Vente envoyée sur Discord !")
        for entry in [vehicule_entry, quantite_entry, ancien_proprio_entry, nouveau_proprio_entry, telephone_entry, immatriculation_entry]:
            entry.delete(0, tk.END)
        type_vente_var.set("")
    else:
        messagebox.showerror("Erreur", "Erreur d'envoi au webhook.")

def on_search(event=None):
    name = name_entry.get().strip()
    category = category_combobox.get().strip()
    try:
        min_price = float(min_price_entry.get().strip()) if min_price_entry.get().strip() else None
        max_price = float(max_price_entry.get().strip()) if max_price_entry.get().strip() else None
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Veuillez entrer des prix valides.")
        return

    if not name and not category and not min_price and not max_price:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Veuillez entrer au moins un critère.")
        return

    results = search_vehicle(name, category, min_price, max_price)
    result_text.delete(1.0, tk.END)

    if results:
        for vehicle in results:
            coffre = trunk_space_by_category.get(vehicle['Catégorie'], 'Inconnu')
            result_text.insert(tk.END, f"Nom : {vehicle['Nom véhicule']}\nCatégorie : {vehicle['Catégorie']}\nPrix : {vehicle['Prix']}\nCoffre : {coffre} kg\n\n")
    else:
        result_text.insert(tk.END, "Aucun véhicule trouvé.")

root = tk.Tk()
root.title("LS MOTOR - Gestion")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

vente_frame = tk.Frame(notebook)
notebook.add(vente_frame, text="Enregistrer une Vente")

fields = [
    ("Nom du véhicule:", "vehicule_entry"),
    ("Type de vente:", "type_vente_var"),
    ("Quantité:", "quantite_entry"),
    ("Date (JJ/MM/AAAA):", "date_entry"),
    ("Ancien Propriétaire:", "ancien_proprio_entry"),
    ("Nouveau Propriétaire:", "nouveau_proprio_entry"),
    ("Téléphone:", "telephone_entry"),
    ("Immatriculation:", "immatriculation_entry")
]

widgets = {}
for label_text, var_name in fields:
    tk.Label(vente_frame, text=label_text).pack()
    if "type_vente" in var_name:
        type_vente_var = tk.StringVar()
        type_vente_menu = ttk.Combobox(vente_frame, textvariable=type_vente_var)
        type_vente_menu['values'] = ("Carte grise", "Double des clés", "Vente véhicule")
        type_vente_menu.pack()
        widgets[var_name] = type_vente_menu
    else:
        entry = tk.Entry(vente_frame)
        if "date" in var_name:
            entry.insert(0, datetime.datetime.now().strftime("%d/%m/%Y"))
        entry.pack()
        widgets[var_name] = entry

vehicule_entry = widgets['vehicule_entry']
quantite_entry = widgets['quantite_entry']
date_entry = widgets['date_entry']
ancien_proprio_entry = widgets['ancien_proprio_entry']
nouveau_proprio_entry = widgets['nouveau_proprio_entry']
telephone_entry = widgets['telephone_entry']
immatriculation_entry = widgets['immatriculation_entry']

type_vente_var = type_vente_var

tk.Button(vente_frame, text="Envoyer la vente", command=on_submit).pack(pady=10)
vente_frame.bind_all("<Return>", lambda event: on_submit())

recherche_frame = tk.Frame(notebook)
notebook.add(recherche_frame, text="Rechercher un Véhicule")

name_entry = tk.Entry(recherche_frame, width=30)
category_combobox = ttk.Combobox(recherche_frame, width=30)
min_price_entry = tk.Entry(recherche_frame, width=30)
max_price_entry = tk.Entry(recherche_frame, width=30)

categories = sorted(set(v['Catégorie'] for v in vehicle_data))
categories = ["Tous"] + categories
category_combobox['values'] = categories

for widget, label in zip([name_entry, category_combobox, min_price_entry, max_price_entry],
                         ["Nom du véhicule:", "Catégorie:", "Prix minimum:", "Prix maximum:"]):
    tk.Label(recherche_frame, text=label).pack()
    widget.pack(pady=5)

tk.Button(recherche_frame, text="Rechercher", command=on_search).pack(pady=10)

result_frame = tk.Frame(recherche_frame)
result_frame.pack(pady=10)

result_text = tk.Text(result_frame, width=60, height=15, wrap=tk.WORD)
scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
result_text.config(yscrollcommand=scrollbar.set)
result_text.pack(side=tk.LEFT)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

name_entry.bind("<Return>", on_search)

root.mainloop()