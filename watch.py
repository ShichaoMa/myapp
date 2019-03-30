import os
import glob
video = glob.glob("*.mp4")
os.system("mkdir -p good/")
for v in video:
    os.system("open '%s'" % v)
    flag = input("是否删除？")
    if flag in ["y", "yes"]:
        os.system("mv '%s' 'default/%s'" % (v, v))
    elif flag == "d":
        os.system("rm '%s'" % v)
    elif flag == "p":
        pass
    else:
        os.system("mv '%s' 'good/%s'" % (v, v))

