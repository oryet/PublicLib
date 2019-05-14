# -*- coding: utf-8 -*-

# 188报文各元素的位置
POS_188_HEAD = 0
POS_188_TYPE = 2
POS_188_ADDR = 4
POS_188_CTRL = 18
POS_188_LEN = 20
POS_188_DI0 = 22
POS_188_DI1 = 24
POS_188_SEQ = 26
POS_188_DATA = 28

# 645报文最小长度
MIN_LEN_188FRAME = 26  # 12


# 校验计算函数
def calcCheckSum(frame):
    checkSum = 0
    for i in range(0, len(frame), 2):
        checkSum += int(frame[i:i + 2], 16)
    return str(hex(checkSum))


# 188解帧函数
def deal188Frame(frame):
    if len(frame) < MIN_LEN_188FRAME:
        return False

    for i in range(0, len(frame), 2):
        if frame[i:i + 2] == '68':
            dataLen = int(frame[(i + POS_188_LEN):(i + POS_188_LEN + 2)], 16) * 2
            if dataLen + POS_188_LEN < len(frame):
                frameLen = i + dataLen + POS_188_LEN
                checkSum = calcCheckSum(frame[i:(frameLen + 2)])
                checkSum = checkSum[-2:]
                if checkSum == frame[frameLen + 2:frameLen + 4] and \
                                frame[frameLen + 4:frameLen + 6] == '16':
                    return True, frame[i + POS_188_ADDR:i + POS_188_ADDR + 14], \
                           frame[i + POS_188_CTRL:i + POS_188_CTRL + 2], \
                           frame[i + POS_188_DI0:i + POS_188_DI0 + dataLen]
    return False


# 188组帧函数
def make188Frame(head, addr, ctrl, data, mode):
    frame = '6810' + addr + ctrl
    datalen = str(hex(len(data) // 2))
    if len(datalen) < 4:
        datalen = '0' + datalen[-1]
    frame += datalen
    frame += data
    checkSum = calcCheckSum(frame)
    checkSum = checkSum[-2:]
    frame += (checkSum + '16')
    frame = head + frame
    return frame


if __name__ == '__main__':
    frame = 'FE FE aa aa 68 10 22 22 22 22 22 22 22 01 03 1F 90 00 19 16'
    frame = frame.replace(' ', '')
    # print (frame)
    l = deal188Frame(frame)
    if l[0]:
        print(l[1:])

    frame = make188Frame('fefefe', '11223344556677', '01', '901F00', 0)
    print(frame)
