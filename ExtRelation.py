# -*- coding: utf-8 -*-
from pyltp import Segmentor, Postagger, Parser
import os
import csv
import ExtLocation
LTP_DATA_DIR = 'E:\\ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`

segmentor = Segmentor()
segmentor.load_with_lexicon(cws_model_path,'E:\\ltp_data_v3.4.0\\personal_seg.txt')

postagger = Postagger()
postagger.load_with_lexicon(pos_model_path,'E:\\ltp_data_v3.4.0\\personal_pos.txt')

parser = Parser()
parser.load(par_model_path)

#输入文件
in_file_path = 'E:\\医疗保险语料待解析\\'
in_files_name = os.listdir(in_file_path)
#实体集
entity_file_path = 'E:\\实体抽取\\'
out_file_path = 'E:\\实体关系抽取2\\'

def extraction_start(in_file_name, out_file_name, entity_file_name):
    """
    总控程序
    :param in_file_name: 输入文件名
    :param out_file_name: 输出文件名
    :param entity_file_name: 实体文件名
    :return:
    """
    #获取实体
    entities = []
    entity_file = open(entity_file_name, 'r', encoding='utf-8')
    for e in entity_file.readlines():
        entities.append(e.strip('\n'))
    entity_file.close()
    #输入文件
    in_file = open(in_file_name, 'r', encoding='utf-8')
    rows = []
    for line in in_file.readlines():
        fact_triple_extract(line.strip('\n'), rows)
    in_file.close()
    #对写入数据进行清洗
    clean_rows(entities, rows)
    write_out_file(out_file_name, rows)

def fact_triple_extract(sentence, rows):
    """
    抽取实体关系三元组
    :param sentence: 待抽取的句子
    :param rows: 字典序列
    :return:
    """
    global segmentor,postagger,parser
    words = segmentor.segment(sentence)
    # print("\t".join(words))
    postags = postagger.postag(words)
    # print('\t'.join(postags))
    arcs = parser.parse(words, postags)
    # print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

    child_dict_list = build_parse_child_dict(words, arcs)
    for index in range(len(postags)):
        # 抽取以谓词为中心的事实三元组
        if postags[index] == 'v':
            child_dict = child_dict_list[index]
            # 主谓宾
            if 'SBV' in child_dict and 'VOB' in child_dict:
                e1_index = child_dict['SBV'][0]
                e1_child_dict = child_dict_list[e1_index]
                e1 = []
                if 'COO' in e1_child_dict.keys() and arcs[index].relation == 'HED':
                    for i in range(len(e1_child_dict['COO'])):
                        e1.append(complete_e(words, postags, child_dict_list, e1_child_dict['COO'][i]))
                e1.append(complete_e(words, postags, child_dict_list, child_dict['SBV'][0]))
                r = complete_r(words, postags, child_dict_list, index)
                e2_index = child_dict['VOB'][0]
                e2_child_dict = child_dict_list[e2_index]
                e2 = []
                e2.append(complete_e(words, postags, child_dict_list, e2_index))
                if 'COO' in e2_child_dict.keys():
                    for i in range(len(e2_child_dict['COO'])):
                        e2.append(complete_e(words, postags, child_dict_list, e2_child_dict['COO'][i]))
                for e_1 in e1:
                    for e_2 in e2:
                        relation = dict()
                        relation['e1'] = e_1
                        relation['r'] = r
                        relation['e2'] = e_2
                        relation['sentence'] = sentence
                        rows.append(relation)
            #前置宾语
            if 'FOB' in child_dict and 'ADV' in child_dict:
                e1_index = child_dict['ADV'][0]
                e1_index_dict = child_dict_list[e1_index]
                e1 = []
                if 'POB' in e1_index_dict:
                    for i in range(len(e1_index_dict['POB'])):
                        e1_coo_index = e1_index_dict['POB'][i]
                        e1.append(complete_e(words, postags, child_dict_list, e1_coo_index))
                        e1_coo_child_dict = child_dict_list[e1_coo_index]
                        if 'COO' in e1_coo_child_dict.keys():
                            for i in range(len(e1_coo_child_dict['COO'])):
                                e1.append(complete_e(words, postags, child_dict_list, e1_coo_child_dict['COO'][i]))
                r = complete_r(words, postags, child_dict_list, index)
                e2 = complete_e(words, postags, child_dict_list, child_dict['FOB'][0])
                for e0 in e1:
                    relation = dict()
                    relation['e1'] = e0
                    relation['r'] = r
                    relation['e2'] = e2
                    relation['sentence'] = sentence
                    rows.append(relation)

        if arcs[index].relation == 'HED':
            child_dict = child_dict_list[index]
            #介宾关系
            if 'SBV' in child_dict and 'POB' in child_dict:
                e1 = complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                eindex = child_dict['POB'][0]
                r = complete_r(words, postags, child_dict_list, index)
                e2 = complete_e(words, postags, child_dict_list, eindex)
                relation = dict()
                relation['e1'] = e1
                relation['r'] = r
                relation['e2'] = e2
                relation['sentence'] = sentence
                rows.append(relation)

def build_parse_child_dict(words, arcs):
    """
    为句子中的每个词语维护一个保存句法依存儿子节点的字典
    Args:
        words: 分词列表
        postags: 词性列表
        arcs: 句法依存列表
    """
    child_dict_list = []
    for index in range(len(words)):
        child_dict = dict()
        for arc_index in range(len(arcs)):
            if arcs[arc_index].head == index + 1:
                keys = child_dict.keys()
                if arcs[arc_index].relation in keys:
                    child_dict[arcs[arc_index].relation].append(arc_index)
                else:
                    child_dict[arcs[arc_index].relation] = []
                    child_dict[arcs[arc_index].relation].append(arc_index)
        # if child_dict.has_key('SBV'):
        #    print words[index],child_dict['SBV']
        child_dict_list.append(child_dict)
    return child_dict_list

def complete_e(words, postags, child_dict_list, word_index):
    """完善论元"""
    child_dict = child_dict_list[word_index]
    prefix = ''

    if 'FOB' in child_dict:
        word_index = child_dict['FOB'][0]
        child_dict = child_dict_list[word_index]

    if 'ATT' in child_dict:
        for i in range(len(child_dict['ATT'])):
            prefix += complete_e(words, postags, child_dict_list, child_dict['ATT'][i])

    postfix = ''
    if postags[word_index] == 'v':
        if 'VOB' in child_dict:
            postfix += complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
        if 'SBV' in child_dict:
            prefix = complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

    return prefix + words[word_index] + postfix

def complete_r(words, postags, child_dict_list, word_index):
    """完善关系"""
    child_dict = child_dict_list[word_index]
    prefix = ''
    if 'ADV' in child_dict:
        for i in range(len(child_dict['ADV'])):
            prefix += complete_r(words, postags, child_dict_list, child_dict['ADV'][i])
    if 'ATT' in child_dict:
        for i in range(len(child_dict['ATT'])):
            prefix += complete_r(words, postags, child_dict_list, child_dict['ATT'][i])
    postfix = ''
    if 'CMP' in child_dict:
        for i in range(len(child_dict['CMP'])):
            postfix += complete_r(words, postags, child_dict_list, child_dict['CMP'][i])
    if 'VOB' in child_dict:
        for i in range(len(child_dict['VOB'])):
            postfix += complete_r(words, postags, child_dict_list, child_dict['VOB'][i])
    if 'POB' in child_dict:
        for i in range(len(child_dict['POB'])):
            postfix += complete_r(words, postags, child_dict_list, child_dict['POB'][i])

    return prefix + words[word_index] + postfix

def write_out_file(out_file_name, rows):
    """
    写入输出文件
    :param out_file_name: 输出文件名称
    :param rows: 写入的数据
    :return:
    """
    #输出文件
    headers = ['e1', 'r', 'e2', 'sentence']
    with open(out_file_name, 'a', encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writerows(rows)
        f.flush()

def clean_rows(entities, rows):
    """
    对要写入的字典序列rows进行清洗，只写入包含实体的rows
    :param rows: 实体关系三元组字典序
    :return:
    """
    tmp = []
    for row in rows:
        e1find = 0
        e2find = 0
        str1 = str(row['e1'])
        str2 = str(row['e2'])
        for e in entities:
            if str1.find(e) != -1 and e1find == 0:
                row['e1'] = e
                e1find = 1
            if str2.find(e) != -1 and e2find == 0:
                row['e2'] = e
                e2find = 1
        if e1find == 1 or e2find ==1:
            tmp.append(row)
    rows.clear()
    for t in tmp:
        rows.append(t)

if __name__ == "__main__":
    # in_files_name2 = ['1.txt']
    ff = []
    with open('./已处理文件.txt', 'r', encoding='utf-8') as f:
        for l in f.readlines():
            ff.append(l.strip('\n'))
    in_files_name2 = []
    for file in in_files_name:
        if file not in ff:
            in_files_name2.append(file.strip('\n'))
    for file in in_files_name2:
        print(file)
        # 合成输入文件位置
        in_file_name = in_file_path + file
        # 获取输入文件的省市
        location = ExtLocation.ExtLocation(in_file_name, segmentor, postagger)
        out_file_name = out_file_path + str(location) + '.csv'
        entity_file_name = entity_file_path + file
        extraction_start(in_file_name, out_file_name, entity_file_name)
