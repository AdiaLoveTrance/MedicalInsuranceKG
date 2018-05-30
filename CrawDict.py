# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen

baseurl = 'http://wiki.mbalib.com'
urllinks = set()
urllinks.add('/wiki/%E5%8C%BB%E7%96%97%E4%BF%9D%E9%99%A9')
donelink = []
words = set()
def PrepareDict(url):
    html = urlopen(str(baseurl + url))
    bsobj = BeautifulSoup(html,"html.parser")
    urls = bsobj.findAll("a")
    print(urls)
    for u in urls:
        urllinks.add(u.attrs['href'])
        words.add(u.attrs['title'])
    donelink.append(url)

k = 0
while len(urllinks) != 0 and k < 20:
    url = urllinks.pop()
    print(url)
    if url not in donelink:
        PrepareDict(url)
    k += 1

print(words)
