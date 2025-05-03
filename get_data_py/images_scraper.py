import os
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

INPUT_JSON = "nom_vehicules_occupants.json"
OUTPUT_DIR = "vehicle_images"
DELAY = 3 
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def google_image_search(query):
    try:
        search_url = f"https://www.google.com/search?tbm=isch&q={quote_plus(query)}"
        headers = {'User-Agent': USER_AGENT}
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('img')
        
        for img in images:
            if 'data-src' in img.attrs:
                img_url = img['data-src']
                if img_url.startswith('http') and img_url.count('gstatic.com') == 0:
                    return img_url
        
        return None
    except Exception as e:
        print(f"⚠️ Erreur recherche Google : {str(e)}")
        return None

def download_image(image_url, save_path):
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(image_url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"❌ Erreur téléchargement : {str(e)}")
        return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    vehicle_name = "Banshee GTA"
    print(f"\n🔍 Recherche Google Images pour : {vehicle_name}")
    
    image_url = google_image_search(vehicle_name)
    
    if image_url:
        print(f"✅ Résultat : {image_url}")
        filename = "Banshee.jpg"
        save_path = os.path.join(OUTPUT_DIR, filename)
        
        if download_image(image_url, save_path):
            print(f"📥 Image sauvegardée : {save_path}")
        else:
            print("❌ Échec du téléchargement")
    else:
        print("❌ Aucune image trouvée")

if __name__ == "__main__":
    main()