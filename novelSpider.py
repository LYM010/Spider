#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging,os,json,requests,csv,time
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
def get_book_rank(url,rule,dictionary):
	for e in dictionary:
		link = url + str(dictionary[e])
		logging.debug(f'Linking to: {link}')
		try:
			res = requests.get(link)
			res.encoding = 'utf-8'
			result = BeautifulSoup(res.text,features='html.parser').select(rule)
			time.sleep(1)
			if len(result) == 0:
				logging.debug('Not Found.')
				continue
			else:
				for e in result:
					logging.debug(f'Saving:{e.get_text()}')
					with open('booksName.txt','a',encoding='utf-8') as bookNameFile:
						bookNameFile.write(e.get_text()+'\n')
		except:
			logging.debug(f'ConnectError: {link}')
			continue
	return
# delete repeat data.
def delete_repeat(old,new):
	with open(old,'r',encoding='utf-8') as oldFile,\
	 open(new,'a',encoding='utf-8') as newFile:
		content = oldFile.readlines()
		content_after = []
		for line in content:
			if line not in content_after:
				newFile.write(line)
				content_after.append(line)


# write data in csv file
def write_data_in_csv(line,file):
	logging.debug(f'Saving: {line} ...')
	with open(file,'w',newline='',encoding='utf-8') as outputFile:
		outputWriter = csv.writer(outputFile)
		outputWriter.writerow(list(line))

# Write data in MissionList file.
# dataStructure = [url,aim,status,level,rules,saveFile,time]
# aim = [content,contents,urlPath]
# status = [Doing,Done,Todo,Time_out,Not_Found]
def write_data_in_missionList(url,aim='URLPATH',status='TODO',\
	level=1,rules='',saveFile='mission.csv',\
	updateTime=time.strftime("%Y-%m-%d %H:%M:%S")):
	with open('mission.csv','w',newline='') as csvFile:
		outputWriter = csv.writer(csvFile)
		outputWriter.writerow([url,aim,status,level,rules,saveFile,updateTime])

def read_data_from_missionList(fileName='mission.csv'):
	with open(fileName) as csvFile:
		csvReader = csv.reader(csvFile)
		missionList = list(csvReader)
	return missionList

if __name__ == '__main__':
	set_env()
	# set seed.
	write_data_in_missionList('https://www.qidian.com/rank?chn=',\
		rules='a[data-eid="qd_C40"]',saveFile='booksName.txt')
	# get books rank
	ml = read_data_from_missionList()
	get_book_rank(ml[0][0],ml[0][4],read_type_dict())
	delete_repeat(ml[0][5],'Clean'+ml[0][5])
	write_data_in_missionList('https://www.biquge5200.cc/modules/article/search.php?searchkey=',\
		aim = 'contents',level = 2,rules = 'td.odd a')

#	get_book_rank(ml[0][0],typeDict,ml[0][4])
