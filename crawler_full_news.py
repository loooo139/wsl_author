'''
Author: li xuefeng
Date: 2021-01-28 15:26:03
LastEditTime: 2021-01-28 20:52:12
LastEditors: lixf
Description:
FilePath: \wsl_author\crawler_full_news.py
more code more  happy
'''
from datetime import datetime
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
import json


class UTC(tzinfo):
    """UTC"""

    def __init__(self, offset=0):
        self._offset = offset

    def utcoffset(self, dt):
        return timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC +%s" % self._offset

    def dst(self, dt):
        return timedelta(hours=self._offset)


def ping(url='tencent.latiaohaochi.cn'):
    print('ping ' + url)
    print('current os is ' + platform.platform())
    if 'Linux' in platform.platform():
        result = os.system(u'ping ' + url + ' -c 3')
    else:
        result = os.system(u"ping " + url + ' -n 3')
    # result = os.system(u"ping www.baidu.com -n 3")
    if result == 0:
        print("the network is good")
    else:
        print("can not connect the wsj,will use the proxy")
    return result


options = webdriver.ChromeOptions()
# 设置中文
mobileEmulation = {'deviceName': 'Galaxy S5'}
options.add_argument('--ignore-certificate-errors')
# from selenium.webdriver.chrome.options import Options
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('mobileEmulation', mobileEmulation)
# options.add_argument('--headless')
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--disable-gpu')
prefs = {
    'profile.default_content_settings': {
        'profile.default_content_setting_values': {
            'images': 2,  # 不加载图片
            'javascript': 2
        }}}
options.add_experimental_option("prefs", prefs)
options.add_argument(
    'user-agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"'
)
if ping() == 0:
    redis_url = 'tencent.latiaohaochi.cn'
    mysql_url = 'tencent.latiaohaochi.cn'
else:
    redis_url = 'latiaohaochi.cn'
    mysql_url = 'latiaohaochi.cn'
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
# res = open('./dis_res.csv', 'a', encoding='utf8', buffering=1)
# len_res=0
full_res = 0
driver.implicitly_wait(10)
# driver.set_page_load_timeout(10)
mysql = pymysql.connect(host=mysql_url,
                        user='root',
                        password='6063268abc',
                        connect_timeout=200,
                        db='crawler')
cursor = mysql.cursor()
sql = 'insert into res_news_v1(news_id,key_word,title,link,id,authors,date,full_title,subtitle,text,plain_text) values("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'
# fail_data = open('./other.csv', 'a', encoding='utf8')
first_crawler = True
while True:
    try:
        while r.scard('full_news_v1') != 0:
            #    time.sleep(5)
            print(datetime.now(UTC(8)))
            print('remain task')
            print(r.scard('full_news_v1'))
            line = r.spop('full_news_v1').decode('utf8').split('\t')
            #    r.lpop('urls')
            # name, start_date, end_date = line[0], line[1], line[2]
            # origin_index, name, start_date, author_ori = line[0], line[
            #     1], line[2], line[-1]
            # end_date = start_date.split()[0]
            # start_date = str(int(end_date.split('/')[0]) - 1)
            # start_date += end_date[4:]
            # author_ori = line[0]
            # company_name = line[0]
            news_link = line[3]
            try:
                # single_url = "https://www.wsj.com/search?query={key}&isToggleOn=true&operator=AND&sort=date-desc&duration=4y&startDate=2001%2F01%2F23&endDate=2020%2F10%2F23&source=wsjie%2Cblog%2Cwsjvideo%2Cinteractivemedia%2Cwsjsitesrch%2Cwsjpro%2Cautowire%2Capfeed".format(
                #     key=company_name)
                # single_url = 'https://www.wsj.com/search/term.html?KEYWORDS=3M&min-date=2015/04/26&max-date=2016/04/26&isAdvanced=true&daysback=90d&byline=Bob%20Tita&andor=AND&sort=date-desc&source=wsjarticle'
                # name = 'Activision'
                # start_date = '2013/01/01'
                # end_date = '2013/12/31'
                # author_ori = 'Ian Sherr'
                # origin_index = '135984'
                single_url = news_link
                print('current url is ', single_url, '\n', 'loading')
                # time.sleep(random.random())
                driver.get(single_url)
                if first_crawler:
                    cookies = json.loads(open('cookies').read())
                    for cookie in cookies:
                        driver.add_cookie(cookie)
                    login_botton = driver.find_elements_by_css_selector('a[role="button"]')[
                        1]
                    login_botton.click()
                    first_crawler = False
                print(datetime.now(UTC(8)))
                # WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located(
                #         (By.XPATH, "//div[@class='headline-container']")))
                # time.sleep(3)
                try:
                    news = driver.find_elements_by_css_selector(
                        'h1[class="wsj-article-headline"')
                    if len(news) == 0:
                        print('no news parse')
                        r.sadd('full_news_v1', '\t'.join(line))
                        continue
                    # len_res = int(
                    #     driver.find_elements_by_css_selector(
                    #         'span[class="strong"]')[0].text.split()[-1])
                except IndexError as e:
                    # r.sadd('urls', '\t'.join(line))
                    print('find no news on this page,put it back to db')
                    print('current url is ', single_url)
                    r.sadd('full_news_v1', '\t'.join(line))
                    continue
                try:
                    head = driver.find_element_by_css_selector(
                        'h1[class="wsj-article-headline"]').text.replace('"', '')
                except:
                    head = 'null'
                try:
                    sub_head = driver.find_element_by_css_selector(
                        'h2[class="sub-head"]').text.replace('"', '')
                except:
                    sub_head = 'null'
                try:
                    body_text = driver.find_element_by_id(
                        'wsj-article-wrap').text.replace('(', '').replace(')', '').replace(',', '.').replace('"', '')
                except:
                    body_text = 'null'
                source_text = driver.find_element_by_tag_name('body').text.replace(
                    '(', '').replace(')', '').replace(',', '.').replace('"', '')
                single_res = '\t'.join(
                    (line[0], line[1], line[2], line[3], line[4], line[5], line[6], head, sub_head, body_text, source_text))
                if r.sadd('text_news_v1', single_res) == 0:
                    print('duplicate news')
                    continue
                try:
                    news_sql = sql.format(
                        line[0].replace('"', ''), line[1].replace('"', ''), line[2].replace('"', ''), line[3].replace('"', ''), line[4].replace('"', ''), line[5].replace('"', ''), line[6].replace('"', ''), head, sub_head, body_text, source_text)
                    news_sql = news_sql.replace('\n', ' ')
                    cursor.execute(news_sql)
                    mysql.commit()
                    print('insert to db success')
                    full_res += 1
                    print('write one news ' + str(full_res))
                    print('finish one  jobs,left is ',
                          r.scard('full_news_v1'))
                except:
                    print(sys.exc_info())
                    print(news_sql)
                    print('insert to db failed')
                    mysql = pymysql.connect(
                        host=mysql_url,
                        user='root',
                        password='6063268abc',
                        connect_timeout=20,
                        db='crawler')
                    cursor = mysql.cursor()
                    mysql.rollback()
            # except Exception as e:
            #     print('exception', e, sys.exc_info())
                # single_res = '\t'.join([company_name, i.text])
                # fail_data.write(single_res + '\n')

                # res.write(i.text)
            except Exception as e:
                print(datetime.now(UTC(8)))
                print('something wrong ', e, e.args, sys.exc_info())
                print('could not load the page,tiemout,try late')
                r = redis.StrictRedis(host=redis_url,
                                      port=6379,
                                      password='6063268abc',
                                      retry_on_timeout=5,
                                      db=0)
                r.sadd('full_news_v1', '\t'.join(line))
        #  得到网页 html, 还能截图
        print('jobs finish ,queue is empty')
        break
    except Exception as e:
        print('maybe redis is down ', sys.exc_info())
        print(e, e.args)
        r = redis.StrictRedis(host=redis_url,
                              port=6379,
                              password='6063268abc',
                              retry_on_timeout=5,
                              db=0)
        mysql = pymysql.connect(host=mysql_url,
                                user='root',
                                password='6063268abc',
                                connect_timeout=20,
                                db='crawler')
        cursor = mysql.cursor()
driver.quit()
