import datetime
import time
import PublicLib.public as pfun

para1cfg = {'最大需量周期': '01',
            '滑差时间': '01',
            '校表脉冲宽度': '0001',
            '两套时区表切换时间': '19010203',
            '两套日时段表切换时间': '19040506',
            '两套分时费率切换时间': '19070809',
            '两套阶梯切换时间': '19101112',
            }

para2cfg = {'年时区数': '01',
            '日时段表数': '01',
            '日时段数': '01',
            '费率数': '03',
            '公共假日数': '0016',
            '谐波分析次数': '02',
            '梯度数': '04',
            }

para3cfg = {'电流互感器变比': '000005',
            '电压互感器变比': '000001',
            }

def readpara1(DI):
    strdata = ''
    # YYMMDDWW         4         日期及星期(其中0代表星期天)
    # hhmmss           3         时间
    # NN               1         最大需量周期
    # NN               1         滑差时间
    # XXXX             2         校表脉冲宽度
    # YYMMDDhhmm       5         两套时区表切换时间
    # YYMMDDhhmm       5         两套日时段表切换时间
    # YYMMDDhhmm       5         两套分时费率切换时间
    # YYMMDDhhmm       5         两套阶梯切换时间
    if DI[3] == 0x01:  # 日期及星期(其中0代表星期天)
        t = time.time()
        dt_obj = datetime.datetime.fromtimestamp(t)
        strdata = dt_obj.strftime("0%w%d%m%y")
    elif DI[3] == 0x02:  # 时间
        t = time.time()
        dt_obj = datetime.datetime.fromtimestamp(t)
        strdata = dt_obj.strftime("%S%M%H")
    elif DI[3] == 0x03:
        strdata = para1cfg['最大需量周期']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x04:
        strdata = para1cfg['滑差时间']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x05:
        strdata = para1cfg['最大需量周期']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x06:
        strdata = para1cfg['两套时区表切换时间']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x07:
        strdata = para1cfg['两套日时段表切换时间']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x08:
        strdata = para1cfg['两套分时费率切换时间']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x09:
        strdata = para1cfg['两套阶梯切换时间']
        strdata = pfun._strReverse(strdata)
    return strdata


def readpara2(DI):
    strdata = ''

    # 年时区数 p≤14
    # 日时段表数 q≤8
    # 日时段数(每日切换数) m≤14
    # 费率数 k≤63
    # 公共假日数 n≤254
    # 谐波分析次数
    # 梯度数
    if DI[3] == 0x01:
        strdata = para2cfg['年时区数']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x02:
        strdata = para2cfg['日时段表数']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x03:
        strdata = para2cfg['日时段数']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x04:
        strdata = para2cfg['费率数']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x05:
        strdata = para2cfg['公共假日数']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x06:
        strdata = para2cfg['谐波分析次数']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x07:
        strdata = para2cfg['梯度数']
        strdata = pfun._strReverse(strdata)
    return strdata

def readpara3(DI):
    strdata = ''

    # 电流互感器变比
    # 电压互感器变比
    if DI[3] == 0x06:
        strdata = para3cfg['电流互感器变比']
        strdata = pfun._strReverse(strdata)
    elif DI[3] == 0x07:
        strdata = para3cfg['电压互感器变比']
        strdata = pfun._strReverse(strdata)
    return strdata

def readexinfo(DI, DevType):
    strdata = ''

    # 2937设备类型
    if DI[3] == 0x01 and DevType == '2937': # TLY2937-SW-V1.0
        strdata = '544c59323933372d53572d56312e300000000000000000000000000000000000'
    elif DI[3] == 0x01 and DevType == '2315': # TLY2315-SW-V1.0
        strdata = '544c59323331352d53572d56312e300000000000000000000000000000000000'
    return strdata

def dl645_readpara(DI, DevType):
    strdata = ''

    if DI[1] == 0x00:
        if DI[2] == 0x01:
            strdata = readpara1(DI)
        elif DI[2] == 0x02:
            strdata = readpara2(DI)
        elif DI[2] == 0x03:
            strdata = readpara3(DI)
    elif DI[1] == 0x80: # 自定义扩展信息
        if DI[2] == 0x00:
            strdata = readexinfo(DI, DevType)
    return strdata


def dl645_readdate():
    pass
