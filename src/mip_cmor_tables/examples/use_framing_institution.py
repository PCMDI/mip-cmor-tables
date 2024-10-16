
from pyld import jsonld
from pathlib import Path
import json
from pprint import pp
print("#" * 40)
print(" #### SCENARIO : we want all locations of all institutions in this repository #### ")
print("#" * 40)
print("")
print("#" * 40)
print("## 1/ : load the jsonld files ")
print("#" * 40)
file_path = Path("datadescriptor/institution/aer.json")
institution_path = Path("datadescriptor/institution") 

def loader(local_path): # For now, only in local
            with open(local_path,"r") as f:
                content = json.load(f)
            contextUrl = local_path.parent / content["@context"]
            with open(contextUrl,"r") as c : 
                context = json.load(c)
            content["@context"] = context["@context"]
            return content

inst = loader(file_path)
pp(inst)

print("")
print("#" * 40)
print("## 2/ frame this data")
print("#" * 40)

mFrame = {
    "@context": {
        'location': {'@id': 'https://schema.org/location'},
        '@vocab' :"http://schema.org/" # to remove prefix from lat, lon, etc.
    },
    "@explicit": True, # to get only what we ask for
    "location": {},       # Extract the location object
}

frame_location_inst = jsonld.frame(inst,mFrame)
pp(frame_location_inst)



print("")
print("#" * 40)
print("## 3/ frame city inside location")
print("#" * 40)

mFrameCity = {
    "@context": {
        'location': {'@id': 'https://schema.org/location'},
        '@vocab' :"http://schema.org/" # to remove prefix from lat, lon, etc.
    },
    "@explicit": True, # to get only what we ask for
    "city": {},       # Extract the location object
}

print("\n# From the already framed location :\n")
frame_location_city = jsonld.frame(frame_location_inst,mFrameCity)
pp(frame_location_city)

print("\n# From the initial jsonld institution:\n")
frame_institution_city = jsonld.frame(inst,mFrameCity)
pp(frame_institution_city)



print("")
print("#" * 40)
print("## 3/ Do the framing for all terms")
print("#" * 40)

city_list = []
for term_path in institution_path.iterdir():
    if term_path.suffix==".json":
        city_list.append(jsonld.frame(loader(term_path),mFrameCity)["city"])

pp(city_list)

print("")
print("#" * 40)
pp("cqfd :D")
print("#" * 40)




