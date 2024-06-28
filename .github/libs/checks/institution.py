import os, json, sys, glob

def validate(jsn,iloc):
    path = os.path.dirname(jsn['@id']).split(':')[-1]
    
    errors = []  
    close = []  
    
    # assert os.path.exists(loc), f"Path does not exist: {loc}"
    # existing = [os.path.splitext(os.path.basename(f))[0] for f in  glob.glob(f"{loc}/*.json")]
    
    if os.path.exists(iloc):
        close.append(f"Current institution already exists:\n see {iloc}")
        
    
    if path not in iloc:
        errors.append(f"@id / location do not match:\n {path} || {jsn['@id']}")
    
    
    graph = open(os.path.dirname(iloc)+"/graph.json",'r').read()
    if jsn['institution:ror'] in graph:
        close.append(f"ROR entry already exists in graph. \n EXITING: {jsn['institution:ror']}")
    
    
    return close,errors