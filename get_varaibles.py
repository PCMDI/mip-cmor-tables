import json
import logging
import os
from pathlib import Path
from multiprocessing import Pool

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
    for var in data['variable_entry'].values():
        try:
            name = (var['out_name'], var['branded_variable_name'])
        except Exception as e:
            # Log and skip entries with missing or unexpected keys
            logging.warning(f"Error processing variable in {filepath}: {e}")
            continue

        if name not in variables:
            variables[tuple(name)] = var
        else:
            # Log conflict for duplicate variables
            logging.warning(f"Variable conflict: {name}")
    
    return variables

def compare_dict(d1, d2, key_to_ignore):
    """
    Compare two dictionaries ignoring a specific key.

    Args:
        d1 (dict): First dictionary.
        d2 (dict): Second dictionary.
        key_to_ignore (str): Key to ignore during the comparison.

    Returns:
        bool: True if the dictionaries are equal ignoring the specified key, False otherwise.
    """
    # Create copies of the dictionaries without the ignored key
    filtered_d1 = {key: d1[key] for key in d1 if key != key_to_ignore}
    filtered_d2 = {key: d2[key] for key in d2 if key != key_to_ignore}

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
    files = Path('./Tables').glob('*.json')

    # Set up logging
    log_file_path = '.logs/var_diff.log'
    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    # Configure logging to create a new log file
    logging.basicConfig(filename=log_file_path, level=logging.WARNING)

    with Pool() as pool:
        results = pool.map(process_file, files)

    merged = {}
    for result in results:
        for name, var in result.items():
            if name in merged:
                # Check for conflicts in variable information, specifically in 'provenance' key
                if compare_dict(merged[name], var, 'provenance'):
                    merged[name]['provenance'].append(var.get('provenance'))
                else:
                    # Log conflicts in variable information
                    logging.warning(f"\n\nConflict for ** {name} **: \n{var} \n!= \n{merged[name]}") 
            else:
                var['provenance'] = [var['provenance']]
                merged[name] = var

    # Sort merged dictionary by key 
    merged = dict(sorted(merged.items()))

    # Save the nested and merged variable information to a JSON file
    with open('Tables/Auxillary/variables.json', 'w') as f:
        json.dump(nest(merged), f, indent=2)
