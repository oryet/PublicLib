import PublicLib.public as pfun


def Mex_CmdParse(c, dt):
    cmd = int(c[:2], 16)
    if cmd & 0x80:
        print('有后续帧')

    if cmd & 0x40:
        dt['prm'] = 1
    else:
        dt['prm'] = 0

    if cmd & 0x01:
        dt['cmd'] = 1
    elif cmd & 0x02:
        dt['cmd'] = 1


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
        sd = pfun._strReverse(d[2:a * 2])  # 长度域字符串倒序
        dl = dt['datalen'] = int(sd, 16)
        dl = dl * 2 + 2
    else:
        dt['datalen'] = a
        dl = 2
    return dl


# 解帧
def Mex_GetFrame(s, dt):
    n = s.find('68')
    if n >= 0:
        dt['frame'] = l = s[n:]  # 获取数据帧
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


if __name__ == '__main__':
    sendframe = '68 01 45 83 11 22 33 03 01 00 05 e0 03 16'
    recvframe = '68 01 45 83 11 22 33 0d 01 00 05 01 00 02 00 03 00 04 00 05 00 c2 e9 16'

    sendframe = sendframe.replace(' ', '')
    recvframe = recvframe.replace(' ', '')

    dt = {}
    Mex_GetFrame(sendframe, dt)
    print(dt)
