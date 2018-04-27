# -*- coding: utf-8 -*-
import os
LTP_DATA_DIR = 'E:\\ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl_win.model')  # 语义角色标注模型

contents = '各档次大病医疗保险所需资金从相应档次基本医疗保险统筹基金中划拨'

def SrlFunction(contents):
    from pyltp import Segmentor
    segmentor = Segmentor()  # 初始化实例
    # segmentor.load(cws_model_path)  # 加载模型
    segmentor.load_with_lexicon(cws_model_path,'E:\\ltp_data_v3.4.0\\personal_seg.txt')
    words = segmentor.segment(contents)  # 分词
    k = 1
    for word in words:
        print(word + str(k) + '  ',end='')
        k = k+1
    print('\n')
    # print('\t'.join(words))
    segmentor.release()  # 释放模型
    wordslist=list(words)

    from pyltp import Postagger
    postagger=Postagger()
    # postagger.load(pos_model_path)
    postagger.load_with_lexicon(pos_model_path,'D:\\ltp_data_v3.4.0\\personal_pos.txt')
    postags=postagger.postag(wordslist)
    print('\t'.join(postags))
    postagger.release()

    # wordslist = ['人力资源社会保障局','主管','医疗保险','工作']
    # postags = ['n','v','n','v']

    from pyltp import Parser
    parser = Parser() # 初始化实例
    parser.load(par_model_path)  # 加载模型
    arcs = parser.parse(wordslist, postags)  # 句法分析
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    parser.release()  # 释放模型

    from pyltp import SementicRoleLabeller
    labeller = SementicRoleLabeller() # 初始化实例
    labeller.load(srl_model_path)  # 加载模型
    # arcs 使用依存句法分析的结果
    roles = labeller.label(wordslist, postags, arcs)  # 语义角色标注

    # 打印结果
    for role in roles:
        print(role.index, "".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
    labeller.release()  # 释放模型

#     A1 = []
#     A0 = []
#     Op = []
#     for role in roles:
#         k = 0
#         a0 = ''
#         a1 = ''
#         for arg in role.arguments:
#             if arg.name == 'A0':
#                 a0 = ''.join(wordslist[arg.range.start:arg.range.end])
#                 k = k + 1
#             if arg.name == 'A1':
#                 a1 = ''.join(wordslist[arg.range.start:arg.range.end])
#                 k = k + 1
#         if k == 2:
#             A0.append(a0)
#             A1.append(a1)
#             Op.append(wordslist[role.index])
#
#     for (a0,o,a1) in zip(A0,Op,A1):
#         print(a0+'-'+o+'-'+a1)
#
# with open('./sentences.txt','r',encoding='utf-8') as f:
#     for line in f.readlines():
#         SrlFunction(line)
SrlFunction(contents)