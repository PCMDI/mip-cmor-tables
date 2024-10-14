from mip_cmor_tables.models.consortia import Consortia
import json
from pathlib import Path
from pprint import pp
with open(Path("datadescriptor/consortia/ncc.json")) as f:
    m_dict = json.load(f)

term = Consortia(**m_dict)
print("Complete Object")
pp(term)

print("##")
print("Member :")
pp(term.members[0])
pp(term.members[0].institution)

print("##")
print("Dates :")
pp(term.members[0].dates[0])

pp(term.members[0].dates[0].from_)
pp(term.members[0].dates[0].to)
