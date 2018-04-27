# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os
import re

def DisposeOrignalFile():
    pathHead="E:\\医疗保险语料"
    txtpath="E:\\MedicareCorpus"
    pathdirs=os.listdir(pathHead)
    # print(pathdirs)
    k=1
    filedir=[]
    for dir in pathdirs:
        pathdir=pathHead+"\\"+str(dir)
        # print(pathdir)
        filedirs=os.listdir(pathdir)
        # print(filedirs)
        for files in filedirs:
            filedir.append(pathdir+"\\"+files)
    print(filedir)
    for file in filedir:
        try:
            f=open(file,'r',encoding='utf-8')
            bsobj=BeautifulSoup(f,"html.parser")
            #打开临时文件
            p=txtpath+"\\tempfile.txt"
            fileobject=open(p,'w',encoding='utf-8')
            fileobject.write(bsobj.text)
            fileobject.close()
            fileobject = open(p, 'r', encoding='utf-8')
            #清洗临时文件并写入最终文件
            fpath = txtpath + "\\" + str(k) + ".txt"
            finalfile = open(fpath, 'w', encoding='utf-8')
            for line in fileobject.readlines():
                data = line.strip()
                if len(data) != 0:
                    finalfile.write(data + '\n')
        except UnicodeDecodeError:
            print(file+"解析失败")
            continue
        fileobject.close()
        k=k+1
        f.close()
        finalfile.close()

def CleanSentence(sentence):
    """
    对句子进行清洗
    :param sentence: 待清洗的句子
    :return:
    """
    pattern = [r'第.*(条|章)', r'（[0-9]{1,2}）', r'（(一|二|三|四|五|六|七|八|九|十)*）', r'[0-9]{1,2}(\．|\.)']
    for p in pattern:
        sentence = re.sub(p, '', sentence)
    # print(sentence)
    return sentence

def Dictionary():
    file = open('E:\\医疗保险语料库\\领域词典.txt', 'r', encoding='utf-8')
    words = set()
    for line in file.readlines():
        words.add(line)
    file.close()
    file2 = open('E:\\医疗保险语料库\\领域词典.txt', 'w', encoding='utf-8')
    for w in words:
        s = w.strip('\n')+ ' n'+ '\n'
        print(s)
        file2.write(s)
    file2.close()

# file = open('E:\\医疗保险语料库\\报错内容.txt', 'r', encoding='utf-8')
# t = False
# g = []
# for l in file.readlines():
#     g.append(l.strip('\n'))
# ans = []
# for i in range(0, len(g), 2):
#     print(i)
#     ans.append(g[i].strip('正在处理'))
# with open('./待处理文件.txt', 'w', encoding='utf-8') as f:
#     for a in ans:
#         f.write(a + '\n')

# filepath = 'E:\\MedicareCorpus\\'
# efilepath = 'E:\\实体抽取\\'
# outpath = 'E:\\医疗保险语料待解析\\'
# files = os.listdir(filepath)

# for file in files:
#     print(file)
#     entities = []
#     foj = open(filepath + file, 'r', encoding = 'utf-8')
#     efoj = open(efilepath + file, 'r', encoding = 'utf-8')
#     for e in efoj.readlines():
#         entities.append(e.strip('\n'))
#     sentences = []
#     for line in foj.readlines():
#         for e in entities:
#             if line.find(e) != -1:
#                 line = CleanSentence(line)
#                 line = line.strip()
#                 sentences.append(line.strip('\n'))
#                 break
#     with open(outpath + file, 'w', encoding='utf-8') as f:
#         for s in sentences:
#             f.write(s + '\n')
#     foj.close()
#     efoj.close()
# files2 = os.listdir(outpath)
# l = []
# for file in files2:
#     print(file)
#     l.append(file)
#     foj = open(outpath + file, 'r', encoding='utf-8')
#     l.append(foj.readline(30))
#     foj.close()
# with open('./line.txt', 'w', encoding='utf-8') as f:
#     for ll in l:
#         f.write(ll+'\n')