import requests
import time

def get_asset_details(asset_id):
    url = f"https://economy.roblox.com/v2/assets/{asset_id}/details"
    response = requests.get(url)
    if response.status_code == 200:
        asset_details = response.json()
        return asset_details
    else:
        print(f"Failed to fetch details for asset ID {asset_id}. Status code: {response.status_code}")
        return None

def save_to_text(creator_id, asset_id, details):
    with open(f"{creator_id}_asset_details.txt", "a") as file:
        file.write(f"Asset ID: {asset_id}\n")
        file.write(f"Name: {details.get('Name', '')}\n")
        file.write(f"Description: {details.get('Description', '')}\n")
        file.write(f"Created: {details.get('Created', '')}\n")
        file.write(f"Updated: {details.get('Updated', '')}\n\n")

def get_asset_details_for_creator_type(asset_id, creator_type_id):
    asset_details = get_asset_details(asset_id)
    if asset_details and asset_details.get("Creator", {}).get("Id", "") == creator_type_id:
        save_to_text(creator_type_id, asset_id, asset_details)

def main():
    starting_asset_id = 1818  # Replace 1818 with any asset ID you want to start from
    creator_type_id = 1  # Replace with the Roblox user/group ID you want to filter by
    
    while starting_asset_id > 0:
        get_asset_details_for_creator_type(starting_asset_id, creator_type_id)
        starting_asset_id -= 1
        time.sleep(1)

if __name__ == "__main__":
    main()
