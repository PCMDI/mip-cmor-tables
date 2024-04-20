import json, os

data = os.environ['PAYLOAD_DATA']

data = json.loads(data)

print(data)
