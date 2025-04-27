import tkinter as tk
from tkinter import ttk
import json
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

with open('all_vehicles_data.json', 'r', encoding='utf-8') as f:
    vehicle_data = json.load(f)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('api_key.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Copie de Staff LS MOTOR").worksheet("Ventes")

def search_vehicle(vehicle_name):
    for vehicle in vehicle_data:
        if vehicle_name.lower() in vehicle['Nom véhicule'].lower():
            return vehicle['Nom véhicule'], vehicle['Prix']
    return None

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

    row = [
        vendeur,            # A
        grade,              # B
        type_vente,         # C
        quantite,           # D
        date_vente,         # E
        nom_vehicule,       # F
        "",                 # G
        cout_usine,         # H
        salaire_variable,   # I
        ancien_proprio,     # J
        nouveau_proprio,    # K
        telephone,          # L
        immatriculation     # M
    ]

    while len(row) < 19:
        row.append("")

    try:
        sheet.append_row(row, table_range="A:S")
        result_label.config(text="✅ Vente enregistrée !")
    except Exception as e:
        result_label.config(text=f"❌ Erreur: {str(e)}")

root = tk.Tk()
root.title("Vente de véhicule")

tk.Label(root, text="Nom du véhicule:").pack()
vehicule_entry = tk.Entry(root)
vehicule_entry.pack()

tk.Label(root, text="Type de vente:").pack()
type_vente_var = tk.StringVar()
type_vente_menu = ttk.Combobox(root, textvariable=type_vente_var)
type_vente_menu['values'] = ("Carte Grise", "Double des clés", "Vente véhicule")
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

submit_button = tk.Button(root, text="Enregistrer la vente", command=on_submit)
submit_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
