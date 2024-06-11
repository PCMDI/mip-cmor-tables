
import os, json
import jsonschema
from jsonschema import validate


def rdjsn(f):
    return json.load(open(f,'r'))

def validate_json(jsn):
    
    if not isinstance(jsn, dict):
        # if we do not give a file, read this
        jsn = rdjsn(jsn)
    name = os.path.basename(jsn['@id'])
    
    schema_url = os.path.dirname(jsn['@id']).split(':')[-1]
    toplevel = os.popen('git rev-parse --show-toplevel').read().strip()
    
    schema_loc = f"{toplevel}/JSONLD/{schema_url}/schema.json"
    # outfile guarantees that we must run this
    
    schema = rdjsn(schema_loc)
    
    try:
        validate(instance=jsn, schema=schema)
        print(f"Validation succeeded: {name}")
        return True, f"Validation succeeded: {name}" 
    except jsonschema.exceptions.ValidationError as err:
        print("Validation error:", err.message, name)
        return False, "Validation error:\n {err.message}\n RelevantFile: {jsn['@id']}", False
    
    