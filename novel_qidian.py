#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import os,requests,logging,bs4,time
logging.basicConfig(level=logging.DEBUG,\
	format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)

typeDict = {'玄幻':21, '奇幻':1,'武侠':2,'仙侠':22,'都市':4,'现实':15,'军事':6,
'历史':5,'游戏':7,'体育':8,'科幻':9,'灵异':10,'二次元':12}

def set_env():
	logging.debug('Setting environment...')
	savePath = os.path.join('..','Novel_qidian')
	os.makedirs(savePath,exist_ok = True)
	os.chdir(savePath)

def getBooks(url,dict):
	logging.debug('Getting books from qidian...')
	bookList = []
	for d in dict:
		link = url + str(dict[d])
		res=requests.get(link)
		res.raise_for_status()
		res.encoding = 'utf-8'
		soup = bs4.BeautifulSoup(res.text,features='html.parser')
		bookElem = soup.select('a[data-eid="qd_C40"]')
		for elem in bookElem:
			if elem.get_text() not in bookList:
				bookList.append(elem.get_text())
				logging.debug(f'Add book: {elem.get_text()}')
	logging.debug('Return bookList')
	return bookList

def writeList(list):
	logging.debug('Writting data in BooksName.txt')
	file = open('BooksName.txt','a')
	file.write(time.strftime("%Y-%m-%d %H:%M:%S")+'\r\n')
	for e in list:
		file.write(str(e)+'\r\n')
	file.close()

if __name__ == '__main__':
	url = 'https://www.qidian.com/rank?chn='
	set_env()
	writeList(getBooks(url,typeDict))


