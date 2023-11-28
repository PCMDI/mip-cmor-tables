import urllib.request
import json
from collections import OrderedDict
import sys,os

base_id,table_name,view_name = 'appaZflpqbFjA6pwV/tblD5m3Bxsph5VjZ0/viwxN1LyTlEA2TZ5W'.split('/')

# read from action
api_key = sys.argv[1]  # Replace with your actual Airtable API key

url = f'https://api.airtable.com/v0/{base_id}/{table_name}?view={view_name}'

# Set up headers with your Airtable API key
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

# Create a request with headers
request = urllib.request.Request(url, headers=headers)


model_components = {}

# Make the API request to get data in JSON format
with urllib.request.urlopen(request) as response:
    # Process the response as needed
    if response.status == 200:
        data = json.loads(response.read().decode('utf-8'))
        records = data.get('records', [])
        for record in records:
            fields = record.get('fields', {})
            realm = fields['realm']
            description = fields['description']
            resolution = fields['resolution']+' km'
            if realm not in model_components: 
                model_components[realm] = {}
            if description not in model_components[realm]:
                model_components[realm][description] = {'description' : description, 'native_nominal_resolutions':[]}

            if resolution not in model_components[realm][description]['native_nominal_resolutions']:
                model_components[realm][description]['native_nominal_resolutions'].append(resolution)
           


    else:
        print(f"Failed to retrieve data. Status code: {response.status}")



def sort_dict_recursive(input_dict):
    if isinstance(input_dict, dict):
        return OrderedDict((key, sort_dict_recursive(value)) for key, value in sorted(input_dict.items()))
    elif isinstance(input_dict, list):
        return [sort_dict_recursive(item) for item in input_dict]
    else:
        return input_dict
    

model_components = sort_dict_recursive(model_components)

if __name__ == '__main__':

    file_path = 'Auxillary_files/MIP_model_components.json'

    # Write the dictionary to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(model_components, json_file, indent=4)

import version

tag = os.environ['GH_TOKEN']
new_contents = version.process_files([file_path],tag=tag,write=False)

with open(file_path, 'w') as json_file:
    json.dump(new_contents, json_file, indent=4)