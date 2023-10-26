from fuzzywuzzy import fuzz
      

import json 

load = lambda f: json.load(open(f,'r'))




def prov(vars):
    failed = []
    success = []

    # varf = '../../Auxillary/variables.json'
    # vars = load(varf)

    cmip6map = load('table_6_to_6plus.json')
    # for i in cmip6map: cmip6map[i].append(i)
    # allmap = [j for i in cmip6map.values() for j in i ]

    mp = dict([[vars[i]['standard_name'],i] for i in vars])

    for mip in [3,5]:
        mipdata = load('./cmip%dvariables.json'%mip)
        MIP = 'CMIP%s'%mip
        for table in mipdata:
            fd=[]
            if table in cmip6map:

                for var in mipdata[table]:
                    v2 = mipdata[table][var]
                    if 'standard_name' in v2 and v2['standard_name'] in mp:
                        newprov = {MIP:{'mip_table': table, 'variable_name': var}}
                        possible = None
                        for possible in cmip6map[table]:
                            try:

                                if fuzz.ratio(var,vars[mp[v2['standard_name']]]['tables'][possible]['provenance']['CMIP6']['variable_name']) > 70 :

                                    
                                    vars[mp[v2['standard_name']]]['tables'][possible]['provenance'].update(newprov)


                                    # Make sure that the variables are atleast similar


                                    # print(fuzz.ratio(var,vars[mp[v2['standard_name']]]['tables'][possible]['provenance']['CMIP6']['variable_name']) ,var,vars[mp[v2['standard_name']]]['tables'][possible]['provenance']['CMIP6']['variable_name'])
                                    
                                    success.append(vars[mp[v2['standard_name']]])

                            except Exception as e:
                                pass

                            
                        if (success) and (success[-1] != vars[mp[v2['standard_name']]]):
                            fd.append(var)
                            

                if fd:
                    failed.append(['No table entry in "tables" (table exists otherwise)',MIP,table,fd])

            else:
                failed.append(['No table entry in cmip6',MIP,table,'--all vars--'])
        
                        

    return str(failed),str(success),vars
