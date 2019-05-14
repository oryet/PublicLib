# -*- coding: utf-8 -*-
import os
import configparser

# 645报文各元素的位置
POS_64507_HEAD = 0
POS_64507_ADDR = 2  # 1
POS_64507_HEAD2 = 14  # 7
POS_64507_CTRL = 16  # 8
POS_64507_LEN = 18  # 9
POS_64507_DATA = 20  # 10

# 645报文最小长度
MIN_LEN_645FRAME = 24  # 12


# 校验计算函数
def calcCheckSum(frame):
    checkSum = 0
    for i in range(0, len(frame), 2):
        checkSum += int(frame[i:i + 2], 16)
    return str(hex(checkSum))


# 645解帧函数
def deal645Frame(frame):
    l = [False]
    if len(frame) < MIN_LEN_645FRAME:
        return l
    frame = frame.upper()
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
                    ctrl = frame[i + POS_64507_CTRL:i + POS_64507_CTRL + 2]
                    data = frame[i + POS_64507_DATA:i + POS_64507_DATA + dataLen]
                    l[0] = True
                    l += [addr, ctrl, data]
                    return l
    return l


# 645组帧函数
def make645Frame(head, addr, ctrl, data, mode):
    frame = '68' + addr + '68' + ctrl
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


def deal645Data(ctrl,data):
#    datalen = len(data)//2
    if len(data) % 2 != 1:
        return False
    print(len(data))


#   XXXXXX.XX函数解析
def FieldParsing645_402(data):
    if len(data) != 8:
        return 'Cannot Parse The data: '+data
    TempStrValue = ''
    for i in range(len(data)-1,-1,-2):
        TempStrValue +=data[i-1]
        TempStrValue +=data[i]

    strValue = ''
    for i in range(0,len(TempStrValue),1):
        if i == 6:
            strValue = strValue + '.'
        strValue =strValue + TempStrValue[i]

    return strValue


#   64个费率值的解析函数
def FieldParsing645_402_FF(data):
#    if len(data) != 512:
#        return 'Cannot Parse The data: ' + data
    TempStrValue = data
    strValue = ''
    for i in range(0,len(TempStrValue), 8):
        Tmp = ''
        for j in range(0,8):
            Tmp = Tmp+TempStrValue[i+j]

        Tmp = FieldParsing645_402(Tmp)
        strValue = strValue + Tmp + " "

    return strValue

#   带有日期的数据解析
def FieldParsing645_DD(data):
    if len(data) != 16:
        return 'Cannot Parse The data: ' + data
    TempStrValue = ''
    strValue = ''
    for i in range(len(data)-1,-1,-2):
        TempStrValue +=data[i-1]
        TempStrValue +=data[i]
    for i in range(0,len(TempStrValue),1):
        if i == 10:
            strValue = strValue + ' '
        if i == 12:
            strValue = strValue + '.'
        strValue =strValue + TempStrValue[i]

    return strValue

def FieldParsing645_DD_FF(data):
    #    if len(data) != 512:
    #        return 'Cannot Parse The data: ' + data
    TempStrValue = data
    strValue = ''
    for i in range(0, len(TempStrValue), 16):
        Tmp = ''
        for j in range(0, 16):
            Tmp = Tmp + TempStrValue[i + j]

        Tmp = FieldParsing645_DD(Tmp)
        strValue = strValue + Tmp + " "

    return strValue

#   电压解析函数
def FieldParsing645_V(data):
    if len(data) != 4:
        return 'Cannot Parse The data: ' + data
    TempStrValue = ''
    strValue = ''
    TempStrValue = Reversal(data)
    for i in range(0,len(TempStrValue),1):
        if i == 3:
            strValue = strValue + '.'
        strValue = strValue + TempStrValue[i]
    return strValue

def FieldParsing645_V_FF(data):
    if len(data) != 12:
        return 'Cannot Parse The data: ' + data
    TempStrValue = data
    strValue = ''
    for i in range(0, len(TempStrValue), 4):
        Tmp = ''
        for j in range(0, 4):
            Tmp = Tmp + TempStrValue[i + j]

        Tmp = FieldParsing645_V(Tmp)
        strValue = strValue + Tmp + " "
    return strValue

def FieldParsing645_I(data):
    if len(data) != 6:
        return 'Cannot Parse The data: ' + data
    TempStrValue = ''
    strValue = ''
    TempStrValue = Reversal(data)
    for i in range(0,len(TempStrValue),1):
        if i == 3:
            strValue = strValue + '.'
        strValue = strValue + TempStrValue[i]
    return strValue

def FieldParsing645_I_FF(data):
    if len(data) != 18:
        return 'Cannot Parse The data: ' + data
    TempStrValue = data
    strValue = ''
    for i in range(0, len(TempStrValue), 6):
        Tmp = ''
        for j in range(0, 6):
            Tmp = Tmp + TempStrValue[i + j]

        Tmp = FieldParsing645_I(Tmp)
        strValue = strValue + Tmp + " "
    return strValue

#   字符串反转
def Reversal(data):
    TempStrValue = ''
    for i in range(len(data) - 1, -1, -2):
        TempStrValue += data[i - 1]
        TempStrValue += data[i]
    return TempStrValue

#   定义带变量新解析函数
def FieldParsing645_X(data,bitL,pointL):
    if len(data) != bitL:
        return 'Cannot Parse The data: ' + data
    TempStrValue = ''
    strValue = ''
    TempStrValue = Reversal(data)
    for i in range(0,len(TempStrValue),1):
        if i == pointL:
            strValue = strValue + '.'
        strValue = strValue + TempStrValue[i]
    return strValue

def FiledParsing645_X_FF(data,bitL,pointL,number):
    if len(data)!= bitL*number:
        return 'Cannot Parse The data: ' + data
    TempStrValue = data
    strValue = ''
    for i in range(0, len(TempStrValue), bitL):
        Tmp = ''
        for j in range(0, bitL):
            Tmp = Tmp + TempStrValue[i + j]

        Tmp = FieldParsing645_X(Tmp,bitL,pointL)
        strValue = strValue + Tmp + " "
    return strValue

#   根据数据标识不同类别，解析不同字段
def judgeMarke(marke,data):
#   加载数据标识配置文件
    conf = configparser.ConfigParser()
    conf.read('marke.ini')
    Marke0402 = conf.get('marke645', 'Marke0402')
    Marke0402_FF = conf.get('marke645', 'Marke0402_FF')
    MarkeDD = conf.get('marke645', 'MarkeDD')
    MarkeDD_FF = conf.get('marke645', 'MarkeDD_FF')
    MarkeV = conf.get('marke645', 'MarkeV')
    MarkeV_FF = conf.get('marke645', 'MarkeV_FF')
    MarkeI_FF = conf.get('marke645', 'MarkeI_FF')
    MarkeI = conf.get('marke645', 'MarkeI')
    MarkeW = conf.get('marke645', 'MarkeW')
    MarkeW_FF = conf.get('marke645', 'MarkeW_FF')
    MarkePF = conf.get('marke645', 'MarkePF')
    MarkePF_FF = conf.get('marke645', 'MarkePF_FF')
    MarkeHW = conf.get('marke645', 'MarkeHW')
    MarkeHW_FF = conf.get('marke645', 'MarkeHW_FF')

    marke = marke.upper()
    if marke in Marke0402:
        return FieldParsing645_402(data)
    elif marke in Marke0402_FF:
        return FieldParsing645_402_FF(data)
    elif marke in MarkeDD:
        return FieldParsing645_DD(data)
    elif marke in MarkeDD_FF:
        return FieldParsing645_DD_FF(data)
    elif marke in MarkeV:
        return FieldParsing645_V(data)
    elif marke in MarkeV_FF:
        return FieldParsing645_V_FF(data)
    elif marke in MarkeI:
        return FieldParsing645_I(data)
    elif marke in MarkeI_FF:
        return FieldParsing645_I_FF(data)
    elif marke in MarkeW:
        return FieldParsing645_X(data,6,2)
    elif marke in MarkeW_FF:
        return FiledParsing645_X_FF(data,6,2,4)
    elif marke in MarkePF:
        return FieldParsing645_X(data,4,1)
    elif marke in MarkePF_FF:
        return FiledParsing645_X_FF(data,4,1,4)
    elif marke in MarkeHW:
        return FieldParsing645_X(data,4,2)
    elif marke in MarkeHW_FF:
        return FiledParsing645_X_FF(data,4,2,15)
    else:
        return "The Mark is not defined!",marke


if __name__ == '__main__':
    frame = 'FE FE FE FE 68 24 02 00 00 00 00 68 91 18 33 32 34 33 C7 47 35 33 37 86 33 33 A7 86 33 33 36 87 33 33 44 87 33 33 eB 16'
#    frame = 'FE FE aa aa 68 22 22 22 22 22 22 68 93 06 55 55 55 55 55 55 33 16'
    frame = frame.replace(' ', '')
#    frame = frame.replace('FE','')
    # print (frame)
    l = deal645Frame(frame)
    if l[0]:
        print(l[1:])

    frame = make645Frame('fefefe', '112233445566', '11', '05060102', 0)
    print(frame)

    frame = '98765432987654329876543298765432'
    print(FieldParsing645_402_FF(frame))

    frame = '998877010101011899887701010101289988770101010138'
    print(FieldParsing645_DD_FF(frame))

    frame = '99981'
    print(FieldParsing645_V(frame))
    print(judgeMarke('0201FF00','999899919992'))
    print(judgeMarke('02030000','998978'))
    print(judgeMarke('0203ff00','998877998866998855998855'))

    print(judgeMarke('0206FF00', '4231222233334444'))
    print(judgeMarke('020A010F', '2233'))
