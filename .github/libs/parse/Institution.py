import json, os, sys
from collections import OrderedDict

# Get the parent directory of the current file
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)

from action_functions import update_issue,jr,jw,getfile,close_issue,pp

# data
issue_number = os.environ['ISSUE']
data = os.environ['PAYLOAD_DATA']
data = json.loads(str(data))


# Load Existing
institutions = jr(getfile('institutions')[0])
ilist = institutions['institutions']




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




def parse_ror_data(ror_data):
    """Parse ROR data and return relevant information."""
    if ror_data:

        return {
            "identifiers": {
                'institution_name': ror_data['name'],
                'aliases': ror_data.get('aliases', []),
                'acronyms': ror_data.get('acronyms', []),
                'labels': [i['label'] for i in ror_data.get('lables', [])],
                'ror': ror_data['id'].split('/')[-1],
                'url': ror_data.get('links', []),
                'established': ror_data.get('established'),
                'type': ror_data.get('types', [])[0] if ror_data.get('types') else None,
            },
            "location": {
                'lat': ror_data['addresses'][0].get('lat') if ror_data.get('addresses') else None,
                'lon': ror_data['addresses'][0].get('lng') if ror_data.get('addresses') else None,
                # 'latest_address': ror_data['addresses'][0].get('line') if ror_data.get('addresses') else None,
                'city': ror_data['addresses'][0].get('city') if ror_data.get('addresses') else None,
            #     'country': ror_data['country']['country_name'] if ror_data.get('country') else None
                'country': list(ror_data['country'].values())  if ror_data.get('country') else None
            },
            "consortiums":[]
            
        }
    else:
        return None
    
    
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



'''
Get the Data
'''

if data['acronym'] in ilist:
  close_issue(issue_number,f'# Closing issue. \n {data["acronym"]} already exists in the institution list. \n\n Please review request and resubmit.')

dta = get_ror_data(data['ror'])
new_entry = parse_ror_data(dta)


update_issue(issue_number,f"# Sanity Check: \n Is '{data['full_name']}' the same as '{new_entry['identifiers']['institution_name']}'",False)


ilist[data['acronym']] = new_entry

# print for pull request
pp( {data['acronym'] : new_entry })


ilist = OrderedDict(sorted(ilist.items(), key=lambda item: item[0]))

institutions['institutions'] = ilist

# Serialize back to JSON
jw(institutions, getfile('institutions')[0])

os.popen(f'git add -A"').read()
os.popen(f'git commit -m "New entry {data["acronym"]} to the Institutions file"').read()









