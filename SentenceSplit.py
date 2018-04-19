import os
from pyltp import SentenceSplitter

#分句函数
def sentence_splitter(sentence):
    sents = SentenceSplitter.split(sentence)
    sents_list = list(sents)
    return sents_list

inputpath="E:\\MedicareCorpus"
outputpath="E:\\医疗保险语料"
k=1
inputfiles=os.listdir(inputpath)
print(inputfiles)
for file in inputfiles:
    #打开待分句文件
    fname=inputpath+"\\"+file
    f=open(fname,'r',encoding='utf-8')
    #打开输出文件
    opath=outputpath+"\\"+str(k)+".txt"
    outputfile=open(opath,'w',encoding='utf-8')
    for line in f.readlines():
        sents=sentence_splitter(line)
        for sent in sents:
            if len(sent)>1:
                outputfile.write(sent+'\n')
    f.close()
    outputfile.close()
    k=k+1


