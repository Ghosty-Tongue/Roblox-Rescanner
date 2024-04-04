import requests
import time
from datetime import datetime, timedelta

def get_asset_details(asset_id):
    url = f"https://economy.roblox.com/v2/assets/{asset_id}/details"
    response = requests.get(url)
    if response.status_code == 200:
        asset_details = response.json()
        return asset_details
    else:
        print(f"Failed to fetch details for asset ID {asset_id}. Status code: {response.status_code}")
        return None

def format_time(timestamp):
    try:
        parsed_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        return parsed_time.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return timestamp

def save_to_text(creator_id, asset_id, details):
    with open(f"{creator_id}_asset_details.txt", "a") as file:
        file.write(f"Asset ID: {asset_id}\n")
        file.write(f"Name: {details.get('Name', '')}\n")
        file.write(f"Description: {details.get('Description', '')}\n")
        file.write(f"Created: {format_time(details.get('Created', ''))}\n")
        file.write(f"Updated: {format_time(details.get('Updated', ''))}\n\n")

def get_asset_details_for_creator_type(asset_id, creator_id, creator_type_id):
    asset_details = get_asset_details(asset_id)
    if asset_details and asset_details.get("Creator", {}).get("Id", "") == creator_id and asset_details.get("Creator", {}).get("CreatorType", "") == creator_type_id:
        save_to_text(creator_id, asset_id, asset_details)

def calculate_total_time(starting_asset_id, rate):
    total_ids = starting_asset_id
    total_time_seconds = total_ids * rate
    total_time_timedelta = timedelta(seconds=total_time_seconds)
    return total_time_timedelta

def human_readable_time(delta):
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds"

def main():
    starting_asset_id = 1818  # Replace 1818 with the starting asset ID
    creator_id = 1  # Replace 1 with the creator ID
    creator_type_id = "User"  # Only accepted types are "User" and "Group"
    rate = 0.5  # Scanning rate in seconds per asset ID
    
    total_time = calculate_total_time(starting_asset_id, rate)
    estimated_finish_time = datetime.now() + total_time
    print(f"Estimated finish time: {estimated_finish_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Estimated total time: {human_readable_time(total_time)}")
    
    while True:
        response = input("Continue scanning? (yes/no): ")
        if response.lower() == "yes":
            break
        elif response.lower() == "no":
            print("Scanning terminated.")
            return
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    while starting_asset_id > 0:
        get_asset_details_for_creator_type(starting_asset_id, creator_id, creator_type_id)
        starting_asset_id -= 1
        time.sleep(rate)

if __name__ == "__main__":
    main()
