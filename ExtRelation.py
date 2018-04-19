# -*- coding: utf-8 -*-
import os
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer
LTP_DATA_DIR = 'D:\\ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl_win.model')  # 语义角色标注模型

print("正在加载LTP模型... ...")

segmentor = Segmentor()
segmentor.load_with_lexicon(cws_model_path,'D:\\ltp_data_v3.4.0\\personal_seg.txt')

postagger = Postagger()
postagger.load_with_lexicon(pos_model_path,'D:\\ltp_data_v3.4.0\\personal_pos.txt')

parser = Parser()
parser.load(par_model_path)

print("加载模型完毕。")

in_file_name = "input.txt"
out_file_name = "output.txt"
begin_line = 1
end_line = 0


def extraction_start(in_file_name, out_file_name, begin_line, end_line):
    """
    事实三元组抽取的总控程序
    Args:
        in_file_name: 输入文件的名称
        #out_file_name: 输出文件的名称
        begin_line: 读文件的起始行
        end_line: 读文件的结束行
    """
    in_file = open(in_file_name, 'r', encoding='utf-8')
    out_file = open(out_file_name, 'a', encoding='utf-8')

    for line in in_file:
        fact_triple_extract(line.strip(), out_file)
    in_file.close()
    out_file.close()


def fact_triple_extract(sentence, out_file):
    """
    对于给定的句子进行事实三元组抽取
    Args:
        sentence: 要处理的语句
    """
    # print sentence
    words = segmentor.segment(sentence)
    print("\t".join(words))
    postags = postagger.postag(words)
    print('\t'.join(postags))
    arcs = parser.parse(words, postags)
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

    child_dict_list = build_parse_child_dict(words, postags, arcs)
    for index in range(len(arcs)):
        # 抽取以谓词为中心的事实三元组
        if arcs[index].relation == 'HED':
            child_dict = child_dict_list[index]
            # 主谓宾
            if 'SBV' in child_dict and 'VOB' in child_dict:
                e1 = complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                # e1 = words[child_dict['SBV'][0]]
                r = words[index]
                e2 = complete_e(words, postags, child_dict_list, child_dict['VOB'][0])

                out_file.write("主语谓语宾语关系\t(%s, %s, %s)\n" % (e1, r, e2))
                out_file.flush()
            # # 定语后置，动宾关系
            # if arcs[index].relation == 'ATT':
            #     if 'VOB' in child_dict:
            #         e1 = complete_e(words, postags, child_dict_list, arcs[index].head - 1)
            #         r = words[index]
            #         e2 = complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
            #         temp_string = r + e2
            #         if temp_string == e1[:len(temp_string)]:
            #             e1 = e1[len(temp_string):]
            #         if temp_string not in e1:
            #             out_file.write("定语后置动宾关系\t(%s, %s, %s)\n" % (e1, r, e2))
            #             out_file.flush()
            # # 含有介宾关系的主谓动补关系
            # if 'SBV' in child_dict and 'CMP' in child_dict:
            #     # e1 = words[child_dict['SBV'][0]]
            #     e1 = complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
            #     cmp_index = child_dict['CMP'][0]
            #     r = words[index] + words[cmp_index]
            #     if 'POB' in child_dict_list[cmp_index]:
            #         e2 = complete_e(words, postags, child_dict_list, child_dict_list[cmp_index]['POB'][0])
            #         out_file.write("介宾关系主谓动补\t(%s, %s, %s)\n" % (e1, r, e2))
            #         out_file.flush()

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
    """
    完善识别的部分实体
    """
    child_dict = child_dict_list[word_index]
    prefix = ''

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


if __name__ == "__main__":
    extraction_start(in_file_name, out_file_name, begin_line, end_line)
