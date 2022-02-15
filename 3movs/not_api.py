'''
Arthur       : kk
Date         : 2022-02-15 15:17:38
LastEditTime : 2022-02-15 16:22:58
LastEditors  : your name
Description  : 自動生成 [嚴格紀律 Description]
FilePath     : /3movs/not_api.py
嚴格紀律
'''
##########
import Bssoup
import Coffig
import CustomEncryption
#####
import re
import time
import os
from urllib.request import urlretrieve
from urllib.parse import urlparse
import requests
import json
# --------------------------------
from bs4 import BeautifulSoup
# --------------------------------


Bssoup = Bssoup.Bssoup()
Coffig = Coffig.Coffig()
CustomEncryption = CustomEncryption.CustomEncryption()

##
host_url = 'https://www.3movs.com'


def _sigle__page(__url):
    # __url = 'https://www.3movs.com/videos/133597/small-titted-lovenia-lux-gets-her-anus-destroyed/'
    soup = Bssoup.get_soup(__url)
    video_src = soup.find(
        'a', {'class': 'item_drop', 'data-attach-session': 'PHPSESSID'}).get('href')
    print(video_src)
    # 影片下載
    # video_src = 'https://www.3movs.com/get_file/8/d6f54af20d0354e5c795cc2f45962a3ee38a4c2c94/133000/133597/133597_lq.mp4/?download_filename=www.3movs.com---small-titted-lovenia-lux-gets-her-anus-destroyed_lq.mp4'
    name_hash = str(CustomEncryption.b16_encode(video_src))
    name_hash = CustomEncryption.md5_encode(name_hash)
    _v_name = 'video/'+name_hash + (".mp4")
    print(_v_name)
    Coffig.download_(video_src, _v_name)


def list_data(_url):
    soup = Bssoup.get_soup(_url)
    if soup == False:
        print('错误')
        return False
    # print(soup)
    # item  div
    list = soup.find('div', {'id': 'list_videos_common_videos_list_items'}).find_all(
        'a', {'class': 'wrap_image'})
    # print(len(list))
    for list_ in list:
        _herf = list_.get('href')
        print(_herf)
        _sigle__page(_herf)

    return True


__url = 'https://www.3movs.com/categories/teen/{}/'
list_data(__url.format(1,))
