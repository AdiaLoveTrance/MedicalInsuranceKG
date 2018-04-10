# -*- coding: UTF-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

def CrawlHospital(urllink):
    html = urlopen()
