from os import name
from pathlib import Path
import json
# run it (working dir) from root dir
input_frequency_terms_directory = Path("_archive/JSONLD/auxillary/frequency/")
output_frequency_terms_directory = Path("datadescriptor/frequency/")

terms_file_list = [p for p in input_frequency_terms_directory.iterdir() if (p.is_file() and "jsonld" not in str(p))]
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
    output_term["id"] = output_term["name"]
    output_term.pop("@id")

    output_term["type"]  = input_term["@type"]
    output_term.pop("@type")

    ordered_output_term = {
        "@context" : output_term["@context"],
        "id" : output_term["id"]

    } 
    for k,v in output_term.items():
        if k not in ordered_output_term:
            ordered_output_term[k]=v

    with open(f"{str(output_frequency_terms_directory)}/{output_term["id"]}.json", "w") as outfile: 
        json.dump(ordered_output_term, outfile,indent=4)
        
