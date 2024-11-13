# The idea is to add the key:value "drs_name" to all terms that appears in DRS
from pathlib import Path
import json

base_dir = Path("datadescriptor")

activity_dir = Path("activity")
for term_path in (base_dir / activity_dir).iterdir():
    # print(term_path)
    if term_path.suffix==".json":
        print(term_path)
        with open(term_path,"r") as f:
            data = json.load(f)
        data["drs_name"] = data["cmip_acronym"]
        with open(term_path,"w") as f:
            json.dump(data, f, indent=4)
            
