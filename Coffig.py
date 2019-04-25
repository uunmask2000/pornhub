
import time
import os
from urllib.request import urlretrieve
from urllib.parse import urlparse
import requests
import json


class Coffig:

    downloads = 0

    def __init__(self):
        pass

    def shwo(self):
        return self.downloads

    def do_create_img(self, content, img_name):
        if content is None:
            return False
        # with open(img_name, 'wb') as file:  # 以byte的形式將圖片數據寫入
        #     file.write(content)
        #     file.flush()
        #     file.close()  # close file
        # urlretrieve(content, img_name)
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        res = requests.get(content, headers=header)
        with open(img_name, 'wb') as f:
            f.write(res.content)
        return img_name

    def download_(self, url, path):
        print('start  ：')
        start = time.time()
        video_time_ = self.video_time(path)
        # print(video_time_)
        if os.path.isfile(path):
            self.downloads -= 1
            print('檔案存在')
        elif video_time_ == True:
            print('檔案存在，格式錯誤')
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
        self.downloads += 1
        return True

    def video_time(self, file_name):
        return False

    def write_json_file(self, post_dict_, path):
        # print(path)
        with open(path, 'w') as fp:
            json.dump(post_dict_, fp)
        return True
