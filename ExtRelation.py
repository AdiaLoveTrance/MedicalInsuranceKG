# -*- coding: utf-8 -*-
import os
import csv
import ExtLocation
import FileDispose
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer
LTP_DATA_DIR = 'E:\\ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl_win.model')  # 语义角色标注模型

segmentor = Segmentor()
segmentor.load_with_lexicon(cws_model_path,'E:\\ltp_data_v3.4.0\\personal_seg.txt')

postagger = Postagger()
postagger.load_with_lexicon(pos_model_path,'E:\\ltp_data_v3.4.0\\personal_pos.txt')

parser = Parser()
parser.load(par_model_path)

#输入文件
in_file_path = 'E:\\医疗保险测试语料库\\'
in_files_name = os.listdir(in_file_path)
#实体集
entity_file_path = 'E:\\规则实体抽取\\'
out_file_path = 'E:\\实体关系抽取\\'

# in_file_name = "input.txt"

def extraction_start(in_file_name, out_file_name, entity_file_name):
    """
    总控程序
    :param in_file_name: 输入文件名
    :param out_file_name: 输出文件名
    :param entity_file_name: 实体文件名
    :return:
    """
    #输入文件
    in_file = open(in_file_name, 'r', encoding='utf-8')
    #获取实体
    entities = []
    entity_file = open(entity_file_name, 'r', encoding='utf-8')
    for e in entity_file.readlines():
        entities.append(e)
    entity_file.close()
    rows = []
    for line in in_file.readlines():
        line = FileDispose.CleanSentence(line.strip())
        fact_triple_extract(line, rows)
    in_file.close()
    #对写入数据进行清洗
    write_out_file(out_file_name, rows)

def fact_triple_extract(sentence, rows):
    """
    抽取实体关系三元组
    :param sentence: 待抽取的句子
    :param rows: 字典序列
    :return:
    """
    words = segmentor.segment(sentence)
    # print("\t".join(words))
    postags = postagger.postag(words)
    # print('\t'.join(postags))
    arcs = parser.parse(words, postags)
    # print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

    child_dict_list = build_parse_child_dict(words, postags, arcs)
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
                # r = words[index]
                r = complete_r(words, postags, child_dict_list, index)
                # e2 = complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                e2_index = child_dict['VOB'][0]
                e2_child_dict = child_dict_list[e2_index]
                e2 = []
                e2.append(complete_e(words, postags, child_dict_list, e2_index))
                if 'COO' in e2_child_dict.keys():
                    for i in range(len(e2_child_dict['COO'])):
                        e2.append(complete_e(words, postags, child_dict_list, e2_child_dict['COO'][i]))
                for e_1 in e1:
                    for e_2 in e2:
                        # out_file.write("#主语谓语宾语关系#\t(%s, %s, %s)\n" % (e_1, r, e_2))
                        # out_file.flush()
                        relation = dict()
                        relation['e1'] = e_1
                        relation['r'] = r
                        relation['e2'] = e_2
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

                r = words[index]
                e2 = complete_e(words, postags, child_dict_list, child_dict['FOB'][0])
                for e0 in e1:
                    # out_file.write("#前置宾语#\t(%s, %s, %s)\n" % (e0, r, e2))
                    # out_file.flush()
                    relation = dict()
                    relation['e1'] = e0
                    relation['r'] = r
                    relation['e2'] = e2
                    rows.append(relation)

        if arcs[index].relation == 'HED':
            child_dict = child_dict_list[index]
            #介宾关系
            if 'SBV' in child_dict and 'POB' in child_dict:
                e1 = complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                eindex = child_dict['POB'][0]
                r = words[eindex]
                e2 = complete_e(words, postags, child_dict_list, eindex)
                relation = dict()
                relation['e1'] = e1
                relation['r'] = r
                relation['e2'] = e2
                rows.append(relation)
                # out_file.write("#介宾关系#\t(%s, %s, %s)\n" % (e1, r, e2))
                # out_file.flush()

def build_parse_child_dict(words, postags, arcs):
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
    # if 'VOB' in child_dict:
    #     for i in range(len(child_dict['VOB'])):
    #         postfix += complete_r(words, postags, child_dict_list, child_dict['VOB'][i])
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
    headers = ['e1', 'r', 'e2']
    with open(out_file_name, 'a', encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writerows(rows)


if __name__ == "__main__":
    for file in in_files_name:
        print("正在处理"+file)
        # 合成输入文件位置
        in_file_name = in_file_path + file
        # 获取输入文件的省市
        location = ExtLocation.ExtLocation(in_file_name)
        out_file_name = out_file_path + str(location) + '.csv'
        entity_file_name = entity_file_path + file
        extraction_start(in_file_name, out_file_name, entity_file_name)
