import asyncio
import glob
import os
import json
from pprint import pprint
from tqdm import tqdm

async def read_json_file(file_path):
    with open(file_path, mode='r') as f:
        content = f.read()
        return json.loads(content)

async def read_json_files(file_paths):
    tasks = [read_json_file(file_path) for file_path in file_paths]
    return await asyncio.gather(*tasks)

async def categorize_files(directory):
    graph_files = []
    context_files = []

    for root, dirs, files in os.walk(directory):
        
        if 'context.json' in files:
          
            context_file_path = os.path.join(root, 'context.json')
            context_files.append(context_file_path)
        
            # Also add all JSON files in this directory to graph_files
            graph_files.extend(os.path.join(root, file) for file in files if file.endswith('.json') and not file.endswith('context.json'))

    graph_data = await read_json_files(graph_files)
    
    
    context_data = {}

    # Loop through each entry in the contexts list
    for entry in await read_json_files(context_files):
        # Loop through each key-value pair in the entry dictionary
        for key, value in entry.items():
            if key in context_data:
                context_data[key]['@context'].update(value['@context'])
            else:
                context_data[key] = value
                
            
    context_data = context_data
    
    return {'graph': graph_data, 'context': context_data}

async def main():
    lddata = await categorize_files('./')

    # Dumping the contents of each category to separate files
    json.dump(lddata['graph'], open('graph_data.json', 'w'), indent=4)
    json.dump(lddata['context'], open('context_data.json', 'w'), indent=4)

# Create a new event loop and run the main coroutine until it completes
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
