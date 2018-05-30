# -*- encoding: utf-8 -*-
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer
import os
import re
LTP_DATA_DIR = 'E:\\ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`

segmentor = Segmentor()
segmentor.load(cws_model_path)
postagger = Postagger()
postagger.load(pos_model_path)

def ExtOrg(wordlist,taglist,filepath):
    centretag = ['#nh', '#ns', '#ni', '#m', '#nz', '#nt', '#j']
    centreword = ['机构', '部门', '局', '管理局', '站', '服务站', '中心', '保险', '对象', '基金', '费用', '资金', '公司', '人群', '人员', '保险费']
    relist = [r'#n(#n)+(#b|#nz)*', r'#n(#n)+(#an|#nz)?', r'#n(#n)+', r'#n(#n)+', r'#n#a(#n)+', r'#n#a(#n)+', r'#n(#n)+(#a)?(#n)*', r'#n(#n)+(#a(#n)*)?', r'(#n)+(#a(#n)*)?', r'#n(#n)+(#a)?(#n)+', r'#n(#n)+(#a|#b)?', r'#n(#n)+(#a)?', r'#n(#n)+', r'(#n)+(#a)?(#n)?', r'#n(#n)+((#b)+|(#a)*|#a(#n)+)', r'#n(#n)+(#v|#a(#n)+)']
    ecrelist = [r'[0-9]+']
    entities = set()
    for it1, it2 in zip(wordlist, taglist):
        if it2 in centretag:
            if it2 == '#m':
                for i in range(len(ecrelist)):
                    pat = re.compile(ecrelist[i])
                    m = pat.match(it1)
                    if m:
                        entities.add(it1)
                        break
            else:
                entities.add(it1)

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
    sentence = inputfile.read()
    words = segmentor.segment(sentence)
    postags = postagger.postag(words)
    for i in range(len(postags)):
        postags[i] = '#' + postags[i]
    # print(' '.join(words))
    # print(' '.join(postags))
    ExtOrg(words,postags,out_file)


in_filepath = 'E:\\MedicareCorpus\\'
out_filepath = 'E:\\实体抽取LTP\\'
in_files = os.listdir(in_filepath)
ffiles = os.listdir(out_filepath)
files = []
for f in in_files:
    if f not in ffiles:
        files.append(f)

for file in files:
    in_file = in_filepath + file    #输入文件路径
    out_file = out_filepath + file  #输出文件路径
    print(file)
    ExtEntity(in_file,out_file)













