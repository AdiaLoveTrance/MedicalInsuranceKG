# -*- coding: utf-8 -*-
from pyltp import SentenceSplitter
from bs4 import BeautifulSoup
import os
import re
import csv,operator
from pypinyin import lazy_pinyin


def DisposeOrignalFile():
    pathHead="E:\\医疗保险语料库\\医疗保险语料原文"
    txtpath="E:\\MedicareCorpus2"
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
                sents = SentenceSplitter.split(line)
                for s in sents:
                    data = s.strip()
                    data = data.strip('\n')
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
    pattern = [r'第.*(条|章)', r'（[0-9]{1,2}）', r'（(一|二|三|四|五|六|七|八|九|十)*）', r'[0-9]{1,2}(\．|\.)'
            , r'(一|二|三|四|五|六|七|八|九|十|[0-9])+(、|\．|\.)', r'(◆|)', r'（?.(府|政|国|法|字|发|办|综)+.[0-9]+.综?[0-9]+号）?']
    for p in pattern:
        sentence = re.sub(p, '', sentence)
    sentence = re.sub(r'(　| )+', '\n', sentence)
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

def PrepareText():
    filepath = 'E:\\MedicareCorpus2\\'
    efilepath = 'E:\\实体抽取\\'
    outpath = 'E:\\医疗保险语料待解析\\'
    files = os.listdir(filepath)
    for file in files:
        print(file)
        entities = []
        foj = open(filepath + file, 'r', encoding = 'utf-8')
        efoj = open(efilepath + file, 'r', encoding = 'utf-8')
        for e in efoj.readlines():
            entities.append(e.strip('\n'))
        sentences = []
        for line in foj.readlines():
            for e in entities:
                if line.find(e) != -1:
                    line = CleanSentence(line)
                    line = line.strip()
                    if len(line) > 1:
                        sentences.append(line.strip('\n'))
                    break
        with open(outpath + file, 'w', encoding='utf-8') as f:
            for s in sentences:
                f.write(s + '\n')
        foj.close()
        efoj.close()

def PrepareEntity(filename):
    entities = set()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            entities.add(line.strip('\n'))
    # for e in entities2:
    #     entities.add(e)
    en = []
    for e in entities:
        en.append(e)
    en.sort(key=lambda x: len(x), reverse=True)
    with open(filename, 'w', encoding='utf-8') as ff:
        for e in en:
            ff.write(e + '\n')

def SortCSVfile(filename):
    data = csv.reader(open(filename, 'r', encoding='utf-8'))
    sortedlist = sorted(data, key=lambda x:(lazy_pinyin(x[0])[0], lazy_pinyin(x[1])[0],lazy_pinyin(x[2])[0]))
    with open(filename, 'w', encoding='utf-8') as f:
        filewriter = csv.writer(f)
        for row in sortedlist:
            filewriter.writerow(row)
    f.close()

# SortCSVfile('E:\\哈尔滨市.csv')
filepath = 'E:\\实体关系抽取\\'
files = os.listdir(filepath)

for file in files:
    print(file)
    filename = filepath + file
    SortCSVfile(filename)




