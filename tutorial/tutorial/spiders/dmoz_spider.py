# -*- coding: utf-8 -*-

import scrapy
from tutorial.items import DmozItem


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["iplaysoft.com"]
    start_urls = [
        "https://www.iplaysoft.com",
    ]

    def parse(self, response):
        item = DmozItem()
        for sel in response.xpath('//ul/li'):
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item
