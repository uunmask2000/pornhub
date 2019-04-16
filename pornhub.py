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

Host = "https://www.pornhub.com/view_video.php?viewkey="
Main_url = 'https://www.pornhub.com/video?o=ht'
Home_url = 'https://www.pornhub.com/'
Host_name = 'pornhub'

# 下載數量
_movie_row = 0
# 錯誤次數
_error_row = 0


_s = [111]
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


def get_soup(url, c=1):
    global _error_row
    # logging.info('get_soup herf' + url)
    # 嚴重錯誤
    if _error_row > 5:
        # print('嚴重錯誤 大於五次')
        # os._exit(0)
        pass

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    }
    proxies = {}
    # proxies['http'] = on_proxies()
    proxies['https'] = _proxy()
    # proxies['https'] = 'https://206.189.165.149:3128'

    # 錯誤三次
    if c > 3:
        _error_row += 1
        return False
    else:
        pass
    c += +1
    ##
    html = ''
    soup = False
    # print(proxies)
    while html == '':
        try:
            html = requests.get(url, headers=headers,
                                proxies=proxies, timeout=1).content
            soup = BeautifulSoup(html, 'html.parser')
        except:
            time.sleep(10)
            # print('重新')
            get_soup(url, c)
            # # print("Was a nice sleep, now let me continue...")
            continue
    # try:
    #     with urllib.request.urlopen(url) as response:
    #         # use whatever encoding as per the webpage
    #         html = response.read().decode('utf-8')
    #         print(html)
    # except urllib.request.HTTPError as e:
    #     if e.code == 404:
    #         print(f"{url} is not found")
    #     elif e.code == 503:
    #         print(f'{url} base webservices are not available')
    #         # can add authentication here
    #     else:
    #         print('http error', e)
    # -----------------------------
    # html = requests.get(url, headers=headers, proxies=proxies).content
    # while True:
    #     soup = BeautifulSoup(html, 'html.parser')
    #     body = soup.find('body').text
    #     # print(body)
    #     if str(body).find('loading...') > 1:
    #         print(body.text)
    #         break
    #     time.sleep(3)
    #     html = requests.get(url, headers=headers, proxies=proxies).content
    #     soup = BeautifulSoup(html, 'html.parser')
    #     # print(soup)

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
    dom = requests.get(url).content
    #     result = re.search(
    #         '"quality":"720","videoUrl":"(.*?)"},', dom.decode("utf-8"))
    try:
        result = re.search('"videoUrl":"(.*?)"},',
                           dom.decode("utf-8")).group(1).replace('\\', '')
        url = str(result)
        return url
    except:
        return False


def download(url, filename, chunk_count):
    # print(str(url) + str(filename))
    if os.path.isfile(filename):
        return False
    else:
        # print(str(filename))
        proxies = {}
        # proxies['http'] = on_proxies()
        proxies['https'] = _proxy()
        ###
        # downloader = Downloader(url, filename, chunk_count, high_speed=True, headers=None, proxies=proxies)
        downloader = Downloader(url, filename, chunk_count)
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
    download(url, V_path,  random.randint(5, 10))
    # 檢查 影片
    json_dict_['mins'] = video_time(V_path)
    # 下載json
    write_json_file(json_dict_, j_path)
    global _movie_row
    _movie_row += 1
    print('下載完成' + str(_movie_row))
    return True


def data_list(url):
    soup = get_soup(url)
    if soup == False:
        time.sleep(60)
        data_list(url)
        return False
    # print(soup)
    _se = soup.find('body').text.strip().replace("", "")
    # print(_se)
    _ss = 'Loading ...'
    if _se == _ss:
        print('異常')
        # raise Exception('異常')
        sys.exit(0)
    # ## videoPreviewBg
    div_wrap = soup.find_all('div', {'class': 'phimage'})
    # print(div_wrap)
    # print(len(div_wrap))
    # return True
    for h_ in div_wrap:
        href_ = h_.find('a').get('href')
        title_ = h_.find('a').get('title')
        img_ = h_.find('a').find('img').get('data-src')
        _d = h_.find(
            'div', {'class': 'marker-overlays js-noFade'}).find('var').text.split(':', 1)
        # print(_d)
        if int(_d[0]) < 5:
            pass
            # print('低於20分')
        else:
            key_1 = href_.replace('/view_video.php?viewkey=', '')
            key_ = pas_(href_, 'viewkey')
            # print(str(href_) + ' : ' + str(title_) + ' : ' + str(key_))
            # print(str(title_))
            url_ = parseURL(key_)
            ##
            u = urlparse(url_)
            ext = os.path.splitext(u.path)[1]

            # print(u.path)
            ##
            global pornhub_path_v
            global pornhub_path_j
            path_v = pornhub_path_v + str(key_) + str(ext)
            path_j = pornhub_path_j + str(key_) + '.json'

            try:
                # pass
                path_i = pornhub_path_i + str(key_) + os.path.splitext(img_)[1]
            except:
                # pass
                path_i = pornhub_path_i + str(key_) + str('.jpg')

                # print(path_v)
            res = True
            if url_ == False:
                # print('找不到網址 :' + str(href_))
                # print(str(href_) + ' : ' + str(title_) + ' : ' + str(key_))
                res = False
                continue
            elif ext != '.mp4':
                # print('找不到網址 :' + str(href_))
                continue
            else:
                res = True
                print('找網址 :' + str(href_))
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

pornhub_path_v = pornhub_path_v_
mkdir_m(pornhub_path_v)
pornhub_path_j = pornhub_path_j_
mkdir_m(pornhub_path_j)
pornhub_path_i = pornhub_path_i_
mkdir_m(pornhub_path_i)

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
        print(_url)
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
        print(_url)
        # time.sleep(5)
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
        os.remove(file_name)
        print('刪除')
        return 0
    # For Windows

    # For Linux
    # a = str(check_output('ffprobe -i  "'+file_name+'" 2>&1 |grep "Duration"',shell=True))
    a = a.split(",")[0].split("Duration:")[1].strip()
    h, m, s = a.split(':')
    duration = int(h) * 3600 + int(m) * 60 + float(s)
    # print(duration)
    return duration


def r1():
    # guard(1, 1000000)
    return True


def r2():
    threadLock = threading.Lock()
    threads = []
    global _s
    __let = _s
    _i = 0
    for rows in __let:
        thread = myThread(_i, "Thread-"+str(_i), rows)
        thread.start()
        threads.append(thread)
        _i += 1
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


def _proxy():
    _proxy_list = []
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
        if td_[6].text == 'yes' and td_[4].text == 'anonymous':
            _s = str('https://' + td_[0].text + ':' + td_[1].text)
            _proxy_list.append(_s)
    ####
    _s = random.choice(_proxy_list)
    # print(_s)
    return _s


if __name__ == '__main__':
    # 單線程
    # r1()
    # 多線程
    # r2()
    # 多線程 首頁
    r3()
    # ----------------
    # _c_()
    # v = _proxy()
    # print(v)
    print('run')
