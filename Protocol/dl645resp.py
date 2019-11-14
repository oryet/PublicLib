import sys
import numpy as np
import datetime

sys.path.append('../')
from PublicLib.public import calcCheckSum
import PublicLib.public as pfun

# 645报文各元素的位置
POS_64507_HEAD = 0
POS_64507_ADDR = 2  # 1
POS_64507_HEAD2 = 14  # 7
POS_64507_CTRL = 16  # 8
POS_64507_LEN = 18  # 9
POS_64507_DATA = 20  # 10

# 645报文最小长度
MIN_LEN_645FRAME = 24  # 12

HEAD_FRAME = 'FEFEFEFE'


# en -33
def str2hex(strdata, en=0):
    data = []
    for j in range(0, len(strdata), 2):
        s = strdata[j:j + 2]
        if en:
            try:
                s = int(s, 16) - 0x33
            except:
                pass
        else:
            try:
                s = int(s, 16)
            except:
                pass
        data += [s]
    return data


# en +33
def hex2str(hexdata, en=0):
    s = ''
    for j in range(len(hexdata)):
        if en:
            try:
                ss = hex(hexdata[j] + 0x33)
            except:
                pass
        else:
            try:
                ss = hex(hexdata[j])
            except:
                pass
        ss = ss.replace('0x', '00')
        ss = ss[-2:]
        # s += hex(hexdata[j]).replace('0x', '00')[-2:0]
        s += ss
    return s


def dl645_dealframe(frame):
    frame = frame.replace(' ', '')
    if len(frame) < MIN_LEN_645FRAME:
        return False, None
    frame = frame.upper()
    dt = {'addr': '', 'ctrl': '', 'data': ''}
    for i in range(0, len(frame), 2):
        if frame[i:i + 2] == '68' and frame[(i + POS_64507_HEAD2):(i + POS_64507_HEAD2) + 2] == '68':
            dataLen = int(frame[(i + POS_64507_LEN):(i + POS_64507_LEN + 2)], 16) * 2
            if dataLen + POS_64507_LEN < len(frame):
                frameLen = i + dataLen + POS_64507_LEN
                checkSum = calcCheckSum(frame[i:(frameLen + 2)])
                checkSum = checkSum[-2:]
                checkSum = checkSum.upper()
                if checkSum == frame[frameLen + 2:frameLen + 4] and \
                                frame[frameLen + 4:frameLen + 6] == '16':
                    addr = frame[i + POS_64507_ADDR:i + POS_64507_ADDR + 12].upper()
                    dt['addr'] = pfun._strReverse(addr)
                    # dt['ctrl'] = frame[i + POS_64507_CTRL:i + POS_64507_CTRL + 2]
                    dt['ctrl'] = int(frame[i + POS_64507_CTRL:i + POS_64507_CTRL + 2], 16)
                    # dt['data'] = frame[i + POS_64507_DATA:i + POS_64507_DATA + dataLen]
                    datastr = frame[i + POS_64507_DATA:i + POS_64507_DATA + dataLen]
                    dt['data'] = str2hex(datastr, 1)

                    if dt['ctrl'] & 0x80 == 0:  # 只响应抄读帧
                        return True, dt
    return False, None


# 十六进制 转 字符串 再 组帧
def dl645_makeframe(dt):
    # datavalue 转换

    if 'datavalue' not in dt or dt['datavalue'] == None or len(dt['datavalue']) == 0:
        dt['data'] = [0x02]
        dt['ctrl'] |= 0xC0
    else:
        dt['data'] += str2hex(dt['datavalue'], 0)

    # 计算长度
    dlen = len(dt['data'])

    dt['dlen'] = hex2str([dlen], 0)
    dt['ctrl'] = hex2str([dt['ctrl'] | 0x80], 0)
    dt['addr'] = pfun._strReverse(dt['addr'])
    dt['data'] = hex2str(dt['data'], 1)  # hex

    frame = '68' + dt['addr'] + '68' + dt['ctrl'] + dt['dlen'] + dt['data']  # + dt['cs'] + '16'

    # 计算CRC
    dt['cs'] = pfun.calcCheckSum(frame)
    frame += dt['cs'] + '16'

    print('Send:', frame)

    # 字节间增加空格
    framespace = ''
    for i in range(0, len(frame), 2):
        framespace += frame[i:i + 2] + ' '
    return framespace

def dl645_freezetime(type, t, n):
    if type == 'day':
        if 0 < n <= 62:
            t -= (24*3600*(n-1))
        else:
            return ''
    else:
        pass
    dt_obj = datetime.datetime.fromtimestamp(t)
    # date_str = dt_obj.strftime("%y%m%d%H%M%S")
    date_str = dt_obj.strftime("000000%d%m%y")
    return date_str


def dl645_read(dt, mtr, index, mmtr=None):
    if mmtr:
        pn = mmtr.getphaseNum(index)
    else:
        pn = mtr.getphaseNum(index)

    if len(dt['data']) < 4:
        return

    DI = dt['data'][:4]
    DI.reverse()

    if DI[0] == 0x00 and DI[3] == 0x00:
        if mmtr:
            eng = mmtr.readenergy(mtr, index)
        else:
            eng = mtr.readenergy(index)
        dt['datavalue'] = dl645_readenergy(DI, eng, pn)
    elif DI[0] == 0x00 and 1 <= DI[3] <= 12:
        if mmtr:
            fzday = None
        else:
            fzday = mtr.readhismon(index, DI[3])
        dt['datavalue'] = dl645_readfremonth(DI, fzday, pn)
    elif DI[0] == 0x01:
        dt['datavalue'] = dl645_readdemand()
    elif DI[0] == 0x02:
        if mmtr:
            ins = mmtr.readins(index)
        else:
            ins = mtr.readins(index)
        dt['datavalue'] = dl645_readins(DI, ins, pn)
    elif DI[0] == 0x03:
        dt['datavalue'] = dl645_readevent()
    elif DI[0] == 0x04:
        dt['datavalue'] = dl645_readpara()
    elif DI[0] == 0x05:
        if mmtr:
            fzday = None
        else:
            fzday = mtr.readhisday(index, DI[3])
        if DI[2] == 0:
            dt['datavalue'] = dl645_freezetime('day', dt['ctime'], DI[3])
        else:
            dt['datavalue'] = dl645_readfreday(DI, fzday, pn)
    elif DI[0] == 0x06:
        dt['datavalue'] = dl645_readcure()


def dl645_write():
    pass


def dl645_readaddr():
    pass


def dl645_writeaddr():
    pass


def dl645_clearmeter():
    pass


# xxxxxx.xx 转 645
def dl645_xxxxxx_xx2hex(e):
    strhex = '00000000' + str((int(e * 100)))
    strhex = strhex[-8:]
    strhex = pfun._strReverse(strhex)
    return strhex


def dl645_xxx_x2hex(e):
    strhex = '00000000' + str((int(e * 10)))
    strhex = strhex[-4:]
    strhex = pfun._strReverse(strhex)
    return strhex


def dl645_xxx_xxx2hex(e, s=0):
    if s == 1 and e < 0:  # 有符号
        strhex = '00000000' + str(int(e * -1000))
        s = str(int(strhex[-6], 10) | 0x8)  # 最高字节 | 0x80 表示符号位
        strhex = s + strhex[-5:]
    else:
        strhex = '00000000' + str((int(e * 1000)))
        strhex = strhex[-6:]
    strhex = pfun._strReverse(strhex)
    return strhex


def dl645_xx_xxxx2hex(e, s=0):
    if s == 1 and e < 0:  # 有符号
        strhex = '00000000' + str(int(e * -10000))
        s = str(int(strhex[-6], 10) | 0x8)  # 最高字节 | 0x80 表示符号位
        strhex = s + strhex[-5:]
    else:
        strhex = '00000000' + str(int(e * 10000))
        strhex = strhex[-6:]
    strhex = pfun._strReverse(strhex)
    return strhex


def dl645_x_xxx2hex(e, s=0):
    if s == 1 and e < 0:  # 有符号
        strhex = '00000000' + str(int(e * -1000))
        s = str(int(strhex[-4], 10) | 0x8)  # 最高字节 | 0x80 表示符号位
        strhex = s + strhex[-3:]
    else:
        strhex = '00000000' + str((int(e * 1000)))
        strhex = strhex[-4:]
    strhex = pfun._strReverse(strhex)
    return strhex


def dl645_xxx_x2hex(e):
    strhex = '00000000' + str((int(e * 10)))
    strhex = strhex[-4:]
    strhex = pfun._strReverse(strhex)
    return strhex

def dl645_datetime():
    strdatetime = ''

    return strdatetime


def dl645_readenergy(DI, eng, pn=3):
    # energy  [相位][类型][费率]
    e = []

    if DI[1] == 0x01:  # (当前)正向有功总电能  00010000 ~ 0001FF00
        if DI[2] == -1:
            e = eng[0][0][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][0][DI[2]]]
    elif DI[1] == 0x02 and pn == 3:  # (当前)反向有功总电能  00020000 ~ 0002FF00
        if DI[2] == -1:
            e = eng[0][1][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][1][DI[2]]]
    elif DI[1] == 0x00:  # (当前)组合有功 = Bit0(有功+)  Bit2(无功+)
        if DI[2] == -1:
            e = eng[0][0][:5] + eng[0][1][:5]
        elif 0 <= DI[1] <= 8:
            e = [eng[0][0][DI[2]] + eng[0][1][DI[2]]]
    elif DI[1] == 0x05 and pn == 3:  # (当前)第一象限无功总电能
        if DI[2] == -1:
            e = eng[0][2][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][2][DI[2]]]
    elif DI[1] == 0x06 and pn == 3:  # (当前)第二象限无功总电能
        if DI[2] == -1:
            e = eng[0][3][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][3][DI[2]]]
    elif DI[1] == 0x07 and pn == 3:  # (当前)第三象限无功总电能
        if DI[2] == -1:
            e = eng[0][4][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][4][DI[2]]]
    elif DI[1] == 0x08 and pn == 3:  # (当前)第四象限无功总电能
        if DI[2] == -1:
            e = eng[0][5][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][5][DI[2]]]
    elif DI[1] == 0x03 and pn == 3:  # 组合无功1 = 一/二象限相加
        if DI[2] == -1:
            e = eng[0][2][:5] + eng[0][3][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][2][DI[2]] + eng[0][3][DI[2]]]
    elif DI[1] == 0x04 and pn == 3:  # 组合无功2 = 三/四象限相加
        if DI[2] == -1:
            e = eng[0][4][:5] + eng[0][5][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][4][DI[2]] + eng[0][5][DI[2]]]

    elif DI[1] == 0x15 and pn == 3:  # (当前)A相正向有功电能
        e = eng[1][0][:1]
    elif DI[1] == 0x29 and pn == 3:  # (当前)B相正向有功电能
        e = eng[2][0][:1]
    elif DI[1] == 0x3d and pn == 3:  # (当前)C相正向有功电能
        e = eng[3][0][:1]

    strdata = ''
    for i in range(len(e)):
        strdata += dl645_xxxxxx_xx2hex(e[i])
    return strdata


def dl645_readdemand():
    pass


def dl645_readins(DI, ins, pn=3):
    strDI = hex2str(DI, 0)
    strdata = ''
    e = []

    # 电压 02010101 ~ 02010300
    if '0201' == strDI[:4]:
        if DI[2] == 1:
            e = [ins[0][0]]
        elif DI[2] == 2 and pn == 3:
            e = [ins[0][1]]
        elif DI[2] == 3 and pn == 3:
            e = [ins[0][2]]
        elif DI[2] == -1 and pn == 3:
            e = ins[0][:3]
        elif DI[2] == -1 and pn == 1:
            e = [ins[0][0]]

        for i in range(len(e)):
            strdata += dl645_xxx_x2hex(e[i])
        return strdata

    # 电流 02020100 ~ 02020300
    if '0202' == strDI[:4]:
        if DI[2] == 1:
            e = [ins[1][0]]
        elif DI[2] == 2 and pn == 3:
            e = [ins[1][1]]
        elif DI[2] == 3 and pn == 3:
            e = [ins[1][2]]
        elif DI[2] == 0:
            e = [ins[1][3]]
        elif DI[2] == -1 and pn == 3:
            e = ins[1]
        elif DI[2] == -1 and pn == 1:
            e = [ins[1][3]]

        for i in range(len(e)):
            strdata += dl645_xxx_xxx2hex(e[i], 1)
        return strdata

    # 有功功率 02030000 ~ 02030300
    if '0203' == strDI[:4]:
        if DI[2] == 1:
            e = [ins[3][0]]
        elif DI[2] == 2 and pn == 3:
            e = [ins[3][1]]
        elif DI[2] == 3 and pn == 3:
            e = [ins[3][2]]
        elif DI[2] == 0:
            e = [ins[3][3]]
        elif DI[2] == -1 and pn == 3:
            e = ins[3]
        elif DI[2] == -1 and pn == 1:
            e = [ins[3][3]]

        for i in range(len(e)):
            strdata += dl645_xx_xxxx2hex(e[i], 1)
        return strdata

    # 无功功率 02040000 ~ 02040300
    if '0204' == strDI[:4] and pn == 3:
        if DI[2] == 1:
            e = [ins[4][0]]
        elif DI[2] == 2:
            e = [ins[4][1]]
        elif DI[2] == 3:
            e = [ins[4][2]]
        elif DI[2] == 0:
            e = [ins[4][3]]
        elif DI[2] == -1:
            e = ins[4]

        for i in range(len(e)):
            strdata += dl645_xx_xxxx2hex(e[i], 1)
        return strdata

    # 视在功率 02050000 ~ 02050300
    if '0205' == strDI[:4] and pn == 3:
        if DI[2] == 1:
            e = [(ins[3][0] ** 2 + ins[4][0] ** 2) ** 0.5]
        elif DI[2] == 2:
            e = [(ins[3][1] ** 2 + ins[4][1] ** 2) ** 0.5]
        elif DI[2] == 3:
            e = [(ins[3][2] ** 2 + ins[4][2] ** 2) ** 0.5]
        elif DI[2] == 0:
            e = [(ins[3][3] ** 2 + ins[4][3] ** 2) ** 0.5]
        elif DI[2] == -1:
            e = (ins[3] ** 2 + ins[4] ** 2) ** 0.5

        for i in range(len(e)):
            strdata += dl645_xx_xxxx2hex(e[i], 1)
        return strdata

    # 功率因数 02060000~ 02060300
    if '0206' == strDI[:4] and pn == 3:
        if DI[2] == 1:
            e = [np.cos(ins[2][0] * np.pi / 180)]
        elif DI[2] == 2:
            e = [np.cos(ins[2][1] * np.pi / 180)]
        elif DI[2] == 3:
            e = [np.cos(ins[2][2] * np.pi / 180)]
        elif DI[2] == 0:
            e = [np.cos(np.sum(ins[2]) * np.pi / 180)]
        elif DI[2] == -1:
            ins[2][3] = np.sum(ins[2])
            e = np.cos(ins[2] * np.pi / 180)

        for i in range(len(e)):
            strdata += dl645_x_xxx2hex(e[i], 1)
        return strdata

    # 相角 02070100 ~ 02070300
    if '0207' == strDI[:4] and pn == 3:
        if DI[2] == 0:
            e = [ins[2][0]]
        elif DI[2] == 1:
            e = [ins[2][1]]
        elif DI[2] == 2:
            e = [ins[2][2]]
        elif DI[2] == -1:
            e = ins[2][:3]

        for i in range(len(e)):
            strdata += dl645_xxx_x2hex(e[i])
        return strdata

    return strdata


def dl645_readevent():
    pass


def dl645_readpara():
    pass


def dl645_readfreday(DI, eng, pn=3):
    e = []
    strdata = ''

    if eng is None:
        return strdata

    # 05060101 ~ 05060A01
    if DI[2] == 0x01:  # (当前)正向有功总电能
        e = eng[0][0][:5]
    elif DI[2] == 0x02 and pn == 3:  # (当前)反向有功总电能
        e = eng[0][1][:5]
    elif DI[2] == 0x05 and pn == 3:  # (当前)第一象限无功总电能
        e = eng[0][2][:5]
    elif DI[2] == 0x06 and pn == 3:  # (当前)第二象限无功总电能
        e = eng[0][3][:5]
    elif DI[2] == 0x07 and pn == 3:  # (当前)第三象限无功总电能
        e = eng[0][4][:5]
    elif DI[2] == 0x08 and pn == 3:  # (当前)第四象限无功总电能
        e = eng[0][5][:5]
    elif DI[2] == 0x03 and pn == 3:  # 组合无功1 = 一/二象限相加
        e = eng[0][2][:5] + eng[0][3][:5]
    elif DI[2] == 0x04 and pn == 3:  # 组合无功2 = 三/四象限相加
        e = eng[0][4][:5] + eng[0][5][:5]

    for i in range(len(e)):
        strdata += dl645_xxxxxx_xx2hex(e[i])
    return strdata

def dl645_readfremonth(DI, eng, pn=3):
    e = []
    strdata = ''

    if eng is None:
        return strdata

    if DI[1] == 0x01:  # (当前)正向有功总电能
        if DI[2] == -1:
            e = eng[0][0][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][0][DI[2]]]
    elif DI[1] == 0x02 and pn == 3:  # (当前)反向有功总电能
        if DI[2] == -1:
            e = eng[0][1][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][1][DI[2]]]
    elif DI[1] == 0x00:  # (当前)组合有功 = Bit0(有功+)  Bit2(无功+)
        if DI[2] == -1:
            e = eng[0][0][:5] + eng[0][1][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][0][DI[2]] + eng[0][1][DI[2]]]
    elif DI[1] == 0x05 and pn == 3:  # (当前)第一象限无功总电能
        if DI[2] == -1:
            e = eng[0][2][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][2][DI[2]]]
    elif DI[1] == 0x06 and pn == 3:  # (当前)第二象限无功总电能
        if DI[2] == -1:
            e = eng[0][3][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][3][DI[2]]]
    elif DI[1] == 0x07 and pn == 3:  # (当前)第三象限无功总电能
        if DI[2] == -1:
            e = eng[0][4][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][4][DI[2]]]
    elif DI[1] == 0x08 and pn == 3:  # (当前)第四象限无功总电能
        if DI[2] == -1:
            e = eng[0][5][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][5][DI[2]]]
    elif DI[1] == 0x03 and pn == 3:  # 组合无功1 = 一/二象限相加
        if DI[2] == -1:
            e = eng[0][2][:5] + eng[0][3][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][2][DI[2]] + eng[0][3][DI[2]]]
    elif DI[1] == 0x04 and pn == 3:  # 组合无功2 = 三/四象限相加
        if DI[2] == -1:
            e = eng[0][4][:5] + eng[0][5][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][4][DI[2]] + eng[0][5][DI[2]]]

    elif DI[1] == 0x15 and pn == 3:  # (当前)A相正向有功电能
        e = eng[1][0][:1]
    elif DI[1] == 0x29 and pn == 3:  # (当前)B相正向有功电能
        e = eng[2][0][:1]
    elif DI[1] == 0x3d and pn == 3:  # (当前)C相正向有功电能
        e = eng[3][0][:1]

    for i in range(len(e)):
        strdata += dl645_xxxxxx_xx2hex(e[i])
    return strdata

def dl645_readcure():
    pass


if __name__ == '__main__':
    from MeterReadingSimulation.devMeter485 import meter485
    from PublicLib.ACModule.simRTC import simrtc

    mtr = meter485()
    mtr.addmeter(1)
    mtr.run(3600)
    mtr.run(3600)

    # frame = 'FE FE FE FE 68 01 00 00 00 50 48 68 11 04 33 32 35 33 4b 16'
    # frame = 'FE FE FE FE 68 01 00 00 00 50 48 68 11 04 33 33 37 35 50 16'
    # frame = '68 01 00 00 00 50 48 68 11 04 33 32 34 35 4C 16'
    frame = 'FE FE FE FE 68 AA AA AA AA AA AA 68 11 04 33 33 39 38 B8 16 '
    ret, dt = dl645_dealframe(frame)
    print(ret, dt)

    rtc = simrtc()
    dt['ctime'] = rtc.gettick()

    if ret:
        index = mtr.readindex(dt['addr'])
        dt['index'] = index

        eng = mtr.readenergy(index)
        # print(eng)
        # dl645_read(dt, eng.energy)

        ins = mtr.readins(index)
        print(ins)
        dl645_read(dt, mtr, index)

        fe = dl645_makeframe(dt)
        print(fe)
