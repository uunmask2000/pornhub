from subprocess import check_output
from glob import glob
from os.path import join
import requests
import lxml
import re
import json
import time
import os
import hashlib
import random
import datetime
import sys

from urllib import parse
from bs4 import BeautifulSoup
from pget.down import Downloader
from urllib.request import urlretrieve
from urllib.parse import urlparse

import threading
import time
##
import urllib.request


###
# 'https://www.pornhub.com/video?c=111&o=cm&hd=1&max_duration=30&page=2'
# 資料夾路徑
_path_list = []
Host = "https://www.pornhub.com/view_video.php?viewkey="
Main_url = 'https://www.pornhub.com/video?o=ht'
Home_url = 'https://www.pornhub.com/'
Host_name = 'pornhub'
# 切換本地代理次數
_切換本地代理次數 = 0

#  代理清單
_proxy_list = []
#  切換不走代理
_proxy_status = 0
#  切換use次數
_proxy_count = 0

# 下載數量
_movie_row = 0
# 錯誤次數
_error_row = 0


_s = [
    111,
    7,
    13,
    90
]
# -------------------------------


def on_proxies():
    str_ = "{}://{}:{}"
    # url = 'https://raw.githubusercontent.com/stamparm/aux/master/fetch-some-list.txt'
    # r = requests.get(url)
    # json_ = r.json()
    # proxies_ = get_dict('http', json_)
    # proxies = proxies_[0]
    # # str_ = proxies['proto'] + "://"
    # str_ = str(proxies['proto']) + "://" + \
    #     str(proxies['ip']) + ":" + str(proxies['port'])

    return str_


def _proxy():
    global _proxy_list
    _proxy_list_ = []
    ####
    if len(_proxy_list) != 0:
        # _s = random.choice(_proxy_list)
        # print(len(_proxy_list))
        _s = _proxy_list.pop(0)
        # print(len(_proxy_list))
        return _s
    else:
        print('空了')
        print(len(_proxy_list))
        # __EEE = random.randint(1, 10)
        # print(__EEE)
        # if __EEE >= 6:
        #     return {}
        # ###
        # pass
    #####
    _url = 'https://www.us-proxy.org/'
    html = requests.get(_url).content
    soup = BeautifulSoup(html, 'html.parser')
    _s = ""
    _tbody = soup.find('table').find('tbody')
    _tr = _tbody.find_all('tr')
    # print(len(_tr))
    for tr in _tr:
        # print(tr)
        # print(len(tr))
        td_ = tr.find_all('td')
        # if td_[6].text == 'yes' and td_[4].text == 'anonymous':
        if td_[6].text == 'yes':
            _s = str('https://' + td_[0].text + ':' + td_[1].text)
            _proxy_list_.append(_s)
    ####
    # print(_proxy_list_)
    _proxy_list = _proxy_list_
    if len(_proxy_list_) == 0:
        return {}
    # _s = random.choice(_proxy_list)
    # 利用pop
    # print(len(_proxy_list))
    _s = _proxy_list.pop(0)
    # print(len(_proxy_list))
    # print(_proxy_list)
    # print(_s)
    # _s = random.choice(_proxy_list)
    # print(_proxy_list)
    return _s


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


def get_soup(url, c=1, __d=0, _p=0):
    # print('get_soup')
    global _error_row
    global _proxy_list
    global _proxy_status
    global _proxy_count
    global _切換本地代理次數
    # logging.info('get_soup herf' + url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }

    ###
    ##
    proxies = {}
    # proxies['http'] = on_proxies()
    var_ = _proxy()
    proxies['https'] = var_
    print(var_)
    if __d == 0:
        ##
        # proxies['http'] = on_proxies()
        if var_ == "":
            print('T1')
            # proxies = {}
            print('代理1' + str(len(_proxy_list)))
            # return get_soup(url, c, 1)
        else:
            print('T2')
    if _proxy_count > 50:
        if _切換本地代理次數 > 10:
            print('安全停止')
            sys.exit(1)
        ###
        _切換本地代理次數 += 1
        _proxy_count = 0
        __d = 0
        _proxy_status = 0
        print('本地代理超過50，切換回外部代理')

    # proxies['https'] = 'https://50.73.137.241'
    # print(_proxy_list)
    # 錯誤三次
    c += +1
    ##
    html = ''
    soup = False
    # 剩餘數量
    _proxy_list_count = len(_proxy_list)
    print(str('剩餘數量')+str(_proxy_list_count))
    ###
    if _proxy_list_count == 0 and __d == 1:
        # 暫時不走代理
        print('暫時不走代理')
        _proxy_status = 1
        proxies = {}
        # _proxy_status
        # 累積次數
        _proxy_count += 1
    elif _proxy_status == 1:
        print('暫時不走代理')
        proxies = {}
        _proxy_count += 1
    else:
        ##
        # print('清空計算器')
        # 清空計算器
        _proxy_count = 0

    ##
    if len(_proxy_list) == 0:
        print('代理1' + str(len(_proxy_list)))
        get_soup(url, c, 1)

    try:
        html_ = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        html = html_.content
        soup = BeautifulSoup(html, 'html.parser')
    except:
        print('重新獲取')
        return get_soup(url, c)

    # print(proxies)
    # while html == '':
    #     try:
    #         html_ = requests.get(url, headers=headers,
    #                              proxies=proxies, timeout=10)
    #         # print(html_.status_code)
    #         html = html_.content
    #         time.sleep(1)
    #         soup = BeautifulSoup(html, 'html.parser')
    #         # print(soup)
    #         _se = soup.find('body').text.strip().replace("", "")
    #         print(_se)
    #         # addlist
    #         _proxy_list.append(var_)
    #     except:
    #         time.sleep(1)
    #         # 刪除代理
    #         __lows = len(_proxy_list)
    #         __lows_c = 0
    #         print('重新獲取')
    #         # while var_ in _proxy_list:
    #         #     if __lows_c >= __lows:
    #         #         get_soup(url, c, 1)
    #         #     ##
    #         #     # print('刪除代理' + str(__lows_c))
    #         #     # print(var_)
    #         #     _proxy_list.remove(var_)
    #         #     __lows_c += 1
    #         # if var_ in _proxy_list:
    #         #     print('刪除代理')
    #         #     _proxy_list.remove(var_)
    #         # else:
    #         #     print(var_)
    #         #     print(_proxy_list)

    #         # 判斷
    #         # print(_proxy_list)
    #         if len(_proxy_list) == 0:
    #             print('代理1' + str(len(_proxy_list)))
    #             get_soup(url, c, 1)
    #         else:
    #             print('代理0' + str(len(_proxy_list)))
    #             get_soup(url, c)

    ###
    if _p == 1:
        return html
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


def json_dict():
    # json 格式
    post_dict = {
        'time': "",  # 時間
        'sig': "",  # 加蜜
        'name': "",  # Title
        'area': "",
        'cate': "",  # 分類
        'year': "2019",
        'director': "",
        'actor': "",
        'type': "",
        'total': "",
        'cover_url': "",  # 封面
        'grade': "",  # 分數
        'mins': "",
        'source_url': "",
        'source_url_old': "",
        'resolution': "",
        'part': "",
        'intro': ""
    }
    return post_dict


def parseURL(ph_key, _type=1):
    # return False
    # 解析
    url = Host + ph_key
    # print(url)
    # dom = requests.get(url).content
    dom = get_soup(url, 1, 0, 1)
    # print(dom.decode("utf-8"))
    #     result = re.search(
    #         '"quality":"720","videoUrl":"(.*?)"},', dom.decode("utf-8"))

    try:
        result_ = re.search('"videoUrl":"(.*?)"},', dom.decode("utf-8"))
        # print(result_)
        result = result_.group(1).replace('\\', '')
        url = str(result)
        return url
    except:
        return False


def download(url, filename, chunk_count):
    # print(str(url) + str(filename))
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    if os.path.isfile(filename):
        return False
    else:
        print(str(filename))
        proxies = {}
        # proxies['http'] = on_proxies()
        proxies['https'] = _proxy()
        # print(proxies)
        ###
        # downloader = Downloader(url, filename, chunk_count, True, headers, proxies)
        downloader = Downloader(url, filename, chunk_count, True)
        downloader.start_sync()
    return True


def singe_2_download_2json(title, V_path, j_path, url, i_path=''):
    json_dict_ = json_dict()
    t = create_time()
    json_dict_['name'] = title
    json_dict_['time'] = t
    json_dict_['sig'] = create_sign(t)
    json_dict_['source_url'] = V_path
    json_dict_['cover_url'] = i_path
    json_dict_['source_url_old'] = url
    # 下載影片
    download(url, V_path, 10)
    # 檢查 影片
    json_dict_['mins'] = video_time(V_path)
    # 下載json
    write_json_file(json_dict_, j_path)
    global _movie_row
    _movie_row += 1
    # 清潔
    os.system("cls")
    print('清空畫面')
    # 清潔
    print('下載完成' + str(_movie_row))
    return True


def data_list(url):
    # print(url)
    soup = get_soup(url)
    div_wrap = soup.find_all('div', {'class': 'phimage'})
    # print(div_wrap)
    print(len(div_wrap))
    # return True
    ###
    ##
    for h_ in div_wrap:
        href_ = h_.find('a').get('href')
        title_ = h_.find('a').get('title')
        img_ = h_.find('a').find('img').get('data-src')
        _d = h_.find(
            'div', {'class': 'marker-overlays js-noFade'}).find('var').text.split(':', 1)
        # print(_d)
        if int(_d[0]) < 5:
            # pass
            print('低於5分')
            continue
        elif int(_d[0]) > 90:
            print('高於90分')
            continue
        else:
            key_1 = href_.replace('/view_video.php?viewkey=', '')
            key_ = pas_(href_, 'viewkey')
            # print(str(href_) + ' : ' + str(title_) + ' : ' + str(key_))
            # print(str(title_))

            url_ = parseURL(key_)
            ##
            # _v_v = str(_path_list[0]) + str(_key) + str('.mp4')
            # _v_j = str(_path_list[1]) + str(_key) + str('.json')
            # _v_i = str(_path_list[2]) + str(_key) + str('.jpg')
            # global pornhub_path_v
            # global pornhub_path_j
            global _path_list
            pornhub_path_v = str(_path_list[0])
            pornhub_path_j = str(_path_list[1])
            pornhub_path_i = str(_path_list[2])

            try:
                # pass
                path_i = pornhub_path_i + str(key_) + os.path.splitext(img_)[1]
            except:
                # pass
                path_i = pornhub_path_i + str(key_) + str('.jpg')
                # print(path_v)
            res = True
            if url_ == False:
                print('找不到網址1 :' + str(href_))
                # print(str(href_) + ' : ' + str(title_) + ' : ' + str(key_))
                res = False
                continue
            else:
                u = urlparse(url_)
                ext = os.path.splitext(u.path)[1]
                if ext != '.mp4':
                    print('找不到網址 2:' + str(href_))
                    continue
                else:
                    res = True
                    print('找網址 :' + str(href_))
                    ###
                    path_v = pornhub_path_v + str(key_) + str(ext)
                    path_j = pornhub_path_j + str(key_) + '.json'
                    ##
                    do_create_img(img_, path_i)
                    singe_2_download_2json(
                        title_, path_v, path_j, str(url_), str(path_i))
    res = True
    return res


def do_create_img(content, img_name):
    if content is None:
        return False
    # with open(img_name, 'wb') as file:  # 以byte的形式將圖片數據寫入
    #     file.write(content)
    #     file.flush()
    #     file.close()  # close file
    urlretrieve(content, img_name)
    return img_name


def pas_(url, key):
    parsed = parse.parse_qs(parse.urlsplit(url).query)
    data_ = dict(parsed)[key]
    data = data_[0]
    return data


# ------------------------------------------------------------------------------
# 先建立資料夾
# path = 'path/'
# mkdir_m(path)
# ###
# now_date = datetime.datetime.now().strftime("%Y%m%d")
# path = 'path/' + now_date + '/'
# mkdir_m(path)

# pathJ = path + 'jsons/'
# mkdir_m(pathJ)
# pathV = path + 'videos/'
# mkdir_m(pathV)
# pathI = path + 'images/'
# mkdir_m(pathI)

# ###
# pornhub_path_v_ = path + 'videos/' + Host_name + '/'
# mkdir_m(pornhub_path_v_)
# pornhub_path_j_ = path + 'jsons/' + Host_name + '/'
# mkdir_m(pornhub_path_j_)
# pornhub_path_i_ = path + 'images/' + Host_name + '/'
# mkdir_m(pornhub_path_i_)

# pornhub_path_v = pornhub_path_v_
# mkdir_m(pornhub_path_v)
# pornhub_path_j = pornhub_path_j_
# mkdir_m(pornhub_path_j)
# pornhub_path_i = pornhub_path_i_
# mkdir_m(pornhub_path_i)

# 評到
chanel = 105
# 重跑次數
Re_row = 0


def guard(start, range_):
    global chanel
    global Re_row
    global Main_url

    if Re_row > 2:
        return True

    MAX = range_+1
    for i in range(start, MAX):
        _url = Main_url + '&page={}'.format(
            i)
        # _url = 'https://www.pornhub.com/video?c={}&max_duration=20&page={}'.format(
        #     chanel, i)
        time.sleep(1)
        # print(_url)
        res = data_list(_url)
        # if res:
        #     print('END' + str(i))
        # else:
        #     print('ERROR' + str(i))
    Re_row += 1
    print('重跑一次' + str(Re_row))
    # return guard(start, range_)
# ----------------------


def run_pool(x):
    MAX = 999
    Main_url = 'https://www.pornhub.com/video?c={}&page={}'
    i = 0
    while True:
        if i > MAX:
            return True
        i += 1
        _url = Main_url.format(x, i)
        print(_url)
        res = data_list(_url)
        pass
    print('跑完' + str(Re_row))
    return True


def run_pool_2(x, y):
    Main_url = 'https://www.pornhub.com/video?page={}'
    for r in range(x, y+1):
        _url = Main_url.format(r)
        # print(_url)
        time.sleep(1)
        res = data_list(_url)
    return True

###


class myThread (threading.Thread):
    def __init__(self, threadID, name, s):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.s = s
        self.e = s

    def run(self):
        print("开始线程：" + self.name)
        run_pool_2(self.s,  self.e)
        print("退出线程：" + self.name)


# ffmpeng 需要安裝


def video_time(file_name):
    # file_name = "TEST\ph5a8b7ec93d417.mp4"

    try:
        a = str(check_output('ffprobe -i  "'+file_name +
                             '" 2>&1 |findstr "Duration"', shell=True))
    except:
        print('檔案刪除')
        try:
            os.remove(file_name)
        except:
            print('檔案刪除出現異常')
        return 0
    # For Windows

    # For Linux
    # a = str(check_output('ffprobe -i  "'+file_name+'" 2>&1 |grep "Duration"',shell=True))
    print('檔案OK')
    a = a.split(",")[0].split("Duration:")[1].strip()
    h, m, s = a.split(':')
    duration = int(h) * 3600 + int(m) * 60 + float(s)
    # print(duration)
    return duration


def r1():
    guard(1, 1000000)
    return True


def r2():
    threadLock = threading.Lock()
    threads = []
    global _s
    __let = _s
    _i = 0
    for rows in __let:
        _i += 1
        thread = myThread(_i, "Thread-"+str(_i), rows)
        thread.start()
        threads.append(thread)

    # 创建新线程
    # thread1 = myThread(1, "Thread-1", 1)
    # thread2 = myThread(2, "Thread-2", 2)
    # thread3 = myThread(3, "Thread-3", 241)
    # 开启新线程
    # thread1.start()
    # thread2.start()
    # thread3.start()
    # 添加线程到线程列表
    # threads.append(thread1)
    # threads.append(thread2)
    # threads.append(thread3)
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("退出主线程")
    while True:
        pass
    return True


def r3():
    global Home_url
    Min_t = 10
    MAX_t = 20
    ##
    threads = []

    # 0*10 + 1  ~ 1*10
    # 1*10 + 1  ~ 2*10
    for r in range(Min_t, MAX_t):
        _s = r * 10 + 1
        _e = (r+1)*10
        ##
        t = threading.Thread(target=run_pool_2, args=(_s, _e,))
        threads.append(t)
        t.start()
        # print(r)
    for t in threads:
        t.join()
    print("退出主线程")
    while True:
        pass

    # https://www.pornhub.com/video?page=1

    # https://www.pornhub.com/video?page=101

    # https://www.pornhub.com/video?page=201

    return True


def _c_():
    url = 'https://httpbin.org/ip'
    for i in range(1, 100):
        soup = get_soup(url)
        print(soup)

    return True


def run_pool_3(_url, x, y):
    Main_url = _url + str({})
    page_ = 1
    while True:
        page_ += 1
        _url = Main_url.format(page_)
        print(_url)
        time.sleep(2)
        res = data_list(_url)
    # for r in range(x, y+1):
    #     _url = Main_url.format(r)
    #     # print(_url)
    #     time.sleep(1)
    #     res = data_list(_url)
    return True


def r4():

    threads = []
    __list_key = [
        # 'https://www.pornhub.com/hd?page=',
        'https://www.pornhub.com/video?c=3&page=',
        'https://www.pornhub.com/video?c=15&page=',
        'https://www.pornhub.com/video?c=16&page=',
        # 'https://www.pornhub.com/video?c=21&page=',
        # 'https://www.pornhub.com/video?c=27&page=',
        # 'https://www.pornhub.com/video?c=29&page=',
    ]
    _s = 25
    _e = 50

    ####
    for _url in __list_key:
        t = threading.Thread(target=run_pool_3, args=(_url, _s, _e,))
        threads.append(t)
        t.setName(_url)
        t.start()
    for t in threads:
        t.join()
    print("退出主线程")
    while True:
        pass

    return True


def _init_(Host_name):
    global _path_list
    # 先建立資料夾
    path = 'path/'
    mkdir_m(path)
    ###
    now_date = datetime.datetime.now().strftime("%Y%m%d")
    path = 'path/' + now_date + '/'
    mkdir_m(path)

    _p = path  + '/' +  Host_name + '/'
    mkdir_m(_p)

    _let_key = [
        'videos/',
        'jsons/',
        'images/'
    ]

    for _a in _let_key:
        _s = _p + _a
        mkdir_m(_s)
        ##
        _path_list.append(_s)
    return _path_list


if __name__ == '__main__':
    print('running')
    # 初始化
    _init_(Host_name)
    _proxy_list_ = []
    # init
    # _proxy
    # 單線程
    r1()  # 有問題嘞
    # 多線程
    # r2() 有問題了
    # 多線程 首頁
    # r3()  有問題嘞
    # 多線程 + 主題
    # r4()
    # ----------------
    # _c_()
    # v = _proxy()
    # print(v)
    print('ending')
