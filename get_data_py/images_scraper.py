import json
import requests
from bs4 import BeautifulSoup
import os
import re
from time import sleep

INPUT_JSON = "nom_vehicules_occupants.json"
OUTPUT_DIR = "vehicle_images"
DELAY = 1

def setup_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_vehicle_names():
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [v["DisplayName"] for v in data]

def get_image_url(vehicle_name):
    try:
        url = f"https://gta.fandom.com/wiki/{vehicle_name.replace(' ', '_')}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        figure = soup.find('figure', {'data-source': 'front_image'}) or \
                 soup.find('figure', class_='pi-item pi-image')

        if figure:
            img_tag = figure.find('img')
            if img_tag and img_tag.has_attr('srcset'):
                srcset = img_tag['srcset'].split(', ')
                high_res_url = srcset[-1].split(' ')[0]
                return high_res_url
            elif img_tag and img_tag.has_attr('src'):
                return img_tag['src']
    except Exception as e:
        print(f"Erreur pour {vehicle_name}: {str(e)}")
    return None


def sanitize_filename(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9]', '_', name) 
    name = re.sub(r'_+', '_', name)
    return name.strip('_')

def download_image(url, vehicle_name):
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            filename = f"{OUTPUT_DIR}/{sanitize_filename(vehicle_name)}.png"
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filename
    except Exception as e:
        print(f"Échec du téléchargement pour {vehicle_name}: {str(e)}")
    return None

def main():
    setup_dirs()
    vehicle_names = load_vehicle_names()
    
    print(f"⏳ Début du scraping pour {len(vehicle_names)} véhicules...")
    
    success_count = 0
    for i, name in enumerate(vehicle_names, 1):
        print(f"\n🔍 Traitement [{i}/{len(vehicle_names)}]: {name}")
        
        img_url = get_image_url(name)
        if not img_url:
            print(f"❌ Image non trouvée pour {name}")
            continue
        
        result = download_image(img_url, name)
        if result:
            print(f"✅ Sauvegardé: {result}")
            success_count += 1
        
        sleep(DELAY)
    
    print(f"\n🎉 Terminé! {success_count}/{len(vehicle_names)} images téléchargées")

if __name__ == "__main__":
    main()