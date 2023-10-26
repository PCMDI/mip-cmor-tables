import json
import concurrent.futures
import re

import os

cmipver = 3

# Function to extract variables from a single file
def process_file(filepath):
    variables = {}
    
    with open(filepath) as f:
        contents = f.read()

        if cmipver == 5:
            table = contents.split('\n')[0].split()[-1]
        if cmipver == 3:
            table = contents.split('\n')[3].split('able')[2].replace(' ','').rstrip('!t')

        
        variable_regex = r"!============\nvariable_entry:\s+([a-zA-Z0-9_]+)\n!============"
        matches = re.findall(variable_regex, contents)
        
        for match in matches:
            try:
                var_name = match
                var_section = re.search(rf"!============\nvariable_entry:\s+{var_name}\n!============([\s\S]*?)!============", contents).group(1)
                
                params = {}
                for line in var_section.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        params[key.strip()] = value.strip()
                
                variables[var_name] = params
            except AttributeError:
                ...
    
    return {table:variables}
            
# Main function to process files in parallel
if __name__ == "__main__":
    filenames = os.listdir("./Tables") # list files in directory
    
    all_variables = {}
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(process_file, [f"./Tables/{f}" for f in filenames])
        
        for result in results:
            all_variables.update(result)
            
    with open(f"cmip{cmipver}variables.json", "w") as f:
        json.dump(all_variables, f, indent=2)