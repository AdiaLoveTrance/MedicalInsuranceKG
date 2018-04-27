# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from bosonnlp import BosonNLP
import os
import re

nlp = BosonNLP('YGrN2PDi.22096.Qp-06MnNaWED')

def ExtOrg(wordlist,taglist,filepath):
    centretag = ['#nr', '#ns', '#nt', '#m', '#nz', '#t']
    centreword = ['机构', '部门', '局', '管理局', '站', '服务站', '中心', '保险', '对象', '基金', '费用', '资金', '公司', '人群', '人员', '保险费']
    relist = [r'(#n)+(#b|z)*', r'(#n)+(#an|#nz)?', r'(#n)+', r'(#n)+', r'#n#an(#n)+', r'#n#an(#n)+', r'(#n)+(#an)?(#n)*', r'(#n)+(#a(#n)*)?', r'(#n)+(#a(#n)*)?', r'(#n)+(#a)?(#n)+', r'(#n)+(#a|#b)?', r'(#n)+(#a)?', r'(#n)+', r'(#n)+(#a)?(#n)?', r'(#n)+((#b)+|(#a)*|#an(#n)+)', r'(#n)+(#v|#a(#n)+)']
    entities = set()
    for it1, it2 in zip(wordlist, taglist):
        if it2 in centretag:
            entities.add(it1)
    # for k in range(0,len(centreword)):
    for i in range(0, len(wordlist)):
        for k in range(0, len(centreword)):
            if wordlist[i] == centreword[k]:
                s = ''
                w = []
                for j in range(i, i - 10, -1):
                    s = s + taglist[j]
                    w.append(wordlist[j])
                # print(s)
                pattern = re.compile(relist[k])
                m = pattern.match(s)
                # print(m)
                if m:
                    cm = m.group()
                    n = cm.count('#')
                    str = ''
                    for l in range(n - 1, -1, -1):
                        str = str + w[l]
                    # print(str)
                    entities.add(str)
    file = open(filepath,'w',encoding='utf-8')
    for en in entities:
        file.write(en+'\n')
    file.close()


def ExtEntity(in_file,out_file):
    inputfile = open(in_file,'r',encoding='utf-8')
    input = inputfile.read()
    result = nlp.tag(input)
    wordlist = []
    taglist = []
    for d in result:
        for it1,it2 in zip(d['word'],d['tag']):
            wordlist.append(it1)
            taglist.append('#'+it2)     #标注的词性前加#号
    ExtOrg(wordlist,taglist,out_file)


in_filepath = 'E:\\MedicareCorpus\\'
out_filepath = 'E:\\实体抽取带数字版本\\'
in_files = os.listdir(in_filepath)
# ffiles = os.listdir(out_filepath)
# files = []
# for f in in_files:
#     if f not in ffiles:
#         files.append(f)
# print(files)
for file in in_files:
    in_file = in_filepath + file    #输入文件路径
    out_file = out_filepath + file  #输出文件路径
    print(file)
    ExtEntity(in_file,out_file)
# for file in files:
#     in_file = in_filepath + file    #输入文件路径
#     out_file = out_filepath + file  #输出文件路径
#     print(file)
#     ExtEntity(in_file,out_file)












