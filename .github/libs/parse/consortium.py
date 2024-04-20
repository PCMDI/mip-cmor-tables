import json, os, sys

data = sys.argv[1]
# os.environ['PAYLOAD_DATA']

print(data)

with open('del.txt','w') as r:
  r.write(data)

os.popen('git add -A').read()

# data = json.loads(data)

# print(data)
