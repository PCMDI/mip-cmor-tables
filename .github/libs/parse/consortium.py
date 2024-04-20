import json, os

data = sys.argv[1]
# os.environ['PAYLOAD_DATA']

print(data)

data = json.loads(data)

print(data)
