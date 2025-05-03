import os
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import random

INPUT_JSON = "nom_vehicules_occupants.json"
OUTPUT_DIR = "vehicle_images"
DELAY = 5  
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
]

def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/'
    }

def google_image_search(query):
    try:
        search_url = f"https://www.google.com/search?tbm=isch&q={quote_plus(query)}"
        
        response = requests.get(search_url, 
                             headers=get_random_headers(),
                             timeout=15,
                             cookies={'CONSENT': 'YES+'})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script')
        
        for script in script_tags:
            if 'AF_initDataCallback' in script.text:
                import re
                matches = re.findall(r'\"(https?:\/\/[^"]+\.(?:jpg|jpeg|png))\"', script.text)
                if matches:
                    return matches[0]  

        return None
        
    except Exception as e:
        print(f"⚠️ Erreur recherche Google : {str(e)}")
        return None

def download_with_retry(image_url, save_path, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(image_url,
                                 headers=get_random_headers(),
                                 stream=True,
                                 timeout=10)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
            
        except Exception as e:
            if attempt == retries - 1:
                print(f"❌ Échec après {retries} tentatives : {str(e)}")
                return False
            time.sleep(2)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    queries = [
        "Banshee GTA 5",
        "Banshee Grand Theft Auto",
        "Banshee GTA V screenshot",
        "Banshee GTA Online"
    ]
    
    for query in queries:
        print(f"\n🔍 Tentative avec : '{query}'")
        image_url = google_image_search(query)
        
        if image_url:
            print(f"✅ URL trouvée : {image_url}")
            filename = f"Banshee_{query.split(' ')[-1]}.jpg"
            save_path = os.path.join(OUTPUT_DIR, filename)
            
            if download_with_retry(image_url, save_path):
                print(f"📥 Sauvegarde réussie : {filename}")
                break
        else:
            print("❌ Aucun résultat")
        
        time.sleep(DELAY)

if __name__ == "__main__":
    main()