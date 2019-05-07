##########
import Cofig
import Bssoup
import CustomEncryption
import Log_save
import Coffig
import Check_video_mins
import Video_API
#####
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


def _web_(___url):

    # d = save_or_check(___url)
    # if d == False:
    #     print('抓過囉')
    #     return False

    soup = False
    ####
    chrome_path = "chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--log-level=3")  # fatal

    try:
        web = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
        web.get(___url)
        time.sleep(1)
        # kt_player  onclik
        web.find_element_by_id('kt_player').click()
        # i-play  onclik
        # driver.find_element_by_css_selector('.i-play').click()

        # time.sleep(1)
        # web.execute_script('load_player()')
        time.sleep(30)
        # time.sleep(5)
        # web.find_element_by_class_name('skip_button').click()
        # # time.sleep(300)
        # time.sleep(10)

    except:
        web.quit()
        print('error')
        return _web_(___url)
    try:
        time.sleep(5)
        html = web.page_source
        soup = BeautifulSoup(html, 'html.parser')
        web.quit()
    except:
        # pass
        web.quit()

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

    # print(soup)
    video_src = soup.find(
        'div', {'class': 'fp-player'}).find('video').get('src')
    # video_src = div.find('video').get('src')
    # print(video_src)
    # return True
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
    video_src = soup.find(
        'div', {'class': 'fp-player'}).find('video').get('src')
    # print(video_src)
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


__url = 'https://www.3movs.com/videos/1/'
list_data(__url)
