import sys

sys.path.append('../')
from PublicLib.public import calcCheckSum
from MeterReadingSimulation.devMeter485 import meter485
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
def str2hex(strdata, en):
    data = []
    for j in range(0, len(strdata), 2):
        s = strdata[j:j + 2]
        if en:
            s = int(s, 16) - 0x33
        else:
            s = int(s, 16)
        data += [s]
    return data


# en +33
def hex2str(hexdata, en):
    s = ''
    for j in range(len(hexdata)):
        if en:
            ss = hex(hexdata[j] + 0x33)
        else:
            ss = hex(hexdata[j])
        ss = ss.replace('0x', '00')
        ss = ss[-2:]
        # s += hex(hexdata[j]).replace('0x', '00')[-2:0]
        s += ss
    return s


def dealframe(frame):
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
                    addr = frame[i + POS_64507_ADDR:i + POS_64507_ADDR + 12]
                    dt['addr'] = pfun._strReverse(addr)
                    # dt['ctrl'] = frame[i + POS_64507_CTRL:i + POS_64507_CTRL + 2]
                    dt['ctrl'] = int(frame[i + POS_64507_CTRL:i + POS_64507_CTRL + 2], 16)
                    # dt['data'] = frame[i + POS_64507_DATA:i + POS_64507_DATA + dataLen]
                    datastr = frame[i + POS_64507_DATA:i + POS_64507_DATA + dataLen]
                    dt['data'] = str2hex(datastr, 1)
                    return True, dt
    return False, None


# 十六进制 转 字符串 再 组帧
def makeframe(dt):
    # 计算长度
    dlen = len(dt['data'])

    # data区组帧
    if dlen > 0:
        cs = pfun.calcHexCheckSum(dt['data'], 1)
        dt['cs'] = hex2str([cs], 0)

    dt['dlen'] = hex2str([dlen], 0)
    dt['ctrl'] = hex2str([dt['ctrl'] | 0x80], 0)
    dt['addr'] = pfun._strReverse(dt['addr'])
    dt['data'] = hex2str(dt['data'], 1)  # hex

    frame = '68' + dt['addr'] + '68' + dt['ctrl'] + dt['dlen'] + dt['data'] + dt['cs'] + '16'
    return frame


def read(dt, eng):
    if len(dt['data']) < 4:
        return

    m = dt['data'][3]
    DI = dt['data'][:4]
    print(DI)

    if m == 0x00:
        readenergy(DI, eng)
    elif m == 0x01:
        readdemand()
    elif m == 0x02:
        readins()
    elif m == 0x03:
        readevent()
    elif m == 0x04:
        readpara()
    elif m == 0x05:
        readfre()
    elif m == 0x06:
        readcure()


def write():
    pass


def readaddr():
    pass


def writeaddr():
    pass


def clearmeter():
    pass


def readenergy(DI, eng):
    eng.eprint()
    if DI[2] == 0x01:  # (当前)正向有功总电能
        a = eng.energy[eng.POSACT]
        print(a)
    elif DI[2] == 0x02:  # (当前)反向有功总电能
        pass
    elif DI[2] == 0x05:  # (当前)第一象限无功总电能
        pass
    elif DI[2] == 0x06:  # (当前)第二象限无功总电能
        pass
    elif DI[2] == 0x07:  # (当前)第三象限无功总电能
        pass
    elif DI[2] == 0x08:  # (当前)第四象限无功总电能
        pass


def readdemand():
    pass


def readins():
    pass


def readevent():
    pass


def readpara():
    pass


def readfre():
    pass


def readcure():
    pass


if __name__ == '__main__':
    mtr = meter485()
    mtr.addmeter(1)

    frame = 'FE FE FE FE 68 01 00 00 00 50 48 68 11 04 33 32 34 33 4a 16'
    ret, dt = dealframe(frame)
    print(ret, dt)

    if ret:
        index = mtr.readindex(dt['addr'])
        dt['index'] = index

        eng = mtr.readenergy(index)
        print(eng)
        read(dt, eng)

        fe = makeframe(dt)
        print(fe)
