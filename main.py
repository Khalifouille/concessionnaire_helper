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

def search_vehicle_simple(vehicle_name):
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

    payload = {"embeds": [embed]}
    response = requests.post(WEBHOOK_URL, json=payload)
    return response.status_code == 204

def open_sale_window():
    sale_window = tk.Toplevel(root)
    sale_window.title("Vente de véhicule")

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

        result = search_vehicle_simple(nom_vehicule)

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

    tk.Label(sale_window, text="Nom du véhicule:").pack()
    vehicule_entry = tk.Entry(sale_window)
    vehicule_entry.pack()

    tk.Label(sale_window, text="Type de vente:").pack()
    type_vente_var = tk.StringVar()
    type_vente_menu = ttk.Combobox(sale_window, textvariable=type_vente_var)
    type_vente_menu['values'] = ("Carte grise", "Double des clés", "Vente véhicule")
    type_vente_menu.pack()

    tk.Label(sale_window, text="Quantité:").pack()
    quantite_entry = tk.Entry(sale_window)
    quantite_entry.pack()

    tk.Label(sale_window, text="Date (JJ/MM/AAAA):").pack()
    date_entry = tk.Entry(sale_window)
    date_entry.insert(0, datetime.datetime.now().strftime("%d/%m/%Y"))
    date_entry.pack()

    tk.Label(sale_window, text="Ancien Propriétaire:").pack()
    ancien_proprio_entry = tk.Entry(sale_window)
    ancien_proprio_entry.pack()

    tk.Label(sale_window, text="Nouveau Propriétaire:").pack()
    nouveau_proprio_entry = tk.Entry(sale_window)
    nouveau_proprio_entry.pack()

    tk.Label(sale_window, text="Téléphone:").pack()
    telephone_entry = tk.Entry(sale_window)
    telephone_entry.pack()

    tk.Label(sale_window, text="Immatriculation:").pack()
    immatriculation_entry = tk.Entry(sale_window)
    immatriculation_entry.pack()

    submit_button = tk.Button(sale_window, text="Envoyer la vente", command=on_submit)
    submit_button.pack(pady=10)

    sale_window.bind("<Return>", lambda event: on_submit())

def open_search_window():
    search_window = tk.Toplevel(root)
    search_window.title("Recherche de Véhicule")

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
            result_text.insert(tk.END, "\n\n".join([f"Nom : {vehicle['Nom véhicule']}\nCatégorie : {vehicle['Catégorie']}\nPrix : {vehicle['Prix']}" for vehicle in results]))
        else:
            result_text.insert(tk.END, "Aucun véhicule trouvé.")

    tk.Label(search_window, text="Nom du véhicule :").pack(pady=10)
    name_entry = tk.Entry(search_window, width=30)
    name_entry.pack(pady=10)

    tk.Label(search_window, text="Catégorie de véhicule :").pack(pady=10)
    categories = sorted(set(vehicle['Catégorie'] for vehicle in vehicle_data))
    categories = ["Tous"] + categories
    category_combobox = ttk.Combobox(search_window, values=categories, width=30)
    category_combobox.pack(pady=10)

    tk.Label(search_window, text="Prix minimum :").pack(pady=10)
    min_price_entry = tk.Entry(search_window, width=30)
    min_price_entry.pack(pady=10)

    tk.Label(search_window, text="Prix maximum :").pack(pady=10)
    max_price_entry = tk.Entry(search_window, width=30)
    max_price_entry.pack(pady=10)

    search_button = tk.Button(search_window, text="Rechercher", command=on_search)
    search_button.pack(pady=20)

    result_frame = tk.Frame(search_window)
    result_frame.pack(pady=20)

    result_text = tk.Text(result_frame, width=50, height=10, wrap=tk.WORD)
    result_text.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    result_text.config(yscrollcommand=scrollbar.set)

    name_entry.bind("<Return>", on_search)

root = tk.Tk()
root.title("LS Motor - Système Central")

tk.Label(root, text="Bienvenue dans LS Motor", font=("Arial", 16)).pack(pady=20)

tk.Button(root, text="Nouvelle Vente", width=30, height=2, command=open_sale_window).pack(pady=10)
tk.Button(root, text="Recherche Véhicule", width=30, height=2, command=open_search_window).pack(pady=10)

root.mainloop()
