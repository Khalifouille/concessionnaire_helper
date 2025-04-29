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

trunk_spaces = {
    "Boats": 1500,
    "Commercial": 1000,
    "Compact": 15,
    "Coupés": 20,
    "Moto-Vélo": 10,
    "Emergency": 500,
    "Helicopters": 1000,
    "Industrial": 2000,
    "Military": 500,
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

def search_vehicle(name):
    for vehicle in vehicle_data:
        if name.lower() in vehicle['Nom véhicule'].lower():
            return vehicle['Nom véhicule'], vehicle['Prix']
    return None

def get_vehicle_price_clean(name):
    for vehicle in vehicle_data:
        if vehicle.get('Nom véhicule', '').upper() == name.upper():
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

def submit_vente():
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
        messagebox.showerror("Erreur", "❌ Quantité invalide.")
        return

    result = search_vehicle(nom_vehicule)

    if result:
        name, price = result
    else:
        price = '0'

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
        "ancien_proprio": ancien_proprio,
        "nouveau_proprio": nouveau_proprio,
        "telephone": telephone,
        "immatriculation": immatriculation
    }

    success = send_to_webhook(vente_data)

    if success:
        messagebox.showinfo("Succès", "✅ Vente envoyée sur Discord !")
        vehicule_entry.delete(0, tk.END)
        type_vente_var.set("")
        quantite_entry.delete(0, tk.END)
        ancien_proprio_entry.delete(0, tk.END)
        nouveau_proprio_entry.delete(0, tk.END)
        telephone_entry.delete(0, tk.END)
        immatriculation_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Erreur", "❌ Erreur d'envoi au webhook.")

def search_vehicle_tab():
    name = name_entry.get().strip()
    category = category_combobox.get().strip()
    trunk_min = trunk_filter_var.get().strip()
    trunk_min = int(trunk_min) if trunk_min and trunk_min != "Tous" else None

    try:
        min_price = float(min_price_entry.get().strip()) if min_price_entry.get().strip() else None
        max_price = float(max_price_entry.get().strip()) if max_price_entry.get().strip() else None
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Veuillez entrer des prix valides.")
        return

    if not name and not category and not min_price and not max_price and not trunk_min:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Veuillez entrer au moins un critère de recherche.")
        return

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

        coffre = trunk_spaces.get(vehicle['Catégorie'], 0)
        if trunk_min is not None and coffre < trunk_min:
            continue

        results.append(vehicle)

    result_text.delete(1.0, tk.END)
    if results:
        for v in results:
            coffre = trunk_spaces.get(v['Catégorie'], "Inconnu")
            result_text.insert(tk.END, f"Nom : {v['Nom véhicule']}\nCatégorie : {v['Catégorie']} (Coffre: {coffre} kg)\nPrix : {v['Prix']}\n\n")
    else:
        result_text.insert(tk.END, "Aucun véhicule trouvé.")

root = tk.Tk()
root.title("Vente & Recherche Véhicules")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

vente_frame = ttk.Frame(notebook)
notebook.add(vente_frame, text="Vente de Véhicule")

recherche_frame = ttk.Frame(notebook)
notebook.add(recherche_frame, text="Recherche de Véhicule")

tk.Label(vente_frame, text="Nom du véhicule:").pack()
vehicule_entry = tk.Entry(vente_frame)
vehicule_entry.pack()

tk.Label(vente_frame, text="Type de vente:").pack()
type_vente_var = tk.StringVar()
type_vente_menu = ttk.Combobox(vente_frame, textvariable=type_vente_var)
type_vente_menu['values'] = ("Carte grise", "Double des clés", "Vente véhicule")
type_vente_menu.pack()

tk.Label(vente_frame, text="Quantité:").pack()
quantite_entry = tk.Entry(vente_frame)
quantite_entry.pack()

tk.Label(vente_frame, text="Date (JJ/MM/AAAA):").pack()
date_entry = tk.Entry(vente_frame)
date_entry.insert(0, datetime.datetime.now().strftime("%d/%m/%Y"))
date_entry.pack()

tk.Label(vente_frame, text="Ancien Propriétaire:").pack()
ancien_proprio_entry = tk.Entry(vente_frame)
ancien_proprio_entry.pack()

tk.Label(vente_frame, text="Nouveau Propriétaire:").pack()
nouveau_proprio_entry = tk.Entry(vente_frame)
nouveau_proprio_entry.pack()

tk.Label(vente_frame, text="Téléphone:").pack()
telephone_entry = tk.Entry(vente_frame)
telephone_entry.pack()

tk.Label(vente_frame, text="Immatriculation:").pack()
immatriculation_entry = tk.Entry(vente_frame)
immatriculation_entry.pack()

submit_button = tk.Button(vente_frame, text="Envoyer Vente", command=submit_vente)
submit_button.pack(pady=10)

tk.Label(recherche_frame, text="Nom du véhicule:").pack()
name_entry = tk.Entry(recherche_frame)
name_entry.pack()

tk.Label(recherche_frame, text="Catégorie:").pack()
categories = sorted(set(vehicle['Catégorie'] for vehicle in vehicle_data))
categories = ["Tous"] + categories
category_combobox = ttk.Combobox(recherche_frame, values=categories)
category_combobox.pack()

tk.Label(recherche_frame, text="Prix minimum:").pack()
min_price_entry = tk.Entry(recherche_frame)
min_price_entry.pack()

tk.Label(recherche_frame, text="Prix maximum:").pack()
max_price_entry = tk.Entry(recherche_frame)
max_price_entry.pack()

tk.Label(recherche_frame, text="Taille minimum du coffre (kg) :").pack()
trunk_filter_var = tk.StringVar()
trunk_filter_menu = ttk.Combobox(recherche_frame, textvariable=trunk_filter_var)
trunk_filter_menu['values'] = ("Tous", "0", "10", "20", "25", "50", "75", "500", "1000", "1500", "2000")
trunk_filter_menu.pack()

search_button = tk.Button(recherche_frame, text="Rechercher", command=search_vehicle_tab)
search_button.pack(pady=10)

result_text = tk.Text(recherche_frame, width=50, height=15)
result_text.pack()

def on_enter(event=None):
    current_tab = notebook.index(notebook.select())
    if current_tab == 0:
        submit_vente()
    elif current_tab == 1:
        search_vehicle_tab()

root.bind("<Return>", on_enter)

root.mainloop()