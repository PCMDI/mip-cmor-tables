# we ll do it from scratch cause it depend of 4 data descriptor

from pathlib import Path
import os, json
from textwrap import indent

realisation_index_terms = []
initialization_index_terms = []
physic_index_terms = []
forcing_index_terms = []

variant_label_terms = []


DD_dir = Path("datadescriptor")

realisation_index_terms.append({
    "@context" : "000_context.jsonld",
    "id" : "one_digit",
    "type" : "realisation_index",
    "regex" : "^r\\d$"
    })

realisation_index_terms.append({
    "@context" : "000_context.jsonld",
    "id" : "run",
    "type" : "realisation_index",
    "regex" : "^run\\d$"
    })


save_path = DD_dir / Path("realisation_index") 
os.makedirs(save_path, exist_ok=True)
for t in realisation_index_terms:
    print(t)
    with open(save_path / f"{t['id']+'.json'}", "w") as f: 
        json.dump(t, f, indent= 4) 
        

initialization_index_terms.append({
    "@context" : "000_context.jsonld",
    "id" : "one_digit",
    "type" : "initialisation_index",
    "regex" : "^i\\d$"
    })

save_path = DD_dir / Path("initialisation_index") 
os.makedirs(save_path, exist_ok=True)
for t in initialization_index_terms:
    print(t)
    with open(save_path / f"{t['id']+'.json'}", "w") as f: 
        json.dump(t, f, indent= 4) 


physic_index_terms.append({
    "@context" : "000_context.jsonld",
    "id" : "one_digit",
    "type" : "physic_index",
    "regex" : "^p\\d$"
    })


save_path = DD_dir / Path("physic_index") 
os.makedirs(save_path, exist_ok=True)
for t in physic_index_terms:
    print(t)
    with open(save_path / f"{t['id']+'.json'}", "w") as f: 
        json.dump(t, f, indent= 4) 

forcing_index_terms.append({
    "@context" : "000_context.jsonld",
    "id" : "one_digit",
    "type" : "forcing_index",
    "regex" : "^f\\d$"
    })

forcing_index_terms.append({
    "@context" : "000_context.jsonld",
    "id" : "multiple_digit",
    "type" : "forcing_index",
    "regex" : "f\\d+$"
    })

save_path = DD_dir / Path("forcing_index") 
os.makedirs(save_path, exist_ok=True)
for t in forcing_index_terms:
    print(t)
    with open(save_path / f"{t['id']+'.json'}", "w") as f: 
        json.dump(t, f, indent= 4) 

variant_label_terms.append({
    "@context" : "000_context.jsonld",
    "id": "rip",
    "type" : "variant_label",
    "separator": "",
    "parts": [
    { 
        "id" : "one_digit",
        "type" : "realisation_index",
        "is_required": True
    },
    { 
        "id" : "one_digit",
        "type" : "initialisation_index",
        "is_required": True
    },
    { 
        "id" : "one_digit",
        "type": "physic_index",
        "is_required": True
    }
    ],
    "description" : "TODO IMPROVE THIS"

})



variant_label_terms.append({
    "@context" : "000_context.jsonld",
    "id": "ripf",
    "type" : "variant_label",
    "separator": "",
    "parts": [
    { 
        "id" : "one_digit",
        "type" : "realisation_index",
        "is_required": True
    },
    { 
        "id" : "one_digit",
        "type" : "initialisation_index",
        "is_required": True
    },
    { 
        "id" : "one_digit",
        "type": "physic_index",
        "is_required": True
    },
    { 
        "id" : "one_digit",
        "type": "forcing_index",
        "is_required": True
    }

    ],
    "description" : "TODO IMPROVE THIS"

})

variant_label_terms.append({
    "@context" : "000_context.jsonld",
	"id": "run",
    "type" : "variant_label",
    "separator": "",
	"parts": [
		{ 
			"id" : "run",
            "type" : "realization",
			"is_required": True
		}
	],
	"description" : "TODO IMPROVE THIS"
})

save_path = DD_dir / Path("variant_label") 
os.makedirs(save_path, exist_ok=True)
for t in variant_label_terms:
    print(t)
    with open(save_path / f"{t['id']+'.json'}", "w") as f: 
        json.dump(t, f, indent= 4) 

