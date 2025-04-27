import requests
from bs4 import BeautifulSoup
import json

def get_vehicle_data(url, category_name):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    vehicle_data = []
    vehicles = soup.find_all('p', class_='zfr3Q CDt4Ke')

    for vehicle in vehicles:
        name_tag = vehicle.find('span', class_='C9DxTc')
        if name_tag:
            name = name_tag.text.strip()
        else:
            continue

        price_tag = vehicle.find('span', style="color: #000000;")
        if price_tag:
            price = price_tag.text.strip()
        else:
            price = "Non disponible"
        
        vehicle_data.append({
            'Catégorie': category_name,
            'Nom véhicule': name,
            'Prix': price
        })

    return vehicle_data

categories = [
    ('Compact', 'https://sites.google.com/view/lsmotornoface/cat%C3%A9gorie/compact?authuser=0'),
    ('Coupés', 'https://sites.google.com/view/lsmotornoface/cat%C3%A9gorie/coup%C3%A9s?authuser=0'),
    ('Sedans', 'https://sites.google.com/view/lsmotornoface/cat%C3%A9gorie/sedans?authuser=0'),
    ('Sportive', 'https://sites.google.com/view/lsmotornoface/cat%C3%A9gorie/sportive?authuser=0'),
    ('Super Sportive', 'https://sites.google.com/view/lsmotornoface/cat%C3%A9gorie/super-sportive?authuser=0'),
    ('SUV', 'https://sites.google.com/view/lsmotornoface/cat%C3%A9gorie/suv?authuser=0'),
    ('Muscles', 'https://sites.google.com/view/lsmotornoface/cat%C3%A9gorie/muscles?authuser=0'),
    ('Sportive Classique', 'https://sites.google.com/view/lsmotornoface/cat%C3%A9gorie/sportive-classique?authuser=0'),
    ('Tout Terrain', 'https://sites.google.com/view/lsmotornoface/cat%C3%A9gorie/tout-terrain?authuser=0'),
    ('Moto-Vélo', 'https://sites.google.com/view/lsmotornoface/cat%C3%A9gorie/moto-v%C3%A9lo?authuser=0'),
    ('Vans', 'https://sites.google.com/view/lsmotornoface/cat%C3%A9gorie/vans?authuser=0')
]

all_vehicle_data = []

for category_name, url in categories:
    print(f"Récupération des données de la catégorie '{category_name}'...")
    vehicle_data = get_vehicle_data(url, category_name)
    all_vehicle_data.extend(vehicle_data)

with open('all_vehicles_data2.json', 'w', encoding='utf-8') as f:
    json.dump(all_vehicle_data, f, ensure_ascii=False, indent=4)

print("Les données de toutes les catégories ont été enregistrées dans 'all_vehicles_data.json'.")
