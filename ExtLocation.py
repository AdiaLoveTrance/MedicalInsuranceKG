import os
import linecache
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer
LTP_DATA_DIR = 'E:\\ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`

segmenter = Segmentor()
segmenter.load_with_lexicon(cws_model_path,'E:\\ltp_data_v3.4.0\\personal_seg.txt')

postaggor = Postagger()
postaggor.load_with_lexicon(pos_model_path,'E:\\ltp_data_v3.4.0\\personal_pos.txt')

def ExtLocation(filename):
    """提取语料所属地名"""
    sentence = linecache.getline(filename, 5).strip()
    words = segmenter.segment(sentence)
    postags = postaggor.postag(words)
    location = ''
    for i in range(len(postags)):
        if postags[i] == 'ns':
            location = words[i]
            break
    print(location)
    # segmenter.release()
    # postaggor.release()
    return location

ExtLocation('E:\\医疗保险测试语料库\\132.txt')
