import json, os, sys

data = sys.argv[1]
# os.environ['PAYLOAD_DATA']

print(data)

data = json.loads(data)

print(data)
