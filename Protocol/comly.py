# coding=utf-8

import time
import serial

TXOUTTIME = 1.0
RXOUTTIME = 2.5
SXOUTTIME = 2.5
RXBUFFSIZE = 1024
COMLIST = []


def hexShow(argv):
    result = ''
    hLen = len(argv)
    for i in xrange(hLen):
        hvol = ord(argv[i])
        hhex = '%02x' % hvol
        result += hhex.upper()
    print 'hexShow:', result
    return result

# 初始化(打开)台体系统串口scom='COM2,2400,E,8,1'
def initsyscom(scom):
    nCt = 0
    slst = scom.split(',')
    if len(slst) != 5:
        return False
    if len(COMLIST) == 0:
        try:
            pcom = serial.Serial(slst[0])
            pcom.baudrate = int(slst[1])
            pcom.parity = slst[2]
            pcom.bytesize = int(slst[3])
            pcom.stopbits = int(slst[4])
            pcom.timeout = 3
            pcom.xonxoff = False
            pcom.rtscts = False
            pcom.dsrdtr = False
            pcom.writeTimeout = TXOUTTIME
            COMLIST.append(pcom)
        except:
            return False
        return True


# return hex报文通信
def comTxRx(sTx):
    if len(COMLIST) == 0:
        return [False]
    if COMLIST[0].isOpen() is False:
        return [False]
    # print('Txto:'+sTx)
    sclear = COMLIST[0].read(RXBUFFSIZE)
    print ('clear-data:' + sclear)
    sout = HextoChar(sTx)
    COMLIST[0].write(sout)
    time.sleep(RXOUTTIME)
    sRx = COMLIST[0].read(RXBUFFSIZE)
    #print('Rxfrom:' + sRx)
    sIn = hexShow(sRx)
    return sIn

# return json串口通信
def comjsonTxRx(sTx):
    if len(COMLIST) == 0:
        return [False]
    if COMLIST[0].isOpen() is False:
        return [False]
    sclear = COMLIST[0].read(RXBUFFSIZE)
    print ('clear-data:' + sclear)
    sout = sTx.replace('\'','\"')
    print('Txto:'+sout)
    COMLIST[0].write(sout)
    time.sleep(SXOUTTIME)
    sRx = COMLIST[0].read(RXBUFFSIZE)
    print('Rxfrom:' + sRx)
    sIn = sRx.replace('\"', '\'')
    return sIn

# 十六进制转char字符串
def HextoChar(sHex):
    out = ''
    sHex = sHex.replace(' ', '')
    # print len(sHex)/2
    for i in range(0, len(sHex), 2):
        tt = sHex[i:i+2]
        out += chr(int(tt, 16))
    hexShow(out)
    return out


if __name__ == '__main__':
    ss='COM4,2400,E,8,1'
    initsyscom(ss)
    ss = '68 AA AA AA AA AA AA 68 1F 00 EB 16 '
    srx = comTxRx(ss)
    print srx

