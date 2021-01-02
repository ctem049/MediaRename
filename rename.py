import sys
import pyexifinfo as p
import os
from datetime import *
import pytz
import json

# 时区1 转 时区2
def tz1_to_tz2(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S.%fZ', local_format = "%Y%m%d_%H%M%S", tz1='UTC', tz2='Asia/Shanghai'):
    local_tz = pytz.timezone(tz2)
    utc_dt = datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.timezone(tz1)).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return time_str

# 获取文件后缀
def file_extension(path): 
    return os.path.splitext(path)[1] 

def auto_rename(f):
    print('file:',f, end="")
    hastime = False
    # 获取媒体信息
    info = p.get_json(f)
    '''
        if (sys.argv[2]):
            print(info)
            print( json.dumps(info, sort_keys=True, indent=4, separators=(',', ': ')) )
            #print(info[0]['File:MIMEType'])
    '''
    tf1='%Y:%m:%d %H:%M:%S'
    tz1='UTC'
    tf2='%Y%m%d_%H%M%S' #c 时间格式
    tz2='Asia/Shanghai'
    pre='PHT_'
    suf='.jpg'
    if ('File:MIMEType' in info[0]):
        mimetype=info[0]['File:MIMEType']
    else:
        mimetype='undefined'
    if (mimetype=='image/jpeg'):
        # 照片
        if ('EXIF:ModifyDate' in info[0]):
            t = info[0]['EXIF:ModifyDate'].replace('-',':') #形式: %Y:%m:%d %H:%M:%S, 2015:06:17 08:51:33
        elif ('EXIF:DateTimeOriginal' in info[0]):
            t = info[0]['EXIF:DateTimeOriginal'].replace('-',':') #形式: %Y:%m:%d %H:%M:%S, 2015:06:17 08:51:33
        elif ('EXIF:CreateDate' in info[0]):
            t = info[0]['EXIF:CreateDate'].replace('-',':') #形式: %Y:%m:%d %H:%M:%S, 2015:06:17 08:51:33
        else:
            t = None
        if t:
            tf1 = '%Y:%m:%d %H:%M:%S'
            tz1 = 'Asia/Shanghai'
            pre = 'PHT_' #c 照片前缀
            suf = '.'+info[0]['File:FileTypeExtension']
            hastime = True
    elif (mimetype=='video/mp4')|(mimetype=='video/3gpp'):
        if ('QuickTime:CreateDate' in info[0]):
            # 视频
            t = info[0]['QuickTime:CreateDate'].replace('-',':') #形式: %Y:%m:%d %H:%M:%S, 2015:06:17 08:51:33
            tf1 = '%Y:%m:%d %H:%M:%S'
            tz1 = 'UTC'
            pre = 'VDO_' #c 视频前缀
            suf = '.'+info[0]['File:FileTypeExtension']
            hastime = True
    else:
        print('>>> unexcepted MIME:',mimetype)
    if hastime:
        # 转为本地时间形式: %Y%m%d_%H%M%S, 20150617_085133
        timeStr = tz1_to_tz2(t, tf1, tf2, tz1, tz2)
        # 文件名 PHT_yyyymmdd_hhiiss.*
        name = pre+timeStr+suf
        # 判断是否存在
        i = 1
        while os.path.exists(name):
            name = pre+timeStr+'_'+str(i)+suf
            i = i + 1
        print('>>>', name)
        # 重命名
        os.rename(f,os.path.join(os.path.dirname(f),name))
    else:
        print('>>> no time')

path = str(sys.argv[1])
if os.path.isdir(path):
    # 目录遍历
    print('path:',path)
    for fpathe,dirs,fs in os.walk(path):
        for f in fs:
            fi = os.path.join(fpathe,f)
            auto_rename(fi)
elif os.path.isfile(path):
    # 文件处理
    auto_rename(path)
else:
    print("it's a special file(socket,FIFO,device file)")
