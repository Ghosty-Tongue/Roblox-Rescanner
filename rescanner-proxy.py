import requests
import time
import json
from itertools import cycle

def load_proxies():
    with open("proxies.json", "r") as f:
        proxies = json.load(f)
    return proxies

def get_asset_details(asset_id, proxy_pool):
    url = f"https://economy.roblox.com/v2/assets/{asset_id}/details"
    proxy = next(proxy_pool)
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=10)
        if response.status_code == 200:
            asset_details = response.json()
            return asset_details
        else:
            print(f"Failed to fetch details for asset ID {asset_id}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching details for asset ID {asset_id} with proxy {proxy}: {e}")
        return None

def save_to_text(creator_id, asset_id, details):
    with open(f"{creator_id}_asset_details.txt", "a") as file:
        file.write(f"Asset ID: {asset_id}\n")
        file.write(f"Name: {details.get('Name', '')}\n")
        file.write(f"Description: {details.get('Description', '')}\n")
        file.write(f"Created: {details.get('Created', '')}\n")
        file.write(f"Updated: {details.get('Updated', '')}\n\n")

def main():
    starting_asset_id = 1818  # Replace 1818 with any asset ID you want to start from
    creator_type_id = 1  # Replace with the Roblox user/group ID you want to filter by
    
    proxies = load_proxies()
    proxy_pool = cycle(proxies)
    
    creator_file_created = False
    while starting_asset_id > 0:
        asset_details = get_asset_details(starting_asset_id, proxy_pool)
        if asset_details:
            creator_id = asset_details.get("Creator", {}).get("Id", "")
            if creator_id == creator_type_id:
                if not creator_file_created:
                    creator_file_created = True
                    with open(f"{creator_id}_asset_details.txt", "w") as file:
                        file.write("") 
                save_to_text(creator_id, starting_asset_id, asset_details)
        starting_asset_id -= 1
        time.sleep(0)  # Optional: Add a delay to avoid rate limiting or making too many requests

if __name__ == "__main__":
    main()
