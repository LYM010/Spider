#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import requests
from bs4 import BeautifulSoup

url = "http://www.zxcs8.com/"

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}


def get_links(url):
    r = requests.get(url)
    result = BeautifulSoup(r.text, features='html.parser').select("div.box li a")
    if len(result) > 0:
        for e in result:
            yield e.get('href')


def get_download_url(url):
    r = requests.get(url)
    result = BeautifulSoup(r.text, features='html.parser').select(".filetit a")
    if result:
        for e in result:
            return e.get('href')


if __name__ == '__main__':
    url = "http://www.zxcs8.com/"
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
    urlList = []
    with open('link.txt', 'r') as f:
        for line in f.readlines():
            link = get_download_url(line.strip())
            print(link)
'''
    for l1 in get_links(url):
        with open('link.txt', 'a') as f:
            f.write(l1 + '\n')

    r = requests.get('http://www.zxcs8.com/post/11169')
    result = BeautifulSoup(r.text, features='html.parser').select('.filetit a')
    if result:
        for e in result:
            print(e.get('href'))
    else:
        print("not found")
'''
