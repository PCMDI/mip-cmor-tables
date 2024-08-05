import json, os, sys, glob
from collections import OrderedDict


from cmipld.git.repo_info import ldpath,commit, commit_override_author,addfile
from cmipld.utils.io import read_url
from cmipld.action_functions import update_issue,jr,jw,getfile,close_issue,pp

path = f'organisations/institutions'
loc = ldpath(path)

# Get the parent directory of the current file
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)
import checks
# from checks import schema,institution

# data
issue_number = int(os.environ['ISSUE'])
data = os.environ['PAYLOAD_DATA']
data = json.loads(str(data))

data['acronym'] = data['acronym'].replace(' ','')
print(data['acronym'])

'''
Functions 
'''

URL_TEMPLATE = 'https://api.ror.org/organizations/{}'



def get_ror_data(name):
    """Get ROR data for a given institution name."""
    url = URL_TEMPLATE.format(name)
    return read_url(url)



def parse_ror_data(cmip_acronym,ror_data):
    """Parse ROR data and return relevant information."""
    if ror_data:

        return {
            "@id": f"mip-cmor-tables:organisations/institutions/{cmip_acronym.lower()}",
            "@type": "cmip:institution",
            "cmip_acronym": cmip_acronym,
            "ror": ror_data['id'].split('/')[-1],
            "name": ror_data['name'],
            "url": ror_data.get('links', []) ,
            "established": ror_data.get('established'),
            "type": ror_data.get('types', [])[0] if ror_data.get('types') else None,
            "labels": [i['label'] for i in ror_data.get('lables', [])],
            "aliases": ror_data.get('aliases', []),
            "acronyms": ror_data.get('acronyms', []),
            "location": {
                "@id": f"mip-cmor-tables:organisations/institutions/location/{ror_data['id'].split('/')[-1]}",
                "@type": "location",
                "@nest": {
                    "lat":  ror_data['addresses'][0].get('lat') if ror_data.get('addresses') else None,
                    "lon":  ror_data['addresses'][0].get('lat') if ror_data.get('addresses') else None,
                    "city": ror_data['addresses'][0].get('city') if ror_data.get('addresses') else None,
                    "country": list(ror_data['country'].values())  if ror_data.get('country') else None
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



    

update_issue(issue_number,f"# Sanity Check: \n Is '{data['full_name']}' the same as '{new_entry['name']}'",False)

# print for pull request
pp( {data['acronym'] : new_entry })

jsn_ordered = OrderedDict(sorted(new_entry.items(), key=lambda item: item[0]))


if 'SUBMIT' in os.environ:
    if len(close):
        sys.exit(' skipping the submission.' )
    if os.environ['SUBMIT'] == 'none':
        sys.exit(' skipping the submission.' )
    elif os.environ['SUBMIT'] == 'auto':
        print("auto",outfile)
        pass
    else:
        sys.exit(' skipping the submission.' )
    
# Serialize back to JSON
jw(jsn_ordered, outfile)

# normal entries if not specified.

addfile(outfile)
if not commit_override_author(data['acronym'],'Institutions'):
    commit(f'New entry {data["acronym"]} to the Institutions LD file')
    













    
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