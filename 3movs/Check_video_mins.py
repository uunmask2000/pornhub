import json
import glob
from subprocess import check_output
# 要安裝 subprocess +


class Check_video_mins:
    def __init__(self):
        pass

    def video_time(self, file_name):
        # file_name = "TEST\ph5a8b7ec93d417.mp4"
        try:
              # For Windows
            a = str(check_output('ffprobe -i  "'+file_name +
                                 '" 2>&1 |findstr "Duration"', shell=True))
            # For Linux
            # a = str(check_output('ffprobe -i  "'+file_name+'" 2>&1 |grep "Duration"',shell=True))
            print('檔案OK')
        except:
            return False

        a = a.split(",")[0].split("Duration:")[1].strip()
        h, m, s = a.split(':')
        duration = int(h) * 3600 + int(m) * 60 + float(s)
        # print(duration)
        return int(duration/60)
