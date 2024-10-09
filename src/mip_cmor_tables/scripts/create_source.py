

import requests
import json
import os
from pprint import pp
# URLs of the JSON files on GitHub
json_url1 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/refs/heads/main/CMIP6_source_id.json'
json_url2 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6Plus_CVs/refs/heads/main/CMIP6Plus_source_id.json'
# Already adapted to jsonld here
jsonld_url3 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6Plus_CVs/refs/heads/jsonldIII/JSONLD/source/id/graph.jsonld '

# But .. not in main 
# + only 6 .. not entire Universe
# so useable to check the final data to save ? 


# Directory where the JSON files will be saved
save_dir = 'datadescriptor/source/'

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
ids1 = data1.get('source_id', {})
ids2 = data2.get('source_id', {})

# Merge both datasets into a single dictionary
_dict = ids1 | ids2

#pp(_dict)

#pp(_dict.keys())


for key, value in _dict.items():
    print("source :", key)
    data={}
    data['@context']='000_context.jsonld'
    data['id']=key.lower()
    data['type']='source'
    if 'license_info' in value:
        data['license'] = {
                "id" : value['license_info']['id'],
                "exceptions-contact" : value['license_info'].get('exceptions-contact',None),
                "source-specific-info" : value['license_info'].get('source_specific_info',None)
                }
        value.pop('license_info')


    for k, v in value.items():
        if k not in data:
            data[k]=v

    file_path = os.path.join(save_dir, f"{key.lower()}.json")
    with open(file_path, 'w') as f:
        print("   save :",key)
        json.dump(data, f, indent=4)

print("source files saved to", save_dir)

    




'''
# Save each experiment as an individual JSON file
for key, value in experiment_dict.items():
    experiment_data = {
        '@context':'000_context.jsonld',
        'id': key.lower(),
        'type':'experiment',
        'experiment_id': key,
        'activity_id': [v.lower() for v in value['activity_id']],
        'additional_allowed_model_components': [v.lower() for v in value['additional_allowed_model_components']],
        'description': value['description'],
        'end_year': value['end_year'],
        'experiment': value['experiment'],
        'min_number_yrs_per_sim': value['min_number_yrs_per_sim'] if (value['min_number_yrs_per_sim'] != "none" and value['min_number_yrs_per_sim']!="" ) else None,
        'parent_activity_id': [v.lower() for v in value['parent_activity_id']],
        'parent_experiment_id': [v.lower() for v in value['parent_experiment_id']],
        'required_model_components': [v.lower() for v in value['required_model_components']],
        'start_year': value['start_year'],
        'sub_experiment_id': [v.lower() for v in value['sub_experiment_id']],
        'tier': value['tier']
    }
    file_path = os.path.join(save_dir, f"{key.lower()}.json")
    with open(file_path, 'w') as f:
        json.dump(experiment_data, f, indent=4)

print("Experiment files saved to", save_dir)
'''
