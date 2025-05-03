import os
import json
import time
import requests
from bs4 import BeautifulSoup

INPUT_JSON = "nom_vehicules_occupants.json"
OUTPUT_DIR = "vehicle_images"
DELAY = 1 

def load_vehicle_names(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [vehicle["DisplayName"] for vehicle in data]
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier JSON : {str(e)}")
        return []

def get_image_url(vehicle_name):
    try:
        wiki_name = vehicle_name.replace(' ', '_').split('(')[0].strip()
        url = f"https://gta.fandom.com/wiki/{wiki_name}"
        print(f"\n🔍 Recherche image pour : {vehicle_name} (URL: {url})")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        image_sources = [
            ('figure', {'class': 'pi-item pi-image', 'data-source': 'front_image'}),
            ('figure', {'class': 'pi-item pi-image'}),
            ('img', {'class': 'thumbimage'})
        ]

        for tag, attrs in image_sources:
            element = soup.find(tag, attrs=attrs)
            if element:
                img_tag = element.find('img') if tag == 'figure' else element
                if img_tag and 'src' in img_tag.attrs:
                    image_url = img_tag['src']
                    if not image_url.startswith('http'):
                        image_url = 'https:' + image_url
                    print(f"✅ Image trouvée : {image_url}")
                    return image_url

        print("❌ Aucune image trouvée avec les méthodes standards")
        return None

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"⚠️ Page wiki non trouvée pour {vehicle_name}")
        else:
            print(f"⚠️ Erreur HTTP pour {vehicle_name} : {str(e)}")
    except Exception as e:
        print(f"⚠️ Erreur inattendue pour {vehicle_name} : {str(e)}")
    return None

def download_image(image_url, save_path):
    try:
        if not image_url:
            return False

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(image_url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()
        
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type:
            print(f"❌ Le fichier téléchargé n'est pas une image (Content-Type: {content_type})")
            return False

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"📥 Image enregistrée : {save_path}")
        return True
    except Exception as e:
        print(f"❌ Erreur téléchargement de l'image : {str(e)}")
        return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        with open(INPUT_JSON, 'r', encoding='utf-8') as f:
            vehicles_data = json.load(f)
            vehicle_names = [vehicle["DisplayName"] for vehicle in vehicles_data]
    except Exception as e:
        print(f"❌ Erreur de lecture du fichier JSON : {str(e)}")
        return

    if not vehicle_names:
        print("❌ Aucun nom de véhicule trouvé. Vérifiez la structure du fichier JSON.")
        return

    print(f"🚗 {len(vehicle_names)} véhicules à traiter...")
    print(f"Exemples : {vehicle_names[:3]}...")

    for i, vehicle_name in enumerate(vehicle_names, 1):
        print(f"\n[{i}/{len(vehicle_names)}] Traitement de : {vehicle_name}")
        
        image_url = get_image_url(vehicle_name)
        if image_url:
            filename = (vehicle_name.replace(" ", "_")
                       .replace("(", "").replace(")", "")
                       .replace("/", "_")
                       .replace("'", "")
                       .replace('"', "")
                       .replace("®", "")
                       .replace("™", "") + ".png")
            
            save_path = os.path.join(OUTPUT_DIR, filename)
            
            if os.path.exists(save_path):
                print(f"ℹ️ L'image existe déjà, on passe au suivant")
                continue
                
            if not download_image(image_url, save_path):
                save_path = save_path.replace(".jpg", ".png")
                download_image(image_url, save_path)
        
        if DELAY > 0 and i < len(vehicle_names):
            time.sleep(DELAY)

if __name__ == "__main__":
    main()