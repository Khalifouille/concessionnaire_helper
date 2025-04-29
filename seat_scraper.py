import json
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote

def get_seats_from_gta_db(vehicle_name):
    try:
        encoded_name = quote(vehicle_name)
        url = f"https://www.gta-db.com/gta-vehicles/gta-5-vehicles/?&sortby=purchase_price&sortorder=asc&search={encoded_name}"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('table', {'class': 'table'})
        if not table:
            return None
            
        rows = table.find_all('tr')[1:]  
        if not rows:
            return None
            
        first_row = rows[0]
        cols = first_row.find_all('td')
        if len(cols) >= 5: 
            seats = cols[4].get_text(strip=True)
            return int(seats) if seats.isdigit() else None
            
    except Exception as e:
        print(f"Erreur pour {vehicle_name}: {str(e)}")
    
    return None

def process_vehicles(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        vehicles = json.load(f)
    
    for i, vehicle in enumerate(vehicles):
        vehicle_name = vehicle["Nom véhicule"]
        print(f"Processing {i+1}/{len(vehicles)}: {vehicle_name}")
        
        price = vehicle["Prix"]
        if not price.replace(" ", "").replace("$", "").replace(".", "").isdigit():
            vehicle["Prix"] = None
        else:
            clean_price = price.replace(" ", "").replace("$", "").replace(".", "")
            vehicle["Prix"] = int(clean_price)
        
        seats = get_seats_from_gta_db(vehicle_name)
        vehicle["Nombre de sièges"] = seats
        
        time.sleep(1)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(vehicles, f, ensure_ascii=False, indent=2)
    
    print(f"Données sauvegardées dans {output_file}")

if __name__ == "__main__":
    input_json = "all_vehicles_data.json"
    output_json = "vehicles_with_seats.json"
    process_vehicles(input_json, output_json)