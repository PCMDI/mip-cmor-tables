from __setup__ import * 
lddata = cmipld.sync(lddata)

frame = {
        "@type": [
            "mip:institution",
            "mip:consortium"
        ],
        "@embed":"@always",
}
# cmipld.sync(lddata)
# await lddata

frame = cmipld.Frame(lddata,frame).clean(['rmld','untag'])
data = cmipld.utils.sorted_dict(frame.filterkeys(['cmip-acronym','name','ror'],True,'consortium').keyval('cmip-acronym'))



cmipld.utils.wjsn(data,base+'/MIP_organisations.json')