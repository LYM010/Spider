#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import os,requests,logging,bs4,json
logging.basicConfig(leven=logging.DEBUG,format=(f'{asctime} - {levelname} - {message}')
# logging.disable(logging.CRITICAL)

typeDict = {'玄幻':21, '奇幻':1,'武侠':2,'仙侠':22,'都市':4,'现实':15}
#{'军事':6,'历史':5,'游戏':7,'体育':8,'科幻':9,'灵异':10,'二次元':12}
billboard_tup = ('原创风云榜·新书','24小时热销榜','新锐会员周点击榜','推荐票榜',
	'收藏榜','完本榜','签约作家新书榜','公众作家新书榜')

savePath = os.path.join('..','Novel_qidiam')
os.chdir(savePaht,exist_ok = True)

url = 'https://www.qidian.com/rank?chn='

res = requests.get(url+str(21))
res.raise_for_status()

print(res)