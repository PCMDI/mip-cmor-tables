from mip_cmor_tables.models.variant_label import VariantLabel
import json, re
from pathlib import Path
from pprint import pp
with open(Path("datadescriptor/variant_label/ripf.json")) as f:
    m_dict = json.load(f)

mytestVariant = "r1i2p4f1"


print("#"*40)
print("Only in Python with pydantic models")
print("#"*40)
term = VariantLabel(**m_dict)
pp(term.parts)

## Output : 
# [Part(id='one_digit', type='realisation_index', is_required=True),
#  Part(id='one_digit', type='initialisation_index', is_required=True),
#  Part(id='one_digit', type='physic_index', is_required=True),
#  Part(id='one_digit', type='forcing_index', is_required=True)]

# so we know now that this variant is build by concatenate 4 other datadescriptor separated by ""
# lets build the composite regex from the 4 regex of each datadescriptor

composite_regex = ""
for part in term.parts:
    with open(f"datadescriptor/{part.type}/{part.id}.json","r") as f:
        m_dict = json.load(f)
        composite_regex += m_dict["regex"]
        print(m_dict["regex"])

composite_regex = "^" + composite_regex.replace("^","").replace("$","") + "$"
print("Eventually : ", composite_regex)

print(f"Validation of {mytestVariant} :",re.match(composite_regex,mytestVariant))

print("cqfd :D")

# print("#"*40)
# print("with Framing with jsonld from local") # TODO 
# print("#"*40)



