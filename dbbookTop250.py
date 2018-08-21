#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}

for i in range(0,251,50):
	url = 'https://book.douban.com/top250?start='+str(i)
	res = requests.get(url=url,headers=headers,timeout=30)
	if res.status_code ==requests.codes.ok:
		result1 = BeautifulSoup(res.text,features='html.parser').select('.pl2 a[title]')
		for e in result1:
			print(e.get_text().strip().replace('\n','').replace(' ',''))
#			print(e.get_text().replace('\n','').strip() + ":" + e.get('href'))
