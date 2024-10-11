
from pathlib import Path
import json
import os
from pprint import pp
# run it (working dir) from root dir
input_terms_directory = Path("_archive/JSONLD/organisations/institutions/")
output_terms_directory = Path("datadescriptor/institution/")

# Create the directory if it doesn't exist
os.makedirs(output_terms_directory, exist_ok=True)


terms_file_list = [p for p in input_terms_directory.iterdir() if (p.is_file() and "jsonld" not in str(p))]
#print(flist)
for p in terms_file_list:
    with open(p,"r") as input_file:
        input_term = json.load(input_file)

    # what to change : 
    # add link to context 
    # id => remove @ + to get uri right => point to URI server
    # type => remove @
    output_term = input_term

    output_term["@context"] = "000_context.jsonld"
    output_term["id"] = output_term["@id"].split('/')[-1]
    output_term.pop("@id")


    output_term.pop("type") # double definition in input for type and @type => remove type before redefine
    output_term["type"]  = input_term["@type"]
    output_term.pop("@type")


    output_term["location"].pop("@id")
    output_term["location"].pop("@type")
    output_term["location"]= input_term["location"]["@nest"]


    ordered_output_term = {
        "@context" : output_term["@context"],
        "id" : output_term["id"]

    } 

    for k,v in output_term.items():
        if k not in ordered_output_term:
            ordered_output_term[k]=v

    pp(ordered_output_term)

    with open(f"{str(output_terms_directory)}/{ordered_output_term['id']}.json", "w") as outfile: 
        json.dump(ordered_output_term, outfile,indent=4)
    
