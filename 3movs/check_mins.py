import json
import glob
import Check_video_mins
import Cofig
###
Check_video_mins = Check_video_mins.Check_video_mins()
# 設定
Cofig = Cofig.Cofig(path='path', Host_name='7msp1')


def __init__():
    json_ = glob.glob('path/**/**/*.json', recursive=True)
    # print(json_)
    for _l in json_:
        print(_l)
        with open(_l) as f:
            data = json.load(f)
            _source_url = data['source_url']
            _video_time = Check_video_mins.video_time(_source_url)
            if _video_time:
                data['mins'] = int(_video_time)
                print(data)
                # print(_source_url)
                # # print(_video_time)
                # print('156')
                Cofig.write_json_file(data, _l)
            else:
                print('錯誤')
    return True


# -------------------------------
# path = 'path/20190424/7msp1/videos/2831706F6E646F29283035303531365F32393329.mp4'
__init__()
