
import requests
import json


class Video_API:

    def __init__(self, api_url):
        self.api_url = api_url
        pass

    def apiVerificationUrlExist(self, url):
        # 資料
        my_data = {'video_dl_url': url}
        print(my_data)
        # 將資料加入 POST 請求中
        r = requests.post(
            self.api_url + str('apiVerificationUrlExist'), data=my_data)
        ###
        content = r.json()
        print(content)
        if int(content['code']) == 200:
            return self.apiCrawlingStart(url)
        elif int(content['code']) == 600:
            return False

    def apiCrawlingStart(self, url):
        # 資料
        my_data = {'video_dl_url': url}
        # 將資料加入 POST 請求中
        r = requests.post(self.api_url + str('apiCrawlingStart'), data=my_data)
        ###
        content = r.json()
        print(content)
        # print(content['code'])
        if int(content['code']) != 200:
            return False
        return content

    def apiCrawlingEnd(self, url, video_dl_id):
        # 資料
        my_data = {'video_dl_url': url, 'video_dl_id': video_dl_id}
        # print(my_data)
        # 將資料加入 POST 請求中
        r = requests.post(self.api_url + str('apiCrawlingEnd'), data=my_data)
        ###
        content = r.json()
        print(content)
        # print(content['code'])
        if int(content['code']) != 200:
            return False
        return content
