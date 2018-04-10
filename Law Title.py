import os
import re

pathHead="E:\\医疗保险测试语料库\\"
outpath='E:\\规则抽取法律\\'
pathdirs=os.listdir(pathHead)

lawtitle=set()
pattern = re.compile(r'《[^《》]*》')
for path in pathdirs:
    in_file = pathHead+path
    inputfile = open(in_file,'r',encoding='utf-8')
    for line in inputfile.readlines():
        names = pattern.findall(line)
        if len(names) != 0:
            for name in names:
                lawtitle.add(name)
    out_file = outpath+path
    outputfile = open(out_file,'a',encoding='utf-8')
    for name in lawtitle:
        outputfile.write(name+'\n')
    outputfile.close()
    lawtitle.clear()

