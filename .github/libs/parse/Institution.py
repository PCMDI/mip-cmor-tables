import json, os, sys, glob
from collections import OrderedDict

path = f'organisations/institutions'
toplevel = os.popen('git rev-parse --show-toplevel').read().strip()
loc = f"{toplevel}/JSONLD/{path}/"



# Get the parent directory of the current file
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)
import checks
from checks import schema,institution
from action_functions import update_issue,jr,jw,getfile,close_issue,pp

# data
issue_number = int(os.environ['ISSUE'])
data = os.environ['PAYLOAD_DATA']
data = json.loads(str(data))
data['acronym'] = data['acronym'].replace(' ','')

'''
Functions 
'''

URL_TEMPLATE = 'https://api.ror.org/organizations/{}'

import urllib.request
import json

def get_ror_data(name):
    """Get ROR data for a given institution name."""
    url = URL_TEMPLATE.format(name)
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            json_data = json.loads(data)
            return json_data
    except urllib.error.HTTPError as e:
        err = f"Error: {e.code} - {e.reason}"
        # print(err)
        return None
    except urllib.error.URLError as e:
        err = f"Error: {e.reason}"
        # print(err)
        return None




def parse_ror_data(cmip_acronym,ror_data):
    """Parse ROR data and return relevant information."""
    if ror_data:

        return {
            "@id": f"mip-cmor-tables:organisations/institutions/{cmip_acronym.lower()}",
            "@type": "cmip:institution",
            "institution:cmip_acronym": cmip_acronym,
            "institution:ror": ror_data['id'].split('/')[-1],
            "institution:name": ror_data['name'],
            "institution:url": ror_data.get('links', []) ,
            "institution:established": ror_data.get('established'),
            "institution:type": ror_data.get('types', [])[0] if ror_data.get('types') else None,
            "institution:labels": [i['label'] for i in ror_data.get('lables', [])],
            "institution:aliases": ror_data.get('aliases', []),
            "institution:acronyms": ror_data.get('acronyms', []),
            "institution:location": {
                "@id": f"mip-cmor-tables:organisations/institutions/location/{ror_data['id'].split('/')[-1]}",
                "@type": "institution:location",
                "@nest": {
                    "location:lat":  ror_data['addresses'][0].get('lat') if ror_data.get('addresses') else None,
                    "location:lon":  ror_data['addresses'][0].get('lat') if ror_data.get('addresses') else None,
                    "location:city": ror_data['addresses'][0].get('city') if ror_data.get('addresses') else None,
                    "location:country": list(ror_data['country'].values())  if ror_data.get('country') else None
                }
            }         
            #  can reverse match consortiums or members from here.    
            
        }
    else:
        return None
    
    

'''
Get the Data
'''


dta = get_ror_data(data['ror'])
new_entry = parse_ror_data(data['acronym'],dta)


outfile = f"{loc}{data['acronym'].lower()}.json"

close,errors = checks.institution.validate(new_entry,outfile)


for error in close:
    update_issue(issue_number,f'# Closing issue. \n {error} \n\n Please review request and resubmit.')
    
for error in errors:
    update_issue(issue_number,f'# {error} \n\n Please update (edit) the entry above.')


valid,validation_message = checks.schema.validate_json(new_entry)

if valid:
    update_issue(issue_number,validation_message,False)
else:
    error = f"Schema Failed.\n\n Please update the entry above. {validation_message}"
    # this exists the script. 
    update_issue(issue_number,error,err=True) 



    

update_issue(issue_number,f"# Sanity Check: \n Is '{data['full_name']}' the same as '{new_entry['institution:name']}'",False)

# print for pull request
pp( {data['acronym'] : new_entry })

jsn_ordered = OrderedDict(sorted(new_entry.items(), key=lambda item: item[0]))





if 'SUBMIT' in os.environ:
    if len(close):
        sys.exit(' skipping the submission.' )
    if os.environ['SUBMIT'] == 'none':
        sys.exit(' skipping the submission.' )
    elif os.environ['SUBMIT'] == 'manual':
        # this does not work
        inp = input('Submit to the repository? [y/n]')
        if not inp.lower() != 'y':
            sys.exit(' skipping the submission.' )
    elif os.environ['SUBMIT'] == 'auto':
        pass
    else:
        sys.exit(' skipping the submission.' )
    
# Serialize back to JSON
jw(jsn_ordered, outfile)

# normal entries if not specified.
os.popen(f'git add -A"').read()
if 'OVERRIDE_AUTHOR' in os.environ:
    os.popen(f'git commit --author="{os.environ["OVERRIDE_AUTHOR"]} {os.environ["OVERRIDE_AUTHOR"]}@users.noreply.github.com" -m "New entry {data["acronym"]} to the Institutions LD file"').read()
else: 
    os.popen(f'git commit -m "New entry {data["acronym"]} to the Institutions LD file"').read()













    
# def search_ror(query):

#     import requests,json
#     import urllib.parse

#     # Strip out strange characters and insert in the desired format
#     format_name = lambda n : urllib.parse.quote(n)
#     # Make the API call
#     url = 'https://api.ror.org/organizations?affiliation=%{}s'

#     response = requests.get(url.format(query))

#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
#         if data.get('items'):
#             org = data['items'][0].get('organization')
#             return data['items'][0]['score'],org['id'].split('/')[-1], org['name']
#         else: return None,None,None
#     else:
#         print(f"Error: {response.status_code} - {response.text}")
#         return None,None,None



# data = parsed['institutions']
# data['institutions'] = parsed['institutions']['cmip6_acronyms']