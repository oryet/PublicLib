import PublicLib.public as pfun

sn = 0


def Mex_CmdParse(c, dt):
    cmd = int(c[:2], 16)
    if cmd & 0x80:
        print('有后续帧')

    dt['dev'] = (cmd >> 5) & 0x03

    dt['cmd'] = cmd & 0x07


def Mex_AddParse(addr, dt):
    a = int(addr[:2], 16)
    if a & 0x80:
        dt['addlen'] = a & 0x7F
        al = (a & 0x7F) * 2 + 2
        dt['addr'] = addr[2:al]
    else:
        dt['addlen'] = 1
        al = 2
        dt['addr'] = addr[:2]
    return al


def Mex_DataLenParse(d, dt):
    a = int(d[:2], 16)
    if a & 0x80:
        a &= 0x7F
        sd = pfun._strReverse(d[2:a * 2 + 2])  # 长度域字符串倒序
        dt['datalen'] = int(sd, 16)
        dl = (a + 1) * 2
    else:
        dt['datalen'] = a
        dl = 2
    return dl


# 解帧
def Mex_GetFrame(s, dt):
    n = s.find('68')
    if n >= 0:
        # dt['frame'] = l = s[n:]  # 获取数据帧
        l = s[n:]  # 获取数据帧
    else:
        dt['err'] = 'head err'
        return

    Mex_CmdParse(l[2:4], dt)

    dt['sn'] = l[4:6]
    l = l[6:]

    n = Mex_AddParse(l, dt)
    l = l[n:]

    n = Mex_DataLenParse(l, dt)
    l = l[n:]

    # 计算CRC
    calcCrc = "0000" + pfun.crc16hex(0xFFFF, l[:-6], True)
    calcCrc = calcCrc[-4:]
    n = dt['datalen'] * 2
    frameCrc = l[n: n + 4].upper()
    if calcCrc != frameCrc:
        dt['err'] = 'crc err'
        dt['ret'] = False
        print(calcCrc, frameCrc)
    else:
        dt['ret'] = True

    dt['data'] = l[:-6]


def Mex_MakeAddr(dt):
    if dt['addlen'] > 1:
        s = 0x80 + dt['addlen']
        s = hex(s)[-2:] + pfun.strReverse(dt['addr'])
    else:
        s = pfun.strReverse(dt['addr'])
    return s


def Mex_MakeDataLen(dt):
    if 0x80 < dt['datalen'] <= 0xFF:
        s = 0x81
        s = hex(s)[-2:] + hex(dt['datalen']).replace('0x', '0000')[-2:]
    elif 0xFF < dt['datalen'] <= 0xFFFF:
        s = 0x82
        n = hex(dt['datalen']).replace('0x', '0000')[-4:]
        n = pfun._strReverse(n)
        s = hex(s)[-2:] + n
    else:
        s = hex(dt['datalen']).replace('0x', '0000')[-2:]
    return s


# 组帧
def Mex_MakeFrame(dt):
    s = '68'
    c = (dt['dev'] << 5) | dt['cmd']
    s += hex(c).replace('0x', '00')[-2:]
    try:
        s += dt['sn']
    except:
        s += hex(sn).replace('0x', '00')[-2:]

    s += Mex_MakeAddr(dt)

    s += Mex_MakeDataLen(dt)

    s += dt['data']

    s += pfun.crc16hex(0xFFFF, dt['data'], True).replace('0x', '0000')[-4:]

    s += '16'

    return s


if __name__ == '__main__':
    sendframe = '68 21 45 83 11 22 33 03 01 00 05 e0 03 16'
    recvframe = '68 21 45 83 11 22 33 0d 01 00 05 01 00 02 00 03 00 04 00 05 00 c2 e9 16'

    sendframe = sendframe.replace(' ', '')
    recvframe = recvframe.replace(' ', '')

    dt = {}
    Mex_GetFrame(recvframe, dt)
    print(dt)


    # dt['addr'] = '123456789012'
    # dt['addlen'] = int(len(dt['addr']) / 2)
    # dt['data'] = dt['data']*122
    # dt['datalen'] = int(len(dt['data']) / 2)

    s = Mex_MakeFrame(dt)
    print(s)

    dt = {}
    Mex_GetFrame(s, dt)
    print(dt)
