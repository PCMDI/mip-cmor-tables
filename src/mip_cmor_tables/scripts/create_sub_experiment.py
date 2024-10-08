
import requests
import json
import os

# URLs of the JSON files on GitHub
json_url1 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/refs/heads/main/CMIP6_sub_experiment_id.json'
json_url2 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6Plus_CVs/refs/heads/main/CMIP6Plus_sub_experiment_id.json'

# Directory where the JSON files will be saved
save_dir = 'datadescriptor/sub_experiment/'

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

# Extract the experiment_id dictionaries from both JSON files
sub_experiment_dict1 = data1.get('sub_experiment_id', {})
sub_experiment_dict2 = data2.get('sub_experiment_id', {})


# Merge both datasets into a single dictionary
sub_experiment_dict = sub_experiment_dict1 | sub_experiment_dict2

for key, value in sub_experiment_dict.items():
    sub_experiment_data = {
        '@context':'000_context.jsonld',
        'id': key.lower(),
        'type':'sub_experiment',
        'description': value,
    }
    file_path = os.path.join(save_dir, f"{key.lower()}.json")
    with open(file_path, 'w') as f:
        json.dump(sub_experiment_data, f, indent=4)

print("sub_experiment files saved to", save_dir)
