# list
# https://raw.githubusercontent.com/stamparm/aux/master/fetch-some-list.txt
import hashlib
import os
import time
import json
import re
import requests
import random
import glob
import os.path
import datetime
##
from pySmartDL import SmartDL
from bs4 import BeautifulSoup
from urllib import parse

###########
Host = "https://www.pornhub.com/view_video.php?viewkey="
Host_name = 'pornhub'


def mkdir_m(Path):
    _path = './path'
    # 檢查目錄是否存在
    if os.path.isdir(_path):
        # print("目錄存在。")
        pass
    else:
        # print("目錄不存在。")
        os.mkdir(_path)

    # os.mkdir(Path)
    # 檢查目錄是否存在
    if os.path.isdir(Path):
        # print("目錄存在。")
        return False
    else:
        # print("目錄不存在。")
        os.mkdir(Path)
        return True


# 先建立資料夾
path = 'path/'
mkdir_m(path)
###
now_date = datetime.datetime.now().strftime("%Y%m%d")
path = 'path/' + now_date + '/'
mkdir_m(path)

pathJ = path + 'jsons/'
mkdir_m(pathJ)
pathV = path + 'videos/'
mkdir_m(pathV)
pathI = path + 'images/'
mkdir_m(pathI)
###
pornhub_path_v_ = path + 'videos/' + Host_name + '/'
mkdir_m(pornhub_path_v_)
pornhub_path_j_ = path + 'jsons/' + Host_name + '/'
mkdir_m(pornhub_path_j_)
pornhub_path_i_ = path + 'images/' + Host_name + '/'
mkdir_m(pornhub_path_i_)
pornhub_path_v = pornhub_path_v_ + '/'
mkdir_m(pornhub_path_v)
pornhub_path_j = pornhub_path_j_ + '/'
mkdir_m(pornhub_path_j)
pornhub_path_i = pornhub_path_i_ + '/'
mkdir_m(pornhub_path_i)

# 評到
chanel = 111
# 重跑次數
Re_row = 0

##############


def on_proxies():
    url = 'https://raw.githubusercontent.com/stamparm/aux/master/fetch-some-list.txt'
    r = requests.get(url)
    json_ = r.json()
    proxies_ = get_dict('http', json_)
    proxies = proxies_[0]
    # str_ = proxies['proto'] + "://"
    # str_ = str(proxies['proto']) + "://" + \
    #     str(proxies['ip']) + ":" + str(proxies['port'])
    str_ = ""
    return str_


def get_dict(key, dict_):
    new_ = []
    for i in dict_:
        if i['proto'] == key and i['anonymity'] == 'high':
            # return i
            new_.append(i)
        else:
            pass
    new = random.sample(new_, 1)
    return new


# url = 'https://raw.githubusercontent.com/stamparm/aux/master/fetch-some-list.txt'
# r = requests.get(url)
# json = r.json()
# print(on_proxies())

# ###
# json = get_dict('http', json)
# print(json)


###
# 'https://www.pornhub.com/video?c=111&o=cm&hd=1&max_duration=30&page=2'


def get_soup(url, c=1):
    # logging.info('get_soup herf' + url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }

    proxies = {
        "http":  ""
    }
    proxies['http'] = on_proxies()
    proxies = {}
    print(proxies)

    # 錯誤三次
    if c > 3:
        return False
    else:
        pass
    c += +1
    ##
    html = ''
    soup = False
    while html == '':
        try:
            html = requests.get(url, headers=headers, proxies=proxies).content
            soup = BeautifulSoup(html, 'html.parser')
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(1)
            # get_soup(url, c)
            print("Was a nice sleep, now let me continue...")
            continue
    return soup


def write_json_file(post_dict_, path):
    # print(path)
    with open(path, 'w') as fp:
        json.dump(post_dict_, fp)
    return True


def create_time():
    # 獲取時間
    return int(time.time())  # 1


def create_sign(t):
    # 建立sign
    sig = "sc%7*g{}@!$%".format(t)
    md = hashlib.md5()
    md.update(sig.encode(encoding='utf-8'))
    sign = md.hexdigest()  # 2
    return sign


def json_dict():
    # json 格式
    post_dict = {
        'time': "",  # 時間
        'sig': "",  # 加蜜
        'name': "",  # Title
        'area': "us",
        'cate': "us",  # 分類
        'year': "2019",
        'director': "",
        'actor': "",
        'type': "movie",
        'total': "",
        'cover_url': "",  # 封面
        'grade': "",  # 分數
        'mins': "",
        'source_url': "",
        'resolution': "",
        'part': "",
        'intro': ""
    }
    return post_dict


def parseURL(ph_key, _type=1):
    # return False
    # 解析
    dom = requests.get(Host + ph_key).content

    if _type == 1:
        result = re.search(
            '"quality":"720","videoUrl":"(.*?)"},', dom.decode("utf-8"))
    else:
        return False
    try:
        return str(result.group(1).replace('\\', ''))
    except:
        return False


def download(url, filename, chunk_count):
    # print(str(url) + str(filename))
    if os.path.isfile(filename):
        return False
    else:
        downloader = Downloader(url, filename, chunk_count)
        downloader.start_sync()
    return True


def singe_2_download_2json(title, V_path, j_path, url):
    # print(title)
    # print(V_path)
    # print(url)
    json_dict_ = json_dict()
    t = create_time()
    json_dict_['name'] = title
    json_dict_['time'] = t
    json_dict_['sig'] = create_sign(t)
    json_dict_['source_url'] = V_path
    # 下載影片
    # download(url, V_path,  10)
    new_download(url, V_path)
    # 下載json
    write_json_file(json_dict_, j_path)
    return True


def data_list(url):
    soup = get_soup(url)
    if soup == False:
        time.sleep(60)
        return False
    else:
        pass
    # print(soup)
    div = soup.find('div', {'class': 'nf-videos'})
    hi = div.find('h1').text
    # print(str(hi)) wrap + phimage
    div_wrap = soup.find_all('div', {'class': 'phimage'})
    # print(div_wrap)
    # print(len(div_wrap))
    # return True
    for h_ in div_wrap:
        href_ = h_.find('a').get('href')
        title_ = h_.find('a').get('title')
        key_1 = href_.replace('/view_video.php?viewkey=', '')
        key_ = pas_(href_, 'viewkey')
        # print(str(href_) + ' : ' + str(title_) + ' : ' + str(key_))
        print(str(title_))
        url_ = parseURL(key_)
        print(key_ + ' ' + key_1)
        # print(type(url_))
        ##
        global pornhub_path_v
        global pornhub_path_j
        path_v = pornhub_path_v + str(key_) + '.mp4'
        path_j = pornhub_path_j + str(key_) + '.json'
        if url_ == False:
            print('找不到網址 :' + str(href_))
            # print(str(href_) + ' : ' + str(title_) + ' : ' + str(key_))
            res = False
            continue
        else:
            # res = True
            res = singe_2_download_2json(title_, path_v, path_j, str(url_))
    return res


def pas_(url, key):
    parsed = parse.parse_qs(parse.urlsplit(url).query)
    data_ = dict(parsed)[key]
    data = data_[0]
    return data


def guard(start, range_):
    global chanel
    global Re_row

    if Re_row > 2:
        return True
    MAX = range_+1
    for i in range(start, MAX):
        _url = 'https://www.pornhub.com/video?c={}&page={}'.format(chanel, i)
        print(_url)
        res = data_list(_url)
        if res:
            print('END')
        else:
            print('ERROR')
    Re_row += 1
    # print('重跑一次' + str(Re_row))
    # return guard(start, range_)

    return True


def new_download(url, path, c=1):
    # url = "https://github.com/iTaybb/pySmartDL/raw/master/test/7za920.zip"
    # dest = "C:\\Users\\user\\Documents\\dw2"  # or '~/Downloads/' on linux
    # dest = './path/videos/pornhub'
    dest = pornhub_path_v
    ##
    currentDirFile(dest)
    if c > 3:
        return False
    else:
        pass
    # print(url)
    # obj = SmartDL(url, dest)
    obj = SmartDL(url, dest, progress_bar=True)
    # obj.start(blocking=True)
    try:
        # obj.start()
        obj.start(blocking=True)
    except:
        c += 1
        new_download(url, path)

    # [*] 0.23 Mb / 0.37 Mb @ 88.00Kb/s [##########--------] [60%, 2s left]
    path_ = obj.get_dest()
    path_n = os.rename(path_, path)
    # print(path_)
    # print(path_n)
    print(obj.isSuccessful())
    return path_n


def currentDirFile(dir):
    fileNames = os.listdir(dir)
    for fn in fileNames:
        fullFileName = os.path.join(dir, fn)
        if not os.path.isdir(fullFileName):
            delFile(fullFileName)
        else:
            currentDirFile(fullFileName)


def delFile(filePath):
    # 分隔字尾名
    formatName = os.path.splitext(filePath)[1]
    # print(formatName)
    if formatName != '.mp4' and filePath.split('/')[-1] != '.DS_Store':
        os.remove(filePath)


# 跑兩頁
guard(1, 2)
# print(on_proxies())
# nnn()
# dest = './path/videos/pornhub'
##
# currentDirFile(dest)


# https://www.pornhub.com/video?c=111&o=cm&hd=1&max_duration=30&page=1- 10
# _url = 'https://www.pornhub.com/video?c=111&page=2'
# res = data_list(_url)

# if res:
#     print('END')
# else:
#     print('ERROR')


# _url = 'https://www.pornhub.com/video?c=111&page=2'
# html = requests.get(_url).content
# soup = BeautifulSoup(html, 'html.parser')
# print(soup
