import os
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

INPUT_JSON = "nom_vehicules_occupants.json"
OUTPUT_DIR = "vehicle_images"
DELAY = 1

def load_vehicle_names(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            unique_vehicles = {v["DisplayName"]: v for v in data}.values()
            return [vehicle["DisplayName"] for vehicle in unique_vehicles]
    except Exception as e:
        print(f"❌ Erreur lecture JSON : {str(e)}")
        return []

def get_wiki_image_url(vehicle_name):
    try:
        wiki_name = vehicle_name.replace(' ', '_').split('(')[0].strip()
        url = f"https://gta.fandom.com/wiki/{wiki_name}"
        print(f"\n🔍 Recherche sur Wiki pour : {vehicle_name}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'fr-FR,fr;q=0.9'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        infobox_img = soup.find('figure', {'data-source': 'image'})
        if infobox_img:
            img_tag = infobox_img.find('img')
            if img_tag and 'src' in img_tag.attrs:
                img_url = img_tag['src']
                if not img_url.startswith('http'):
                    img_url = 'https:' + img_url
                return img_url

        meta_og = soup.find('meta', property='og:image')
        if meta_og and 'content' in meta_og.attrs:
            return meta_og['content']

        return None

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"⚠️ Page wiki non trouvée pour {vehicle_name}")
        else:
            print(f"⚠️ Erreur HTTP : {e.response.status_code}")
        return None
    except Exception as e:
        print(f"⚠️ Erreur lors de la recherche : {str(e)}")
        return None

def download_image(image_url, save_path):
    try:
        if not image_url:
            return False

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
        elif not image_url.startswith('http'):
            image_url = 'https://' + image_url

        response = requests.get(image_url, headers=headers, stream=True, timeout=15)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '')
        if 'image' not in content_type:
            print(f"❌ Le contenu n'est pas une image (Type: {content_type})")
            return False

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
                
        print(f"✅ Image sauvegardée : {save_path}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de téléchargement : {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue : {str(e)}")
        return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Initialisation du scraper...")

    vehicle_names = load_vehicle_names(INPUT_JSON)
    if not vehicle_names:
        print("Aucun véhicule trouvé dans le fichier JSON.")
        return

    print(f"\n🚗 {len(vehicle_names)} véhicules uniques à traiter")
    
    for i, vehicle_name in enumerate(vehicle_names, 1):
        print(f"\n[{i}/{len(vehicle_names)}] Traitement : {vehicle_name}")
        
        filename = (vehicle_name.replace(" ", "_")
                   .replace("(", "").replace(")", "")
                   .replace("/", "_") + ".png")
        save_path = os.path.join(OUTPUT_DIR, filename)
        
        if os.path.exists(save_path):
            print("ℹ️ Fichier existe déjà - Skip")
            continue
            
        image_url = get_wiki_image_url(vehicle_name)
        
        if image_url:
            print(f"🖼️ URL trouvée : {image_url[:100]}...")
            
            if not download_image(image_url, save_path):
                save_path = save_path.replace('.jpg', '.png')
                download_image(image_url, save_path)
        else:
            print("❌ Aucune image trouvée")
            
        if i < len(vehicle_names) and DELAY > 0:
            time.sleep(DELAY)

    print("\n✅ Traitement terminé !")

if __name__ == "__main__":
    main()