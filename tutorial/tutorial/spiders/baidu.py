# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import BaiduItem

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['readthedocs.io']
    start_urls = ['https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/commands.html']

    def parse(self, response):
        item = BaiduItem()
        item['title'] = response.xpath('/html/head/title/text()')
        print(item['title'])
