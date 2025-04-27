import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime
import requests
from dotenv import load_dotenv
import os

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

with open('all_vehicles_data.json', 'r', encoding='utf-8') as f:
    vehicle_data = json.load(f)

def search_vehicle(vehicle_name):
    for vehicle in vehicle_data:
        if vehicle_name.lower() in vehicle['Nom véhicule'].lower():
            return vehicle['Nom véhicule'], vehicle['Prix']
    return None

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
        "footer": {
            "text": "LS MOTOR - Système de Vente"
        },
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    payload = {
        "embeds": [embed]
    }

    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        return True
    else:
        print(response.text)
        return False

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
    else:
        messagebox.showerror("Erreur", "❌ Erreur d'envoi au webhook.")

root = tk.Tk()
root.title("Vente de véhicule")

tk.Label(root, text="Nom du véhicule:").pack()
vehicule_entry = tk.Entry(root)
vehicule_entry.pack()

tk.Label(root, text="Type de vente:").pack()
type_vente_var = tk.StringVar()
type_vente_menu = ttk.Combobox(root, textvariable=type_vente_var)
type_vente_menu['values'] = ("Carte grise", "Double des clés", "Vente véhicule")
type_vente_menu.pack()

tk.Label(root, text="Quantité:").pack()
quantite_entry = tk.Entry(root)
quantite_entry.pack()

tk.Label(root, text="Date (JJ/MM/AAAA):").pack()
date_entry = tk.Entry(root)
date_entry.insert(0, datetime.datetime.now().strftime("%d/%m/%Y"))
date_entry.pack()

tk.Label(root, text="Ancien Propriétaire:").pack()
ancien_proprio_entry = tk.Entry(root)
ancien_proprio_entry.pack()

tk.Label(root, text="Nouveau Propriétaire:").pack()
nouveau_proprio_entry = tk.Entry(root)
nouveau_proprio_entry.pack()

tk.Label(root, text="Téléphone:").pack()
telephone_entry = tk.Entry(root)
telephone_entry.pack()

tk.Label(root, text="Immatriculation:").pack()
immatriculation_entry = tk.Entry(root)
immatriculation_entry.pack()

submit_button = tk.Button(root, text="Envoyer la vente", command=on_submit)
submit_button.pack(pady=10)

root.mainloop()
