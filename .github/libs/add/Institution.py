
import json,sys,os,re

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)

from action_functions import parse_md, dispatch, update_issue


issue_number = os.environ.get('ISSUE_NUMBER')
issue_title = os.environ.get('ISSUE_TITLE')
issue_body = os.environ.get('ISSUE_BODY')
issue_submitter = os.environ.get('ISSUE_SUBMITTER')
repo = os.environ.get('REPO').replace('https://github.com','https://api.github.com/repos')
token = os.environ.get('GH_TOKEN')


parsed = parse_md(issue_body)


'''
Lets submit the data to a dispatch event
'''


data = parsed['consortium']
data['institutions'] = parsed['institutions']['cmip6_acronyms']





kind = __file__.split('/')[-1].replace('.py','')

payload = {
    "event_type": kind,
    "client_payload": {
        "name": data['acronym'], # we need this to define the pull request
        "issue": issue_number,
        "author" : issue_submitter,
        "data" : str(json.dumps(data).encode('utf-8'))
    }
}

update_issue (issue_number,kind,payload)


dispatch(token,payload,repo)

