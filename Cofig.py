import json
import hashlib
import time
import os
import datetime


class Cofig:
    '''
    預設值
    '''

    def __init__(self, path='data/', _path_list=[], Host_name='main'):
        # 先建立資料夾
        self._path_list = _path_list
        self.Host_name = Host_name
        self.path = path
        # -----------------------------------------------------
        path = self.path
        self.mkdir_m(path)
        ###
        now_date = datetime.datetime.now().strftime("%Y%m%d")
        path = path + now_date + '/'

        self.mkdir_m(path)

        _p = path + Host_name + '/'
        self.mkdir_m(_p)

        _let_key = [
            'videos/',
            'jsons/',
            'images/'
        ]

        for _a in _let_key:
            _s = _p + _a
            self.mkdir_m(_s)
            ##
            self._path_list.append(_s)
        print(self._path_list)

    def get_path_list(self,):
        #####
        return self._path_list

    def write_json_file(self, post_dict_, path):
            # print(path)
        with open(path, 'w') as fp:
            json.dump(post_dict_, fp)
        return True

    def create_time(self, ):
        # 獲取時間
        return int(time.time())  # 1

    def create_sign(self, t):
        # 建立sign
        sig = "sc%7*g{}@!$%".format(t)
        md = hashlib.md5()
        md.update(sig.encode(encoding='utf-8'))
        sign = md.hexdigest()  # 2
        return sign

    def mkdir_m(self, Path):
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

    def json_dict(self,):
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
