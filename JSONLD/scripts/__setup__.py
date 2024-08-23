import cmipld
import cmipld.utils.git
base = cmipld.utils.git.toplevel()

print(base)

lddata = cmipld.CMIPFileUtils.load([base + '/compiled/graph_data.min.json'])


#  cmipld.sync(lddata)

