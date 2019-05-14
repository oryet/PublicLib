# -*- coding: utf-8 -*-
# PACKAGE TOOL

MIN_LEN_PT4FRAME = 6


# 四通道组帧
def pt4_makeframe(frame, channel=0):
    chanstr = str(channel)
    chanstr = chanstr.zfill(2)

    frame = "6833" + chanstr + frame + "16"
    return frame


# 四通道解帧
def pt4_dealframe(frame):
    l = [False]
    if len(frame) < MIN_LEN_PT4FRAME:
        return l
    frame = frame.upper()

    if frame[0:4] == '6833':
        l[0] = True
        l += [frame[2:4]]  # ctrl
        l += [frame[4:-2]]  # data 去除 16
        return l

    for i in range(0, len(frame), 2):
        if frame[i:i + 2] == '68':
            dataLen = int(frame[i + 4:i + 6], 16) * 2
            if (frame[(i + dataLen + 8):(i + dataLen + 8) + 2] == '16'):
                l[0] = True
                l += [frame[i + 2:i + 4]]  # ctrl
                l += [dataLen]  # len
                l += [frame[(i + 8):-2]]  # data
                return l
    return l


def pt4_dealsenddataframe(frame):
    dataList = []

    dataList += [frame[0:2]]  # 通道号
    dataList += [frame[2:]]  # 无线报文（不包含物理层）
    return dataList

def pt4_dealrecvdataframe(frame):
    dataList = []

    dataList += [frame[0:2]]  # 通道号
    dataList += [frame[2:4]]  # 信道索引
    dataList += [frame[4:6]]  # 接收信号强度
    dataList += [frame[6:]]  # 无线报文（包含物理层）
    return dataList


def pt4_dealframemain(frame):
    frame = frame.replace(' ', '')
    l = pt4_dealframe(frame)
    if l[0]:
        if l[1] == '20':  # 数据接收帧
            l = l[:-2] + pt4_dealrecvdataframe(l[-1]) # 取list最后一个元组
        elif l[1] == '33':
            l = l[:-2] + pt4_dealsenddataframe(l[-1]) #
    return l


if __name__ == '__main__':
    frame = "11 22 33 44 55 66"
    frame = frame.replace(' ', '')

    frame = pt4_makeframe(frame, 3)
    print(frame)

    frame = '68 33 00 01 0C 0A FF FF 01 00 04 03 02 01 AA AA AA AA AA AA 00 0C 01 00 04 03 02 01 AA AA AA AA AA AA ' \
            'F1 01 09 04 16 '

    '''
    frame = "68 20 39 00 00 00 17 33 00 33 01 0C 25 FF FF 09 00 00 55 07 00 01 00 04 03 02 01 01 0C 09 00 00 55 07 " \
            "00 01 00 04 03 02 01 21 11 10 02 09 00 00 55 07 00 32 58 29 08 70 41 20 59 65 B7 16"
    '''
    '''
    frame = frame.replace(' ', '')
    l = pt4_dealframe(frame)
    print(l)
    if l[0] == '20': # 数据接收帧
        f = pt4_dealdataframe(l[2])
        print(f)
    '''
    l = pt4_dealframemain(frame)
    print(l)
    print(l[-1])
