# -*- coding: UTF-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool
import csv
import time
import requests

baseurl = 'https://www.zgylbx.com/index.php?m=content&c=index&a=lists&catid=105&page='
hos_info = []

def CrawlHospital(pagenum):
    print(pagenum)
    pageurl = baseurl + str(pagenum) + "&k1=&k2=&k3=&k4="
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
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

    for h in hos1:
        s = h.get_text()
        tmp = s.split('\n')
        temp = []
        temp.append(tmp[1])
        temp.append(tmp[2])
        temp.append(tmp[3])
        # print(temp)
        hos_info.append(tuple(temp))
    for h in hos2:
        s = h.get_text()
        tmp = s.split('\n')
        temp = []
        temp.append(tmp[1])
        temp.append(tmp[2])
        temp.append(tmp[3])
        # print(temp)
        hos_info.append(tuple(temp))


if __name__ == '__main__':
    for i in range(1, 800):
        time.sleep(1)
        CrawlHospital(i)
    headers = ['Med_Name','Med_Kind','Med_Plc']
    with open('./药品信息.csv','w',encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        try:
            f_csv.writerows(hos_info)
        except UnicodeEncodeError as e:
            print(e)