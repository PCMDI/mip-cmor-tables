

import requests
import json
import os

# URLs of the JSON files on GitHub
json_url1 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/refs/heads/main/CMIP6_nominal_resolution.json'

# Directory where the JSON files will be saved
save_dir = 'datadescriptor/resolution/'

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
list1 = data1.get('nominal_resolution', {})

'''

    name =i.replace(' ','')
    parts = name.split(' ')
    entry = {
        "@type":"resolution",
        "@id": f"mip-cmor-tables:auxillary/resolution/{name.lower()}",
        "name": i,
        "value": parts[0],
        "description": f"Resolution of {i}",
        "unit": parts[1],
    }
    '''


for value in list1:
    data = {
        '@context':'000_context.jsonld',
        'id': value.replace(' ','').lower(),
        'name':value.replace(' ',''),
        'value' : value.split(' ')[0].strip(),
        'unit' : value.split(' ')[1].strip(),
        'type':'resolution',
        'description': f"Resolution of {value}",
    }
    file_path = os.path.join(save_dir, f"{data['id'].lower()}.json")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

print("resolution files saved to", save_dir)
