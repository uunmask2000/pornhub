'''
Arthur       : kk
Date         : 2022-02-15 15:15:28
LastEditTime : 2022-02-15 16:12:29
LastEditors  : your name
Description  : 自動生成 [嚴格紀律 Description]
FilePath     : /3movs/CustomEncryption.py
嚴格紀律
'''
import base64
import hashlib


class CustomEncryption:
    '''
    預設值
    '''

    def __init__(self, key=None):
        if key == None:
            self.key = '1234567'
        self.key = key

    def md5_encode(self, srt_):
        return hashlib.md5(srt_.encode('utf-8')).hexdigest()

    def b16_encode(self, srt_):
        # 貼加密字串
        encoded = base64.b16encode(srt_.encode('utf-8')).decode('ascii')
        return encoded

    def b16_decode(self, encoded):
        # 加密字串取代為空
        # data = base64.b16decode(encoded).decode('utf-8')
        data = base64.b16decode(encoded.encode('ascii')).decode('utf-8')
        return data
