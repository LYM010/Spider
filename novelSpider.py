#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging,os,json,requests,csv
from bs4 import BeautifulSoup

logging.basicConfig(level = logging.DEBUG,\
	format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.CRITICAL)

# Initialize enviroment
def set_env():
	logging.debug('Initialize environment...')
	savePath = os.path.join('..','NovelSpider')
	os.makedirs(savePath,exist_ok=True)
	os.chdir(savePath)
	logging.debug('Enviroment had initialize.')

# Read dictionary
def read_type_dict():
	logging.debug('Loading type dict...')
	with open('type_dict.json','r') as jFile:
		return json.load(jFile)

# Get book's name from qidian.com's rank
def get_book_rank(url,dictionary):
	rankSoup = []
	for e in dictionary:
		link = url + str(dictionary[e])
		logging.debug(f'Linking to: {link}')
		try:
			res = requests.get(link)
			res.raise_for_status()
			res.encoding = 'utf-8'
			rankSoup.append(BeautifulSoup(res.text,features='html.parser'))
		except:
			logging.debug(f'ConnectError: {link}')
			continue
	return rankSoup

# Analysis BeautifulSoup with appointed rule.
def analysis_soup(soupList,rule):
	logging.debug('Analysising BeartifulSoup...')
	for soup in soupList:
		result = soup.select(rule)
	return result

# Get book's name from rank
def get_book_name(elems):
	logging.debug("Get book's name from rank.")
	bookNameList = []
	if len(elems) == 0:
		return 0
	else:
		for e in elems:
			if e.get_text() not in bookNameList:
				bookNameList.append(e.get_text())
	return list(bookNameList)

# write data in csv file
def write_data_in_csv(list,file):
	for line in list:
		with open(file,'w',newline='') as outputFile:
			outputWriter = csv.writer(outputFile)
			outputWriter.writerow(line)

# Write data in MissionList file.
# dataStructure = [url,aim,status,level,rules,saveFile,time]
# aim = [content,contents,urlPath]
# status = [Doing,Done,Todo,Time_out,Not_Found]
if __name__ == '__main__':
	set_env()
	typeDict = read_type_dict()
	qdRule = 'a[data-eid="qd_C40"]'
	qdurl = 'https://www.qidian.com/rank?chn='
