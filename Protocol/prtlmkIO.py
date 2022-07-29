# -*- coding: utf-8 -*-
import os
import datetime
import time
# import unicodedata
# import configparser
# from OpenExcelTestPlan import ExcelPlan
from Protocol.FCSccc import *
from Protocol import General
import configparser

MIN_LEN_MKIO_FRAME = 16
CTRL_OK = 0
CTRL_NO = 1
CTRL_DATA = 2

# LINK_APDU_Request = '01'
# LINK_APDU_Response = '81'
# LinkRequestType_LOGIN = '00'
# LinkRequestType_HEART = '01'
# LinkRequestType_EXIT = '02'

POS_oop_HEAD = 0   # 0
POS_oop_LEN = 2    # 1
POS_oop_CTRL = 6   # 3
# POS_oop_ADDR = 8   # 4
POS_oop_DATA = 10  # 14
MIN_LEN_MKFRAME = 18  # 18

APDU_CONNECT_Request = '01' # 链路协商请求 [1]
APDU_GET_Request = '02'     # 读取请求 [2]
APDU_SET_Request = '03'     # 设置请求 [3]
APDU_REPORT_Notification = '04'  # 上报通知 [4]
APDU_CONNECT_Response = '81'       # 链路协商响应 [129]
APDU_GET_Response = '82'           # 读取响应 [130]
APDU_SET_Response = '83'           # 设置响应 [131]
APDU_REPORT_Notification_Response = '84'    # 上报通知响应 [132] ，
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
DT_DT = 80
DT_Scaler_Unit = 81
# 自定义任意数据标识 方案采集方式 事件采集方式
DT_facjtype = 100
DT_sjcjtype = 101

LINK_APDU_SET = [APDU_CONNECT_Request, APDU_CONNECT_Response]
APDU_SET = [APDU_CONNECT_Request, APDU_GET_Request, APDU_SET_Request, APDU_REPORT_Notification, APDU_CONNECT_Response,
            APDU_GET_Response, APDU_SET_Response, APDU_REPORT_Notification_Response]
APDU_APP_SET = [APDU_CONNECT_Request, APDU_GET_Request, APDU_SET_Request, APDU_REPORT_Notification,
                APDU_CONNECT_Response, APDU_GET_Response, APDU_SET_Response, APDU_REPORT_Notification_Response]

ENUM_MK = ['GPRS', 'PLC', 'RS485', 'YX', 'CAN', 'BUS', 'CTRL', 'PT100', 'RS232', 'XJY']

FRAME = {'CTRL': 'C2', 'FID': '', 'APDU': '', 'CTRL_BS': {'C_DIR': [7, 7, 0], 'C_PRM': [6, 6, 1], 'C_AFN': [0, 5, 6]}}


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


def calcCheckSum(fr):
    checkSum = 0
    for i in range(0, len(fr), 2):
        checkSum += int(fr[i:i + 2], 16)
    return str(hex(checkSum))

# add // N字节地址
# vxd // 逻辑地址0，终端，1，交采
# type // 地址类型0,表示单地址，1表示通配地址，2表示组地址，3表示广播地址
# 输出字符串
def makeTSA(type, vxd, add):
    stmp = ''
    sbin = bin(type).replace('0b', '').zfill(2)
    sbin += bin(vxd).replace('0b', '').zfill(2)
    if len(add) % 2 == 1: add = add.zfill((len(add)//2+1)*2)
    sbin += bin(len(add)//2 - 1).replace('0b', '').zfill(4)
    stmp = hex(int(sbin,2)).replace('0x', '').zfill(2)
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
        hexbuff = hex(ndata).replace('0x', '').zfill(nlen)[:nlen].upper()
    elif isinstance(ndata, float):
        pass
    return hexbuff

# FRAME{ctrl,master,slaver,segment,buf}
# FRAME = {
# 'CTRL':'43'
# 'FID':'00',
# 'APDU':'',
# 'CTRL_BS':{'C_DIR_bit7':'7_7,0','C_PRM_bit6':'6_6,1','C_AFN_bit50':'0_5',6'}}
def Make_MKIO_Frame(frame):
    # buff = '68'
    ilen = 0
    buff = ''
    buff += frame['CTRL']
    # frame['FID'] = General.inttosHex(ipiid, 2)
    buff += frame['FID']
    ilen += len(frame['APDU'])/2
    buff = makelen(ilen) + buff
    buff += frame['APDU']
    buff = buff + OOP_CalcCRC(buff)
    buff = '68'+ buff + '16'
    return buff

# 'CTRL_BS': {'C_DIR': [7, 7, 0], 'C_PRM': [6, 6, 1], 'C_SEG': [5, 5, 0], 'C_NULL': [4, 4, 0],
# 'C_CODE': [3, 3, 0], 'C_AFN': [0, 2, 3]},
def Get_MKIO_CTRL_BS(data):
    dtmp = {}
    dtmp['C_DIR'] = [7, 7, int(getbit(data, 7, 8, 1), 2)]
    dtmp['C_PRM'] = [6, 6, int(getbit(data, 6, 7, 1), 2)]
    dtmp['C_AFN'] = [0, 5, int(getbit(data, 0, 6, 1), 2)]
    return dtmp

# 'SA_BS': {'SA_TYPE': [6, 7, 0], 'SA_VS': [4, 5, 0], 'SA_LEN': [0, 3, 5]},
# def GetSA_BS(data):
#     dtmp = {}
#     dtmp['SA_TYPE'] = [6, 7, int(getbit(data, 6, 8, 1), 2)]
#     dtmp['SA_VS'] = [4, 5, int(getbit(data, 4, 6, 1), 2)]
#     dtmp['SA_LEN'] = [0, 3, int(getbit(data, 0, 4, 1), 2) + 1 ]
#     return dtmp

# 'SEG_WORD_BS': {'SEG_INDEX': [0, 11, 0], 'SEG_NULL': [12, 13, 0], 'SEG_TYPE': [14, 15, 0]}
# def GetSEG_WORD_BS(data):
#     dtmp = {}
#     dtmp['SEG_INDEX'] = [0, 11, int(getbit(data, 0, 12, 2), 2)]
#     dtmp['SEG_NULL'] = [12, 13, int(getbit(data, 12, 14, 2), 2)]
#     dtmp['SEG_TYPE'] = [14, 15, int(getbit(data, 14, 16, 2), 2)]
#     return dtmp

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

# 解析帧
# ->(True, {'LEN': 3, 'CTRL': '42', 'CTRL_BS': {'C_DIR': [7, 7, 0], 'C_PRM': [6, 6, 1], 'C_AFN': [0, 5, 2]}, 'FID': '01', 'APDU': '020000'})
def Get_MKIO_Frame(buff):
    bretn  = []
    if CheckValid(buff) == False:
        bretn += [False, {}]
        return bretn
    ipos = 0
    while ipos < len(buff):
        if CheckValid(buff[ipos:]) == False:
            # print(buff[ipos:])
            break
        istart = ipos
        dfrm = {}
        ipos += 2
        dfrm['LEN'] = stoint(buff[ipos:ipos+4])
        ipos += 4
        dfrm['CTRL'] = buff[ipos:ipos+2]
        ipos += 2
        dfrm['CTRL_BS'] = Get_MKIO_CTRL_BS(dfrm['CTRL'])
        dfrm['FID'] = buff[ipos:ipos+2]
        ipos += 2
        dfrm['APDU'] = buff[ipos: ipos + dfrm['LEN']*2]
        ipos += dfrm['LEN']*2
        bretn += [True, dfrm]
        ipos += 6
        dfrm['MKZ'] = buff[istart:ipos]
    # print('bretn', bretn)
    return bretn

#  2100->33
def stoint(buff):
    if len(buff) != 4:
        return 0
    return int(reverse(buff), 16)

# 合法帧检查
def CheckValid(buff):
    if len(buff) < MIN_LEN_MKIO_FRAME:
        print('Error_Frame length too short')
        return False
    if buff[0:2] == '68':
        ilen = stoint(buff[2:6])
        # print(buff[2+ilen*2:4+ilen*2])
        # print('CheckValid', ilen, len(buff))
        if (ilen*2+MIN_LEN_MKIO_FRAME) > len(buff):
            print('Error_Frame length')
            return False
        # print('Error_Frame', buff[POS_oop_DATA+ilen*2+4:POS_oop_DATA+ilen*2+6])
        if buff[POS_oop_DATA+ilen*2+4:POS_oop_DATA+ilen*2+6] != '16':
            print('Error_Frame 16')
            return False
        else:
            # print('Error_Frame', buff[POS_oop_LEN:POS_oop_DATA+ilen*2+4])
            if OOP_CheckCRC(buff[POS_oop_LEN:POS_oop_DATA+ilen*2+4]):
                return True
            else:
                print('Error_Frame FCS')
                return False
    print('Error_Frame_Head 68')
    return False

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
    btime += hex(dt.weekday()).replace('0x', '').zfill(2)
    # print(dt.weekday()())
    btime += hex(dt.hour).replace('0x', '').zfill(2)
    btime += hex(dt.minute).replace('0x', '').zfill(2)
    btime += hex(dt.second).replace('0x', '').zfill(2)
    # ms
    btime += hex(dt.microsecond//1000).replace('0x', '').zfill(4)
    return btime

# 20191126 000142 0000->   datetime
def bcdtodatetime(dt):
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
    ds['Req_Type'] = int(buff[2:4], 16)
    ds['Heart_Beat'] = int(buff[4:8],16)
    ds['Req_Time'] = hextodatetime(buff[8:])
    # print(ds)
    return ds

# stime1 datetime  stime2 datetime ->07E3 0B 1A 02 00 012F 135C
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
    hextime += hex(n.year).replace('0x', '').zfill(4)
    hextime += hex(n.month).replace('0x', '').zfill(2)
    hextime += hex(n.day).replace('0x', '').zfill(2)
    hextime += hex(n.hour).replace('0x', '').zfill(2)
    hextime += hex(n.minute).replace('0x', '').zfill(2)
    hextime += hex(n.second).replace('0x', '').zfill(2)
    return  hextime

# 功能配置
ENUM_MK_TYPE = {'MG': 0, 'GPRS': 1, 'PLC': 2, 'RS485': 3, 'YX': 4, 'CAN': 5, 'BUS': 6, 'CTRL': 7, 'PT100': 8, 'RS232': 9,
                'XJY': 11}

# 工作模式
ENUM_IOTYPE = {'CDC-ACM': 1, 'CDC-ECM': 2, 'HID': 3}


# 'RS232' -> 09H
def stypeToHex(stype):
    sHex = ''
    try:
        itype = ENUM_MK_TYPE[stype]
        sHex = General.inttosHex(itype, 2)
    except KeyError:
        print('stypeToHex输入错误参数', stype)
    return sHex

#
def makeResponsebuffbymktype(stype):
    shex = ''
    if stype in ['GPRS', 'YX', 'CTRL', 'PT100', 'XJY', 'RS485', 'PLC', 'BUS', 'CAN', 'RS232']:
        print('makeResponsebuffbymktype ok')
    sys_config = configparser.ConfigParser()
    syspath = os.getcwd().replace('\Protocol', '') + "\config\sysmkIO.ini"
    # print('makeResponsebuffbymktype syspath', syspath)
    sys_config.read(syspath)
    shex += reverse(sys_config.get(stype, "MK_PROTOCOL_VER").zfill(4)[-4:])
    shex += makebydatatype(DT_visible_string, sys_config.get(stype, "MK_SETTYPY"))
    shex += makebydatatype(DT_visible_string, sys_config.get(stype, "MK_SETID"))
    shex += makebydatatype(DT_long_unsigned, sys_config.get(stype, "MK_MAXTD"))
    shex += makebydatatype(DT_long_unsigned, sys_config.get(stype, "MK_MAXRD"))
    shex += makebydatatype(DT_unsigned, int(sys_config.get(stype, "MK_COMNUM")))
    # print('makeResponsebuffbymktype', shex)
    return shex


#  链路协商响应 ，输出响应帧
def make_LINK_APDU_Response(buff_APDU, stype):
    stmp = ''
    if buff_APDU[0:2] == '01':
        # dapdu = analy_LINK_APDU(buff_APDU[2:])
        stmp = '81'
        stmp += makeResponsebuffbymktype(stype)
        if stype in ['GPRS', 'YX', 'CTRL', 'PT100', 'XJY']:
            # stmp += '01'
            stmp += '02'
            # print('ENUM_IOTYPE', ENUM_IOTYPE['CDC-ACM'])
            stmp += General.inttosHex(ENUM_IOTYPE['CDC-ACM'], 2)
            stmp += General.inttosHex(ENUM_MK_TYPE['MG'], 2)
            for i in range(1, 2, 1):
                # stmp += General.inttosHex(DT_enum, 2)
                stmp += General.inttosHex(ENUM_IOTYPE['CDC-ACM'], 2)
                # stmp += General.inttosHex(DT_unsigned, 2)
                stmp += stypeToHex(stype)
        elif stype == 'RS485':
            # stmp += '01'
            stmp += '05'
            stmp += General.inttosHex(ENUM_IOTYPE['CDC-ACM'], 2)
            stmp += General.inttosHex(ENUM_MK_TYPE['MG'], 2)
            for i in range(1, 5, 1):
                # stmp += General.inttosHex(DT_enum, 2)
                stmp += General.inttosHex(ENUM_IOTYPE['CDC-ACM'], 2)
                # stmp += General.inttosHex(DT_unsigned, 2)
                stmp += stypeToHex(stype)
        elif stype in ['PLC', 'BUS', 'CAN', 'RS232']:
            # stmp += '01'
            stmp += '03'
            stmp += General.inttosHex(ENUM_IOTYPE['CDC-ACM'], 2)
            stmp += General.inttosHex(ENUM_MK_TYPE['MG'], 2)
            for i in range(1, 3, 1):
                # stmp += General.inttosHex(DT_enum, 2)
                stmp += General.inttosHex(1, 2)
                # stmp += General.inttosHex(DT_unsigned, 2)
                stmp += stypeToHex(stype)
    return stmp.upper()


ENUM_DAR = {'00': '成功', '01': '拒绝读写', '02': '硬件失效', '03': '信息类未定义', '04': '暂时失效', '05': '对象未定义',
            '06': '对象接口类不符合', '07': '对象不存在', '08': '类型不匹配', '09': '越界', '0A': '数据块不可用', 'FF': '其他'}

# DAR ->解释
def GetErrName(bDAR):
    sErr = ENUM_DAR[bDAR]
    if len(sErr) == 0:
        sErr = '未知错误'
    return sErr


SCALER_UNIT_4 = ['-4','23010700', '23010800', '23010900', '23011000', '1010', '1011', '1012', '1013', '1020', '1021',
                 '1022', '1023', '1030', '1031', '1032', '1033', '1040', '1041', '1042', '1043', '1050', '1051', '1052',
                 '1053', '1060', '1061', '1062', '1063', '1070', '1071', '1072', '1073', '1080', '1081', '1082', '1083',
                 '1090', '1091', '1092', '1093', '10A0', '10A1', '10A2', '10A3', '1110', '1111', '1112', '1113', '1120',
                 '1121', '1122', '1123', '1130', '1131', '1132', '1133', '1140', '1141', '1142', '1143', '1150', '1151',
                 '1152', '1153', '1160', '1161', '1162', '1163', '1170', '1171', '1172', '1173', '1180', '1181', '1182',
                 '1183', '1190', '1191', '1192', '1193', '11A0', '11A1', '11A2', '11A3', '2017', '2018', '2019', '201A',
                 '201B']
SCALER_UNIT_3 = ['-3', '20010200', '2001', '200A']
SCALER_UNIT_2 = ['-2', '0010', '0011', '0012', '0013', '0020', '0021', '0022', '0023', '0030', '0031', '0032',
                 '0033', '0040', '0041', '0042', '0043', '0050', '0051', '0052', '0053', '0060', '0061', '0062', '0063',
                 '0070', '0071', '0072', '0073', '0080', '0081', '0082', '0083', '0090', '0091', '0092', '0093', '00A0',
                 '00A1', '00A2', '00A3', '0110', '0111', '0112', '0113', '0120', '0121', '0122', '0123', '0210', '0211',
                 '0212', '0213', '0220', '0221', '0222', '0223', '0300', '0301', '0302', '0303', '0400', '0401', '0402',
                 '0403', '0500', '0501', '0502', '0503', '200B', '200C', '200D', '200E', '200F', '2011', '2012', '2026',
                 '2027', '2028', '2029', '202C', '202D', '202E', '2031', '2032']
SCALER_UNIT_1 = ['-1', '20000200', '2000', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010']
SCALER_UNIT_BS = ['BS', '2014', '2015', '2040', '2041']

#01---1;00---0
def str0(str):
    if str[0] == '0':
        str = str[1]
    return str
# 无符号数值转换
def hextonum(soad, data):
    sValue = ''
    if soad[:4] in SCALER_UNIT_4:
        fv = int(data, 16) * 0.0001
        sValue += str(float('%.4f' % fv))
    elif soad[:4] in SCALER_UNIT_3:
        fv = int(data, 16) * 0.001
        sValue += str(float('%.3f' % fv))
    elif soad[:4] in SCALER_UNIT_2:
        fv = int(data, 16) * 0.01
        sValue += str(float('%.2f' % fv))
    elif soad[:4] in SCALER_UNIT_1:
        fv = int(data, 16) * 0.1
        sValue += str(float('%.1f' % fv))
    elif soad[:4] in ['0000']:
        # sValue += data
        # sValue += str(int(data, 16))
        version = str0(data[:2]) + '.' + str0(data[2:4]) + '.' + str0(data[4:6]) +'.' + str0(data[6:])
        sValue += version
    elif soad[:4] in SCALER_UNIT_BS:
        pass
    else:
        sValue += str(int(data, 16))
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


# 带符号 '00000000B11FEEE0' ->'297166.0000' DT_long64
def hextolong64(soad,data):
    sValue = ''
    idata = int(data, 16)
    if idata >= 0x8000000000000000:
        idata = idata - 0x10000000000000000
    if soad[:4] in SCALER_UNIT_4:
        fv = idata*0.0001
        sValue = str(float('%.4f' % fv))
    else:
        print('hextolong64 增加处理', soad, data)
    return sValue


# '07E30C04111E28'->'20191204173040'
def hextodatetime_s(data):
    sValue = ''
    sValue += str(int(data[0:4], 16)).zfill(4)
    sValue += str(int(data[4:6], 16)).zfill(2)
    sValue += str(int(data[6:8], 16)).zfill(2)
    sValue += str(int(data[8:10], 16)).zfill(2)
    sValue += str(int(data[10:12], 16)).zfill(2)
    sValue += str(int(data[12:14], 16)).zfill(2)
    return sValue

# '07E30C04'->'20191204'
def hextodate(data):
    sValue = ''
    sValue += str(int(data[0:4], 16)).zfill(4)
    sValue += str(int(data[4:6], 16)).zfill(2)
    sValue += str(int(data[6:8], 16)).zfill(2)
    sValue += str(int(data[8:], 16)).zfill(2)
    return sValue

# '07E30B1A 02 00012F 135C'->'20191126 02 000147 4956'
def hexbufftodatetime(data):
    sValue = ''
    # 年月日
    sValue += str(int(data[0:4], 16)).zfill(4)
    sValue += str(int(data[4:6], 16)).zfill(2)
    sValue += str(int(data[6:8], 16)).zfill(2)
    # 周
    sValue += str(int(data[8:10], 16)).zfill(2)
    # 时分秒
    sValue += str(int(data[10:12], 16)).zfill(2)
    sValue += str(int(data[12:14], 16)).zfill(2)
    sValue += str(int(data[14:16], 16)).zfill(2)
    # 毫秒
    sValue += str(int(data[16:20], 16)).zfill(4)
    return sValue

# 有符号 000007AE->1.996, FFFFEB02->-5.374 DT_double_long
def hextodouble_long(soad,data):
    sValue = ''
    idata = int(data, 16)
    if idata >= 0x80000000:
        idata = idata - 0x100000000
    if soad[:4] in SCALER_UNIT_3:
        fv = idata*0.001
        sValue = str(float('%.3f' % fv))
    elif soad[:4] in SCALER_UNIT_2:
        fv = idata * 0.01
        sValue = str(float('%.2f' % fv))
    elif soad[:4] in SCALER_UNIT_1:
        fv = idata * 0.1
        sValue = str(float('%.1f' % fv))
    elif soad[:4] in ['8000']:
        fv = idata
        sValue = str(float('%.0f' % fv))
    else:
        print('hextodouble_long 增加处理', soad, data)
    return sValue

# 单位
ENUM_ERATED = {'01': '年', '02': '月', '03': '周', '04': '日', '05': '小时', '06': '分', '07': '秒', '08': '度',
               '09': '摄氏度', '0A': '（当地）货币', '0B': '米', '0C': '米/秒', '0D': '立方米', '0E': '立方米',
               '0F': '立方米/小时', '10': '立方米/小时', '11': '立方米/天', '12': '立方米/天', '13': '升', '14': '千克',
               '15': '牛顿', '16': '牛顿米', '17': '帕斯卡', '18': '巴', '19': '焦耳', '1A': '焦每小时', '1B': '瓦',
               '1C': '千瓦', '1D': '伏安', '1E': '千伏安', '1F': '乏', '20': '千乏', '21': '千瓦·时',
               '22': '千伏·安·小时', '23': '千乏·时', '24': '安培', '25': '库仑', '26': '伏特', '27': '伏/米',
               '28': '法拉', '29': '欧姆', '2A': '欧姆米', '2B': '韦伯', '2C': '特斯拉', '2D': '安培/米', '2E': '亨利',
               '2F': '赫兹', '30': '有功能量表常数或脉冲', '31': '无功能量表常数或脉冲', '32': '视在能量表常数或脉冲',
               '33': '百分之', '34': '字节', '35': '分贝毫瓦', '36': '电价', '37': '安时', '38': '毫秒', '39': '发射电平'
               }

# Scaler_Unit 0F04 160D->4(倍率)_立方米
def hextoScaler_Unit(data):
    sValue = ''
    if len(data) < 12:
        return sValue
    ipos = 2
    if data[:ipos] == DT_integer:
        sValue = hextoint(data[ipos: ipos+2])+'_'
        ipos += 2
    else:
        sValue = '未知倍率:'+data[:ipos]+'_'
        ipos += 2
    if data[ipos: ipos+2] == DT_enum:
        ipos += 2
        sValue = hextoint(data[ipos: ipos+2])
    else:
        ipos += 2
        sValue = '未知单位:' + data[ipos: ipos+2]
    return sValue

# 有符号  DT_long
def hextolong(soad,data):
    sValue = ''
    idata = int(data, 16)
    if idata >= 0x8000:
        idata = idata - 0x10000
    if soad[:4] in SCALER_UNIT_3:
        fv = idata*0.001
        sValue = str(float('%.3f' % fv))
    elif soad[:4] in SCALER_UNIT_2:
        fv = idata * 0.01
        sValue = str(float('%.2f' % fv))
    elif soad[:4] in SCALER_UNIT_1:
        fv = idata * 0.1
        sValue = str(float('%.1f' % fv))
    else:
        print('hextolong 增加处理', data)
    return sValue

#报文中的bit_string转为正确的16进制（bit—string在698中是倒置的，例如：8C00->0031）
def bitstrtohex(buffhex):
    b = bin(int(buffhex, 16))[2:].zfill(len(buffhex) * 4)
    c = b[::-1]
    d = hex(int(c, 2))[2:].zfill(len(buffhex)).upper()
    if len(d) == 1: d += '0'
    return d


ENUM_RATED = {'00': '秒', '01': '分', '02': '时', '03': '日', '04': '月', '05': '年'}
CHOICE_MS = {'00': '无表计', '01': '全部用户地址', '02': '一组用户类型', '03': '一组用户地址',
             '04': '一组配置序号', '05': '一组用户类型区间', '06': '一组用户地址区间', '07': '一组配置序号区间'}
def hextoTI(data):
    sValue= ''
    if len(data) >= 6:
        sValue += str(int(data[2:6], 16))
        sValue += ENUM_RATED[data[0:2]]
    return sValue

# 010506000030B00600000000060000000006000030B00600000000->'124.64,0,0,0,124.64,0',ipos
def GetRequestNormalValue(soad, data):
    sValue = ''
    # if len(data) <= 0:
    #     return sValue
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
                                for j in range(0, id, 1):
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
                                                sValue = str(int(data[ipos:ipos + 2], 16))
                                                ipos += 2
                                            elif it5 == DT_unsigned:
                                                sValue += str(int(data[ipos:ipos + 2], 16))
                                                ipos += 2
                                            elif it5 == DT_array or it5 == DT_structure:
                                                print('try5')
                                                print(data[ipos:])
                                            elif it5 == DT_double_long_unsigned:
                                                sValue += hextonum(soad, data[ipos:ipos + 8])
                                                ipos += 8
                                            elif it5 == DT_NULL:
                                                sValue += "'NULL'"
                                            ## 增加elif
                                            else:
                                                print('GetRequestNormalValue it5 增加类型处理')
                                                sValue += data[ipos:]
                                            if k < ie - 1: sValue += ','
                                        sValue += ']'
                                    elif it4 == DT_enum:
                                        sValue = str(int(data[ipos:ipos + 2], 16))
                                        ipos += 2
                                    elif it4 == DT_double_long_unsigned:
                                        sValue += hextonum(soad, data[ipos:ipos + 8])
                                        ipos += 8
                                    elif it4 == DT_NULL:
                                        sValue += "'NULL'"
                                    elif it4 == DT_long_unsigned:
                                        sValue = hextonum('', data[ipos:ipos + 4])
                                        ipos += 4
                                    ##elif 增加
                                    else:
                                        print('try4:', data[ipos:])
                                        sValue += data[ipos:]
                                    if j < id - 1: sValue += ','
                                sValue += ']'
                            elif it3 == DT_enum:
                                sValue += str(int(data[ipos:ipos + 2], 16))
                                ipos += 2
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
                            elif it3 == DT_date_time_s:
                                sValue += "'" + hextodatetime_s(data[ipos:ipos + 14]) + "'"
                                ipos += 14
                            elif it3 == DT_NULL:
                                sValue += "'NULL'"
                            elif it3 == DT_double_long_unsigned:
                                sValue += hextonum(soad, data[ipos:ipos + 8])
                                ipos += 8
                            else:
                                print('try3:', data[ipos:])
                                sValue += data[ipos:]
                            if k < ic-1: sValue += ','
                        sValue += ']'
                    elif it2 == DT_enum:
                        sValue += str(int(data[ipos:ipos + 2], 16))
                        ipos += 2
                    elif it2 == DT_octet_string:
                        octetLen = int(data[ipos:ipos + 2], 16)
                        ipos += 2
                        sValue += "'" + data[ipos: ipos + 2*octetLen] + "'"
                        ipos += 2*octetLen
                    elif it2 == DT_unsigned:
                        sValue += str(int(data[ipos:ipos + 2], 16))
                        ipos += 2
                    elif it2 == DT_long_unsigned:
                        sValue += str(int(data[ipos:ipos + 4], 16))
                        ipos += 4
                    elif it2 == DT_date_time_s:
                        sValue += "'" + hextodatetime_s(data[ipos:ipos + 14]) + "'"
                        ipos += 14
                    elif it2 == DT_double_long_unsigned:
                        sValue += hextonum(soad, data[ipos:ipos + 8])
                        ipos += 8
                    elif it2 == DT_NULL:
                        sValue += "'NULL'"
                    elif it2 == DT_double_long:
                        sValue += hextodouble_long(soad, data[ipos:ipos + 8])
                        ipos += 8
                    elif it2 == DT_date_time:
                        # sValue += "'" + hextodatetime_s(data[ipos:ipos + 14]) + "'"
                        # ipos += 14
                        sValue += "'" + hexbufftodatetime(data[ipos:ipos + 20]) + "'"
                        ipos += 20
                    elif it2 == DT_Scaler_Unit:
                        sValue += "'" + hextoint(data[ipos:ipos + 2])+ "_"
                        ipos += 2
                        sValue += ENUM_ERATED[data[ipos:ipos + 2]]+ "'"
                        ipos += 2
                    else:
                        print('try2', it2, data[ipos:])
                        sValue += data[ipos:]
                    if j < ib - 1: sValue += ','
                sValue += ']'
            elif it1 == DT_date_time_s:
                sValue += "'" + hextodatetime_s(data[ipos:ipos+14]) + "'"
                ipos += 14
            elif it1 == DT_long64:
                sValue += hextolong64(soad, data[ipos:ipos+16])
                ipos += 16
            elif it1 == DT_long_unsigned:
                sValue += hextonum(soad, data[ipos:ipos + 4])
                ipos += 4
            elif it1 == DT_enum:
                sValue += str(int(data[ipos:ipos + 2], 16))
                ipos += 2
            elif it1 == DT_octet_string:
                octetLen =int(data[ipos:ipos + 2], 16)
                ipos += 2
                sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
                ipos += 2 * octetLen
            elif it1 == DT_unsigned:
                sValue += str(int(data[ipos:ipos + 2], 16))
                ipos += 2
            elif it1 == DT_double_long_unsigned:
                sValue += "'" + hextonum(soad, data[ipos:ipos + 8]) + "'"
                ipos += 8
            elif it1 == DT_NULL:
                sValue += "'NULL'"
            elif it1 == DT_double_long:
                sValue += hextodouble_long(soad, data[ipos:ipos + 8])
                ipos += 8
            elif it1 == DT_visible_string:
                sss, ii = General.hextovisiblestring(data[ipos:])
                sValue += "'" + sss + "'"
                ipos += ii
            elif it1 == DT_date:
                sValue += "'" + hextodate(data[ipos:ipos+10]) + "'"
                ipos += 10
            elif it1 == DT_bit_string:
                bitLen = int(data[ipos:ipos + 2], 16)
                ipos += 2
                hexreallen = int(bitLen / 4)
                sValue += "'" + bitstrtohex(data[ipos: ipos + hexreallen]) + "'"
                ipos += hexreallen
            elif it1 == DT_date_time:
                sValue += hexbufftodatetime(data[ipos:ipos + 20])
                ipos += 20
            elif it1 == DT_Scaler_Unit:
                sValue += hextoScaler_Unit(data[ipos:ipos + 4])
                ipos += 4
            else:
                print('try1:', data[ipos:])
                sValue += data[ipos:]
            if i < ia - 1: sValue += ','
        sValue += ']'
    elif it == DT_long64:
        sValue += hextolong64(soad, data[ipos:ipos + 16])
        ipos += 16
    elif it == DT_date_time_s:
        sValue += "'" + hextodatetime_s(data[ipos:ipos + 14]) + "'"
        ipos += 14
    elif it == DT_double_long:
        sValue += hextodouble_long(soad, data[ipos:ipos + 8])
        ipos += 8
    elif it == DT_enum:
        sValue += str(int(data[ipos:ipos + 2], 16))
        ipos += 2
    elif it == DT_octet_string:
        octetLen = int(data[ipos:ipos + 2], 16)
        ipos += 2
        sValue += "'" + data[ipos: ipos + 2 * octetLen] + "'"
        ipos += 2 * octetLen
    elif it == DT_unsigned:
        sValue = hextonum(soad, data[ipos:ipos + 2])
        ipos += 2
    elif it == DT_long_unsigned:
        sValue = hextonum(soad, data[ipos:ipos + 4])
        ipos += 4
    elif it == DT_NULL:
        sValue += "'NULL'"
    elif it == DT_visible_string:
        sss, ii = General.hextovisiblestring(data[ipos:])
        sValue += "'" + sss + "'"
        ipos += ii
    elif it == DT_date:
        sValue += hextodate(data[ipos:ipos + 10])
        ipos += 10
    elif it == DT_bit_string:
        bitLen = int(data[ipos:ipos + 2], 16)
        ipos += 2
        hexreallen = int(bitLen/4)
        sValue += "'" + bitstrtohex(data[ipos: ipos + hexreallen])+"'"
        ipos += hexreallen
    elif it == DT_date_time:
        sValue += hexbufftodatetime(data[ipos:ipos + 20])
        ipos += 20
    elif it == DT_Scaler_Unit:
        sValue += hextoScaler_Unit(data[ipos:ipos+4])
        ipos += 4
    else:
        sValue += data[ipos:]
    print(sValue)
    return sValue, ipos

# 0705000000000003->000000000003,14
def hextoTSA(data):
    ipos = 0
    sValue = ''
    ilen = int(data[ipos:ipos+2])
    ipos += 2
    # ipos += 2
    sValue = data[ipos: ipos + ilen*2]
    ipos += ilen*2
    return sValue, ipos

# DT 解析数据
# 0000 0001 0002 0003只读 0100读写 0200 0201只写
def analy_databyDT(sdt, data):
    tValue = ''
    if sdt == '0000':
        if len(data) < 40:
            tValue += '模块信息:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '模块信息:'+ sss
    elif sdt == '0001':
        if len(data) < 30:
            tValue += '链路协商信息:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '链路协商信息:' + sss
    elif sdt == '0002':
        if len(data) < 4:
            tValue += '协议版本:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '协议版本:' + sss
    elif sdt == '0003':
        if len(data) < 2:
            tValue += '电源状态:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '电源状态:' + sss
    elif sdt == '0004':
        if len(data) < 10:
            tValue += '文件传输状态:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '文件传输状态:' + sss
    elif sdt == '0100':
        if len(data) < 20:
            tValue += '时钟:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '时钟:' + sss
    elif sdt == '0200':
        tValue += '硬件初始化:NULL'
    elif sdt == '0201':
        tValue += '参数初始化:NULL'
    elif sdt == '0202':
        tValue += '数据初始化:NULL'
    elif sdt == '0203':
        if len(data) < 20:
            tValue += '文件传输:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '文件传输:' + sss
    elif sdt == '4000':
        if len(data) < 8:
            tValue += '遥信状态:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '遥信状态:' + sss
    elif sdt == '4001':
        if len(data) < 8:
            tValue += '上一次脉冲计数和时间:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '上一次脉冲计数和时间:' + sss
    elif sdt == '4002':
        if len(data) < 8:
            tValue += '脉冲计数及统计时间:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '脉冲计数及统计时间:' + sss
    elif sdt == '4100':
        if len(data) < 4:
            tValue += '脉冲功能配置:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '脉冲功能配置:' + sss
    elif sdt == '4101':
        if len(data) < 4:
            tValue += '遥信防抖时间(ms):数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '遥信防抖时间:' + sss + 'ms'
    elif sdt == '7100':
        if len(data) < 4:
            tValue += '继电器输出模式:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '继电器输出模式:' + sss
    elif sdt == '7101':
        if len(data) < 6:
            tValue += '继电器输出脉冲宽度:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '继电器输出脉冲宽度:' + sss
    elif sdt == '8000':
        if len(data) < 8:
            tValue += '模拟量采样:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '模拟量采样:' + sss
    elif sdt == '9000':
        if len(data) < 132:
            tValue += '回路状态巡检模块工况信息:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '回路状态巡检模块工况信息:' + sss
    elif sdt == '9001':
        if len(data) < 264:
            tValue += '回路状态巡检模块事件发生时工况信息:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '回路状态巡检模块事件发生时工况信息:' + sss
    elif sdt == '9002':
        if len(data) < 16:
            tValue += '回路状态巡检模块运行信息:数据体长度错误'
        else:
            sss, ii = GetRequestNormalValue(sdt, data)
            tValue += '回路状态巡检模块运行信息:' + sss
    return tValue


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
                sValue += ENUM_DAR[data[ipos:ipos + 2]] + "']"
                ipos += 2
            elif data[ipos:ipos+2] == "01":
                ipos += 2
                lv = GetRequestNormalValue(sOAD, data[ipos:])
                sValue += lv[0] + "']"
                ipos += lv[1]
            else:
                print("getProxyGetRequestListValue 未知结果类型", data[ipos:], sValue)
            if j < ida - 1: sValue += ","
        sValue += "]"
        if i < ilen - 1: sValue += ","
    return sValue

# apdu解析->{'DT':'','Value':['OAD1VALUE,OAD2VALUE,OAD2VALUE,,',,,,,,],
# 'Err':'','Errbuff':'','TimeTag':'','NextAPUD':''}
def analy_DATA_APDU(apdu):
    dvalue = {}
    ipos = 0
    apduType = apdu[ipos:ipos+2]
    ipos += 2
    dvalue['DT'] = ''
    dvalue['Err'] = 'NO'
    dvalue['Errbuff'] = ''
    # ipos += 2
    if apduType == APDU_CONNECT_Request:
        dvalue['Value'] = analy_LinkRequest(apdu[ipos:])
    elif apduType == APDU_CONNECT_Response:
        dvalue['Value'] = analy_LinkResponse(apdu[ipos:])
    elif apduType in [APDU_SET_Request, APDU_GET_Request, APDU_REPORT_Notification_Response]:
        if len(apdu[ipos:]) > 4:
            dvalue['DT'] = apdu[ipos:ipos+4]
            ipos += 4
            dvalue['Value'] = analy_databyDT(dvalue['DT'], apdu[ipos:])
        elif len(apdu[ipos:]) == 4:
            dvalue['DT'] = apdu[ipos:]
            dvalue['Value'] = ''
        else:
            dvalue['Err'] = "YES"
            dvalue['Errbuff'] = apdu[ipos:]
    elif apduType in [APDU_GET_Response, APDU_REPORT_Notification]:
        if len(apdu[ipos:]) > 6:
            dvalue['DT'] = apdu[ipos:ipos+4]
            ipos += 4
            schoice = apdu[ipos:ipos+2]
            ipos += 2
            if schoice == '00':
                dvalue['Value'] = GetErrName(apdu[ipos:ipos+2])
            elif schoice == '01':
                dvalue['Value'] = analy_databyDT(dvalue['DT'], apdu[ipos:])
            else:
                dvalue['Value'] = '位置错误'
        else:
            dvalue['Err'] = "YES"
            dvalue['Errbuff'] = apdu[ipos:]
    elif apduType in [APDU_SET_Response]:
        if len(apdu[ipos:]) == 6:
            dvalue['DT'] = apdu[ipos:ipos+4]
            ipos += 4
            dvalue['Value'] = GetErrName(apdu[ipos:ipos+2])
            ipos += 2
        else:
            dvalue['Err'] = "YES"
            dvalue['Errbuff'] = apdu[ipos:]
    else:
        print('analy_DATA_APDU未定义类型', apduType, apdu[ipos:])
    return dvalue

# LinkRequest解析->{'PIID':'','seq_no':'','seq_type':'' ,'buff':'',,,,,,],
def analy_LinkRequest(apdu):
    tValue = ''
    if len(apdu) < 18:
        tValue += '链路协商请求:数据体长度错误'
    else:
        # sss, ii = GetRequestNormalValue('', apdu)
        ipos = 0
        tValue += '链路协商请求:'
        tValue += '协议版本号:' + apdu[ipos: ipos+4] + ','
        ipos += 4
        sss, ii = General.hextovisiblestring(apdu[ipos:])
        tValue +=  '终端设备型号:' + sss + ','
        ipos += ii
        sss, ii = General.hextovisiblestring(apdu[ipos:])
        tValue += '终端设备ID:' + sss + ','
        ipos += ii
        tValue += '最大发送缓冲长度:' + str(int(apdu[ipos: ipos + 4], 16)) + ','
        ipos += 4
        tValue += '最大接收缓冲长度:' + str(int(apdu[ipos: ipos + 4], 16)) + ','
        ipos += 4
        tValue += '并发传输窗口数:' + str(int(apdu[ipos: ipos + 2], 16))
        ipos += 2
    return tValue

# LinkRequest解析
def analy_LinkResponse(apdu):
    tValue = ''
    if len(apdu) < 18:
        tValue += '链路协商响应:数据体长度错误'
    else:
        # sss, ii = GetRequestNormalValue('', apdu)
        ipos = 0
        tValue += '链路协商响应:'
        tValue += '协议版本号:' + apdu[ipos: ipos+4] + ','
        ipos += 4
        sss, ii = General.hextovisiblestring(apdu[ipos:])
        tValue +=  '终端设备型号:' + sss + ','
        ipos += ii
        sss, ii = General.hextovisiblestring(apdu[ipos:])
        tValue += '终端设备ID:' + sss + ','
        ipos += ii
        tValue += '最大发送缓冲长度:' + str(int(apdu[ipos: ipos + 4], 16)) + ','
        ipos += 4
        tValue += '最大接收缓冲长度:' + str(int(apdu[ipos: ipos + 4], 16)) + ','
        ipos += 4
        tValue += '并发传输窗口数:' + str(int(apdu[ipos: ipos + 2], 16)) + ','
        ipos += 2
        icout = int(int(apdu[ipos: ipos + 2], 16))
        # tValue += '并发传输窗口数:' + str(icout) + ','
        ipos += 2
        svv = '['
        for i in range(0, icout, 1):
            svv += '[' + getkey(ENUM_IOTYPE, int(apdu[ipos: ipos + 2], 16)) + ','
            ipos += 2
            svv += getkey(ENUM_MK_TYPE, int(apdu[ipos: ipos + 2], 16)) + ']'
            ipos += 2
            if i < icout-1:
                svv += ','
        svv += ']'
        tValue += '虚拟通道工作模式:' + svv
    return tValue

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

# buff '6803004201020000B75A16'
# 分析 [bool,CTRL_DATA, FID，{datalist}, APDU,]
# 分析帧-> [True, 2, '01', {'DT': '0000', 'Err': 'NO', 'Errbuff': '', 'APDU_TYPE':'','Value': ''}, '020000', 68...16]
def Receive(buff):
    ll = [False]
    if len(buff) < MIN_LEN_MKIO_FRAME:
        return ll
    stime, sdata = splitframetime(buff)
    ll = []
    # ll += [stime]
    dfme = []
    dfme = Get_MKIO_Frame(sdata)
    print('Receive:Get_MKIO_Frame', dfme, len(dfme))
    ipos = 0
    while ipos < len(dfme):
        ll += [dfme[ipos]]
        if dfme[ipos]:
            if dfme[ipos+1]['CTRL_BS']['C_AFN'][2] == CTRL_DATA:
                ll += [CTRL_DATA]
                ll += [dfme[ipos+1]['FID']]
                dapdu = analy_DATA_APDU(dfme[ipos+1]['APDU'])
                # print('Receive:dapdu', dapdu)
                ll += [dapdu]
                ll += [dfme[ipos+1]['APDU']]
                ll += [dfme[ipos+1]['MKZ']]
            elif dfme[ipos+1]['CTRL_BS']['C_AFN'][2] == CTRL_OK:
                if len(dfme[1]['APDU']) == 0:
                    ll += [CTRL_OK]
                    ll += [dfme[ipos+1]['FID']]
                    ll += ['OK']
                    ll += ['']
                    ll += [dfme[ipos + 1]['MKZ']]
                else:
                    ll += [CTRL_OK]
                    ll += [dfme[ipos+1]['FID']]
                    ll += ['OK_Err']
                    ll += [dfme[ipos+1]['APDU']]
                    ll += [dfme[ipos + 1]['MKZ']]
            elif dfme[ipos+1]['CTRL_BS']['C_AFN'][2] == CTRL_NO:
                if len(dfme[1]['APDU']) == 4:
                    ll += [CTRL_NO]
                    ll += [dfme[ipos+1]['FID']]
                    ll += [GetErrName(dfme[ipos+1]['APDU'][2:])]
                    ll += [dfme[ipos+1]['APDU']]
                    ll += [dfme[ipos + 1]['MKZ']]
                else:
                    ll += [CTRL_NO]
                    ll += [dfme[ipos+1]['FID']]
                    ll += ['NO_Err']
                    ll += [dfme[ipos+1]['APDU']]
                    ll += [dfme[ipos + 1]['MKZ']]
        else:
            ll += [False, '', '', {}, '', '']
        ipos += 2
    # print('Receive:', ll)
    return ll


# 和Excel表中操作名称一致
dMKOPName = {'模组链路协商请求': '01',  '模组链路协商响应': '81', '模组数据读取请求': '02', '模组数据读取响应': '82',
             '模组设置请求': '03', '模组设置响应': '83', '模组上报通知': '04', '模组上报通知响应': '84'}


# 操作描述符->data
def getbuffbyMKOPName(name):
    bdata = ''
    if name in dMKOPName:
        bdata = dMKOPName[name]
    else:
        print('getbuffbyrequest Err')
    return bdata

# 和Excel表中逻辑设备地址名称一致
dVaddr = {'终端': 0, '交采': 1}
# 逻辑设备地址描述->data
def getintbyvaddrname(vaddr):
    bdata = ''
    if vaddr in dVaddr:
        bdata = dVaddr[vaddr]
    else:
        print('getintbyvaddr Err')
    return bdata

# 和Excel表中服务器地址名称一致
dCA = {'单地址': 0, '组地址': 1, '通配地址': 2, '广播地址': 3}
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
# OOP_RSD_CHOICE_VALUE = {'不选择': '00', '选择方法1': '01', '选择方法2': '02', '选择方法3': '03', '选择方法4': '04',
#                  '选择方法5': '05', '选择方法6': '06', '选择方法7': '07', '选择方法8': '08', '选择方法9': '09',
#                  '选择方法10': '0A'}
#
# RSD_NULL = "不选择"
# RSD_Selector1 = "选择方法1"
# RSD_Selector2 = "选择方法2"
# RSD_Selector3 = "选择方法3"
# RSD_Selector4 = "选择方法4"
# RSD_Selector5 = "选择方法5"
# RSD_Selector6 = "选择方法6"
# RSD_Selector7 = "选择方法7"
# RSD_Selector8 = "选择方法8"
# RSD_Selector9 = "选择方法9"
# RSD_Selector10 = "选择方法10"

# 描述CSD Selector数据结构
# OOP_RSD_SelectornDY = {RSD_Selector1: [DT_OAD, ''],
#                      RSD_Selector2: [DT_OAD, '', '', ''],
#                      RSD_Selector3: [DT_array, [DT_OAD, '', '', '']],
#                      RSD_Selector4: [DT_date_time_s, DT_MS],
#                      RSD_Selector5: [DT_date_time_s, DT_MS],
#                      RSD_Selector6: [DT_date_time_s, DT_date_time_s, DT_TI, DT_MS],
#                      RSD_Selector7: [DT_date_time_s, DT_date_time_s, DT_TI, DT_MS],
#                      RSD_Selector8: [DT_date_time_s, DT_date_time_s, DT_TI, DT_MS],
#                      RSD_Selector9: [DT_unsigned],
#                      RSD_Selector10: [DT_unsigned, DT_MS]}

# defing CSD
OOP_CSD = {'0': 'OAD', '1': 'OOP_ROAD'}


# defind ROAD
# OOP_ROAD = [DT_array, [DT_OAD, [DT_array,[DT_OAD]]]]
# OOP_RCSD = [DT_array, [DT_array, [DT_OAD, [DT_array,[DT_OAD]]]]]


# 定义属性结构字 增加完善
MKSXDY = {'0000': [DT_structure, [DT_visible_string, DT_visible_string, DT_double_long_unsigned, DT_date,
                                  DT_double_long_unsigned, DT_date, DT_visible_string]],
          '0001': [DT_structure, [DT_long_unsigned, DT_visible_string, DT_visible_string, DT_long_unsigned,
                                  DT_long_unsigned, DT_unsigned, [DT_array, [DT_structure, [DT_enum, DT_unsigned]]]]],
          '0002': [DT_long_unsigned], '0003': [DT_enum], '0004': [DT_structure], '0100': [DT_date_time],
          '0200': [DT_NULL], '0201': [DT_NULL], '0202': [DT_NULL],
          '0203': [DT_structure, [DT_unsigned, DT_double_long_unsigned, DT_double_long_unsigned,DT_octet_string]],
          '0004': [DT_structure, [DT_double_long_unsigned, DT_bit_string]],
          '4000': [DT_structure, [DT_bit_string, DT_bit_string, [DT_array, [DT_date_time]]]],
          '4001': [DT_array, [DT_structure, [DT_double_long_unsigned, DT_double_long_unsigned]]],
          '4002': [DT_array, [DT_structure, [DT_double_long_unsigned, DT_double_long_unsigned]]],
          '4100': [DT_bit_string], '4101': [DT_long_unsigned], '7100': [DT_enum], '7101': [DT_long_unsigned],
          '8000': [DT_array, [DT_structure, [DT_double_long, DT_Scaler_Unit]]],
          '9000': [DT_structure, [[DT_array, [DT_octet_string]], [DT_array,[DT_octet_string]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  ]],
          '9001': [DT_structure, [[DT_array, [DT_octet_string]], [DT_array,[DT_octet_string]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_octet_string]], [DT_array,[DT_octet_string]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  [DT_array, [DT_double_long_unsigned]], [DT_array, [DT_double_long_unsigned]],
                                  ]],
          '9002': [DT_structure, [[DT_array, [DT_octet_string]], [DT_array, [DT_octet_string]],
                                  [DT_array, [DT_double_long_unsigned]]]]
          }


# 定义数据处理类型集合
OOPSPDATA = [DT_NULL, DT_bool, DT_double_long, DT_double_long_unsigned, DT_integer, DT_long, DT_unsigned,
             DT_visible_string, DT_Scaler_Unit,
             DT_long_unsigned, DT_long64, DT_long64_unsigned, DT_enum, DT_float32, DT_float64, DT_date_time, DT_date,
             DT_time, DT_date_time_s, DT_octet_string, DT_bit_string]
OOPARRATDATA = [DT_array, DT_structure]
OOPVSDATA = [DT_facjtype, DT_sjcjtype]


# True,'True', '01', 1->'01'
def valuetoboolbuff(value):
    bdata = ''
    if isinstance(value, str):
        if value.upper() == 'TRUE' or value == '1' or value == '01':
            bdata += '01'
    elif isinstance(value, float):
        if value > 0:
            bdata += '01'
    elif isinstance(value, bool):
        if value == True:
            bdata += '01'
    else:
        bdata += '00'
    return bdata


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

# 有符号 '-20' -20 ->'EC'
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


# 有符号'EC' '0xEC' 0xEC 0xec->'-20'
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


# '20200117133824' ->'07E401110D2618' date_time_s
def valuetodtsbuff(value):
    bdts = ''
    if len(value) == 0:
        return '07CF0102030405'
    dt = bcdtodatetime(value)
    bdts += hex(dt.year).replace('0x', '').zfill(4)
    bdts += hex(dt.month).replace('0x', '').zfill(2)
    bdts += hex(dt.day).replace('0x', '').zfill(2)
    bdts += hex(dt.hour).replace('0x', '').zfill(2)
    bdts += hex(dt.minute).replace('0x', '').zfill(2)
    bdts += hex(dt.second).replace('0x', '').zfill(2)
    bdts = bdts.upper()
    return bdts


# date_time '20191126000147 4956' ->'07E30B1A 02 00012F 135C'
def valuetodtbuff(value):
    bdts = ''
    if len(value) == 0:
        return '07CF0102030405'
    dt = bcdtodatetime(value)
    bdts += hex(dt.year).replace('0x', '').zfill(4)
    bdts += hex(dt.month).replace('0x', '').zfill(2)
    bdts += hex(dt.day).replace('0x', '').zfill(2)
    bdts += hex(dt.weekday()).replace('0x', '').zfill(2)
    bdts += hex(dt.hour).replace('0x', '').zfill(2)
    bdts += hex(dt.minute).replace('0x', '').zfill(2)
    bdts += hex(dt.second).replace('0x', '').zfill(2)
    # print('dt.microsecond', int(dt.microsecond/1000))
    bdts += hex(int(dt.microsecond/1000)).replace('0x', '').zfill(4)
    bdts = bdts.upper()
    return bdts

# '20200117133824' '20200117' ->07E4011105 date
def valuetodatebuff(value):
    bdts = ''
    if len(value) == 0:
        return '07CF010203'
    if len(value) < 14:
        value += '00000000000000'
    # dt = bcdtodatetime(value)
    # bdts += hex(dt.year).replace('0x', '').zfill(4)
    # bdts += hex(dt.month).replace('0x', '').zfill(2)
    # bdts += hex(dt.day).replace('0x', '').zfill(2)
    # bdts += hex(dt.weekday()).replace('0x', '').zfill
    bdts += hex(int(value[0:4])).replace('0x', '').zfill(4)
    bdts += hex(int(value[4:6])).replace('0x', '').zfill(2)
    bdts += hex(int(value[6:8])).replace('0x', '').zfill(2)
    bdts += hex(int(value[8:10])).replace('0x', '').zfill(2)
    bdts = bdts.upper()
    print('valuetodatebuff bdts', bdts)
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
def valuetolongunsigedbuff(value, scaler):
    sdata = ''
    idata = 0
    if isinstance(value, str):
        idata = int(value)
    elif isinstance(value, int) or isinstance(value, float):
        idata = value
    else:
        print('valuetolongunsigedbuff 未知值', value)
    if scaler == 0:
        sdata += numbertohex(idata, 4)
        # print('valuetolongunsigedbuff 0', sdata)
    elif scaler == -1:
        idata = int(idata*10)
        sdata += numbertohex(idata, 4)
    elif scaler == -2:
        idata = int(idata*100)
        sdata += numbertohex(idata, 4)
    else:
        print('valuetolongunsigedbuff 未知换算', scaler)
        # sdata += numbertohex(idata, 4)
    return sdata

#  '538968849' ->20200311
def valuetodoublelongbuff(value, scaler):
    sdata = ''
    idata = 0
    if isinstance(value, str):
        # print('valuetodoublelongbuff', value)
        idata = int(value)
    elif isinstance(value, int) or isinstance(value, float):
        idata = value
    else:
        print('valuetolongunsigedbuff 未知值', value)
    if scaler == 0:
        sdata += numbertohex(idata, 8)
        # print('valuetolongunsigedbuff 0', sdata)
    elif scaler == -1:
        idata = int(idata*10)
        sdata += numbertohex(idata, 8)
    elif scaler == -2:
        idata = int(idata*100)
        sdata += numbertohex(idata, 8)
    else:
        print('valuetolongunsigedbuff 未知换算', scaler)
        # sdata += numbertohex(idata, 4)
    return sdata


# '0000' -> '020000'
def valuetooctetstringbuff(value):
    sdata = ''
    if isinstance(value, str):
        ilen = len(value)
        sdata += numbertohex(int(ilen/2), 2)
        for i in range(0, ilen, 1):
            sdata += value[i*2: i*2+2]
    else:
        print('valuetooctetstringbuff excel 值类型错误', value)
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
    sdata += getkey(ENUM_RATED, value[ilen-1:ilen+1])
    # print('valuetoTIbuff', value[0:ilen-1])
    sdata += valuetolongunsigedbuff(value[0:ilen-1], 0)
    # print('valuetoTIbuff sdata', value, sdata)
    return sdata

# TI '15分' -> 01000F , RetryMetering[TI, long_unsigned] '5分,3'
def valuetofacjtypebuff(value):
    sdata = ''
    # if value.find('NULL') >= 0:
    #     # print("valuetofacjtypebuff==", value.find('NULL'))
    #     sdata += '00'
    # # TI
    # elif value.find('秒') > 0 or value.find('分') > 0 or value.find('时') > 0 or value.find('日') > 0 or \
    #         value.find('月') > 0 or value.find('年') > 0:
    #     sdata += numbertohex(DT_TI, 2)
    #     sdata += valuetoTIbuff(value)
    # #RetryMetering '5分,3'
    # elif value.find(',') > 0:
    #     RetryMetering = value.split(',')
    #     sdata += numbertohex(DT_structure, 2)
    #     sdata += numbertohex(len(RetryMetering), 2)
    #     if len(RetryMetering) == 2:
    #         sdata += numbertohex(DT_TI, 2)
    #         sdata += valuetoTIbuff(RetryMetering[0])
    #         sdata += numbertohex(DT_long_unsigned, 2)
    #         sdata += valuetolongunsigedbuff(RetryMetering[0], 2)
    #     else:
    #         print('valuetofacjtypebuff RetryMetering 输入错误', value)
    #     pass
    # elif is_number(value):
    #     sdata += numbertohex(DT_unsigned, 2)
    #     sdata += valuetounsignedbuff(value)
    # else:
    #     print('valuetofacjtypebuff 输入错误', value)
    return sdata


# 'MS' '一组用户地址,05000000000003'  ->buff
def valuetoMSbuff(value):
    sdata = ''
    tMS = value.split(",")
    iMS = getkey(CHOICE_MS, tMS[0])
    # if iMS == '00' or iMS == '01':
    #     sdata += iMS
    # # '一组用户类型,2'->
    # elif iMS == '02' and len(tMS) == 2:
    #     sdata += numbertohex(DT_unsigned, 2)
    #     if is_number(tMS[1]):
    #         sdata += numbertohex(int(tMS[1]), 2)
    #     else:
    #         print('valuetoMSbuff iMS=', iMS, value)
    # # '一组用户地址,05000000000003'->
    # elif iMS == '03' and len(tMS) == 2:
    #     sdata += numbertohex(DT_TSA, 2)
    #     sdata += valuetoTSAbuff(tMS[1])
    # # '一组用户地址,05000000000003'->
    # elif iMS == '04' and len(tMS) == 2:
    #     sdata += numbertohex(DT_long_unsigned, 2)
    #     if is_number(tMS[1]):
    #         sdata += valuetolongunsigedbuff(int(tMS[1]), 0)
    #     else:
    #         print('valuetoMSbuff iMS=', iMS, value)
    # elif iMS == '05' and len(tMS) == 2:
    #     print('valuetoMSbuff 增加处理iMS=', iMS, value)
    # elif iMS == '06' and len(tMS) == 2:
    #     print('valuetoMSbuff 增加处理iMS=', iMS, value)
    # elif iMS == '07' and len(tMS) == 2:
    #     print('valuetoMSbuff 增加处理iMS=', iMS, value)
    # else:
    #     print('valuetoMSbuff 未知', iMS, value)
    return sdata

#['20000200', '00300200']
def valuetoDTCSDbuff(value):
    sdata = ''
    # print("valuetoDTCSDbuff===",value)
    iarray = 0
    if isinstance(value, list):
        ilen = len(value)
        # for i in range(0, ilen, 1):
        #     # print("value", value[i], i)
        #     if i == 0 and isinstance(value[i], list):
        #         print('valuetoDTCSDbuff CSD 输入错误', value)
        #         continue
        #     if i < ilen-1:
        #         if isinstance(value[i], list):
        #             pass
        #         elif isinstance(value[i], str) and isinstance(value[i + 1], str):
        #             sdata += numbertohex(DT_CSD, 2)
        #             sdata += '00'
        #             sdata += value[i]
        #             iarray += 1
        #         elif isinstance(value[i], str) and isinstance(value[i + 1], list):
        #             sdata += numbertohex(DT_CSD, 2)
        #             sdata += '01'
        #             sdata += value[i]
        #             iROAD = len(value[i + 1])
        #             sdata += numbertohex(iROAD, 2)
        #             for j in range(0, iROAD, 1):
        #                 sdata += value[i + 1][j]
        #             iarray += 1
        #     elif i == ilen-1:
        #         if isinstance(value[i], list):
        #             pass
        #         elif isinstance(value[i], str):
        #             sdata += numbertohex(DT_CSD, 2)
        #             sdata += '00'
        #             sdata += value[i]
        #             iarray += 1
        # sdata = numbertohex(iarray, 2) + sdata
        # print('sdata=', sdata)
    else:
        print('valuetoDTCSDbuff输入值错误 非list', value)
    return sdata


# Scaler_Unit 4(倍率)_立方米->0F04 160D
def valuetoScaler_Unitbuff(value):
    sdata = ''
    tvv = value.split("_")
    if len(tvv) < 2:
        return sdata
    # sdata += inttohex(DT_integer)
    sdata += inttohex(int(tvv[0]))
    # sdata += inttohex(DT_enum)
    sdata += getkey(ENUM_ERATED, tvv[1])
    return sdata

# 'LIN YANG CTRL MOUDLE'-> '14 4C494E2059414E47204354524C204D4F55444C45'
def valuetovisiblestringbuff(value):
    sdata = ''
    if isinstance(value, str):
        valuelase, ilen = General.visibletobuff(value)
        sdata += General.makeXDR(ilen)
        sdata += valuelase
    else:
        print('valuetovisiblestringbuff excel 值类型错误', value)
        sdata += '00'
    return sdata

# '0031'->'108C00'
def valuetobitstringbuff(value):
    sdata = ''
    if isinstance(value, str):
        ilen = len(value)*4
        sdata += numbertohex(int(ilen), 2)
        sdata += bitstrtohex(value)
    else:
        print('valuetobitstringbuff excel 值类型错误', value)
        sdata += '00'
    return sdata

# dtype 数据类型，value数值 ->buff
def makebydatatype(dtype, value):
    bdata = ''
    if dtype == DT_NULL:
        bdata += ''
    elif dtype == DT_bool:
        bdata += valuetoboolbuff(value)
    elif dtype == DT_unsigned or dtype == DT_enum:
        bdata += valuetounsignedbuff(value)
    elif dtype == DT_integer:
        bdata += inttohex(value)
    elif dtype == DT_date_time_s:
        bdata += valuetodtsbuff(value)
    elif dtype == DT_long_unsigned:
        bdata += valuetolongunsigedbuff(value, 0)
    elif dtype == DT_octet_string:
        bdata += valuetooctetstringbuff(value)
    elif dtype == DT_facjtype:
        bdata += valuetofacjtypebuff(value)
        # print('makebydatatype 完成处理类型DT_facjtype==', dtype, value, bdata)
    elif dtype == DT_Scaler_Unit:
        bdata += valuetoScaler_Unitbuff(value)
    elif dtype == DT_visible_string:
        bdata += valuetovisiblestringbuff(value)
    elif dtype == DT_bit_string:
        # print('DT_bit_string', value)
        bdata += valuetobitstringbuff(value)
    elif dtype == DT_date_time:
        bdata += valuetodtbuff(value)
    elif dtype == DT_date:
        bdata += valuetodatebuff(value)
    elif dtype == DT_double_long_unsigned:
        bdata += valuetodoublelongbuff(value, 0)
        # print('makebydatatype DT_double_long_unsigned ', value,bdata)
    elif dtype == DT_double_long:
        bdata += valuetodoublelongbuff(value, 0)
    else:
        print('makebydatatype 增加处理类型', dtype, value)
    return bdata

# DT= []  param [] 生成buff
def make_GETSET_Response(oadoam, param):
    bdata = ''
    if oadoam in MKSXDY:
        bdata += numbertohex(MKSXDY[oadoam][0], 2)
        if MKSXDY[oadoam][0] == DT_date_time_s:
            bdata += valuetodtsbuff(param)
        elif MKSXDY[oadoam][0] == DT_enum:
            bdata += makebydatatype(MKSXDY[oadoam][0], param)
        elif MKSXDY[oadoam][0] == DT_NULL:
            bdata += makebydatatype(MKSXDY[oadoam][0], param)
        elif MKSXDY[oadoam][0] == DT_structure:
            lparam = strtolist(param)
            if len(MKSXDY[oadoam][1]) != len(lparam):
                bdata += numbertohex(0, 2)
                print('make_GETSET_Response DT_structure excel对应输入参数有误:', param)
            else:
                bdata += numbertohex(len(MKSXDY[oadoam][1]),2)
                for i in range(0, len(MKSXDY[oadoam][1]), 1):
                    bdata += numbertohex(MKSXDY[oadoam][1][i], 2)
                    if MKSXDY[oadoam][1][i] in OOPSPDATA:
                        bdata += makebydatatype(MKSXDY[oadoam][1][i], lparam[i])
                    elif MKSXDY[oadoam][1][i] in OOPARRATDATA:
                        print('make_GETSET_Response OOPARRATDATA 增加处理:', MKSXDY[oadoam][1][i], param[i])
                    elif isinstance(MKSXDY[oadoam][1][i],list):
                        if MKSXDY[oadoam][1][i][0] in OOPSPDATA:
                            print('make_GETSET_Response OOPSPDATA  增加处理:', MKSXDY[oadoam][1][i][0], param[i])
                            pass
                        elif MKSXDY[oadoam][1][i][0] == DT_array:
                            bdata += numbertohex(MKSXDY[oadoam][1][i][0], 2)
                            print('param[i]', MKSXDY[oadoam][1][i][0],lparam[i],MKSXDY[oadoam][1])
                            bdata += numbertohex(len(lparam[i]), 2)
                            for j in range(0, len(lparam[i]), 1):
                                if MKSXDY[oadoam][1][i][1][0] in OOPSPDATA:
                                    bdata += numbertohex(MKSXDY[oadoam][1][i][1][0], 2)
                                    bdata += makebydatatype(MKSXDY[oadoam][1][i][1][0], lparam[i][j])
                                else:
                                    pass
                                    # print('make_GETSET_Response list  增加处理:', MKSXDY[oadoam][1][i][1], param[i])
                        else:
                            print('make_GETSET_Response list  增加处理:', MKSXDY[oadoam][1][i][0], param[i])
                    else:
                        print('make_GETSET_Response DT_structure  增加处理:', MKSXDY[oadoam][1][i], param[i])
        elif MKSXDY[oadoam][0] == DT_array:
            lparam = strtolist(param)
            bdata += numbertohex(len(lparam), 2)
            if len(lparam) == 0:
                print('make_GETSET_Response DT_array excel 111对应输入参数有误:', param)
            else:
                if MKSXDY[oadoam][1][0] in OOPSPDATA:
                    # bdata += makebydatatype(MKSXDY[oadoam][1][i], lparam[i])
                    print("增加处理oad")
                    pass
                elif MKSXDY[oadoam][1][0] == DT_structure:
                    for item in lparam:
                        bdata += numbertohex(MKSXDY[oadoam][1][0], 2)
                        bdata += numbertohex(len(item), 2)
                        if len(item) == 0:
                            pass
                        elif len(MKSXDY[oadoam][1][1]) != len(item):
                            print('make_GETSET_Response DT_array excel 222对应输入参数有误:', param)
                        else:
                            for i in range(0, len(MKSXDY[oadoam][1][1]), 1):
                                # print('MKSXDY[oadoam][1][1][i]==', MKSXDY[oadoam][1][1][i])
                                if isinstance(MKSXDY[oadoam][1][1][i], list):
                                    if MKSXDY[oadoam][1][1][i][0] == DT_structure:
                                        bdata += numbertohex(MKSXDY[oadoam][1][1][i][0], 2)
                                        bdata += numbertohex(len(item[i]), 2)
                                        if len(item[i]) == 0:
                                            print('pass1')
                                            pass
                                        elif len(MKSXDY[oadoam][1][1][i][1]) == len(item[i]):
                                            for j in range(0, len(MKSXDY[oadoam][1][1][i][1]), 1):
                                                bdata += numbertohex(MKSXDY[oadoam][1][1][i][1][j], 2)
                                                if MKSXDY[oadoam][1][1][i][1][j] in OOPSPDATA:
                                                    # print('dd', MKSXDY[oadoam][1][1][i][1][j], item[i][j])
                                                    bdata += makebydatatype(MKSXDY[oadoam][1][1][i][1][j], item[i][j])
                                                elif MKSXDY[oadoam][1][1][i][1][j] in OOPARRATDATA:
                                                    print(
                                                        'make_GETSET_Response MKSXDY[oadoam][1][1][i][1][j] in OOPARRATDATA',
                                                        MKSXDY[oadoam][1][1][i][1][j])
                                                elif isinstance(MKSXDY[oadoam][1][1][i][1][j], list):
                                                    if MKSXDY[oadoam][1][1][i][1][j][0] == DT_array:
                                                        bdata += numbertohex(MKSXDY[oadoam][1][1][i][1][j][0], 2)
                                                        bdata += numbertohex(len(item[i][j]), 2)
                                                        for item1 in item[i][j]:
                                                            if MKSXDY[oadoam][1][1][i][1][j][1][0] in OOPSPDATA:
                                                                bdata += numbertohex(
                                                                    MKSXDY[oadoam][1][1][i][1][j][1][0], 2)
                                                                bdata += makebydatatype(MKSXDY[oadoam][1][1][i][1][j][1][0], item1)
                                                            elif MKSXDY[oadoam][1][1][i][1][j][1][0] == DT_structure:
                                                                bdata += numbertohex(MKSXDY[oadoam][1][1][i][1][j][1][0], 2)
                                                                bdata += numbertohex(len(MKSXDY[oadoam][1][1][i][1][j][1][1]), 2)
                                                                # print('MKSXDY[oadoam][1][1][i][1][j][1][1]',MKSXDY[oadoam][1][1][i][1][j][1][1])
                                                                if len(MKSXDY[oadoam][1][1][i][1][j][1][1]) == 0:
                                                                    pass
                                                                elif len(MKSXDY[oadoam][1][1][i][1][j][1][1]) == len(item1):
                                                                    for k in range(0, len(MKSXDY[oadoam][1][1][i][1][j][1][1]), 1):
                                                                        if MKSXDY[oadoam][1][1][i][1][j][1][1][k] in OOPSPDATA:
                                                                            bdata += numbertohex(
                                                                                MKSXDY[oadoam][1][1][i][1][j][1][1][k], 2)
                                                                            bdata += makebydatatype(
                                                                                MKSXDY[oadoam][1][1][i][1][j][1][1][k],
                                                                                item1[k])
                                                                        else:
                                                                            print(
                                                                                'MKSXDY[oadoam][1][1][i][1][j][1][1][k] 2',
                                                                                MKSXDY[oadoam][1][1][i][1][j][1][1][k])
                                                                else:
                                                                    print('MKSXDY[oadoam][1][1][i][1][j][1][1][k] 2',
                                                                          MKSXDY[oadoam][1][1][i][1][j][1][1][k])
                                                    else:
                                                        print(
                                                            'make_GETSET_Response MKSXDY[oadoam][1][1][i][1][j][0]',
                                                            MKSXDY[oadoam][1][1][i][1][j][0], item[i][j])
                                                elif MKSXDY[oadoam][1][1][i][1][j] in OOPVSDATA:
                                                    bdata = bdata[:-2]
                                                    bdata +=  makebydatatype(MKSXDY[oadoam][1][1][i][1][j], item[i][j])
                                                    # print("MKSXDY[oadoam][1][1][i][1][j] in OOPVSDATA", MKSXDY[oadoam][1][1][i][1][j], item[i][j])
                                                else:
                                                    print(
                                                        'make_GETSET_Response MKSXDY[oadoam][1][1][i][1][j] else',
                                                        MKSXDY[oadoam][1][1][i][1][j], item[i][j])
                                        else:
                                            print('make_GETSET_Response MKSXDY[oadoam][1][1][i][1][j] else 111')
                                    elif MKSXDY[oadoam][1][1][i][0] == DT_array:
                                        bdata += numbertohex(MKSXDY[oadoam][1][1][i][0], 2)
                                        bdata += numbertohex(len(item[i]), 2)
                                        if len(item[i]) == 0:
                                            pass
                                        elif len(MKSXDY[oadoam][1][1][i][1]) == len(item[i]):
                                            print('make_GETSET_Response MKSXDY[oadoam][1][1][i][0]', item[i])
                                        # elif MKSXDY[oadoam][1][1][i][1][0] == DT_CSD:
                                        #     bdata = bdata[:-2]
                                        #     bdata += makebydatatype(MKSXDY[oadoam][1][1][i][1][0], item[i])
                                            # print('MKSXDY[oadoam][1][1][i][1][0]==DT_CSD:',MKSXDY[oadoam][1][1][i][1][0], item[i])
                                        else:
                                            print("MKSXDY[oadoam][1][1][i][1]增加处理", MKSXDY[oadoam][1][1][i][1],
                                                  item[i])
                                    else:
                                        print('make_GETSET_Response MKSXDY[oadoam][1][1][i][0]', MKSXDY[oadoam][1][1][i][0])
                                elif MKSXDY[oadoam][1][1][i] in OOPSPDATA:
                                    bdata += numbertohex(MKSXDY[oadoam][1][1][i], 2)
                                    bdata += makebydatatype(MKSXDY[oadoam][1][1][i], item[i])
                                else:
                                    print('make_GETSET_Response MKSXDY[oadoam][1][1][i]] ddd', MKSXDY[oadoam][1][1][i], item[i])
                elif MKSXDY[oadoam][1][0] == DT_array:
                    print('make_GETSET_Response MKSXDY[oadoam][1][1][i][1][j] DT_array')
                else:
                    print('make_GETSET_Response DT_array其他参数类型处理', param)
        else:
            print('make_GETSET_Response 增加处理 ', oadoam)
    else:
        print('make_GETSET_Response 增加[MKSXDY]定义处理', oadoam, param)
    return bdata


# '模组数据读取请求','0000' ,[LIN YANG CTRL MOUDLE,NJLY-CTRL-0001,2.56,20191111,2.56,20191111,NJLY]
# '模组数据读取请求响应'
def make_MKIO_APDU_Response(response_name, sDT, dparam):
    buff = ''
    bOPtype = getbuffbyMKOPName(response_name)
    buff += bOPtype
    buff += sDT
    if bOPtype in [APDU_GET_Response, APDU_REPORT_Notification]:
        if len(dparam) == 0:
            buff += '00'
            buff += 'FF'
        elif sDT in ['0000', '0004', '4000', '4001', '4002', '8000']:
            sparam = make_GETSET_Response(sDT, dparam)
            buff += '01'
            buff += sparam
        elif sDT in ['9000', '9001', '9002', '9003']:
            if len(dparam) >= 4:
                buff += '01'
                buff += dparam
            else:
                buff += '00'
                buff += dparam
        elif dparam[0] == 0:
            sparam = make_GETSET_Response(sDT, dparam)
            if len(sparam) == 0:
                buff += '00'
                buff += '01'
            else:
                buff += '01'
                buff += sparam
        elif dparam[0] in [1, 2, 255]:
            buff += '00'
            buff += General.inttosHex(dparam[0], 2)
    elif bOPtype == APDU_SET_Response:
        if len(dparam) == 0:
            buff += '00'
        else:
            buff += General.inttosHex(dparam[0], 2)
    elif bOPtype == APDU_SET_Request:
        if len(dparam) == 0:
            pass
        else:
            sparam = make_GETSET_Response(sDT, dparam)
            buff += sparam
    elif bOPtype in [APDU_GET_Request, APDU_REPORT_Notification_Response]:
        pass
    else:
        print('make_MKIO_APDU_Response未处理类型增加处理', response_name)
    return buff

# 依据接收报文sRx响应 bRes True 响应确认帧， False 响应否认帧
# sRx '[2018-12-03-10:10:51:859]680E00422D0301001907E4081C00112E070031EC0216'
# buff 680400C22D8201000120D916
def make_MKIO_Response(sRx, bRes=True):
    buff = ''
    qqtt = Receive(sRx)
    frm = {}
    print('qqtt',qqtt)
    if qqtt[1] == 2:
        frm['CTRL'] = 'C2'
    else:
        print("make_MKIO_Response接收为非设置请求帧", sRx)
        return buff
    frm['FID'] = qqtt[2]
    apdu = hex(int(qqtt[4][:2], 16) + 0x80)[2:].zfill(2)
    sapdu = apdu
    sapdu += qqtt[3]['DT']
    if bRes:
        sapdu += '00'
    else:
        sapdu += '01'
    frm['APDU'] = sapdu
    buff += Make_MKIO_Frame(frm)
    return buff


# srev '682300425B01000011456E6572677920436F6E74726F6C6C65720830303030303030310400040001FB8E16'字符串
# return  [1(链路协议数据), FIID, senddata, {datalist}, apdu[:2], FID, '68...16']
# return  [2(模组协议数据), FIID, b'h0\x00\x01\x05\x03\x00'， {datalist}, apdu[:2],FIDm,'68...16']
def islinkorappReturn(srev, stype):
    relst = []
    # revhex = General.hexShow(srev)
    revhex = srev.replace(' ', '')
    revhex = srev.replace(':', '')
    ll = Receive(revhex)
    # print('islinkReturn_Receive_ll', ll)
    ipos = 0
    while ipos < len(ll):
        if ll[ipos] and ll[ipos+1] == CTRL_DATA and ll[ipos+4][:2] in LINK_APDU_SET:
            relst += [1]
            relst += [ll[ipos+2]]
            frm = {}
            frm['CTRL'] = 'C2'
            frm['FID'] = ll[ipos+2]
            frm['APDU'] = make_LINK_APDU_Response(ll[ipos+4], stype)
            sfr = Make_MKIO_Frame(frm)
            # print('islinkorappReturn sfr', sfr)
            relst += [sfr]
            relst += [ll[ipos+4]]
            relst += [ll[ipos+4][:2]]
            relst += [ll[ipos + 5]]
        elif ll[ipos] and ll[ipos+1] == CTRL_DATA and ll[ipos+4][:2] in APDU_SET:
            relst += [2]
            relst += [ll[ipos+2]]
            relst += [ll[ipos+3]]
            relst += [ll[ipos+4]]
            relst += [ll[ipos+4][:2]]
            relst += [ll[ipos + 5]]
        else:
            relst += [0, '00', revhex, '', '', '']
        ipos += 6
    print('islinkorappReturn', relst)
    return relst

# srev '682300425B01000011456E6572677920436F6E74726F6C6C65720830303030303030310400040001FB8E16'字符串
# return  [0(其他协议数据), FIID, apdu[:2]]
# return  [1(链路协议数据), FIID, apdu[:2]]
# return  [2(模组协议数据), FIID, apdu[:2]]
# 无响应帧， 未处理 680E0042050301001907E40B0D0012122A01B95D9516680F00020F820100011907E40B0D0012130301D9617316
def islinkorapp(srev):
    relst = []
    # revhex = General.hexShow(srev)
    revhex = srev.replace(' ', '')
    revhex = srev.replace(':', '')
    ll = Receive(revhex)
    # print('islinkorapp', ll, len(ll))
    # for i in range(0, len(ll), 2):
    ipos = 0
    while ipos < len(ll):
        if ll[ipos] and ll[ipos+1] == CTRL_DATA and ll[ipos+4][:2] in LINK_APDU_SET:
            relst += [ipos+1]
            relst += [ll[ipos+1]]
            relst += [ll[ipos+4][:2]]
        elif ll[ipos] and ll[ipos+1] == CTRL_DATA and ll[ipos+4][:2] in APDU_SET:
            relst += [2]
            relst += [ll[ipos+1]]
            relst += [ll[ipos+4][:2]]
        else:
            relst += [0]
            relst += ['NULL']
            relst += [revhex]
        ipos += 6
    # print('islinkorapp', relst)
    return relst


if __name__ == '__main__':
    frm = {}
    frm['CTRL'] = '42'
    frm['FID'] = General.inttosHex(1, 2)
    # # frm['APDU'] = make_LINK_APDU_Response('01', 'PT100')
    dpr = strtolist("['00','F0',['202007151135400020','202007151135400020','202007151135400020','202007151135400020']]")
    dpr = "['0','F',['202007151135400020','202007151135400020','202007151135400020','202007151135400020']]"
    # frm['APDU'] = make_MKIO_APDU_Response('模组上报通知', '4000', dpr)
    frm['APDU'] = make_MKIO_APDU_Response('模组数据读取请求', '0000', '')
    print('make_MKIO_APDU_Response', frm['APDU'])
    ss = Make_MKIO_Frame(frm)
    print('Make_MKIO_Frame:', ss)
    # tt = Get_MKIO_Frame(ss)
    # print('Get_MKIO_Frame', tt)
    ss = '686400C2038200000102070A0E47424831332d53434443563131300A303031303239433031433146423430354135413432343830303030303130374146333736413046313833363445433843300601343B771A07E4030B0306013265E51A07E4030B030A0453435343D39D16'
    ss = '680500429D0371001600FCDB16'
    ss = '68 33 00 C2 01 82 00 00 01 02 07 0A 08 54 4C 59 32 39 34 30 41 0A 07 4C 59 35 30 30 30 38 06 00 00 01 00 1A 07 E6 05 1F 02 06 00 00 01 00 1A 07 E6 05 1F 02 0A 02 4C 59 6F 76 16'

    tt = Receive(ss)
    print('tt Receive', tt)
    # tt = islinkorappReturn(ss, 'GPRS')
    # print('islinkorappReturn tt',tt)
    tt = islinkorapp(ss)
    print('la',tt)
    # ssss = make_MKIO_Response(ss, False)
    # print('ssss', ssss)
    # analy_DATA_APDU('82900101024001030901020901020901020100010306000001E106000001EA06000001AC01030600003A0306000037300600003806010306000039F1060000371A06000037FB01030600000000060000000006000000000103060000003206000000320600000032010306000000030600000002060000000501030600000DAC0600000DAC0600000DAC0103060000006406000000640600000064010306000000000600000002060000000301030600000DAC0600000DAC0600000DAC0103060000009606000000960600000096010306000000040600000001060000000401030600000DAC0600000DAC0600000DAC0100010001000100010001000100010001000100010001000100010001000100010001030901000901000901000100010306000000000600000000060000000001030600000000060000000006000000000103060000000006000000000600000000010306000000000600000000060000000001030600000000060000000006000000000103060000000006000000000600000000010306000000000600000000060000000001030600000000060000000006000000000103060000000006000000000600000000010306000000000600000000060000000001030600000000060000000006000000000103060000000006000000000600000000010306000000000600000000060000000001000100010001000100010001000100010001000100010001000100010001000100')
    # ss = '[2018-12-03-10:10:51:859]6803004201020000B75A16'
    # tt = Receive(ss)
    # print(islinkorappReturn('68030042C5020000821316', 'GPRS'))
    print('inttohex', inttohex('-2'))