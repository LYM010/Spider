#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging,os,json,requests,csv,time,openpyxl
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
	with open('mission.csv','a',newline='',encoding='utf-8') as csvFile:
		outputWriter = csv.writer(csvFile)
		outputWriter.writerow([url,aim,status,level,rules,saveFile,updateTime])

def read_data_from_missionList(fileName='mission.csv'):
	with open(fileName) as csvFile:
		csvReader = csv.reader(csvFile)
		missionList = list(csvReader)
	return missionList

def read_excel(file='mission.xlsx'):
	wb = openpyxl.load_workbook(file,read_only = True)
	sheet = wb['mission']
	for rowNum in range(1,sheet.max_row+1):
		logging.debug(f'Reading row {rowNum}')
		yield {
		'rowNum':rowNum,
		'url':sheet.cell(row=rowNum,column=1),
		'aim':sheet.cell(row=rowNum,column=2),
		'status':sheet.cell(row=rowNum,column=3),
		'level':sheet.cell(row=rowNum,column=4),
		'rules':sheet.cell(row=rowNum,column=5),
		'saveFile':sheet.cell(row=rowNum,column=6),
		'time':sheet.cell(row=rowNum,column=7)
		}

def write_in_excel(dict,file='mission.xlsx'):
	wb = openpyxl.load_workbook(file,encoding='utf-8')
	sheet = wb['mission']
	if dict['rowNum'] == 0:
		logging.debug(f'Append data in row {sheet.max_row+1}')
		sheet.append(dict)
	else:
		logging.debug(f'Updating data in row {dict["rowNum"]}')
		sheet.cell(row=dict['rowNum'],column=1).value=dict['url']
		sheet.cell(row=dict['rowNum'],column=2).value=dict['aim']
		sheet.cell(row=dict['rowNum'],column=3).value=dict['status']
		sheet.cell(row=dict['rowNum'],column=4).value=dict['level']
		sheet.cell(row=dict['rowNum'],column=5).value=dict['rules']
		sheet.cell(row=dict['rowNum'],column=6).value=dict['saveFile']
		sheet.cell(row=dict['rowNum'],column=7).value=dict['time']
	wb.save(file)

def search_book(url,rule,charMode='gbk'):
	

if __name__ == '__main__':
	set_env()
	# set seed.
#	write_data_in_missionList('https://www.qidian.com/rank?chn=',rules='a[data-eid="qd_C40"]',saveFile='booksName.txt')

	# get books rank
#	ml = read_data_from_missionList()
#	get_book_rank(ml[0][0],ml[0][4],read_type_dict())
#	delete_repeat(ml[0][5],'Clean'+ml[0][5])

#	write_data_in_missionList('https://www.biquge5200.cc/modules/article/search.php?searchkey=',\
#		aim = 'contents',level = 2,rules = 'td.odd a')

#	with open('CleanbooksName.txt','r',encoding='utf-8') as bookText:
#		for line in bookText.readlines():
#			logging.debug(f'Add url to search:{line.strip()}')
#			write_data_in_missionList('https://www.biquge5200.cc/modules/article/search.php?searchkey='+line.strip(),\
#				aim = 'contents',level = 2,rules = 'td.odd a')
	flag = 0
	for d in read_excel():
		if flag == 1:
			break
		else:
			flag += 1
			print(type(d['rowNum']))