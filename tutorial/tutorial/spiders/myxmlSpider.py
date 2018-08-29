# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
from tutorial.items import MyxmlItem


class MyxmlspiderSpider(XMLFeedSpider):
    name = 'myxmlSpider'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://blog.sina.com.cn/rss/1146583824.xml',
                  'http://blog.sina.com.cn/rss/1615888477.xml']
    iterator = 'iternodes'  # you can change this; see the docs
    itertag = 'rss'  # change it accordingly

    def parse_node(self, response, node):
        i = MyxmlItem()
        #i['url'] = selector.select('url').extract()
        #i['name'] = selector.select('name').extract()
        #i['description'] = selector.select('description').extract()
        i['title'] = node.xpath('/rss/channel/item/title/text()').extract()
        i['link'] = node.xpath('/rss/channel/item/link/text()').extract()
        i['author'] = node.xpath('/rss/channel/item/author/text()').extract()
        for j in range(len(i['title'])):
            print(f'第{str(j+1)}篇文章')
            print(f"Title is 「{i['title'][j]}」")
            print(f"Link is {i['link'][j]}")
            print(f"Author is 「{i['author'][j]}」")
            print('------------------------')
        return i
