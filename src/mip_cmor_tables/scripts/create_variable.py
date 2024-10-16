

import requests
import json
import os

# URLs of the JSON files on GitHub
json_url1 = 'https://raw.githubusercontent.com/PCMDI/mip-cmor-tables/refs/heads/main/MIP_variables.json'
# Directory where the JSON files will be saved
save_dir = 'datadescriptor/variable/'

# Create the directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

# Function to fetch and load JSON data from a URL
def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    return response.json()

# Fetch the JSON data from both URLs
data1 = fetch_json(json_url1)

# Extract the activity_id dictionaries from both JSON files
variable_ids1 = data1.get('variables', {})

#print(variable_ids1)


for key, value in variable_ids1.items():
    print(key)
    #print(value)
    res = {} 
    var_infos = variable_ids1.get(key,{})
    print("    ",var_infos)
    ## NEED TO MODIFIY 2,3 THINGS
    res["@context"] = "000_context.jsonld"  
    res["id"] = key
    res["cmip_acronym"] = value["out_name"]
    res["long_name"] = value["long_name"]
    res["standard_name"] = value["standard_name"]
    res["type"] = value["type"]
    res["units"] = value["units"]


    
    file_path = os.path.join(save_dir, f"{key.lower()}.json")
    with open(file_path, 'w') as f:
        json.dump(res, f, indent=4)
    


