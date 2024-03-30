import requests
import csv
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

def save_to_csv(csv_filename, asset_id, details):
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            details.get("AssetId", ""),
            details.get("Name", ""),
            details.get("Description", ""),
            details.get("Created", ""),
            details.get("Updated", "")
        ])

def get_asset_details_for_creator_type(asset_id, creator_type_id):
    asset_details = get_asset_details(asset_id)
    if asset_details and asset_details.get("Creator", {}).get("Id", "") == creator_type_id:
        csv_filename = f"{creator_type_id}_asset_details.csv"
        save_to_csv(csv_filename, asset_id, asset_details)
        print(f"Asset ID: {asset_id}")
        print("Details:", asset_details)
        print("\n")

def main():
    starting_asset_id = 1818  # Replace 1818 with any asset ID you want to start from
    creator_type_id = 1  # Replace with the Roblox user/group ID you want to filter by
    unique_creators = set()  # Store unique creator IDs

    while starting_asset_id > 0:
        asset_details = get_asset_details(starting_asset_id)
        if asset_details:
            creator_id = asset_details.get("Creator", {}).get("Id", "")
            if creator_id == creator_type_id:
                get_asset_details_for_creator_type(starting_asset_id, creator_type_id)
                unique_creators.add(creator_id)
        
        starting_asset_id -= 1
        time.sleep(1)

    for creator_id in unique_creators:
        with open(f"{creator_id}_asset_details.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["AssetId", "Name", "Description", "Created", "Updated"])

if __name__ == "__main__":
    main()
