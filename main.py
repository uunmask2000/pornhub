# import base64
import base64
import Cofig
import Bssoup
import CustomEncryption
# ###############################################
import os
import re
import json
from urllib.request import urlretrieve
from urllib.parse import urlparse
# ###############################################
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import time
from bs4 import BeautifulSoup


# ###############################################
_temple_xhr = 'http://www.yzz13.com/?mode=async&function=get_block&block_id=list_videos_most_recent_videos&sort_by=post_date&from={}'
# 01 -09
_xhr_list = []
# xhr = ''
_start = 1
_end = 11
####
downloads = 0


def run_pool():
    global _xhr_list
    global _temple_xhr
    global _start
    global _end
    for _list in range(_start, _end + 1):
        if _list < 10:
            _str = str(0) + str(_list)
        else:
            _str = str(_list)

        _xhr_list.append(_temple_xhr.format(_str,))

    return _xhr_list


def _web_(___url):
    soup = False
    ####
    chrome_path = "chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--hide-scrollbars')
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--log-level=3")  # fatal
    web = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
    web.get(___url)
    try:
        html = web.page_source
        soup = BeautifulSoup(html, 'html.parser')
    except:
        pass

    return soup


def stie_page(___url):
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

    _soup = _web_(___url)
    if _soup == False:
        print('錯誤')
        return False
    ###
    _json_dict['intro'] = ___url
    _json_dict['time'] = Cofig.create_time()
    _json_dict['sig'] = Cofig.create_sign(_json_dict['time'])

    # <h1>男性宅に訪問どこが感じるかあててみてネ</h1>
    h1_ = str(_soup.find('h1').text)
    _json_dict['name'] = h1_

    # 影片路徑
    video_src = _soup.find('video',  {'class': 'fp-engine'}).get('src')
    # 圖片路徑
    _img_src = _soup.find('div', {'class': 'no-player'}).find('img').get('src')
    _json_dict['name'] = h1_
    _json_dict['source_url_old'] = video_src
    _json_dict['cover_url_old'] = _img_src

    # print(h1_)
    if len(h1_) >= 20:
        h1_ = h1_[:20]
    _v_name = str(_path_list[0]) + \
        CustomEncryption.b16_encode(h1_) + str('.mp4')
    _s_name = str(_path_list[1]) + \
        CustomEncryption.b16_encode(h1_) + str('.json')
    _i_name = str(_path_list[2]) + \
        CustomEncryption.b16_encode(h1_) + str('.jpg')

    _json_dict['source_url'] = _v_name
    _json_dict['cover_url'] = _i_name

    # 影片下載
    download_(video_src, _v_name)
    # 圖片下載
    do_create_img(_img_src, _i_name)
    # json 產生
    # print(_json_dict)
    write_json_file(_json_dict, _s_name)
    downloads += 1
    # 清潔
    os.system("cls")
    print(str('下載成功') + str(downloads))
    return True


def list_page(__url):
    soup = Bssoup.get_soup(__url)
    if soup == False:
        print('錯誤')
        return False
    # ------------------------------
    a_list = soup.find('div', {'class': "list-videos"}).find_all('a')
    for a_tag in a_list:
        _herf = a_tag.get('href')
        print(_herf + str('閱讀'))
        stie_page(_herf)

    return True


def download_(url, path):
    print('start  ：')
    start = time.time()
    if os.path.isfile(path):
        print('檔案存在')
    else:
        # 当把get函数的stream参数设置成False时，
        # 它会立即开始下载文件并放到内存中，如果文件过大，有可能导致内存不足。
        # 当把get函数的stream参数设置成True时，它不会立即开始下载，
        # 使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载
        r = requests.get(url, stream=True)
        f = open(path, "wb")
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
                f.flush()
                # iter_content：一块一块的遍历要下载的内容
                # iter_lines：一行一行的遍历要下载的内容
                # 这两个函数下载大文件可以防止占用过多的内存，因为每次只下载小部分数据
    end = time.time()
    print('Finish in ：', end - start)
    return True


def do_create_img(content, img_name):
    if content is None:
        return False
    # with open(img_name, 'wb') as file:  # 以byte的形式將圖片數據寫入
    #     file.write(content)
    #     file.flush()
    #     file.close()  # close file
    urlretrieve(content, img_name)
    return img_name


def write_json_file(post_dict_, path):
    # print(path)
    with open(path, 'w') as fp:
        json.dump(post_dict_, fp)
    return True


# 設定
Cofig = Cofig.Cofig(path='path', Host_name='www_yzz13_com')
Bssoup = Bssoup.Bssoup()
CustomEncryption = CustomEncryption.CustomEncryption()
# 路徑
_path_list = Cofig.get_path_list()
# print(_path_list)
# 範本
_json_dict = Cofig.json_dict()
# print(_json_dict)

##
_A = run_pool()
for item in _A:
    list_page(item)


# print(_A)
# __url = 'http://www.yzz13.com/?mode=async&function=get_block&block_id=list_videos_most_recent_videos&sort_by=post_date&from=11'
# list_page(__url)
