

from os import name
from pathlib import Path
import json, os
from pprint import pp
# run it (working dir) from root dir
input_terms_directory = Path("_archive/Tables/")
output_terms_directory = Path("datadescriptor/table/")
os.makedirs(output_terms_directory, exist_ok=True)

terms_file_list = [p for p in input_terms_directory.iterdir() if (p.suffix==".json") ]
#print(terms_file_list)
for p in terms_file_list:
    with open(p,"r") as input_file:
        input_term = json.load(input_file)

    # what to change : 
    # add link to context 
    # id => remove @ + to get uri right => point to URI server
    # type => remove @
    output_term = {}
    #pp(output_term)

    output_term["@context"] = "000_context.jsonld"
    output_term["id"] = input_term["Header"]["table_id"]

    output_term["type"]  = "table"

    output_term["product"]  = input_term["Header"]["product"]
    output_term["table_date"]  = input_term["Header"]["table_date"]

    output_term["variable_entry"] = []
    for k,v in input_term["variable_entry"].items():
        output_term["variable_entry"].append(k) # It is OK ? only the var name ? see TODO 



    ordered_output_term = {
        "@context" : output_term["@context"],
        "id" : output_term["id"]

    }


    for k,v in output_term.items():
        if k not in ordered_output_term:
            ordered_output_term[k]=v

    pp(ordered_output_term)

    

    with open(f"{str(output_terms_directory)}/{output_term['id']}.json", "w") as outfile: 
        json.dump(ordered_output_term, outfile,indent=4)
     
