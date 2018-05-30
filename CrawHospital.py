# -*- coding: UTF-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
import csv
import time
import requests
k = 0
baseurl = 'https://www.zgylbx.com/index.php?m=content&c=index&a=lists&catid=106&page='
list = []


def CrawlHospital(pagenum):
    print(pagenum)
    pageurl = baseurl + str(pagenum) + "&k1=&k2=&k3=&k4="
    session = requests.Session()
    headers = {
        "User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    try:
        html = session.get(pageurl, headers=headers)
    except ConnectionError as e:
        print(e)
        print(str(pagenum)+"页请求失败")
        return
    bsobj = BeautifulSoup(html.text,"html.parser")
    hos1 = bsobj.findAll("tr",{"class":" tr-dt"})
    hos2 = bsobj.findAll("tr",{"class":"tr-b tr-dt"})
    hos3 = bsobj.findAll("tr",{"class":"tr-dd dn"})
    list_hos1 = []
    list_hos2 = []


    for h in hos1:
        s = h.get_text()
        tmp = s.split('\n')
        temp = {}
        temp['Hos_Name'] = tmp[1]
        temp['Hos_City'] = tmp[2]
        temp['Hos_Grade'] = tmp[3]
        temp['Hos_Speciality'] = tmp[4]
        # hos_info.append(tuple(temp))
        list_hos1.append(temp)

    for h in hos2:
        s = h.get_text()
        tmp = s.split('\n')
        temp = {}
        temp['Hos_Name'] = tmp[1]
        temp['Hos_City'] = tmp[2]
        temp['Hos_Grade'] = tmp[3]
        temp['Hos_Speciality'] = tmp[4]
        # hos_info.append(tuple(temp))
        list_hos2.append(temp)

    for i in range(len(list_hos1)):
        list.append(list_hos1[i])
        list.append(list_hos2[i])

    global k
    for h in hos3:
        s = h.get_text()
        s = s.strip()
        tmp = s.split('\n')
        # for t in tmp:
        #     print(t.strip())
        list[k]['Hos_Address'] = tmp[0].strip()
        list[k]['Hos_PhoneNumber'] = tmp[1].strip()
        list[k]['Hos_Email'] = tmp[2].strip()
        list[k]['Hos_Website'] = tmp[3].strip()
        k += 1


if __name__ == '__main__':
    for i in range(1, 1530):
        # time.sleep(1)
        CrawlHospital(i)
    headers = ['Hos_Name','Hos_City','Hos_Grade','Hos_Speciality','Hos_Address','Hos_PhoneNumber','Hos_Email','Hos_Website']
    with open('./医院信息2.csv','w',encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        try:
            f_csv.writerows(list)
        except UnicodeEncodeError as e:
            print(e)