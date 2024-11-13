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

activity_dir = Path("activity")

for term_path in (base_dir / activity_dir).iterdir():
    # print(term_path)
    if term_path.suffix==".json":
        print(term_path)
        data = load_data(term_path)
        data["drs_name"] = data["cmip_acronym"]
        save_data(data,term_path)
                    
