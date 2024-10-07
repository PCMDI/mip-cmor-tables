
import requests
import json
import os

# URLs of the JSON files on GitHub
json_url1 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/main/CMIP6_activity_id.json'
json_url2 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6Plus_CVs/main/CMIP6Plus_activity_id.json'

# Directory where the JSON files will be saved
save_dir = 'datadescriptor/activity/'

# Create the directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

# Function to fetch and load JSON data from a URL
def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    return response.json()

# Fetch the JSON data from both URLs
data1 = fetch_json(json_url1)
data2 = fetch_json(json_url2)

# Extract the activity_id dictionaries from both JSON files
activity_ids1 = data1.get('activity_id', {})
activity_ids2 = data2.get('activity_id', {})

# Create a dictionary with activity ID as key and a dictionary with long_name and url set to None
activity_dict = {key: {'long_name': value, 'url': None} for key, value in activity_ids1.items()}

# Update the dictionary with data from the second JSON, adding URL and long_name if available
for key, value in activity_ids2.items():
    activity_dict[key] = {
        'long_name': value.get('long_name', activity_dict[key]['long_name'] if key in activity_dict else None),
        'url': value.get('URL', None)
    }

# Save each activity as an individual JSON file
for key, value in activity_dict.items():
    activity_data = {
        '@context': "000_context.jsonld",
        'type':'activity',
        'id': key.lower(),
        'name': key,
        'cmip_acronym': key,
        'long_name': value['long_name'],
        'url': value['url']
    }
    file_path = os.path.join(save_dir, f"{key.lower()}.json")
    with open(file_path, 'w') as f:
        json.dump(activity_data, f, indent=4)

print("Activity files saved to", save_dir)
