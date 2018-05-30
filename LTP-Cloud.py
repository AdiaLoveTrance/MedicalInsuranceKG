# -*- coding:utf8 -*-
import os

path = 'E:\\实体关系抽取2\\'
files = os.listdir(path)
for f in files:
    print(f)
    file = path + f
    e = set()
    with open(file, 'r', encoding='utf-8') as ff:
        for line in ff.readlines():
            part = line.split(',')
            # if not part[0].isdigit():
            if len(part[0]) != 1:
                e.add(line)
    ff.close()
    with open(file, 'w', encoding='utf-8') as fff:
        for ee in e:
            fff.write(ee)

# path = 'E:\\实体抽取\\'
# files = os.listdir(path)
# entity = set()
#
# for file in files:
#     filename = path + file
#     with open(filename, 'r', encoding='utf-8') as f:
#         for line in f.readlines():
#             entity.add(line)
#
# print(len(entity))

