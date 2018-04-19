# -*- encoding: utf-8 -*-
import os

inputpath = 'D:\\医疗保险测试语料库\\'
filesname = os.listdir(inputpath)
sentence = []

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

for file in filesname:
    filename = inputpath + file
    fileobject = open(filename,'r',encoding='utf-8')
    for line in fileobject.readlines():
        if hasNumbers(line) is True:
            sentence.append(line)
    fileobject.close()

with open('./sentence.txt','w',encoding='utf-8') as f:
    for s in sentence:
        f.write(s+'\n')

