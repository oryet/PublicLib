# -*- coding: cp936 -*-
import json
import re
from PublicLib.MySqldb.Json2db import Json2db
import time


def frameforma(data):
    jdatalist = []
    if data['type'] == 'json':
        recv = data['recvData']
        jdata = re.sub('\'', '\"', recv)
        # ��������
        n = jdata.count("{\"Len\":")
        end = 0
        for i in range(n):
            try:
                start = end
                end = jdata.find("{\"Len\":", start+1)
                if end == -1:
                    datatmp = jdata[start:]
                else:
                    datatmp = jdata[start:end]
                data_json = json.loads(datatmp)
                jdatalist += [data_json]
            except:
                jdatalist += [None]
        return data['ip'], data['port'], jdatalist
    else:
        return None, None, jdatalist


def datetimeformat(datetime):
    fdatetime = datetime[:2] + '-' + datetime[2:4] + '-' + datetime[4:6] + ' ' + datetime[6:8] + ':' \
                + datetime[8:10] + ':' + datetime[10:12]
    return fdatetime

def formatdate(date):
    # ������ȡ
    date = '20' + date
    ts = time.strptime(date, "%Y%m%d%H%M")
    # ��ʽ��ʱ��תʱ���
    time.mktime(ts)
    # ��ʽ��ʱ��
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    return format_time

def getcurtime():
    # ʱ���
    now = time.time()
    int(now)

    # ʱ��
    tl = time.localtime(now)

    # ��ʽ��ʱ��
    return time.strftime("%Y-%m-%d %H:%M:%S", tl)


def formatfloatdata(data):
    return float(data)

def cuver2data(cuver):

    datelist = []
    datalist = []

    if cuver == 'N':
        return datelist, datalist

    cuver += '#'
    n = cuver.count('#') # �ֶ���
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
        if jdata['DataValue'] == '04A20209':
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
        if jdata['DataValue'] == '04A20208':
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
    # cuv = "1907290215#230.2#000.0#000.0#1907290220#230.4#000.0#000.0#1907290225#230.5#000.0#000.0"
    # le, ld = cuver2data(cuv)
    # print(le, ld)
    # cuv = {'ip': '221.178.127.231', 'port': '10301', 'type': 'json', 'recvData': "{'Len':'0099','Cmd':'Report','SN':'6140','DataTime':'190808122802','CRC':'FFFF','DataValue':{'02010100':'227.3'}}{'Len':'0380','Cmd':'Report','SN':'6141','DataTime':'190808123002','CRC':'FFFF','DataValue':{'061001FF':'1908081215#226.8#000.0#000.0#1908081220#227.3#000.0#000.0#1908081225#227.0#000.0#000.0','061002FF':'1908081215#000.039#000.000#000.000#1908081220#000.045#000.000#000.000#1908081225#000.036#000.000#000.000','06100901':'1908081215#000000.1645#1908081220#000000.1645#1908081225#000000.1645'}}{'Len':'0379','Cmd':'Report','SN':'6142','DataTime':'190808123102','CRC':'FFFF','DataValue':{'061003FF':'1908081220#00.0000#00.0000#00.0000#00.0000#1908081225#00.0000#00.0000#00.0000#00.0000#1908081230#00.0000#00.0000#00.0000#00.0000','061004FF':'1908081220#00.0000#00.0508#00.0000#00.0000#1908081225#00.0000#00.0508#00.0000#00.0000#1908081230#00.0000#00.0508#00.0000#00.0000','061005FF':'N'}}{'Len':'0101','Cmd':'Report','SN':'6143','DataTime':'190808123202','CRC':'FFFF','DataValue':{'02020100':'000.040'}}{'Len':'0099','Cmd':'Report','SN':'6144','DataTime':'190808123302','CRC':'FFFF','DataValue':{'02010100':'227.2'}}"}
    cuv = {'ip': '218.204.252.22', 'port': '58098', 'type': 'json', 'recvData': "{'Len':'0099','Cmd':'Report','SN':'9993','DataTime':'190812230802','CRC':'FFFF','DataValue':{'02010100':'228.3'}}{'Len':'0105','Cmd':'Heart','SN':'9994','DataTime':'190812230845','CRC':'FFFF','DataValue':{'04A20208':'111111111111'}}{'Len':'0101','Cmd':'Report','SN':'9995','DataTime':'190812231202','CRC':'FFFF','DataValue':{'02020100':'000.036'}}{'Len':'0099','Cmd':'Report','SN':'9996','DataTime':'190812231302','CRC':'FFFF','DataValue':{'02010100':'227.6'}}{'Len':'0380','Cmd':'Report','SN':'9997','DataTime':'190812231502','CRC':'FFFF','DataValue':{'061001FF':'1908122300#228.1#000.0#000.0#1908122305#228.2#000.0#000.0#1908122310#228.2#000.0#000.0','061002FF':'1908122300#000.036#000.000#000.000#1908122305#000.038#000.000#000.000#1908122310#000.033#000.000#000.000','06100901':'1908122300#000000.1645#1908122305#000000.1645#1908122310#000000.1645'}}{'Len':'0379','Cmd':'Report','SN':'9998','DataTime':'190812231602','CRC':'FFFF','DataValue':{'061003FF':'1908122305#00.0000#00.0000#00.0000#00.0000#1908122310#00.0000#00.0000#00.0000#00.0000#1908122315#00.0000#00.0000#00.0000#00.0000','061004FF':'1908122305#00.0000#00.0508#00.0000#00.0000#1908122310#00.0000#00.0508#00.0000#00.0000#1908122315#00.0000#00.0508#00.0000#00.0000','061005FF':'N'}}{'Len':'0101','Cmd':'Report','SN':'9999','DataTime':'190812231702','CRC':'FFFF','DataValue':{'02020100':'000.040'}}{'Len':'0096','Cmd':'Report','SN':'1',"}
    ip, port, jdata = frameforma(cuv)
    if len(jdata) > 0:
        for data in jdata:
            if data is not None:
                print(data)
                processdata(ip, port, data)
    else:
        print("jdata err")
