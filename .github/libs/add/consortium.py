import re
import os

issue_title = os.environ.get('ISSUE_TITLE')
issue_body = os.environ.get('ISSUE_BODY')
issue_submitter = os.environ.get('ISSUE_SUBMITTER')

print(issue_body, issue_submitter)


def parse_md(body):
    # remove comments
    pattern = r'<!---(.*?)--->'

    # Remove comments using re.sub
    body = re.sub(pattern, '', body, flags=re.DOTALL)
    print(body)

    template_data = {}

    # Read lines from the file
    lines = body.split('\n')
    # [i for i in body.split('\n') if i.strip(' ')[0] != '#']

    # Iterate over each line
    current_key = None
    for line in lines:
        # Strip leading and trailing whitespaces
        line = line.strip()

        # Skip empty lines and lines starting with '##' (section headings)
        if not line or line.startswith("##"):
            continue

        # Check for lines containing '**'
        if line.startswith("**") and ":" in line:
            # Extract key and value
            key, value = line.split(":", 1)
            key = key.strip("**").strip()
            value = value.strip()

            # Store the current key-value pair
            template_data[key] = value
            current_key = key
        else:
            # If it's a continuation of the previous line, append it to the value
            if current_key:
                template_data[current_key] += " " + line

    return template_data


parsed = parse_md(issue_body)
print(parsed)
