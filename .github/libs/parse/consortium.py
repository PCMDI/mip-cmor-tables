import json, os

data = os.environ['PAYLOAD_DATA']

print(data)

data = json.loads(data)

print(data)
