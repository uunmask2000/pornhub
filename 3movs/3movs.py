##########
import Cofig
import Bssoup
import CustomEncryption
import Log_save
import Coffig
import Check_video_mins
import Video_API
#####
import re
import time
import os
from urllib.request import urlretrieve
from urllib.parse import urlparse
import requests
import json
# --------------------------------
# ------
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# --------------------------------
# 設定
Video_API = Video_API.Video_API(api_url='http://211.233.25.166:1154/api/')
Cofig = Cofig.Cofig(path='path', Host_name='3movs')
Bssoup = Bssoup.Bssoup()
CustomEncryption = CustomEncryption.CustomEncryption()
Log_save = Log_save.Log_save()
Coffig = Coffig.Coffig()
Check_video_mins = Check_video_mins.Check_video_mins()
# 路徑
_path_list = Cofig.get_path_list()
# print(_path_list)
# 範本
_json_dict = Cofig.json_dict()
# print(_json_dict)

##
host_url = 'https://www.3movs.com'

# 要從2開始
_home_name = ''

##
# Min = 0
# Max = 302

####
downloads = 0
error = 0


def _web_(___url):

    # d = save_or_check(___url)
    # if d == False:
    #     print('抓過囉')
    #     return False

    soup = False
    ####
    chrome_path = "chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--log-level=3")  # fatal
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    chrome_options.add_experimental_option(
        "prefs",  {"profile.managed_default_content_settings.images": 2})

    # try:
    web = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
    web.get(___url)
    time.sleep(1)
    web.find_element_by_id('kt_player').click()
    time.sleep(1)
    html = web.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # a fp-play
    _href = soup.find('a', {'id': 'download_text_link_2'}).get('href')
    if _href is None:
        web.quit()
        return _web_(___url)
        # print(soup)
        # web.quit()
    # except:
    #     print('')
        # return _web_(___url)
        # web.quit()
    # time.sleep(45)
    web.quit()
    return soup


def __list__pages(_url):
    global host_url
    # print(_url)
    soup = Bssoup.get_soup(_url)
    if soup == False:
        print('錯誤')
        return False
    # print(soup)
    _a = soup.find_all('a', {'class': 'thumbnail'})
    print(len(_a))
    for _h in _a:
        _href = str(host_url) + _h.get('href')
        # print(_href)
        _sigle__page(_href)
        Log_save.save_or_check2(_href)

    return True


def _sigle__page(_url):
    RES = Video_API.apiVerificationUrlExist(_url)
    # print(RES)
    if RES == False:
        print('抓過囉')
        return True
    # d = Log_save.save_or_check(_url)
    # if d == False:
    #     print('抓過囉')
    #     return True
    ####
    global _path_list
    global _json_dict
    global downloads
    global error
    '''
    _let_key = [
    'videos/',
    'jsons/',
    'images/'
    ]
    '''
    # soup = Bssoup.get_soup(_url)
    soup = _web_(_url)
    if soup == False:
        print('錯誤')
        return False

    # fp-time-elapsed
    # div_time = soup.find('div', {'class': 'fp-time-elapsed'}).text
    ##
    # if div_time == '00:00':
    #     print(div_time)
    #     print('影片有問題')
    #     return True
    ###
    _json_dict['intro'] = _url
    _json_dict['time'] = Cofig.create_time()
    _json_dict['sig'] = Cofig.create_sign(_json_dict['time'])
    # property   og:title
    title_ = soup.find("title").text
    # print(title_)

    # property og:image
    _img_src = soup.find("meta",  property="og:image").get('content')
    # print(_img_src)
    # print(soup)
    # video_src = soup.find('div', {'class': 'fp-player'}).find('video').get('src')
    video_src = soup.find('a', {'id': 'download_text_link_2'}).get('href')
    # print(video_src)
    if re.search('https://www.3movs.com/get_file', video_src) is None:
        error += 1
        if error > 1:
            print('影片有問題')
            return True
        else:
            print('重新爬取', _url)
            ####
            return _sigle__page(_url)
    # if video_src.re('https://www.3movs.com/get_file')
    # a = 1
    # --------------------------------
    _json_dict['name'] = title_
    _json_dict['source_url_old'] = video_src
    _json_dict['cover_url_old'] = _img_src
    # ---------------------------
    if len(title_) >= 20:
        title_ = title_[:20]
    name_hash = str(CustomEncryption.b16_encode(title_))
    _v_name = str(_path_list[0]) + name_hash + str('.mp4')
    _s_name = str(_path_list[1]) + name_hash + str('.json')
    _i_name = str(_path_list[2]) + name_hash + str('.jpg')
    _json_dict['source_url'] = _v_name
    _json_dict['cover_url'] = _i_name
    # -----------------------------------
    # 影片下載
    Coffig.download_(video_src, _v_name)
    ##
    _video_time = Check_video_mins.video_time(_v_name)
    _json_dict['mins'] = int(_video_time)
    # print(_json_dict)
    # 圖片下載
    Coffig.do_create_img(_img_src, _i_name)
    # json 產生
    # print(_json_dict)
    Coffig.write_json_file(_json_dict, _s_name)
    # downloads += 1
    downloads = Coffig.shwo()
    # 清潔
    # os.system("cls")
    print(str('下載成功') + str(downloads))
    ##
    MSG = Video_API.apiCrawlingEnd(_url, RES['data']['video_dl_id'])
    print('影片下載完畢', MSG)
    time.sleep(5)

    return True


def list_data(_url):
    soup = Bssoup.get_soup(_url)
    if soup == False:
        print('错误')
        return False
    # print(soup)
    # item  div
    div_item = soup.find('div', {'id': 'list_videos_all_videos'}).find_all(
        'div', {'class': 'item'})

    for list_ in div_item:
        _herf = list_.find('a').get('href')
        # print(_herf)
        _sigle__page(_herf)

    return True


# __url = 'https://www.3movs.com/videos/133597/small-titted-lovenia-lux-gets-her-anus-destroyed/'
# _sigle__page(__url)
page = 1
while True:
    page += 1
    __url = 'https://www.3movs.com/videos/{}/'
    # __url = 'https://www.3movs.com/categories/teen/{}/'
    list_data(__url.format(page,))


# __url = 'https://www.3movs.com/videos/1/'
# list_data(__url)

# _v_name = 'path/20190507/3movs/videos/4275737479206272756E65747465204D494C4620.mp4'
# _video_time = Check_video_mins.video_time(_v_name)
# print(_video_time)
