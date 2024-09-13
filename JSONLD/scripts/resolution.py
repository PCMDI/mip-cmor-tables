from __setup__ import * 

lddata = cmipld.sync(lddata)

name = 'nominal_resolution'

frame = {
        "@type": [
            f"mip:resolution", 
        ],
        "@embed":"@always",
}


frame = cmipld.Frame(lddata,frame).clean(['rmld','untag'])

data = frame.key_value('name','description')


cmipld.utils.wjsn(finalise(data,name),base+f'/MIP_{name}.json')