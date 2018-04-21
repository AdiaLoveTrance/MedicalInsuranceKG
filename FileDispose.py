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

CleanSentence('1．第一、二档次')

