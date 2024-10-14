
from pathlib import Path
import json
import os
from pprint import pp
# run it (working dir) from root dir
input_terms_directory = Path("_archive/JSONLD/organisations/consortia/")
output_terms_directory = Path("datadescriptor/consortia/")

# Create the directory if it doesn't exist
os.makedirs(output_terms_directory, exist_ok=True)


terms_file_list = [p for p in input_terms_directory.iterdir() if (p.is_file() and "jsonld" not in str(p) and "txt" not in str(p) )]
#print(flist)

for p in terms_file_list:
    with open(p,"r") as input_file:
        input_term = json.load(input_file)
    
    #pp(input_term["members"])
    # what to change : 
    # add link to context 
    # id => remove @ + to get uri right => point to URI server
    # type => remove @
    output_term = input_term.copy()

    output_term["@context"] = "000_context.jsonld"
    output_term["id"] = output_term["@id"].split('/')[-1]
    output_term.pop("@id")


    #output_term.pop("type") # double definition in input for type and @type => remove type before redefine
    output_term["type"]  = input_term["@type"]
    output_term.pop("@type")

    output_term["members"] = []
    for item in input_term["members"]:
        member ={
            
            "type" : "member",
            "institution" : item["institution"]["@id"].split("/")[-1],
            "dates" : item["dates"]
        }
        for it in member["dates"]:
            #pp(it["phase"])
            if type(it["phase"])==dict:
                it["phase"] = it["phase"]["@id"].split("/")[-1].lower()
            else:
                it["phase"] = it["phase"].lower() # to get the id
        if "consortia:membership-type" in item:
            member["membership_type"] = item["consortia:membership-type"]
        else:
            member["membership_type"] = item["membership-type"]
        
        output_term["members"].append(member) 


    ordered_output_term = {
        "@context" : output_term["@context"],
        "id" : output_term["id"],
        "type" : output_term["type"]

    } 

    for k,v in output_term.items():
        if k not in ordered_output_term:
            ordered_output_term[k]=v

    #pp(ordered_output_term)
    #pp(input_term)
    '''
    if "consortia:status" in input_term and input_term["consortia:status"] not in knowntype:
        knowntype.append(input_term["consortia:status"])
    '''


    '''
    if "members" in input_term:
        for item in input_term["members"]:
            if "membership-type" in item:
                if item["membership-type"] not in knowntype:
                    knowntype.append(item["membership-type"])
            if "consortia:membership-type" in item:
                if item["consortia:membership-type"] not in knowntype:
                    knowntype.append(item["consortia:membership-type"])
    if "consortium:members" in input_term:
        print("COUCOU")
        for item in input_term["consortium:members"]["@set"]:
            print("OLA")
            if "membership-type" in item:
                if item["membership-type"] not in knowntype:
                    knowntype.append(item["membership-type"])
            if "consortia:membership-type" in item:
                if item["consortia:membership-type"] not in knowntype:
                    knowntype.append(item["consortia:membership-type"])
    '''

    
    with open(f"{str(output_terms_directory)}/{ordered_output_term['id']}.json", "w") as outfile: 
        json.dump(ordered_output_term, outfile,indent=4)
    
    #pp(ordered_output_term)


# TERMS to be reviewed 

pp("TO BE REVIEWED")
input_terms_directory = Path("_archive/JSONLD/organisations/consortia/forReview")

# Create the directory if it doesn't exist
os.makedirs(output_terms_directory, exist_ok=True)


terms_file_list = [p for p in input_terms_directory.iterdir() if (p.is_file() and "jsonld" not in str(p) and "txt" not in str(p) )]
#print(flist)

for p in terms_file_list:
    with open(p,"r") as input_file:
        input_term = json.load(input_file)
    
    # what to change : 
    # add link to context 
    # id => remove @ + to get uri right => point to URI server
    # type => remove @
    output_term = input_term.copy()

    output_term["@context"] = "000_context.jsonld"
    output_term["id"] = output_term["@id"].split('/')[-1]
    output_term.pop("@id")


    #output_term.pop("type") # double definition in input for type and @type => remove type before redefine
    output_term["type"]  = input_term["@type"]
    output_term.pop("@type")
    
   
    for k,v in input_term.items():
        if len(k.split(":"))==2:
            kp, ks = k.split(":")
            print(kp,ks)
            output_term[ks] = input_term[k]
            output_term.pop(k)

    output_term["members"] = []
    for item in input_term["consortium:members"]["@set"]:
        member ={
            
            "type" : "member",
            "institution" : item["consortia:institution"]["@id"].split("/")[-1],
            "dates" : item["consortia:dates"]
        }
        for it in member["dates"]:
            if type(it["phase"])==dict:
                it["phase"] = it["phase"]["@id"].split("/")[-1].lower()
            else:
                it["phase"] = it["phase"].lower() # to get the id
        if "consortia:membership-type" in item:
            member["membership_type"] = item["consortia:membership-type"]
        else:
            member["membership_type"] = item["membership-type"]
        
        output_term["members"].append(member) 


    ordered_output_term = {
        "@context" : output_term["@context"],
        "id" : output_term["id"],
        "type" : output_term["type"]

    } 

    for k,v in output_term.items():
        if k not in ordered_output_term:
            ordered_output_term[k]=v

    #pp(ordered_output_term)
    #pp(input_term)
    '''
    if "consortia:status" in input_term and input_term["consortia:status"] not in knowntype:
        knowntype.append(input_term["consortia:status"])
    '''


    '''
    if "members" in input_term:
        for item in input_term["members"]:
            if "membership-type" in item:
                if item["membership-type"] not in knowntype:
                    knowntype.append(item["membership-type"])
            if "consortia:membership-type" in item:
                if item["consortia:membership-type"] not in knowntype:
                    knowntype.append(item["consortia:membership-type"])
    if "consortium:members" in input_term:
        print("COUCOU")
        for item in input_term["consortium:members"]["@set"]:
            print("OLA")
            if "membership-type" in item:
                if item["membership-type"] not in knowntype:
                    knowntype.append(item["membership-type"])
            if "consortia:membership-type" in item:
                if item["consortia:membership-type"] not in knowntype:
                    knowntype.append(item["consortia:membership-type"])
    '''

    
    with open(f"{str(output_terms_directory)}/_{ordered_output_term['id']}.json", "w") as outfile: 
        json.dump(ordered_output_term, outfile,indent=4)
    
    pp(ordered_output_term)
