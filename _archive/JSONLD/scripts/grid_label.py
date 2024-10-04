from __setup__ import * 

lddata = cmipld.sync(lddata)

name = 'grid_label'

frame = {
        "@type": [
            f"mip:{name.replace('_','-')}", 
        ],
        "@embed":"@always",
}


frame = cmipld.Frame(lddata,frame).clean(['rmld','untag'])

data = cmipld.utils.sorted_dict(frame.key_value('name','description'))


cmipld.utils.wjsn(finalise(data,name),base+f'/MIP_{name}.json')