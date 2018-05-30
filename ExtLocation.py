import os
# from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer
# LTP_DATA_DIR = 'E:\\ltp_data_v3.4.0'  # ltp模型目录的路径
# cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
# pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
#
# segmenter = Segmentor()
# segmenter.load_with_lexicon(cws_model_path,'E:\\ltp_data_v3.4.0\\personal_seg.txt')
#
# postaggor = Postagger()
# postaggor.load_with_lexicon(pos_model_path,'E:\\ltp_data_v3.4.0\\personal_pos.txt')

def ExtbySentence(sentence, segmentor, postagger):
    words = segmentor.segment(sentence)
    postags = postagger.postag(words)
    location = ''
    for i in range(len(postags)):
        if postags[i] == 'ns':
            location = words[i]
            # print(location)
            return location

def ExtLocation(filename, segmentor, postagger):
    """提取语料所属地名"""
    file = open(filename, 'r', encoding='utf-8')
    loc = None
    while loc == None:
        sentence = next(file)
        loc = ExtbySentence(sentence, segmentor, postagger)
    return loc



