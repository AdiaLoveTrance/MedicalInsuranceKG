# -*- coding: utf-8 -*-
from pyltp import SentenceSplitter
from bs4 import BeautifulSoup
import os

filepath0 = 'E:\\医疗保险语料库\\医疗保险语料原文\\'
outpath = 'E:\\MedicareCorpus\\'
filepath1 = os.listdir(filepath0)
files = []
for path in filepath1:
    fp = filepath0 + path
    f = os.listdir(fp)
    for fi in f:
        files.append(fp + '\\' + fi)
k = 1

#分句函数
def sentence_splitter(sentence):
    sents = SentenceSplitter.split(sentence)
    sents_list = list(sents)
    return sents_list

# inputpath="E:\\MedicareCorpus"
# outputpath="E:\\医疗保险语料"
# k=1
# inputfiles=os.listdir(inputpath)
# print(inputfiles)
# for file in inputfiles:
#     #打开待分句文件
#     fname=inputpath+"\\"+file
#     f=open(fname,'r',encoding='utf-8')
#     #打开输出文件
#     opath=outputpath+"\\"+str(k)+".txt"
#     outputfile=open(opath,'w',encoding='utf-8')
#     for line in f.readlines():
#         sents=sentence_splitter(line)
#         for sent in sents:
#             if len(sent)>1:
#                 outputfile.write(sent+'\n')
#     f.close()
#     outputfile.close()
#     k=k+1

for file in files:
    try:
        fobj = open(file, 'r', encoding='utf-8')
        bsobj = BeautifulSoup(fobj.read(), "lxml")
        s = bsobj.text
        slist = sentence_splitter(s)
        outfile = outpath + str(k) + '.txt'
        with open(outfile, 'w', encoding='utf-8') as f:
            for ss in slist:
                if len(ss) > 1:
                    ss = ss.strip()
                    ss = ss.strip('\n')
                    f.write(ss + '\n')
        k += 1
    except UnicodeDecodeError:
        print(file)







