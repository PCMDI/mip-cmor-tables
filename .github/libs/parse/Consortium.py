import json, os, sys
from collections import OrderedDict

# Get the parent directory of the current file
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)

from action_functions import update_issue,jr,jw,getfile,close_issue



# data
issue_number = os.environ['ISSUE']
data = os.environ['PAYLOAD_DATA']
data = json.loads(data)

# Load Existing
consortiums = jr(getfile('Consortiums')[0])
institutions = jr(getfile('Institution')[0])['institutions']

# Add new value and sort
conly = consortiums["consortiums"]


if data['acronym'] in conly:
  close_issue(issue_number,f'{data["name"]} already exists in the consortium list. Please review request.')

error = ''
inst = {}
for i in data['institutions']:
  if i not in institutions:
    error += f' - Institution [{i}] does not exists in the institutions file. Please add this to proceed.\n'
  else:
    inst[i] = f'{i} [{institutions[i]['identifiers']['ror']} - {institutions[i]['identifiers']['institution_name']}]'
  
if error: update_issue(issue_number,error)



conly[data['acronym']] = {"name": data['name'], "contains": sorted(list(inst.values()))}

sorted_consortiums = OrderedDict(sorted(conly.items()))


# Update data
data["consortiums"] = sorted_consortiums

# Serialize back to JSON
new_json_data = jw(data, getfile('Consortiums')[0])
















# with open('del.txt','w') as r:
#   r.write(data)

# os.popen('git add -A').read()

# 

# print(data)
