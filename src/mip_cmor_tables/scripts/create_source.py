

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

knownK = []

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

    data["activity_participation"]=[item.lower() for item in data["activity_participation"]]


    data["organisation_id"]=[item.lower() for item in data["institution_id"]]
    data.pop("institution_id")
    
    model_component_new_dict={}
    for k,v in data["model_component"].items():
        if v["description"] != "none":
            model_component_new_dict[k]=v["description"].split(" ")[0].lower()
        if k not in knownK:
            knownK.append(k)

    data["model_component"]= model_component_new_dict
    
    data.pop("source_id")

    file_path = os.path.join(save_dir, f"{key.lower()}.json")
    with open(file_path, 'w') as f:
        print("   save :",key)
        json.dump(data, f, indent=4)
print(knownK)
print("source files saved to", save_dir)

    


'''
print("Experiment files saved to", save_dir)
'''
