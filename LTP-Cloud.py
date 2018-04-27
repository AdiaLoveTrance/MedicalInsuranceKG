# -*- coding:utf8 -*-
import urllib.request
import urllib.parse

if __name__ == '__main__':
    url_get_base = "https://api.ltp-cloud.com/analysis/"
    args = {
        'api_key' : 'j1o7q6T2P6NpsCTUhfDYDrIPCOspevdOwWglmylX',
        'text' : '经市政府研究同意，现将《宜春市整合城乡居民基本医疗保险工作实施方案》印发给你们，请对照要求，结合实际，认真执行，抓好落实。',
        'pattern' : 'ner',
        'format' : 'plain',
        'only_ner':'true'
    }
    result=urllib.request.urlopen(url_get_base,urllib.parse.urlencode(args).encode('utf-8'))
    content = result.read().strip()
    print(content.decode('utf-8'))


