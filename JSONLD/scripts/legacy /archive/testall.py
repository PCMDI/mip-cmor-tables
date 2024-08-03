import pyld
from p_tqdm import p_map
import json 
import glob

def jldtest(file):
    js = json.load(open(file))
    try:
        pyld.jsonld.expand(js)
    except Exception as e: 
        print('--failed--',file, e)
        
        
files  = glob.glob('../miptables/tables/*.json')
# print(files)


p_map(jldtest,files)
