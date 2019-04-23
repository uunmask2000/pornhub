import requests
from urllib import parse
from urllib.request import urlretrieve
from urllib.parse import urlparse
from bs4 import BeautifulSoup
###############################################


class Bssoup:
    '''
    預設值
    '''

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        self.proxies = {}

    def get_soup(self, url, count=0, max_count=10, mode=2,  headers=None, proxies=None, html=False):
        ###
        if headers == None:
            headers = self.headers
        if proxies == None:
            proxies = self.proxies
        # ----------------------------------------
        if mode == 1:
            # 代理IP
            _v = self.get_soup_pu(url, headers, proxies, html)
        elif mode == 2:
            # 真實IP
            _v = self.get_soup_pv(url, html)
        ##
        if _v == False:
            count += 1
            return self.get_soup(url,  count, mode,  headers,  proxies, html)
        else:
            return _v

    def get_soup_pu(self, url, headers, proxies, html_c):
        # 代理ip
        soup = False
        try:
            html_ = requests.get(url, headers=headers,
                                 proxies=proxies, timeout=10)
            html = html_.content.decode("utf-8")
            if html_c == True:
                return html
            soup = BeautifulSoup(html, 'html.parser')
        except:
            pass
            # return False
        return soup

    def get_soup_pv(self, url, html_c):
        # 真實ip
        soup = False
        try:
            html_ = requests.get(url, timeout=10)
            html = html_.content.decode("utf-8")
            if html_c == True:
                return html
            soup = BeautifulSoup(html, 'html.parser')
        except:
            pass
            # return False
        return soup
