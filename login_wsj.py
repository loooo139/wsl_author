'''
Author: li xuefeng
Date: 2021-01-28 17:47:42
LastEditTime: 2021-01-28 21:38:09
LastEditors: lixf
Description:
FilePath: \wsl_author\login_wsj.py
more code more  happy
'''
from datetime import datetime
import json
import threading
import queue
from selenium import webdriver
from datetime import date
from datetime import timedelta
import time
import redis
import pymysql
import sys
import os
import platform
from datetime import datetime, tzinfo, timedelta
import random
import urllib
options = webdriver.ChromeOptions()
# 设置中文
mobileEmulation = {'deviceName': 'Galaxy S5'}
options.add_argument('--ignore-certificate-errors')
# from selenium.webdriver.chrome.options import Options
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('mobileEmulation', mobileEmulation)
# options.add_argument('--headless')
# 更换头部
options.add_argument(
    'user-agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"'
)
redis_url = 'tencent.latiaohaochi.cn'
mysql_url = 'ali.latiaohaochi.top'
# if ping('www.google.com') != 0:
#     print('using proxy browse the wjs')
#     # options.add_argument("--proxy-server=socks5://n1.latiaohaochi.top:10808")
driver = webdriver.Chrome(options=options)  # 打开 Chrome 浏览器
r = redis.StrictRedis(host=redis_url,
                      port=6379,
                      password='6063268abc',
                      retry_on_timeout=5,
                      db=0)
cookies = json.loads(open('cookies').read())
driver.get(
    'https://www.wsj.com')
for cookie in cookies:
    driver.add_cookie(cookie)
login_botton = driver.find_elements_by_css_selector('a[role="button"]')[1]
login_botton.click()
driver.find_element_by_id("username").send_keys('Hong.wu.pitt@gmail.com')
driver.find_element_by_id("password").send_keys('jay871125')
driver.find_element_by_css_selector('button[type="submit"]').click()
open('cookies', 'w').write(json.dumps(driver.get_cookies()))
driver.get('https://www.wsj.com/articles/huntsman-mulls-repatriating-overseas-cash-for-bolt-on-deals-1533319750')
head = driver.find_element_by_css_selector(
    'h1[class="wsj-article-headline]"').text
sub_head = driver.find_element_by_css_selector('h2[class="sub-head]"').text
text = driver.find_element_by_id('wsj-article-wrap').text
source_text = driver.find_element_by_tag_name('body').text
# jar = requests.cookies.RequestsCookieJar()
