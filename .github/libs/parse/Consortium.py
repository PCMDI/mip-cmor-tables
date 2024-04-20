import json, os, sys
from collections import OrderedDict

# Get the parent directory of the current file
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)

from action_functions import update_issue,jr,jw,getfile,close_issue



# data
issue_number = os.environ['ISSUE']
data = os.environ['PAYLOAD_DATA']
data = json.loads(str(data))


# Load Existing
consortiums = jr(getfile('consortiums')[0])
institutions = jr(getfile('institutions')[0])['institutions']

# Add new value and sort
conly = consortiums["consortiums"]


if data['acronym'] in conly:
  close_issue(issue_number,f'# Closing issue. \n {data["acronym"]} already exists in the consortium list. \n\n Please review request and resubmit.')

error = ''
inst = {}
for i in data['institutions']:
  if i not in institutions:
    error += f'    - Institution [{i}] does not exists in the institutions file. Please add this to proceed.\n'
  else:
    inst[i] = f"{i} [{institutions[i]['identifiers']['ror']} - {institutions[i]['identifiers']['institution_name']}]"
  
if error: 
  error = '#Error: \n Pausing submission. Please edit the initial config (above) addressing the issues below to try again. \n\n ' + error
  update_issue(issue_number,error)



conly[data['acronym']] = {"name": data['name'], "contains": sorted(list(inst.values()))}

sorted_consortiums = OrderedDict(sorted(conly.items()))


# Update data
data["consortiums"] = sorted_consortiums

# Serialize back to JSON
new_json_data = jw(data, getfile('consortiums')[0])









