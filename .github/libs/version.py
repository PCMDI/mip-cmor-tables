import glob
import os
import sys
import re
import json
from collections import OrderedDict
from urllib.request import Request, urlopen
from checksum_tools import validate_checksum, calculate_checksum
from datetime import datetime
import argparse

##########################################
# load the maintainer file
##########################################

maintainers = json.load(open('.github/maintainer_institutes.json', 'r'))
##########################################
# get repo information
##########################################
tag = os.popen("git describe --tags --abbrev=0").read().strip()
# release_date = subprocess.check_output(["git", "log", "-1", "--format=%aI", tag]).strip().decode("utf-8")


##########################################
# Get the Tag information from the CVs
##########################################
def get_latest_tag_info(repo_owner, repo_name, github_token=None):
    tags_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/tags"
    headers = {"Authorization": f"Bearer {github_token}"} if github_token else {}

    try:
        # Get the list of tags
        request = Request(tags_url, headers=headers)
        with urlopen(request) as response:
            tags_data = json.loads(response.read())

        if tags_data:
            # Select the latest tag
            latest_tag = tags_data[0]
            tag_name = latest_tag['name']
            commit_sha = latest_tag['commit']['sha']

            return {"tag_name": tag_name, "commit_sha": commit_sha}

    except Exception as e:
        print(f"Error: {e}")

    return None


def process_files(files,token = None, branch=None,force=False):
    CVs = get_latest_tag_info('WCRP-CMIP', 'CMIP6Plus_CVs', token)

    for f in files:
        print(f)
        contents = json.load(open(f, 'r'))

        if 'version_metadata' not in contents:
            contents['version_metadata'] = dict(checksum='', commit='')


        # this now has a different setup due to CVs.  
        # if validate_checksum(contents):
        #     print(f,'checksum the same')
        #     continue
            

        skip = 'CMIP-IPO: Automated GitHub Action <actions@wcrp-cmip.org>'  
        # commit_info = os.popen(f'git log -n 1 -- {f} ').read()
        full = os.popen(f'git log -- {f} ').read()


        previous_commit = ''
        commit_info = False
        
        

        commit_blocks = re.split(r'\n(?=commit\s)', full)
        for c in commit_blocks:
            if 'reset-checksum' in c:
                continue
            if 'Automated Versioning Update' in c:
                continue
            if skip not in c:
                if not commit_info:
                    commit_info = c
                elif commit_info and not previous_commit:
                    previous_commit = re.search(r"commit (\S+)", c)
                    break

        if 'commit_info' not in locals():
            print(f)
            print(commit_blocks)
            print('no suitable commit found')
            sys.exit('no suitable commit found')


        ##########################################
        # extract commit info
        ##########################################

        commit_dict = {}

        # Extract information using regular expressions
        commit_match = re.search(r"commit (\S+)", commit_info)
        author_match = re.search(r"Author: (.+)", commit_info)
        date_match = re.search(r"Date: (.+)", commit_info)
        commit_message_match = re.search(r"    (.+)", commit_info)

        if commit_match:
            commit_dict["commit_sha"] = commit_match.group(1)

        if author_match:
            author_info = author_match.group(1).split(" <")
            commit_dict["author_name"] = author_info[0]
            try:
                commit_dict["author_institute"] = maintainers[author_info[0]]['institute']
                commit_dict["author_name"] = maintainers[author_info[0]]['published_name']
            except:
                commit_dict["author_name"] = author_match.group(1)
                
                print( f'Please add \n\t "{author_info[0]}": \n\t\t','{"institute": "", "published_name": "Name you wish to use"}')
                # this was a keyerror
                
            commit_dict["author_email"] = author_info[1][:-1]  

        if date_match:
            commit_dict["commit_date"] = date_match.group(1)

        if commit_message_match:
            commit_dict["commit_message"] = commit_message_match.group(1)



        ##########################################
        # create a new version metadata
        ##########################################

        short = f.replace('.json','')
        
        try:
            old_checksum = contents['version_metadata']['checksum'] 
        except:
            old_checksum = ''
            
        template =  OrderedDict({
            "version_tag": tag,
            "checksum": 'checksum',
            f"{short}_modified": commit_dict.get('commit_date','new file').lstrip(),
            f"{short}_note": commit_dict.get('commit_message','no previous commit'),
            "commit": commit_dict.get('commit_sha', 'none'),
            "previous_commit": "",
            "author": commit_dict.get('author_name', 'CMIP-IPO'),
            "institution_id": commit_dict.get('author_institute', 'CMIP-IPO'),
            "CV_collection_version": CVs['tag_name'],
            "specs_doc": "v6.5.0"
        })

        contents = OrderedDict(contents)
        del contents['version_metadata']
        contents['version_metadata'] = template

        contents = calculate_checksum(contents,update=True)

        # print('writing', f)

        if old_checksum != contents['version_metadata']['checksum'] or force:

            with open(f, 'w') as write:
                write.write(json.dumps(contents, indent=4))
                
                import pprint
                pprint.pprint(contents['version_metadata'])

            ##########################################
            # keep the individualized commit messages
            ##########################################
            
            print(author_match.group(1),f)
            print(commit_dict['commit_message'])

            # os.popen(f"git add {f}").read()

            # os.popen(f'git commit --author="{author_match.group(1)}" -m "{commit_dict["commit_message"]}"').read()
            
    # os.popen('git push').read()

    

if __name__ == "__main__":
    files = glob.glob('*.json')
    files.extend(glob.glob('Auxillary_files/*.json'))

    parser = argparse.ArgumentParser(description="Retrieve details for the latest tag of a GitHub repository.")
    parser.add_argument("-t", "--token", help="gh token")
    parser.add_argument("-b","--branch" ,help="branch name")

    args = parser.parse_args()

    process_files(files, token=args.token, branch = args.branch)
