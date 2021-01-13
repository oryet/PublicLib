import sys
sys.path.append("..")
from PublicLib.Protocol.dl645resp import *
from PublicLib.Protocol.dl645format import *
import time
import PublicLib.public as pfun


def upgradeRecvDataToMap(bmapstr, uplist):
    bmapstr = pfun._strReverse(bmapstr)
    for i in range(0, len(bmapstr), 2):
        b = bmapstr[i:i + 2]
        n = int(b, 16)
        for j in range(8):
            if n & (1 << j):
                uplist["bmap"][i * 4 + j] = 1
            else:
                uplist["bmap"][i * 4 + j] = 0

'''
def upgradeRecvDataToMap(index, bmapstr, self):
    bmapstr = pfun._strReverse(bmapstr)
    for i in range(0, len(bmapstr), 2):
        b = bmapstr[i:i + 2]
        n = int(b, 16)
        for j in range(8):
            if n & (1 << j):
                self.uplist["bmap"][index*512 + i * 4 + j] = 1
            else:
                self.uplist["bmap"][index*512 + i * 4 + j] = 0
'''

def upgradeSendData(uplist):
    for i in range(len(uplist["bmap"])):
        if uplist["bmap"][i] != 1:
            # print(i, uplist["bmap"][i])
            uplist["bmap"][i] = 1
            return i
    return -1


def upgradeDataProc_DL645(recv, uplist):
    ret, dt = dl645_dealframe(recv, False)
    if ret:
        strDI = pfun.strReverse(dt['data'][:8])
        strData = pfun.strReverse(dt['data'][8:])
        strDI = hex2str(str2hex(strDI, 1))
        strData = hex2str(str2hex(strData, 1))
        print('strDI:', strDI, 'strData:', strData)

        if strDI == '04a00501': # 查询漏包
            upgradeRecvDataToMap(strData, uplist)



def upgradeRecvProc(self):
    while 1:
        time.sleep(1)
        while not self.qRecv.empty():
            recv = self.qRecv.get()
            print('upgradeRecvProc recv:', recv)
            if 'Len' in recv:
                pass
            elif 'HexStr' in recv:
                upgradeDataProc_DL645(recv['HexStr'], self.uplist)
            else:
                pass

def upgradeGetCurPackNum(uplist):
    for i in range(len(uplist["bmap"])):
        if uplist["bmap"][i] == 0:
            return i

if __name__ == '__main__':
    # frame645 = '68AAAAAAAAAAAA6891C43438D337343333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333D816'
    # frame645 = '68AAAAAAAAAAAA6891C43438D337C433333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333336816'
    frame645 = '68AAAAAAAAAAAA6891C43438D337323232323633333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333D616'
    bitmap = [0]*2048
    uplist = {"ip": "", "port": "", "bmap": bitmap}
    upgradeDataProc_DL645(frame645, uplist)

    n = upgradeGetCurPackNum(uplist)
    print('upgradeGetCurPackNum:', n)

    for i in range(16):
        upgradeSendData(uplist)

    n = upgradeGetCurPackNum(uplist)
    print('upgradeGetCurPackNum:', n)
