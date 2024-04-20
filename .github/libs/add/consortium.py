import re
import os
import re,configparser
import json,ast
from io import StringIO

issue_number = os.environ.get('ISSUE_NUMBER')
issue_title = os.environ.get('ISSUE_TITLE')
issue_body = os.environ.get('ISSUE_BODY')
issue_submitter = os.environ.get('ISSUE_SUBMITTER')
repo = os.environ.get('REPO').replace('https://github.com','https://api.github.com/repos')
token = os.environ.get('GH_TOKEN')

print(repo,issue_number, issue_body, issue_submitter,token)


def parse_md(body):
    # remove comments
    pattern = r'<!---(.*?)--->'

    # Remove comments using re.sub
    body = re.sub(r'/r/n',r'/n', re.sub(pattern, '', body, flags=re.DOTALL))
    

    config_str = re.search(r'```\sconfigfile(.*?)```',body, re.DOTALL).group(1)
    print(config_str)

    # Create a file-like object from the string
    config_file = StringIO(config_str)
    
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    
    # Read configuration from the file-like object
    config.read_file(config_file)

    # Initialize an empty dictionary to hold the configuration data
    config_dict = {}

    # Iterate over sections and options
    for section in config.sections():
        config_dict[section] = {}
        for option in config.options(section):
            config_dict[section][option] = ast.literal_eval(config.get(section, option))
    
    return config_dict


parsed = parse_md(issue_body)
print(parsed)


'''
Lets submit the data to a dispatch event
'''


# {'consortium': {'acronym': 'TC', 'name': 'Test Consortium'}, 'consortium.institutions': {'cmip6_acronyms': ['CMIP-IPO', 'WCRP']}}
# Construct the dispatch event payload

data = parsed['consortium']
data['institutions'] = parsed['institutions']['cmip6_acronyms']


payload = {
    "event_type": __file__.split('/')[-1].replace('.py',''),
    "client_payload": {
        "name": data['acronym'], # we need this to define the pull request
        "issue": issue_number,
        "author" : issue_submitter,
        "data" : data
    }
}


# change issue name to reflect contents. 
print(os.popen(f'gh issue edit {issue_number} --title "Add Consortium: {payloda["client_payload"]["name"]}"').read())


# cmd = f'''
# gh api {repos.split("github.com/")[1]/dispatches \\
#   --field event_type="consortium" \\
#   --field client_payload="{payload}"
# '''

# print(os.popen(cmd).read())








import json
from urllib import request

# Construct the request headers
headers = {
    "Accept": "application/vnd.github.everest-preview+json",
    "Authorization": f"token {token}",
    "Content-Type": "application/json"
}

# Encode the payload
datapayload = json.dumps(payload).encode('utf-8')

# Make the POST request
req = request.Request(f"{repo}/dispatches", data=datapayload, headers=headers, method='POST')

# Perform the request
try:
    with request.urlopen(req) as response:
        if response.getcode() == 204:
            print("Dispatch event triggered successfully.")
        else:
            print(f"Failed to trigger dispatch event. Status code: {response.getcode()}")
            print(response.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
