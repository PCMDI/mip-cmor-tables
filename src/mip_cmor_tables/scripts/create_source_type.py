
import requests
import json
import os

# URLs of the JSON files on GitHub
json_url1 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/refs/heads/main/CMIP6_source_type.json'

# Directory where the JSON files will be saved
save_dir = 'datadescriptor/source_type/'

# Create the directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

# Function to fetch and load JSON data from a URL
def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    return response.json()

# Fetch the JSON data from both URLs
data1 = fetch_json(json_url1)

# Extract the experiment_id dictionaries from both JSON files
dict1 = data1.get('source_type', {})

for key, value in dict1.items():
    data = {
        '@context':'000_context.jsonld',
        'id': key.lower(),
        'type':'source_type',
        'description': value,
    }
    file_path = os.path.join(save_dir, f"{key.lower()}.json")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

print("source_type files saved to", save_dir)
