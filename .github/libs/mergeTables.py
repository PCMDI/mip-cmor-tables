'''
A script to generate the searchable index and aggregate miptables for display. 

Contact: daniel.ellis@wcrp-cmip.org

Installation:
    https://pypi.org/project/lunr/
    pip install lunr
'''


import json
import glob
from collections import OrderedDict

keys = [
        'table',
        'out_name',
        'comment',
        'dimensions',
        'frequency',
        'long_name',
        'modeling_realm',
        #  'ok_max_mean_abs',
        #  'ok_min_mean_abs',
        'positive',
        'standard_name',
        'type',
        'units',
        #  'valid_max',
        #  'valid_min',
        'cell_measures',
        'cell_methods',
        'commit']

index = [
        'table',
        'out_name',
        'comment',
        'dimensions',
        # 'frequency', this is in the table name
        'long_name',
        'modeling_realm',
        #  'ok_max_mean_abs',
        #  'ok_min_mean_abs',
        # 'positive',
        'standard_name',
        # 'type',
        # 'units', 
        #  'valid_max',
        #  'valid_min',
        # 'cell_measures', 
        # 'cell_methods',
        # 'commit'
        ]


def process_table(t):
    with open(t, 'r') as file:
        data = json.load(file)

    header = data['Header']
    table = header['table_id']
    commit = ''

    entries = data["variable_entry"]
    for k in entries:
        
        entries[k]['table'] = table
        entries[k]['commit'] = commit
        # entries[k]['id'] = f"{table}_{entries[k]['out_name']}"
        
        
        entries[k]= OrderedDict((key, entries[k][key]) for key in keys)

    return list(entries.values())



def main():
        
    tables = glob.glob('Tables/*.json')
    merged = []

    for t in tables:
        merged.extend(process_table(t))
        
    with open('.github/mip-cmor-tables.json', 'w') as outfile:
        for i,k in enumerate(merged):
            k['id'] = i
            outfile.write(f'{json.dumps(k)}\n')
            

    # lets create the index and save it. 
    from lunr import lunr

    idx = lunr(
    ref='id', fields=(index), documents=merged
    )

    serialized_idx = idx.serialize()
    with open('.github/idx.json', 'w') as outfile:
        json.dump(serialized_idx, outfile)
        
if __name__ == "__main__":
    main()


# Search all | field in main document. 


''' 
# To reverse the process

from lunr.index import Index
with open("idx.json") as fd:
    serialized_idx = json.loads(fd.read())

idx = Index.load(serialized_idx)


  # note we can boost documents in the results list
    # }, { 'boost': 10 }

'''


