# MediaRename

媒体自动更名工具

1. 视频更名为VDO_yyyymmdd_hhiiss.* 时间为encoded_date 并转换为本地时间
2. 图片更名为PHT_yyyymmdd_hhiiss.* 时间为exif拍摄时间 并转换为本地时间

# 使用方法

## 1 安装exifinfo

linux安装:
```
apt install exifinfo
```
windows请参照[pyexiftool](https://github.com/guinslym/pyexifinfo)说明安装exiftool

## 2 安装pyexifinfo

```
pip3 install -U pyexifinfo
```

## 3 重命名路径下所有文件

```
python3 rename.py [路径]
```