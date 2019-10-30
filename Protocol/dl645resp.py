import sys

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
def str2hex(strdata, en):
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
def hex2str(hexdata, en):
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
    if 'datavalue' in dt and dt['datavalue'] != None:
        dt['data'] += str2hex(dt['datavalue'], 0)
    else:
        dt['data'] = [0x02]
        dt['ctrl'] |= 0xC0

    # 计算长度
    dlen = len(dt['data'])

    dt['dlen'] = hex2str([dlen], 0)
    dt['ctrl'] = hex2str([dt['ctrl'] | 0x80], 0)
    dt['addr'] = pfun._strReverse(dt['addr'])
    dt['data'] = hex2str(dt['data'], 1)  # hex

    frame = '68' + dt['addr'] + '68' + dt['ctrl'] + dt['dlen'] + dt['data'] # + dt['cs'] + '16'

    # 计算CRC
    dt['cs'] = pfun.calcCheckSum(frame)
    frame += dt['cs'] + '16'

    # 字节间增加空格
    framespace = ''
    for i in range (0, len(frame), 2):
        framespace += frame[i:i+2] + ' '
    return framespace


def dl645_read(dt, eng):
    if len(dt['data']) < 4:
        return

    m = dt['data'][3]
    DI = dt['data'][:4]
    print(DI)

    if m == 0x00:
        dt['datavalue'] = dl645_readenergy(DI, eng)
    elif m == 0x01:
        dt['datavalue'] = dl645_readdemand()
    elif m == 0x02:
        dt['datavalue'] = dl645_readins()
    elif m == 0x03:
        dt['datavalue'] = dl645_readevent()
    elif m == 0x04:
        dt['datavalue'] = dl645_readpara()
    elif m == 0x05:
        dt['datavalue'] = dl645_readfre()
    elif m == 0x06:
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
def dl645_energydata2hex(e):
    strhex = '00000000' + str((int(e*100)))
    strhex = strhex[-8:]
    strhex = pfun._strReverse(strhex)
    return strhex



def dl645_readenergy(DI, eng):
    # eng.eprint()
    # energy  [相位][类型][费率]

    if DI[2] == 0x01:  # (当前)正向有功总电能
        e = eng[0][0]
    elif DI[2] == 0x02:  # (当前)反向有功总电能
        e = eng[0][1]
    elif DI[2] == 0x05:  # (当前)第一象限无功总电能
        e = eng[0][2]
    elif DI[2] == 0x06:  # (当前)第二象限无功总电能
        e = eng[0][3]
    elif DI[2] == 0x07:  # (当前)第三象限无功总电能
        e = eng[0][4]
    elif DI[2] == 0x08:  # (当前)第四象限无功总电能
        e = eng[0][5]

    strdata = ''
    for i in range(len(e)):
        strdata += dl645_energydata2hex(e[i])
    return strdata


def dl645_readdemand():
    pass


def dl645_readins():
    pass


def dl645_readevent():
    pass


def dl645_readpara():
    pass


def dl645_readfre():
    pass


def dl645_readcure():
    pass


if __name__ == '__main__':
    from MeterReadingSimulation.devMeter485 import meter485

    mtr = meter485()
    mtr.addmeter(1)
    mtr.run(3600)
    mtr.run(3600)

    frame = 'FE FE FE FE 68 01 00 00 00 50 48 68 11 04 33 32 35 33 4b 16'
    # frame = 'FE FE FE FE 68 01 00 00 00 50 48 68 11 04 33 33 37 35 50 16'
    ret, dt = dl645_dealframe(frame)
    print(ret, dt)

    if ret:
        index = mtr.readindex(dt['addr'])
        dt['index'] = index

        eng = mtr.readenergy(index)
        print(eng)
        dl645_read(dt, eng.energy)

        fe = dl645_makeframe(dt)
        print(fe)
