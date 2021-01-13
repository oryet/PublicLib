import PublicLib.public as pfun

# en -33
def str2hex(strdata, en=0):
    data = []
    for j in range(0, len(strdata), 2):
        s = strdata[j:j + 2]
        if en:
            try:
                # s = int(s, 16) - 0x33
                d = int(s, 16)
                if d >= 0x33:
                    s = d - 0x33
                else:
                    s = d + 0x100 - 0x33
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
