import re
import os
import re,configparser
import json,ast
from io import StringIO

issue_number = os.environ.get('ISSUE_NUMBER')
issue_title = os.environ.get('ISSUE_TITLE')
issue_body = os.environ.get('ISSUE_BODY')
issue_submitter = os.environ.get('ISSUE_SUBMITTER')

print(issue_number, issue_body, issue_submitter)


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
