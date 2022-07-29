# -*- coding: utf-8 -*-
import os
import datetime
import time
# import unicodedata
# import configparser
# from OpenExcelTestPlan import ExcelPlan
from Protocol.FCSccc import *
from Protocol import General
import binascii
from binascii import a2b_hex
#王梦新增
from Protocol.excelchange import *
from Protocol.dl645 import *
import re
#王梦新增



MIN_LEN_OOP_FRAME = 36
CTRL_LINK = 1
#服务器发起的上报
CTRL_REPORT = 2
CTRL_DATA = 3

LINK_APDU_Request = '01'
LINK_APDU_Response = '81'
#0:登录
LinkRequestType_LOGIN = '00'
#1：心跳
LinkRequestType_HEART = '01'
#2：退出登录
LinkRequestType_EXIT = '02'

POS_oop_HEAD = 0   # 0
POS_oop_LEN = 2    # 1
POS_oop_CTRL = 6   # 3
POS_oop_ADDR = 8   # 4
POS_oop_DATA = 28  # 14
MIN_LEN_698FRAME = 42  # 21

Client_APDU_CONNECT_Request = '02' # 建立应用连接请求
Client_APDU_RELEASE_Request = '03' # 断开应用连接请求
Client_APDU_GET_Request = '05'     # 读取请求 [5]
Client_APDU_SET_Request = '06'     # 设置请求 [6]
Client_APDU_ACTION_Request = '07'  # 操作请求 [7]
Client_APDU_REPORT_Response = '08' # 上报应答 [8] ，
Client_APDU_PROXY_Request = '09'   # 代理请求 [9]
Client_APDU_ERROR_Response = '6E'  # 异常响应 [110]

Server_APDU_CONNECT_Response = '82'       # 建立应用连接响应 [130]
Server_APDU_RELEASE_Response = '83'       # 断开应用连接响应 [131]
Server_APDU_RELEASE_Notification = '84'   # 断开应用连接通知 [132]
Server_APDU_GET_Response = '85'           # 读取响应 [133]
Server_APDU_SET_Response = '86'           # 设置响应 [134]
Server_APDU_ACTION_Response = '87'        # 操作响应 [135]
Server_APDU_REPORT_Notification = '88'    # 上报通知 [136] ，
Server_APDU_PROXY_Response = '89'         # 代理响应 [137] ，
Server_APDU_ERROR_Response = 'EE'         # 异常响应 [238]

SECURITY_APDU_SECURITY_Request = '10'     # 安全请求 [16] SECURITY_Request，
SECURITY_APDU_SECURITY_Response = '90'    # 安全响应 [144] SECURITY_Response

GetRequestNormal = '01'        # 请求读取一个对象属性 [1]
GetRequestNormalList = '02'    # 请求读取若干个对象属性[2]
GetRequestRecord = '03'        # 请求读取一个记录型对象属性[3]
GetRequestRecordList = '04'    # 请求读取若干个记录型对象属性[4]
GetRequestNext = '05'          # 请求读取分帧传输的下一帧[5]
GetRequestMD5 = '06'           # 请求读取一个对象属性的MD5值[6]

SetRequestNormal = '01'                # 请求设置一个对象属性[1]
SetRequestNormalList = '02'            # 请求设置若干个对象属性[2]
SetThenGetRequestNormalList = '03'     # 请求设置后读取若干个对象属性[3]
ActionRequestNormal = '01'             # 请求操作一个对象方法[1]
ActionRequestNormalList = '02'         # 请求操作若干个对象方法[2]
ActionThenGetRequestNormalList = '03'  # 请求操作若干个对象方法后读取若干个对象属性[3]
ReportNotificationList = '01'          # 通知上报若干个对象属性[1] ，
ReportNotificationRecordList = '02'    # 通知上报若干个记录型对象属性[2] ，
ReportNotificationTransData = '03'     # 通知上报透明数据[3] ，

ProxyGetRequestList = '01'          # 请求代理读取若干个服务器的若干个对象属性[1] ，
ProxyGetRequestRecord = '02'        # 请求代理读取一个服务器的一个记录型对象属性[2] ，
ProxySetRequestList = '03'          # 请求代理设置若干个服务器的若干个对象属性[3] ，
ProxySetThenGetRequestList = '04'   # 请求代理设置后读取若干个服务器的若干个对象属性[4] ，
ProxyActionRequestList = '05'       # 请求代理操作若干个服务器的若干个对象方法[5] ，
ProxyActionThenGetRequestList = '06' # 请求代理操作后读取若干个服务器的若干个对象方法和属性[6] ，
ProxyTransCommandRequest = '07'      # 请求代理透明转发命令[7] 
# DataType
DT_NULL= 0
DT_array = 1
DT_structure = 2
DT_bool = 3
DT_bit_string = 4
DT_double_long = 5
DT_double_long_unsigned	= 6
DT_octet_string = 9
DT_visible_string = 10
DT_UTF8_string = 12
DT_integer = 15
DT_long	= 16
DT_unsigned	= 17
DT_long_unsigned =18
DT_long64 = 20
DT_long64_unsigned = 21
DT_enum	= 22
DT_float32 = 23
DT_float64 = 24
DT_date_time = 25
DT_date = 26
DT_time	= 27
DT_date_time_s = 28
DT_OI = 80
DT_OAD = 81
DT_ROAD = 82
DT_OMD = 83
DT_TI = 84
DT_TSA = 85
DT_MAC = 86
DT_RN = 87
DT_Region = 88
DT_Scaler_Unit = 89
DT_RSD = 90
DT_CSD = 91
DT_MS = 92
DT_SID = 93
DT_SID_MAC = 94
DT_COMDCB = 95
DT_RCSD = 96
# 自定义任意数据标识 方案采集方式 事件采集方式
DT_facjtype = 100
DT_sjcjtype = 101#春哥建的，目前没用
#王梦新增：自定义任意数据类型，区间统计类：越限判断参数
DT_yxparam=102#  要根据关联的OAD的数据类型进行数据类型确定，目前没用。
DT_ENUMERATED=103#区间类型选择，目前没用。
#事件采集方案
DT_eventtype = 104
#上报方案
DT_reporttype = 105
#行方法1
DT_se1 = 106
#行方法2、3
DT_se2 = 107
hearttimesave=''



LINK_APDU_SET = [LINK_APDU_Request, LINK_APDU_Response]
Client_APDU_SET = [Client_APDU_CONNECT_Request, Client_APDU_RELEASE_Request, Client_APDU_GET_Request,
                   Client_APDU_SET_Request, Client_APDU_ACTION_Request, Client_APDU_REPORT_Response,
                   Client_APDU_PROXY_Request, Client_APDU_ERROR_Response]
Server_APDU_SET = [Server_APDU_CONNECT_Response, Server_APDU_RELEASE_Response, Server_APDU_RELEASE_Notification,
                   Server_APDU_GET_Response, Server_APDU_SET_Response, Server_APDU_ACTION_Response,
                   Server_APDU_REPORT_Notification, Server_APDU_PROXY_Response, Server_APDU_ERROR_Response]


FRAME = {'CTRL': '43', 'SA': '05', 'TSA_TYPE': '0', 'TSA_VS': '00', 'TSA_AD': '123456789012', 'CA': '00',
         'SEG_WORD': '', 'APDU': '',
         'CTRL_BS': {'C_DIR': [7, 7, 0], 'C_PRM': [6, 6, 1], 'C_SEG': [5, 5, 0], 'C_NULL': [4, 4, 0],
                     'C_CODE': [3, 3, 0], 'C_AFN': [0, 2, 3]},
         'SA_BS': {'SA_TYPE': [6, 7, 0], 'SA_VS': [4, 5, 0], 'SA_LEN': [0, 3, 5]},
         'SEG_WORD_BS': {'SEG_INDEX': [0, 11, 0], 'SEG_NULL': [12, 14, 0], 'SEG_TYPE': [14, 15, 0]}}
#王梦新增：定义含有IP的标识
Iplist=["45000200","45000300","45100200","45100300","45100400","45200200","45000E00"]
#极值统计：极值统计在换算时，要转回原本关联的OAD，才能正常换算。做一个列表，来区分是否是极值统计
extlist=['2120','2121','2122','2123','2124']
#累加平均统计：被关联的数据标识，都被处理成  float64类型的
avelist=['2110','2111','2112','2113','2114']




def mframe():
    sframe = ''
    return sframe

# 563412 ->123456
def reverse(data):
    string = ''
    for i in range(len(data)-1, -1, -2):
        string += data[i-1]
        string += data[i]
    return string

def splitfram(buff):
    timestyle = ''
    rigtfrm = True
    allfrmlist = []
    frmlen = ''
    print('splitframbuff:',buff)
    if CheckValid(buff) == False:
        return allfrmlist
    else:
        rigtfrm,frmlen = CheckValid(buff)
        while len(buff) > frmlen:
            if CheckValid(buff[frmlen:]) == False:
                return allfrmlist
            allfrmlist.append(buff[:frmlen])
            buff = buff[frmlen:]
            rigtfrm, frmlen = CheckValid(buff)
        allfrmlist.append(buff)
        return allfrmlist

def calcCheckSum(fr):
    checkSum = 0
    for i in range(0, len(fr), 2):
        checkSum += int(fr[i:i + 2], 16)
    return str(hex(checkSum))
# add // N字节地址
# vxd // 逻辑地址0，终端，1，交采，2：逻辑地址2（扩展规约）#20200915王梦新增
# type // 地址类型0,表示单地址，1表示通配地址，2表示组地址，3表示广播地址
# 输出字符串
def makeTSA(type, vxd, add):
    # print('type, vxd, add:',type, vxd, add)
    stmp = ''
    sbin = bin(type).replace('0b', '').zfill(2)
    sbin += bin(vxd).replace('0b', '').zfill(2)
    if len(add) % 2 == 1: add = add.zfill((len(add)//2+1)*2)
    # 扩展规约：回路巡检，考虑逻辑地址是2的情况
    if vxd == 2:
        sbin += bin(len(add) // 2 ).replace('0b', '').zfill(4)
    else:
        sbin += bin(len(add) // 2 - 1).replace('0b', '').zfill(4)
    stmp = hex(int(sbin,2)).replace('0x', '').zfill(2)
    #扩展规约：回路巡检，考虑逻辑地址是2的情况
    if vxd == 2:
        stmp +="02"
    else:pass
    stmp += reverse(add)
    return  stmp

# num 数值
# 输出字符串倒置
def makelen(num):
    temp = '0000'
    if isinstance(num, float) == False:
        return temp
    ss = hex(int(num)).replace('0x', '').zfill(4)
    temp = reverse(ss)
    # print(temp)
    return temp

# 获取位状态   istart:Dn, iend:Dn-1, lbytes 字节数
def getbit(data,istart,iend,lbytes):
    if len(data) == 0: return False, ''
    sbin = bin(int(data,16)).replace('0b', '').zfill(lbytes*8)
    # print(sbin)
    ilen = len(sbin)
    if istart>ilen or iend > ilen: return False, ''
    stmp = sbin[lbytes*8-iend:lbytes*8-istart]
    return stmp

# number->hexbuff
def numbertohex(ndata, nlen):
    hexbuff = ''
    if isinstance(ndata, int):
        aa= hex(ndata)
        hexbuff =aa[2:]
        hexbuff=hexbuff.zfill(nlen)
        hexbuff=hexbuff[:nlen]
        hexbuff=hexbuff.upper()
    elif isinstance(ndata, float):
        ndata=int(ndata)
        aa = hex(ndata)
        hexbuff = aa[2:]
        hexbuff = hexbuff.zfill(nlen)
        hexbuff = hexbuff[:nlen]
        hexbuff = hexbuff.upper()
    elif isinstance(ndata, str):
        ndata = int(ndata)
        aa = hex(ndata)
        hexbuff = aa[2:]
        hexbuff = hexbuff.zfill(nlen)
        hexbuff = hexbuff[:nlen]
        hexbuff = hexbuff.upper()
    return hexbuff

def chinese_hex(value):#中文转16进制
    res = value.encode("gb2312")
    aa = str(res)
    aa = aa.strip("'").replace(r"\x", '')[2:]
    return aa

def visibletobuff(s): # 以gb2312的编码格式，组帧成16进制
    cc = bytes(s, 'gb2312')
    ee = ""
    for x in cc:
        dd = str(hex(x))
        ee += dd[2:].zfill(2)
    return ee,len(ee)/2

# def settollist(data):#80027F00中包含“，”和“-”的特殊情况
#     ldad = data.split(',')
#     dalist = []
#     for item in ldad:
#         if item.find('-') >= 0:
#             it = item.split('-')
#             for k in range(int(it[0]), int(it[1])+1, 1):
#                 dalist.append(str(k))
#         else:
#             dalist.append(item)
#     return dalist

def settollist(data, num):#处理虚拟表表号（回复，不回复中的测量点）中有“，”和“-”的特殊情况
    cc=data.replace("M","")
    ldad = cc.split(',')
    dalist = []
    for item in ldad:
        if item.find('-') >= 0:
            it = item.split('-')
            for k in range(int(it[0]), int(it[1])+1, 1):
                dalist.append(num+str(k))
        else:
            dalist.append(num+item)
    return dalist

def regiontotime(timerlist):
    mm=""
    aa = "000000000000000000000000"
    bb = settollist(timerlist,'')
    for item in bb:
        item = int(item)
        # print(item)
        aa = aa[0:item] + "1" + aa[item + 1:]
    aa=str(hex(int(aa,2)))[2:]
    ilen = len(aa)
    mm += numbertohex(int(ilen / 2), 2)
    mm=mm+aa


    print(mm)
    return mm

#王梦新增，区间类型数据类型转换
def makeRegion(value):
    bdata = ''
    if isinstance(value, str):
        print ("excel输入格式错误")
    elif isinstance(value, float):
        idata = int(value)
        bdata += numbertohex(idata, 2)
    elif isinstance(value, int):
        bdata += numbertohex(value, 2)
    else:
        print("excel输入格式错误")
    return bdata

#王梦新增，通过对应OAD找到对应数据类型
def makeOadtotype(value):
    if value in OOPSXDY:
        aa=OOPSXDY[value][0]
        return aa




# FRAME{ctrl,master,slaver,segment,buf}
# FRAME = {
# 'CTRL':'43'
# 'TSA_TYPE':'0'
# 'TSA_VS':'01',
# 'TSA_AD':'123456789012',
# 'CA':'00',
# 'SEG_WORD':'0000',
# 'APDU':'',
# 'CTRL_BS':{'C_DIR_bit7':'7_7,0','C_PRM_bit6':'6_6,1','C_SEG_bit5':'5_5,0','C_NULL_bit4':'4_4,0','C_CODE_bit3':'3_3',0,'C_AFN_bit20':'0_2',3'},
# 'TSA_BS':{'SA_TYPE_bit67':'6_7,0','SA_VS_bit45':'4_5,0','SA_LEN_bit30':'0_3,5','SA_AD':'123456789012'},
# 'SEG_NO_BS':{'SEG_INDEX_bit110':'0_11,0','SEG_NULL_bit1214':'12_14,0','SEG_TYPE_bit1415':'14_15,0',}}
def MakeFrame(frame):
    # buff = '68'
    ilen = 0
    buff = ''
    buff += frame['CTRL']
    buff += makeTSA(frame['TSA_TYPE'], frame['TSA_VS'], frame['TSA_AD'])
    buff += frame['CA']
    buff += frame['SEG_WORD']
    ilen = len(buff)//2
    ilen += 6
    ilen += len(frame['APDU'])/2
    buff = makelen(ilen) + buff
    buff = buff + OOP_CalcCRC(buff)
    buff += frame['APDU']
    buff = buff + OOP_CalcCRC(buff)
    buff = '68'+ buff + '16'
    return buff

# 'CTRL_BS': {'C_DIR': [7, 7, 0], 'C_PRM': [6, 6, 1], 'C_SEG': [5, 5, 0], 'C_NULL': [4, 4, 0],
# 'C_CODE': [3, 3, 0], 'C_AFN': [0, 2, 3]},
def GetCTRL_BS(data):
    dtmp = {}
    dtmp['C_DIR'] = [7, 7, int(getbit(data, 7, 8, 1), 2)]
    dtmp['C_PRM'] = [6, 6, int(getbit(data, 6, 7, 1), 2)]
    dtmp['C_SEG'] = [5, 5, int(getbit(data, 5, 6, 1), 2)]
    dtmp['C_NULL'] = [4, 4, int(getbit(data, 4, 5, 1), 2)]
    dtmp['C_CODE'] = [3, 3, int(getbit(data, 3, 4, 1), 2)]
    dtmp['C_AFN'] = [0, 2, int(getbit(data, 0, 3, 1), 2)]
    return dtmp

# 'SA_BS': {'SA_TYPE': [6, 7, 0], 'SA_VS': [4, 5, 0], 'SA_LEN': [0, 3, 5]},
def GetSA_BS(data):
    dtmp = {}
    dtmp['SA_TYPE'] = [6, 7, int(getbit(data, 6, 8, 1), 2)]
    dtmp['SA_VS'] = [4, 5, int(getbit(data, 4, 6, 1), 2)]
    dtmp['SA_LEN'] = [0, 3, int(getbit(data, 0, 4, 1), 2) + 1 ]
    return dtmp

# 'SEG_WORD_BS': {'SEG_INDEX': [0, 11, 0], 'SEG_NULL': [12, 13, 0], 'SEG_TYPE': [14, 15, 0]}
def GetSEG_WORD_BS(data):
    dtmp = {}
    dtmp['SEG_INDEX'] = [0, 11, int(getbit(data, 0, 12, 2), 2)]
    dtmp['SEG_NULL'] = [12, 13, int(getbit(data, 12, 14, 2), 2)]
    dtmp['SEG_TYPE'] = [14, 15, int(getbit(data, 14, 16, 2), 2)]
    return dtmp

# 加扰码加33  0022->3355
def Add33(data):
    stmp = ''
    for i in range(0, len(data), 2):
        itm = (int(data[i:i+2], 16) + 0x33) % 256
        stmp += hex(itm).replace('0x', '').zfill(2)
    return stmp

# 加扰码减33  3355->0022
def Reduce33(data):
    stmp = ''
    for i in range(0, len(data), 2):
        itm = (int(data[i:i+2], 16) - 0x33) % 256
        stmp += hex(itm).replace('0x', '').zfill(2)
    return stmp

# 处理连帧的情况
def Contirame(buff):
    rigtfrm = True
    frmlen = ''
    if CheckValid(buff) == False:
        return buff
    else:
        rigtfrm,frmlen = CheckValid(buff)
        if len(buff) > frmlen:
            if CheckValid(buff[frmlen:]) == False:
                return buff
            buff = buff[frmlen:]
            return buff
        else:
            return buff
# 解析帧
def GetFrame(buff):
    if CheckValid(buff) == False:
        return False, {}
    dfrm = {}
    ipos = 2
    dfrm['LEN'] = stoint(buff[ipos:ipos+4])
    ipos += 4
    dfrm['CTRL'] = buff[ipos:ipos+2]
    ipos += 2
    dfrm['CTRL_BS'] = GetCTRL_BS(dfrm['CTRL'])
    dfrm['SA'] = buff[ipos:ipos+2]
    ipos += 2
    dfrm['SA_BS'] = GetSA_BS(dfrm['SA'])
    # print(ipos)
    dfrm['TSA_TYPE'] = dfrm['SA_BS']['SA_TYPE'][2]
    dfrm['TSA_VS'] = dfrm['SA_BS']['SA_VS'][2]
    dfrm['TSA_AD'] = reverse(buff[ipos:ipos+dfrm['SA_BS']['SA_LEN'][2]*2])
    # print(dfrm['SA_BS']['SA_LEN'][2]*2)
    ipos += dfrm['SA_BS']['SA_LEN'][2]*2
    # print(ipos)
    dfrm['CA'] = buff[ipos:ipos+2]
    ipos += 2
    ipos += 4
    # print(dfrm['CTRL_BS']['C_CODE'][2])
    if dfrm['CTRL_BS']['C_CODE'][2] == 0:
        # print(buff)
        # print(ipos)
        dfrm['APDU'] = buff[ipos: dfrm['LEN']*2 + 4 - 6]
    else:
        dfrm['APDU'] = Reduce33(buff[ipos: dfrm['LEN']*2 + 2 - 6])
    if dfrm['CTRL_BS']['C_SEG'][2] == 1:
        dfrm['SEG_WORD'] = reverse(dfrm['APDU'][0:4])
        dfrm['SEG_WORD_BS'] = GetSEG_WORD_BS(dfrm['SEG_WORD'])
    else:
        dfrm['SEG_WORD'] = ''
        dfrm['SEG_WORD_BS'] = {}
    return True, dfrm
#  2100->33
def stoint(buff):
    if len(buff) != 4:
        return 0
    return int(reverse(buff), 16)
#
# # 合法帧检查
# def CheckValid(buff):
#     if len(buff) < MIN_LEN_OOP_FRAME:
#         print('Error_Frame length too short')
#         return False
#     if buff[0:2] == '68':
#         ilen = stoint(buff[2:6])
#         # print(buff[2+ilen*2:4+ilen*2])
#         if (ilen*2+4) > len(buff):
#             print('Error_Frame length')
#             return False
#         if buff[2+ilen*2:4+ilen*2] != '16':
#             print('Error_Frame 16')
#             return False
#         else:
#             if OOP_CheckCRC(buff[2:2+ilen*2]):
#                 return True
#             else:
#                 print('Error_Frame FCS')
#                 return False
#     print('Error_Frame 68')
#     return False

# 合法帧检查
def CheckValid(buff):
    if len(buff) < MIN_LEN_OOP_FRAME:
        # print('Error_Frame length too short')
        return False, 0
    if buff[0:2] == '68':
        ilen = stoint(buff[2:6])
        # print(buff[2+ilen*2:4+ilen*2])
        if (ilen*2+4) > len(buff):
            # print('Error_Frame length')
            return False, 0
        if buff[2+ilen*2:4+ilen*2] != '16':
            # print('Error_Frame 16')
            return False, 0
        else:
            if OOP_CheckCRC(buff[2:2+ilen*2]):
                ipos = 4+ilen*2
                return True, ipos
            else:
                # print('Error_Frame FCS')
                return False,0
    # print('Error_Frame 68')
    return False, 0

# '07E3 0B 1A 02 00 01 2A 0000' ->datetime
def hextodatetime(btime):
    # print(int(btime[16:],16)*1000)
    tt = datetime.datetime(int(btime[0:4], 16), int(btime[4:6], 16), int(btime[6:8], 16), int(btime[10:12], 16),
                           int(btime[12:14], 16), int(btime[14:16], 16) + int(btime[16:],16)*1000//1000000 ,
                           int(btime[16:],16)*1000%1000000 )
    return tt

# datetime->'07E3 0B 1A 02 00 01 2A 0000'  data_time
# 07e3 0c 02 00 0d2b22 0115
def datetimetohex(dt):
    btime = ''
    btime += hex(dt.year).replace('0x', '').zfill(4)
    btime += hex(dt.month).replace('0x', '').zfill(2)
    btime += hex(dt.day).replace('0x', '').zfill(2)
    btime += hex(dt.isoweekday()).replace('0x', '').zfill(2)
    # print(dt.isoweekday())
    btime += hex(dt.hour).replace('0x', '').zfill(2)
    btime += hex(dt.minute).replace('0x', '').zfill(2)
    btime += hex(dt.second).replace('0x', '').zfill(2)
    # ms
    btime += hex(dt.microsecond//1000).replace('0x', '').zfill(4)
    return btime

# 时间戳处理
def time_handle(time_str):
    timestr = ''
    str1 = time_str.split(' ')
    str2 = []
    for item in str1:
        if item != '':
            str2.append(item)
    YMD = str2[0].split('/')
    HMS = str2[1].split(':')
    for time_YMD in YMD:
        if len(time_YMD) < 2:
            timestr += time_YMD.zfill(2)
        else:
            timestr += time_YMD
    for time_HMS in HMS:
        if len(time_HMS) < 2:
            timestr += time_HMS.zfill(2)
        else:
            timestr += time_HMS
    return timestr

# 20191126 00 01 42 0000->   datetime
def bcdtodatetime(dt):
    if dt.find('-') >= 0:
        dt = dt.replace('-','').replace(' ','').replace(':','')
    dt.zfill(14)
    if len(dt) == 14:
        dt += '0000'
    tt = datetime.datetime(int(dt[0:4]), int(dt[4:6]), int(dt[6:8]), int(dt[8:10]),
                           int(dt[10:12]), int(dt[12:14]), int(dt[14:])*1000%1000000)
    return tt

# 1F 01 00B4 07E30B1A0000012A0000
def analy_LINK_APDU(buff):
    ds = {}
    # print(buff)
    ds['PIID'] = buff[0:2]
    #判断是心跳还是登录帧，可在此处做分支，来取心跳时间。
    ds['Req_Type'] = int(buff[2:4], 16)
    ds['Heart_Beat'] = int(buff[4:8],16)
    ds['Req_Time'] = hextodatetime(buff[8:])
    hearttimesave=str( ds['Req_Time']).replace('-', '').replace(" ", '').replace(":", '')
    print('hearttimesave:',hearttimesave)
    # print(ds)
    return ds,hearttimesave

# stime1 datetime  stime2 datetime ->07E30B1A0200012F 135C
def make_datetime(stime1, stime2):
    hextime = ''
    dd = stime2-stime1
    # print(dd)
    ms = dd.seconds *1000 + dd.microseconds//1000
    hextime += hex(stime2.year).replace('0x', '').zfill(4)
    hextime += hex(stime2.month).replace('0x', '').zfill(2)
    hextime += hex(stime2.day).replace('0x', '').zfill(2)
    hextime += hex(stime2.weekday()).replace('0x', '').zfill(2)
    hextime += hex(stime2.hour).replace('0x', '').zfill(2)
    hextime += hex(stime2.minute).replace('0x', '').zfill(2)
    hextime += hex(stime2.second).replace('0x', '').zfill(2)
    hextime += hex(ms).replace('0x', '').zfill(4)[-4:]
    return hextime


# now -> datetime_s  now()->0707E30B1A00012F
def makenowtodatetime_s():
    hextime = ""
    n = datetime.datetime.now()
    # print("时间格式：",n)
    hextime += hex(n.year).replace('0x', '').zfill(4)
    hextime += hex(n.month).replace('0x', '').zfill(2)
    hextime += hex(n.day).replace('0x', '').zfill(2)
    hextime += hex(n.hour).replace('0x', '').zfill(2)
    hextime += hex(n.minute).replace('0x', '').zfill(2)
    hextime += hex(n.second).replace('0x', '').zfill(2)
    return  hextime

# now -> datetime_s  wrong  n  ->0707E30B1A00012F
#王梦新增：无效时标
def makewrongdatetime_s():
    hextime = ""
    n=datetime.datetime(2020,3,1,0,0,0,0)
    # print("时间格式：",n)
    hextime += hex(n.year).replace('0x', '').zfill(4)
    hextime += hex(n.month).replace('0x', '').zfill(2)
    hextime += hex(n.day).replace('0x', '').zfill(2)
    hextime += hex(n.hour).replace('0x', '').zfill(2)
    hextime += hex(n.minute).replace('0x', '').zfill(2)
    hextime += hex(n.second).replace('0x', '').zfill(2)
    return  hextime


# 链路帧  out 输出响应帧
# 01 1F0100B407E30B1A0000012A0000 stime 20191112010203
# ->81 1F01 07E30B1A0000012A000007E30B1A0200012F135C07E30B1A0200012F135C
def make_LINK_APDU_Response(buff_APDU, stime):
    stmp = ''
    #01：代表预连接请求
    if buff_APDU[0:2] == '01':
        dapdu,hearttime = analy_LINK_APDU(buff_APDU[2:])
        stmp = '81'
        stmp += dapdu['PIID']
        stmp += '01'
        stmp += datetimetohex(dapdu['Req_Time'])
        stmp += make_datetime( dapdu['Req_Time'],bcdtodatetime(stime))
        stmp += make_datetime( dapdu['Req_Time'],datetime.datetime.now(),)
    return stmp.upper(),hearttime


EMUN_DAR = {'00': '成功', '01': '硬件失效', '02': '暂时失效', '03': '拒绝读写', '04': '对象未定义',
            '05': '对象接口类不符', '06': '对象不存在', '07': '类型不匹配', '08': '越界',
            '09': '数据块不可用', '0A': '分帧传输已取消', '0B': '不处于分帧传输状态', '0C': '块写取消',
            '0D': '不存在块写状态',
            '0E': '数据块序号无效', '0F': '密码错未授权', '10': '通信速率不能更改', '11': '年时区数超',
            '12': '日时段数超',
            '13': '费率数超', '14': '安全认证不匹配', '15': '重复充值', '16': 'ESAM验证失败', '17': '安全认证失败',
            '18': '客户编号不匹配', '19': '充值次数错误', '1A': '购电超囤积', '1B': '地址异常',
            '1C': '对称解密错误',
            '1D': '非对称解密错误', '1E': '签名错误', '1F': '电能表挂起', '20': '时间标签无效', '21': '请求超时',
            '22': 'ESAM的P1P2不正确', '23': 'ESAM的LC错误', 'FF': '其它'}

# DAR ->解释
def GetErrName(bDAR):
    sErr = EMUN_DAR[bDAR]
    if len(sErr) == 0:
        sErr = '未知错误'
    return sErr

#定义换算
SCALER_UNIT_4 = ['-4','23010700', '23010800', '23010900','23010300','23010400', '23011000','23011100', '23081000','23081100','23071000','23071100','23061000','23061100','23051000','23051100','23041000','23041100','23031000','23031100','23021000','23021100', '1010', '1011', '1012', '1013', '1020', '1021','24010F00',
                 '1022', '1023', '1030', '1031', '1032', '1033', '1040', '1041', '1042', '1043', '1050', '1051', '1052',
                 '1053', '1060', '1061', '1062', '1063', '1070', '1071', '1072', '1073', '1080', '1081', '1082', '1083',
                 '1090', '1091', '1092', '1093', '10A0', '10A1', '10A2', '10A3', '1110', '1111', '1112', '1113', '1120',
                 '1121', '1122', '1123', '1130', '1131', '1132', '1133', '1140', '1141', '1142', '1143', '1150', '1151',
                 '1152', '1153', '1160', '1161', '1162', '1163', '1170', '1171', '1172', '1173', '1180', '1181', '1182',
                 '1183', '1190', '1191', '1192', '1193', '11A0', '11A1', '11A2', '11A3', '2017', '2018', '2019', '201A',
                 '201B', '2004', '2005', '2006', '2007', '2008', '2009','8100','4019']
SPESCALER_4 = ['8103','8104','8105','8107','8108','23010B00','23020B00','23030B00','23040B00','23050B00',
               '23060B00','23070B00','23080B00'
               ]

SCALER_UNIT_3 = ['-3', '20010200', '2001', '200A','20010400']
SCALER_UNIT_2 = ['-2', '0000', '0010', '0011', '0012', '0013', '0020', '0021', '0022', '0023', '0030', '0031', '0032',
                 '0033', '0040', '0041', '0042', '0043', '0050', '0051', '0052', '0053', '0060', '0061', '0062', '0063',
                 '0070', '0071', '0072', '0073', '0080', '0081', '0082', '0083', '0090', '0091', '0092', '0093', '00A0',
                 '00A1', '00A2', '00A3', '0110', '0111', '0112', '0113', '0120', '0121', '0122', '0123', '0210', '0211',
                 '0212', '0213', '0220', '0221', '0222', '0223', '0300', '0301', '0302', '0303', '0400', '0401', '0402',
                 '0403', '0500', '0501', '0502', '0503', '200B', '200C', '200D', '200E', '200F', '2011', '2012', '2026',
                 '2027', '2028', '2029', '202C', '202D', '202E', '2031', '2032','3040']
SCALER_UNIT_1 = ['-1', '20000200', '2000', '2002', '2003', '2010','301F','4030']
SCALER_UNIT_BS = ['BS', '2014', '2015', '2040', '2041',"4500"]

#long_usigned:换算为-1的标识（事件）
long_usigned_scalerlist=['30000500','300005000','30010500','300105000','30020500','300205000',
'30030500','300305000','30040500','300405000','30060500','300605000']
#double_long:换算为-4的标识（事件）
double_long_scalerlist=['30000500','300005000','30030500','300305000','30040500','300405000',
'30050500','300505000','30060500','300605000' ]
#double_long:换算为-1的标识（事件）
double_long_1_scalerlist=['30070500','300705000','30080500','300805000' ]

#double_long_unsigned:换算为-4
double_long_unsignedlist=['30090600','300A0600','300B0500','300B05000','40190200','40180200']


# 无符号数值转换
def hextonum(soad,data):
    sValue = ''
    if (soad[:4] in SCALER_UNIT_4 )or (soad=="80000201")or (soad=="301F0600") or (soad in double_long_unsignedlist) or (soad  in SCALER_UNIT_4 ):
        fv = int(data, 16) * 0.0001
        sValue = str(float('%.4f' % fv))
    elif soad[:4] in SCALER_UNIT_3:
        fv = int(data, 16) * 0.001
        sValue = str(float('%.3f' % fv))
    elif soad[:4] in SCALER_UNIT_2:
        fv = int(data, 16) * 0.01
        sValue = str(float('%.2f' % fv))
    elif soad[:4] in SCALER_UNIT_1 or (soad in long_usigned_scalerlist ):
        fv = int(data, 16) * 0.1
        sValue = str(float('%.1f' % fv))
    elif soad[:4] in SCALER_UNIT_BS:
        sValue = str(int(data, 16))
    else:
        sValue = str(int(data, 16))
    return sValue

# '0000317D'->'126.69'
def hextolong_unsigned(soad,data):
    sValue = ''
    if soad  in SCALER_UNIT_2:
        sValue = str(int(data, 16)*0.01)
    elif soad  in SCALER_UNIT_1:
        sValue = str(int(data, 16)*0.1)
    else:
        sValue = data
    return sValue
#报文中的bit_string转为正确的16进制（bit—string在698中是倒置的，例如：8C00->0031）
def bitstrtohex(buffhex):
    b = bin(int(buffhex, 16))[2:].zfill(len(buffhex) * 4)
    c = b[::-1]
    d = hex(int(c, 2))[2:].zfill(len(buffhex)).upper()
    return d



# 带符号 '00000000B11FEEE0' ->'297166.0000' DT_long64
def hextolong64(soad,data):
    sValue = ''
    idata = int(data, 16)
    if idata >= 0x8000000000000000:
        idata = idata - 0x10000000000000000
    if (soad[:4] in SCALER_UNIT_4) or (soad[:4] in SPESCALER_4) or (soad in SPESCALER_4) or (soad  in SCALER_UNIT_4 ):
        idata=str(idata)
        #这种转换方法，考虑到特别大的浮点数，这样小数位数不会丢失。
        idata1=idata[0:-4]
        idata2=idata[-4:]
        if idata2 == '0000' or idata2 == '0':
            if idata1=="":
                sValue = '0.0'
            else:
                sValue = idata1 + '.0'
        else:
            if idata1 == '':
                sValue = '0' + '.' + idata2.zfill(4)
            else:
                sValue = idata1 + '.' + idata2
    elif soad[:4] in SCALER_UNIT_1 :
        fv = idata*0.1
        sValue = str(float('%.1f' % fv))
    else:
        sValue = str(idata)
    return sValue
# 带符号 ''40A1F20000000000'' ->'2297.0' DT_float64
def hextofloat64(soad,data):
    sValue = ''
    data1 = int(data, 16)
    idata = General.hex2float64(data1)
    if (soad[:4] in SCALER_UNIT_4) or (soad[:4] in SPESCALER_4) or (soad in SPESCALER_4):
        fv = idata / 10000
        sValue = str(float('%.4f' % fv))
    elif soad[:4] in SCALER_UNIT_3:
        fv = idata /1000
        sValue = str(float('%.3f' % fv))
    elif soad[:4] in SCALER_UNIT_2:
        fv = idata /100
        sValue = str(float('%.2f' % fv))
    elif soad[:4] in SCALER_UNIT_1 :
        fv = idata/10
        sValue = str(float('%.1f' % fv))
    else:
        sValue = str(idata)
    return sValue


# "429325BD" ->'73.57371' DT_float32
def hextofloat32(soad,data):
    sValue = ''
    idata = General.hex2float32(data)
    if (soad[:4] in SCALER_UNIT_4) or (soad[:4] in SPESCALER_4) or (soad in SPESCALER_4):
        fv = idata / 10000
        sValue = str(float('%.4f' % fv))
    elif soad[:4] in SCALER_UNIT_3:
        fv = idata /1000
        sValue = str(float('%.3f' % fv))
    elif soad[:4] in SCALER_UNIT_2:
        fv = idata /100
        sValue = str(float('%.2f' % fv))
    elif soad[:4] in SCALER_UNIT_1 :
        fv = idata/10
        sValue = str(float('%.1f' % fv))
    else:
        sValue = str(idata)
    return sValue

#王梦新增，16进制转10进制
def hextoten(soad,data):
    sValue = ''
    sValue = int(data, 16)
    if sValue >= 0x80:
        sValue = sValue - 0x100
    sValue=str(sValue)
    return sValue

# def intdt_long(soad,data):
#     sValue = ''
#     idata = int(data, 16)
#     sValue=str(idata-256)
#     return sValue


#行方法解析函数  报文格式转：['选择方法8',['FFFF/FF/FF/FF/FF/FF','FFFF/FF/FF/FF/FF/FF','1日','一组用户类型,[4,5,13,14,23,24,33,34]']]
def Rsdtovalue(aa,i):
    cc=''
    bb=aa[i:i+2]
    i+=2
    cc+="['"+ getkey(OOP_RSD_CHOICE_VALUE, bb)+ "',["
    #行方法选择10
    if bb== '0A':
        cc +=  str(int(aa[i:i+2], 16))+ ","
        i += 2
        sValue1, i = MsAnaly(i, aa)
        cc += sValue1
    #行方法选择7
    elif bb== '06'or bb== '07'or bb== '08':
        cc += "'" + hextodatetime_s(aa[i:i + 14]) + "',"
        i += 14
        cc += "'" + hextodatetime_s(aa[i:i + 14]) + "',"
        i += 14
        cc += "'" + hextoTI(aa[i:i + 6]) + "',"
        i += 6
        sValue1, i = MsAnaly(i, aa)
        cc += sValue1
    else:print("增加RSD处理：行方法1,2,3,4,5,9,10")
    cc+="]]"
    return cc,i
def timespcialdisplay(data):
    sValue = ''
    data1 = [data[0:4],data[4:6],data[6:8],data[8:10],data[10:12],data[12:]]
    for item in data1:
        sValue+=item + '-'
    sValue=sValue[:-1]
    return sValue


# '07E30C04111E28'->'20191204173040'
def hextodatetime_s(data):
    sValue = ''
    if data == 'FFFFFFFFFFFFFF':
        sValue='FFFFFFFFFFFFFF'
    else:
        sValue += str(int(data[0:4], 16)).zfill(4)
        sValue += str(int(data[4:6], 16)).zfill(2)
        sValue += str(int(data[6:8], 16)).zfill(2)
        sValue += str(int(data[8:10], 16)).zfill(2)
        sValue += str(int(data[10:12], 16)).zfill(2)
        sValue += str(int(data[12:14], 16)).zfill(2)
        #将时间转换为时间格式
        # sValue = str(bcdtodatetime(sValue))
    return sValue

# '07E30C0405'->'2019120405'十六进制报文，转为时间（日期date数据类型处理）
def hextodate(data):
    sValue = ''
    if data == 'FFFFFFFFFF':
        sValue='FFFFFFFFFF'
    else:
        sValue += str(int(data[0:4], 16)).zfill(4)
        sValue += str(int(data[4:6], 16)).zfill(2)
        sValue += str(int(data[6:8], 16)).zfill(2)
        sValue += str(int(data[8:10], 16)).zfill(2)
    return sValue

def hextospecialdatetime_s(data):#8104厂休控，时间格式特殊处理
    sValue = ''
    sValue += str(int(data[8:10], 16)).zfill(2)
    sValue += str(int(data[10:12], 16)).zfill(2)
    sValue += str(int(data[12:14], 16)).zfill(2)
    return sValue

def hextosdatetime_s(data):#8104厂休控，时间格式特殊处理
    sValue = ''
    sValue += str(int(data[0:4], 16)).zfill(4)
    sValue += str(int(data[4:6], 16)).zfill(2)
    sValue += str(int(data[6:8], 16)).zfill(2)
    sValue += str(int(data[8:10], 16)).zfill(2)
    sValue += str(int(data[10:12], 16)).zfill(2)
    if str(data[12:14]) == 'FF':
        sValue += "FF"
    else:
        sValue += str(int(data[12:14], 16)).zfill(2)
    return sValue

def hextospecial8105datetime_s(data): #8105营业报停控，时间格式特殊处理
    sValue = ''
    sValue += str(int(data[0:4], 16)).zfill(4)
    sValue += str(int(data[4:6], 16)).zfill(2)
    sValue += str(int(data[6:8], 16)).zfill(2)
    return sValue


def hextovisble(h):#16进制转gb2312编码格式的字节串，编码成gb2312格式中英文
    p1 = bytes(h, 'gb2312')
    p2 = a2b_hex(p1)
    ee = p2.decode('gb2312')
    return ee



# 王梦新增：time类型解析：173B3B->235959
def hextotime(data):
    sValue = ''
    sValue += str(int(data[0:2], 16)).zfill(2)
    sValue += str(int(data[2:4], 16)).zfill(2)
    sValue += str(int(data[4:6], 16)).zfill(2)
    return sValue
#double_long16进制，转为界面显示的形式(带点的形式)
def hextoversionpoint(data):
    sValue = ''
    data1 = []
    i=0
    data1 = [data[0:2],data[2:4],data[4:6],data[6:]]
    for item in data1:
        if item[:1] == '0':
            item = item[1:]
        else:pass
        sValue += item +"."
    sValue = sValue[:-1]
    return sValue






# 有符号 000007AE->1.996, FFFFEB02->-5.374 DT_double_long
def hextodouble_long(soad,data):
    sValue = ''
    idata = int(data, 16)
    if idata >= 0x80000000:
        idata = idata - 0x100000000
    else:
        idata=idata
    if soad[:4] in SCALER_UNIT_3:
        fv = idata*0.001
        sValue = str(float('%.3f' % fv))
    elif soad[:4] in SCALER_UNIT_2:
        fv = idata * 0.01
        sValue = str(float('%.2f' % fv))
    elif soad[:4] in SCALER_UNIT_1 or  (soad in double_long_1_scalerlist):
        fv = idata * 0.1
        sValue = str(float('%.1f' % fv))
    elif soad[:4] in SCALER_UNIT_4 or  (soad in double_long_scalerlist) or (soad  in SCALER_UNIT_4 ):
        fv = idata * 0.0001
        sValue = str(float('%.4f' % fv))

    elif soad[:4] in SCALER_UNIT_BS:
        sValue = str(idata)
    else:
        sValue = str(idata)
    return sValue

# # 有符号  DT_long
def hextolong(soad,data):
    sValue = ''
    idata = int(data, 16)
    if idata >= 0x8000:
        idata = idata - 0x10000
    else:
        idata=idata
    if soad[:4] in SCALER_UNIT_3:
        fv = idata*0.001
        sValue = str(float('%.3f' % fv))
    elif soad[:4] in SCALER_UNIT_2 or soad == '301E0600' :
        fv = idata * 0.01
        sValue = str(float('%.2f' % fv))
    elif soad[:4] in SCALER_UNIT_1 or soad == '300C0600' or soad == '301D0600'or soad == '303B0500':
        fv = idata * 0.1
        sValue = str(float('%.1f' % fv))
    elif soad[:4] in SCALER_UNIT_BS:
        sValue = str(idata)

    else:
        pass
    return sValue


EMUN_RATED = {'00': '秒', '01': '分', '02': '时', '03': '日', '04': '月', '05': '年'}
CHOICE_MS = {'00': '无表计', '01': '全部用户地址', '02': '一组用户类型', '03': '一组用户地址',
             '04': '一组配置序号', '05': '一组用户类型区间', '06': '一组用户地址区间', '07': '一组配置序号区间'}
#波特率选择
CHOICE_BR = {'00': '300', '01': '600', '02': '1200', '03': '2400',
             '04': '4800', '05': '7200', '06': '9600', '07': '19200','08': '38400', '09': '57600', '10': '115200', '255': '自适应',}
#校验位选择
CHOICE_CRC = {'00': '无校验', '01': '奇校验', '02': '偶校验'}

#数据位选择
CHOICE_DATA = {'05': '5', '06': '6','07': '7', '08': '8','00':'0'}

#停止位选择
CHOICE_STOP = {'01': '1', '02': '2','00':'0'}

#流控选择
CHOICE_CTRO = {'00': '无', '01': '硬件', '02': '软件'}


# MS解析：
def MsAnaly(ipos, data):
    sValue = ""
    Mstype = data[ipos:ipos + 2]
    sValue += "'" + CHOICE_MS[Mstype] + ","
    ipos += 2
    if Mstype == "01":
        sValue = sValue[:-1] + "'"
        ipos=ipos
    else:
        Mslen = int(data[ipos:ipos + 2], 16)
        ipos += 2
    if Mstype == "02":
        sValue += "["
        for i in range(0, Mslen, 1):
            sValue += hextonum('', data[ipos:ipos + 2]) + ","
            ipos += 2
        sValue = sValue[:-1] + "]'"
    elif Mstype == "03":
        sValue += "["
        for i in range(0, Mslen, 1):
            octetLen = int(data[ipos:ipos + 2], 16)
            ipos += 2
            sValue += data[ipos: ipos + 2 * octetLen] + ","
            ipos += 2 * octetLen
        sValue =  sValue[:-1] + "]'"
    elif Mstype == "04":
        sValue += "["
        for i in range(0, Mslen, 1):
            sValue += hextonum('', data[ipos:ipos + 4]) + ","
            ipos += 4
        sValue =  sValue[:-1] + "]'"
    elif Mstype == "05":
        for i in range(0, Mslen, 1):
            sValue += "["
            sValue += data[ipos+1:ipos + 2] + ","
            ipos += 4
            sValue += hextonum('', data[ipos:ipos + 2]) + ","
            ipos += 4
            sValue += hextonum('', data[ipos:ipos + 2]) + "],"
            ipos += 2
        sValue = sValue[:-1] + "'"
    elif Mstype == "06":
        for i in range(0, Mslen, 1):
            sValue += "["
            sValue += data[ipos+1:ipos + 2] + ","
            ipos += 4
            octetLen = int(data[ipos:ipos + 2], 16)
            ipos += 2
            sValue += data[ipos: ipos + 2 * octetLen] + ","
            ipos += 2 * octetLen + 2
            octetLen = int(data[ipos:ipos + 2], 16)
            ipos += 2
            sValue += data[ipos: ipos + 2 * octetLen] + "],"
            ipos += 2 * octetLen
        sValue = sValue[:-1] + "'"
    elif Mstype == "07":
        for i in range(0, Mslen, 1):
            sValue += "["
            sValue += data[ipos+1:ipos + 2] + ","
            ipos += 4
            sValue += hextonum('', data[ipos:ipos + 4]) + ","
            ipos += 6
            sValue += hextonum('', data[ipos:ipos + 4]) + "],"
            ipos += 4
        sValue = sValue[:-1] + "'"
    elif Mstype == "01":
        pass
    else:
        print("MS类型解析错误")
    return  sValue,ipos






def hextoTI(data):
    sValue= ''
    if len(data) >= 6:
        sValue += str(int(data[2:6], 16))
        sValue += EMUN_RATED[data[0:2]]
    return sValue
#王梦新增：IP解析：例如："C08A7F7F"->"192.168.127.127"
def octetIp(data):
    bb = ''
    for item in range(0, len(data), 2):
        cc = data[item:item + 2]
        aa = int(cc, 16)
        bb += str(aa) + "."
    ss = bb.strip(".")
    return ss


def hextotimeregion(hextot):#王梦新增：做告警时段解析函数，将F08FFF->0-3,8,12-23
    bb = bin(int(hextot, 16))[2:]
    cc = str(bb)
    i = -1
    bb = ""
    for item in cc:
        i += 1
        if item == "1":

            bb += str(i) + ","
        else:
            bb += str("-")
    print(bb)
    bb = bb.split("-")
    print(bb)
    e = ""
    for item in bb:
        if len(item) > 2:
            item = item.strip(",")

            item = item.split(",")
            e += item[0] + "-" + item[len(item) - 1] + ","
            print(e)
        elif len(item) > 1:
            item = item.strip(",")
            e += item + ","
    timeregion = e.strip(",")
    return timeregion



# 解帧函数  010506000030B00600000000060000000006000030B00600000000->'124.64,0,0,0,124.64,0',ipos
#读取记录型的值才会用到 reuse参数
def GetRequestNormalValue(soad, data,reuse):
    sValue = ''
    ipos = 0
    it = int(data[ipos:ipos+2], 16)
    ipos += 2
    if it == DT_array or it == DT_structure:
        sValue += '['
        ia = int(data[ipos:ipos+2], 16)
        ipos += 2
        for i in range(0, ia, 1):
            it1 = int(data[ipos:ipos+2], 16)
            ipos += 2
            if it1 == DT_array or it1 == DT_structure:
                sValue += '['
                ib = int(data[ipos:ipos+2], 16)
                ipos += 2
                for j in range(0, ib, 1):
                    it2 =  int(data[ipos:ipos+2], 16)
                    ipos += 2
                    if it2 == DT_array or it2 == DT_structure:
                        sValue += '['
                        ic = int(data[ipos:ipos + 2], 16)
                        ipos += 2
                        for k in range(0, ic, 1):
                            it3 = int(data[ipos:ipos + 2], 16)
                            ipos += 2
                            if it3 == DT_array or it3 == DT_structure:
                                sValue += '['
                                id = int(data[ipos:ipos + 2], 16)
                                ipos += 2
                                for j3 in range(0, id, 1):#王梦修改：这里不可以用j来循环，在it1=DT_structure时，已经用了j来循环，故修改j为j3
                                    it4 = int(data[ipos:ipos + 2], 16)
                                    ipos += 2
                                    if it4 == DT_unsigned:
                                        sValue += str(int(data[ipos:ipos + 2], 16))
                                        ipos += 2
                                    elif it4 == DT_array or it4 == DT_structure:
                                        sValue += '['
                                        ie = int(data[ipos:ipos + 2], 16)
                                        ipos += 2
                                        for k in range(0, ie, 1):
                                            it5 = int(data[ipos:ipos + 2], 16)
                                            ipos += 2
                                            if it5 == DT_enum:
                                                sValue += str(int(data[ipos:ipos + 2], 16))
                                                ipos += 2
                                            elif it5 == DT_unsigned:
                                                sValue += str(int(data[ipos:ipos + 2], 16))
                                                ipos += 2
                                            elif it5 == DT_array or it5 == DT_structure:
                                                #王梦新增（601C0200）
                                                sValue += '['
                                                ig = int(data[ipos:ipos + 2], 16)
                                                ipos += 2
                                                for k5 in range(0, ig, 1):
                                                    it6 = int(data[ipos:ipos + 2], 16)
                                                    ipos += 2
                                                    if it6 == DT_enum:
                                                        sValue += str(int(data[ipos:ipos + 2], 16))
                                                        ipos += 2
                                                    elif it6 == DT_unsigned:
                                                        sValue += str(int(data[ipos:ipos + 2], 16))
                                                        ipos += 2
                                                    elif it6 == DT_array or it6 == DT_structure:
                                                        sValue += '['
                                                        ih = int(data[ipos:ipos + 2], 16)
                                                        ipos += 2
                                                        for k6 in range(0, ih, 1):
                                                            it7 = int(data[ipos:ipos + 2], 16)
                                                            ipos += 2
                                                            if it7 == DT_enum:
                                                                sValue += str(int(data[ipos:ipos + 2], 16))
                                                                ipos += 2
                                                            elif it7 == DT_unsigned:
                                                                sValue += str(int(data[ipos:ipos + 2], 16))
                                                                ipos += 2
                                                            elif it7 == DT_array or it7 == DT_structure:
                                                                print('try7')
                                                                print(data[ipos:])
                                                            elif it7 == DT_double_long_unsigned:
                                                                sValue += hextonum(soad, data[ipos:ipos + 8])
                                                                ipos += 8
                                                            elif it7 == DT_NULL:
                                                                sValue += "'NULL'"
                                                            elif it7 == DT_long_unsigned:
                                                                sValue += hextonum('', data[ipos:ipos + 4])
                                                                ipos += 4
                                                            elif it7 == DT_bool:  ##bool类型的数据解析
                                                                sValue += data[ipos+1:ipos + 2]
                                                                ipos += 2
                                                            elif it7 == DT_octet_string:
                                                                octetLen = int(data[ipos:ipos + 2], 16)
                                                                ipos += 2
                                                                sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
                                                                ipos += 2 * octetLen
                                                            ## 增加elif
                                                            else:
                                                                print('GetRequestNormalValue it7 增加类型处理',data[ipos:])
                                                                sValue += data[ipos:]
                                                            if k6 < ih - 1: sValue += ','
                                                        sValue += ']'
                                                    elif it6 == DT_double_long_unsigned:
                                                        sValue += hextonum(soad, data[ipos:ipos + 8])
                                                        ipos += 8
                                                    elif it6 == DT_NULL:
                                                        sValue += "'NULL'"
                                                    elif it6 == DT_long_unsigned:
                                                        sValue += hextonum('', data[ipos:ipos + 4])
                                                        ipos += 4
                                                    elif it6 == DT_bool:  ##bool类型的数据解析
                                                        sValue += data[ipos+1:ipos + 2]
                                                        ipos += 2
                                                    elif it6 == DT_octet_string:
                                                        octetLen = int(data[ipos:ipos + 2], 16)
                                                        ipos += 2
                                                        sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
                                                        ipos += 2 * octetLen
                                                    else:
                                                        print('GetRequestNormalValue it6 增加类型处理',data[ipos:])
                                                        sValue += data[ipos:]
                                                    if k5 < ig - 1: sValue += ','
                                                sValue += ']'
                                            elif it5 == DT_double_long_unsigned:
                                                sValue += hextonum(soad, data[ipos:ipos + 8])
                                                ipos += 8
                                            elif it5 == DT_NULL:
                                                sValue += "'NULL'"
                                            elif it5 == DT_long_unsigned:
                                                sValue += hextonum('', data[ipos:ipos + 4])
                                                ipos += 4
                                            elif it5 == DT_bool:  ##bool类型的数据解析
                                                sValue += data[ipos+1:ipos + 2]
                                                ipos += 2
                                            elif it5 == DT_octet_string:
                                                octetLen = int(data[ipos:ipos + 2], 16)
                                                ipos += 2
                                                sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
                                                ipos += 2 * octetLen
                                            ## 增加elif
                                            else:
                                                print('GetRequestNormalValue it5 增加类型处理',data[ipos:])
                                                sValue += data[ipos:]
                                            if k < ie - 1: sValue += ','
                                        sValue += ']'
                                    elif it4 == DT_enum:
                                        sValue += str(int(data[ipos:ipos + 2], 16))
                                        ipos += 2
                                    elif it4 == DT_double_long_unsigned:
                                        sValue += hextonum(soad, data[ipos:ipos + 8])
                                        ipos += 8
                                    elif it4 == DT_NULL:
                                        sValue += "'NULL'"
                                    elif it4 == DT_TI:
                                        sValue += "'" + hextoTI(data[ipos:ipos + 6]) + "'"
                                        ipos += 6
                                    elif it4 == DT_long_unsigned:
                                        sValue+= hextonum('', data[ipos:ipos + 4])
                                        ipos += 4
                                    elif it4 == DT_octet_string:
                                        octetLen = int(data[ipos:ipos + 2], 16)
                                        ipos += 2
                                        if (octetLen == 4) and (soad in Iplist):  # 王梦新增：IP解析
                                            sValue += "'" + octetIp(data[ipos: ipos + 2 * octetLen]) + "'"
                                        else:
                                            sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
                                        ipos += 2 * octetLen
                                    ##elif 增加其它数据类型解析
                                    elif it4 == DT_ROAD:
                                        sValue += "['" + data[ipos:ipos + 8] + "'"+',['
                                        ipos += 8
                                        Oadlen=int(data[ipos:ipos + 2],16)
                                        ipos += 2
                                        for ilen in range(0,Oadlen,1):
                                            sValue += "'" + data[ipos:ipos + 8] + "'"+','
                                            ipos += 8
                                        sValue=sValue[:-1]+']]'
                                    elif it4 == DT_OAD:
                                        sValue += "'" + data[ipos:ipos + 8] + "'"
                                        ipos += 8
                                    elif it4 == DT_MS:
                                        sValue1, ipos = MsAnaly(ipos, data)
                                        sValue += sValue1
                                    elif it4 == DT_TSA:
                                        octetLen = int(data[ipos:ipos + 2], 16)
                                        ipos += 2
                                        sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
                                        ipos += 2 * octetLen
                                    elif it4 == DT_bool:  ##bool类型的数据解析
                                        sValue += data[ipos+1:ipos + 2]
                                        ipos += 2
                                    elif it4 == DT_RCSD:
                                        DT_CSDLen = int(data[ipos:ipos + 2], 16)
                                        ipos += 2
                                        sValue +="["
                                        for CSDLen in range(0,DT_CSDLen ,1):
                                            if data[ipos:ipos + 2] == "00":
                                                ipos += 2
                                                sValue +=  "'" + data[ipos:ipos + 8]+ "'"+','
                                                ipos += 8
                                            elif data[ipos:ipos + 2] == "01":
                                                ipos += 2
                                                sValue += "'" + data[ipos:ipos + 8] + "'"+',['
                                                ipos += 8
                                                Oadlen=int(data[ipos:ipos + 2],16)
                                                ipos += 2
                                                for iOadlen in range(0,Oadlen,1):
                                                    sValue += "'" + data[ipos:ipos + 8] + "'"+','
                                                    ipos += 8
                                                sValue=sValue[:-1]+']'
                                                if CSDLen < DT_CSDLen - 1: sValue += ','


                                            else:print('try4:RCSD', data[ipos:])
                                        sValue += "]"
                                    elif it4 == DT_RSD:
                                        sValue4,ipos=Rsdtovalue(data,ipos)
                                        sValue +=sValue4



                                    else:
                                        print('try4:', data[ipos:])
                                        sValue += data[ipos:]
                                    if j3 < id - 1: sValue += ','
                                sValue += ']'
                            elif it3 == DT_TSA:
                                octetLen = int(data[ipos:ipos + 2], 16)
                                ipos += 2
                                sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
                                ipos += 2 * octetLen
                            elif it3 == DT_visible_string:  # 王梦新增
                                visibleLen = int(data[ipos:ipos + 2], 16)
                                if visibleLen > 127:
                                    ipos += 2
                                    visibleLen = int(data[ipos:ipos + 2], 16)
                                    ipos += 2
                                else:
                                    ipos += 2
                                visibleaa1 = data[ipos: ipos + 2 * visibleLen]
                                visiblec1 = hextovisble(visibleaa1)  # 将十六进制转中英文
                                sValue += "'" + visiblec1 + "'"
                                ipos += 2 * visibleLen

                            elif it3 == DT_Region:#王梦新增，区间统计解析，区间定义为一个列表的形式进行处理
                                sValue += "["
                                rEgiontype1=0
                                rEgiontype2 = 0
                                sValue+= data[ipos:ipos +2] +","
                                ipos += 2
                                rEgiontype1=int(data[ipos:ipos + 2], 16)
                                ipos += 2
                                if rEgiontype1 == DT_long_unsigned:
                                    sValue += hextonum(regiongoad, data[ipos:ipos + 4])+","
                                    ipos += 4
                                elif rEgiontype1 == DT_double_long:
                                    sValue += hextodouble_long(regiongoad, data[ipos:ipos + 8])+","
                                    ipos += 8
                                elif rEgiontype1 == DT_long:
                                    sValue += hextolong(regiongoad, data[ipos:ipos + 4])+","
                                    ipos += 4
                                rEgiontype2 = int(data[ipos:ipos + 2], 16)
                                ipos += 2
                                if rEgiontype2 == DT_long_unsigned:
                                    sValue += hextonum(regiongoad, data[ipos:ipos + 4])+"]"
                                    ipos += 4
                                elif rEgiontype2 == DT_double_long:
                                    sValue += hextodouble_long(regiongoad, data[ipos:ipos + 8])+"]"
                                    ipos += 8
                                elif rEgiontype2 == DT_long:
                                    sValue += hextolong(regiongoad, data[ipos:ipos + 4])+"]"
                                    ipos += 4
                                else:
                                    print(u"增加区间统计属性解析")



                            elif it3 == DT_enum:
                                sValue += str(int(data[ipos:ipos + 2], 16))
                                ipos += 2
                            elif it3 == DT_OAD:
                                sValue += "'" + data[ipos:ipos + 8] + "'"
                                ipos += 8
                            elif it3 == DT_octet_string:
                                octetLen = int(data[ipos:ipos + 2], 16)
                                ipos += 2
                                sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
                                ipos += 2 * octetLen
                            elif it3 == DT_unsigned:
                                sValue += str(int(data[ipos:ipos + 2], 16))
                                ipos += 2
                            elif it3 == DT_long_unsigned:
                                sValue += str(int(data[ipos:ipos + 4], 16))
                                ipos += 4
                            elif it3 == DT_TI:
                                sValue += "'" + hextoTI(data[ipos:ipos + 6]) + "'"
                                ipos += 6
                            elif it3 == DT_date_time_s:
                                sValue += "'" + hextodatetime_s(data[ipos:ipos + 14]) + "'"
                                ipos += 14
                            elif it3 == DT_NULL:
                                sValue += "'NULL'"
                            elif it3 == DT_CSD:
                                csdtype3 = int(data[ipos:ipos + 2], 16)
                                ipos += 2
                                if csdtype3 == 0: # oad
                                    sValue += "'" + data[ipos:ipos + 8] + "'"
                                    ipos += 8
                                elif csdtype3 == 1: # road
                                    sValue += "'" + data[ipos:ipos + 8] + "',["
                                    ipos += 8
                                    road_len3 = int(data[ipos:ipos + 2], 16)
                                    ipos += 2
                                    for k1 in range(0, road_len3, 1):
                                        sValue += "'" + data[ipos:ipos + 8] + "'"
                                        ipos += 8
                                        if k1 < road_len3 - 1: sValue += ','
                                    sValue += ']'
                            elif it3 == DT_MS:
                                sValue1, ipos = MsAnaly(ipos, data)
                                sValue += sValue1
                            elif it3 == DT_double_long_unsigned:
                                sValue += hextonum(soad, data[ipos:ipos + 8])
                                ipos += 8
                            elif it3 == DT_bit_string:  # 王梦新增#现在用例预期值没有要求转为2进制，若后期新增需求，可调整该流程。
                                bitLen = int(data[ipos:ipos + 2], 16)
                                ipos += 2
                                hexreallen = int(bitLen / 4)
                                if bitLen % 4 > 0:
                                    hexreallen += 1
                                sValue += "'" + bitstrtohex(data[ipos: ipos + hexreallen])+"'"
                                ipos +=  hexreallen
                            elif it3 == DT_long64:
                                sValue += hextolong64(soad, data[ipos:ipos + 16])
                                ipos += 16
                            elif it3 == DT_ROAD:
                                sValue += "['" + data[ipos:ipos + 8] + "'" + ',['
                                ipos += 8
                                Oadlen = int(data[ipos:ipos + 2], 16)
                                ipos += 2
                                for ilen in range(0, Oadlen, 1):
                                    sValue += "'" + data[ipos:ipos + 8] + "'" + ','
                                    ipos += 8
                                sValue = sValue[:-1] + ']]'
                            elif it3 == DT_bool:  ##bool类型的数据解析
                                sValue += data[ipos+1:ipos + 2]
                                ipos += 2
                            elif it3 == DT_RCSD:
                                DT_CSDLen = int(data[ipos:ipos + 2], 16)
                                ipos += 2
                                sValue += "["
                                for CSDLen in range(0, DT_CSDLen, 1):
                                    if data[ipos:ipos + 2] == "00":
                                        ipos += 2
                                        sValue += "'" + data[ipos:ipos + 8] + "'" + ','
                                        ipos += 8
                                    elif data[ipos:ipos + 2] == "01":
                                        ipos += 2
                                        sValue += "'" + data[ipos:ipos + 8] + "'" + ',['
                                        ipos += 8
                                        Oadlen = int(data[ipos:ipos + 2],16)
                                        ipos += 2
                                        for iOadlen in range(0, Oadlen, 1):
                                            sValue += "'" + data[ipos:ipos + 8] + "'" + ','
                                            ipos += 8
                                        sValue = sValue[:-1] + '],'
                                    else:
                                        print('try3:RCSD', data[ipos:])
                                sValue += "]"
                            elif it3 == DT_RSD:
                                sValue4, ipos = Rsdtovalue(data, ipos)
                                sValue += sValue4
                            else:
                                print('try3:', data[ipos:])
                                sValue += data[ipos:]
                            if k < ic-1: sValue += ','
                        sValue += ']'
                    elif it2 == DT_TSA:
                        octetLen = int(data[ipos:ipos + 2], 16)
                        ipos += 2
                        sValue += "'" + data[ipos: ipos + 2*octetLen] + "'"
                        ipos += 2*octetLen
                    elif it2 == DT_enum:
                        sValue += str(int(data[ipos:ipos + 2], 16))
                        ipos += 2
                    elif it2 == DT_OAD:
                        regiongoad=""#王梦新增：区间统计时，取出具体的OAD，数据解析时，换算的时候会用到
                        sValue += "'" + data[ipos:ipos + 8] + "'"
                        regiongoad = data[ipos:ipos + 8]
                        ipos += 8

                    elif it2 == DT_octet_string:
                        octetLen = int(data[ipos:ipos + 2], 16)
                        ipos += 2
                        octetData=str(data[ipos: ipos + 2*octetLen])
                        if len(octetData) == 8:  # 王梦新增（增加解析IP分支）：IP解析
                            sValue += "'"+octetIp(octetData) + "'"
                        else:
                            sValue += "'" + data[ipos: ipos + 2*octetLen] + "'"
                        ipos += 2*octetLen
                    elif it2 == DT_visible_string:  # 王梦新增
                        visibleLen = int(data[ipos:ipos + 2], 16)
                        if visibleLen>127:
                            ipos += 2
                            visibleLen = int(data[ipos:ipos + 2], 16)
                            ipos += 2
                        else:
                             ipos += 2
                        visibleaa1 = data[ipos: ipos + 2 * visibleLen]
                        visiblec1 = hextovisble(visibleaa1)#将十六进制转中英文
                        sValue +="'"+ visiblec1+"'"
                        ipos += 2 * visibleLen
                    elif it2 == DT_date:
                        sValue += "'" + hextodate(data[ipos:ipos + 10]) + "'"
                        ipos += 10
                    elif it2 == DT_unsigned:
                        sValue += str(int(data[ipos:ipos + 2], 16))
                        ipos += 2
                    elif it2 == DT_long_unsigned:
                        sValue += str(int(data[ipos:ipos + 4], 16))
                        ipos += 4
                    elif it2 == DT_date_time_s:
                        if soad[:4] == "8104":
                            sValue += "'" + hextospecialdatetime_s(data[ipos:ipos + 14]) + "'"
                        elif soad[:4] == "8105":
                            sValue += "'" + hextospecial8105datetime_s(data[ipos:ipos + 14]) + "'"
                        elif soad == 'F20F0200':
                            sValue += "'" + timespcialdisplay(hextodatetime_s(data[ipos:ipos + 14])) + "'"
                        else:
                            sValue += "'" + hextodatetime_s(data[ipos:ipos + 14]) + "'"
                        ipos += 14
                    elif it2 == DT_TI:
                        sValue += "'" + hextoTI(data[ipos:ipos + 6]) + "'"
                        ipos += 6
                    elif it2 == DT_MS:
                        sValue1,ipos= MsAnaly(ipos, data)
                        sValue+=sValue1

                    elif it2 == DT_double_long_unsigned:
                        if soad == 'F20F0200':
                            sValue += "'" + hextoversionpoint(data[ipos:ipos + 8])+ "'"
                        else:
                            sValue += hextonum(soad, data[ipos:ipos + 8])
                        ipos += 8
                    elif it2 == DT_NULL:
                        sValue += "'NULL'"
                    elif it2 == DT_double_long:
                        if soad == 'F20D0200':
                            #特殊需求，不用转为10进制，直接16进制显示
                            sValue += "'" +data[ipos:ipos + 8] + "'"
                        else:
                            sValue += hextodouble_long(soad, data[ipos:ipos + 8])
                        ipos += 8
                    elif it2 == DT_bool:  ##bool类型的数据解析
                        sValue += data[ipos+1:ipos + 2]
                        ipos += 2
                    elif it2 == DT_bit_string:  # 王梦新增#现在用例预期值没有要求转为2进制，若后期新增需求，可调整该流程。
                        bitLen = int(data[ipos:ipos + 2], 16)
                        ipos += 2
                        hexreallen = int(bitLen / 4)
                        if bitLen % 4 > 0:
                            hexreallen += 1
                        sValue += "'" + bitstrtohex(data[ipos: ipos + hexreallen])+"'"
                        ipos += hexreallen
                    elif it2 == DT_long64:
                        sValue += hextolong64(soad, data[ipos:ipos + 16])
                        ipos += 16
                    elif it2 == DT_OI:
                        sValue += "'" + data[ipos:ipos + 4] + "'"
                        ipos += 4
                    elif it2 == DT_integer:
                        sValue += hextoten(soad, data[ipos:ipos + 2])
                        ipos += 2
                    elif it2 == DT_COMDCB:
                        sValue += "'" +CHOICE_BR[str(int(data[ipos:ipos + 2],16)).zfill(2)]+ "'"+','
                        ipos += 2
                        sValue += "'" + CHOICE_CRC[data[ipos:ipos + 2]] + "'"+','
                        ipos += 2
                        sValue += "'" + CHOICE_DATA[data[ipos:ipos + 2]] + "'"+','
                        ipos += 2
                        sValue += "'" + CHOICE_STOP[data[ipos:ipos + 2]] + "'"+','
                        ipos += 2
                        sValue += "'" + CHOICE_CTRO[data[ipos:ipos + 2]] + "'"
                        ipos += 2
                    elif it2 == DT_time:
                        sValue += "'" + hextotime(data[ipos:ipos + 6]) + "'"
                        ipos += 6
                    elif it2 == DT_ROAD:
                        sValue += "['" + data[ipos:ipos + 8] + "'" + ',['
                        ipos += 8
                        Oadlen = int(data[ipos:ipos + 2], 16)
                        ipos += 2
                        for ilen in range(0, Oadlen, 1):
                            sValue += "'" + data[ipos:ipos + 8] + "'" + ','
                            ipos += 8
                        sValue = sValue[:-1] + ']]'
                    elif it2 == DT_CSD:
                        csdtype3 = int(data[ipos:ipos + 2], 16)
                        ipos += 2
                        if csdtype3 == 0:  # oad
                            sValue += "'" + data[ipos:ipos + 8] + "'"
                            ipos += 8
                        elif csdtype3 == 1:  # road
                            sValue += "'" + data[ipos:ipos + 8] + "',["
                            ipos += 8
                            road_len3 = int(data[ipos:ipos + 2], 16)
                            ipos += 2
                            for k1 in range(0, road_len3, 1):
                                sValue += "'" + data[ipos:ipos + 8] + "'"
                                ipos += 8
                                if k1 < road_len3 - 1: sValue += ','
                            sValue += ']'
                    elif it2 == DT_RCSD:
                        DT_CSDLen = int(data[ipos:ipos + 2], 16)
                        ipos += 2
                        sValue += "["
                        for CSDLen in range(0, DT_CSDLen, 1):
                            if data[ipos:ipos + 2] == "00":
                                ipos += 2
                                sValue += "'" + data[ipos:ipos + 8] + "'" + ','
                                ipos += 8
                            elif data[ipos:ipos + 2] == "01":
                                ipos += 2
                                sValue += "'" + data[ipos:ipos + 8] + "'" + ',['
                                ipos += 8
                                Oadlen = int(data[ipos:ipos + 2],16)
                                ipos += 2
                                for iOadlen in range(0, Oadlen, 1):
                                    sValue += "'" + data[ipos:ipos + 8] + "'" + ','
                                    ipos += 8
                                sValue = sValue[:-1] + '],'

                            else:
                                print('try3:RCSD', data[ipos:])
                        sValue += "]"
                    elif it2 == DT_RSD:
                        sValue4, ipos = Rsdtovalue(data, ipos)
                        sValue += sValue4
                    elif it2 == DT_float32:
                        sValue += hextofloat32(soad, data[ipos:ipos + 8])
                        ipos += 8
                    else:
                        print('try2', data[ipos:])
                        sValue += data[ipos:]

                    if j < ib - 1:
                        sValue += ','




                sValue += ']'
            elif it1 == DT_date_time_s:
                if soad[:4] == "8104":
                    sValue += "'" + hextospecialdatetime_s(data[ipos:ipos + 14]) + "'"
                elif soad[:4] == "8105":
                    sValue += "'" + hextospecial8105datetime_s(data[ipos:ipos + 14]) + "'"
                else:
                    sValue += "'" + hextodatetime_s(data[ipos:ipos + 14]) + "'"
                ipos += 14
            elif it1 == DT_date:
                sValue += "'" + hextodate(data[ipos:ipos + 10]) + "'"
                ipos += 10
            elif it1 == DT_long64:
                sValue += hextolong64(soad, data[ipos:ipos+16])
                ipos += 16
            #王梦新增
            elif it1 == DT_integer:
                sValue += hextoten(soad, data[ipos:ipos+2])
                ipos +=2
            # 王梦新增
            elif it1 == DT_OI:
                sValue += "'"+data[ipos:ipos+4]+"'"
                ipos += 4
            # 王梦新增
            elif it1 == DT_time:
                sValue += "'" + hextotime(data[ipos:ipos+6]) + "'"
                ipos += 6
            elif it1 == DT_bool:  ##bool类型的数据解析
                sValue += data[ipos+1:ipos + 2]
                ipos += 2
            elif it1 == DT_long:  # 王梦新增:调用春哥写好的hextolong
                # 如果是极值统计，为了换算，变回原本的OAD(电压、电流等关联对象的OAD)
                # 不改变全局变量，此处单独创建一个局部变量：extsoad
                if soad[:4] in extlist:
                    extsoad = data[6:14]
                else:
                    extsoad = soad
                sValue += hextolong(extsoad, data[ipos:ipos + 4])
                ipos += 4


            elif it1 == DT_long_unsigned:#王梦新增：同一个标识，不同换算时，或需完善！！！
                if (soad == "80000200")or(soad == "80000201"):#为了处理这个特殊的标识，同一个标识，不同换算
                    soad = "80000200"
                else:pass
                #如果是极值统计，为了换算，变回原本的OAD(电压、电流等关联对象的OAD)
                #不改变全局变量，此处单独创建一个局部变量：extsoad
                if soad[:4] in extlist:
                    extsoad = data[6:14]
                else:
                    extsoad=soad
                sValue += hextonum(extsoad, data[ipos:ipos + 4])
                ipos += 4
            elif it1 == DT_TSA:
                octetLen = int(data[ipos:ipos + 2], 16)
                ipos += 2
                sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
                ipos += 2 * octetLen
            elif it1 == DT_TI:
                sValue += "'" + hextoTI(data[ipos:ipos + 6]) + "'"
                ipos += 6
            elif it1 == DT_enum:
                sValue += str(int(data[ipos:ipos + 2], 16))
                ipos += 2
            elif it1 == DT_OAD:
                sValue += "'" + data[ipos:ipos + 8] + "'"
                ipos += 8
            elif it1 == DT_octet_string:
                octetLen = int(data[ipos:ipos + 2], 16)
                ipos += 2
                if (octetLen == 4) and (soad in Iplist):  # 王梦新增：IP解析
                    sValue += "'"+ octetIp(data[ipos: ipos + 2 * octetLen] ) + "'"
                elif soad=="80020300":
                    sValue += "'" + hextotimeregion(data[ipos: ipos + 2 * octetLen]) + "'"

                else:
                    sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
                ipos += 2 * octetLen
            elif it1 == DT_visible_string:  # 王梦新增
                visibleLen = int(data[ipos:ipos + 2], 16)
                if visibleLen > 127:
                    ipos += 2
                    visibleLen = int(data[ipos:ipos + 2], 16)
                    ipos += 2
                else:
                    ipos += 2
                visibleaa1 = data[ipos: ipos + 2 * visibleLen]
                visiblec1 = hextovisble(visibleaa1)  # 将十六进制转中英文
                #非法字符删掉 2021915
                sValue += "'"+visiblec1.strip('\x00')+"'"
                ipos += 2 * visibleLen
            elif it1 == DT_unsigned:
                if (soad == "45000200")or (soad == "45100200"):  # 王梦新增：如果是45000200，到此处要解析出重发次数和超时时间
                    aa = bin(int(data[ipos:ipos + 2], 16))
                    cc = aa[2:]
                    ff = cc[-2:]
                    hh = cc[:-2]
                    gg = int(ff, 2)
                    sValue += "'"+str(gg) + "_"
                    ii = int(hh, 2)
                    sValue += str(ii)+ "'"
                elif soad=="81010200":
                    binvalue0=str(bin(int(data[ipos:ipos + 2], 16))[2:].zfill(8))
                    sValue +="'" +bintoman(binvalue0)+ "'"

                else:
                    sValue += str(int(data[ipos:ipos + 2], 16))
                ipos += 2
            elif it1 == DT_double_long_unsigned:#王梦新增：同一个标识，不同换算时，或需完善！！！
                if soad=="80000200":
                    soad="80000201"
                else:pass
                # 如果是极值统计，为了换算，变回原本的OAD(电压、电流等关联对象的OAD)
                # 不改变全局变量，此处单独创建一个局部变量：extsoad
                if soad[:4] in extlist:
                    extsoad = data[6:14]
                else:
                    extsoad = soad
                sValue += hextonum(extsoad, data[ipos:ipos + 8])
                ipos += 8
            elif it1 == DT_NULL:
                sValue += "'NULL'"
            elif it1 == DT_double_long:
                if soad[:4] in extlist:
                    extsoad = data[6:14]
                else:
                    extsoad = soad
                sValue += hextodouble_long(extsoad, data[ipos:ipos + 8])
                ipos += 8
            elif it1 == DT_bit_string:
                bitLen = int(data[ipos:ipos + 2], 16)
                ipos += 2
                hexreallen = int(bitLen / 4)
                if bitLen % 4 > 0:
                    hexreallen += 1
                sValue +="'" + bitstrtohex(data[ipos: ipos + hexreallen])+"'"
                ipos +=  hexreallen
            elif it1 == DT_COMDCB:
                sValue += "'" + CHOICE_BR[str(int(data[ipos:ipos + 2], 16)).zfill(2)] + "'" + ','
                ipos += 2
                sValue += "'" + CHOICE_CRC[data[ipos:ipos + 2]] + "'" + ','
                ipos += 2
                sValue += "'" + CHOICE_DATA[data[ipos:ipos + 2]] + "'" + ','
                ipos += 2
                sValue += "'" + CHOICE_STOP[data[ipos:ipos + 2]] + "'" + ','
                ipos += 2
                sValue += "'" + CHOICE_CTRO[data[ipos:ipos + 2]] + "'"
                ipos += 2
            elif it1 == DT_MS:
                sValue1, ipos = MsAnaly(ipos, data)
                sValue += sValue1
            elif it1 == DT_CSD:
                csdtype3 = int(data[ipos:ipos + 2], 16)
                ipos += 2
                if csdtype3 == 0:  # oad
                    sValue += "'" + data[ipos:ipos + 8] + "'"
                    ipos += 8
                elif csdtype3 == 1:  # road
                    sValue += "'" + data[ipos:ipos + 8] + "',["
                    ipos += 8
                    road_len3 = int(data[ipos:ipos + 2], 16)
                    ipos += 2
                    for k1 in range(0, road_len3, 1):
                        sValue += "'" + data[ipos:ipos + 8] + "'"
                        ipos += 8
                        if k1 < road_len3 - 1: sValue += ','
                    sValue += ']'
            elif it1 == DT_float64:
                if soad[:4] in avelist:
                    avesoad = data[6:14]
                else:
                    avesoad = soad
                sValue += hextofloat64(avesoad, data[ipos:ipos + 16])
                ipos += 16
            elif it1 == DT_long64_unsigned:
                sValue += hextolong64(soad, data[ipos:ipos + 16])
                ipos += 16
            elif it1 == DT_float32:
                sValue += hextofloat32(soad, data[ipos:ipos + 8])
                ipos += 8
            else:
                print('try1:',it1, data[ipos:])
                sValue += data[ipos:]
            if i < ia - 1:
                if reuse == "|" and (it == DT_array):
                    sValue += '|'
                else:
                    sValue += ','


        sValue += ']'

    #王梦新增
    elif it == DT_long:#王梦新增:调用春哥写好的hextolong
        sValue +=hextolong(soad, data[ipos:ipos + 4])
        ipos += 4
    # 王梦新增
    elif it == DT_bool:##bool类型的数据解析
        sValue += data[ipos+1:ipos + 2]
        ipos += 2
    elif it == DT_long64:
        sValue += hextolong64(soad, data[ipos:ipos + 16])
        ipos += 16
    elif it == DT_date_time_s:
        if (soad == "40090200") or (soad == "40080200")or (soad == "400A0200")or (soad == "400B0200"):
            sValue += "'" + hextosdatetime_s(data[ipos:ipos + 14]) + "'"
        else:
            sValue += "'" + hextodatetime_s(data[ipos:ipos + 14]) + "'"

        ipos += 14
    elif it == DT_double_long:
        sValue += hextodouble_long(soad, data[ipos:ipos + 8])
        ipos += 8
    elif it == DT_TSA:
        octetLen = int(data[ipos:ipos + 2], 16)
        ipos += 2
        sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
        ipos += 2 * octetLen
    elif it == DT_enum:
        sValue += str(int(data[ipos:ipos + 2], 16))
        ipos += 2
    elif it == DT_TI:
        sValue += "'" + hextoTI(data[ipos:ipos + 6]) + "'"
        ipos += 6
    elif it == DT_OAD:
        sValue += "'" + data[ipos:ipos + 8] + "'"
        ipos += 8
    elif it == DT_octet_string:
        octetLen = int(data[ipos:ipos + 2], 16)
        ipos += 2
        sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
        if (len(sValue)==8) and (soad in Iplist) :#王梦新增：IP解析
            sValue="'"+octetIp(sValue)+ "'"
        elif soad == 'F1000200':  #部分不是gb2312,不能解析。为什么不是现在不是？以前就是的，新产品测的时候要关注一下20220709
            sValue = hextovisble(data[ipos: ipos + 2 * octetLen])
        else:
            sValue=sValue
        ipos += 2 * octetLen

    elif it == DT_visible_string:  # 王梦新增  it 是这个类型，说明数据本身只有这一个，所以不需要引号。
        visibleLen = int(data[ipos:ipos + 2], 16)
        ipos += 2
        visibleaa = data[ipos: ipos + 2 * visibleLen]
        visiblec = binascii.a2b_hex(visibleaa)
        visibled = str(visiblec).strip('b')
        sValue += visibled
        ipos += 2 * visibleLen
    elif it == DT_bit_string:  # 王梦新增#现在用例预期值没有要求转为2进制，若后期新增需求，可调整该流程。
        bitLen = int(data[ipos:ipos + 2], 16)
        ipos += 2
        hexreallen = int(bitLen/4)
        if bitLen % 4 > 0:
            hexreallen += 1
        sValue += "'" + bitstrtohex(data[ipos: ipos + hexreallen])+"'"
        ipos += hexreallen
    elif it == DT_unsigned:
        sValue = hextonum(soad, data[ipos:ipos + 2])
        ipos += 2
    elif it == DT_long_unsigned:
        sValue = hextonum(soad, data[ipos:ipos + 4])
        ipos += 4
    elif it == DT_NULL:
        sValue += "'NULL'"
    elif it == DT_MS:
        sValue1, ipos = MsAnaly(ipos, data)
        sValue += sValue1
    elif it == DT_double_long_unsigned:
        sValue += hextonum(soad, data[ipos:ipos + 8])
        ipos += 8
    elif it == DT_long64_unsigned:
        sValue += hextolong64(soad, data[ipos:ipos + 16])
        ipos += 16
    else:
        print("tryit:",it,data[ipos:])
        sValue += data[ipos:]
    # print(sValue)
    return sValue, ipos

# 0705000000000003->000000000003,14
def hextoTSA(data):
    ipos = 0
    sValue = ''
    ilen = int(data[ipos:ipos+2],16)
    ipos += 2
    # ipos += 2
    sValue = data[ipos: ipos + ilen*2]
    ipos += ilen*2
    return sValue, ipos

# 0A5507050000000000031C07E30C05080000010201031208DC120000120000010305000007AE05000000000500000000 ->
# ['ROW1','ROW2','ROW3','']
def GetRequestRecordValue(soad, data, sRcoad):
    tValue = []
    ipos = 0
    irow = int(data[ipos:ipos+2] , 16)
    ipos += 2
    for i in range(0, irow, 1):
        row = ''
        for j in range(0, len(sRcoad), 1):
            itype = int(data[ipos:ipos + 2], 16)
            ipos += 2
            if itype == DT_TSA:
                tt = hextoTSA(data[ipos:])
                row += "'" + tt[0] + "'"
                ipos += tt[1]
            elif itype == DT_date_time_s:
                row += "'" + hextodatetime_s(data[ipos:ipos+14]) + "'"
                ipos += 14
            elif itype == DT_array or itype == DT_structure:
                icoun = int(data[ipos:ipos+2], 16)
                ipos += 2
                ioad = sRcoad[j].find(':')
                toad = sRcoad[j][ioad+1:].split(',')
                row += '['
                # print("GetRequestRecordValue", str(len(toad)))
                redavalue='|'
                if len(toad) == icoun:
                    for k in range(0,icoun,1):
                        # 循环
                        #redavalue:标记是记录型的值，值与值之间用“|”隔开
                        tt = GetRequestNormalValue(toad[k],data[ipos:],redavalue)
                        # print(tt)
                        ipos += tt[1]
                        row += tt[0]
                        if k < icoun - 1:
                            row += '|'
                else:
                    for k in range(0,icoun,1):
                        # 循环
                        tt = GetRequestNormalValue(sRcoad[j],data[ipos:],redavalue)
                        # print(tt)
                        ipos += tt[1]
                        row += tt[0]
                        if k < icoun - 1:
                            row += '|'
                row += ']'
            elif itype == DT_long64:
                row += hextolong64(soad, data[ipos:ipos + 16])
                ipos += 16
            elif itype == DT_NULL:
                row += 'NULL'
            elif itype == DT_double_long:
                row += hextodouble_long(sRcoad[j], data[ipos:ipos + 8])
                ipos += 8
            elif itype == DT_double_long_unsigned:
                row += hextonum(sRcoad[j], data[ipos:ipos + 8])
                ipos += 8
            elif itype == DT_long:
                row += hextonum(sRcoad[j], data[ipos:ipos + 8])
                ipos += 8
            elif itype == DT_long_unsigned:
                row += hextonum(sRcoad[j], data[ipos:ipos + 4])
                ipos += 4
            elif itype == DT_OI:
                row += data[ipos:ipos + 4]
                ipos += 4
            elif itype == DT_bit_string:
                bitLen = int(data[ipos:ipos + 2], 16)
                ipos += 2
                hexreallen = int(bitLen / 4)
                if bitLen % 4 > 0:
                    hexreallen +=1
                row += "'" + bitstrtohex(data[ipos: ipos + hexreallen]) + "'"
                ipos += hexreallen
            elif itype == DT_enum:
                row += str(int(data[ipos:ipos + 2], 16))
                ipos += 2
            else:
                print('GetRequestRecordValue 增加类型', data[ipos:])
            if j < len(sRcoad)-1: row += ';'

        tValue += [row]
        if i < irow - 1: tValue += '!'

    return tValue, ipos


# 解析ProxyGetRequestList代理数据响应数据体020705000008022702012000020000FF0705000008022703012000020000210000->
# ->
def getProxyGetRequestListValue(data):
    sValue = ''
    ipos = 0
    ilen = int(hextoint(data[ipos:ipos+2]))
    ipos += 2
    # print("getProxyGetRequestListValue", ilen)
    for i in range(0, ilen, 1):
        tt = hextoTSA(data[ipos:])
        sValue += "['" + tt[0] + "',"
        ipos += tt[1]
        ida = int(hextoint(data[ipos:ipos+2]))
        ipos += 2
        for j in range(0, ida, 1):
            sOAD = data[ipos:ipos+8]
            sValue += "['" + sOAD + ':'
            ipos += 8
            if data[ipos:ipos+2] == "00":
                ipos += 2
                sValue += EMUN_DAR[data[ipos:ipos + 2]] + "']"
                ipos += 2
            elif data[ipos:ipos+2] == "01":
                ipos += 2
                lv = GetRequestNormalValue(sOAD, data[ipos:],'')
                sValue += lv[0] + "']"
                ipos += lv[1]
            else:
                print("getProxyGetRequestListValue 未知结果类型", data[ipos:], sValue)
            if j < ida - 1: sValue += ","
        sValue += "]"
        if i < ilen - 1: sValue += ","
    return sValue

# apdu解析（无链路分帧）->{'PIID':'','OAD':'','RCSD': ['OAD',,'ROAD:OAD1,OAD2,...'],'Value':['OAD1VALUE,OAD2VALUE,OAD2VALUE,,',,,,,,],
# 'Err':'','FollowReport':'','TimeTag':'','NextAPUD':''}
def analy_DATA_APDU(apdu):
    # dvalueNextAPUD = 0
    dvalue = {}
    ipos = 0
    apduType = apdu[ipos:ipos+2]#判断是什么类型：比如：86：SET-Response（设置响应）等
    ipos += 2
    if apduType == SECURITY_APDU_SECURITY_Response:
        bchoice = apdu[ipos:ipos+2]
        ipos += 2
        if bchoice == '00':
            ilen = int(apdu[ipos:ipos+2], 16)*2
            ipos += 2
            tapdu = apdu[ipos:ipos+ilen]
            # print('tapdu', tapdu)
            ipos1 = 0
            apduSX1 = tapdu[ipos1:ipos1 + 2]
            ipos1 += 2
            apduSX2 = tapdu[ipos1:ipos1 + 2]
            ipos1 += 2
            # print('tapdu[ipos:ipos + 2]', apduSX1, apduSX2)
            dvalue['PIID'] = int(tapdu[ipos1:ipos1 + 2], 16)
            dvalue['NextAPUD'] = ''
            dvalue['Err'] = 'NO'
            dvalue['SECURITY'] = '明文+mac'
            ipos1 += 2
            if apduSX1 == Server_APDU_GET_Response:
                if apduSX2 == GetRequestNormal:
                    dvalue['OAD'] = tapdu[ipos1:ipos1 + 8]
                    dvalue['RCSD'] = ['']
                    ipos1 += 8
                    Result = tapdu[ipos1:ipos1 + 2]
                    ipos1 += 2
                    if Result == '00':
                        dvalue['VALUE'] = [GetErrName(tapdu[ipos1:ipos1 + 2])]
                        dvalue['Err'] = GetErrName(tapdu[ipos1:ipos1 + 2])
                        ipos1 += 2
                    elif Result == '01':
                        value = []
                        value = GetRequestNormalValue(dvalue['OAD'], tapdu[ipos1:],'')
                        print('analy_DATA_APDU Server_APDU_GET_Response', value, dvalue['OAD'], tapdu[ipos1:])
                        dvalue['VALUE'] = [value[0]]
                        ipos1 += value[1]
                        # dvalue['Err'] = 'NO'
                    else:
                        dvalue['VALUE'] = [tapdu[ipos1:]]
                        dvalue['Err'] = 'Error'
            elif apduSX1 == Server_APDU_ACTION_Response:
                if apduSX2 == ActionRequestNormal:
                    dvalue['OAD'] = tapdu[ipos1:ipos1 + 8]
                    ipos1 += 8
                    dvalue['VALUE'] = [EMUN_DAR[tapdu[ipos1:ipos1 + 2]]]
                    ipos1 += 2
                    # print('analy_DATA_APDU Server_APDU_ACTION_Response ActionRequestNormalList 增加处理', apdu[ipos:])
                elif apduSX2 == ActionRequestNormalList:
                    print('analy_DATA_APDU Server_APDU_ACTION_Response ActionRequestNormalList 增加处理', apdu[ipos:])
                elif apduSX2 == ActionThenGetRequestNormalList:
                    print('analy_DATA_APDU Server_APDU_ACTION_Response ActionThenGetRequestNormalList 增加处理',
                          apdu[ipos1:])
            elif apduSX1 == Server_APDU_SET_Response:
                if apduSX2 == SetRequestNormal:
                    dvalue['OAD'] = tapdu[ipos1:ipos1 + 8]
                    ipos1 += 8
                    dvalue['VALUE'] = [EMUN_DAR[tapdu[ipos1:ipos1 + 2]]]
                    ipos1 += 2



            else:
                print('analy_DATA_APDU 明文+mac未处理', apdu[ipos1:])

        elif bchoice == '01':
            print('analy_DATA_APDU 增加密文数据解析', apdu[ipos:])
        else:
            print('analy_DATA_APDU 未知', apdu[ipos:])
        return dvalue
    apduSX = apdu[ipos:ipos+2]
    ipos += 2
    dvalue['PIID'] = int(apdu[ipos:ipos + 2], 16)
    dvalue['NextAPUD'] = ''
    dvalue['Err'] = 'NO'
    ipos += 2
    if apduType == Server_APDU_GET_Response:
        if apduSX == GetRequestNormal:
            dvalue['OAD'] = apdu[ipos:ipos+8]
            dvalue['RCSD'] =['']
            ipos += 8
            Result = apdu[ipos:ipos+2]
            ipos += 2
            if Result == '00':
                dvalue['VALUE'] = [EMUN_DAR[apdu[ipos:ipos+2]]]#把DAR直接输出到表格
                dvalue['Err'] = GetErrName(apdu[ipos:ipos+2])
                ipos += 2
            elif Result == '01':
                value = []
                value = GetRequestNormalValue(dvalue['OAD'], apdu[ipos:],'')
                print('analy_DATA_APDU Server_APDU_GET_Response', value)
                dvalue['VALUE'] = [value[0]]
                ipos += value[1]
                # dvalue['Err'] = 'NO'
            else:
                dvalue['VALUE'] = [apdu[ipos:]]
                dvalue['Err'] = 'Error'
        elif apduSX == GetRequestNormalList:
            dvalue['squencelen']=int(apdu[ipos:ipos + 2], 16)
            ipos +=2
            dvalueturn=[]
            for i in range(dvalue['squencelen']):
                dvalue['OAD'] = apdu[ipos:ipos + 8]
                dvalue['RCSD'] = ['']
                ipos += 8
                Result = apdu[ipos:ipos + 2]
                ipos += 2
                if Result == '00':
                    dvalue['VALUE'] =  [EMUN_DAR[apdu[ipos:ipos+2]]]#把DAR直接输出到表格
                    dvalueturn.append(dvalue['OAD']+":" + dvalue['VALUE']+";")
                    dvalue['Err'] = GetErrName(apdu[ipos:ipos + 2])
                    ipos += 2
                elif Result == '01':
                    value = []
                    value = GetRequestNormalValue(dvalue['OAD'], apdu[ipos:],'')
                    print('analy_DATA_APDU Server_APDU_GET_Response', value)
                    dvalue['VALUE'] =  value[0]#王梦新增：在数据内容前加上标识
                    dvalueturn.append(dvalue['OAD']+":" + dvalue['VALUE']+";")
                    ipos += value[1]
                    # dvalue['Err'] = 'NO'
                else:
                    dvalue['VALUE'] = [apdu[ipos:]]
                    dvalueturn.append(dvalue['OAD']+":" + dvalue['VALUE']+";")
                    dvalue['Err'] = 'Error'
                dvalue['VALUE']=dvalueturn
        elif apduSX == GetRequestRecord:

            dvalue['OAD'] = apdu[ipos:ipos+8]
            ipos += 8
            irscd = int(apdu[ipos:ipos+2],16)
            ipos += 2
            sRCSD = []

            for i in range(0, irscd, 1):
                CSD_TYPE = apdu[ipos:ipos+2]
                ipos += 2
                if CSD_TYPE == '00':
                    sRCSD += [apdu[ipos:ipos+8]]
                    ipos += 8
                elif CSD_TYPE == '01':
                    sROAD = apdu[ipos:ipos+8] + ':'
                    ipos += 8
                    ilen = int(apdu[ipos:ipos+2], 16)
                    ipos += 2
                    for j in range(0, ilen, 1):
                        sROAD += apdu[ipos:ipos+8]
                        ipos += 8
                        if j < ilen-1: sROAD += ','
                    sRCSD += [sROAD]
            dvalue['RCSD'] = sRCSD
            Result = apdu[ipos:ipos+2]
            ipos += 2
            if Result == '00':
                dvalue['VALUE'] = [GetErrName(apdu[ipos:ipos+2])]
                dvalue['Err'] = GetErrName(apdu[ipos:ipos+2])
                ipos += 2
            elif Result == '01':
                value = []
                value = GetRequestRecordValue(dvalue['OAD'], apdu[ipos:], dvalue['RCSD'])
                print('analy_DATA_APDU GetRequestRecord', value)
                dvalue['VALUE'] = value[0]
                ipos += value[1]
                dvalue['Err'] = 'NO'
            else:
                dvalue['VALUE'] = [apdu[ipos:]]
                dvalue['Err'] = 'Error'
        elif apduSX == GetRequestRecordList:
            #王梦新增：读取若干个记录型
            dvalue['squencelen'] = int(apdu[ipos:ipos + 2], 16)
            ipos += 2
            dvalueturn = []
            for i in range(dvalue['squencelen']):
                dvalue['OAD'] = apdu[ipos:ipos + 8]
                ipos += 8
                irscd = int(apdu[ipos:ipos + 2], 16)
                ipos += 2
                sRCSD = []

                for i in range(0, irscd, 1):
                    CSD_TYPE = apdu[ipos:ipos + 2]
                    ipos += 2
                    if CSD_TYPE == '00':
                        sRCSD += [apdu[ipos:ipos + 8]]
                        ipos += 8
                    elif CSD_TYPE == '01':
                        sROAD = apdu[ipos:ipos + 8] + ':'
                        ipos += 8
                        ilen = int(apdu[ipos:ipos + 2], 16)
                        ipos += 2
                        for j in range(0, ilen, 1):
                            sROAD += apdu[ipos:ipos + 8]
                            ipos += 8
                            if j < ilen - 1: sROAD += ','
                        sRCSD += [sROAD]
                dvalue['RCSD'] = sRCSD
                Result = apdu[ipos:ipos + 2]
                ipos += 2
                if Result == '00':
                    dvalue['VALUE'] = [GetErrName(apdu[ipos:ipos + 2])]
                    dvalueturn.append(dvalue['VALUE'])
                    dvalue['Err'] = GetErrName(apdu[ipos:ipos + 2])
                    ipos += 2
                elif Result == '01':
                    value = []
                    value = GetRequestRecordValue(dvalue['OAD'], apdu[ipos:], dvalue['RCSD'])
                    print('analy_DATA_APDU GetRequestRecord', value)
                    dvalue['VALUE'] = value[0]
                    dvalueturn.append(dvalue['VALUE'])
                    ipos += value[1]
                    dvalue['Err'] = 'NO'
                else:
                    dvalue['VALUE'] = [apdu[ipos:]]
                    dvalueturn.append(dvalue['VALUE'])
                    dvalue['Err'] = 'Error'
                dvalue['VALUE'] = dvalueturn
                #分帧响应一个数据块
        elif apduSX == GetRequestNext:
            #末帧标志
            dvalue['OVER'] = apdu[ipos:ipos+2]
            ipos += 2
            if dvalue['OVER'] == "00":
                dvalue['NextAPUD'] = 'False'
            else:
                dvalue['NextAPUD'] = ''
                # dvalueNextAPUD+=1
            #分帧序号
            dvalue['SEQ'] = apdu[ipos:ipos+4]
            ipos += 4
            #分帧选择：
            dvalue['Nexttype'] = apdu[ipos:ipos + 2]
            ipos += 2
            # dvalue['OAD'] = apdu[ipos:ipos+8]
            # ipos += 8
            if dvalue['Nexttype'] == '00':
                dvalue['VALUE'] = ['']
                dvalue['Err'] = GetErrName(apdu[ipos:ipos + 2])
                #分帧响应，错误信息
            elif dvalue['Nexttype'] == '01':
                # 以下为王梦新增：分帧响应CHOICE为01，待调试
                dvalue['squencelen'] = int(apdu[ipos:ipos + 2], 16)
                ipos += 2
                dvalueturn = []
                for i in range(dvalue['squencelen']):
                    dvalue['OAD'] = apdu[ipos:ipos + 8]
                    dvalue['RCSD'] = ['']
                    ipos += 8
                    Result = apdu[ipos:ipos + 2]
                    ipos += 2
                    if Result == '00':
                        dvalue['VALUE'] = [EMUN_DAR[apdu[ipos:ipos + 2]]]  # 把DAR直接输出到表格
                        dvalueturn.append(dvalue['VALUE'])
                        dvalue['Err'] = GetErrName(apdu[ipos:ipos + 2])
                        ipos += 2
                    elif Result == '01':
                        value = []
                        value = GetRequestNormalValue(dvalue['OAD'], apdu[ipos:],'')
                        print('analy_DATA_APDU Server_APDU_GET_Response', value)
                        dvalue['VALUE'] =  value[0]  # 王梦新增：在数据内容前加上标识
                        dvalueturn.append(dvalue['VALUE'])
                        ipos += value[1]
                        # dvalue['Err'] = 'NO'
                    else:
                        dvalue['VALUE'] = [apdu[ipos:]]
                        dvalueturn.append(dvalue['VALUE'])
                        dvalue['Err'] = 'Error'
                    dvalue['VALUE'] = dvalueturn
                    #以上为王梦新增：分帧响应CHOICE为01，待调试
                    # 分帧响应，记录型对象属性
            elif dvalue['Nexttype'] == '02':
                #函数少传了一个参数，王梦完善，待验证2020041018:45此处：暂时不用关注，调试分帧时再关注，报错是因为有分帧。
                dvalue['squencelen'] = int(apdu[ipos:ipos + 2], 16)
                ipos += 2
                dvalueturn = []
                for i in range(dvalue['squencelen']):
                    dvalue['OAD'] = apdu[ipos:ipos + 8]
                    ipos += 8
                    irscd = int(apdu[ipos:ipos + 2], 16)
                    ipos += 2
                    sRCSD = []

                    for i in range(0, irscd, 1):
                        CSD_TYPE = apdu[ipos:ipos + 2]
                        ipos += 2
                        if CSD_TYPE == '00':
                            sRCSD += [apdu[ipos:ipos + 8]]
                            ipos += 8
                        elif CSD_TYPE == '01':
                            sROAD = apdu[ipos:ipos + 8] + ':'
                            ipos += 8
                            ilen = int(apdu[ipos:ipos + 2], 16)
                            ipos += 2
                            for j in range(0, ilen, 1):
                                sROAD += apdu[ipos:ipos + 8]
                                ipos += 8
                                if j < ilen - 1: sROAD += ','
                            sRCSD += [sROAD]
                    dvalue['RCSD'] = sRCSD
                    Result = apdu[ipos:ipos + 2]
                    ipos += 2
                    if Result == '00':
                        dvalue['VALUE'] = [GetErrName(apdu[ipos:ipos + 2])]
                        dvalueturn.append(dvalue['VALUE'])
                        dvalue['Err'] = GetErrName(apdu[ipos:ipos + 2])
                        ipos += 2
                    elif Result == '01':
                        value = []
                        value = GetRequestRecordValue(dvalue['OAD'], apdu[ipos:], dvalue['RCSD'])
                        print('analy_DATA_APDU GetRequestRecord', value)
                        dvalue['VALUE'] = value[0]
                        dvalueturn.append(dvalue['VALUE'])
                        ipos += value[1]
                        dvalue['Err'] = 'NO'
                    else:
                        dvalue['VALUE'] = [apdu[ipos:]]
                        dvalueturn.append(dvalue['VALUE'])
                        dvalue['Err'] = 'Error'
                    dvalue['VALUE'] = dvalueturn

            # 生成下一帧APDU 050500000000  此处要生成下一帧
        elif apduSX == GetRequestMD5:
            pass
    elif apduType == Server_APDU_SET_Response:
        if apduSX == SetRequestNormal:
            dvalue['OAD'] = apdu[ipos:ipos+8]
            ipos += 8
            dvalue['VALUE'] = [EMUN_DAR[apdu[ipos:ipos+2]]]
            ipos += 2
            # print('analy_DATA_APDU Server_APDU_SET_Response Server_APDU_SET_Response 增加处理', apdu[ipos:])
        elif apduSX == SetRequestNormalList:
            ipos += 2
            print('analy_DATA_APDU Server_APDU_SET_Response SetRequestNormalList 增加处理', apdu[ipos:])
        elif apduSX == SetThenGetRequestNormalList:
            ipos += 2
            print('analy_DATA_APDU Server_APDU_SET_Response SetThenGetRequestNormalList 增加处理', apdu[ipos:])
    elif apduType == Server_APDU_ACTION_Response:
        if apduSX == ActionRequestNormal:
            dvalue['OAD'] = apdu[ipos:ipos+8]
            ipos += 8
            dvalue['VALUE'] = [EMUN_DAR[apdu[ipos:ipos+2]]]
            ipos += 2
            # print('analy_DATA_APDU Server_APDU_ACTION_Response ActionRequestNormalList 增加处理', apdu[ipos:])
        elif apduSX == ActionRequestNormalList:
            print('analy_DATA_APDU Server_APDU_ACTION_Response ActionRequestNormalList 增加处理', apdu[ipos:])
        elif apduSX == ActionThenGetRequestNormalList:
            print('analy_DATA_APDU Server_APDU_ACTION_Response ActionThenGetRequestNormalList 增加处理', apdu[ipos:])
    elif apduType == Server_APDU_REPORT_Notification:
        if apduSX == ReportNotificationList:
            dvalue['squencelen'] = int(apdu[ipos:ipos + 2], 16)
            ipos += 2
            dvalueturn = []
            for i in range(dvalue['squencelen']):
                dvalue['OAD'] = apdu[ipos:ipos + 8]
                dvalue['RCSD'] = ['']
                ipos += 8
                Result = apdu[ipos:ipos + 2]
                ipos += 2
                if Result == '00':
                    dvalue['VALUE'] = [EMUN_DAR[apdu[ipos:ipos + 2]]]  # 把DAR直接输出到表格
                    dvalueturn.append(dvalue['VALUE'])
                    dvalue['Err'] = GetErrName(apdu[ipos:ipos + 2])
                    ipos += 2
                elif Result == '01':
                    value = []
                    value = GetRequestNormalValue(dvalue['OAD'], apdu[ipos:], '')
                    print('analy_DATA_APDU ReportNotificationList', value)
                    dvalue['VALUE'] = value[0]  # 王梦新增：在数据内容前加上标识
                    dvalueturn.append(dvalue['VALUE'])
                    ipos += value[1]
                    # dvalue['Err'] = 'NO'
                else:
                    dvalue['VALUE'] = [apdu[ipos:]]
                    dvalueturn.append(dvalue['VALUE'])
                    dvalue['Err'] = 'Error'
                dvalue['VALUE'] = dvalueturn
        elif apduSX == ReportNotificationRecordList:
            dvalue['squencelen'] = int(apdu[ipos:ipos + 2], 16)
            ipos += 2
            dvalueturn = []
            for i in range(dvalue['squencelen']):
                dvalue['OAD'] = apdu[ipos:ipos + 8]
                ipos += 8
                irscd = int(apdu[ipos:ipos + 2], 16)
                ipos += 2
                sRCSD = []

                for i in range(0, irscd, 1):
                    CSD_TYPE = apdu[ipos:ipos + 2]
                    ipos += 2
                    if CSD_TYPE == '00':
                        sRCSD += [apdu[ipos:ipos + 8]]
                        ipos += 8
                    elif CSD_TYPE == '01':
                        sROAD = apdu[ipos:ipos + 8] + ':'
                        ipos += 8
                        ilen = int(apdu[ipos:ipos + 2], 16)
                        ipos += 2
                        for j in range(0, ilen, 1):
                            sROAD += apdu[ipos:ipos + 8]
                            ipos += 8
                            if j < ilen - 1: sROAD += ','
                        sRCSD += [sROAD]
                dvalue['RCSD'] = sRCSD
                Result = apdu[ipos:ipos + 2]
                ipos += 2
                if Result == '00':
                    dvalue['VALUE'] = [GetErrName(apdu[ipos:ipos + 2])]
                    dvalueturn.append(dvalue['VALUE'])
                    dvalue['Err'] = GetErrName(apdu[ipos:ipos + 2])
                    ipos += 2
                elif Result == '01':
                    value = []
                    value = GetRequestRecordValue(dvalue['OAD'], apdu[ipos:], dvalue['RCSD'])
                    print('analy_DATA_APDU ReportNotificationRecordList', value)
                    dvalue['VALUE'] = value[0]
                    dvalueturn.append(dvalue['VALUE'])
                    ipos += value[1]
                    dvalue['Err'] = 'NO'
                else:
                    dvalue['VALUE'] = [apdu[ipos:]]
                    dvalueturn.append(dvalue['VALUE'])
                    dvalue['Err'] = 'Error'
                dvalue['VALUE'] = dvalueturn
        elif apduSX == ReportNotificationTransData:
            print('analy_DATA_APDU Server_APDU_REPORT_Notification ReportNotificationTransData 增加处理', apdu[ipos:])
    elif apduType == Server_APDU_PROXY_Response:
        if apduSX == ProxyGetRequestList:
            if len(apdu[ipos:]) < 16:
                dvalue['VALUE'] = '无数据'
                dvalue['Err'] = '未知错误 无数据'
            dvalue['OAD'] = ''
            dvalue['RCSD'] =['']
            # itemlen = hextoint(apdu[ipos:ipos+2])
            # ipos += 2
            value = getProxyGetRequestListValue(apdu[ipos:])
            dvalue['VALUE'] = [value]
            dvalue['Err'] = ''
            # print('analy_DATA_APDU Server_APDU_PROXY_Response ProxyGetRequestList 增加处理', apdu[ipos:])
        elif apduSX == ProxyGetRequestRecord:
            print('analy_DATA_APDU Server_APDU_PROXY_Response ProxyGetRequestRecord 增加处理', apdu[ipos:])
        elif apduSX == ProxySetRequestList:
            print('analy_DATA_APDU Server_APDU_PROXY_Response ProxySetRequestList 增加处理', apdu[ipos:])
        elif apduSX == ProxySetThenGetRequestList:
            print('analy_DATA_APDU Server_APDU_PROXY_Response ProxySetThenGetRequestList 增加处理', apdu[ipos:])
        elif apduSX == ProxyActionRequestList:
            print('analy_DATA_APDU Server_APDU_PROXY_Response ProxyActionRequestList 增加处理', apdu[ipos:])
        elif apduSX == ProxyActionThenGetRequestList:
            print('analy_DATA_APDU Server_APDU_PROXY_Response ProxyActionThenGetRequestList 增加处理', apdu[ipos:])
        elif apduSX == ProxyTransCommandRequest:
            dvalue['OAD'] = apdu[ipos:ipos+8]
            dvalue['RCSD'] = ['']
            ipos += 8
            #目前先取01  00  来判断是否代理到数据。01:正常响应；00为正常响应，没代理到值。
            Result = apdu[ipos:ipos + 2]
            ipos += 2
            if Result == '01':
                datalen = (int((apdu[ipos:ipos + 2]),16))*2
                print('打印收到的698抄表报文：',apdu[ipos:ipos + datalen])
                ipos += 2
                if apdu[ipos:ipos + datalen] == '685F00C30576010000000000A0819000468502310200100200010105060001EA710600006B3706000072740600008D2B0600007F9B0020020001010506000151600600004E3D06000065BB0600005FB70600003DAF0000010004123456784A5D16':
                    dvalue['VALUE'] = '代理成功'
                else:
                    try:
                        dvalue['VALUE'] = get645data(apdu[ipos:ipos + datalen])
                        if dvalue['VALUE'].find('Cannot Parse The data:') >= 0:
                            dvalue['VALUE'] = '代理失败'
                    except:dvalue['VALUE'] = '代理失败'
            elif Result == '00':
                dvalue['VALUE'] = '代理失败'
            dvalue['Err'] = ''
    elif apduType == Server_APDU_ERROR_Response:
        print('analy_DATA_APDU Server_APDU_ERROR_Response 增加处理', apdu[ipos:])

    return  dvalue

# link分帧处理apdu解析->{'PIID':'','seq_no':'','seq_type':'' ,'buff':'',,,,,,],
def analy_DATA_APDU_SEQ(apdu):
    pass

# 上报帧APDU解析处理
def analy_DATA_APDU_Report(apdu):
    return ''
    pass

# [2018-12-03-10:10:51:859]682100430503000000000000A4B705010123010A000107E30B1A0F15340001F454E216
# ->682100430503000000000000A4B705010123010A000107E30B1A0F15340001F454E216
def splitframetime(sdata):
    sdata1 = sdata.replace(' ', '')
    pos = sdata1.find(']')
    stime = sdata1[:pos]
    stime = stime.replace('-', '')
    stime = stime.replace(':', '')
    stime = stime.replace('[', '')
    stime = stime.replace(']', '')
    rdata = sdata1[pos+1:]
    return stime, rdata

def frametimeget(sdata):
    sdata1 = sdata.replace(' ', '')
    pos = sdata1.find(']')
    stime = sdata1[:pos+1]
    rdata = sdata1[pos+1:]
    return stime, rdata


# 数据应用
# 分析帧->输出分析数据、响应帧[bool,time,CTRL_LINK,xybuff,questtype(登录，心跳),laddr]
# 数据响应[bool,time,CTRL_DATA,{datalist},APDU,laddr,nextapdubuff]
def Receive(buff):
    #测试发送分帧次数：
    # cesfenzhentimes=0
    ll = [False]
    Nextframe = ''
    if len(buff) < MIN_LEN_OOP_FRAME:
        return Nextframe,ll
    stime, sdata = splitframetime(buff)
    ll[0] = True
    ll += [stime]
    dfme = []
    dfme = GetFrame(sdata)
    #分帧标志位
    Nextsend=0
    # print('Receive', dfme)
    if dfme[0]:
       # if dfme[1]['CTRL_BS'][''] ==
        if dfme[1]['CTRL_BS']['C_AFN'][2] == CTRL_LINK:
            #10:服务器发起的上报
            if dfme[1]['CTRL_BS']['C_DIR'][2] == 1 and dfme[1]['CTRL_BS']['C_PRM'][2] == 0:
                ll += [CTRL_LINK]
                frm = {}
                frm['CTRL'] = '01'
                # print(dfme[1]['TSA_TYPE'])
                frm['TSA_TYPE'] = dfme[1]['TSA_TYPE']
                frm['TSA_VS'] = dfme[1]['TSA_VS']
                frm['TSA_AD'] = dfme[1]['TSA_AD']
                frm['CA'] = dfme[1]['CA']
                frm['SEG_WORD'] = dfme[1]['SEG_WORD']
                frm['APDU'] ,frm['HEARTIME']= make_LINK_APDU_Response(dfme[1]['APDU'], ll[1])
                ll += [MakeFrame(frm)]
                # ll += [dfme[1]['TSA_VS']]
                # LinkRequestType_LOGIN LinkRequestType_HEART LinkRequestType_EXIT
                ll += [dfme[1]['APDU'][4:6]]
                ll += [dfme[1]['TSA_AD']]
                #王梦新增，将心跳时间传回去
                ll += [frm['HEARTIME']]

            else:
                ll += [dfme[1]['APDU']]
                print('Err DIR_PRM')
                print(str(dfme[1]['CTRL_BS']['C_DIR'][2]) + str(dfme[1]['CTRL_BS']['C_PRM'][2]))
# [True, '20181203101051859', 1, '683000010503000000000000E9EE813F0107E30C0201082F02000007E20C03000A0A33BFE307E30C0A01102C3A908FD0B816', 0, '000000000003']
        #王梦新增上报流程
        elif dfme[1]['CTRL_BS']['C_AFN'][2] == CTRL_DATA or  dfme[1]['CTRL_BS']['C_AFN'][2] == CTRL_REPORT:
            if dfme[1]['CTRL_BS']['C_DIR'][2] == 1 and dfme[1]['CTRL_BS']['C_PRM'][2] == 1:
                if dfme[1]['CTRL_BS']['C_SEG'][2] == 0:
                    ll += [CTRL_DATA]
                    # ll += [dfme['APDU']]
                    dapdu = analy_DATA_APDU(dfme[1]['APDU'])
                    ll += [dapdu]
                    ll += [dfme[1]['APDU']]
                    ll += [dfme[1]['TSA_AD']]
                    print('NextAPUD:' + dapdu['NextAPUD'])
                    if len(dapdu['NextAPUD']) > 0:

                        # print('生成下一帧')
                        #拿到帧的对应位置数据，利用组帧函数组帧：MakeFrame(frame)。
                        Nextframe={}
                        Nextframe['CTRL']= '4'+ str(dfme[1]['CTRL']) [1:]
                        Nextframe['TSA_TYPE']=dfme[1]['TSA_TYPE']
                        Nextframe['TSA_VS']=dfme[1]['TSA_VS']
                        Nextframe['TSA_AD']=dfme[1]['TSA_AD']
                        Nextframe['CA']=dfme[1]['CA']
                        Nextframe['SEG_WORD']=''
                        #组成APDU:0505:读取分帧响应的下一帧；PIIDPIID要处理一下：10进制整型-》16进制,帧序号，时间标签
                        Nextframe['APDU']='0505'+str(hex(dapdu['PIID']))[2:].zfill(2)+str(dapdu['SEQ'])+'00'
                        # print(Nextframe,'组帧前')
                        #下发报文
                        Nextframe = MakeFrame(Nextframe)
                        Nextframe = Nextframe.upper()
                        # print(Nextframe,'组帧后')
                        # 生成下一帧
                        Nextsend =1

                    else:
                        ll += dapdu['NextAPUD']
                elif dfme[1]['CTRL_BS']['C_SEG'][2] == 1:
                    ll += [CTRL_DATA]
                    ll += analy_DATA_APDU_SEQ(dfme[1]['APDU'])
                    ll += [dfme[1]['APDU']]
                    ll += [dfme[1]['TSA_AD']]
                    # 后续帧
                else:
                    ll += [dfme[1]['APDU']]
                    print('需要增加[服务器对客户机请求的响应]APDU解析解析处理')
            elif dfme[1]['CTRL_BS']['C_DIR'][2] == 1 and dfme[1]['CTRL_BS']['C_PRM'][2] == 0:
                if dfme[1]['CTRL_BS']['C_SEG'][2] == 0:
                    ll += [CTRL_DATA]
                    # ll += [dfme['APDU']]
                    dapdu = analy_DATA_APDU(dfme[1]['APDU'])
                    ll += [dapdu]
                    ll += [dfme[1]['APDU']]
                    ll += [dfme[1]['TSA_AD']]
                    print('NextAPUD:' + dapdu['NextAPUD'])
                else:
                    print('增加其它上报的处理')
 # 2019-12-2313:42:32接收(上报通知)：68C4008305030000000000004023880222013115020006002022020000201E020000202002000020240200003300020000330A0205010106000000091C07E30C170D2A1D1C07E30C170D2A1D51F20502020104020251450000001101020251451000001101020251F20002011100020251F20C0201110001081400000000000000001400000000000000001400000000000000001400000000000000001400000000000000001400000000000000001400000000000000001400000000000000000000684E16
 # 2019-12-2313:42:32发送(上报响应)：681800030503000000000000332B080222013115020000B9EC16
 #                ll += [CTRL_DATA]
 #                ll += analy_DATA_APDU_Report(dfme[1]['APDU'])

            elif dfme[1]['CTRL_BS']['C_DIR'][2] == 0 and dfme[1]['CTRL_BS']['C_PRM'][2] == 1:
                ll += [dfme[1]['APDU']]
                print('需要增加[客户机发起的请求]APDU解析处理')
            elif dfme[1]['CTRL_BS']['C_DIR'][2] == 0 and dfme[1]['CTRL_BS']['C_PRM'][2] == 0:
                ll += [dfme[1]['APDU']]
                print('需要增加[客户机对服务器上报的响应]APDU解析处理')
            else:
                ll += [dfme[1]['APDU']]
                print('需要增加APDU解析处理')
    else:
        ll[0] = False
    print('Receive:', ll)
    #如果有分帧，就将组好的分帧报文以参数的形式传过去，继续下发报文。没有分帧就返回空。
    if Nextsend ==1:
        Nextframe=Nextframe
        # cesfenzhentimes+=1
        # print('cesfenzhentimes:',cesfenzhentimes)

    else:
        Nextframe=''


    return Nextframe,ll


# 和Excel表中操作名称一致
dOPName={'读取一个对象属性':'0501', '读取若干个对象属性':'0502', '读取一个记录型对象属性':'0503',
         '读取若干个记录型对象属性': '0504', '读取分帧传输的下一帧': '0505', '读取一个对象属性的 MD5 值': '0506',
         '设置一个对象属性': '0601', '设置若干个对象属性': '0602', '设置后读取若干个对象属性': '0603',
         '操作一个对象方法': '0701', '操作若干个对象方法': '0702',
         '操作若干个对象方法后读取若干个对象属性': '0703', '代理读取若干个服务器的若干个对象属性': '0901',
         '代理读取一个服务器的一个记录型对象属性': '0902', '代理设置若干个服务器的若干个对象属性': '0903',
         '代理设置后读取若干个服务器的若干个对象属性': '0904', '代理操作若干个服务器的若干个对象方法': '0905',
         '代理操作后读取若干个服务器的若干个对象方法和属性': '0906', '代理透明转发命令': '0907',
         '通知上报若干个对象属性': '8801', '通知上报若干个记录型对象属性': '8802', '通知上报透明数据': '8803',
         '预连接': '01', '建立应用连接': '02', '断开应用连接': '03'}


# 操作描述符->data
def getbuffbyOPName(name):
    bdata = ''
    if name in dOPName:
        bdata = dOPName[name]  #'设置一个对象属性': '0601',

    else:
        print('getbuffbyrequest Err')
    return bdata

# 和Excel表中逻辑设备地址名称一致
dVaddr = {'终端': 0, '交采': 1,'回路巡检':2,'终端通道2': 0,'终端通道3': 0,'终端通道4': 0,'终端通道5': 0,'终端通道6': 0,'终端通道4交采': 1}
# 逻辑设备地址描述->data
def getintbyvaddrname(vaddr):
    bdata = ''
    if vaddr in dVaddr:
        bdata = dVaddr[vaddr]
    else:
        print('getintbyvaddr Err')
    return bdata

# 和Excel表中服务器地址名称一致
dCA = {'单地址': 0, '组地址': 2, '通配地址': 1, '广播地址': 3}
# 服务器地址描述->data
def getbitbyCA(ca):
    bdata = ''
    if ca in dCA:
        bdata = dCA[ca]
    else:
        print('getbitbyCA Err')
    return bdata


#bpriority 优先级 True高 False低
def getPIIDBuff(bpriority, iPIID):
    bdata = ''
    ipiid = 0
    if bpriority:
        ipiid = 0x80 + iPIID % 64
    else:
        ipiid = iPIID % 64
    bdata = hex(ipiid).replace('0x', '').zfill(2)
    return bdata


# 带[]字符串转换成list '[c,d,e]'->[c,d,e]
def strtolist(slist):
    lrtn = eval("%s" % slist)
    return lrtn


# defing RSD
OOP_RSD_CHOICE_VALUE = {'不选择': '00', '选择方法1': '01', '选择方法2': '02', '选择方法3': '03', '选择方法4': '04',
                 '选择方法5': '05', '选择方法6': '06', '选择方法7': '07', '选择方法8': '08', '选择方法9': '09',
                 '选择方法10': '0A'}

RSD_NULL = "不选择"
RSD_Selector1 = "选择方法1"
RSD_Selector2 = "选择方法2"
RSD_Selector3 = "选择方法3"
RSD_Selector4 = "选择方法4"
RSD_Selector5 = "选择方法5"
RSD_Selector6 = "选择方法6"
RSD_Selector7 = "选择方法7"
RSD_Selector8 = "选择方法8"
RSD_Selector9 = "选择方法9"
RSD_Selector10 = "选择方法10"

# 描述CSD Selector数据结构,给传入的参数组帧使用
OOP_RSD_SelectornDY = {RSD_Selector1: [DT_OAD, DT_se1],
                     RSD_Selector2: [DT_OAD, DT_se2, DT_se2, DT_se2],
                     RSD_Selector3: [DT_array, [DT_OAD, DT_se2, DT_se2, DT_se2]],
                     RSD_Selector4: [DT_date_time_s, DT_MS],
                     RSD_Selector5: [DT_date_time_s, DT_MS],
                     RSD_Selector6: [DT_date_time_s, DT_date_time_s, DT_TI, DT_MS],
                     RSD_Selector7: [DT_date_time_s, DT_date_time_s, DT_TI, DT_MS],
                     RSD_Selector8: [DT_date_time_s, DT_date_time_s, DT_TI, DT_MS],
                     RSD_Selector9: [DT_unsigned],
                     RSD_Selector10: [DT_unsigned, DT_MS]}

# defing CSD
OOP_CSD = {'0': 'OAD', '1': 'OOP_ROAD'}


# defind ROAD
OOP_ROAD = [DT_array, [DT_OAD, [DT_array,[DT_OAD]]]]


OOP_RCSD = [DT_array, [DT_array, [DT_OAD, [DT_array,[DT_OAD]]]]]


## 定义特殊属性结构字(设置和方法操作时，属性与方法标识一样时，需做区分：) 增加完善
SpecialOOPDY=['21000300', '21010300', '21020300', '21030300', '21040300',  #区间统计
              '21100300', '21110300', '21120300', '21130300', '21140300',  #累加平均
              '21200300', '21210300', '21220300', '21230300', '21240300',  #极值统计
              '24010400', '24010300', '24020400', '24020300',  #脉冲1、2
              '24030400','24030300', '24040400','24040300',  #脉冲3、4
              '24050400','24050300', '24060400','24060300',  #脉冲5、6
              '24070400','24070300', '24080400','24080300',  #脉冲7、8
              '30000500',#电能表失压事件
              '30010500',#电能表欠压事件
              '30020500',#电能表过压事件
              '30030500',#电能表断相事件
              '30040500',#电能表失流事件
              '30050500',#电能表过流事件
              '30060500',#电能表断流事件
              '30070500',#电能表功率反向事件
              '30080500',#电能表过载事件
              '300B0500',#电能表过载事件
              '43000700',#服务授权开启
              '81030300',  #时段功控
              '81040300',  # 时段功控
              '81050300',  #营业报停控
              '81070300',  #购电控
              '81080300',  #月电控
              '50020300',  #分钟冻结
              '50030300',  #小时冻结
              '50040300',  #日冻结
              '50050300',  #结算日冻结
              '50060300',  # 月冻结
              '50070300',  # 年冻结
              'F2090B00',  # 台区识别启停标志

              ]
# 定义接口函数相关标识
Excelchangelist=["60127F00","60120300","60008000","60147F00","60167F00","60187F00","601C7F00"]
#定义参数筛选相关标识
paramselectlist=["60000200",'60120200','60140200','60160200','60180200','601C0200']
#定义终端数据筛选相关标识
rtudataselectlist=['50030200','50030200','50040200','50050200','50060200']








# 定义属性结构字 增加完善
OOPSXDY = {
           '20210200': [DT_date_time_s],
           '40000200': [DT_date_time_s], '40000300': [DT_enum],
           '40000400': [DT_structure,[DT_unsigned, DT_unsigned, DT_unsigned, DT_unsigned, DT_unsigned]],
           '40000500':[DT_long_unsigned, DT_long_unsigned],  #广播校时
           '40000600':[DT_double_long_unsigned, DT_double_long_unsigned],  #广播校时
           '40007F00':[DT_date_time_s ],  #广播校时

           #以下王梦新增：
           '40010200':[DT_octet_string],  #通讯地址
           '40020200':[DT_octet_string],  #表号
           '40030200':[DT_octet_string],  #客户编号


           '40040200':[DT_structure,[[DT_structure,[DT_enum,DT_long_unsigned,DT_float32]],[DT_structure,[DT_enum,DT_long_unsigned,DT_float32]],DT_double_long]],  #设备地理坐标
           '40050200': [DT_array,[DT_octet_string]],  # 组地址
           '40060200': [DT_structure, [DT_enum, DT_enum]],  # 时钟源
           '40067F00': [DT_NULL],  # 启用时钟源
           '40068000': [DT_NULL],  # 禁用时钟源

           '40070200': [DT_structure, [DT_unsigned, DT_long_unsigned,DT_long_unsigned,DT_long_unsigned,DT_unsigned,DT_unsigned,DT_unsigned]
                        ],  # LCD参数
           #上电全显时间
          '40070201': [DT_unsigned],
           #背光点亮时长
          '40070202': [DT_unsigned],
            #显示查看背光点亮时长
          '40070203': [DT_unsigned],
            #无电按键屏幕驻留最大时长
          '40070204': [DT_unsigned],
          # 显示电能小数位数
          '40070205': [DT_unsigned],
          # 显示功率（最大需量）小数位数
          '40070206': [DT_unsigned],
          # 液晶①②字样意义
          '40070207': [DT_unsigned],



    '40240200': [DT_enum],  # 剔除
           '40250300': [DT_structure, [DT_unsigned,DT_unsigned] ],  # 采集器升级控制参数
           '40300200': [DT_structure, [DT_long_unsigned,DT_long_unsigned,DT_long_unsigned,DT_long_unsigned] ],  # 电压合格率参数
           '42040200': [DT_structure, [DT_time,DT_bool]],  # 终端对电能表广播校时参数
           '42040300': [DT_structure, [DT_integer ,DT_time, DT_bool]],  # 单地址广播校时参数
           '43000500': [DT_array, [DT_OI]],  # 电气设备子设备列表
           '43000600': [DT_array, [DT_visible_string]],  # 电气设备支持规约列表
           #属性
           '430007000': [DT_bool],  # 电气设备允许跟随上报
           #方法
           '430007001': [DT_structure,[DT_unsigned,DT_unsigned]],  # 电气设备允许跟随上报

           '43000800': [DT_bool],  # 电气设备允许主动上报
           '43000900': [DT_bool],  # 电气设备允许与主站通话
           '43000A00': [DT_array, [DT_OAD]],  # 电气设备上报通道
          # 应用语境信息
          '44000300': [DT_structure,[DT_long_unsigned,DT_long_unsigned,DT_long_unsigned,DT_long_unsigned,DT_bit_string,DT_bit_string,DT_double_long_unsigned]],
           #协议版本号
          '44000301': [DT_long_unsigned],
          #认证密码
          '44010200': [DT_visible_string],




           '45000100':[DT_octet_string],  #无线公网通讯模块1：逻辑名

           '45000200': [DT_structure,[DT_enum,DT_enum,DT_enum,DT_enum,[DT_array,[DT_long_unsigned]],
                                      DT_visible_string, DT_visible_string, DT_visible_string,DT_octet_string,
                                      DT_long_unsigned,DT_unsigned,DT_long_unsigned]
                        ],  # 无线公网通讯模块1：通讯配置
           '45000300': [DT_array, [DT_structure, [DT_octet_string, DT_long_unsigned]]],
           # # 无线公网通讯模块1：主站通讯参数表
           '45000400':[DT_structure,[DT_visible_string,[DT_array,[DT_visible_string]],[DT_array,[DT_visible_string]]]],
           #无线公网通讯模块1：短信通信参数
           '45000500': [DT_structure, [DT_visible_string, DT_visible_string, DT_visible_string, DT_visible_string,
                                       DT_visible_string, DT_visible_string]],  # 无线公网通讯模块1：版本信息
           '45000600': [DT_array, [DT_visible_string]],  #  无线公网通讯模块1：支持规约列表
           '45000700': [DT_visible_string],  # #无线公网通讯模块1：SIM卡ICCID
           '45000800': [DT_visible_string],  # #无线公网通讯模块1：IMSI
           '45000900': [DT_long],  # #无线公网通讯模块1：IMSI
           '45000A00': [DT_visible_string],  # #无线公网通讯模块1：SIM卡号码
           '45000B00': [DT_octet_string],  # #无线公网通讯模块1：终端IP
           '45000C00': [DT_visible_string],  # #无线公网通讯模块1：设备描述符
           '45000D00': [DT_structure,[DT_unsigned,DT_unsigned]],  # 运营商及网络制式（只读）
           '45000E00': [DT_array, [DT_structure, [DT_enum, DT_enum,DT_visible_string,DT_visible_string,
                       DT_visible_string, DT_octet_string,DT_long_unsigned,DT_enum,
                       [DT_array,[DT_structure,[DT_octet_string,DT_long_unsigned]]]]]],  #多网络配置，鉴权方式



           '45100200': [DT_structure,[DT_enum,DT_enum,DT_enum,[DT_array,[DT_long_unsigned]],
                                      DT_octet_string,
                                      DT_long_unsigned,DT_unsigned,DT_long_unsigned] ],  # 以太网通讯模块1：通讯配置
           '45100300': [DT_array, [DT_structure, [DT_octet_string, DT_long_unsigned]]],  #以太网通讯模块1：主站通讯参数
           '45100400': [DT_structure, [DT_enum, DT_octet_string,DT_octet_string, DT_octet_string,
                                       DT_visible_string, DT_visible_string]],  ##以太网通讯模块1：网络配置
           '45100500': [DT_octet_string],  # 以太网通讯模块1：MAC地址

           '45200200': [DT_array, [DT_structure, [DT_enum, DT_enum,DT_visible_string, DT_visible_string,
                        DT_visible_string, DT_octet_string,DT_long_unsigned,
                       [ DT_array,[DT_structure, [DT_octet_string,DT_long_unsigned]]]]]],  #公网远程通信多接入点备用通道
           '45200300': [DT_structure, [DT_enum,DT_enum ]],  ##公网远程通信多接入点备用通道：运营商和网络类型
           '45200400': [ DT_enum],  ##公网远程通信多接入点备用通道：锁定网络

            #电能表跟随上报模式字
           '20150400':[DT_bit_string],
            # 电能表跟随上报方式
           '20150500':[DT_enum],
           #区间统计类
           ##特殊数据标识，多加1位来判断是属性还是方法，+“0”是属性，+“1”是方法
           '210003001': [DT_structure,[DT_OAD,[DT_array,[DT_Region,[DT_ENUMERATED,DT_yxparam,DT_yxparam]]],DT_unsigned,DT_TI]],  ##区间统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '210003000':[DT_array,[DT_structure,[DT_OAD,[DT_array,[DT_Region,[DT_ENUMERATED,DT_yxparam,DT_yxparam]]],
                                    DT_unsigned,DT_TI]] ],  ##分钟区间统计属性设置
           '210103001': [DT_structure,[DT_OAD,[DT_array,[DT_Region,[DT_ENUMERATED,DT_yxparam,DT_yxparam]]],DT_unsigned,DT_TI]],  ##区间统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '210103000':[DT_array,[DT_structure,[DT_OAD,[DT_array,[DT_Region,[DT_ENUMERATED,DT_yxparam,DT_yxparam]]],
                                    DT_unsigned,DT_TI]] ],  ##小时区间统计属性设置
           '210203001': [DT_structure,[DT_OAD,[DT_array,[DT_Region,[DT_ENUMERATED,DT_yxparam,DT_yxparam]]],DT_unsigned,DT_TI]],  ##区间统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '210203000':[DT_array,[DT_structure,[DT_OAD,[DT_array,[DT_Region,[DT_ENUMERATED,DT_yxparam,DT_yxparam]]],
                                    DT_unsigned,DT_TI]] ],  ##日区间统计属性设置

           '210303001': [DT_structure,[DT_OAD,[DT_array,[DT_Region,[DT_ENUMERATED,DT_yxparam,DT_yxparam]]],DT_unsigned,DT_TI]],  ##区间统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '210303000':[DT_array,[DT_structure,[DT_OAD,[DT_array,[DT_Region,[DT_ENUMERATED,DT_yxparam,DT_yxparam]]],
                                    DT_unsigned,DT_TI]] ],  ##月区间统计属性设置

           '210403001': [DT_structure,[DT_OAD,[DT_array,[DT_Region,[DT_ENUMERATED,DT_yxparam,DT_yxparam]]],DT_unsigned,DT_TI]],  ##区间统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '210403000':[DT_array,[DT_structure,[DT_OAD,[DT_array,[DT_Region,[DT_ENUMERATED,DT_yxparam,DT_yxparam]]],
                                    DT_unsigned,DT_TI]] ],  ##年区间统计属性设置
           #累加平均类
           '211003001': [DT_structure,[DT_OAD,DT_unsigned,DT_TI]],  ##分钟，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '211003000':[DT_array,[DT_structure,[DT_OAD, DT_unsigned,DT_TI]] ],  ##分钟统计属性设置
           '211103001': [DT_structure, [DT_OAD, DT_unsigned, DT_TI]],  ##小时统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '211103000': [DT_array, [DT_structure, [DT_OAD, DT_unsigned, DT_TI]]],  ##小时统计属性设置
           '211203001': [DT_structure, [DT_OAD, DT_unsigned, DT_TI]],  ##日统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '211203000': [DT_array, [DT_structure, [DT_OAD, DT_unsigned, DT_TI]]],  ##日统计属性设置
           '211303001': [DT_structure, [DT_OAD, DT_unsigned, DT_TI]],  ##月统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '211303000': [DT_array, [DT_structure, [DT_OAD, DT_unsigned, DT_TI]]],  ##月统计属性设置
           '211403001': [DT_structure, [DT_OAD, DT_unsigned, DT_TI]],  ##年统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '211403000': [DT_array, [DT_structure, [DT_OAD, DT_unsigned, DT_TI]]],  ##年统计属性设置

           #极值类
           '212003001': [DT_structure,[DT_OAD,DT_unsigned,DT_TI]],  ##分钟，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '212003000':[DT_array,[DT_structure,[DT_OAD, DT_unsigned,DT_TI]] ],  ##分钟统计属性设置
           '212103001': [DT_structure, [DT_OAD, DT_unsigned, DT_TI]],  ##小时统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '212103000': [DT_array, [DT_structure, [DT_OAD, DT_unsigned, DT_TI]]],  ##小时统计属性设置
           '212203001': [DT_structure, [DT_OAD, DT_unsigned, DT_TI]],  ##日统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '212203000': [DT_array, [DT_structure, [DT_OAD, DT_unsigned, DT_TI]]],  ##日统计属性设置
           '212303001': [DT_structure, [DT_OAD, DT_unsigned, DT_TI]],  ##月统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '212303000': [DT_array, [DT_structure, [DT_OAD, DT_unsigned, DT_TI]]],  ##月统计属性设置
           '212403001': [DT_structure, [DT_OAD, DT_unsigned, DT_TI]],  ##年统计，DT_yxparam这个参数暂时没有用到，程序中直接根据关联OAD进行转换的
           '212403000': [DT_array, [DT_structure, [DT_OAD, DT_unsigned, DT_TI]]],  ##年统计属性设置
           #区间统计 删除
           '21000400': [DT_OAD], '21010400': [DT_OAD], '21020400': [DT_OAD], '21030400': [DT_OAD], '21040400': [DT_OAD],
           #累加平均统计 删除
           '21100400': [DT_OAD], '21110400': [DT_OAD], '21120400': [DT_OAD], '21130400': [DT_OAD], '21140400': [DT_OAD],
           #极值统计 删除
           '21200400': [DT_OAD], '21210400': [DT_OAD], '21220400': [DT_OAD], '21230400': [DT_OAD], '21240400': [DT_OAD],
           #逻辑名对应数据类型，统计类等关联对象属性时，确定越限判断参数的数据类型
           '20000201':[DT_long_unsigned], '20000202':[DT_long_unsigned], '20000203':[DT_long_unsigned],  #电压
           '20010201':[DT_double_long], '20010202':[DT_double_long], '20010203':[DT_double_long], '20010400':[DT_double_long], '20010200':[DT_double_long],
           #电流
           '20040201':[DT_double_long], '20040202':[DT_double_long], '20040203':[DT_double_long], '20040204':[DT_double_long],  #有功功率
           '20050201': [DT_double_long], '20050202': [DT_double_long], '20050203': [DT_double_long], '20050204': [DT_double_long],  #无功功率
           '20060201': [DT_double_long], '20060202': [DT_double_long], '20060203': [DT_double_long], '20060204': [DT_double_long],  #视在功率
           #为了区间统计特意加的标识：200A0200方法2目前不用，属性只存在召测，故目前这么使用是可以的，以后如果有更改，需要对方法和属性或者当前的标识做优化。wm 2020 11 11
           '200A0200': [DT_long],
           '200A0201': [DT_long], '200A0202': [DT_long], '200A0203': [DT_long], '200A0204': [DT_long],  #功率因数
           '20260200': [DT_long_unsigned],  #电压不平衡率
           '20270200': [DT_long_unsigned],  #电流不平衡率


           #脉冲：
           #脉冲1
           '24010200': [DT_octet_string],
           ##特殊数据标识，多加1位来判断是属性还是方法，+“0”是属性，+“1”是方法
           '240103000': [DT_structure, [DT_long_unsigned,DT_long_unsigned]],  ##脉冲1：属性3：互感器倍率
           '240103001': [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]],  ##脉冲1：方法3：添加脉冲输入单元

           '240104000':  [DT_array,[DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]]],  ##脉冲1：属性4：脉冲配置
           '240104001': [DT_OAD],
           #脉冲2
           '24020200': [DT_octet_string],
           ##特殊数据标识，多加1位来判断是属性还是方法，+“0”是属性，+“1”是方法
           '240203000': [DT_structure, [DT_long_unsigned,DT_long_unsigned]],  ##脉冲1：属性3：互感器倍率
           '240203001': [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]],  ##脉冲1：方法3：添加脉冲输入单元

           '240204000':  [DT_array,[DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]]],  ##脉冲1：属性4：脉冲配置
           '240204001': [DT_OAD],

           # 脉冲3
           '24030200': [DT_octet_string],
           ##特殊数据标识，多加1位来判断是属性还是方法，+“0”是属性，+“1”是方法
           '240303000': [DT_structure, [DT_long_unsigned, DT_long_unsigned]],  ##脉冲1：属性3：互感器倍率
           '240303001': [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]],  ##脉冲1：方法3：添加脉冲输入单元

           '240304000': [DT_array, [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]]],  ##脉冲1：属性4：脉冲配置
           '240304001': [DT_OAD],
           # 脉冲4
           '24040200': [DT_octet_string],
           ##特殊数据标识，多加1位来判断是属性还是方法，+“0”是属性，+“1”是方法
           '240403000': [DT_structure, [DT_long_unsigned, DT_long_unsigned]],  ##脉冲1：属性3：互感器倍率
           '240403001': [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]],  ##脉冲1：方法3：添加脉冲输入单元

           '240404000': [DT_array, [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]]],  ##脉冲1：属性4：脉冲配置
           '240404001': [DT_OAD],

           # 脉冲5
           '24050200': [DT_octet_string],
           ##特殊数据标识，多加1位来判断是属性还是方法，+“0”是属性，+“1”是方法
           '240503000': [DT_structure, [DT_long_unsigned, DT_long_unsigned]],  ##脉冲1：属性3：互感器倍率
           '240503001': [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]],  ##脉冲1：方法3：添加脉冲输入单元

           '240504000': [DT_array, [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]]],  ##脉冲1：属性4：脉冲配置
           '240504001': [DT_OAD],
           # 脉冲6
           '24060200': [DT_octet_string],
           ##特殊数据标识，多加1位来判断是属性还是方法，+“0”是属性，+“1”是方法
           '240603000': [DT_structure, [DT_long_unsigned, DT_long_unsigned]],  ##脉冲1：属性3：互感器倍率
           '240603001': [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]],  ##脉冲1：方法3：添加脉冲输入单元

           '240604000': [DT_array, [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]]],  ##脉冲1：属性4：脉冲配置
           '240604001': [DT_OAD],

           # 脉冲7
           '24070200': [DT_octet_string],
           ##特殊数据标识，多加1位来判断是属性还是方法，+“0”是属性，+“1”是方法
           '240703000': [DT_structure, [DT_long_unsigned, DT_long_unsigned]],  ##脉冲1：属性3：互感器倍率
           '240703001': [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]],  ##脉冲1：方法3：添加脉冲输入单元

           '240704000': [DT_array, [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]]],  ##脉冲1：属性4：脉冲配置
           '240704001': [DT_OAD],
           # 脉冲8
           '24080200': [DT_octet_string],
           ##特殊数据标识，多加1位来判断是属性还是方法，+“0”是属性，+“1”是方法
           '240803000': [DT_structure, [DT_long_unsigned, DT_long_unsigned]],  ##脉冲1：属性3：互感器倍率
           '240803001': [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]],  ##脉冲1：方法3：添加脉冲输入单元

           '240804000': [DT_array, [DT_structure, [DT_OAD, DT_enum, DT_long_unsigned]]],  ##脉冲1：属性4：脉冲配置
           '240804001': [DT_OAD],


           #总加组
           #总加组1
           '23010100': [DT_NULL],
           '23010200':[DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],

           '23010300': [DT_structure, [DT_TSA, DT_enum, DT_enum]],
           '23010400':[DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],
           '23010500': [DT_TSA],
           '23010D00': [DT_unsigned],
           '23010E00': [DT_bit_string],
           '23010F00': [DT_bit_string],

           # 总加组2
           '23020100': [DT_NULL],
           '23020200': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],

           '23020300': [DT_structure, [DT_TSA, DT_enum, DT_enum]],
           '23020400': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],
           '23020500': [DT_TSA],
           '23020D00': [DT_unsigned],
           '23020E00': [DT_bit_string],
           '23020F00': [DT_bit_string],

           # 总加组3
           '23030100': [DT_NULL],
           '23030200': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],

           '23030300': [DT_structure, [DT_TSA, DT_enum, DT_enum]],
           '23030400': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],
           '23030500': [DT_TSA],
           '23030D00': [DT_unsigned],
           '23030E00': [DT_bit_string],
           '23030F00': [DT_bit_string],

           # 总加组4
           '23040100': [DT_NULL],
           '23040200': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],

           '23040300': [DT_structure, [DT_TSA, DT_enum, DT_enum]],
           '23040400': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],
           '23040500': [DT_TSA],
           '23040D00': [DT_unsigned],
           '23040E00': [DT_bit_string],
           '23040F00': [DT_bit_string],

           # 总加组5
           '23050100': [DT_NULL],
           '23050200': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],

           '23050300': [DT_structure, [DT_TSA, DT_enum, DT_enum]],
           '23050400': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],
           '23050500': [DT_TSA],
           '23050D00': [DT_unsigned],
           '23050E00': [DT_bit_string],
           '23050F00': [DT_bit_string],

           # 总加组6
           '23060100': [DT_NULL],
           '23060200': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],

           '23060300': [DT_structure, [DT_TSA, DT_enum, DT_enum]],
           '23060400': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],
           '23060500': [DT_TSA],
           '23060D00': [DT_unsigned],
           '23060E00': [DT_bit_string],
           '23060F00': [DT_bit_string],

           # 总加组7
           '23070100': [DT_NULL],
           '23070200': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],

           '23070300': [DT_structure, [DT_TSA, DT_enum, DT_enum]],
           '23070400': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],
           '23070500': [DT_TSA],
           '23070D00': [DT_unsigned],
           '23070E00': [DT_bit_string],
           '23070F00': [DT_bit_string],

           # 总加组8
           '23080100': [DT_NULL],
           '23080200': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],

           '23080300': [DT_structure, [DT_TSA, DT_enum, DT_enum]],
           '23080400': [DT_array, [DT_structure, [DT_TSA, DT_enum, DT_enum]]],
           '23080500': [DT_TSA],
           '23080D00': [DT_unsigned],
           '23080E00': [DT_bit_string],
           '23080F00': [DT_bit_string],

           #事件
           #电能表失压事件
           '30000100':[DT_integer],
           '300005000': [DT_structure,[DT_long_unsigned,DT_long_unsigned,DT_double_long,DT_unsigned]],
           '300005001': [DT_OAD],
           '30000B00':[DT_enum],
           '30000C00':[DT_bool],
           #电能表欠压事件
           '300105000': [DT_structure,[DT_long_unsigned,DT_unsigned]],
           '300105001': [DT_OAD],
           '30010B00':[DT_enum],
           '30010C00':[DT_bool],
           # 属性和方法标识相同
           '30020100':[DT_integer],
           '300205000': [DT_structure, [DT_long_unsigned,  DT_unsigned]],
           '300205001': [DT_OAD],
           '30020B00':[DT_enum],
           '30020C00': [DT_bool],
           '30030100':[DT_integer],
           '300305000': [DT_structure, [DT_long_unsigned,DT_double_long, DT_unsigned]],
           '300305001': [DT_OAD],
           '30030B00':[DT_enum],
           '30030C00': [DT_bool],
           '30040100':[DT_integer],
           '300405000': [DT_structure, [DT_long_unsigned, DT_double_long,DT_double_long, DT_unsigned]],
           '300405001': [DT_OAD],
           '30040B00':[DT_enum],
           '30040C00': [DT_bool],
           '30050100':[DT_integer],
           '300505000': [DT_structure, [DT_double_long,  DT_unsigned]],
           '300505001': [DT_OAD],
           '30050B00':[DT_enum],
           '30050C00': [DT_bool],
           '30050F00': [DT_enum],
           '30060100':[DT_integer],
           '300605000': [DT_structure, [DT_long_unsigned,DT_double_long,  DT_unsigned]],
           '300605001': [DT_OAD],
           '30060B00':[DT_enum],
           '30060C00': [DT_bool],
           '30070100':[DT_integer],
           '300705000': [DT_structure, [DT_double_long,  DT_unsigned]],
           '300705001': [DT_OAD],
           '30070B00':[DT_enum],
           '30070C00': [DT_bool],
           '30080100':[DT_integer],
           '300805000': [DT_structure, [DT_double_long,  DT_unsigned]],
           '300805001': [DT_OAD],
           '30080B00':[DT_enum],
           '30080C00': [DT_bool],
           '300B0100':[DT_integer],
           '300B05000': [DT_structure, [DT_double_long_unsigned,  DT_unsigned]],
           '300B05001': [DT_OAD],
           '300B0B00':[DT_enum],
           '300B0C00': [DT_bool],
           '30190100': [DT_integer],
           '30090600': [DT_structure, [DT_double_long_unsigned, DT_unsigned]],
           '30090800':[DT_enum],
           '30090900': [DT_bool],
           '30090400': [DT_OAD],
           '30090500': [DT_OAD],
           '301A0100': [DT_integer],
           '301B0800': [DT_enum],
           '301B0B00': [DT_enum],
           '300A0100':[DT_integer],
           '300A0600': [DT_structure,[DT_double_long_unsigned,DT_unsigned]],
           '300A0800':[DT_enum],
           '300A0900': [DT_bool],
           '300A0400': [DT_OAD],
           '300A0500': [DT_OAD],
           '301C0100': [DT_integer],
           '300C0600': [DT_structure,[DT_long,DT_unsigned]],
           '300C0800':[DT_enum],
           '300C0900': [DT_bool],
           '300C0400': [DT_OAD],
           '300C0500': [DT_OAD],
           '30090100': [DT_integer],
           '300E0600': [DT_structure,[DT_unsigned]],
           '300E0800':[DT_enum],
           '300E0900': [DT_bool],
           '300E0400': [DT_OAD],
           '300E0500': [DT_OAD],

           '300F0600': [DT_structure,[DT_unsigned]],
           '300F0800':[DT_enum],
           '300F0900': [DT_bool],
           '300F0400': [DT_OAD],
           '300F0500': [DT_OAD],
           '30130800': [DT_enum],
           '30130900': [DT_bool],
           '30140100': [DT_integer],
           '30140800': [DT_enum],
           '30140900': [DT_bool],
           '300C0100': [DT_integer],
           '30150800':[DT_enum],
           '30150900':[DT_bool],
           '30140100': [DT_integer],
           '301D0100': [DT_integer],
           '301E0100': [DT_integer],
           '301D0600': [DT_structure,[DT_long,DT_unsigned]],
           '301D0800':[DT_enum],
           '301D0900': [DT_bool],
           '301D0400': [DT_OAD],
           '301D0500': [DT_OAD],
           '30140100': [DT_integer],
           '301E0600': [DT_structure,[DT_long,DT_unsigned]],
           '301E0800':[DT_enum],
           '301E0900': [DT_bool],
           '301E0400': [DT_OAD],
           '301E0500': [DT_OAD],

           '301F0600': [DT_structure,[DT_long,DT_long,DT_double_long_unsigned,DT_unsigned]],
           '301F0400': [DT_OAD],
           '301F0500': [DT_OAD],
           '303B0500': [DT_structure,[DT_long,DT_unsigned]],
           '303B0B00':[DT_enum],
           '303B0C00': [DT_bool],

           '30400600': [DT_structure,[DT_long_unsigned,DT_long_unsigned,DT_unsigned]],
           '30400400': [DT_OAD],
           '30400500': [DT_OAD],
           '302A0800': [DT_enum],
           '302A0B00': [DT_enum],
           '302E0300':[DT_array,[DT_OAD]],
           '302E0800': [DT_enum],
           '302E0B00': [DT_enum],
           '302F0300':[DT_array,[DT_OAD]],
           '30110800': [DT_enum],
           '30110B00': [DT_enum],
           '31040800': [DT_enum],
           '31040900': [DT_bool],
           '310A0800': [DT_enum],
           '310A0900': [DT_bool],
           #电流互感器事件
           '31200800': [DT_enum],
           '31200900': [DT_bool],
           '32000800':[DT_enum],
           '32000900': [DT_bool],
           '32010800':[DT_enum],
           '32010900': [DT_bool],
           '32020800':[DT_enum],
           '32020900': [DT_bool],
           '32030800':[DT_enum],
           '32030900': [DT_bool],
           '31150800':[DT_enum],
           '31150900': [DT_bool],
           '31400800': [DT_enum],
           '31400900': [DT_bool],
            #通讯地址
           '40010200': [DT_octet_string],
           #备用套时区表切换时间
           '40080200': [DT_date_time_s],
           #备用套阶梯电价切换时间
           '400B0200': [DT_date_time_s],
           #备用套阶梯电价切换时间
           '400D0200': [DT_unsigned],
           #公共假日表
           '40110200': [DT_array,[DT_structure,[DT_date,DT_unsigned]]],
            #周休日特征字
           '40120200': [DT_bit_string],
           #周休日采用的日时段表号
           '40130200': [DT_unsigned],
           #当前套时区表
           '40140200': [DT_array,[DT_structure,[DT_unsigned,DT_unsigned,DT_unsigned]]],
           #备用套时区表
           '40150200': [DT_array,[DT_structure,[DT_unsigned,DT_unsigned,DT_unsigned]]],
           #当前套阶梯电价
           '401A0200': [DT_structure, [[DT_array,[DT_double_long_unsigned]],[DT_array,[DT_double_long_unsigned]],[DT_array,[DT_structure,[DT_unsigned,DT_unsigned,DT_unsigned]]]]],
            #备用套阶梯电价
           '401B0200': [DT_structure, [[DT_array,[DT_double_long_unsigned]],[DT_array,[DT_double_long_unsigned]],[DT_array,[DT_structure,[DT_unsigned,DT_unsigned,DT_unsigned]]]]],
           # 电流互感器变比
           '401C0200': [DT_double_long_unsigned],
           # 电压互感器变比
           '401D0200': [DT_double_long_unsigned],
           #电流回路监测使能
           '40410200': [DT_structure,[DT_bool,DT_bool,DT_bool]],
           #最大需量周期
           '41000200': [DT_unsigned],
           #最大需量周期
           '41010200': [DT_unsigned],
           #资产管理码
           '41030200': [DT_visible_string],
          # 资产管理码
           '41040200': [DT_visible_string],
           #有功组合方式特征字
           '41120200': [DT_bit_string],
           #无功组合方式1特征字
           '41130200': [DT_bit_string],
           # 无功组合方式2特征字
           '41140200': [DT_bit_string],
           # 结算日
           '41160200': [DT_array,[DT_structure,[DT_unsigned,DT_unsigned]]],
           # 每月第1结算日
           '41160201': [DT_structure,[DT_unsigned,DT_unsigned]],
           # 每月第2结算日
           '41160202': [DT_structure,[DT_unsigned,DT_unsigned]],
           # 每月第3结算日
           '41160203': [DT_structure,[DT_unsigned,DT_unsigned]],

           # 期间需量冻结周期
           '41170200': [DT_TI],







            '80000201':[DT_double_long_unsigned],
            '80000201': [DT_long_unsigned],
           #控制
           #保电
           '80010300': [DT_long_unsigned],  #允许与主站最大通讯时长（分钟）
           '80010400': [DT_long_unsigned],  #上电自动保电时长（分钟）
           '80010500': [DT_array,[DT_structure,[DT_unsigned,DT_unsigned]]],  #自动保电时段
           '80017F00': [DT_NULL],  #投入保电
           '80018000': [DT_NULL],  #解除保电
           '80018100': [DT_NULL],  #解除自动保电
           #催费告警
           '80027F00': [DT_structure, [DT_octet_string, DT_visible_string]],  # 催费告警投入
           '80020300': [DT_structure, [DT_octet_string, DT_visible_string]],  # 催费告警参数读取
           #一般中文信息80038000
           '80038000': [DT_unsigned],  #删除信息（序号）
           '80030400': [DT_long_unsigned],  #最大元素个数
           '80037F00': [DT_structure, [DT_unsigned, DT_date_time_s,DT_visible_string]],  # 添加信息
           # 重要中文信息80048000
           '80048000': [DT_unsigned],  # 删除信息（序号）
           '80040400': [DT_long_unsigned],  # 最大元素个数
           '80047F00': [DT_structure, [DT_unsigned, DT_date_time_s, DT_visible_string]],  # 添加信息
           #远程控制：
           '80000200': [DT_structure,[DT_double_long_unsigned,DT_long_unsigned]],  # 配置参数
           '80000400': [DT_bit_string],  # 告警状态，只读参数
           '80007F00': [DT_NULL],  #触发报警
           '80008000': [DT_NULL],  #解除报警
           '80008100': [DT_array, [DT_structure, [DT_OAD, DT_unsigned, DT_long_unsigned, DT_bool]]],  #跳闸
           '80008200': [DT_array,[DT_structure, [DT_OAD, DT_enum ]]],  #合闸
           #终端保安定值
           '81000200': [DT_long64],
           #终端工控时段
           '81010200': [DT_array,[DT_unsigned]],
           # 工控告警时间
           '81020200': [DT_array, [DT_unsigned]],

           ##时段工控
           '810303000': [DT_array,[DT_structure, [DT_OI, DT_enum ]]],  #控制投入状态
           '810303001': [DT_structure, [DT_OI,DT_bit_string,[DT_structure,[DT_bit_string,DT_long64,DT_long64,DT_long64,DT_long64,DT_long64,DT_long64,DT_long64,
                                            DT_long64]], [DT_structure,[DT_bit_string,DT_long64,DT_long64,
                                            DT_long64,DT_long64,DT_long64,DT_long64,DT_long64,DT_long64]],[DT_structure,[DT_bit_string,DT_long64,DT_long64,
                                            DT_long64,DT_long64,DT_long64,DT_long64,DT_long64,DT_long64,]],DT_integer ]],  #添加控制方案单元
           '81030500': [DT_structure, [DT_OI, DT_bit_string, [DT_structure,
                                                               [DT_bit_string, DT_long64, DT_long64, DT_long64,
                                                                DT_long64, DT_long64, DT_long64, DT_long64,
                                                                DT_long64]],
                                        [DT_structure, [DT_bit_string, DT_long64, DT_long64,
                                                        DT_long64, DT_long64, DT_long64, DT_long64, DT_long64,
                                                        DT_long64]],
                                        [DT_structure, [DT_bit_string, DT_long64, DT_long64,
                                                        DT_long64, DT_long64, DT_long64, DT_long64, DT_long64,
                                                        DT_long64, ]], DT_integer]],  # 更新控制方案单元
           '81037F00':[DT_structure, [DT_OI, [DT_structure,[DT_bit_string,DT_unsigned]]]],
           '81030600':[DT_OI], '81030700':[DT_OI],
           '81030400':[DT_OI],
           '81030200':[DT_array,[DT_structure, [DT_OI, DT_bit_string, [DT_structure,
                                                              [DT_bit_string, DT_long64, DT_long64, DT_long64,
                                                               DT_long64, DT_long64, DT_long64, DT_long64,
                                                               DT_long64]],
                                       [DT_structure, [DT_bit_string, DT_long64, DT_long64,
                                                       DT_long64, DT_long64, DT_long64, DT_long64, DT_long64,
                                                       DT_long64]],
                                       [DT_structure, [DT_bit_string, DT_long64, DT_long64,
                                                       DT_long64, DT_long64, DT_long64, DT_long64, DT_long64,
                                                       DT_long64, ]], DT_integer]]],  # 控制方案集
           ##厂休控
           '810403000': [DT_array, [DT_structure, [DT_OI, DT_enum]]],  # 控制投入状态
           '810403001':[DT_structure, [DT_OI,DT_long64,DT_date_time_s,DT_long_unsigned,DT_bit_string]],
           '81040500':[DT_structure, [DT_OI,DT_long64,DT_date_time_s,DT_long_unsigned,DT_bit_string]],
           '81040600':[DT_OI], '81040700':[DT_OI],
           '81040400':[DT_OI],
           '81040200':[DT_array,[DT_structure, [DT_OI,DT_long64,DT_date_time_s,DT_long_unsigned,DT_bit_string]]],

           ##营业报停控
           '810503000': [DT_array, [DT_structure, [DT_OI, DT_enum]]],  # 控制投入状态
           '810503001': [DT_structure, [DT_OI, DT_date_time_s, DT_date_time_s,DT_long64 ]],
           '81050500': [DT_structure, [DT_OI, DT_date_time_s, DT_date_time_s,DT_long64 ]],
           '81050600': [DT_OI], '81050700': [DT_OI],
           '81050400': [DT_OI],
           '81050200':  [DT_array, [DT_structure, [DT_OI, DT_date_time_s, DT_date_time_s, DT_long64]]],

           #下浮控
           '81067F00':[DT_structure,[DT_OI,[DT_structure,[DT_unsigned,DT_integer,DT_unsigned,DT_unsigned,DT_unsigned,DT_unsigned,DT_unsigned,DT_unsigned]]]],
           '81060500': [DT_structure, [DT_OI, [DT_structure, [DT_unsigned, DT_integer, DT_unsigned, DT_unsigned, DT_unsigned, DT_unsigned, DT_unsigned, DT_unsigned]]]],  #不支持
           '81060600': [DT_OI], '81060700': [DT_OI], '81060400': [DT_OI],  #04删除不支持
           '81060300': [DT_array, [DT_structure, [DT_OI, DT_enum]]],  # 控制投入状态

           ##购电控
           '810703000': [DT_array, [DT_structure, [DT_OI, DT_enum]]],  # 控制投入状态
           '810703001': [DT_structure, [DT_OI, DT_double_long_unsigned, DT_enum, DT_enum,DT_long64,DT_long64,DT_long64,DT_enum]],
           '81070500': [DT_structure, [DT_OI, DT_double_long_unsigned, DT_enum, DT_enum,DT_long64,DT_long64,DT_long64,DT_enum]],
           '81070600': [DT_OI], '81070700': [DT_OI],
           '81070400': [DT_OI],
           '81070200': [DT_array,  [DT_structure, [DT_OI, DT_double_long_unsigned, DT_enum, DT_enum,DT_long64,DT_long64,DT_long64,DT_enum]]],

           ##月电控
           '810803000': [DT_array, [DT_structure, [DT_OI, DT_enum]]],  # 控制投入状态
           '810803001': [DT_structure, [DT_OI, DT_long64,DT_unsigned,DT_integer]],
           '81080500': [DT_structure, [DT_OI, DT_long64,DT_unsigned,DT_integer]],
           '81080600': [DT_OI], '81080700': [DT_OI],
           '81080400': [DT_OI],
           '81080200': [DT_array,  [DT_structure, [DT_OI, DT_long64,DT_unsigned,DT_integer]]],

           #时区时段数
           '400C0200': [DT_structure, [DT_unsigned, DT_unsigned,DT_unsigned,DT_unsigned,DT_unsigned]],  #时区时段数
           #年时区数
           '400C0201':  [DT_unsigned],
           #日时段表数
           '400C0202':  [DT_unsigned],
           #日时段数
           '400C0203':  [DT_unsigned],
           #费率数
           '400C0204':  [DT_unsigned],
           #公共假日数
           '400C0205':  [DT_unsigned],
           '40160200': [DT_array, [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]]],  # 当前套日时段表
           #当前套第一日时段表数据
           '40160201':  [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40160202':  [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40160203':  [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40160204':  [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
          # 当前套第1日时段表数据
           '40160205': [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40160206': [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40160207': [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40160208': [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40170200': [DT_array, [DT_array, [DT_structure,[DT_unsigned,DT_unsigned,DT_unsigned]]]],  #备用套日时段表
            #备用套第1日时段表数据
           '40170201':  [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40170202':  [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40170203':  [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40170204':  [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
          # 当前套第一日时段表数据
           '40170205': [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40170206': [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40170207': [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40170208': [DT_array, [DT_structure, [DT_unsigned, DT_unsigned, DT_unsigned]]],
           '40180200': [DT_array, [DT_double_long_unsigned]],  #备用套费率电价
           '40190200': [DT_array, [DT_double_long_unsigned]],  #备用套费率电价
           '400A0200':[DT_date_time_s],
           '40090200': [DT_date_time_s],
           #报警金额限值
           '401E0200':[DT_structure,[DT_double_long_unsigned,DT_double_long_unsigned]],
           #报警金额1限值
           '401E0201':[DT_double_long_unsigned],
           #报警金额2限值
           '401E0202':[DT_double_long_unsigned],
           #其它金额限值
           '401F0200':[DT_structure,[DT_double_long_unsigned,DT_double_long_unsigned,DT_double_long_unsigned]],
           #透支金额限值
           '401F0201':[DT_double_long_unsigned],
           #囤积金额限值
           '401F0202':[DT_double_long_unsigned],
           #合闸允许金额限值
           '401F0203':[DT_double_long_unsigned],
           #主站会话时效门限
           'F1000500':[DT_double_long_unsigned],
           #安全模式参数
           'F1010200':[DT_enum],
           #显式安全模式参数
           'F1010300':[DT_array,[DT_structure,[DT_OI,DT_long_unsigned]]],
           #接口类
           'F2000300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F2007F00':  [DT_structure,[DT_OAD,[DT_COMDCB,[CHOICE_BR,CHOICE_CRC,CHOICE_DATA,CHOICE_STOP,CHOICE_CTRO]],DT_enum]],  #串口控制块定义特殊
           'F2010300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F2017F00':  [DT_structure,[DT_OAD,[DT_COMDCB,[CHOICE_BR,CHOICE_CRC,CHOICE_DATA,CHOICE_STOP,CHOICE_CTRO]],DT_enum]],  #串口控制块定义特殊
            #第1路RS485
           'F2010201': [DT_structure, [DT_visible_string, DT_COMDCB,DT_enum]],
           # 第2路RS485
           'F2010202': [DT_structure, [DT_visible_string, DT_COMDCB, DT_enum]],
            #红外端口
           'F2020201':[DT_structure,[DT_visible_string,DT_COMDCB]],
           'F2020300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F2027F00':  [DT_structure,[DT_OAD,[DT_COMDCB,[CHOICE_BR,CHOICE_CRC,CHOICE_DATA,CHOICE_STOP,CHOICE_CTRO]]]],  #串口控制块定义特殊
           'F2030300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F2030400':  [DT_structure,[DT_bit_string,DT_bit_string]],
           'F2040300':[DT_structure,[DT_unsigned,DT_unsigned]],
           #继电器输出
           'F2050201': [DT_structure, [DT_visible_string, DT_enum, DT_enum, DT_enum]],
           'F2050202': [DT_structure, [DT_visible_string, DT_enum, DT_enum, DT_enum]],
           'F2050300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F2057F00':  [DT_structure,[DT_OAD,DT_enum]],
           'F2060300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F2060400':  [DT_array,[DT_structure,[DT_time,DT_time]]],
           'F2070300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F2077F00':  [DT_structure,[DT_OAD,DT_enum]],
           'F2080300':[DT_structure,[DT_unsigned,DT_unsigned]],
            # #载波/微功率无线接口:::;部分数据类型自动化程序不支持，需要完善
            'F2090201':[DT_structure,[DT_visible_string,DT_COMDCB,[DT_structure,[DT_visible_string,DT_visible_string,DT_date,DT_long_unsigned]]]],
           'F2090300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F2090600': [DT_TI],
           'F2090900': [DT_unsigned],
           'F2090A00': [DT_array,[DT_visible_string]],
           'F2090B001': [DT_unsigned],
           'F2090B000': [DT_enum],
           'F20A0300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F20B0300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F20B7F00':[DT_structure,[DT_OAD,[DT_structure,[DT_visible_string,DT_octet_string]]]],
           'F20C0300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F20D0300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F20E0300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F20F0300':[DT_structure,[DT_unsigned,DT_unsigned]],
           'F2137F00':[DT_structure,[DT_OAD,[DT_array,[DT_OAD]]]],
           'F2138000':[DT_structure,[DT_OAD,[DT_array,[DT_OAD]]]],
           'F2138100':[DT_structure,[DT_OAD]],

           #自动轮显每屏显示时间
           'F3000300':[DT_long_unsigned],
           #显示类
           'F3000500':[DT_structure,[DT_CSD,DT_unsigned,DT_long_unsigned]],
           #按键轮显每屏显示时间
           'F3010300':[DT_long_unsigned],

           #冻结类
           #分钟
           '50020400':  [DT_structure, [DT_long_unsigned, DT_OAD,DT_long_unsigned]],
           '50020500': [DT_OAD],
           '50020700': [DT_array, [DT_structure, [DT_long_unsigned, DT_OAD,DT_long_unsigned]]],
           '50020800': [DT_NULL],
           '500203000': [DT_array, [DT_structure, [DT_long_unsigned, DT_OAD,DT_long_unsigned]]],
           '500203001': [DT_long_unsigned],
           #小时
           '50030400': [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]],
           '50030500': [DT_OAD],
           '50030700': [DT_array, [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]]],
           '50030800': [DT_NULL],
           '500303000': [DT_array, [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]]],
           '500303001': [DT_long_unsigned],
           # 日
           '50040400': [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]],
           '50040500': [DT_OAD],
           '50040700': [DT_array, [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]]],
           '50040800': [DT_NULL],
           '500403000': [DT_array, [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]]],
           '500403001': [DT_long_unsigned],
           # 结算日
           '50050400': [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]],
           '50050500': [DT_OAD],
           '50050700': [DT_array, [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]]],
           '500503000': [DT_array, [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]]],
           '500503001': [DT_long_unsigned],

           # 月
           '50060400': [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]],
           '50060500': [DT_OAD],
           '50060700': [DT_array, [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]]],
           '50060800': [DT_NULL],
           '500603000': [DT_array, [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]]],
           '500603001': [DT_long_unsigned],

           # 年
           '50070400': [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]],
           '50070500': [DT_OAD],
           '50070700': [DT_array, [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]]],
           '50070800': [DT_NULL],
           '500703000': [DT_array, [DT_structure, [DT_long_unsigned, DT_OAD, DT_long_unsigned]]],
           '500703001': [DT_long_unsigned],























           '43000100': [DT_NULL], '43000300': [DT_NULL], '43000400': [DT_NULL], '43000500': [DT_NULL], '43000600': [DT_NULL],
           '43000700':[DT_bool],
           '43000800':[DT_bool],
           '43000A00': [DT_array, [DT_OAD]],
           '60008000': [DT_array, [DT_structure, [DT_long_unsigned, [DT_structure, [DT_TSA, DT_enum, DT_enum, DT_OAD,
                                                                                   DT_octet_string, DT_unsigned,
                                                                                   DT_unsigned, DT_enum,
                                                                                   DT_long_unsigned, DT_long_unsigned]],
                                   [DT_structure, [DT_TSA, DT_octet_string, DT_long_unsigned, DT_long_unsigned]],
                                   [DT_array, [DT_structure, [DT_OAD, '']]]]]],

           #6000采集档案配置表

           '60010201':[DT_long_unsigned],
           '60008300':[DT_long_unsigned],
           '60008400':[DT_structure, [DT_TSA, DT_enum, DT_enum, DT_OAD, DT_octet_string, DT_unsigned, DT_unsigned,
                                                                         DT_enum, DT_long_unsigned, DT_long_unsigned]],
           '60008500':[DT_structure,[DT_TSA,DT_OAD]],



           '60007F00': [DT_structure, [DT_long_unsigned, [DT_structure, [DT_TSA, DT_enum, DT_enum, DT_OAD,
                                                                         DT_octet_string, DT_unsigned, DT_unsigned,
                                                                         DT_enum, DT_long_unsigned, DT_long_unsigned]],
                                       [DT_structure, [DT_TSA, DT_octet_string, DT_long_unsigned, DT_long_unsigned]],
                                       [DT_array, [DT_structure, [DT_OAD, DT_long_unsigned]]]]],
           '60008600': [DT_NULL],
           '60008100': [DT_structure, [DT_long_unsigned, [DT_structure, [DT_TSA, DT_enum, DT_enum, DT_OAD,
                                                                         DT_octet_string, DT_unsigned, DT_unsigned,
                                                                         DT_enum, DT_long_unsigned, DT_long_unsigned]],
                                     ]],
           '60008200': [DT_structure, [DT_long_unsigned, [DT_structure, [DT_TSA, DT_octet_string, DT_long_unsigned, DT_long_unsigned]],
                        [DT_array, [DT_structure, [DT_OAD, '']]]]],

           #6012任务配置表
           '60130201':[DT_long_unsigned],
           '60130203':[DT_enum],
           '60130204':[DT_unsigned],
           '60130208':[DT_unsigned],
           '60130209':[DT_enum],

           #删除一组配置单元
           '60128000':[DT_array,[DT_unsigned]],
           #Clear
           '60128100':[DT_NULL],
           #Update
           '60128200': [DT_structure, [DT_unsigned, DT_enum]],
           '60120200': [DT_array, [DT_structure, [DT_unsigned, DT_TI, DT_enum, DT_unsigned, DT_date_time_s,
                                                  DT_date_time_s, DT_TI, DT_unsigned, DT_enum, DT_long_unsigned,
                                                  DT_long_unsigned, [DT_structure, [DT_enum, [DT_array, [DT_structure,
                                                                                                         [DT_unsigned,
                                                                                                          DT_unsigned,
                                                                                                          DT_unsigned,
                                                                                                          DT_unsigned]]]]]]]],






           '60127F00': [DT_array, [DT_structure, [DT_unsigned, DT_TI, DT_enum, DT_unsigned, DT_date_time_s,
                                                  DT_date_time_s, DT_TI, DT_unsigned, DT_enum, DT_long_unsigned,
                                                  DT_long_unsigned, [DT_structure, [DT_enum, [DT_array, [DT_structure,
                        [DT_unsigned, DT_unsigned,DT_unsigned,DT_unsigned]]]]]]]],














           #普通采集方案集
           '60150201':[DT_unsigned],
           #删除一组普通采集方案
           '60148000': [DT_array, [DT_unsigned]],
           # Clear
           '60148100': [DT_NULL],
           #Set_CSD
           '60148200': [DT_structure,[DT_unsigned,[DT_array,[DT_CSD]]]],

           '60140200': [DT_array, [DT_structure, [DT_unsigned, DT_long_unsigned, [DT_structure, [DT_unsigned, DT_facjtype]],
                                                  [DT_array, [DT_CSD]], DT_MS, DT_enum]]],


           '60147F00': [DT_array, [DT_structure, [DT_unsigned, DT_long_unsigned, [DT_structure, [DT_unsigned, DT_facjtype]],
                                                  [DT_array, [DT_CSD]], DT_MS, DT_enum]]],






           #事件采集方案
           '60168000': [DT_array,[DT_unsigned]],
           '60168100': [DT_NULL],
           '60168200': [DT_structure,[DT_unsigned,DT_bool]],

           '60167F00':  [DT_array, [DT_structure, [DT_unsigned,  [DT_structure, [DT_unsigned, DT_eventtype]],DT_MS,DT_bool,DT_long_unsigned]]],

           '60170201': [DT_unsigned],


           #读取记录型
           '60120300': [DT_RSD, DT_RCSD],
           #上报方案
           '601C7F00': [DT_array,[DT_structure,[DT_unsigned,[DT_array,[DT_OAD]],DT_TI,DT_unsigned,[DT_structure,[DT_unsigned,DT_reporttype]]]]],
           '601C8000': [DT_array, [DT_unsigned]],
           '601C8100': [DT_NULL],
           '601D0201': [DT_unsigned],




           #透明方案集
           '60188000': [DT_structure, [DT_unsigned,DT_TSA,[DT_structure,[DT_bool,DT_long_unsigned,DT_enum,[DT_structure,
                        [DT_unsigned,DT_long_unsigned,DT_long_unsigned]]]],[DT_array,[DT_structure,[DT_unsigned,DT_octet_string]]]]],
           '60188100': [DT_structure,[DT_unsigned,[DT_array,[DT_TSA]]]],
           '60188200': [DT_array, [DT_unsigned]],
           '60188300': [DT_NULL],
           '60190201': [DT_unsigned],




           '60187F00': [DT_structure,[DT_unsigned,[DT_array,[DT_structure,[DT_long_unsigned,DT_TSA,
        DT_long_unsigned,DT_long_unsigned,[DT_structure,[DT_bool,DT_long_unsigned,DT_enum,[DT_structure,
        [DT_unsigned,DT_long_unsigned,DT_long_unsigned]]]],[DT_array,[DT_structure,[DT_unsigned,DT_octet_string]]]]]],DT_long_unsigned] ],
           'F2087F00':[DT_octet_string],

        #扩展模块工装测试工具
        'FF147F00':[DT_array,[DT_structure,[DT_OAD,DT_enum]]],
        'FF148100':[DT_array,[DT_OAD]]


















           }


# 定义数据处理类型集合
OOPSPDATA = [DT_NULL, DT_bool, DT_double_long, DT_double_long_unsigned, DT_integer, DT_long, DT_unsigned,
             DT_long_unsigned, DT_long64, DT_long64_unsigned, DT_enum, DT_float32, DT_float64, DT_date_time, DT_date,
             DT_time,DT_bit_string,DT_date_time_s, DT_OI, DT_OAD, DT_OMD, DT_octet_string,DT_visible_string, DT_TSA, DT_TI, DT_MS]
OOPARRATDATA = [DT_array, DT_structure]
OOPVSDATA = [DT_facjtype, DT_sjcjtype,DT_eventtype,DT_reporttype]


# True,'True', '01', 1->'01'
def valuetoboolbuff(value):
    bdata = ''
    if isinstance(value, str):
        if value.upper() == 'TRUE' or value == '1' or value == '01':
            bdata += '01'
        else:
            bdata += '00'
    elif isinstance(value, float):
        if value > 0:
            bdata += '01'
        else:
            bdata += '00'
    elif isinstance(value, int):
        if value > 0:
            bdata += '01'
        else:
            bdata += '00'

    elif isinstance(value, bool):
        if value == True:
            bdata += '01'
        else:
            bdata += '00'
    else:
        bdata += '00'



    return bdata
#王梦新增：终端工控人视化转为机器识别（02020101->01011010）
def mantobin(manvalue):
    ee = ""
    cc = manvalue.split(",")
    for item in cc:
        dd = bin(int(item, 10))[2:].zfill(2)
        ee += str(dd)
    ff = reverse(ee)
    #unsigned :长度为2，要考虑到值为0的情况
    ff=hex(int(ff,2))[2:].zfill(2)
    return ff


def bintoman(binvalue):
    ss = ""
    bb = reverse(binvalue)
    for i in range(0, len(bb), 2):
        mm = str(int(bb[i:i + 2], 2))
        ss += "0" + mm + ","
    ss = ss.strip(",")
    return ss




# '13','13.0',13.0 ->0D
def valuetounsignedbuff(value):
    bdata = ''
    if isinstance(value, str):
        ifpos = value.find('.')
        if ifpos > 0:
            value = value[:ifpos]
        elif ifpos == 0:
            value = '0'
        idata = int(value, 10)
        bdata += numbertohex(idata, 2)
    elif isinstance(value, float):
        idata = int(value)
        bdata += numbertohex(idata, 2)
    elif isinstance(value, int):
        bdata += numbertohex(value, 2)
    else:
        bdata += '00'
    return bdata

# '-20' -20 ->'EC'
def inttohex(ivalue):
    shex = ''
    idata = 0
    if isinstance(ivalue, str):
        idata = int(ivalue)
    elif isinstance(ivalue, int):
        idata = ivalue
    else:
        idata = 0
    if idata >= 0:
        idata = idata % 128
        shex += numbertohex(idata, 2)
    else:
        idata = (128 - abs(idata))|0x80
        shex += numbertohex(idata, 2)
    return shex


# 'EC' '0xEC' 0xEC 0xec->'-20'
def hextoint(shex):
    sint = ''
    if isinstance(shex, str):
        shex = shex.replace('0x', '')
    elif isinstance(shex, int):
        shex = numbertohex(shex, 2)
    else:
        idata = 0
    bu = int(getbit(shex, 7, 8, 1))
    if bu == 1:
        itt = int(getbit(shex, 0, 7, 1), 2)
        sint += str((128 - itt)*(-1))
    else:
        sint += str(int(getbit(shex, 0, 7, 1), 2))
    return sint


# '20200117133824' ->'07E401110D2618' date_time_s  王梦新增分支：考虑到起始时间和结束时间有FF的情况，故需新增分支
def valuetodtsbuff(value):
    bdts = ''
    if len(value) == 0:
        return '07CF0102030405'
    if value =="FFFFFFFFFFFFFF":
        bdts="FFFFFFFFFFFFFF"
    else:
        dt = bcdtodatetime(value)
        bdts += hex(dt.year).replace('0x', '').zfill(4)
        bdts += hex(dt.month).replace('0x', '').zfill(2)
        bdts += hex(dt.day).replace('0x', '').zfill(2)
        bdts += hex(dt.hour).replace('0x', '').zfill(2)
        bdts += hex(dt.minute).replace('0x', '').zfill(2)
        bdts += hex(dt.second).replace('0x', '').zfill(2)
        bdts = bdts.upper()
    return bdts

# '20200117133824' ->'07E401110D2618' date_time_s
def valueto8104specialdtsbuff(value):
    bdts = ''
    if len(value) == 0:
        return '07CF0102030405'
    value="20190101"+value  #为了处理时间，给了一个固定的年月日，但后续程序不使用该年月日。
    dt = bcdtodatetime(value)
    bdts += 'FFFF'
    bdts += 'FF'
    bdts += 'FF'
    bdts += hex(dt.hour).replace('0x', '').zfill(2)
    bdts += hex(dt.minute).replace('0x', '').zfill(2)
    bdts += hex(dt.second).replace('0x', '').zfill(2)
    bdts = bdts.upper()
    return bdts

def valueto8105specialdtsbuff(value):
    bdts = ''
    if len(value) == 0:
        return '07CF0102030405'
    value=value+"120300" #为了处理时间，给了一个固定的年月日，但后续程序不使用该年月日。
    dt = bcdtodatetime(value)
    bdts += hex(dt.year).replace('0x', '').zfill(4)
    bdts += hex(dt.month).replace('0x', '').zfill(2)
    bdts += hex(dt.day).replace('0x', '').zfill(2)
    bdts += 'FF'
    bdts += 'FF'
    bdts += 'FF'
    bdts = bdts.upper()
    return bdts

#秒为FF
def valueto4009specialdtsbuff(value):
    bdts = ''
    if len(value) == 0:
        return '07CF0102030405'
    value=value[0:-2]+"00" #为了处理时间，给了一个固定的年月日，但后续程序不使用该年月日。
    if value[:-2] == '000000000000':
        bdts += '000000000000FF'
    else:
        dt = bcdtodatetime(value)
        bdts += hex(dt.year).replace('0x', '').zfill(4)
        bdts += hex(dt.month).replace('0x', '').zfill(2)
        bdts += hex(dt.day).replace('0x', '').zfill(2)
        bdts += hex(dt.hour).replace('0x', '').zfill(2)
        bdts += hex(dt.minute).replace('0x', '').zfill(2)
        bdts += 'FF'
        bdts = bdts.upper()
    return bdts



#王梦新增
def valuetotbuff(value):
    bdts = ''
    if len(value) == 0:
        return '000000'
    bdts += hex(int(value[0:2],10)).replace('0x', '').zfill(2)
    bdts += hex(int(value[2:4], 10)).replace('0x', '').zfill(2)
    bdts += hex(int(value[4:6], 10)).replace('0x', '').zfill(2)
    bdts = bdts.upper()
    return bdts


# '20200117133824' '20200117' ->07E4011105 date
def valuetodatebuff(value):
    bdts = ''
    if len(value) == 0:
        return '07CF010203'
    if len(value) < 14:
        value += '00000000000000'
    dt = bcdtodatetime(value)
    bdts += hex(dt.year).replace('0x', '').zfill(4)
    bdts += hex(dt.month).replace('0x', '').zfill(2)
    bdts += hex(dt.day).replace('0x', '').zfill(2)
    bdts += hex(dt.isoweekday()).replace('0x', '').zfill(2)
    bdts = bdts.upper()
    return bdts


# '20200117133824' '133824' ->0D2618 time
def valuetotimebuff(value):
    bdts = ''
    if len(value) == 0:
        return '010203'
    if len(value) < 14:
        value = value.zfill(14)
        value = '20200117' + value[8:]
    dt = bcdtodatetime(value)
    bdts += hex(dt.hour).replace('0x', '').zfill(2)
    bdts += hex(dt.minute).replace('0x', '').zfill(2)
    bdts += hex(dt.second).replace('0x', '').zfill(2)
    bdts = bdts.upper()
    return bdts

# '220.0', '2200'-> 0898
def valuetolongusingedbuff(value, scaler):
    sdata = ''
    idata = 0
    if isinstance(value, str):
        idata = int(value)
    elif isinstance(value, int) or isinstance(value, float):
        idata = value
    else:
        print('valuetolongusingedbuff 未知值', value)
    if scaler == 0:
        sdata += numbertohex(idata, 4)
    elif scaler == -1:
        idata = int(idata*10)
        sdata += numbertohex(idata, 4)
    elif scaler == -2:
        idata = int(idata*100)
        sdata += numbertohex(idata, 4)
    elif scaler == -3:
        idata = int(idata*1000)
        sdata += numbertohex(idata, 4)
    elif scaler == -4:
        idata = int(idata*10000)
        sdata += numbertohex(idata, 4)
    else:
        print('valuetolongusingedbuff 未知换算', scaler)
        sdata += numbertohex(idata, 2)
    return sdata


# '220.0', '2200'-> 0898#王梦新增：十进制转为doublelong，转为Buff(正负数都可以转)
def valuetodoublelongbuff(value, scaler):
    sdata = ''
    idata = 0
    if isinstance(value, str):
        idata = float(value)
    elif isinstance(value, int) or isinstance(value, float):
        idata = value
    else:
         print('valuetolongusingedbuff 未知值', value)
    if scaler == 0:
        idata=idata
    elif scaler == -1:
        idata = int(idata*10)
    elif scaler == -2:
        idata = int(idata*100)
    elif scaler == -3:
        idata = int(idata*1000)
    elif scaler == -4:
        idata = int(idata*10000)
    else:
        print('valuetolongusingedbuff 未知换算', scaler)
    if idata < 0:
       dd = "FFFFFFFF"
       aa = int(dd, 16)
       bb = idata + 1
       cc = aa + bb
       # idata = hex(int(str(cc), 10))[2:].upper()
       idata = cc
    else:
        idata = idata
    sdata += numbertohex(idata, 8)
    return sdata

# '220.0', '2200'-> 0898#王梦新增：十进制转为long，转为Buff(正负数都可以转)
def valuetolongbuff(value, scaler):
    sdata = ''
    idata = 0
    if isinstance(value, str):
        idata = int(value)
    elif isinstance(value, int) or isinstance(value, float):
        idata = value
    else:
         print('valuetolongusingedbuff 未知值', value)
    if scaler == 0:
        idata=idata
    elif scaler == -1:
        idata = int(idata*10)
    elif scaler == -2:
        idata = int(idata*100)
    elif scaler == -3:
        idata = int(idata*1000)
    elif scaler == -4:
        idata = int(idata*10000)
    else:
        print('valuetolongusingedbuff 未知换算', scaler)
    if idata < 0:
       dd = "FFFF"
       aa = int(dd, 16)
       bb = idata + 1
       cc = aa + bb
       # idata = hex(int(str(cc), 10))[2:].upper()
       idata = cc
    else:
        idata = idata
    sdata += numbertohex(idata, 4)
    return sdata

# #王梦新增：十进制转为long64，转为Buff(正负数都可以转)
def valuetolong64buff(value, scaler):
    sdata = ''
    idata = 0
    if isinstance(value, str):
        if value.find(".")>=0:
            idata1 = value.split(".")
            idata2=idata1[0]
            idata3 = '0.'+idata1[1]
            idata=float(idata3)
        else:
            idata = int(value)
    elif isinstance(value, int) or isinstance(value, float):
        if str(value).find(".") >= 0:
            idata1 = str(value).split(".")
            idata2 = idata1[0]
            idata3 = '0.' + idata1[1]
            idata = float(idata3)
        else:
            idata = value
    else:
         print('valuetolongusingedbuff 未知值', value)
    if scaler == 0:
        idata=idata
    elif scaler == -1:
        idata = int(idata*10)
    elif scaler == -2:
        idata = int(idata*100)
    elif scaler == -3:
        idata = int(idata*1000)
    elif scaler == -4:
        idata = int(idata*10000)
    else:
        print('valuetolongusingedbuff 未知换算', scaler)
    if idata < 0:
       dd = "FFFFFFFFFFFFFFFF"
       aa = int(dd, 16)
       bb = idata + 1
       cc = aa + bb
       # idata = hex(int(str(cc), 10))[2:].upper()
       idata = cc
    elif str(value).find(".")>=0:
        if idata==0.0:
            #或考虑到先以浮点数保存也可以，字符串是要先转为浮点数才可以再转为整数，且会丢失位。字符串小数（8.5）不可以直接转Int
            #小数部分为0，要考虑整数部分是否为0，若整数部分为0，则最终结果处理为0，否则4位还是要补上。
            if idata2=='0':
                idata = int(idata2)
            elif scaler == -1:
                idata=int(idata2+"0")
            elif scaler == -2:
                idata=int(idata2+"00")
            elif scaler == -3:
                idata=int(idata2+"000")
            elif scaler == -4:
                idata=int(idata2+"0000")
            else:
                print('valuetolongusingedbuff 未知换算', scaler)


        else:
            idata = int(idata2 + str(idata))

    else:
        idata = idata
    sdata += numbertohex(idata, 16)
    return sdata

# #王梦新增：十进制转为float32，转为Buff(正负数都可以转)
def valuetofloat32buff(value, scaler):
    sdata = ''
    idata = 0
    if isinstance(value, str):
        if value.find(".")>=0:
            idata1 = value.split(".")
            idata2=idata1[0]
            idata3 = '0.'+idata1[1]
            idata=float(idata3)
        else:
            idata = int(value)
    elif isinstance(value, int) or isinstance(value, float):
        if str(value).find(".") >= 0:
            idata1 = str(value).split(".")
            idata2 = idata1[0]
            idata3 = '0.' + idata1[1]
            idata = float(idata3)
        else:
            idata = value
    else:
         print('valuetolongusingedbuff 未知值', value)
    if scaler == 0:
        idata=idata
    elif scaler == -1:
        idata = int(idata*10)
    elif scaler == -2:
        idata = int(idata*100)
    elif scaler == -3:
        idata = int(idata*1000)
    elif scaler == -4:
        idata = int(idata*10000)
    else:
        print('valuetolongusingedbuff 未知换算', scaler)
    if idata < 0:
       dd = "FFFFFFFF"
       aa = int(dd, 16)
       bb = idata + 1
       cc = aa + bb
       # idata = hex(int(str(cc), 10))[2:].upper()
       idata = cc
    elif str(value).find(".")>=0:
        if idata==0.0:
            #或考虑到先以浮点数保存也可以，字符串是要先转为浮点数才可以再转为整数，且会丢失位。字符串小数（8.5）不可以直接转Int
            #小数部分为0，要考虑整数部分是否为0，若整数部分为0，则最终结果处理为0，否则4位还是要补上。
            if idata2=='0':
                idata = int(idata2)
            elif scaler == -1:
                idata=int(idata2+"0")
            elif scaler == -2:
                idata=int(idata2+"00")
            elif scaler == -3:
                idata=int(idata2+"000")
            elif scaler == -4:
                idata=int(idata2+"0000")
            else:
                print('valuetolongusingedbuff 未知换算', scaler)


        else:
            idata = int(idata2 + str(idata))

    else:
        idata = idata
    sdata += numbertohex(idata, 8)
    return sdata
#
# # '220.0', '2200'-> 0898#王梦新增：十进制转为doublelong，转为Buff
# def valuetodoublelongbuff(value, scaler):
#     sdata = ''
#     idata = 0
#     if isinstance(value, str):
#         idata = int(value)
#         if value < 0:
#             dd = "FFFFFFFF"
#             aa = int(dd, 16)
#             bb = value + 1
#             cc = aa + bb
#            # idata = hex(int(str(cc), 10))[2:].upper()
#             idata=cc
#         else:
#             idata = int(value)
#     elif isinstance(value, int) or isinstance(value, float):
#         if value < 0:
#             dd = "FFFFFFFF"
#             aa = int(dd, 16)
#             bb = value + 1
#             cc = aa + bb
#            # idata = hex(int(str(cc), 10))[2:].upper()
#             idata=cc
#         else:
#             idata = value
#     else:
#         print('valuetolongusingedbuff 未知值', value)
#     if scaler == 0:
#         sdata += numbertohex(idata, 8)
#     elif scaler == -1:
#         idata = int(idata*10)
#         sdata += numbertohex(idata, 8)
#     elif scaler == -2:
#         idata = int(idata*100)
#         sdata += numbertohex(idata, 8)
#     elif scaler == -3:
#         idata = int(idata*1000)
#         sdata += numbertohex(idata, 8)
#     elif scaler == -4:
#         idata = int(idata*10000)
#         sdata += numbertohex(idata, 8)
#     else:
#         print('valuetolongusingedbuff 未知换算', scaler)
#         sdata += numbertohex(idata, 8)
#     return sdata







# '0000' -> '020000' 或 IP:"192.168.127.127"->"C0A87F7F"#王梦新增，增加IP组帧分支部分
def valuetooctetstringbuff(value):
    sdata = ''
    if isinstance(value, str):
        if value.find('.')>=0:#增加IP组帧分支部分
            value=value.split(".")
            ilen = len(value)
            sdata += numbertohex(int(ilen ), 2)
            for item in value:
                sdata += (hex(int(item))[2:]).zfill(2).upper()
        elif value.find(',')>=0 or value.find('-')>=0:
            sdata +=regiontotime(value)

        else:
            ilen = len(value)
            sdata += numbertohex(int(ilen / 2), 2)
            for i in range(0, ilen, 1):
                sdata += value[i * 2: i * 2 + 2]
    else:
        print('valuetooctetstringbuff excel 值类型错误', value)
        sdata += '00'
    return sdata

#王梦新增:ASCII转16进制
def AS_hex(ashex):
    e = 0  # 暂存结果
    for i in ashex:
        d = ord(i)  # 单个字符转换成ASCii码
        e = e * 256 + d  # 将单个字符转换成的ASCii码相连
    e = ("e:%x" % e)[2:].zfill(2)
    return e






#王梦新增
def valuetovisiblestringbuff(value,hoad):
    sdata = ''
    if isinstance(value, str):
        valuelase,ilen=visibletobuff(value)#使用 字节串转换函数bytes()进行数据转换
        if ilen>127:
            sdata+="81"
            sdata += numbertohex(int(ilen), 2)
        else:
            sdata += numbertohex(int(ilen), 2)
        sdata += valuelase




    else:
        print('valuetovisiblestringbuff excel 值类型错误', value)
        sdata += '00'
    return sdata

def valuetobitstringbuff(value):
    sdata = ''
    if isinstance(value, str):
        ilen = len(value)*4
        sdata += numbertohex(int(ilen), 2)
        sdata+=bitstrtohex(value)
    else:
        print('valuetobitstringbuff excel 值类型错误', value)
        sdata += '00'
    return sdata




# '05000000000003'-> '0705000000000003'
def valuetoTSAbuff(value):
    sdata = ''
    if isinstance(value, str):
        ilen = len(value)
        sdata += numbertohex(int(ilen/2), 2)
        for i in range(0, ilen, 1):
            sdata += value[i*2: i*2+2]
    else:
        print('valuetoTSAbuff excel 值类型错误', value)
        sdata += '00'
    return sdata

# publice function
def getkey(dd, value):
    sdata = ''
    for i, j in dd.items():
        # print('i,j', i, j, value)
        if j == value:
            sdata = i
            break
    # print('getkey', sdata)
    return sdata

# publice function '4'->True
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False


# '5分' ->01 0005
def valuetoTIbuff(value):
    sdata = ''
    ilen = len(value)
    sdata += getkey(EMUN_RATED, value[ilen-1:ilen+1])
    # print('valuetoTIbuff', value[0:ilen-1])
    sdata += valuetolongusingedbuff(value[0:ilen-1], 0)
    # print('valuetoTIbuff sdata', value, sdata)
    return sdata

# TI '15分' -> 01000F , RetryMetering[TI, long_unsigned] '5分,3'
def valuetofacjtypebuff(value):
    sdata = ''
    if isinstance(value, list):#王梦新增处理60147F00补抄的情况
        RetryMetering = value
        sdata += numbertohex(DT_structure, 2)
        sdata += numbertohex(len(RetryMetering), 2)
        if len(RetryMetering) == 2:
            sdata += numbertohex(DT_TI, 2)
            sdata += valuetoTIbuff(RetryMetering[0])
            sdata += numbertohex(DT_long_unsigned, 2)
            sdata += valuetolongusingedbuff(RetryMetering[1], 0)
        else:
            print('valuetofacjtypebuff RetryMetering 输入错误', value)
        pass
    elif is_number(value):
        sdata += numbertohex(DT_unsigned, 2)
        sdata += valuetounsignedbuff(value)
    elif value.find('NULL') >= 0:
        # print("valuetofacjtypebuff==", value.find('NULL'))
        sdata += '00'

    # TI
    elif (value.find('秒') > 0 or value.find('分') > 0 or value.find('时') > 0 or value.find('日') > 0 or \
            value.find('月') > 0 or value.find('年') > 0)and(value.find("[")<=0) :
        sdata += numbertohex(DT_TI, 2)
        sdata += valuetoTIbuff(value)
    #RetryMetering '5分,3'
    else:
        print('valuetofacjtypebuff 输入错误', value)
    return sdata

#王梦新增时间采集方案：采集内容Data处理（自己建的类型，eventtype）
def valuetoeventtypebuff(value):
    sdata = ''
    if str(value).find('NULL') >= 0:
        # print("valuetofacjtypebuff==", value.find('NULL'))
        sdata += '00'
    # array ROAD
    else:
        sdata += numbertohex(DT_array, 2)
        sdata += numbertohex(len(value), 2)
        for item in value:
            sdata += numbertohex(DT_ROAD, 2)
            sdata +=item[0]
            sdata += numbertohex(len(item[1]), 2)
            for item1 in item[1]:
                sdata += item1
    return sdata


#上报value:['60120300',['202A0200','60400200','60410200','60420200','50020200',['00100200','00200200'],'50020200',['20000200','20010200']],
#['选择方法7', ['20190727000000', '20190727235959','15分','全部用户地址']]]
def valuetoreporttypebuff(value):
    sdata = ''
    #区分上报类型 0  和  1(0：不是列表，1是列表，依此来区分)

    if isinstance(value, list):
        sdata += numbertohex(DT_structure, 2)
        sdata += numbertohex(3, 2)
        sdata += numbertohex(DT_OAD, 2)
        sdata += value[0]
        sdata += numbertohex(DT_RCSD, 2)
        sdata += valuetoRCSDbuff(value[1])
        sdata += numbertohex(DT_RSD, 2)
        sdata += makeRSDbuff(value[2])
    # array ROAD
    else:
        sdata += numbertohex(DT_OAD, 2)
        sdata += value
    return sdata


# 'MS' '一组用户地址,05000000000003'  ->buff
def valuetoMSbuff(value):
    sdata = ''
    if value.find("["):#王梦新增：修改MS处理类型：新增03,04,05,06,07.
        tMS = value.replace("]","").split(",[")
        # sdata += numbertohex(len(tMS[1].split(",")), 2)
    else:
        print("MS增加区间类处理")
    iMS = getkey(CHOICE_MS, tMS[0])
    sdata += iMS
    # sdata +=numbertohex(len(tMS[1].split(",")), 2)

    if iMS == '00' or iMS == '01':
        pass
    # '一组用户类型,2'->
    elif iMS == '02' and len(tMS) == 2:
        tMS1len=tMS[1].strip(",").split(",")
        sdata += numbertohex(len(tMS1len), 2)
        for item in tMS[1].strip(",").split(","):
            if is_number(item):
                sdata += numbertohex(int(item), 2)
            else:
                print('valuetoMSbuff iMS=', iMS, value)
    # '一组用户地址,05000000000003'->
    elif iMS == '03' and len(tMS) == 2:
        tMS1len = tMS[1].strip(",").split(",")
        sdata += numbertohex(len(tMS1len), 2)
        for item in tMS[1].strip(",").split(","):
            sdata += valuetoTSAbuff(item)
    # '一组用户地址,05000000000003'->
    elif iMS == '04' and len(tMS) == 2:
        tMS1len = tMS[1].strip(",").split(",")
        sdata += numbertohex(len(tMS1len), 2)
        for item in tMS[1].strip(",").split(","):
            if is_number(item):
                sdata += valuetolongusingedbuff(int(item), 0)
            else:
                print('valuetoMSbuff iMS=', iMS, value)

    elif iMS == '05'or iMS == '06'or iMS == '07' :
        cc = tMS[1:]
        # print("这是区间的个数：" + str(len(cc)))
        sdata += numbertohex(len(cc), 2)
        for item in cc:
            dd = item.split(",")
            # print(dd[0])
            enumzhuanhuan = makeRegion(int(dd[0]))
            # print("这是区间类型：" + enumzhuanhuan)
            sdata += enumzhuanhuan
            if tMS[0] == "一组用户类型区间":
                sdata += numbertohex(DT_unsigned, 2)
                sdata += numbertohex(int(dd[1]), 2)
                sdata += numbertohex(DT_unsigned, 2)
                sdata += numbertohex(int(dd[2]), 2)
            elif tMS[0] == "一组用户地址区间":
                sdata += numbertohex(DT_TSA, 2)
                sdata += valuetoTSAbuff(dd[1])
                sdata += numbertohex(DT_TSA, 2)
                sdata += valuetoTSAbuff(dd[2])
            elif tMS[0] == "一组配置序号区间":
                sdata += numbertohex(DT_long_unsigned, 2)
                sdata += valuetolongusingedbuff(int(dd[1]), 0)
                sdata += numbertohex(DT_long_unsigned, 2)
                sdata += valuetolongusingedbuff(int(dd[2]), 0)


    else:
        print('valuetoMSbuff 未知', iMS, value)
    return sdata


#valuetodoublebuff(value)：王梦新增10进制转16进制（1111111->0010F447）
def valuetodoublebuff(value,scaler):
    sdata = ''
    idata = float(str(value))
    if scaler == 0:
        idata = int(idata)
    elif scaler == -1:
        idata = int(idata * 10)
    elif scaler == -2:
        idata = int(idata * 100)
    elif scaler == -3:
        idata = int(idata * 1000)
    elif scaler == -4:
        idata = int(idata * 10000)
    else:
        print('valuetolongusingedbuff 未知换算', scaler)
    print('idata:',idata)
    ss = hex(idata)[2:]
    sdata = ss.zfill(8).upper()
    return sdata


#['20000200', '00300200']
def valuetoDTCSDbuff(value):
    sdata = ''
    # print("valuetoDTCSDbuff===",value)
    iarray = 0
    if isinstance(value, list):
        ilen = len(value)
        for i in range(0, ilen, 1):
            # print("value", value[i], i)
            if i == 0 and isinstance(value[i], list):
                print('valuetoDTCSDbuff CSD 输入错误', value)
                continue
            if i < ilen-1:
                if isinstance(value[i], list):
                    pass
                elif isinstance(value[i], str) and isinstance(value[i + 1], str):
                    sdata += numbertohex(DT_CSD, 2)
                    sdata += '00'
                    sdata += value[i]
                    iarray += 1
                elif isinstance(value[i], str) and isinstance(value[i + 1], list):
                    sdata += numbertohex(DT_CSD, 2)
                    sdata += '01'
                    sdata += value[i]
                    iROAD = len(value[i + 1])
                    sdata += numbertohex(iROAD, 2)
                    for j in range(0, iROAD, 1):
                        sdata += value[i + 1][j]
                    iarray += 1
            elif i == ilen-1:
                if isinstance(value[i], list):
                    pass
                elif isinstance(value[i], str):
                    sdata += numbertohex(DT_CSD, 2)
                    sdata += '00'
                    sdata += value[i]
                    iarray += 1
        sdata = numbertohex(iarray, 2) + sdata
        # print('sdata=', sdata)
    #考虑，CSD不是列表的情况，可能会影响以前流程，需关注。
    elif isinstance(value, str):
        sdata += numbertohex(DT_CSD, 2)
        sdata += '00'
        sdata += value
    else:
        print('valuetoDTCSDbuff输入值错误 非list', value)
    return sdata


# dtype 数据类型，value数值 ->buff   原不考虑换算流程！！！
def makebydatatype(dtype, value):
    bdata = ''
    if dtype == DT_NULL:
        bdata += ''
    elif dtype == DT_bool:
        bdata += valuetoboolbuff(value)
    elif dtype == DT_unsigned or dtype == DT_enum:
         if ( isinstance(value, str))and(value.find("_")) >=0:
             bb = value.split("_")
             cc = bin(int(bb[1], 10))[2:]
             dd = bin(int(bb[0], 10))[2:]
             ee = str(cc) + str(dd)
             bdata+=str( hex(int(ee, 2))[2:])
         elif( isinstance(value, str)) and((value.find(",")) >=0):#王梦新增：终端工控人视化转为机器识别（02020101->01011010）
             bdata+=mantobin(value)
         else:
             bdata += valuetounsignedbuff(value)
    elif dtype == DT_integer:
        bdata += inttohex(value)
    elif dtype == DT_date_time_s:
        bdata += valuetodtsbuff(value)
        #王梦新增
    elif dtype == DT_time:
        bdata += valuetotbuff(value)

    elif dtype == DT_long_unsigned:
        bdata += valuetolongusingedbuff(value, 0)
    elif dtype == DT_double_long:#王梦新增：考虑到传入参数为负数的情况（DT_long可参考改流程）
        bdata += valuetodoublelongbuff(value, 0)
    elif dtype == DT_long:  # 王梦新增：考虑到传入参数为负数的情况（DT_long可参考改流程）
        bdata += valuetolongbuff(value, 0)
    elif dtype == DT_long64:  # 王梦新增：考虑到传入参数为负数的情况（DT_long可参考改流程）
        bdata += valuetolong64buff(value, 0)

    elif dtype == DT_OAD:
        bdata += value
    elif dtype == DT_TSA:
        bdata += valuetoTSAbuff(value)
    elif dtype == DT_octet_string:
        bdata += valuetooctetstringbuff(value)
    elif dtype == DT_visible_string:  # 王梦新增
        bdata += valuetovisiblestringbuff(value,0)
    elif dtype == DT_bit_string:  # 王梦新增
        bdata += valuetobitstringbuff(value)
    elif dtype == DT_TI:
        bdata += valuetoTIbuff(value)
    elif dtype == DT_facjtype:
        bdata += valuetofacjtypebuff(value)
        # print('makebydatatype 完成处理类型DT_facjtype==', dtype, value, bdata)
    elif dtype == DT_eventtype:
        bdata += valuetoeventtypebuff(value)
    elif dtype == DT_MS:
        bdata += valuetoMSbuff(value)
    elif dtype == DT_reporttype:
        bdata += valuetoreporttypebuff(value)
    elif dtype == DT_MS:
        bdata += valuetoMSbuff(value)
    elif dtype == DT_double_long_unsigned:
        bdata += valuetodoublebuff(value,0)


    elif dtype == DT_CSD:
        bdata += valuetoDTCSDbuff(value)
    elif dtype == DT_OI:
        bdata += value

    else:
        print('makebydatatype 增加处理类型', dtype, value)
    return bdata


# 王梦新增：复制上面的流程，给函数多传一个需要进行换算的OAD。dtype 数据类型，value数值 ->buff  hoad：标识，是换算的依据
def makebyhoaddatatype(dtype, value,hoad):
    bdata = ''
    if dtype == DT_NULL:
        bdata += ''
    elif dtype == DT_bool:
        bdata += valuetoboolbuff(value)
    elif dtype == DT_unsigned or dtype == DT_enum:
         if ( isinstance(value, str))and(value.find("_")) >=0:
             bb = value.split("_")
             cc = bin(int(bb[1], 10))[2:]
             dd = bin(int(bb[0], 10))[2:]
             ee = str(cc) + str(dd)
             bdata+=str( hex(int(ee, 2))[2:])
         elif( isinstance(value, str)) and((value.find(",")) >=0):#王梦新增：终端工控人视化转为机器识别（02020101->01011010）
             bdata+=mantobin(value)
         else:
             bdata += valuetounsignedbuff(value)
    elif dtype == DT_integer:
        bdata += inttohex(value)
    elif dtype == DT_date_time_s:
        if hoad[:4]=="8104":
            bdata += valueto8104specialdtsbuff(value)
        elif hoad[:4]=="8105":
            bdata += valueto8105specialdtsbuff(value)
        elif (hoad=="40090200") or (hoad=="40080200")or (hoad=="400A0200")or (hoad=="400B0200"):
            bdata += valueto4009specialdtsbuff(value)
        else:
            bdata += valuetodtsbuff(value)
        #王梦新增
    elif dtype == DT_time:
        bdata += valuetotbuff(value)

    elif dtype == DT_long_unsigned:
        if hoad[:4] in SCALER_UNIT_4 or (hoad in SCALER_UNIT_4 ):
            hoad=-4
        elif hoad[:4] in SCALER_UNIT_3:
            hoad = -3
        elif hoad[:4] in SCALER_UNIT_2:
            hoad = -2
        elif (hoad[:4] in SCALER_UNIT_1) or (hoad in long_usigned_scalerlist ) :
            hoad = -1
        else:hoad = 0

        bdata += valuetolongusingedbuff(value, hoad)
    elif dtype == DT_double_long:#王梦新增：考虑到传入参数为负数的情况（DT_long可参考改流程）
        if (hoad[:4] in SCALER_UNIT_4)  or (hoad in double_long_scalerlist ) or (hoad in SCALER_UNIT_4)   :
            hoad=-4
        elif hoad[:4] in SCALER_UNIT_3:
            hoad = -3
        elif hoad[:4] in SCALER_UNIT_2:
            hoad = -2
        elif hoad[:4] in SCALER_UNIT_1 or (hoad in double_long_1_scalerlist):
            hoad = -1
        else:hoad = 0
        bdata += valuetodoublelongbuff(value, hoad)
    elif dtype == DT_long:#王梦新增：考虑到传入参数为负数的情况
        if (hoad[:4] in SCALER_UNIT_4) or (hoad in SCALER_UNIT_4) :
            hoad=-4
        elif hoad[:4] in SCALER_UNIT_3:
            hoad = -3
        elif hoad[:4] in SCALER_UNIT_2 or hoad == '301E0600' :
            hoad = -2
        elif hoad[:4] in SCALER_UNIT_1 or hoad == '300C0600'or hoad == '301D0600' or hoad == '303B0500':
            hoad = -1
        else:hoad = 0
        bdata += valuetolongbuff(value, hoad)
    elif dtype == DT_long64:  # 王梦新增：考虑到传入参数为负数的情况
        if (hoad[:4] in SCALER_UNIT_4 ) or (hoad[:4] in SPESCALER_4) or (hoad in SPESCALER_4 ):
            hoad = -4
        elif hoad[:4] in SCALER_UNIT_3:
            hoad = -3
        elif hoad[:4] in SCALER_UNIT_2:
            hoad = -2
        elif hoad[:4] in SCALER_UNIT_1:
            hoad = -1
        else:
            hoad = 0
        bdata += valuetolong64buff(value, hoad)


    elif dtype == DT_OAD:
        bdata += value
    elif dtype == DT_TSA:
        bdata += valuetoTSAbuff(value)
    elif dtype == DT_octet_string:
        bdata += valuetooctetstringbuff(value)
    elif dtype == DT_visible_string:  # 王梦新增：需要汉字转16进制的数据标识需要单独传进来，否则无法判断参数中是否有中文，不知道走哪个分支。
        bdata += valuetovisiblestringbuff(value,hoad)


    elif dtype == DT_TI:
        bdata += valuetoTIbuff(value)
    elif dtype == DT_facjtype:
        bdata += valuetofacjtypebuff(value)
        # print('makebydatatype 完成处理类型DT_facjtype==', dtype, value, bdata)
    elif dtype == DT_eventtype:
        bdata += valuetoeventtypebuff(value)
    elif dtype == DT_MS:
        bdata += valuetoMSbuff(value)
    elif dtype == DT_double_long_unsigned:#王梦新增，考虑换算（同一个标识，不同换算，把具体的标识列出来）
        if hoad=="80000200" or hoad=="301F0600" or (hoad in double_long_unsignedlist):
            hoad = -4
        else:
            hoad=0
        bdata += valuetodoublebuff(value,hoad)

    elif dtype == DT_CSD:
        bdata += valuetoDTCSDbuff(value)
    elif dtype == DT_OI:
        bdata += value
    elif dtype == DT_bit_string:  # 王梦新增
        bdata += valuetobitstringbuff(value)
    elif dtype == DT_float32:  # 王梦新增
        if (hoad[:4] in SCALER_UNIT_4 ) or (hoad[:4] in SPESCALER_4) or (hoad in SPESCALER_4 ):
            hoad = -4
        elif hoad[:4] in SCALER_UNIT_3:
            hoad = -3
        elif hoad[:4] in SCALER_UNIT_2:
            hoad = -2
        elif hoad[:4] in SCALER_UNIT_1:
            hoad = -1
        else:
            hoad = 0
        bdata += valuetofloat32buff(value,hoad)
    else:
        print('makebyhoaddatatype 增加处理类型', dtype, value)
    return bdata

#孙 接口函数通过序号的形式选择参数
def excelnumselect(param,paramexecel,oad):
    paramreal = ""
    selectnum = []
    selectnum = settollist(param,'')
    for item in selectnum:
        paramreal += paramexecel[int(item)] + ','
    #不是array--->structure类型的，不需要加最外层的中括号。等处理到了，加入oad即可。
    if oad == "60187F00"  :
        param="[" +paramreal[:-1]+ "]"
    else:
        #数组类型的，需要最外层增加[]
        param = "[[" + paramreal[:-1] + "]]"
    param=strtolist(param)
    return param


# 组帧：依据oadoam= []  param [] 生成buff   Clienttype操作或者设置
def makebyoadvalue(oadoam, param,Clienttype):
    bdata = ''
    #以下为王梦新增流程：为了处理属性和方法标识相同的情况。如果标识相同，就通过传入Clienttype来区分是方法还是属性。
    if oadoam in SpecialOOPDY:
        # 如果是操作请求，oadoam就多加1位“1”，否则，目前只有设置一个对象属性的情况：加“0”。
        if Clienttype == Client_APDU_ACTION_Request:
            oadoam = oadoam + "1"
        elif param[:2] == '11':
            oadoam = oadoam + "1"
            param = param[2:]
        elif param[:2] == '16':
            oadoam = oadoam + "0"
            param = param[2:]
        else:
            oadoam = oadoam + "0"
    #以上为王梦新增
    if oadoam in OOPSXDY:
        bdata += numbertohex(OOPSXDY[oadoam][0], 2)#根据属性结构字（类似数据标识，来确定数据类型）例如：    '40000400': [DT_structure,[DT_unsigned, DT_unsigned, DT_unsigned, DT_unsigned, DT_unsigned]],
        if OOPSXDY[oadoam][0] == DT_date_time_s:
            bdata += makebyhoaddatatype(OOPSXDY[oadoam][0], param, oadoam)
        elif OOPSXDY[oadoam][0] == DT_enum:
            bdata += makebydatatype(OOPSXDY[oadoam][0], param)

        elif OOPSXDY[oadoam][0] == DT_octet_string:#王梦新增流程
            bdata += makebydatatype(OOPSXDY[oadoam][0], param)

        elif OOPSXDY[oadoam][0] == DT_NULL:
            bdata += makebydatatype(OOPSXDY[oadoam][0], param)
        elif OOPSXDY[oadoam][0] == DT_structure:
            lparam = strtolist(param)
            if len(OOPSXDY[oadoam][1]) != len(lparam):
                bdata += numbertohex(0, 2)
                print('makebyoadvalue DT_structure excel对应输入参数有误:', param)
            else:
                bdata += numbertohex(len(OOPSXDY[oadoam][1]),2)
                if oadoam=="45000400":
                    for i in range(0, (len(OOPSXDY[oadoam][1]) - 1), 1):  # 王梦新增：修改len为len-1(为了对应数据结构的循环正确)
                        bdata += numbertohex(OOPSXDY[oadoam][1][i], 2)
                        if OOPSXDY[oadoam][1][i] in OOPSPDATA:
                            bdata += makebydatatype(OOPSXDY[oadoam][1][i], lparam[i])

                        elif OOPSXDY[oadoam][1][i] in OOPARRATDATA:
                            print('makebyoadvalue OOPARRATDATA 增加处理:', OOPSXDY[oadoam][1][i], param[i])
                        # 以下为王梦新增：写参数时，要合理利用表格中的数据，来确定传入的具体数据和数据个数
                        elif isinstance(OOPSXDY[oadoam][1][i], list):  # 这个elif为王梦新增流程：处理450000400
                            if OOPSXDY[oadoam][1][i][0] == DT_array:
                                for j in range(1, (len(OOPSXDY[oadoam][1][i]) + 1), 1):
                                    bdata += numbertohex(OOPSXDY[oadoam][1][j][0], 2)
                                    bdata += numbertohex(len(lparam[j]), 2)
                                    for item in lparam[j]:
                                        if OOPSXDY[oadoam][1][j][1][0] in OOPSPDATA:
                                            bdata += numbertohex(OOPSXDY[oadoam][1][j][1][0], 2)
                                            bdata += makebydatatype(OOPSXDY[oadoam][1][j][1][0], item)

                                        else:
                                            print('makebyoadvalue [oadoam][1][i][1][0] 增加处理:', OOPSXDY[oadoam][1][i],
                                                  param)



                            else:
                                print('makebyoadvalue OOPSXDY[oadoam][1][i][0] 增加处理:', OOPSXDY[oadoam][1][j][0], param)

                        else:
                            print(''
                                  '  增加处理:', OOPSXDY[oadoam][1][i], param[i])
                else:#原流程
                    for i in range(0, len(OOPSXDY[oadoam][1]) , 1):
                        if isinstance(OOPSXDY[oadoam][1][i], list):
                            bdata += numbertohex(OOPSXDY[oadoam][1][i][0], 2)#王梦新增（F2007F00）这里加了数据类型（数组和结构体），故后面数据和结构体，不可以再加数据类型，否则会出现数据类型多加一次。
                        else:
                            bdata += numbertohex(OOPSXDY[oadoam][1][i], 2)
                        if OOPSXDY[oadoam][1][i] in OOPSPDATA:
                            bdata += makebyhoaddatatype(OOPSXDY[oadoam][1][i], lparam[i],oadoam)
                        elif isinstance(OOPSXDY[oadoam][1][i], list):
                            if OOPSXDY[oadoam][1][i][0] == DT_array:
                                # bdata += numbertohex(OOPSXDY[oadoam][1][i][0], 2)
                                bdata += numbertohex(len(lparam[i]), 2)
                                for item11 in lparam[i]:  # 王梦新增：补充array循环，只要是array类型，必须考虑到有多个相同数据项的循环处理问题。
                                    # if len(item11) == 0:
                                    #     pass
                                    if OOPSXDY[oadoam][1][i][1][0] in OOPSPDATA:
                                        bdata += numbertohex(OOPSXDY[oadoam][1][i][1][0], 2)
                                        bdata += makebydatatype(OOPSXDY[oadoam][1][i][1][0], item11)
                                    elif OOPSXDY[oadoam][1][i][1][0] == DT_Region:#区间统计
                                        bdata += numbertohex(OOPSXDY[oadoam][1][i][1][0], 2)
                                        bdata += makeRegion(item11[0])
                                        bdata += numbertohex((makeOadtotype(lparam[0])), 2)
                                        bdata += makebyhoaddatatype((makeOadtotype(lparam[0])), item11[1],lparam[0])#王梦新增，通过关联属性OAD找到对应数据类型，进行数据处理，组帧
                                        bdata += numbertohex((makeOadtotype(lparam[0])), 2)
                                        bdata += makebyhoaddatatype((makeOadtotype(lparam[0])), item11[2],lparam[0])
                                        #60187F00 王梦新增：：： 参数格式复杂，要考虑全面
                                    elif OOPSXDY[oadoam][1][i][1][0] == DT_structure:
                                        if len(OOPSXDY[oadoam][1][i][1][1]) != len(lparam[i][0]):
                                            bdata += numbertohex(0, 2)
                                            print('makebyoadvalue DT_structure excel对应输入参数有误:', param[i][0])
                                        else:
                                            bdata += numbertohex(OOPSXDY[oadoam][1][i][1][0], 2)
                                            bdata += numbertohex(len(OOPSXDY[oadoam][1][i][1][1]), 2)
                                        for j in range(0, len(OOPSXDY[oadoam][1][i][1][1]), 1):
                                            if isinstance(OOPSXDY[oadoam][1][i][1][1][j], list):
                                                bdata += numbertohex(OOPSXDY[oadoam][1][i][1][1][j][0], 2)
                                            else:
                                                bdata += numbertohex(OOPSXDY[oadoam][1][i][1][1][j], 2)
                                            if OOPSXDY[oadoam][1][i][1][1][j] in OOPSPDATA:
                                                bdata += makebyhoaddatatype(OOPSXDY[oadoam][1][i][1][1][j], item11[j], oadoam)
                                            elif isinstance(OOPSXDY[oadoam][1][i][1][1][j], list):
                                                if OOPSXDY[oadoam][1][i][1][1][j][0] == DT_array:
                                                    # bdata += numbertohex(OOPSXDY[oadoam][1][i][1][1][j][0], 2)
                                                    bdata += numbertohex(len(lparam[i][0][j]), 2)
                                                    # for item111 in lparam[i][0][j]:  # 王梦新增：补充array循环，只要是array类型，必须考虑到有多个相同数据项的循环处理问题。
                                                    for item111 in item11[j]:  # 王梦新增：补充array循环，只要是array类型，必须考虑到有多个相同数据项的循环处理问题。


                                                        # if len(item11) == 0:
                                                        #     pass
                                                        if OOPSXDY[oadoam][1][i][1][1][j][1][0] in OOPSPDATA:  # 王梦新增：之前调通的流程，没有考虑array类型为列表，加了一个break，后期调试，如有需求，可以调整流程,此处加了循环后，加了一个break，不回影响原流程，原流程可能需要扩展成循环的模式。
                                                            bdata += numbertohex(OOPSXDY[oadoam][1][i][1][1][j][1][0], 2)
                                                            bdata += makebydatatype(OOPSXDY[oadoam][1][i][1][1][j][1][0], item111)
                                                        elif OOPSXDY[oadoam][1][i][1][1][j][1][0] == DT_structure:
                                                            if len(OOPSXDY[oadoam][1][i][1][1][j][1][1]) != len( lparam[i][0][j][0]):

                                                                bdata += numbertohex(0, 2)
                                                                print('makebyoadvalue DT_structure excel对应输入参数有误:',  param[i][0][j][0])

                                                            else:
                                                                bdata += numbertohex(OOPSXDY[oadoam][1][i][1][1][j][1][0],2)
                                                                bdata += numbertohex(len(OOPSXDY[oadoam][1][i][1][1][j][1][1]), 2)

                                                            for k in range(0, len(OOPSXDY[oadoam][1][i][1][1][j][1][1]), 1):
                                                                if isinstance(OOPSXDY[oadoam][1][i][1][1][j][1][1][k], list):
                                                                    bdata += numbertohex(OOPSXDY[oadoam][1][i][1][1][j][1][1][k][0], 2)

                                                                else:
                                                                    bdata += numbertohex( OOPSXDY[oadoam][1][i][1][1][j][1][1][k], 2)
                                                                if OOPSXDY[oadoam][1][i][1][1][j][1][1][k] in OOPSPDATA:
                                                                    bdata += makebyhoaddatatype( OOPSXDY[oadoam][1][i][1][1][j][1][1][k],item111[k], oadoam)
                                                        else:
                                                            print('makebyoadvalue OOPARRATDATA 增加处理:',OOPSXDY[oadoam][1][i], param[i])

                                                elif OOPSXDY[oadoam][1][i][1][1][j][0] == DT_structure:
                                                     if len(OOPSXDY[oadoam][1][i][1][1][j][1]) != len(lparam[i][0][j]):
                                                         bdata += numbertohex(0, 2)
                                                         print('makebyoadvalue DT_structure excel对应输入参数有误:', param[i][0])

                                                     else:
                                                         bdata += numbertohex(len(OOPSXDY[oadoam][1][i][1][1][j][1]), 2)
                                                     for n in range(0, len(OOPSXDY[oadoam][1][i][1][1][j][1]), 1):
                                                         if isinstance(OOPSXDY[oadoam][1][i][1][1][j][1][n], list):
                                                             bdata += numbertohex(OOPSXDY[oadoam][1][i][1][1][j][1][n][0], 2)
                                                         else:
                                                             bdata += numbertohex(OOPSXDY[oadoam][1][i][1][1][j][1][n], 2)
                                                         if OOPSXDY[oadoam][1][i][1][1][j][1][n] in OOPSPDATA:
                                                             bdata += makebyhoaddatatype(OOPSXDY[oadoam][1][i][1][1][j][1][n],item11[j][n], oadoam)
                                                         elif OOPSXDY[oadoam][1][i][1][1][j][1][n][0] == DT_structure:
                                                             if len(OOPSXDY[oadoam][1][i][1][1][j][1][n][1]) != len( lparam[i][0][j][n]):
                                                                 bdata += numbertohex(0, 2)
                                                                 print('makebyoadvalue DT_structure excel对应输入参数有误:',param[i][0][j][n])
                                                             else:
                                                                 bdata += numbertohex(len(OOPSXDY[oadoam][1][i][1][1][j][1][n][1]), 2)
                                                             for m in range(0, len(OOPSXDY[oadoam][1][i][1][1][j][1][n][1]),1):
                                                                 if isinstance(OOPSXDY[oadoam][1][i][1][1][j][1][n][1][m],list):
                                                                     bdata += numbertohex(OOPSXDY[oadoam][1][i][1][1][j][1][n][1][m][0], 2)
                                                                 else:
                                                                     bdata += numbertohex(OOPSXDY[oadoam][1][i][1][1][j][1][n][1][m], 2)
                                                                 if OOPSXDY[oadoam][1][i][1][1][j][1][n][1][m] in OOPSPDATA:
                                                                     bdata += makebyhoaddatatype(OOPSXDY[oadoam][1][i][1][1][j][1][n][1][m],item11[j][n][m], oadoam)
                                    elif OOPSXDY[oadoam][1][i][1][0] == DT_CSD:
                                        bdata = bdata[:-2]
                                        bdata += makebydatatype(OOPSXDY[oadoam][1][i][1][0], lparam[i])
                                        break







                                    #以上王梦新增，调试60187F00
                                    else:
                                        print('makebyoadvalue OOPARRATDATA 增加处理:', OOPSXDY[oadoam][1][i], param[i])
                                        # 40040200

                            elif OOPSXDY[oadoam][1][i][0] == DT_structure:
                                # bdata += numbertohex(OOPSXDY[oadoam][1][i][0], 2)
                                bdata += numbertohex(len(OOPSXDY[oadoam][1][i][1]), 2)
                                if len(OOPSXDY[oadoam][1][i][1]) == 0:
                                    print('pass1')
                                    pass
                                elif len(OOPSXDY[oadoam][1][i][1]) == len(lparam[i]):
                                    for j in range(0, len(OOPSXDY[oadoam][1][i][1]), 1):
                                        bdata += numbertohex(OOPSXDY[oadoam][1][i][1][j], 2)
                                        if OOPSXDY[oadoam][1][i][1][j] in OOPSPDATA:
                                            bdata += makebyhoaddatatype(OOPSXDY[oadoam][1][i][1][j], lparam[i][j],oadoam)
                                        elif OOPSXDY[oadoam][1][i][1][j][0] == DT_structure:
                                            bdata += numbertohex(OOPSXDY[oadoam][1][i][1][j][0],2)
                                            bdata += numbertohex(len(OOPSXDY[oadoam][1][i][1][j][1]), 2)
                                            if len(OOPSXDY[oadoam][1][i][1][j][1]) == 0:
                                                print('pass1')
                                                pass
                                            elif len(OOPSXDY[oadoam][1][i][1][j][1]) == len(lparam[i][j]):
                                                for j1 in range(0, len(OOPSXDY[oadoam][1][i][1][j][1]), 1):
                                                    bdata += numbertohex(OOPSXDY[oadoam][1][i][1][j][1][j1], 2)
                                                    if OOPSXDY[oadoam][1][i][1][j][1][j1] in OOPSPDATA:
                                                        # print('dd', OOPSXDY[oadoam][1][1][i][1][j], item[i][j])
                                                        bdata += makebyhoaddatatype(OOPSXDY[oadoam][1][i][1][j][1][j1],lparam[i][j][j1],oadoam)
                                                    else:
                                                        print(
                                                            'makebyoadvalue OOPSXDY[oadoam][[1][i][1][j][1][j1] in OOPARRATDATA',
                                                            OOPSXDY[oadoam][1][i][1][j][1][j1])
                                        else:
                                            print('makebyoadvalue OOPSXDY[oadoam][1][i][1][j] in OOPVSDATA',OOPSXDY[oadoam][1][i][1][j])


                            elif OOPSXDY[oadoam][1][i][0] == DT_COMDCB:  # 串口控制块
                                bdata +=hex(int(getkey(CHOICE_BR, lparam[i][0]),10)) [2:].zfill(2)
                                bdata += getkey(CHOICE_CRC, lparam[i][1])
                                bdata += getkey(CHOICE_DATA, lparam[i][2])
                                bdata += getkey(CHOICE_STOP, lparam[i][3])
                                bdata += getkey(CHOICE_CTRO, lparam[i][4])




#以上

                            else:
                                print('makebyoadvalue OOPARRATDATA 增加处理:', OOPSXDY[oadoam][1][i], param[i])
                        elif OOPSXDY[oadoam][1][i] in OOPARRATDATA:
                            print('makebyoadvalue OOPARRATDATA 增加处理:', OOPSXDY[oadoam][1][i], lparam[i])
                        elif OOPSXDY[oadoam][1][i] == DT_CSD:
                            bdata = bdata[:-2]
                            bdata += makebydatatype(OOPSXDY[oadoam][1][i], lparam[i])

                        else:
                            print('makebyoadvalue DT_structure/DT_array  增加处理:', OOPSXDY[oadoam][1][i], param[i])




        # 以上为王梦新增：

        elif OOPSXDY[oadoam][0] == DT_array:
            lparam = strtolist(param)
            bdata += numbertohex(len(lparam), 2)
            if len(lparam) == 0:
                print('DT_array为空  或  makebyoadvalue DT_array excel 111对应输入参数有误:', param)
            else:
                if OOPSXDY[oadoam][1][0] in OOPSPDATA:
                    for item in lparam:
                        bdata += numbertohex(OOPSXDY[oadoam][1][0], 2)
                        bdata += makebyhoaddatatype(OOPSXDY[oadoam][1][0], item,oadoam)
                elif OOPSXDY[oadoam][1][0] == DT_structure:
                    for item in lparam:
                        bdata += numbertohex(OOPSXDY[oadoam][1][0], 2)
                        bdata += numbertohex(len(item), 2)
                        if len(item) == 0:
                            pass
                        elif len(OOPSXDY[oadoam][1][1]) != len(item):
                            print('makebyoadvalue DT_array excel 222对应输入参数有误:', param)
                        else:
                            for i in range(0, len(OOPSXDY[oadoam][1][1]), 1):
                                # print('OOPSXDY[oadoam][1][1][i]==', OOPSXDY[oadoam][1][1][i])
                                if isinstance(OOPSXDY[oadoam][1][1][i], list):
                                    if OOPSXDY[oadoam][1][1][i][0] == DT_structure:
                                        bdata += numbertohex(OOPSXDY[oadoam][1][1][i][0], 2)
                                        bdata += numbertohex(len(item[i]), 2)
                                        if len(item[i]) == 0:
                                            print('pass1')
                                            pass
                                        elif len(OOPSXDY[oadoam][1][1][i][1]) == len(item[i]):
                                            for j in range(0, len(OOPSXDY[oadoam][1][1][i][1]), 1):
                                                bdata += numbertohex(OOPSXDY[oadoam][1][1][i][1][j], 2)
                                                if OOPSXDY[oadoam][1][1][i][1][j] in OOPSPDATA:
                                                    # print('dd', OOPSXDY[oadoam][1][1][i][1][j], item[i][j])
                                                    bdata += makebyhoaddatatype(OOPSXDY[oadoam][1][1][i][1][j], item[i][j],oadoam)
                                                elif OOPSXDY[oadoam][1][1][i][1][j] in OOPARRATDATA:
                                                    print(
                                                        'makebyoadvalue OOPSXDY[oadoam][1][1][i][1][j] in OOPARRATDATA',
                                                        OOPSXDY[oadoam][1][1][i][1][j])
                                                    #上报方案
                                                elif OOPSXDY[oadoam][1][1][i][1][j] in OOPVSDATA:
                                                    bdata = bdata[:-2]
                                                    bdata += makebydatatype(OOPSXDY[oadoam][1][1][i][1][j], item[i][j])

                                                elif isinstance(OOPSXDY[oadoam][1][1][i][1][j], list):
                                                    if OOPSXDY[oadoam][1][1][i][1][j][0] == DT_array:
                                                        bdata += numbertohex(OOPSXDY[oadoam][1][1][i][1][j][0], 2)
                                                        bdata += numbertohex(len(item[i][j]), 2)
                                                        for item1 in item[i][j]:
                                                            if OOPSXDY[oadoam][1][1][i][1][j][1][0] in OOPSPDATA:
                                                                bdata += numbertohex(
                                                                    OOPSXDY[oadoam][1][1][i][1][j][1][0], 2)
                                                                bdata += makebydatatype(OOPSXDY[oadoam][1][1][i][1][j][1][0], item1)
                                                            elif OOPSXDY[oadoam][1][1][i][1][j][1][0] == DT_structure:
                                                                bdata += numbertohex(OOPSXDY[oadoam][1][1][i][1][j][1][0], 2)
                                                                bdata += numbertohex(len(OOPSXDY[oadoam][1][1][i][1][j][1][1]), 2)
                                                                # print('OOPSXDY[oadoam][1][1][i][1][j][1][1]',OOPSXDY[oadoam][1][1][i][1][j][1][1])
                                                                if len(OOPSXDY[oadoam][1][1][i][1][j][1][1]) == 0:
                                                                    pass
                                                                elif len(OOPSXDY[oadoam][1][1][i][1][j][1][1]) == len(item1):
                                                                    for k in range(0, len(OOPSXDY[oadoam][1][1][i][1][j][1][1]), 1):
                                                                        if OOPSXDY[oadoam][1][1][i][1][j][1][1][k] in OOPSPDATA:
                                                                            bdata += numbertohex(
                                                                                OOPSXDY[oadoam][1][1][i][1][j][1][1][k], 2)
                                                                            bdata += makebydatatype(
                                                                                OOPSXDY[oadoam][1][1][i][1][j][1][1][k],
                                                                                item1[k])
                                                                        else:
                                                                            print(
                                                                                'OOPSXDY[oadoam][1][1][i][1][j][1][1][k] 2',
                                                                                OOPSXDY[oadoam][1][1][i][1][j][1][1][k])
                                                                else:
                                                                    print('OOPSXDY[oadoam][1][1][i][1][j][1][1][k] 2',
                                                                          OOPSXDY[oadoam][1][1][i][1][j][1][1][k])
                                                    else:
                                                        print(
                                                            'makebyoadvalue OOPSXDY[oadoam][1][1][i][1][j][0]',
                                                            OOPSXDY[oadoam][1][1][i][1][j][0], item[i][j])
                                                elif OOPSXDY[oadoam][1][1][i][1][j] in OOPVSDATA:
                                                    bdata = bdata[:-2]
                                                    bdata +=  makebydatatype(OOPSXDY[oadoam][1][1][i][1][j], item[i][j])
                                                    # print("OOPSXDY[oadoam][1][1][i][1][j] in OOPVSDATA", OOPSXDY[oadoam][1][1][i][1][j], item[i][j])
                                                else:
                                                    print(
                                                        'makebyoadvalue OOPSXDY[oadoam][1][1][i][1][j] else',
                                                        OOPSXDY[oadoam][1][1][i][1][j], item[i][j])
                                        else:
                                            print('makebyoadvalue OOPSXDY[oadoam][1][1][i][1][j] else 111')
                                    elif OOPSXDY[oadoam][1][1][i][0] == DT_array:
                                        bdata += numbertohex(OOPSXDY[oadoam][1][1][i][0], 2)
                                        bdata += numbertohex(len(item[i]), 2)
                                        for item11 in item[i]:#王梦新增：补充array循环，只要是array类型，必须考虑到有多个相同数据的处理循环。
                                            # if len(item11) == 0:
                                            #     pass
                                            # elif len(OOPSXDY[oadoam][1][1][i][1]) == len(item11):流程已完善，不需要该分支
                                            #     print('makebyoadvalue OOPSXDY[oadoam][1][1][i][0]', item11)
                                            if OOPSXDY[oadoam][1][1][i][1][0] == DT_CSD:#王梦新增：修改流程：当为DT_CSD类型时，比较特殊(已在具体数据类型处理中做了本该在此做的循环)，不需要再继续循环。
                                                bdata = bdata[:-2]
                                                bdata += makebydatatype(OOPSXDY[oadoam][1][1][i][1][0], item[i])
                                                break
                                                # print('OOPSXDY[oadoam][1][1][i][1][0]==DT_CSD:',OOPSXDY[oadoam][1][1][i][1][0], item[i])

                                            elif OOPSXDY[oadoam][1][1][i][1][0] == DT_structure:  # 王梦新增：处理45200200

                                                # 以下111
                                                bdata += numbertohex(OOPSXDY[oadoam][1][1][i][1][0], 2)
                                                bdata += numbertohex(len(OOPSXDY[oadoam][1][1][i][1][1]), 2)
                                                if len(item11) == 0:
                                                    print('pass1')
                                                    pass
                                                elif len(OOPSXDY[oadoam][1][1][i][1][1]) == len(item11):
                                                    for j in range(0, len(OOPSXDY[oadoam][1][1][i][1][1]), 1):
                                                        bdata += numbertohex(OOPSXDY[oadoam][1][1][i][1][1][j], 2)
                                                        if OOPSXDY[oadoam][1][1][i][1][1][j] in OOPSPDATA:
                                                            # print('dd', OOPSXDY[oadoam][1][1][i][1][j], item[i][j])
                                                            bdata += makebydatatype(OOPSXDY[oadoam][1][1][i][1][1][j], item11[j])

                                                        else:
                                                            print("OOPSXDY[oadoam][1][1][i][1][0]增加处理",OOPSXDY[oadoam][1][1][i][1][0], item[i])


                                                else:
                                                    print("OOPSXDY[oadoam][1][1][i][1]增加处理",OOPSXDY[oadoam][1][1][i][1], item[i])



                                                # 以
                                                #王梦新增  以下为了处理区间统计
                                            elif OOPSXDY[oadoam][1][1][i][1][0] == DT_Region:
                                                bdata += numbertohex(OOPSXDY[oadoam][1][1][i][1][0], 2)
                                                bdata +=makeRegion(item11[0])
                                                bdata += numbertohex((makeOadtotype(item[0])), 2)
                                                bdata += makebyhoaddatatype((makeOadtotype(item[0])), item11[1],item[0])
                                                bdata += numbertohex((makeOadtotype(item[0])), 2)
                                                bdata += makebyhoaddatatype((makeOadtotype(item[0])), item11[2],
                                                                            item[0])
                                            elif OOPSXDY[oadoam][1][1][i][1][0] == DT_OAD:
                                                bdata += numbertohex(OOPSXDY[oadoam][1][1][i][1][0], 2)
                                                bdata += makebydatatype(OOPSXDY[oadoam][1][1][i][1][0], item11)



                                            else:
                                                print('增加处理makebyoadvalue OOPSXDY[oadoam][1][1][i][1][0]',item11)
                                    else:
                                        print('增加处理makebyoadvalue OOPSXDY[oadoam][1][1][i][0]', OOPSXDY[oadoam][1][1][i][0])
                                elif OOPSXDY[oadoam][1][1][i] in OOPSPDATA:
                                    bdata += numbertohex(OOPSXDY[oadoam][1][1][i], 2)
                                    bdata += makebyhoaddatatype(OOPSXDY[oadoam][1][1][i], item[i],oadoam)
                                else:
                                    print('makebyoadvalue OOPSXDY[oadoam][1][1][i]] ddd', OOPSXDY[oadoam][1][1][i], item[i])
                elif OOPSXDY[oadoam][1][0] == DT_array:
                    lparam = strtolist(param)
                    bdata += numbertohex(len(lparam), 2)
                    bdata += numbertohex(len(lparam[0]), 2)
                    if OOPSXDY[oadoam][1][1][0]== DT_structure:
                        for i in range(0,len(lparam[0]),1):
                            bdata += numbertohex(OOPSXDY[oadoam][1][1][0], 2)
                            bdata += numbertohex(len(lparam[0][i]), 2)
                            if len(lparam[0]) == 0:
                                print('pass1')
                                pass
                            elif len(OOPSXDY[oadoam][1][1][1]) == len(lparam[0][i]):
                                for j in range(0, len(OOPSXDY[oadoam][1][1][1]), 1):
                                    bdata += numbertohex(OOPSXDY[oadoam][1][1][1][j], 2)
                                    if OOPSXDY[oadoam][1][1][1][j] in OOPSPDATA:
                                        # print('dd', OOPSXDY[oadoam][1][1][i][1][j], item[i][j])
                                        bdata += makebydatatype(OOPSXDY[oadoam][1][1][1][j], lparam[0][i][j])
                                    elif OOPSXDY[oadoam][1][1][1][j] in OOPARRATDATA:
                                        print(
                                            'makebyoadvalue OOPSXDY[oadoam][1][1][i][1][j] in OOPARRATDATA',
                                            OOPSXDY[oadoam][1][1][1][j])
                else:
                    print('makebyoadvalue DT_array其他参数类型处理', param)
        elif OOPSXDY[oadoam][0] == DT_bool:
            bdata += makebydatatype(OOPSXDY[oadoam][0], param)
        elif OOPSXDY[oadoam][0] == DT_OAD:
            bdata += makebydatatype(OOPSXDY[oadoam][0], param)
        elif OOPSXDY[oadoam][0] == DT_TSA:
            bdata += makebydatatype(OOPSXDY[oadoam][0], param)
        elif OOPSXDY[oadoam][0] == DT_unsigned:
            bdata += makebydatatype(OOPSXDY[oadoam][0], param)
        elif OOPSXDY[oadoam][0] == DT_bit_string:
            bdata += makebydatatype(OOPSXDY[oadoam][0], param)
        elif OOPSXDY[oadoam][0] == DT_long_unsigned:
            bdata += makebydatatype(OOPSXDY[oadoam][0], param)
        elif OOPSXDY[oadoam][0] == DT_long64:
            bdata += makebyhoaddatatype(OOPSXDY[oadoam][0], param,oadoam)
        elif OOPSXDY[oadoam][0] == DT_OI:
            bdata += makebyhoaddatatype(OOPSXDY[oadoam][0], param, oadoam)
        elif OOPSXDY[oadoam][0] == DT_TI:
            bdata += makebyhoaddatatype(OOPSXDY[oadoam][0], param, oadoam)
        elif OOPSXDY[oadoam][0] == DT_NULL:
            bdata += makebyhoaddatatype(OOPSXDY[oadoam][0], param, oadoam)
        elif OOPSXDY[oadoam][0] == DT_integer:
            bdata += makebyhoaddatatype(OOPSXDY[oadoam][0], param, oadoam)
        elif OOPSXDY[oadoam][0] == DT_visible_string:
            bdata += makebyhoaddatatype(OOPSXDY[oadoam][0], param, oadoam)
        elif OOPSXDY[oadoam][0] == DT_double_long_unsigned:
            bdata += makebyhoaddatatype(OOPSXDY[oadoam][0], param, oadoam)
        else:
            print('makebyoadvalue 增加处理 ', oadoam)
    else:
        print('makebyoadvalue 增加[OOPSXDY]定义处理', oadoam, param)
    return bdata


def ActionRqtNormalbyoadvalue(oadoam, param):
    pass

#组一帧 645报文（透明转发使用）
def frm645(di,addr):
    frame = ''
    frame = make645Frame('', addr , '11', di,'', 1)
    return frame

def get645data(data):
    realdata =''
    l = is645Return(data, '', '30', '')
    print('l:', l)
    print('l[3]:', l[3])
    realdata = judgeMarkeIDwm(l[3])
    print('realdata:', judgeMarkeIDwm(l[3]))
    return realdata




# 透明代理编码 "'F2010202','0602080100',50,100,'68726701903120681104333334336D16'"
def makeProxyTransCommandRequestListbuff(param,di):
    bdata = ''
    lparam = strtolist(param)
    frame = ''
    if len(lparam) < 5: print("makeProxyTransCommandRequestListbuff 输入错误", param)
    # print("lparam", len(lparam))
    if len(lparam[0]) == 8:
        bdata += lparam[0]
    else:
        print("makeProxyTransCommandRequestListbuff param[0] 输入错误", param[0])
    # im = lparam[1].split(',')
    if len(lparam[1]) == 10:
        bdata += lparam[1]
    else:
        print("makeProxyTransCommandRequestListbuff param[1] 输入错误", param[1])

    bdata += valuetolongusingedbuff(lparam[2], 0)
    bdata += valuetolongusingedbuff(lparam[3], 0)
    if len(lparam) == 6:
        frame = frm645(lparam[5],lparam[4])
    elif len(lparam) == 5:
        frame = lparam[4]
    bdata += numbertohex(int(len(frame)/2), 2)
    bdata += frame
    return bdata


# 代理编码 '60,[['05000008022702',60,['20000200']],['05000008022703',60,['20000200']]]'
def makeProxyGetRequestListbuff(param):
    bdata = ''
    lparam = strtolist(param)
    if len(lparam) != 2: print("makeProxyGetRequestListbuff 输入错误", param)
    # print("lparam", len(lparam))
    if is_number(lparam[0]):
        bdata += valuetolongusingedbuff(lparam[0], 0)
    else:
        print("makeProxyGetRequestListbuff param[0] 输入错误", param[0])
    im = len(lparam[1])
    bdata += valuetounsignedbuff(im)
    # print("im==", im)
    for i in range(0, im, 1):
        ii = len(lparam[1][i])
        if ii != 3:
            print("makeProxyGetRequestListbuff lparam[1] 输入错误", lparam[1])
            break
        bdata += valuetoTSAbuff(lparam[1][i][0])
        bdata += valuetolongusingedbuff(lparam[1][i][1], 0)
        if isinstance(lparam[1][i][2], list):
            ii = len(lparam[1][i][2])
            bdata += valuetounsignedbuff(ii)
            for j in range(0, ii, 1):
                bdata += lparam[1][i][2][j]
        else:
            bdata += '00'
            print("makeProxyGetRequestListbuff 缺代理OAD")
    return bdata

# "['选择方法10',[1,'全部用户地址']],['202A0200','60420200','10100200']"
def valuetoRCSDbuff(value):
    sdata = ''
    # print("valuetoDTCSDbuff===", value)
    iarray = 0
    if isinstance(value, list):
        ilen = len(value)
        for i in range(0, ilen, 1):
            # print("value", value[i], i)
            if i == 0 and isinstance(value[i], list):
                print('valuetoRCSDbuff RCSD 输入错误', value)
                continue
            if i < ilen-1:
                if isinstance(value[i], list):
                    pass
                elif isinstance(value[i], str) and isinstance(value[i + 1], str):
                    sdata += '00'
                    sdata += value[i]
                    iarray += 1
                elif isinstance(value[i], str) and isinstance(value[i + 1], list):
                    sdata += '01'
                    sdata += value[i]
                    iROAD = len(value[i + 1])
                    sdata += numbertohex(iROAD, 2)
                    for j in range(0, iROAD, 1):
                        sdata += value[i + 1][j]
                    iarray += 1
            elif i == ilen-1:
                if isinstance(value[i], list):
                    pass
                elif isinstance(value[i], str):
                    sdata += '00'
                    sdata += value[i]
                    iarray += 1
        sdata = numbertohex(iarray, 2) + sdata
        # print('sdata=', sdata)
    else:
        print('valuetoRCSDbuff输入值错误 非list', value)
    return sdata


# dy RSD_Selector7: [DT_date_time_s, DT_date_time_s, DT_TI, DT_MS]
# value ['20200227140400', '20200227140400', '5分', '全部用户地址']
def makeRSDSelecbuff(dy, value):
    sdata = ''
    ilen = len(dy)
    # print('dy0==', dy[0])
    # RSD_Selector2
    if dy[0] == DT_array:
        sdata += numbertohex(len(value), 2)
        for item in value:
            if dy[1][0] == DT_OAD:
                # 王梦新增：行方法3
                if dy[1][1] == DT_se2:
                    sdata += item[0]
                    if len(dy[1]) == len(item):
                        for j in range(1, len(item) -1 , 1):
                            itemtype = OOPSXDY[item[0]][0]
                            sdata += numbertohex(itemtype, 2)
                            sdata += makebydatatype(itemtype, item[j])
                        if itemtype == DT_date_time or itemtype == DT_date_time_s:
                            sdata += numbertohex(DT_TI, 2)
                            sdata += makebydatatype(DT_TI, item[len(item) - 1])
                        else:
                            sdata += numbertohex(itemtype, 2)
                            sdata += makebydatatype(itemtype, item[len(item) - 1])
                    else:
                        print("makeRSDSelecbuff DT_unsigned输入值不匹配", dy, value)
                else:
                    print("makeRSDSelecbuff DT_array", dy, value)
    # RSD_Selector1 RSD_Selector2
    elif dy[0] == DT_OAD:
        #王梦新增：行方法1、2
        if dy[1] == DT_se1:
            sdata += value[0]
            dy1type = OOPSXDY[value[0]][0]
            sdata += numbertohex(dy1type, 2)
            sdata += makebydatatype(dy1type, value[1])
        elif dy[1] == DT_se2:
            sdata +=value[0]
            if len(dy) == len(value):
                for i in range(1, len(dy) - 1, 1):
                    dyitype=OOPSXDY[value[0]][0]
                    sdata += numbertohex(dyitype, 2)
                    sdata += makebydatatype(dyitype, value[i])
                if dyitype == DT_date_time or dyitype == DT_date_time_s:
                    sdata += numbertohex(DT_TI, 2)
                    sdata += makebydatatype(DT_TI, value[len(dy) - 1])
                else:
                    sdata += numbertohex(dyitype, 2)
                    sdata += makebydatatype(dyitype, value[len(dy) - 1])

            else:
                print("makeRSDSelecbuff DT_unsigned输入值不匹配", dy, value)
        else:
            print("makeRSDSelecbuff DT_OAD", dy, value)
    elif dy[0] == DT_unsigned or dy[0] == DT_date_time_s:
        if isinstance(value,list):
            if len(dy) == len(value):
                for i in range(0, len(dy), 1):
                    sdata += makebydatatype(dy[i], value[i])
            else:
                print("makeRSDSelecbuff DT_unsigned输入值不匹配", dy, value)
        elif isinstance(value,int):
            #方法9：['选择方法9', 1]；；；value = 1，不是列表类型，单独做个分支。20201210
            sdata += makebydatatype(dy[0], value)
        else:print('value的类型有误，请查看')

    else:
        print("makeRSDSelecbuff else输入值错误", dy, value)
    return  sdata

# lRSD ['选择方法7', ['20200227140400', '20200227140400', '5分', '全部用户地址']]
def makeRSDbuff(lRSD):
    sdata = ''
    # OOP_RSD_SelectornDY[lparam[0][0]],
    if lRSD[0] == RSD_NULL:
        sdata += '00'
        #春哥做的，其它方法，王梦新增流程中，方法3的len(lRSD）也为2，故要做区分：(lRSD[0]!= '选择方法3')
    elif lRSD[0] in OOP_RSD_CHOICE_VALUE and len(lRSD) == 2 and (lRSD[0]!= '选择方法3'):
        sdata += OOP_RSD_CHOICE_VALUE[lRSD[0]]
        sdata += makeRSDSelecbuff(OOP_RSD_SelectornDY[lRSD[0]], lRSD[1])
        #方法1
    elif lRSD[0] in OOP_RSD_CHOICE_VALUE and len(lRSD) == 3:
        sdata += OOP_RSD_CHOICE_VALUE[lRSD[0]]
        sdata += makeRSDSelecbuff(OOP_RSD_SelectornDY[lRSD[0]], lRSD[1:])
        #方法2
    elif lRSD[0] in OOP_RSD_CHOICE_VALUE and len(lRSD) == 5:
        sdata += OOP_RSD_CHOICE_VALUE[lRSD[0]]
        sdata += makeRSDSelecbuff(OOP_RSD_SelectornDY[lRSD[0]], lRSD[1:])
        #方法3
    elif (lRSD[0] in OOP_RSD_CHOICE_VALUE) and (isinstance(lRSD[1],list)):
        sdata += OOP_RSD_CHOICE_VALUE[lRSD[0]]
        sdata += makeRSDSelecbuff(OOP_RSD_SelectornDY[lRSD[0]], lRSD[1:])

    else:
        print('makeRSDbuff 输入参数异常', lRSD)
    return  sdata


# param = [RSD, RCSD]
# "['选择方法7', ['20200227140400', '20200227140400', '5分', '全部用户地址']], ['50020200',['00200200','00400200']]"
# "['选择方法5', ['20190725235800', '全部用户地址']],['202A0200','60400200','60410200','60420200','50040200',['20210200','00100200','00200200']]"
def makegetrecordbuff(param,oadoam):
    bdata = ''
    lparam = strtolist(param)
    #60120300
    if len(lparam) == 2 and len(lparam[0]) == 2:
        bdata += makeRSDbuff(lparam[0])
        bdata += valuetoRCSDbuff(lparam[1])
    #60000200
    #方法2
    elif len(lparam) == 2 and len(lparam[0]) == 5:
        bdata += makeRSDbuff(lparam[0])
        bdata += valuetoRCSDbuff(lparam[1])
    #方法3
    elif len(lparam) == 2 and isinstance(lparam[0][1],list):
        bdata += makeRSDbuff(lparam[0])
        bdata += valuetoRCSDbuff(lparam[1])
    #方法1
    elif len(lparam) == 2 and len(lparam[0]) == 3:
        bdata += makeRSDbuff(lparam[0])
        bdata += valuetoRCSDbuff(lparam[1])

    else:
        print('makegetrecordbuff 输入参数异常param', param)
    return  bdata


# sTimeTag "无时间标签" 10秒， 5分  此流程为无时间标签或有效时间标签
def makeTimeTag(sTimeTag):
    bdata = ''
    if sTimeTag == "无时间标签":
        bdata += "00"
    else:
        bdata += "01"
        bdata += makenowtodatetime_s()
        bdata += makebydatatype(DT_TI, sTimeTag)
    return bdata

# sTimeTag "无效时间标签" 此流程为无效时间标签
def makeTimeTaglose(sTimeTag):
    bdata = ''
    bdata += "01"
    bdata += makewrongdatetime_s()#传入无效的时间
    bdata += makebydatatype(DT_TI, sTimeTag)
    return bdata



def paramdeal(param):
    d=[]
    wrongtime=0
    truetime=0
    Tp=""
    if str(param).find("有效时标")>=0:
        truetime=1
        d = param.split(",有效时标,")
        Tp = d[1]
        d = d[0]
        d = [d]

    elif param.find(u"无效时标")>=0:
        wrongtime=1
        d = param.split(",无效时标,")
        Tp = d[1]
        d = d[0]
        d = [d]
    elif param.find(u"对至系统时间") >= 0:
        d= [General.getcurrenttime()]
    elif param.find(u"对至当前日") >= 0:
        d= [General.getcurrenttimenew(param)]
    elif param.find(u"对至当前月末") >= 0:
        d = [General.getcurmonlastday(param)]
    elif param.find(u"对至当前年末") >= 0:
        d = [General.getcuryearlastday(param)]
        #对时至（系统）当前日的后一天。
    elif param.find(u"对至后一天") >= 0:
        d = [General.getcurrenttimeafter(param)]
    else:
        d.append(param)
    return truetime,wrongtime,d,Tp

# oop解帧函数 返回 [data]
def deal_oop_Frame(frame):
    lreturn = [False]
    if len(frame) < MIN_LEN_OOP_FRAME:
        return lreturn
    frame = frame.upper()
    for i in range(0, len(frame), 2):
        bb, ippp = CheckValid(frame[i:])
        if bb:
            lreturn[0] = True
            lreturn += [frame[i:i + ippp]]
    return lreturn




# 组帧，request_name apdu操作类型, oad_omd 属性方法标识'[]', dparam 参数'[]',tname:（用例名称列）用来传进来是否带时间标签的参数， TimeTag， 输出apdu buff
def make_DATA_APDU_Request(security, request_name, ipiid, oad_omd, dparam, ttime,wtime,Tp,sTimeTag = "无时间标签"):
    buff = ''
    #给交采计量使用
    if security == '明文+MAC':
        # 增加密文处理
        buff += '1000'
        btype = getbuffbyOPName(request_name)
        bPIID = getPIIDBuff(False, ipiid)
        btype += bPIID
        #5246-5247只支持读取一个对象属性的原代码。被我改为5252--5266行
        # if len(oad_omd) >= 1:
        #     print('len(oad_omd[0])', len(oad_omd[0]), oad_omd[0])
        #     if len(oad_omd[0]) == 8:
        #         btype += oad_omd[0]
        #     else:
        #         print('make_DATA_APDU_Request 输入oad错误')
        if btype[:2] == Client_APDU_GET_Request and btype[2:4] == GetRequestNormal:
            if len(oad_omd) >= 1:
                if len(oad_omd[0]) == 8:
                    btype += oad_omd[0]
                else:
                    print('make_DATA_APDU_Request 输入oad错误')
        elif btype[:2] == Client_APDU_GET_Request and btype[2:4] == GetRequestNormalList:
            oad_omd = oad_omd[0].strip(",").split(",")
            load = len(oad_omd)
            btype += numbertohex(load, 2)
            for item in oad_omd:
                if len(item) == 8:
                    btype += item
                else:
                    print('Client_APDU_GET_Request 输入oad错误')
        elif btype[:2] == Client_APDU_SET_Request and btype[2:4] == SetRequestNormal:
            # 优先
            print(oad_omd[0])
            if len(oad_omd[0]) == 8:
                btype += oad_omd[0]
            else:
                print('make_DATA_APDU_Request Excel输入错误"明文+MAC"', oad_omd[0])
            btype += makebyoadvalue(oad_omd[0], dparam[0], btype[:2])
        elif btype[:2] == Client_APDU_ACTION_Request and btype[2:4] == ActionRequestNormal:
            # 优先
            # print("Client_APDU_ACTION_Request==",oad_omd, dparam)
            if len(oad_omd[0]) == 8:
                btype += oad_omd[0]
            else:
                print('make_DATA_APDU_Request Excel输入错误', oad_omd[0])
            btype += makebyoadvalue(oad_omd[0], dparam[0], btype[:2])

        buff += numbertohex(int(len(btype)/2), 2)
        buff += btype
        buff += '01'
        buff += "106AD30D71BB6DD596952CF28E44922A69"
        return buff
    else:pass
    if security == '密文':
        # 增加密文处理
        return buff
    btype = getbuffbyOPName(request_name)
    buff += btype
    bPIID = getPIIDBuff(False, ipiid)
    buff += bPIID
    if len(btype) < 4:
        # 增加处理
        return buff
    if isinstance(oad_omd, list) and isinstance(dparam, list):
        pass
    else:
        return buff
    if btype[:2] == Client_APDU_GET_Request and btype[2:] == GetRequestNormal:
        if len(oad_omd) >= 1:
            if len(oad_omd[0]) == 8:
                buff += oad_omd[0]
            else:
                print('make_DATA_APDU_Request 输入oad错误')
    elif btype[:2] == Client_APDU_GET_Request and btype[2:] == GetRequestNormalList:
        oad_omd=oad_omd[0].strip(",").split(",")
        load = len(oad_omd)
        buff += numbertohex(load, 2)
        for item in oad_omd:
            if len(item) == 8:
                buff += item
            else:
                print('Client_APDU_GET_Request 输入oad错误')
    elif btype[:2] == Client_APDU_GET_Request and btype[2:] == GetRequestRecord:
        if len(oad_omd) >= 1:
            if len(oad_omd[0]) == 8:
                buff += oad_omd[0]
            else:
                print('Client_APDU_GET_Request GetRequestRecord 输入oad错误', oad_omd[0])
        else:
            print('Client_APDU_GET_Request GetRequestRecord 输入oad错误', oad_omd)
        buff += makegetrecordbuff(dparam[0],oad_omd[0])
        # print('make_DATA_APDU_Request GetRequestRecord 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_GET_Request and btype[2:] == GetRequestRecordList:
        #王梦新增
        buff += numbertohex(len(dparam), 2)
        for item in dparam:
            if len(oad_omd) >= 1:
                if len(oad_omd[0]) == 8:
                    buff += oad_omd[0]
                else:
                    print('Client_APDU_GET_Request GetRequestRecordList 输入oad错误', oad_omd[0])
            else:
                print('Client_APDU_GET_Request GetRequestRecordList 输入oad错误', oad_omd)
            buff += makegetrecordbuff(item[0], oad_omd[0])
    elif btype[:2] == Client_APDU_GET_Request and btype[2:] == GetRequestNext:
        # 优先
        print('make_DATA_APDU_Request GetRequestNext 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_GET_Request and btype[2:] == GetRequestMD5:
        print('make_DATA_APDU_Request GetRequestMD5 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_SET_Request and btype[2:] == SetRequestNormal:
        # 优先
        print(oad_omd[0])
        if len(oad_omd[0]) == 8: buff += oad_omd[0]
        else: print('make_DATA_APDU_Request Excel输入错误', oad_omd[0])
        buff += makebyoadvalue(oad_omd[0], dparam[0],btype[:2])
        # print('make_DATA_APDU_Request SetRequestNormal 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_SET_Request  and btype[2:] == SetRequestNormalList:
        print('make_DATA_APDU_Request SetRequestNormalList 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_SET_Request  and btype[2:] == SetThenGetRequestNormalList:
        print('make_DATA_APDU_Request SetThenGetRequestNormalList 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_ACTION_Request  and btype[2:] == ActionRequestNormal:
        # 优先
        # print("Client_APDU_ACTION_Request==",oad_omd, dparam)
        if len(oad_omd[0]) == 8: buff += oad_omd[0]
        else: print('make_DATA_APDU_Request Excel输入错误', oad_omd[0])
        buff += makebyoadvalue(oad_omd[0], dparam[0],btype[:2])
        # print('make_DATA_APDU_Request ActionRequestNormal 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_ACTION_Request  and btype[2:] == ActionRequestNormalList:
        print('make_DATA_APDU_Request ActionRequestNormalList 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_ACTION_Request  and btype[2:] == ActionThenGetRequestNormalList:
        print('make_DATA_APDU_Request ActionThenGetRequestNormalList 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_PROXY_Request and btype[2:] == ProxyGetRequestList:
        # 优先
        buff += makeProxyGetRequestListbuff(dparam[0])
        print('make_DATA_APDU_Request ProxyGetRequestList 处理完成', oad_omd, dparam)
    elif btype[:2] == Client_APDU_PROXY_Request and btype[2:] == ProxyGetRequestRecord:
        print('make_DATA_APDU_Request ProxyGetRequestRecord 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_PROXY_Request and btype[2:] == ProxySetRequestList:
        print('make_DATA_APDU_Request ProxySetRequestList 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_PROXY_Request and btype[2:] == ProxySetThenGetRequestList:
        print('make_DATA_APDU_Request ProxySetThenGetRequestList 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_PROXY_Request and btype[2:] == ProxyActionRequestList:
        print('make_DATA_APDU_Request ProxyActionRequestList 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_PROXY_Request and btype[2:] == ProxyActionThenGetRequestList:
        print('make_DATA_APDU_Request ProxyActionThenGetRequestList 增加处理', oad_omd, dparam)
    elif btype[:2] == Client_APDU_PROXY_Request and btype[2:] == ProxyTransCommandRequest:
        buff += makeProxyTransCommandRequestListbuff(dparam[0],oad_omd)
    else:
        print('未处理类型增加处理')
        pass
    if ttime==1:
        sTimeTag=Tp
        buff += makeTimeTag(sTimeTag)
    elif wtime==1:
        sTimeTag =Tp
        buff += makeTimeTaglose(sTimeTag)
    else:
        buff += makeTimeTag(sTimeTag)


    return buff

# srev 字符串，LinkRequestType=LinkRequestType_LOGIN, LinkRequestType_HEART
# return  [True, LinkRequestType, b'h0\x00\x01\x05\x03\x00']
def islinkReturn(srev):
    relst = [False]
    revhex = General.hexShow(srev)
    # print('revhex', revhex)
    revhex = revhex.replace(' ', '')
    fenzhen,ll = Receive(revhex)
    print('islinkReturnll:', ll)
    hearttime0=ll[-1]
    if len(ll) > 5:
        relst[0] = True
        if CTRL_LINK == ll[2]:
            relst += [ll[4]]
            relst += [General.hexascii(ll[3])]
        else:
            relst[0] = False
            relst += ['NULL']
            relst += [revhex]
    else:
        relst[0] = False
        relst += ['NULL']
        relst += [revhex]
    print('islinkReturn', relst)
    return relst,hearttime0

# 上报响应apdu
def make_REP_APDU_Response(buff_APDU):
    stmp = ''
    if buff_APDU[0:2] == '88':
        stmp = '08'
        if buff_APDU[2:4] == '02':
            stmp += buff_APDU[2:4]
            stmp += buff_APDU[4:8]
            stmp += buff_APDU[8:16]
            stmp += '00'
        elif buff_APDU[2:4] == '01':
            pass
        elif buff_APDU[2:4] == '03':
            pass
    return stmp.upper()


# srev 字符串，
# return  [True, afn, b'h0\x00\x01\x05\x03\x00']
def isappReturn(srev):
    relst = [False]
    revhex = General.hexShow(srev)
    ldata = splitframetime(revhex)
    #上报时，发现有连帧的情况，故写一个函数，专门处理连帧的情况（已经不会有连帧了，上一层已经处理过了，此处改动不影响流程，不再改回去）。
    dataneed = ldata[1]
    dataneed = Contirame(ldata[1])
    dfme = GetFrame(dataneed)
    if dfme[0]:
        relst[0] = True
        tcz = dfme[1]['APDU'][:2]
        #tid = reverse(ll[4][8:16])
        # print('tcz', tcz)
        if tcz == Server_APDU_REPORT_Notification:
            relst += [tcz]
            frm = {}
            frm['CTRL'] = '03'
            # print(dfme[1]['TSA_TYPE'])
            frm['TSA_TYPE'] = dfme[1]['TSA_TYPE']
            frm['TSA_VS'] = dfme[1]['TSA_VS']
            frm['TSA_AD'] = dfme[1]['TSA_AD']
            frm['CA'] = dfme[1]['CA']
            frm['SEG_WORD'] = dfme[1]['SEG_WORD']
            frm['APDU'] = make_REP_APDU_Response(dfme[1]['APDU'])
            sfr = [MakeFrame(frm)]
            print('sfr', sfr)
            relst += [General.hexascii(sfr[0])]
        elif tcz in Server_APDU_SET:
            relst[0] = True
            relst += [tcz]
            relst += [srev]
        else:
            relst[0] = False
            relst += [tcz]
            relst += [srev]
    print('isappReturn', relst)
    return relst


if __name__ == '__main__':
    # print(reverse('123456'))
    # eee = getbit('43',7,8,1)
    # print(eee)
    frm = {}
    frm['CTRL'] = '43'
    frm['TSA_TYPE'] = 0
    frm['TSA_VS'] = 1
    frm['TSA_AD'] = '000000000003'
    frm['CA'] = '00'
    frm['SEG_WORD'] = ''
    frm['APDU'] = '05010123010A000107E30B1A0F15340001F4'
    s = '明文'
    r = '操作一个对象方法'
    i = 0
    i += 1
    o = ['60147F00']
    d = []
    # frm['APDU'] = make_DATA_APDU_Request(s, r, i, o, d)
    # print(makeTSA(frm['TSA_TYPE'],frm['TSA_VS'],frm['TSA_AD']))
# 682100430503000000000000A4B705010123010A000107E30B1A0F15340001F454E216
    # print(MakeFrame(frm))
    s = '[2018-12-03-10:10:51:859]682100430503000000000000A4B705010123010A000107E30B1A0F15340001F454E216'
    # print(CheckValid(s))
    # print(Add33('FF22334455'))
    # print(Reduce33('3255667788'))
    ss='[2018-12-03-10:10:51:859]685200C305030000000000000AD385010023010900010105140000000094644800140000000094644800140000000000000000140000000000000000140000000000000000000107E30B1B0D2E360001F4A8EE16'
    # dd = GetFrame(ss)
    # print(dd[1])
    # print(hextodatetime('07E30B1A0200012A1230'))
    # print(datetimetohex(datetime.datetime.now()))
    # print(hextodatetime(datetimetohex(datetime.datetime.now())))
    # print(bcdtodatetime('201911260112131234'))
    # dd1 = datetime.datetime.now()
    # print(datetimetohex(dd1))
    # time.sleep(0.5)
    # dd2 = datetime.datetime.now()
    # print(datetimetohex(dd2))
    # print(make_datetime(dd1,dd2))
    slk = '[2018-12-03-10:10:51:859]681E008105030000000000006981013F01012C07E30C0200082F020000A3F516'
    # print(Receive('[2018-12-03-10:10:51:859]681E008105030000000000006981013F01012C07E30C0200082F020000A3F516'))
    da = '[2018-12-03-10:10:51:859]68DB00C305030000000000002AA8850100600002000101030204120000020A550705000000000003' \
         '1603160351F208020109010011041103160312089812003C020455070500000000000009030000001200011200010100020412000' \
         '1020A5507050000080227021603160251F201020209010011041103160312089812003C0204550705000000000000090300000012' \
         '000112000101000204120002020A5507051111111111111606160351F201020109010011041103160312089812003C02045507050' \
         '000000000000903000000120001120001010000005C2C16'
    rw = '[2018-12-03-10:10:51:859]683D01C30503000000000000EECC85010160120200010105020C110154010005160111011C07E30A' \
          '010001001C08330A0100010054010001110516011200001200000202160001010204110011001117113B020C11025402000116011' \
          '1021C07E30A010001001C08330A0100010054010002110716011200001200000202160001010204110011001117113B020C110354' \
          '030001160111031C07E30A010001001C08330A010001005401000F110116011200001200000202160001010204110011001117113' \
          'B020C110454040001160111041C07E30A010001001C08330A010001005401001E1100160112000012000002021600010102041100' \
          '11001117113B020C110554030001160111051C07E30A010001001C08330A010001005401001411031601120000120000020216000' \
          '1010204110011001117113B0000FF2216'
    fa = '[2018-12-03-10:10:51:859]689801C30503000000000000BBB7850100601402000101050206110112003E020211000001145B00' \
          '200002005B00200102005B00200402005B00200502005B00200A02005B00101002005B00102002005B00200202005B00200302005' \
          'B00001002005B00003002005B00002002005B00004002005B00000002005B00005002005B00006002005B00007002005B00008002' \
          '005B00400002005B00200104005C01160102061102120002020211035401000F01015B01500202000A20000200200102002001040' \
          '02004020020050200200A0200001002000030020000200200004002005C0116060206110312003E020211020001015B0150040200' \
          '0A101002001020020000100200002002000030020000400200005002000060020000700200008002005C0116020206110412000C0' \
          '20211020001015B0150060200091010020000100200002002000030020000400200005002000060020000700200008002005C0116' \
          '050206110512003E020211020001015B0150050200061010020010200200001002000020020000300200004002005C0116020000B' \
          '59D16'
    ss3 = '[2018-12-03-10:10:51:859]684800C30503000000000000C7B5850100230109000101051400000001AD2748001400000001AD27' \
          '480014000000000000000014000000000000000014000000000000000000000DC216'
    ss4 = '[2018-12-03-10:10:51:859]681A00C30503000000000000A5A28501000010020000060000551116'
    ss5 = '[2018-12-03-10:10:51:859]683400C315030000000000008A528501000010020001010506000020640600000000060000000006' \
          '000020640600000000000001B516'
    ss6 = '[2018-12-03-10:10:51:859]686600C31503000000000000E84585010010100200010105020206000012941C07E30C120B1D0002' \
          '0206000000001C07D00101000000020206000000001C07D00101000000020206000012941C07E30C120B1D00020206000000001C0' \
          '7D001010000000000D14E16'
    ss7 = '[2018-12-03-10:10:51:859]682204C305030000000000005C3D8503006012030001015004020014200002002001020020010400' \
          '2004020020050200200A0200101002001020020020020200200302000010020000200200003002000040020000500200006002000' \
          '0700200008002000000020040000200010301140100010000010001000100010502020600000DBF1C07E30C0B122D000202060000' \
          '00001C07D00101000000020206000000001C07D0010100000002020600000DBF1C07E30C0B122D00020206000000001C07D001010' \
          '00000010001000100010506000000B40600000000060000000006000000B406000000000105060000000006000000000600000000' \
          '060000000006000000000105050000000105000000000500000000050000000105000000000105050000000005000000000500000' \
          '000050000000005000000000105060000000106000000000600000000060000000106000000000105060000000006000000000600' \
          '000000060000000006000000000105060000000006000000000600000000060000000006000000000105060000000006000000000' \
          '600000000060000000006000000000100000114010001000001000100010001050202060000478E1C07E30B1C090E000202060000' \
          '47891C07E30B1C090F00020206000044991C07E30B1C032B000202060000446F1C07E30C091635000202060000453E1C07E30B1C0' \
          '0100001000100010001050600025CCF060000AA250600009A790600009D8F0600007AA10105060000000006000000000600000000' \
          '0600000000060000000001050500000ADC050000032E05000002CB05000002CA05000002180105050000000005000000000500000' \
          '0000500000000050000000001050600000ADC060000032E06000002CB06000002CA06000002180105060000000006000000000600' \
          '000000060000000006000000000105060000000006000000000600000000060000000006000000000105060000000006000000000' \
          '6000000000600000000060000000001000001140100010000010001000100010502020600000B6D1C07E30C0A0003000202060000' \
          '0B1B1C07E30C0A022A0002020600000B231C07E30C0A032F0002020600000B371C07E30C0A07170002020600000B691C07E30C091' \
          '73B00010001000100010506000049030600001201060000122F060000127A06000012580105060000000006000000000600000000' \
          '06000000000600000000010505000000BC050000002D050000002E0500000030050000002F0105050000000005000000000500000' \
          '00005000000000500000000010506000000BC060000002D060000002E0600000030060000002F0105060000000006000000000600' \
          '000000060000000006000000000105060000000006000000000600000000060000000006000000000105060000000006000000000' \
          '600000000060000000006000000000100000000B1AE16'
    ss8 = '[2018-12-03-10:10:51:859]68A300C305030000000000004A4A850300601203000500202A02000060420200002000020000200F0' \
          '200002001020001035507050000000000031C07E30C0C0E2900010000010305000005D605000000000500000000550705000008022' \
          '7021C07E30C0C0E2900010000010305000005DD05000005D605000005D15507051111111111111C07E30C0C0E29000100000103050' \
          '00005D50500000000050000000000006ACE16'

    ss9 = '[2018-12-03-10:10:51:859]689A00C30503000000000000BE308502030423010200010104020355070580008000800116001600' \
          '020355070580008000800216001600020355070580008000800316001600020355070580008000800416001600230202000101010' \
          '203550705000000000003160016002303020001010102035507050000080227021600160023040200010101020355070511111111' \
          '1111160016000000E94316'
    st = '[2020-01-10-08:39:10:967] 681E00810503000000000000698101330000B407E4010A000827270000F86416'
    # 上报
    sb = '68AD00830503000000000000F4E588020401320002000A002022020000201E020000202002000020240200003300020000330502060' \
         '03305020700330502080033050209003305020A0101060000000E1C07E30C150002001C07E30C1500020050810301040202514500000' \
         '01101020251451000001101020251F20002011100020251F20C02011100140000000000000000502301040880140000000001D905C01' \
         '400000000044AA2000000168F16'
    # 登录
    xt = '[2018-12-03-10:10:51:859]681E00810503000000000000698101230100B407E30C1E0002063500006FD116'
    denglu = '[2018-12-03-10:10:51:859]681E00810503000000000000698101020000B407E30C1E000A141E0000FD8516'
    st = '[2018-12-03-10:10:51:859]682500C30503000000000000262D8501004000040001020511001100110011001100000089AD16'
    # 代理：响应异常
    dljsyc = "[2020-02-28-16:26:11:718]683300C3050300000000000014A9890114020705000008022702012000020000FF0705000008022703012000020000210000B75616"
    # 代理：响应正常1
    dljs1 = "[2020-02-28-16:26:11:718]681201C3050100000000001012158901060107050000000000030900100200010105060012AF98060001E208060008578C060004F394060003827000200200010105060012AF98060001E208060008578C060004F394060003827000000200010105050012AF98050001E208050008578C050004F39405000382700030020101050012AF980040020101050012AF9800500200010105060012AF98060001E208060008578C060004F394060003827000600200010105060012AF98060001E208060008578C060004F394060003827000700200010105060012AF98060001E208060008578C060004F394060003827000800200010105060012AF98060001E208060008578C060004F39406000382700000046916"
    # 代理：响应正常2
    dljs = "[2020-02-28-16:26:11:718]689000C30503000000000000362789010003070500000802270601001002000101050600024D3D0600000000060000A24A06000130A70600007A4B07051111111111110100100200010105060000609806000017E6060000181F0600001873060000181F07050000080226970100100200010105060001E0CB0600009B4506000070920600004A970600008A5D0000CD2216"
    # 分钟曲线
    fzjl ='683800C31501000000000000CE878501334004020001020302031600120000170000000002031600120000170000000005000000000000064616'
    dd = Receive(fzjl)
    # Receive (True,
    # {'LEN': 163, 'CTRL': 'C3',
    # 'CTRL_BS': {'C_DIR': [7, 7, 1], 'C_PRM': [6, 6, 1], 'C_SEG': [5, 5, 0], 'C_NULL': [4, 4, 0], 'C_CODE': [3, 3, 0], 'C_AFN': [0, 2, 3]},
    # 'SA': '05',
    # 'SA_BS': {'SA_TYPE': [6, 7, 0], 'SA_VS': [4, 5, 0], 'SA_LEN': [0, 3, 6]},
    # 'TSA_TYPE': 0,
    # 'TSA_VS': 0,
    # 'TSA_AD': '000000000003',
    # 'CA': '00', 'APDU': '850300601203000500202A02000060420200002000020000200F0200002001020001035507050000000000031C07E30C0C0E2900010000010305000005D6050000000005000000005507050000080227021C07E30C0C0E2900010000010305000005DD05000005D605000005D15507051111111111111C07E30C0C0E2900010000010305000005D5050000000005000000000000',
    # 'SEG_WORD': '',
    # 'SEG_WORD_BS': {}}
    # )
    print('dd:')
    print(dd)
    print('dd:')
    # bss = b'h\x1e\x00\x81\x05\x03\x00\x00\x00\x00\x00\x00i\x81\x01\t\x00\x00\xb4\x07\xe4\x01\n\x00\t\x18(\x00\x00\xaf' \
    #       b'\xba\x16'
    # print(islinkReturn(bss))
    pa = b'hz\x00\x83\x05\x03\x00\x00\x00\x00\x00\x00Ik\x88\x02\x02\x011\x06\x02\x00\x06\x00 "\x02\x00\x00 \x1e\x02' \
         b'\x00\x00  \x02\x00\x00 $\x02\x00\x003\x00\x02\x00\x003\t\x02\x06\x01\x01\x06\x00\x00\x00\x06\x1c\x07\xe4' \
         b'\x01\n\x116\x16\x1c\x07\xe4\x01\n\x117\x07\x16\x01\x01\x04\x02\x02QE\x00\x00\x00\x11\x00\x02\x02QE\x10\x00' \
         b'\x00\x11\x00\x02\x02Q\xf2\x00\x02\x01\x11\x00\x02\x02Q\xf2\x0c\x02\x01\x11\x00\x04\x08\x00\x00\x00\xc5\xaf' \
         b'\x16'
    sj = '689700C30503000000000000D087850103600002000101020204120001020A5507050000000000011603160351F208020109010011041115160312089812000F020455070500000000000009010012000112000101000204120002020A5507051111111111111603160251F201020109010011041101160312089812000F0204550705000000000000090100120001120001010000000CB716'
    sssb = General.hexascii(sj)
    print(isappReturn(sssb))
    print(islinkReturn(sssb))
    # print(getbitbyCA('单地址'))
    if '操作一个对象方法' in dOPName: print('True')
    print(makebyoadvalue('40000200', '20200116053000',0))
    print('test make struct:')
    print(makebyoadvalue('40000400', '[0,0,0,0,0]',0))
    smn = "[[0,['05000000000003',3,3,'F2080201','00',4,3,3,2200,60],['05000000000000','000000',1,1],[]],[1,['05000008022702',3,2,'F2010202','00',4,3,3,2200,60],['05000000000000','000000',1,1],[]],[2,['05111111111111',6,3,'F2010201','00',4,3,3,2200,60],['05000000000000','000000',1,1],[]]]"
    print("array struct表档案编码")
    print(makebyoadvalue('60008000', smn,0))
    srw = "[[1,'5分',1,1,'20191001000100','20991001000100','1分',5,1,0,0,[0,[[0,0,23,59]]],],[2,'1时',1,2,'20191001000100','20991001000100','2分',7,1,0,0,[0,[[0,0,23,59]]],],[3,'1日',1,3,'20191001000100','20991001000100','15分',1,1,0,0,[0,[[0,0,23,59]]],],[4,'1月',1,4,'20191001000100','20991001000100','30分',0,1,0,0,[0,[[0,0,23,59]]],],[5,'1日',1,5,'20191001000100','20991001000100','20分',3,1,0,0,[0,[[0,0,23,59]]],]]"
    print("array struct 任务编码")
    print(makebyoadvalue('60127F00', srw,0))
    # sfa = "[[1,62,[0,'NULL'],['20000200','20010200','20040200','20050200','200A0200','10100200','10200200','20020200','20030200','00100200','00300200','00200200','00400200','00000200','00500200','00600200','00700200','00800200','40000200','20010400'],'全部用户地址',1],[2,2,[3,'15分'],['50020200':['20000200','20010200','20010400','20040200','20050200','200A0200','00100200','00300200','00200200','00400200']],'全部用户地址',6],[3,62,[2,'NULL'],['50040200':['10100200','10200200','00100200','00200200','00300200','00400200','00500200','00600200','00700200','00800200']],'全部用户地址',2],[4,12,[2,'NULL'],['50060200':['10100200','00100200','00200200','00300200','00400200','00500200','00600200','00700200','00800200']],'全部用户地址',5],[5,62,[2,'NULL'],['50050200':['10100200','10200200','00100200','00200200','00300200','00400200']],'全部用户地址',2]]"
    sfa = "[[1,62,[0,'NULL'],['20000200','20010200','20040200','20050200','200A0200','10100200','10200200','20020200','20030200','00100200','00300200','00200200','00400200','00000200','00500200','00600200','00700200','00800200','40000200','20010400'],'全部用户地址',1],[2,2,[3,'15分'],['50020200',['20000200','20010200','20010400','20040200','20050200','200A0200','00100200','00300200','00200200','00400200']],'全部用户地址',6],[3,62,[2,'NULL'],['50040200',['10100200','10200200','00100200','00200200','00300200','00400200','00500200','00600200','00700200','00800200']],'全部用户地址',2],[4,12,[2,'NULL'],['50060200',['10100200','00100200','00200200','00300200','00400200','00500200','00600200','00700200','00800200']],'全部用户地址',5],[5,62,[2,'NULL'],['50050200',['10100200','10200200','00100200','00200200','00300200','00400200']],'全部用户地址',2]]"
    print("array struct 方案编码")
    print(makebyoadvalue('60147F00', sfa,0))
    o = ['60008000']
    d = [smn]
    # print("dd= ", d)
    frm['APDU'] = make_DATA_APDU_Request(s, r, i, o, d, '3分')
    # print(makeTSA(frm['TSA_TYPE'],frm['TSA_VS'],frm['TSA_AD']))
    # 682100430503000000000000A4B705010123010A000107E30B1A0F15340001F454E216
    print(MakeFrame(frm))
    print(inttohex(-20))
    print(hextoint(0xce))
    print(valuetodtsbuff('20200117133824'))
    print(valuetodatebuff('20200117'))
    print(valuetotimebuff('7700133824'))
    print(hextodouble_long('2001','FFFFEB02'))
    lmn = strtolist(sfa)
    print(len(lmn))
    for i in lmn:
        print(i)
    dl = "60,[['05000008022702',60,['20000200']],['05000008022703',60,['20000200']]]"
    # ldl = strtolist(dl)
    # print("ldl=", len(ldl[1][0]))
    print(makeProxyGetRequestListbuff(dl))
    # 日冻结
    sr = "['选择方法5', ['20190725235900', '全部用户地址']],['202A0200','60400200','60410200','60420200','50040200',['20210200','00100200','00200200']]"
    # 曲线数据
    sr = "['选择方法7', ['20190727000000', '20190727235959','15分','全部用户地址']],['60420200','202A0200','50020200',['20210200','00100200','00200200']]"
    # 实时数据
    sr = "['选择方法10', [1, '全部用户地址']],['202A0200','60420200','10100200']"
    # 结算日
    sr = "['选择方法7', ['20191214000000', '20191216010000','1日','全部用户地址']],['202A0200','60400200','60410200','60420200','50050200',['10100200','10200200','00100200','00200200','00300200','00400200','00500200','00600200','00700200','00800200']]"
    # 月冻结
    sr = "['选择方法7',['20191201000000','20191231000000','1月','全部用户地址']],['202A0200','60400200','60410200','60420200','50060200',['10100200','10200200','00100200','00200200','00300200','00400200','00500200','00600200','00700200','00800200']]"
    print(makegetrecordbuff(sr))
    print(makeTimeTag("5时"))