import json, os

data = os.environ['DATA']

data = json.loads(data)

print(data)
