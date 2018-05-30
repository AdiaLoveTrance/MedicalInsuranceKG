# import os
#
# file = 'E:\\医疗保险语料库\\领域词典.txt'
# fo = open(file,'r',encoding='utf-8')
# e = []
# for l in fo.readlines():
#     e.append(l.strip('\n'))
# e.sort(key=lambda x:len(x))
# fo.close()
# e.reverse()
# ff = open(file,'w',encoding='utf-8')
# for ee in e:
#     ff.write(ee+'\n')
# ff.close()

# 统计某文件夹下的所有csv文件的行数（多线程）
import threading
import csv
import os


class MyThreadLine(threading.Thread):  # 用于统计csv文件的行数的线程类
    def __init__(self, path):
        threading.Thread.__init__(self)  # 父类初始化
        self.path = path  # 路径
        self.line = -1  # 统计行数

    def run(self):
        reader = csv.reader(open(self.path, "r", encoding='utf-8'))  # 读取csv文件
        lines = 0
        for item in reader:  # 读取每一行
            lines += 1
        self.line = lines  # 保存行数
        print(self.getName(), self.line)


path = "E:\\实体关系抽取2"  # 所有csv文件所在的文件夹
filelist = os.listdir(path)  # 存储了所有的csv文件名
threadlist = []  # 线程列表
for filename in filelist:
    newpath = path + "\\" + filename  # 代表绝对路径
    mythd = MyThreadLine(newpath)  # 创建线程类对象
    mythd.start()  # 线程开始干活
    threadlist.append(mythd)  # 增加线程到线程列表
for mythd in threadlist:  # 遍历每一个线程
    mythd.join()  # 等待所有线程干完活，再继续执行以下代码
linelist = []  # csv文件行数列表
for mythd in threadlist:
    linelist.append(mythd.line)
print(linelist)
ans = 0
for l in linelist:
    ans += l
print(ans)