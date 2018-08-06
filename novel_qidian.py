#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import os,requests,logging,bs4,time,json,csv,shelve
from itertools import islice
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

def getRankBooks(url):
	logging.debug('Getting books from qidian...')
	bookList = []
	with open('type_dict.json','r') as jFile:
		dict = json.load(jFile)
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
	file = open('BooksName.txt','w')
	file.write('Upadte Time: ' + time.strftime("%Y-%m-%d %H:%M:%S")+'\r\n')
	for e in list:
		file.write(str(e)+'\r\n')
	file.close()

def searchBook(s_url,list):
	searchCSV = []
	for e in islice(list,1,None):
		link = s_url + e
		logging.debug(f'Searching: {link}')
		try:
			res = requests.get(link)
			res.raise_for_status()
			res.encoding = 'gbk'
		except:
			searchCSV.append([e,link,'Connect_Error'])
			logging.debug(f'Connnect_Error:{e} - {link}')
			continue
		soup = bs4.BeautifulSoup(res.text,features='html.parser')
		sElem = soup.select('td.odd a')
		logging.debug(f'Result: {len(sElem)}')
		if len(sElem) == 0:
			logging.debug(f'Not Found: {e}')
		tmp = []
		for se in sElem:
			if e.replace('\n','') == se.get_text():
				searchCSV.append([e,se.get('href'),'Succeed'])
	return searchCSV
			

if __name__ == '__main__':
	url = 'https://www.qidian.com/rank?chn='
	s_url = 'https://www.biquge5200.cc/modules/article/search.php?searchkey='
	set_env()
	shelfFile = shelve.open('mydata')
	shelfFile['url'] = url
	shelfFile['s_url'] = s_url
	shelFile.close()
	file = open('BooksName.txt')
	fList = file.readlines()
	file.close
	s_CSV = searchBook(s_url,fList)
	with open('searchBook.csv','w') as csvFile:
		outputWriter = csv.writer(csvFile)
		for i in range(len(s_CSV)):
			outputWriter.writerow(s_CSV[i])


