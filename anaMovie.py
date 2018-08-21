#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

import pandas as pd
from pyecharts import Geo, Style, Line, Bar, Overlap

with open('爱情公寓_new.txt', encoding='utf-8') as f:
    data = pd.read_csv(f, sep=',', header=None,
                       encoding='utf-8', names=['date', 'nickname',
                                                'city', 'rate', 'comment'])
    city = data.groupby(['city'])
    rate_group = city['rate']
    city_com = city['rate'].agg(['mean', 'count'])
    city_com.reset_index(inplace=True)
    city_com['mean'] = round(city_com['mean'], 2)
    # print(city_com)

# 热力图
data_map = [(city_com['city'][i], city_com['count'][i]) for i in range(0, city_com.shape[0])]
print(data_map)
style = Style(title_color="#fff", title_pos="center", width=1200, height=600, background_color="#404a59")
geo = Geo("人群地理位置", "数据来源：Leon", **style.init_style)

while True:
    try:
        attr, val = geo.cast(data_map)
        geo.add("", attr, val, visual_range=[0, 20],
                visual_text_color="#fff", symbol_size=20,
                is_visualmap=True, is_piecewise=True,
                visual_split_number=4)
    except ValueError as e:
        e = str(e)
        e = e.split("No coordinate is specified for ")[1]  # 获取不支持的城市名
        for i in range(0, len(data_map)):
            if e in data_map[i]:
                data_map.pop(i)
                break
        continue
    else:
        break
geo.render('aqgw.html')
