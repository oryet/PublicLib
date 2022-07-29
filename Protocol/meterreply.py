# coding=utf-8

import time
import serial
import _thread
import datetime
import Protocol.General
import Protocol.prtl698

TXOUTTIME = 1.0
RXOUTTIME = 2.5
SXOUTTIME = 2.5
RXBUFFSIZE = 1024
COMLIST = []
LIST_RXDATA = []
LIST_TXDATA = []

# 初始化(打开)台体系统串口scom='COM2,2400,E,8,1'
def initsyscom(scom):
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
    print('clear-data:' + sclear)
    sout = Protocol.General.hexascii(sTx)
    COMLIST[0].write(sout)
    time.sleep(RXOUTTIME)
    sRxx = COMLIST[0].read(RXBUFFSIZE)
    #print('Rxfrom:' + sRx)
    sInn = Protocol.General.hexShow(sRxx)
    return sInn


class mkserial:
    recdata = ""
    sbuff = ""
    senddata = ""
    overflag = 0
    def __init__(self, port, baudrate,check,datanum, timeout):
        self.port = serial.Serial(port, baudrate, datanum, check, 1)
        if (self.port.is_open):
            print("打开", self.port.portstr)
        else:
            print("打开端口失败")

    # tRxData =  ['','',...]
    def receivemsg(self, tRxData,tTxData):
        # print("rec")
        sRqq = ''
        self.recdata = ""
        srec = ''
        while True:
            # sRqq = ''
            # self.recdata = ""
            size = self.port.in_waiting
            time.sleep(0.03)
            if size:
                time.sleep(0.01)
                self.recdata = self.port.read_all()
                if self.recdata != "":
                    srec = Protocol.General.hexShowNoTime(self.recdata)
                    # print("receivemsg sRqq:", datetime.datetime.now(), sRqq, srec)
                    #为模组协议做的临时处理。（模组协议和698协议共用一个串口！！！特殊处理）
                    if srec[6:24] == 'C2018200000102070A':
                        tRxData.append(srec)
                    else:
                        # 处理多帧
                        if srec[-2:] == '16':
                            sRqq += srec
                            bb = Protocol.prtl698.deal_oop_Frame(sRqq)
                            if bb[0]:
                                for i in range(1, len(bb), 1):
                                    tRxData.append(bb[i])
                                sRqq = ''
                        else:
                            sRqq += srec
                    print('srec:', sRqq)
                    if sRqq.find('68222200307003681104333434359C16') >= 0 :
                        tTxData.append('68222200307003689106333434353355A616')
                        sRqq = ''
                        srec = ''
                    elif sRqq.find('6852004304000000009C01000000000076') >=0 :
                        time.sleep(2.2)
                        tTxData.append('685F00C30576010000000000A0819000468502310200100200010105060001EA710600006B3706000072740600008D2B0600007F9B0020020001010506000151600600004E3D06000065BB0600005FB70600003DAF0000010004123456784A5D16')
                        sRqq = ''
                        srec = ''
            if self.overflag == 1:
                break
    # tTxData = [[iorder, icom_order, data(sHex)],...]
    def sendmsg(self, tTxData):
        while True:
            if len(tTxData) > 0:
                senddata = tTxData[0]
                print('senddata:',senddata)
                # print('sendmsg_senddata', senddata)
                # stxx = Protocol.prtlmkIO_LY.makemkIO_LY_Frame(senddata[0], senddata[1], senddata[2])
                print('sendmsg senddata',datetime.datetime.now(), senddata)
                sout = Protocol.General.hexascii(senddata)
                # sout=bytes(senddata,encoding='ascii')
                time.sleep(0.3)
                self.port.write(sout)
                print('port.write', sout)
                time.sleep(0.5)
                time.sleep(0.4)
                if len(tTxData) > 0:
                    del tTxData[0:]
            time.sleep(0.05)
            if self.overflag == 1:
                break
            # senddata = input("plz input:")
            # senddata = senddata.encode('utf-8')

    def close_port(self):
        self.overflag = 1
        self.port.close()

#蓝牙串口通讯
class mkblserialbl:
    recdata = ""
    sbuff = ""
    senddata = ""
    def __init__(self, port, baudrate, timeout):
        self.port = serial.Serial(port, baudrate, 8, 'N', 1)
        if (self.port.is_open):
            print("打开", self.port.portstr)
        else:
            print("打开端口失败")

    # tRxData =  ['','',...]
    def receivemsg(self, tRxData):
        # print("rec")
        sRqq = ''
        while True:
            size = self.port.in_waiting
            time.sleep(0.05)
            if size:
                time.sleep(0.1)
                self.recdata = self.port.read_all()
                if self.recdata != "":
                    # print("receivemsg recdata:", datetime.datetime.now(),  self.recdata)
                    srec = Protocol.General.hexShowNoTime(self.recdata)
                    # print("receivemsg sRqq:", datetime.datetime.now(), sRqq, srec)
                    # 原处理多帧，这里用来区分698报文还是AT指令
                    if srec[-2:] == '16':
                        sRqq += srec
                        bb = Protocol.prtl698.deal_oop_Frame(sRqq)
                        if bb[0]:
                            for i in range(1, len(bb), 1):
                                tRxData.append(bb[i])
                            sRqq = ''
                    else:
                        tRxData.append(srec)
                        # sRqq += srec


    # tTxData = [[iorder, icom_order, data(sHex)],...]
    def sendmsg(self, tTxData):
        while True:
            if len(tTxData) > 0:
                senddata = tTxData[0]
                # print('sendmsg_senddata', senddata)
                # stxx = Protocol.prtlmkIO_LY.makemkIO_LY_Frame(senddata[0], senddata[1], senddata[2])
                print('sendmsg senddata',datetime.datetime.now(), senddata)
                # sout = Protocol.General.hexascii(senddata)
                sout=bytes(senddata,encoding='ascii')
                self.port.write(sout)
                print('port.write', sout)
                time.sleep(0.5)
                del tTxData[0]
            time.sleep(0.05)
            # senddata = input("plz input:")
            # senddata = senddata.encode('utf-8')

if __name__ == '__main__':
    # ss='COM4,2400,E,8,1'
    # initsyscom(ss)
    # ss = '68 AA AA AA AA AA AA 68 1F 00 EB 16 '
    # srx = comTxRx(ss)
    # print(srx)
    # print("starting")
    # 实例化
    mport = mkserial('COM1', baudrate=9600, timeout=1)
    # 线程开启
    _thread.start_new_thread(mport.receivemsg, (LIST_RXDATA, ))
    _thread.start_new_thread(mport.sendmsg,(LIST_TXDATA, ))
    print("here")
    # LIST_TXDATA.append('68AAAA AA AA AA AA 68 1F 00 EB 16')
    # LIST_TXDATA.append('68AAAA AA AA AA AA 68 1F 01 EB 16')
    # LIST_TXDATA.append('68AAAA AA AA AA AA 68 1F 02 EB 16')
    # LIST_TXDATA.append('68AAAA AA AA AA AA 68 1F 03 EB 16')
    while True:
        time.sleep(1)
        # LIST_TXDATA.append('68AAAA AA AA AA AA 68 1F 04 EB 16')
        print('LIST_TXDATA_len:', len(LIST_TXDATA))
        print('LIST_TXDATA:', LIST_TXDATA)
        print('LIST_RXDATA_len:', len(LIST_RXDATA))
        print('LIST_RXDATA:', LIST_RXDATA)
        # if len(LIST_TXDATA) == 0:
        #     break
    #     mport.sendmsg()
