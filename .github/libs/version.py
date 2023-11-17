import glob,os,sys,re,json
from collections import OrderedDict
import argparse
from urllib.request import Request, urlopen
from checksum_tools import validate_checksum,calculate_checksum


    ##########################################
    # load the maintainer file
    ##########################################

maintainers = json.load(open('.github/maintainer_institutes.json','r'))

    ##########################################
    # get repo information
    ##########################################

tag = os.popen("git describe --tags --abbrev=0").read().strip()
# release_date = subprocess.check_output(["git", "log", "-1", "--format=%aI", tag]).strip().decode("utf-8")

files = glob.glob('*.json')
files.extend(glob.glob('Auxillary_files/*.json'))

print('hi')
    ##########################################
    # read api keys
    ##########################################
parser = argparse.ArgumentParser(description="Retrieve details for the latest tag of a GitHub repository.")
parser.add_argument("-t","--tag" ,help="tag number")

args = parser.parse_args()


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

            # # Retrieve timestamp for the latest tag
            # tag_info_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/tags/{tag_name}"
            # request = Request(tag_info_url, headers=headers)
            # with urlopen(request) as response:
            #     tag_info = json.loads(response.read())
            # print(tag_info)
            # timestamp = ''
            # timestamp = tag_info['object']

            return {"tag_name": tag_name, "commit_sha": commit_sha}

    except Exception as e:
        print(f"Error: {e}")

    return None

CVs = get_latest_tag_info('WCRP-CMIP','CMIP6Plus_CVs',args.tag)


    ##########################################
    # iterate over all the files. 
    ##########################################
for f in files:


    contents = json.load(open(f,'r'))


    if 'version_metadata' not in contents:
        contents['version_metadata'] = dict(checksum='',commit='')



    if validate_checksum(contents):
        continue


    
    
    skip = 'Author: CMIP-IPO: Automated GitHub Action <actions@wcrp-cmip.org>'  
    # commit_info = os.popen(f'git log -n 1 -- {f} ').read()
    full = os.popen(f'git log -- {f} ').read()
    commit_blocks = re.split(r'\n(?=commit\s)', full)
    for c in commit_blocks:
        if skip not in c:
            commit_info = c
            break


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
            raise KeyError(f'Please add \n\t "{author_info[0]}": \n\t\t','{"institute": "", "published_name": "Name you wish to use"}')
        commit_dict["author_email"] = author_info[1][:-1]  

    if date_match:
        commit_dict["commit_date"] = date_match.group(1)

    if commit_message_match:
        commit_dict["commit_message"] = commit_message_match.group(1)


    ##########################################
    # create a new version metadata 
    ##########################################

    previous_commit = contents['version_metadata'].get('commit','')
    short = f.replace('.json','')

    template =  {"version_metadata":OrderedDict({

            "version_tag": tag,
            "checksum": 'checksum',
            
            f"{short}_modified":commit_dict['commit_date'],
            f"{short}_note":commit_dict['commit_message'],

            "commit":commit_dict['commit_sha'],
            "previous_commit":"",

            "author":commit_dict['author_name'],
            "institution_id":commit_dict['author_institute'],
            
            # "CV_collection_modified":CVs['timestamp'],
            "CV_collection_version":CVs['tag_name'],
            "specs_doc":"v6.5.0"

        })} 


    contents = OrderedDict(contents)
    del contents['version_metadata']
    contents['version_metadata'] = template

    print('writing',f)

    with open(f,'w') as write:
        write.write(json.dumps(contents,indent=4))


# checksum. If checksum is not the same, update.



'''
export PATH="${HOME}/Applications/Docker.app/Contents/Resources/bin:$PATH"

act -s GITHUB_TOKEN="$(gh auth token)" --container-architecture linux/amd64 -b & sleep 4 

'''
