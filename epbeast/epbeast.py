##########
import Video_API
#####
import time
import os
from urllib.request import urlretrieve
from urllib.parse import urlparse
import requests
import json
# ------
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# --------------------------------
import threading
import time
# ----------------------------
import urllib3
import glob
urllib3.disable_warnings()
# ------------------------

_host = 'https://www.epbeast.com'
###
download_coms = 0
mp4_list = []
mp4_list2 = []
####
Video_API = Video_API.Video_API(api_url='http://211.233.25.166:1154/api/')
####


def _web_(___url):
    headers = {'user-agent': 'my-app/0.0.1'}
    res = requests.get(___url, headers=headers, verify=False)
    html = res.content.decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')

    # # d = save_or_check(___url)
    # # if d == False:
    # #     print('抓過囉')
    # #     return False

    # soup = False
    # ####
    # chrome_path = "chromedriver.exe"
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--hide-scrollbars')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument("--log-level=3")  # fatal

    # try:
    #     web = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
    #     web.get(___url)
    #     # time.sleep(300)

    # except:
    #     # web.quit()
    #     print('error')
    #     # return _web_(___url)
    # try:
    #     html = web.page_source
    #     soup = BeautifulSoup(html, 'html.parser')
    # except:
    #     # pass
    #     web.quit()

    # web.quit()

    return soup


def new_web_down(url, download_default_directory='D:\epbeast_開發中\download_mp4'):
    ####
    if check_mp4() >= 30:
        print('超過30部')
    ####
    ####
    chrome_path = "chromedriver.exe"
    chrome_options = Options()
    ###
    prefs = {
        "download.default_directory": download_default_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # 無頭模式（就是不開啟瀏覽器）
    # chrome_options.add_argument("--headless")
    ##
    web = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
    ##
    web.get(url)
    time.sleep(100)
    while True:
        # print(check_Temp())
        if check_Temp() == 0:
            print('抓完囉')
            web.quit()
            return True

    ###
    time.sleep(60*60*24)
    ###
    web.quit()

    return True


def check_Temp():
    # crdownload
    v = glob.glob('./download_mp4/*.crdownload')
    return len(v)


def check_mp4():
    # crdownload
    v = glob.glob('./download_mp4/*.mp4')
    return len(v)


def _sigle__page(_url):
    ###
    global download_coms
    global _host
    global mp4_list
    global mp4_list2
    ### 
    if len(mp4_list2) > 2:
        return True
    soup = _web_(_url)
    #####
    # print(soup)
    # hd-porn-dload
    div_hd_porn_dload = soup.find('div', {'id': 'hd-porn-dload'}).find_all('a')
    # print(div_hd_porn_dload)
    # for item in div_hd_porn_dload:
    #     _href = str(_host) + item.get('href')
    #     print(_href)
    ###
    ##
    # print(len(div_hd_porn_dload))
    # mp4_list.append(str(_host) + div_hd_porn_dload[-1].get('href'))
    # mp4_list.append(str(_host) + div_hd_porn_dload[0].get('href'))
    _mp4 = str(_host) + div_hd_porn_dload[-1].get('href')

    if download_coms >= 30:
        print('本日額度滿了')
        return True

    print(_mp4)
    # new_web_down(_mp4)
    RES = Video_API.apiVerificationUrlExist(_mp4)
    if RES:
        print('影片正確')
        print(RES['data']['video_dl_id'])
        dl = new_web_down(_mp4)
        download_coms += 1
        if dl:
            MSG = Video_API.apiCrawlingEnd(_mp4, RES['data']['video_dl_id'])
            print('影片下載完畢', MSG)
    else:
        print('影片下載過囉')

    return True


def list_data(_url):
    ###
    global _host
    global mp4_list
    global mp4_list2
    ###

    soup = _web_(_url)
    # print(soup)
    # mb hdy
    div_mb_hdy = soup.find_all('div', {'class': 'mb hdy'})
    # print(div_mb_hdy)
    res = False
    for item in div_mb_hdy:
        _href = str(_host) + item.find('a').get('href')
        res = _sigle__page(_href)
        # print(_href)
    if res:
        print('掃描完畢', '準備下載')
        # print(mp4_list2)
        # new_web_down(mp4_list)

    return True


_url = 'https://www.epbeast.com/category/4k-porn/1/'
list_data(_url)
# new_web_down('https://www.epbeast.com/dload/Zilm0NTNH5S/240/2478261-240p.mp4')
# ------------------------------------------------------------

# _url = 'https://www.epbeast.com/hd-porn/ax1bjbYiuNv/Czech-Casting-2017/'
# _sigle__page(_url)
# new_web_down(mp4_list)

# https://www.epbeast.com/category/4k-porn/1/~ 5

# error https://www.epbeast.com/category/4k-porn/6/
# ------------------------------------------------------------------
# print(mp4_list2)
# mp4_list = ['https://www.epbeast.com/dload/9lw7IAHLOH9/2160/2487061-2160p.mp4', 'https://www.epbeast.com/dload/w2M2ZX9pZaJ/2160/2487080-2160p.mp4', 'https://www.epbeast.com/dload/MGBA2tt0gtx/1440/2480668-1440p.mp4',
#             'https://www.epbeast.com/dload/4iaNkDoPdVc/1440/2480588-1440p.mp4', 'https://www.epbeast.com/dload/Zilm0NTNH5S/2160/2478261-2160p.mp4', 'https://www.epbeast.com/dload/OOw8ExDEWXp/1440/2479636-1440p.mp4', 'https://www.epbeast.com/dload/jpqDmvh3VOy/1440/2478263-1440p.mp4']
# new_web_down(mp4_list)

# new_list = [['https://www.epbeast.com/dload/9lw7IAHLOH9/240/2487061-240p.mp4', 'https://www.epbeast.com/dload/w2M2ZX9pZaJ/240/2487080-240p.mp4'], ['https://www.epbeast.com/dload/MGBA2tt0gtx/240/2480668-240p2480668-240p.mp4', 'https://www.epbeast.com/dload/4iaNkDoPdVc/240/2480588-240p.mp4'], ['https://www.epbeast.com/dload/Zilm0NTNH5S/240/2478261-240p.mp4', 'https://www.epbeast.com/dload/OOw8ExDEWXp/240/2479636-240p.mp4']]
# for target_list in new_list:
#     print(target_list)
