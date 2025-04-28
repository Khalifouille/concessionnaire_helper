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

def open_vente_page():
    vente_page = tk.Toplevel(root)
    vente_page.title("Vente de Véhicule")

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
            messagebox.showerror("Erreur", "❌ Quantité invalide.")
            return

        result = search_vehicle(nom_vehicule)

        if result:
            name, price = result
            cout_usine = price
            try:
                salaire_variable = int(price.replace(" ", "").replace("$", "")) // 10
            except:
                salaire_variable = ""
        else:
            cout_usine = ""
            salaire_variable = ""

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

    tk.Label(vente_page, text="Nom du véhicule:").pack()
    vehicule_entry = tk.Entry(vente_page)
    vehicule_entry.pack()

    tk.Label(vente_page, text="Type de vente:").pack()
    type_vente_var = tk.StringVar()
    type_vente_menu = ttk.Combobox(vente_page, textvariable=type_vente_var)
    type_vente_menu['values'] = ("Carte grise", "Double des clés", "Vente véhicule")
    type_vente_menu.pack()

    tk.Label(vente_page, text="Quantité:").pack()
    quantite_entry = tk.Entry(vente_page)
    quantite_entry.pack()

    tk.Label(vente_page, text="Date (JJ/MM/AAAA):").pack()
    date_entry = tk.Entry(vente_page)
    date_entry.insert(0, datetime.datetime.now().strftime("%d/%m/%Y"))
    date_entry.pack()

    tk.Label(vente_page, text="Ancien Propriétaire:").pack()
    ancien_proprio_entry = tk.Entry(vente_page)
    ancien_proprio_entry.pack()

    tk.Label(vente_page, text="Nouveau Propriétaire:").pack()
    nouveau_proprio_entry = tk.Entry(vente_page)
    nouveau_proprio_entry.pack()

    tk.Label(vente_page, text="Téléphone:").pack()
    telephone_entry = tk.Entry(vente_page)
    telephone_entry.pack()

    tk.Label(vente_page, text="Immatriculation:").pack()
    immatriculation_entry = tk.Entry(vente_page)
    immatriculation_entry.pack()

    submit_button = tk.Button(vente_page, text="Envoyer la vente", command=on_submit)
    submit_button.pack(pady=10)

    vente_page.bind("<Return>", lambda event: on_submit())

def open_recherche_page():
    recherche_page = tk.Toplevel(root)
    recherche_page.title("Recherche de Véhicule")

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

            results.append(vehicle)

        result_text.delete(1.0, tk.END)
        if results:
            for v in results:
                coffre = trunk_spaces.get(v['Catégorie'], "Inconnu")
                result_text.insert(tk.END, f"Nom : {v['Nom véhicule']}\nCatégorie : {v['Catégorie']} (Coffre: {coffre} kg)\nPrix : {v['Prix']}\n\n")
        else:
            result_text.insert(tk.END, "Aucun véhicule trouvé.")

    tk.Label(recherche_page, text="Nom du véhicule :").pack(pady=5)
    name_entry = tk.Entry(recherche_page, width=30)
    name_entry.pack(pady=5)

    tk.Label(recherche_page, text="Catégorie de véhicule :").pack(pady=5)
    categories = sorted(set(vehicle['Catégorie'] for vehicle in vehicle_data))
    categories = ["Tous"] + categories
    category_combobox = ttk.Combobox(recherche_page, values=categories, width=30)
    category_combobox.pack(pady=5)

    tk.Label(recherche_page, text="Prix minimum :").pack(pady=5)
    min_price_entry = tk.Entry(recherche_page, width=30)
    min_price_entry.pack(pady=5)

    tk.Label(recherche_page, text="Prix maximum :").pack(pady=5)
    max_price_entry = tk.Entry(recherche_page, width=30)
    max_price_entry.pack(pady=5)

    search_button = tk.Button(recherche_page, text="Rechercher", command=on_search)
    search_button.pack(pady=10)

    result_text = tk.Text(recherche_page, width=50, height=15)
    result_text.pack(pady=10)

    recherche_page.bind("<Return>", on_search)

root = tk.Tk()
root.title("Menu Principal")

tk.Label(root, text="Bienvenue ! Choisissez une option :").pack(pady=20)

tk.Button(root, text="Enregistrer une Vente", command=open_vente_page, width=30).pack(pady=10)
tk.Button(root, text="Rechercher un Véhicule", command=open_recherche_page, width=30).pack(pady=10)

root.mainloop()