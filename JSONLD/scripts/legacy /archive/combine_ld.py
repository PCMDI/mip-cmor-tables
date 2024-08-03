"""
CMIP6Plus JSON-LD File Extractor and Organizer

This script traverses through a directory structure, processes JSON-LD files, and organizes
them into graph, context, and version categories. It supports parallel execution for faster
processing and allows exclusion of specific directories and files.

Key Features:
- Asynchronous file reading and Git history retrieval
- Parallel execution using asyncio
- Customizable file and directory exclusion
- Generation of graph, context, and version data
- Minified JSON output for efficient storage

Dependencies:
- asyncio: For asynchronous operations
- json: For JSON parsing and serialization
- glob: For file pattern matching
- os: For file and directory operations

Usage:
python cmip6plus_jsonld_extractor.py [--exclude-dirs DIR1,DIR2] [--exclude-files FILE1,FILE2]
"""

import asyncio
import aiofiles
import glob
import os
import shlex,subprocess
import json
import argparse
from typing import List, Dict, Any, Tuple
from p_tqdm import p_map

# Constants
SHORTHAND = "mip-cmor-tables:"
REPO = os.popen('git remote get-url origin').read().replace('.git','/blob/main/JSONLD/').strip()
CVTAG = os.popen("curl -s https://api.github.com/repos/WCRP-CMIP/CMIP6Plus_CVs/tags| jq -r '.[0].name'").read().strip()
MIPTAG = os.popen("curl -s https://api.github.com/repos/PCMDI/mip-cmor-tables/tags| jq -r '.[0].name'").read().strip()

# Default exclusions
DEFAULT_SKIP_FILES = ['schema.json', 'graph.json', ".DS_Store", "create.ipynb", "version.json"]
DEFAULT_SKIP_DIRS = ['.git', '__pycache__','archive']

async def githistory(file: str, root: str, rstr: bool = True, location: str = '') -> Dict[str, Any] | str:
    """Retrieve Git history information for a given file."""
    update = {}
    
    # Use a raw string (r'...') to handle escapes in the Git command
    # Use f-string only for the file and root variables
    cmd = rf"""git log -n 1 --pretty=format:'{{
        "version:date": "%cd",
        "version:commit": {{
            "hash": "%h",
            "message": "%s",
            "author": {{
                "name": "%an",
                "email": "%ae"
            }}
        }}
    }}' --date=iso-strict -- {root}/{file}"""
    
    rtn = os.popen(cmd).read()
    ncommits = int(os.popen(f'git log --oneline -- "{root}/{file}" | wc -l').read().strip() or 0)

    if rtn:
        # Strip any leading/trailing whitespace and newlines
        rtn = rtn.strip()
        try:
            update = json.loads(rtn)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from git log for {file}: {rtn}")

    if rstr:
        return f'{file.ljust(30)} - {update.get("version:date", "Unknown date")}'
    else:
        return {
            "@id": f'{location}/{file}',
            "@type": "version",
            "version:file": file,
            "version:release": {"mip-cmor-tables": MIPTAG, "cmip6plus": CVTAG},
            "version:previous_updates": ncommits,
            **update,
            "version:data": {"@id": f"{root.replace('../', SHORTHAND)}/{file.rstrip('.json')}"}
        }

async def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    Asynchronously read a JSON file.

    :param file_path: Path to the JSON file
    :return: Parsed JSON content as a dictionary
    """
    async with aiofiles.open(file_path, mode='r') as f:
        content = await f.read()
        return json.loads(content)

async def read_json_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Asynchronously read multiple JSON files.

    :param file_paths: List of paths to JSON files
    :return: List of parsed JSON contents as dictionaries
    """
    tasks = [read_json_file(file_path) for file_path in file_paths]
    return await asyncio.gather(*tasks)



def safe_git_log(root: str, file: str) -> Dict[str, Any]:
    """
    Safely execute git log command and parse its output.

    :param root: Directory root
    :param file: File name
    :return: Git log information as a dictionary
    """
    cmd = rf'git log -n 1 --pretty=format:\'{{"version:date":"%cd","version:commit":{{"hash":"%h","message":"%s","author":{{"name":"%an","email":"%ae"}}}}}}\' --date=iso-strict -- "{os.path.join(root, file)}"'
    
    # Use shlex to properly handle command-line arguments
    args = shlex.split(cmd)
    
    try:
        output = subprocess.check_output(args, universal_newlines=True)
        if output:
            return json.loads(output)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Error processing {file} in {root}: {e}")
    
    # Return a default dictionary if there's an error
    return {
        "version:date": "Unknown",
        "version:commit": {
            "hash": "Unknown",
            "message": "Error retrieving Git history",
            "author": {
                "name": "Unknown",
                "email": "Unknown"
            }
        }
    }

def process_directory(args: Tuple[str, List[str], List[str], List[str], List[str]]) -> Dict[str, Any]:
    """
    Process a single directory, handling its JSON-LD files.

    :param args: Tuple containing (root, dirs, files, skip_files, skip_dirs)
    :return: Dictionary with graph and version data for this directory
    """
    root, dirs, files, skip_files, skip_dirs = args

    # Skip excluded directories
    dirs[:] = [d for d in dirs if d not in skip_dirs]

    # Skip excluded files
    files = [f for f in files if f.endswith('.json') and f not in skip_files]
    files.sort()

    

    if 'frame.json' in files:
        files.remove("frame.json")

        # Process JSON files in this directory
        graph_files = [os.path.join(root, file) for file in files]
        graph_data = [json.load(open(file)) for file in graph_files]  # Synchronous for now

        complete_graph = {
            "@id": root.replace('../', REPO),
            "@type": "cmip:graph",
            "ldroot": root[1:],
            "@graph": graph_data,
            "files": files
        }

        json.dump(complete_graph, open(f"{root}/graph.json", 'w'), indent=4)

        # Create version file
        location = root.replace('../', REPO + "/blob/main/")
        version = []

        for f in files:
            git_info = safe_git_log(root, f)
            v = {
                "@id": f'{location}/{f}',
                "@type": "version",
                "version:file": f,
                "version:release": {"mip-cmor-tables": MIPTAG, "cmip6plus": CVTAG},
                "version:previous_updates": 0,  # We'll update this later
                **git_info,
                "version:data": {"@id": f"{root.replace('../', SHORTHAND)}/{f.rstrip('.json')}"}
            }

            try:
                v["version:previous_updates"] = int(subprocess.check_output(shlex.split(f'git log --oneline -- "{os.path.join(root, f)}" | wc -l'), universal_newlines=True).strip() or 0)
            except subprocess.CalledProcessError:
                print(f"Error counting commits for {f} in {root}")

            version.append(v)
            
        print('>>> ', root)
        json.dump(version, open(f"{root}/version.json", 'w'), indent=4)

        return {'graph': complete_graph, 'version': version}
    
    return {'graph': None, 'version': None}
    
async def categorize_files(directory: str, skip_files: List[str], skip_dirs: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Categorize JSON-LD files in the given directory into graph and version categories.

    :param directory: Root directory to start traversal
    :param skip_files: List of file names to skip
    :param skip_dirs: List of directory names to skip
    :return: Dictionary containing graph and version data
    """
    combined_graphs = {}
    vcollection = []

    directory_info = [(root, dirs, files, skip_files, skip_dirs) for root, dirs, files in os.walk(directory)]
    
    # Use p_map for parallel processing
    results = p_map(process_directory, directory_info)

    for id,result in enumerate(results):
        if result['graph']:
            combined_graphs[id] = result['graph']
        if result['version']:
            vcollection.extend(result['version'])

    return {'graph': combined_graphs, 'version': vcollection}

async def main(exclude_dirs: List[str], exclude_files: List[str]):
    """
    Main function to orchestrate the JSON-LD file processing.

    :param exclude_dirs: List of directories to exclude
    :param exclude_files: List of files to exclude
    """
    skip_files = DEFAULT_SKIP_FILES + exclude_files
    skip_dirs = DEFAULT_SKIP_DIRS + exclude_dirs

    lddata = await categorize_files('../', skip_files, skip_dirs)

    # Save full and minified JSON outputs
    json.dump(lddata['graph'], open('graph_data.json', 'w'), indent=4)
    json.dump(lddata['graph'], open('graph_data.min.json', 'w'), separators=(',', ':'))
    json.dump(lddata['version'], open('version.min.json', 'w'), separators=(',', ':'))

    # Print unique group types for analysis
    # group_types = set(entry.get('@type', 'Unknown') for entry in lddata['graph'])
    # for group_type in group_types:
    #     print(group_type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CMIP6Plus JSON-LD files.")
    parser.add_argument("--exclude-dirs", type=str, help="Comma-separated list of directories to exclude")
    parser.add_argument("--exclude-files", type=str, help="Comma-separated list of files to exclude")
    args = parser.parse_args()

    exclude_dirs = args.exclude_dirs.split(',') if args.exclude_dirs else []
    exclude_files = args.exclude_files.split(',') if args.exclude_files else []

    asyncio.run(main(exclude_dirs, exclude_files))