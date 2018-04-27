import os

entityfile = 'E:\\规则实体抽取\\1.txt'
originalfile = 'E:\\医疗保险测试语料库\\1.txt'

entities = []
with open(entityfile, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        entities.append(line)
print(entities)
sentences = []
with open(originalfile, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        for e in entities:
            e = e.strip('\n')
            if line.find(e) != -1:
                sentences.append(line)
                break
print(sentences)
with open('./sentences.txt','w',encoding='utf-8') as f:
    for s in sentences:
        f.write(s)
