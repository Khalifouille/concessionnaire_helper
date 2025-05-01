import requests
from bs4 import BeautifulSoup
import re
import os

def download_vehicle_images(vehicle_name, save_dir="vehicle_images"):
    os.makedirs(save_dir, exist_ok=True)
    
    base_url = f"https://gta.fandom.com/wiki/{vehicle_name.replace(' ', '_')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        image_figures = soup.find_all('figure', class_='pi-item pi-image')
        
        if not image_figures:
            print("❌ Aucune image trouvée dans les figures")
            return []

        downloaded_files = []
        
        for fig in image_figures:
            a_tag = fig.find('a', class_='image')
            if a_tag and 'href' in a_tag.attrs:
                img_url = a_tag['href']
                
                if 'revision/latest' in img_url:
                    img_url = img_url.split('?')[0] + '?' + img_url.split('?')[-1]
                
                try:
                    img_data = requests.get(img_url, headers=headers).content
                    
                    img_name = re.search(r'/([^/]+\.png)', img_url).group(1)
                    filename = os.path.join(save_dir, f"{vehicle_name}_{img_name}")
                    
                    with open(filename, 'wb') as f:
                        f.write(img_data)
                    
                    downloaded_files.append(filename)
                    print(f"✅ Téléchargé: {filename}")
                    
                except Exception as e:
                    print(f"⚠️ Erreur sur {img_url}: {str(e)}")
        
        return downloaded_files

    except Exception as e:
        print(f"🚨 Erreur majeure: {str(e)}")
        return []

download_vehicle_images("Sultan")