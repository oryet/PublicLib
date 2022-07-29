# -*- coding: utf-8 -*-
import chardet  # 导入chardet库
import os
import re

import datetime
import time
import logging
import difflib
# from pprint import pprint
#
# test1 = 'wenming1grtt'
# test2 = 'wenming'
# d = difflib.HtmlDiff()
# with open('test.html',"w") as file:
#     file.write(d.make_file(test1,test2))
import filecmp

def alter(file,new_str,newname):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:旧字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        i = 0
        for line in f:
            if i == 0:
            # if old_str in line:
                line = newpath
            # if oldname in line:
            if i == 1:
                line = newname
            i += 1
            file_data += line
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)
#终端中，要下载的文件的路径
newpath = 'cd /lib/hal_lib/\n'
#终端中要下载的文件的名称
newname = 'mget libhaldrv.so\n'
#本地电脑要传到终端中的路径（终端路径）
#电脑要上传到电脑的路径
# newpath = 'cd /tmp/test_dir/\n'
# #电脑要上传到终端的文件名称
# newname = 'mput 777.txt\n'
path = 'ftp_get_file.bat'
alter(path,newpath,newname)

os.system('test.bat')
pathget = os.getcwd()+ '\libhaldrv.so'
#2个文件纯文本或.tar文件或.so比较。
print(filecmp.cmp('C:\\Users\Administrator\Desktop\ECU\TLY2205-03-SW1600-20211124-00-公变-量产 (1)\TLY2205-03-SW1600-20211124-00-公变-量产\TLY2205-03-SW1600-20211124-00-pu-mp\extlibs\libhaldrv.so',pathget,False))

def com_rtu_filecmp():
    alter(path, newpath, newname)
