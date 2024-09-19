import json
import logging
import os
import copy
from pathlib import Path
from multiprocessing import Pool

from collections import defaultdict
import update_provenance as up


def process_file(filepath):
    """
    Process a JSON file and extract relevant variable information.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict: Dictionary containing variable information.
    """
    with open(filepath) as f:
        data = json.load(f)

    variables = {}
    mipt = data['Header']["table_id"]
    for var in data['variable_entry'].values():
        var['mip_table'] = mipt

        try:
            name = var['out_name']
            # (var['out_name'], var['branded_variable_name'])
        except Exception as e:
            # Log and skip entries with missing or unexpected keys
            logging.warning(f"Error processing variable in {filepath}: {e}")
            continue

        if name not in variables:
            var['mip_table'] = mipt
            variables[name] = var
        else:
            # Log conflict for duplicate variables
            logging.warning(f"Variable conflict: {name}")
            raise KeyError(name)

    return variables


def clean(d, key_to_ignore):
    return {key: d[key] for key in d if key not in key_to_ignore}


def compare_dict(d1, d2, key_to_ignore):
    """
    Compare two dictionaries ignoring a specific key.

    Args:
        d1 (dict): First dictionary.
        d2 (dict): Second dictionary.
        key_to_ignore (list): Keys to ignore during the comparison.

    Returns:
        bool: True if the dictionaries are equal ignoring the specified key, False otherwise.
    """
    assert isinstance(key_to_ignore, list)

    # Create copies of the dictionaries without the ignored key
    filtered_d1 = clean(d1, key_to_ignore)
    filtered_d2 = clean(d2, key_to_ignore)

    # print('\n\n',filtered_d1.keys(),'\n', filtered_d2.keys())

    # Compare the filtered dictionaries
    return filtered_d1 == filtered_d2


def nest(dictionary_with_tuples):
    """
    Nest a dictionary with tuples as keys into a hierarchical dictionary.

    Args:
        dictionary_with_tuples (dict): Dictionary with tuples as keys.

    Returns:
        dict: Nested hierarchical dictionary.
    """
    nested_dict = {}
    for keys, value in dictionary_with_tuples.items():
        new = {keys[1]: value}
        if keys[0] in nested_dict:
            nested_dict[keys[0]].update(new)
        else:
            nested_dict[keys[0]] = new
    return nested_dict


if __name__ == '__main__':

    # Find all JSON files in the 'Tables' directory
    files = Path('../../Tables').glob('*.json')

    # Set up logging
    log_file_path = '../.logs/var_diff.log'
    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    # Configure logging to create a new log file
    logging.basicConfig(filename=log_file_path, level=logging.WARNING)

    with Pool() as pool:
        results = pool.map(process_file, files)



    merged = defaultdict(dict)
    for result in results:
        for name, var in result.items():


            # if 'provenance' not in merged[name]:
            # merged[name]['provenance'] = defaultdict(dict)

            
            if 'tables' not in var:
                var['tables'] = {}

            entry = {}
            for key in ['frequency', 'branded_variable_name', "modeling_realm", 'dimensions','validation','comment','provenance']:
                entry[key] = var[key]
            # del entry['variable_name']

            var['tables'][var['mip_table']]=dict(sorted(entry.items(),key=lambda x: (isinstance(x[1], (list, dict)), x[0])))

            if name in merged:
                # Check for conflicts in variable information, specifically in 'provenance' key
     
                if compare_dict(merged[name], var, ['tables','provenance', 'frequency', 'branded_variable_name', "modeling_realm", 'cell_measures', 'cell_methods', 'dimensions','comment','validation','mip_table']):
                    # dreq uid in provenances
                    # merged[name]['provenance'].append(var.get('provenance'))

                    # for MIP in var['tables']:
                    #     # merged[name]['provenance'][MIP][var['provenance'][entry['mip_table']]] = var['provenance'][MIP]
                    merged[name]['tables'].update(var['tables'])
                    # inefficient I know.. 
                    merged[name]['tables'] = dict(sorted(merged[name]['tables'].items()))
                    ...
                else:
                    # Log conflicts in variable information
                    logging.warning(
                        f"\n\nConflict for ** {name} **: \n{var} \n!= \n{merged[name]}")
            else:

                merged[name] = clean(var, ['frequency', 'branded_variable_name',
                                     "modeling_realm", 'cell_measures', 'cell_methods','dimensions','comment','validation','mip_table','provenance'])
                # merged[name]['dimensions'] = [
                #     tuple(merged[name]['dimensions'])]
            merged[name] = dict(sorted(merged[name].items(),key=lambda x: (isinstance(x[1], (list, dict)), x[0])))

    f,s,merged = up.prov(merged)
    logging.error(f)

            
    # Sort merged dictionary by key
    merged = dict(sorted(merged.items()))




    # Save the nested and merged variable information to a JSON file
    with open('../../MIP_variables.json', 'w') as f:
        json.dump(merged, f, indent=2)

    print(len(merged))



'''
preov cmip var list -> make the key the name 

'''