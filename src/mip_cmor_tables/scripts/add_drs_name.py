# The idea is to add the key:value "drs_name" to all terms that appears in DRS
from pathlib import Path
import json

base_dir = Path("datadescriptor")

def load_data(term_path:Path):
    with open(term_path,"r") as f:
        data = json.load(f)
    return data

def save_data(data:dict, term_path:Path):
    with open(term_path,"w") as f:
        json.dump(data, f, indent=4)

def add_drs(dir_path:Path,key:str):
 for term_path in (base_dir / dir_path).iterdir():
    # print(term_path)
    if term_path.suffix==".json":
        print(term_path)
        data = load_data(term_path)
        print(data)
        data["drs_name"] = data[key]
        save_data(data,term_path)

   

add_drs(Path("activity"),"cmip_acronym")
add_drs(Path("consortia"),"cmip-acronym")



                    
