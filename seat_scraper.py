import json
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote
import re

MANUAL_MAPPING = {
    "TAMPA DRIFT": "Drift Tampa",
    "SPEEDO (CUSTOM)": "Speedo",
    "BRIOSO 300 LARGE": "Brioso 300",
    "FELON GT": "Felon GT",
    "COGCABRIO": "Cognoscenti Cabrio",
    "ORACLE XSLE": "Oracle",
    "SUPER DIAMOND LIMOUSIN": "Super Diamond",
    "COMET 62 500 $": "Comet",
    "SCHARTZER S": "Schwartzer",
    "TOROS 156 250 $": "Toros",
}

def normalize_vehicle_name(name):
    if name in MANUAL_MAPPING:
        return MANUAL_MAPPING[name]
    
    name = re.sub(r'\d+\s?\$|\$|\d+|\(.*?\)|INVENDABLE|invendable|Invendable', '', name).strip()
    name = name.lower().title()
    name = name.replace("Xr", "XR").replace("Gt", "GT").replace("R/A", "RA")
    
    return name

def get_seats_from_gta_db(vehicle_name):
    try:
        normalized_name = normalize_vehicle_name(vehicle_name)
        encoded_name = quote(normalized_name)
        url = f"https://www.gta-db.com/gta-vehicles/gta-5-vehicles/?&sortby=purchase_price&sortorder=asc&search={encoded_name}"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'table'})
        if not table:
            return None
            
        rows = table.find_all('tr')[1:] 
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 1:  
                db_name = cols[0].get_text(strip=True)
                if normalized_name.lower() in db_name.lower() or db_name.lower() in normalized_name.lower():
                    if len(cols) >= 5:  
                        seats = cols[4].get_text(strip=True)
                        return int(seats) if seats.isdigit() else None
        
        if normalized_name != vehicle_name:
            return get_seats_from_gta_db(vehicle_name)
            
    except Exception as e:
        print(f"Erreur pour {vehicle_name}: {str(e)}")
    
    return None

def process_vehicles(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        vehicles = json.load(f)
    
    results = []
    for i, vehicle in enumerate(vehicles):
        vehicle_name = vehicle["Nom véhicule"]
        print(f"Processing {i+1}/{len(vehicles)}: {vehicle_name}")
        
        price = vehicle["Prix"]
        if isinstance(price, str):
            clean_price = re.sub(r'[^\d]', '', price)
            vehicle["Prix"] = int(clean_price) if clean_price.isdigit() else None
        else:
            vehicle["Prix"] = price if isinstance(price, int) else None
        
        seats = get_seats_from_gta_db(vehicle_name)
        vehicle["Nombre de sièges"] = seats
        
        results.append(vehicle)
        time.sleep(0.5)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Données sauvegardées dans {output_file}")

if __name__ == "__main__":
    input_json = "all_vehicles_data.json"
    output_json = "vehicles_with_seats_improved.json"
    process_vehicles(input_json, output_json)