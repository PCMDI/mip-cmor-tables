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

data = sorted(list(frame.keystr('name','description').keys()))


cmipld.utils.wjsn(finalise(data,name),base+f'/MIP_{name}.json')