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

import asyncio,aiofiles
import glob
import os
import json
import argparse
from typing import List, Dict, Any, Tuple

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

async def categorize_files(directory: str, skip_files: List[str], skip_dirs: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Categorize JSON-LD files in the given directory into graph, context, and version categories.

    :param directory: Root directory to start traversal
    :param skip_files: List of file names to skip
    :param skip_dirs: List of directory names to skip
    :return: Dictionary containing graph, context, and version data
    """
    combined = []
    vcollection = []

    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        # Skip excluded files
        files = [f for f in files if f.endswith('.json') and f not in skip_files]
        files.sort()

        print('>>> ',root)

        
        if 'frame.json' in files:
            files.remove("frame.json")

            # Process JSON files in this directory
            graph_files = [os.path.join(root, file) for file in files]
            graph_data = await read_json_files(graph_files)

            complete_graph = {
                "@id": root.replace('../', REPO),
                "@type": "cmip:graph",
                "ldroot": root[1:],
                "@graph": graph_data,
                "files": files
            }

            combined.append(complete_graph)
            json.dump(complete_graph, open(f"{root}/graph.json", 'w'), indent=4)

            # Create version file
            location = root.replace('../', REPO + "/blob/main/")
            version = [await githistory(f, root, False, location) for f in files]
            tasks = [githistory(f, root, False, location) for f in files]
            version = await asyncio.gather(*tasks)
            json.dump(version, open(f"{root}/version.json", 'w'), indent=4)

            vcollection.extend(version)

    return {'graph': combined, 'version': vcollection}

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
    group_types = set(entry.get('@type', 'Unknown') for entry in lddata['graph'])
    for group_type in group_types:
        print(group_type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CMIP6Plus JSON-LD files.")
    parser.add_argument("--exclude-dirs", type=str, help="Comma-separated list of directories to exclude")
    parser.add_argument("--exclude-files", type=str, help="Comma-separated list of files to exclude")
    args = parser.parse_args()

    exclude_dirs = args.exclude_dirs.split(',') if args.exclude_dirs else []
    exclude_files = args.exclude_files.split(',') if args.exclude_files else []

    asyncio.run(main(exclude_dirs, exclude_files))