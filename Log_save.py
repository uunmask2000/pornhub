
import json
import os


class Log_save:
    '''
    預設值
    '''

    def __init__(self):
        _list = [
            'downloads_list.json',
            'downloads_list2.json',
            'downloads_list3.json',
        ]
        # 建立預設log
        for file in _list:
            self.chech_json_file(file)

    def chech_json_file(self, file):
        print(file)
        if os.path.exists(file) != True:
            print('建立檔案')
            number = []
            with open(file, 'w') as file_object:
                json.dump(number, file_object)

        return True

    def save_or_check(self, url):
                ###
                # global downloads_list
        json_file = 'downloads_list.json'
        with open(json_file, 'r') as reader:
            jf = json.loads(reader.read())

        # print(jf)
        ##
        if url in jf:
            # print('有了')
            return False
        else:
            jf.append(url)
            with open(json_file, 'w') as fp:
                json.dump(jf, fp)
            # print('沒有')
            return True

    def save_or_check2(self, url):
        ###
        # global downloads_list
        json_file = 'downloads_list2.json'
        with open(json_file, 'r') as reader:
            jf = json.loads(reader.read())

        # print(jf)
        ##
        if url in jf:
            # print('有了')
            return False
        else:
            jf.append(url)
            with open(json_file, 'w') as fp:
                json.dump(jf, fp)
            # print('沒有')
            return True

    def save_or_check3(self, url):
        ###
        # global downloads_list
        json_file = 'downloads_list3.json'
        with open(json_file, 'r') as reader:
            jf = json.loads(reader.read())

        # print(jf)
        ##
        if url in jf:
            # print('有了')
            return False
        else:
            jf.append(url)
            with open(json_file, 'w') as fp:
                json.dump(jf, fp)
            # print('沒有')
            return True
