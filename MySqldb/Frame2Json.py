# -*- coding: cp936 -*-
import json
import re
from PublicLib.MySqldb.Json2db import Json2db
import time


def frameforma(data):
    if data['type'] == 'json':
        recv = data['recvData']
        jdata = re.sub('\'', '\"', recv)
        data_json = json.loads(jdata)
        return data['ip'], data['port'], data_json
    else:
        return None, None, None


def datetimeformat(datetime):
    fdatetime = datetime[:2] + '-' + datetime[2:4] + '-' + datetime[4:6] + ' ' + datetime[6:8] + ':' \
                + datetime[8:10] + ':' + datetime[10:12]
    return fdatetime

def formatdate(date):
    # 日期提取
    date = '20' + date
    ts = time.strptime(date, "%Y%m%d%H%M")
    # 格式化时间转时间戳
    time.mktime(ts)
    # 格式化时间
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    return format_time

def getcurtime():
    # 时间戳
    now = time.time()
    int(now)

    # 时间
    tl = time.localtime(now)

    # 格式化时间
    return time.strftime("%Y-%m-%d %H:%M:%S", tl)


def formatfloatdata(data):
    return float(data)

def cuver2data(cuver):

    datelist = []
    datalist = []

    if cuver == 'N':
        return datelist, datalist

    cuver += '#'
    n = cuver.count('#') # 分段数
    s = cuver
    for i in range(n):
        x = s.find('#')
        if x == 10:
            datelist += [formatdate(s[:x])]
            # print("date:", s[:x], date)
            s = s[11:]
        else:
            data = formatfloatdata(s[:x])
            datalist += [data]
            # print("data:", s[:x], data)
            s = s[x+1:]
    return datelist, datalist

def processdata(ip, port, jdata):
    jdb = Json2db("192.168.127.200", "test")
    if jdata['Cmd'] == 'Login':
        '''
       {'ip':'218.204.253.169','port':'59080', 'recvData':{'Len':'0124','Cmd':'Login','SN':'1',
       'DataTime':'190719130028','CRC':'FFFF','DataValue':{'04A20209':'111111111111#000000000000#00000000'}}}
       '''
        addr = jdata['DataValue']['04A20209'][:12]
        dt = datetimeformat(jdata['DataTime'])
        iport = int(port, 10)
        # cdt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jdb.insertlogin(addr, ip, iport, dt)
    elif jdata['Cmd'] == 'Heart':
        '''
       {'ip':'36.113.229.239','port':'25344', 'recvData':{'Len':'0105','Cmd':'Heart','SN':'8266',
       'DataTime':'190729021526','CRC':'FFFF','DataValue':{'04A20208':'201708090001'}}}
       '''
        addr = jdata['DataValue']['04A20208'][:12]
        dt = datetimeformat(jdata['DataTime'])
        iport = int(port, 10)
        # cdt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        jdb.insertlogin(addr, ip, iport, dt)
    elif jdata['Cmd'] == 'Report':
        '''
        {'ip':'218.204.253.169','port':'59080', 'recvData':{'Len':'0380','Cmd':'Report','SN':'8272',
        'DataTime':'190729023003','CRC':'FFFF','DataValue':{'061001FF':'1907290215#230.2#000.0#000.0
        #1907290220#230.4#000.0#000.0#1907290225#230.5#000.0#000.0','061002FF':'1907290215#000.034
        #000.000#000.000#1907290220#000.040#000.000#000.000#1907290225#000.034#000.000#000.000',
        '06100901':'1907290215#000000.1645#1907290220#000000.1645#1907290225#000000.1645'}}}
        '''

        if '061001FF' in jdata['DataValue']:
            cuver = jdata['DataValue']['061001FF']
            le, ld = cuver2data(cuver)
            loop = len(le)
            for i in range(loop):
                jdb.insertvol(ip, getcurtime(), le[i], ld[i*3], ld[i*3+1], ld[i*3+2])
        if '061001FF' in jdata['DataValue']:
            cuver = jdata['DataValue']['061002FF']
            le, ld = cuver2data(cuver)
            loop = len(le)
            for i in range(loop):
                jdb.insertcur(ip, getcurtime(), le[i], ld[i*3], ld[i*3+1], ld[i*3+2])
        if '061003FF' in jdata['DataValue']:
            cuver = jdata['DataValue']['061003FF']
            le, ld = cuver2data(cuver)
            loop = len(le)
            for i in range(loop):
                jdb.insertinsq(ip, getcurtime(), le[i], ld[i*4], ld[i*4+1], ld[i*4+2], ld[i*4+3])
        if '061004FF' in jdata['DataValue']:
            cuver = jdata['DataValue']['061004FF']
            le, ld = cuver2data(cuver)
            loop = len(le)
            for i in range(loop):
                jdb.insertinsp(ip, getcurtime(), le[i], ld[i*4], ld[i*4+1], ld[i*4+2], ld[i*4+3])
        if '061005FF' in jdata['DataValue']:
            cuver = jdata['DataValue']['061005FF']
            le, ld = cuver2data(cuver)
            loop = len(le)
            for i in range(loop):
                jdb.insertpwrf(ip, getcurtime(), le[i], ld[i*4], ld[i*4+1], ld[i*4+2], ld[i*4+3])
        if '06100901' in jdata['DataValue']:
            cuver = jdata['DataValue']['06100901']
            le, ld = cuver2data(cuver)
            loop = len(le)
            cnt = int(len(ld)/loop)
            for i in range(loop):
                if cnt <= 8:
                    ldd = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                    ldt = []
                    for n in range(cnt):
                        ldt += [ld[i*cnt+n]]
                    ldd = ldt + ldd
                    jdb.insertposeng(ip, getcurtime(), le[i], ldd[0], ldd[1], ldd[2], ldd[3], ldd[4], ldd[5], ldd[6], ldd[7], ldd[8])
        if '06100902' in jdata['DataValue']:
            cuver = jdata['DataValue']['06100902']
            le, ld = cuver2data(cuver)
            loop = len(le)
            cnt = int(len(ld)/loop)
            for i in range(loop):
                if cnt <= 8:
                    ldd = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                    ldt = []
                    for n in range(cnt):
                        ldt += [ld[i*cnt+n]]
                    ldd = ldt + ldd
                    jdb.insertnegeng(ip, getcurtime(), le[i], ldd[0], ldd[1], ldd[2], ldd[3], ldd[4], ldd[5], ldd[6], ldd[7], ldd[8])
    else:
        pass

if __name__ == '__main__':
    cuv = "1907290215#230.2#000.0#000.0#1907290220#230.4#000.0#000.0#1907290225#230.5#000.0#000.0"
    le, ld = cuver2data(cuv)
    print(le, ld)
