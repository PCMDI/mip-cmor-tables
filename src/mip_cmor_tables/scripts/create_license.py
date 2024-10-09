

from pathlib import Path
import json
from pprint import pp
import os

# License are found in source (in sense : model)
dir_source= Path("datadescriptor/source")
save_dir= Path("datadescriptor/license")
# Create the directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

already_done = []
for source_path in dir_source.glob("*.json"):
    with open(source_path) as f:
        print(source_path)

        data = json.load(f)
        #print(data)
    #pp(data.get("license_info",[]))
    license_data=data.get("license_info",None)
    if license_data is not None:
        if license_data["id"] not in already_done: 

            _dict = {
                "@context":"000_context.jsonld",
                "id" : license_data["id"].lower().replace(" ","_"),
                "kind" :license_data["id"],
                "license" : license_data["license"],
                "url" : license_data["url"]
            }
            already_done.append(license_data["id"])
            
            '''
            else:
                pp(license_data["exceptions_contact"])
                # there is some customization
                # depending on the source .. but .. license it self is not defined by those => the specific license stuff for a specific source will be stored in sources (terms)

            '''
            # save :
            file_path = os.path.join(save_dir, f"{_dict['id'].lower()}.json")
            with open(file_path, 'w') as f:
                json.dump(_dict, f, indent=4)




    

