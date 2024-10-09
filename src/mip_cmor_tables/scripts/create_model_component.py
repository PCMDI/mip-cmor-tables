from pathlib import Path
import json
import os
import requests
import re
# run it (working dir) from root dir
#input_terms_directory = Path("_archive/JSONLD/auxillary/realm/")



output_terms_directory = Path("datadescriptor/model_component")

os.makedirs(output_terms_directory, exist_ok=True)

# URL of the GitHub directory
url = "https://github.com/WCRP-CMIP/CMIP6Plus_CVs/tree/jsonldIII/JSONLD/model/component"

# Send request to get the HTML content of the page
response = requests.get(url)

# Find all occurrences of .json links using regex
# GitHub links to files include '/blob/branch/filename'
json_files = re.findall(r'href="(/WCRP-CMIP/CMIP6Plus_CVs/blob/jsonldIII/JSONLD/model/component/[^"]+\.json)"', response.text)

json_files = list(set(json_files))
# Build the full URLs for the JSON files
json_urls = ["https://github.com" + link.replace('/blob/', '/raw/') for link in json_files]
print(json_urls)

# Function to fetch and load JSON data from a URL
def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    return response.json()

for json_url in json_urls:
    input_term = fetch_json(json_url)
    print(input_term)
    # what to change : 
    # add link to context 
    # id => remove @ + to get uri right => point to URI server
    # type => remove @
    output_term = input_term

    output_term["@context"] = "000_context.jsonld"
    output_term["id"] = output_term["name"].lower()
    output_term.pop("@id")

    output_term["type"]  = input_term["@type"].replace("-","_")
    output_term.pop("@type")

    output_term["nominal_resolution"] = {
        "id" : input_term["nominal-resolution"]["@id"].split("/")[-1]
    }
    output_term.pop("nominal-resolution")
    #output_term["nominal_resolution"].pop("@id")

    output_term["realm"] = {
        "id" : input_term["realm"]["@id"].split("/")[-1]
    }
    #output_term["realm"].pop("@id")



    ordered_output_term = {
        "@context" : output_term["@context"],
        "id" : output_term["id"]

    } 
    for k,v in output_term.items():
        if k not in ordered_output_term:
            ordered_output_term[k]=v


    with open(f"{str(output_terms_directory)}/{output_term['id']}.json", "w") as outfile: 
        json.dump(ordered_output_term, outfile,indent=4)

print("model_component files saved to", output_terms_directory)

    


