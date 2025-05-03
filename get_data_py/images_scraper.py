import os
import json
import time
import requests
from bs4 import BeautifulSoup

INPUT_JSON = "nom_vehicules_occupants.json"
OUTPUT_DIR = "vehicle_images"
DELAY = 1 

def load_vehicle_names(json_file):
    """Charge les noms des véhicules depuis un fichier JSON"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [vehicle["Nom véhicule"] for vehicle in data]
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier JSON : {str(e)}")
        return []

def get_image_url(vehicle_name):
    try:
        url = f"https://gta.fandom.com/wiki/{vehicle_name.replace(' ', '_')}"
        print(f"\n🔍 Recherche image pour : {vehicle_name}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        figure = soup.find('figure', class_='pi-item pi-image', attrs={'data-source': 'front_image'})
        if figure:
            a_tag = figure.find('a', href=True, class_='image image-thumbnail')
            if a_tag:
                image_url = a_tag['href']
                print(f"✅ Image trouvée : {image_url}")
                return image_url
            else:
                print("❌ Lien <a> image non trouvé dans la figure.")
        else:
            print("❌ Figure front_image non trouvée.")
    except Exception as e:
        print(f"⚠️ Erreur lors de la récupération pour {vehicle_name} : {str(e)}")
    return None

def download_image(image_url, save_path):
    try:
        response = requests.get(image_url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"📥 Image enregistrée : {save_path}")
    except Exception as e:
        print(f"❌ Erreur téléchargement de l'image : {str(e)}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        vehicles_data = json.load(f)
    
    vehicle_names = [vehicle["Nom véhicule"] for vehicle in vehicles_data]
    
    if not vehicle_names:
        print("Aucun nom de véhicule trouvé. Vérifiez le fichier JSON.")
        return

    print(f"🚗 {len(vehicle_names)} véhicules à traiter...")

    for vehicle_name in vehicle_names:
        image_url = get_image_url(vehicle_name)
        if image_url:
            filename = (vehicle_name.replace(" ", "_")
                        .replace("(", "").replace(")", "")
                        .replace("/", "_") + ".png")
            save_path = os.path.join(OUTPUT_DIR, filename)
            download_image(image_url, save_path)
        
        if DELAY > 0:
            time.sleep(DELAY)

if __name__ == "__main__":
    main()