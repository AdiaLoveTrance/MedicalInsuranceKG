from py2neo import Graph
from py2neo import Node, Relationship
import os
import csv
graph = Graph("http://127.0.0.1:7474",username="chenjialinily@outlook.com",password="123456")
# path = 'E:\\实体关系抽取\\  '
# files = os.listdir(path)

#将医院信息导入图数据库
# hos_file = 'E:\\PyCharm Project\\NLP\\医院信息2.csv'
def ImportHospital(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            if len(row) != 0:
                str = row[1]
                s = str.split('-')
                graph.run('MERGE (p:Province {Pro_Name:{proname}}) '
                          'MERGE (c:City {City_Name:{cityname}}) '
                          'MERGE (c)-[s:属于]->(p) '
                          'CREATE (h:Hospital {Hos_Name:{hosname},Hos_Grade:{hosgrade},Hos_Speciality:{hosspe},Hos_Address:{address},Hos_PhoneNumber:{pn},Hos_Email:{email},Hos_Website:{web}})-[b:附属]->(c)'
                          ,proname = s[0], cityname = s[1], hosname = row[0], hosgrade = row[2], hosspe = row[3], address = row[4], pn = row[5], email = row[6], web = row[7])

#将药品信息导入图数据库
med_file = 'E:\\PyCharm Project\\NLP\\药品信息2.csv'
def ImportMedicine(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            if len(row) != 0:
                graph.run('CREATE (m:Medicine {Med_Name:{medname},Med_Kind:{medkind},Med_Remark:{remark}}) '
                          'MERGE(p:Province :{proname} {Pro_Name:{proname}}) '
                          'CREATE (m)-[r:参保地区]->(p)'
                          ,medname = row[0], medkind = row[1], proname = row[2], remark = row[3])

def Import(filename, cityname):
    """
    将指定csv文件导入Neo4j数据库
    :param filename: csv文件名称
    :return:
    """
    with open(filename, 'r', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            graph.run('MERGE (a:Entity1 {Entity_Name:{e1name},City_Name:{cityname}}) '
                      'MERGE(b:Entity2 {Entity_Name:{e2name},City_Name:{cityname}}) '
                      'CREATE (a)-[r:Relation {name:{rname},City_Name:{cityname},Detail:{detail}}]->(b)'
                      , e1name=row[0], cityname=cityname, rname=row[1], e2name=row[2], detail=row[3])

#导入三元组
# for file in files:
#     print(file)
#     filepath = path + file
#     city = file.strip('.csv')
#     Import(filepath, city)

# data = graph.data("MATCH (h:Hospital)-[]->(c:City) WHERE c.City_Name='长沙市' RETURN h.Hos_Name")
# print(data)
ImportMedicine(med_file)



