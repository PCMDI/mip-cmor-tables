
import requests
import json
import os

# URLs of the JSON files on GitHub
json_url1 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/main/CMIP6_experiment_id.json'
json_url2 = 'https://raw.githubusercontent.com/WCRP-CMIP/CMIP6Plus_CVs/main/CMIP6Plus_experiment_id.json'

# Directory where the JSON files will be saved
save_dir = 'datadescriptor/experiment/'

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
experiment_ids1 = data1.get('experiment_id', {})
experiment_ids2 = data2.get('experiment_id', {})

# Normalize and merge data
def normalize_experiment_data(experiment_data):
    start_year = experiment_data.get('start', experiment_data.get('start_year', ''))
    end_year = experiment_data.get('end', experiment_data.get('end_year', ''))

    try:
        start_year = int(start_year)
    except ValueError:
        start_year = None  # or handle as needed if conversion fails
    try:
        end_year = int(end_year)
    except ValueError:
        end_year = None  # or handle as needed if conversion fails
    
    return {
        'activity_id': experiment_data.get('activity_id', []),
        'additional_allowed_model_components': experiment_data.get('additional_allowed_model_components', []),
        'description': experiment_data.get('description', ''),
        'end_year':end_year,
        'experiment': experiment_data.get('experiment', ''),
        'experiment_id': experiment_data.get('experiment_id', ''),
        'min_number_yrs_per_sim': experiment_data.get('min_number_yrs_per_sim', ''),
        'parent_activity_id': experiment_data.get('parent_activity_id', []),
        'parent_experiment_id': experiment_data.get('parent_experiment_id', []),
        'required_model_components': experiment_data.get('required_model_components', []),
        'start_year': start_year,
        'sub_experiment_id': experiment_data.get('sub_experiment_id', []),
        'tier': experiment_data.get('tier', '')
    }

# Merge both datasets into a single dictionary
experiment_dict = {}
for key, value in experiment_ids1.items():
    experiment_dict[key] = normalize_experiment_data(value)

for key, value in experiment_ids2.items():
    if key in experiment_dict:
        experiment_dict[key].update(normalize_experiment_data(value))
    else:
        experiment_dict[key] = normalize_experiment_data(value)

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
