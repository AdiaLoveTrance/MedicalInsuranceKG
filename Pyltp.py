# -*- coding: utf-8 -*-
from pyltp import SentenceSplitter
import os
sents = SentenceSplitter.split('元芳你怎么看？我就趴窗口上看呗！')  # 分句
print('\n'.join(sents))

import os
LTP_DATA_DIR = 'E:\\ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`

from pyltp import Segmentor
segmentor = Segmentor()  # 初始化实例 
# segmentor.load(cws_model_path)  # 加载模型
segmentor.load_with_lexicon(cws_model_path,'E:\\ltp_data_v3.4.0\\personal.txt')

with open('E:\\医疗保险测试语料库\\2.txt','r',encoding='utf-8') as f:
    contents=f.read()

words = segmentor.segment(contents)  # 分词
# print('\t'.join(words))
segmentor.release()  # 释放模型
wordslist=list(words)

from pyltp import Postagger
postagger=Postagger()
postagger.load(pos_model_path)
postags=postagger.postag(wordslist)
# print('\t'.join(postags))
postagger.release()

from pyltp import NamedEntityRecognizer
recognizer=NamedEntityRecognizer()
recognizer.load(ner_model_path)
netags=recognizer.recognize(wordslist,postags)
count=0
for word,netag in zip(wordslist,netags):
    if netag is not 'O':
        print(word+' '+netag)
recognizer.release()