import requests
import bs4
from bs4 import BeautifulSoup
import json
APPID = '74783449'
APPSecret = 'e9PPXtOn'
url = 'https://tianqiapi.com/api?version=v6&appid='+APPID+'&appsecret='+APPSecret
r = requests.get(url)
bs1 = BeautifulSoup(r.content, features='lxml')
tp = eval(bs1.text)
ret = '今天' + tp['city'] + '天气' + tp['wea'] + \
    ',气温' + tp['tem2'] + '到' + tp['tem1'] + '摄氏度。' + '当前户外' + tp['tem'] + '摄氏度，' + '风力' + tp['win_speed'] + \
    '。PM2.5指数为' + tp['air'] + '。' + tp['air_tips']
print(ret)
