import json, os, sys

data = sys.argv[1]
# os.environ['PAYLOAD_DATA']

print(data)

with open('del.txt','w') as r:
  r.write(data)

# data = json.loads(data)

# print(data)
