# coding=utf-8

import datetime
import logging
import math
import os
import random
import time
import re
import xlrd
import xlwt
from Protocol.nzscset import *
from Protocol import General
from Protocol import prtl698
from Protocol import prtlmkIO
from Protocol import prtlmkIO_LY
from Protocol import mkcom
from Protocol import SSH2ccc
from Protocol import prtl3763
from Protocol import CTRL1375
from Protocol import dl645
from Protocol import SSH2ccc_ex
from Protocol import prtl3762
import socket
import threading
import socketserver
import configparser
import _thread

__RTUTYPE__ = 'fk'
__EXCELTYPE__ = 'task'

SYSCONFIG = {'VMETERHOST': '192.168.124.137', 'VMETERPORT': 9999, 'SERVERIP': '192.168.88.219', 'SERVERPORT': 11039,
             'SSH_SERVERIP': '192.168.8.203', 'SSH_SERVERPORT': 8888, 'DSOCKTTIMEOUT': 900, 'BUFFSIZE': 4096,
             'RXOUTTIME': 90.0, 'TXOUTTIME': 5.0, 'JGTIME':1.0, 'VMOUTTIME': 5.0}

client_addr = []
client_socket = []
public_sRxBuff = []
# public_repRxBuff_temp = []
client_addr_temp = []
client_socket_temp = []
public_sRxBuff_temp = []
public_thread_temp = True
lst_vmBuff = []
# 槽位串口存
LIST_CW1_RXDATA = []
LIST_CW1_TXDATA = []
LIST_CW2_RXDATA = []
LIST_CW2_TXDATA = []
LIST_CW3_RXDATA = []
LIST_CW3_TXDATA = []
LIST_CW4_RXDATA = []
LIST_CW4_TXDATA = []
LIST_CW5_RXDATA = []
LIST_CW5_TXDATA = []
DATETIME_T = [datetime.datetime.now(), datetime.datetime.now()]

LSIT_MK_CW = ['GPRS', 'PLC', 'RS485', 'YX', 'XJY']

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    ip = ''
    port = ''
    timeout = SYSCONFIG['DSOCKTTIMEOUT']
    def setup(self):
        self.ip = self.client_address[0].strip()
        self.port = self.client_address[1]
        self.request.settimeout(None)
        print(self.ip + ':' + str(self.port) + 'connected server!')
        logging.info(self.ip + ':' + str(self.port) + 'connected server!')
        # client_addr.clear()
        # client_socket.clear()
        client_addr.append(self.client_address)
        client_socket.append(self.request)

    def handle(self):
        while True:
            time.sleep(0.1)
            try:
                if self.request:
                    data = self.request.recv(SYSCONFIG['BUFFSIZE'])
                else:
                    data = ''
            except socket.timeout:
                print(self.ip + ':' + str(self.port) + 'Rx timeout!break connect!')
                logging.info(self.ip + ':' + str(self.port) + 'Rx timeout!break connect!')
                # break
            if data:
                cur_thread = threading.current_thread()
                # print('redata', data)
                # print('len', len(data))
                response = "{}: {}".format(cur_thread.name, General.hexShow(data))
                # self.request.sendall(response)
                print('rx:', response)
                logging.info(response)
                print('rx:' + General.hexShow(data))
                # logging.info('rx:' + hexShow(data))
                bb = prtl698.islinkReturn(data)
                if bb[0] is True:
                    if bb[1] == prtl698.LinkRequestType_LOGIN:
                        logging.info('登录!')
                    elif bb[1] == prtl698.LinkRequestType_HEART:
                        logging.info('心跳!')
                    time.sleep(0.1)
                    self.request.sendall(bb[2])
                    time.sleep(1.1)
                    logging.info('link-tx:' + General.hexShow(bb[2]))
                    print('link-tx:' + General.hexShow(bb[2]))
                else:
                    rr = prtl698.isappReturn(data)
                    if rr[0]:
                        if rr[1] == prtl698.Server_APDU_SET_Response:
                            logging.info('Set:' + General.hexShow(rr[2]))
                            print('Set:' + General.hexShow(rr[2]))
                            public_sRxBuff.append([rr[1], rr[2]])
                        elif rr[1] == prtl698.Server_APDU_GET_Response:
                            logging.info('Get:' + General.hexShow(rr[2]))
                            print('Get:' + General.hexShow(rr[2]))
                            public_sRxBuff.append([rr[1], rr[2]])
                        elif  rr[1] == prtl698.Server_APDU_ACTION_Response :
                            logging.info('action:' + General.hexShow(rr[2]))
                            print('action:' + General.hexShow(rr[2]))
                            public_sRxBuff.append([rr[1], rr[2]])
                        elif rr[1] == prtl698.Server_APDU_PROXY_Response:
                            logging.info('proxy:' + General.hexShow(rr[2]))
                            print('proxy:' + General.hexShow(rr[2]))
                            public_sRxBuff.append([rr[1], rr[2]])
                        elif rr[1] == prtl698.Server_APDU_REPORT_Notification:
                            logging.info('上报:' + General.hexShow(data))
                            print('report:' + General.hexShow(data))
                            if len(rr) == 3:
                                time.sleep(0.1)
                                self.request.sendall(rr[2])
                                time.sleep(1.1)
                                logging.info('report-confirm:' + General.hexShow(rr[2]))
                                print('report-confirm:' + General.hexShow(rr[2]))
                            public_sRxBuff.append([rr[1], rr[4]])
                            # public_sRxBuff.append([rr[1], rr[2]])
                        # elif rr[1] == nwlyzd.afn_READALARM:
                        #     logging.info('readalarm:' + rr[2])
                        #     print 'readalarm:' + rr[2]
                        #     if len(rr) == 4:
                        #         time.sleep(0.1)
                        #         self.request.sendall(rr[3])
                        #         time.sleep(2.0)
                        #         logging.info('alarm-confirm:' + nwlyzd.hexShow(rr[3]))
                        #         print 'alarm-confirm:' + nwlyzd.hexShow(rr[3])
                        #     #public_sRxBuff.append([rr[1], rr[2]])
                        # elif rr[1] == nwlyzd.afn_CONFIRM:
                        #     logging.info('confirm:' + rr[2])
                        #     print 'confirm:' + rr[2]
                        #     public_sRxBuff.append([rr[1], rr[2]])


    def finish(self):
        print('client is disconnect!')
        client_addr.remove(self.client_address)
        client_socket.remove(self.request)
        logging.info('client is disconnect!')


class ThreadedTCPRequestTempHandler(socketserver.BaseRequestHandler):
    ip = ''
    port = ''
    timeout = 900
    def setup(self):
        self.ip = self.client_address[0].strip()
        self.port = self.client_address[1]
        self.request.settimeout(None)
        print(self.ip + ':' + str(self.port) + 'connected temp server!')
        logging.info(self.ip + ':' + str(self.port) + 'connected temp server!')
        # client_addr_temp.clear()
        # client_socket.clear()
        client_addr_temp.append(self.client_address)
        client_socket_temp.append(self.request)

    def handle(self):
        while public_thread_temp:
            time.sleep(0.1)
            try:
                if self.request:
                    data = self.request.recv(SYSCONFIG['BUFFSIZE'])
                else:
                    data = ''
            except socket.timeout:
                print(self.ip + ':' + str(self.port) + 'Rx temp timeout!break connect!')
                logging.info(self.ip + ':' + str(self.port) + 'Rx temp timeout!break connect!')
                # break
            if data:
                cur_thread = threading.current_thread()
                # print('redata', data)
                # print('len', len(data))
                response = "{}: {}".format(cur_thread.name, General.hexShow(data))
                # self.request.sendall(response)
                print('temp rx:', response)
                logging.info(response)
                print('temp rx:' + General.hexShow(data))
                # logging.info('rx:' + hexShow(data))
                bb = prtl698.islinkReturn(data)
                if bb[0] is True:
                    if bb[1] == prtl698.LinkRequestType_LOGIN:
                        logging.info('temp 登录!')
                    elif bb[1] == prtl698.LinkRequestType_HEART:
                        logging.info('temp 心跳!')
                    time.sleep(0.1)
                    self.request.sendall(bb[2])
                    time.sleep(1.1)
                    logging.info('temp link-tx:' + General.hexShow(bb[2]))
                    print('temp link-tx:' + General.hexShow(bb[2]))
                else:
                    rr = prtl698.isappReturn(data)
                    if rr[0]:
                        if rr[1] == prtl698.Server_APDU_SET_Response:
                            logging.info('temp Set:' + General.hexShow(rr[2]))
                            print('temp Set:' + General.hexShow(rr[2]))
                            public_sRxBuff_temp.append([rr[1], rr[2]])
                        elif rr[1] == prtl698.Server_APDU_GET_Response:
                            logging.info('temp Get:' + General.hexShow(rr[2]))
                            print('temp Get:' + General.hexShow(rr[2]))
                            public_sRxBuff_temp.append([rr[1], rr[2]])
                        elif  rr[1] == prtl698.Server_APDU_ACTION_Response :
                            logging.info('temp action:' + General.hexShow(rr[2]))
                            print('temp action:' + General.hexShow(rr[2]))
                            public_sRxBuff_temp.append([rr[1], rr[2]])
                        elif rr[1] == prtl698.Server_APDU_PROXY_Response:
                            logging.info('temp proxy:' + General.hexShow(rr[2]))
                            print('temp proxy:' + General.hexShow(rr[2]))
                            public_sRxBuff_temp.append([rr[1], rr[2]])
                        elif rr[1] == prtl698.Server_APDU_REPORT_Notification:
                            logging.info('temp 上报:' + General.hexShow(data))
                            print('temp report:' + General.hexShow(data))
                            if len(rr) == 3:
                                time.sleep(0.1)
                                self.request.sendall(rr[2])
                                time.sleep(1.1)
                                logging.info('temp report-confirm:' + General.hexShow(rr[2]))
                                print('temp report-confirm:' + General.hexShow(rr[2]))
                            # public_sRxBuff_temp.append([rr[1], rr[2]])


    def finish(self):
        print('temp client is disconnect!')
        client_addr_temp.remove(self.client_address)
        client_socket_temp.remove(self.request)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(bytes(message))
    response = str(sock.recv(1024))
    print("Received: {}".format(response))

# replace 接收数据  oad_oam
def recvdata(safn):
    sframe = ""
    if len(public_sRxBuff) == 0:
        return sframe
    print('recvdata', safn)
    for item in public_sRxBuff:
        # print(item[0] + ':' + safn)
        # print(item)
        if General.hexShow(item[1]).find(safn) >= 0:
            sframe = General.hexShow(item[1])
            break
    while len(public_sRxBuff) > 0:
        del public_sRxBuff[0]
    return sframe

# replace 接收上报数据 by soad
# def recReportdata(soad):
#     sframe = ""
#     if len(public_repRxBuff_temp) == 0:
#         return sframe
#     print('recvdata', soad)
#     for item in public_repRxBuff_temp:
#         if General.hexShow(item[1]).find(soad) >= 0:
#             sframe = General.hexShow(item[1])
#             break
#     while len(public_repRxBuff_temp) > 0:
#         del public_repRxBuff_temp[0]
#     return sframe


# 槽位接收数据 iorder= -1 不判序号, sdt ''不判标识
def MK_recvdata(iorder, icom, sdt, Protocol_TYPE = prtlmkIO_LY.Protocol_MKLINK_TYPE):
    # scwbuff1 [True, iorder icom , dictdata/hex]
    scwbuff1 = []
    scwbuff2 = []
    scwbuff3 = []
    scwbuff4 = []
    scwbuff5 = []
    rt = [False, scwbuff1, scwbuff2, scwbuff3, scwbuff4, scwbuff5]
    # print('LIST_CW1_RXDATA', LIST_CW1_RXDATA)
    # print('LIST_CW2_RXDATA', LIST_CW2_RXDATA)
    # if len(LIST_CW1_RXDATA) == 0 or len(LIST_CW2_RXDATA) == 0 or len(LIST_CW3_RXDATA) == 0 or len(LIST_CW4_RXDATA) == 0 \
    #         or len(LIST_CW5_RXDATA) == 0:
    #     return False, scwbuff1, scwbuff2, scwbuff3, scwbuff4, scwbuff5
    if len(LIST_CW1_RXDATA) == 0:
        return rt
    for item in LIST_CW1_RXDATA:
        # print('MK_recvdata item', item)
        logging.info('MK_recvdata' + str(item))
        if item[0]:
            ttt = prtlmkIO.islinkorappReturn(item[3], LSIT_MK_CW[0])
            print('MK_recvdata　ttt', ttt)
            # ipos = 0
            # while ipos < len(ttt):
            if item[4] == prtlmkIO_LY.Protocol_MKLINK_TYPE and item[4] == Protocol_TYPE:
                logging.info('模组协议link Rx1:' + ttt[5])
                LIST_CW1_TXDATA.append([item[1], item[2], ttt[2]])
                logging.info('模组协议链路层 Tx:' + ttt[2])
                rt[0] = True
                # break
            elif item[4] == prtlmkIO_LY.Protocol_MKDATA_TYPE and item[4] == Protocol_TYPE:
                # ttt[ipos+2]['FID'] = ttt[ipos+1]
                logging.info('模组协议data Rx2:' + ttt[5])
                # 模组协议数据 自动响应
                ipos = 0
                while ipos < len(ttt):
                    if ttt[ipos+2]['DT'] in ['0100', '0200', '0201', '0202', '7100', '7101'] and ttt[ipos+4] in [prtlmkIO.APDU_SET_Request]:
                        sstx = prtlmkIO.make_MKIO_Response(item[3])
                        LIST_CW1_TXDATA.append([item[1], item[2], sstx])
                        logging.info('模组协议应用自动响应 Tx:' + sstx)
                        # rt[0] = True
                        # break
                    elif ttt[ipos+2]['DT'] in ['4101'] and ttt[ipos+4] in [prtlmkIO.APDU_SET_Request]:
                        sstx = prtlmkIO.make_MKIO_Response(item[3])
                        LIST_CW1_TXDATA.append([item[1], item[2], sstx])
                        logging.info('设置4101响应模组协议 Tx:' + sstx)
                        rt[0] = True
                        scwbuff1 += [item[1], item[2], ttt[ipos+5]]
                        break
                    elif item[2] == icom and ttt[ipos+2]['DT'] == sdt and ttt[ipos+4] in [prtlmkIO.APDU_SET_Request]:
                        print("MK_recvdata APDU_SET_Request ttt", ttt)
                        scwbuff1 += [item[1], item[2], ttt[ipos+5]]
                        rt[0] = True
                        break
                    elif item[2] == icom and ttt[ipos+2]['DT'] == sdt and ttt[ipos+4] in [prtlmkIO.APDU_GET_Response]:
                        print("MK_recvdata APDU_GET_Response ttt", ttt)
                        scwbuff1 += [item[1], item[2], ttt[ipos+5]]
                        rt[0] = True
                        break
                    elif item[2] == icom and ttt[ipos+2]['DT'] == sdt and ttt[ipos+4] in [prtlmkIO.APDU_GET_Request]:
                        print("MK_recvdata APDU_GET_Request ttt", ttt)
                        scwbuff1 += [item[1], item[2], ttt[ipos+5]]
                        rt[0] = True
                        break
                    elif item[0] and item[2] == icom and sdt == '':
                        scwbuff1 += [item[1], item[2], ttt[ipos+5]]
                        rt[0] = True
                        break
                    elif item[0] and iorder == -1 and sdt == '':
                        scwbuff1 += [item[1], item[2], ttt[ipos+5]]
                        rt[0] = True
                        break
                    ipos += 6
            elif item[4] == prtlmkIO_LY.Protocol_13751_TYPE:
                logging.info('控制模块协议 Rx:' + item[3])
                ttt1 = CTRL1375.dealCTRLFrame(item[3])
                print('CTRU_recvdata　ttt', ttt1)
                scwbuff1 += [item[1], item[2], item[3]]
                rt[0] = True
            elif item[4] == prtlmkIO_LY.Protocol_13762_TYPE:
                logging.info('HPLC模块协议 Rx:' + item[3])
                scwbuff1 += [item[1], item[2], item[3]]
                rt[0] = True
            elif item[4] == prtlmkIO_LY.Protocol_13763_TYPE:
                logging.info('远程模块协议 Rx:' + item[3])
                # print('LIST_CW1_RXDATA',item)
                # ttt [True, '0D0A4F4B0D0A', 'AT', '\r\nOK\r\n']
                ttt3 = prtl3763.isATReqest(item[3])
                print('GPRS_recvdata　ttt', ttt3)
                if ttt3[0]:
                    if ttt3[2] in ['AT', 'ATE0']:
                        scwbuff1 += [item[1], item[2], item[3]]
                        rt[0] = True
                        break
                    else:
                        LIST_CW1_TXDATA.append([item[1], item[2], ttt3[1]])
                        logging.info('远程模块协议 Tx:' + ttt3[2])
            elif item[4] == prtlmkIO_LY.Protocol_DATA_TYPE:
            # 数据流
                scwbuff1 += [item[1], item[2], item[3]]
                rt[0] = True
                break
    # for item in LIST_CW2_RXDATA:
    #     if item[0]:
    #         logging.info(item)
    #         print('LIST_CW2_RXDATA', logging.info(item))
    #         ttt = prtlmkIO.islinkorappReturn(item[3], LSIT_MK_CW[1])
    #         if ttt[0] == 0:
    #             # 数据流
    #             scwbuff2 += [ttt[2]]
    #             break
    #         elif ttt[0] == 1:
    #             # 模组协议链路层
    #             LIST_CW2_TXDATA.append([item[1], item[2], ttt[2]])
    #             break
    #         elif ttt[0] == 2:
    #             # 模组协议数据
    #             if item[0] and item[1] == iorder and item[2] == icom:
    #                 scwbuff2 += [ttt[2]]
    #                 break
    #             elif item[0] and iorder == -1:
    #                 scwbuff2 += [ttt[2]]
    #                 break
    #         else:
    #             pass
    # for item in LIST_CW3_RXDATA:
    #     if item[0]:
    #         logging.info(item)
    #         print('LIST_CW3_RXDATA', logging.info(item))
    #         ttt = prtlmkIO.islinkorappReturn(item[3], LSIT_MK_CW[2])
    #         if ttt[0] == 0:
    #             # 数据流
    #             scwbuff3 += [ttt[2]]
    #             break
    #         elif ttt[0] == 1:
    #             # 模组协议链路层
    #             LIST_CW3_TXDATA.append([item[1], item[2], ttt[2]])
    #             break
    #         elif ttt[0] == 2:
    #             # 模组协议数据
    #             if item[0] and item[1] == iorder and item[2] == icom:
    #                 scwbuff3 += [ttt[2]]
    #                 break
    #             elif item[0] and iorder == -1:
    #                 scwbuff3 += [ttt[2]]
    #                 break
    #         else:
    #             pass
    # for item in LIST_CW4_RXDATA:
    #     if item[0]:
    #         logging.info(item)
    #         print('LIST_CW4_RXDATA', logging.info(item))
    #         ttt = prtlmkIO.islinkorappReturn(item[3], LSIT_MK_CW[3])
    #         if ttt[0] == 0:
    #             scwbuff4 += [ttt[2]]
    #             break
    #         elif ttt[0] == 1:
    #             LIST_CW4_TXDATA.append([item[1], item[2], ttt[2]])
    #             break
    #         elif ttt[0] == 2:
    #             if item[0] and item[1] == iorder and item[2] == icom:
    #                 scwbuff4 += [ttt[2]]
    #                 break
    #             elif item[0] and iorder == -1:
    #                 scwbuff4 += [ttt[2]]
    #                 break
    #         else:
    #             pass
    # for item in LIST_CW5_RXDATA:
    #     if item[0]:
    #         logging.info(item)
    #         print('LIST_CW5_RXDATA', logging.info(item))
    #         ttt = prtlmkIO.islinkorappReturn(item[3], LSIT_MK_CW[4])
    #         if ttt[0] == 0:
    #             scwbuff5 += [ttt[2]]
    #             break
    #         elif ttt[0] == 1:
    #             # 模组协议链路层
    #             LIST_CW5_TXDATA.append([item[1], item[2], ttt[2]])
    #             break
    #         elif ttt[0] == 2:
    #             # 模组协议数据
    #             if item[0] and item[1] == iorder and item[2] == icom:
    #                 scwbuff5 += [ttt[2]]
    #                 break
    #             elif item[0] and iorder == -1:
    #                 scwbuff5 += [ttt[2]]
    #                 break
    #         else:
    #             pass
    # ClearMKRXBuff(0)
    while len(LIST_CW1_RXDATA) > 0:
        del LIST_CW1_RXDATA[0:]
    # while len(LIST_CW2_RXDATA) > 0:
    #     del LIST_CW2_RXDATA[0:]
    # while len(LIST_CW3_RXDATA) > 0:
    #     del LIST_CW3_RXDATA[0:]
    # while len(LIST_CW4_RXDATA) > 0:
    #     del LIST_CW4_RXDATA[0:]
    # while len(LIST_CW5_RXDATA) > 0:
    #     del LIST_CW5_RXDATA[0:]
    return rt

# 发送数据
def senddata(sframe):
    schar = General.hexascii(sframe)
    if len(client_socket) > 0:
        ints = len(client_socket) - 1
        client_socket[ints].sendall(schar)
        time.sleep(SYSCONFIG['TXOUTTIME'])
    return True

# 功能模块发送数据
def MK_senddata(sframe):
    schar = General.hexascii(sframe)
    LIST_CW1_TXDATA.append(sframe)
    LIST_CW2_TXDATA.append(sframe)
    LIST_CW3_TXDATA.append(sframe)
    LIST_CW4_TXDATA.append(sframe)
    LIST_CW5_TXDATA.append(sframe)
    return True


def run():
    try:
        conMeter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conMeter.connect((SYSCONFIG['VMETERHOST'], SYSCONFIG['VMETERPORT']))
        time.sleep(3)
        while True:
            # conn.send(("toserver" + str(time.time())).encode())
            if len(lst_vmBuff) > 1:
                # stx = 'toserver:' + str(time.time())
                print('check:' + lst_vmBuff[1])
                conMeter.send(lst_vmBuff[1])
                print('tx:' + lst_vmBuff[1])
                time.sleep(0.2)
                lst_vmBuff[0] = 1
                data = conMeter.recv(1024)
                if len(data) > 0:
                    lst_vmBuff[0] = 2
                    if lst_vmBuff[1].find('set') >= 0:
                        lst_vmBuff[2] = data
                    elif lst_vmBuff[1].find('get') >= 0:
                        lst_vmBuff[2] = data
                    print('rx:' + data)
            # print("来自服务端数据 :" + data + "|" + str(time.time()))
            time.sleep(0.1)
    except:
        print("虚拟表服务器连接异常,尝试重新连接 (10s) ...")
        conMeter.close()
        time.sleep(10)  # 断开连接后,每10s重新连接一次
        run()
    finally:
        print("客户端已关闭 ...")

# 检查配置文件etype oop mrtu
def readexcel(lfile, sname, etype):
    workbook = xlrd.open_workbook(lfile)
    rtem = {}
    for ns in workbook.sheet_names():
        sheet2 = workbook.sheet_by_name(ns)
        if ns == sname:
            for ir in range(0, sheet2.nrows):
                rowvalue = {}
                if etype == "oop_mk":
                    rowvalue['nu'] = sheet2.cell(ir, 0).value
                    rowvalue['cut'] = sheet2.cell(ir, 1).value
                    rowvalue['name'] = sheet2.cell(ir, 2).value
                    rowvalue['protype'] = sheet2.cell(ir, 3).value
                    rowvalue['secure'] = sheet2.cell(ir, 4).value
                    rowvalue['vadd'] = sheet2.cell(ir, 5).value
                    rowvalue['addrtype'] = sheet2.cell(ir, 6).value
                    rowvalue['caddr'] = sheet2.cell(ir, 7).value
                    rowvalue['op'] = sheet2.cell(ir, 8).value
                    rowvalue['oad_omd'] = sheet2.cell(ir, 9).value
                    rowvalue['param'] = sheet2.cell(ir, 10).value
                    rowvalue['save'] = sheet2.cell(ir, 11).value
                    rowvalue['delay'] = sheet2.cell(ir, 12).value
                    rowvalue['expect'] = sheet2.cell(ir, 13).value
                    rowvalue['real'] = sheet2.cell(ir, 14).value
                    rowvalue['result'] = sheet2.cell(ir, 15).value
                    rtem[ir] = rowvalue
                elif etype == 'ml':
                    rowvalue['nu'] = sheet2.cell(ir, 0).value
                    rowvalue['cut'] = sheet2.cell(ir, 1).value
                    rowvalue['name'] = sheet2.cell(ir, 2).value
                    rowvalue['alias'] = sheet2.cell(ir, 3).value
                    rowvalue['rtutype'] = sheet2.cell(ir, 4).value
                    rowvalue['remarks'] = sheet2.cell(ir, 5).value
                    rtem[ir] = rowvalue
                elif etype == 'mrtu':
                    rowvalue['rtu'] = sheet2.cell(ir, 0).value.encode('utf-8')
                    rowvalue['M1'] = sheet2.cell(ir, 1).value.encode('utf-8')
                    rowvalue['M2'] = sheet2.cell(ir, 2).value.encode('utf-8')
                    rowvalue['M3'] = sheet2.cell(ir, 3).value.encode('utf-8')
                    rowvalue['M4'] = sheet2.cell(ir, 4).value.encode('utf-8')
                    rowvalue['M5'] = sheet2.cell(ir, 5).value.encode('utf-8')
                    rowvalue['M6'] = sheet2.cell(ir, 6).value.encode('utf-8')
                    rowvalue['M7'] = sheet2.cell(ir, 7).value.encode('utf-8')
                    rowvalue['M8'] = sheet2.cell(ir, 8).value.encode('utf-8')
                    rowvalue['07data'] = sheet2.cell(ir, 9).value.encode('utf-8')
                    rtem[ir] = rowvalue
                elif etype == 'vmdata':
                    rowvalue['no'] = sheet2.cell(ir, 0).value
                    rowvalue['name'] = sheet2.cell(ir, 1).value
                    rowvalue['dt'] = sheet2.cell(ir, 2).value.encode('utf-8')
                    rowvalue['07id'] = sheet2.cell(ir, 3).value.encode('utf-8')
                    rowvalue['97id'] = sheet2.cell(ir, 4).value
                    # print(rowvalue['97id'])
                    rtem[ir] = rowvalue
    return rtem

# save
def saveasexcel(temfile, tlist):
    # print temfile
    wb = xlwt.Workbook()
    sheet0 = wb.add_sheet(tlist['fname'], cell_overwrite_ok=True)
    # print tlist[0]['name']
    if tlist.__contains__('fname'):
        del tlist['fname']
    for key in tlist:
        # print(tlist[key]['name'])
        # print(tlist[key]['nu'])
        if tlist[key]['nu'] == u'步骤':
            sheet0.write(0, 0, tlist[key]['nu'])
            sheet0.write(0, 1, tlist[key]['cut'])
            sheet0.write(0, 2, tlist[key]['name'])
            sheet0.write(0, 3, tlist[key]['protype'])
            sheet0.write(0, 4, tlist[key]['secure'])
            sheet0.write(0, 5, tlist[key]['vadd'])
            sheet0.write(0, 6, tlist[key]['addrtype'])
            sheet0.write(0, 7, tlist[key]['caddr'])
            sheet0.write(0, 8, tlist[key]['op'])
            sheet0.write(0, 9, tlist[key]['oad_omd'])
            sheet0.write(0, 10, tlist[key]['param'])
            sheet0.write(0, 11, tlist[key]['save'])
            sheet0.write(0, 12, tlist[key]['delay'])
            sheet0.write(0, 13, tlist[key]['expect'])
            sheet0.write(0, 14, tlist[key]['real'])
            sheet0.write(0, 15, tlist[key]['result'])
        else:
            sheet0.write(key, 0, tlist[key]['nu'])
            sheet0.write(key, 1, tlist[key]['cut'])
            sheet0.write(key, 2, tlist[key]['name'])
            sheet0.write(key, 3, tlist[key]['protype'])
            sheet0.write(key, 4, tlist[key]['secure'])
            sheet0.write(key, 5, tlist[key]['vadd'])
            sheet0.write(key, 6, tlist[key]['addrtype'])
            sheet0.write(key, 7, tlist[key]['caddr'])
            sheet0.write(key, 8, tlist[key]['op'])
            sheet0.write(key, 9, tlist[key]['oad_omd'])
            sheet0.write(key, 10, tlist[key]['param'])
            sheet0.write(key, 11, tlist[key]['save'])
            sheet0.write(key, 12, tlist[key]['delay'])
            sheet0.write(key, 13, tlist[key]['expect'])
            sheet0.write(key, 14, tlist[key]['real'])
            sheet0.write(key, 15, tlist[key]['result'])
    wb.save(temfile)


# 检查所需配置文件是否在路径目录下存在
def checkfl(pfiles):
    path = os.getcwd() + "\config"
    files = os.listdir(path)
    count = 0
    for temf in pfiles:
        for file in files:
            if pfiles[temf] == file:
                # print (file.decode('gbk'))
                count = count + 1
    if len(pfiles) == count:
        return True
    else:
        return False


# 检查本用例所需的设备
def checkset():
    if initsyscom(nzsc_Y220mode):
        return True
    else:
        return False


#  启动虚拟表连接是否成功
def convmeter():
    lst_vmBuff.append(0)
    lst_vmBuff.append('set M1 data value 1D000100 23')
    lst_vmBuff.append('')
    told = time.time()
    brtn = False
    while True:
        if lst_vmBuff[0] == 2:
            brtn = True
            del lst_vmBuff[:3]
            break
        tnew = time.time()
        if (tnew - told) > 5.0:
            if len(lst_vmBuff) == 3:
                del lst_vmBuff[:3]
            break
        time.sleep(0.1)
    return brtn

# 检查在线
def checkRtuline():
    itime = 0.0
    istart = time.time()
    idelay = 60.0
    breturn = False
    while itime < idelay:
        time.sleep(0.1)
        if len(client_socket) > 0:
            breturn = True
            break
        itime = time.time() - istart
    return  breturn

# 获取终端信息
def getRtuini():
    sys_config = configparser.ConfigParser()
    syspath = os.getcwd() + "\config\sysmkIO.ini"
    sys_config.read(syspath)
    rtuini = {}
    rtuini['ADDR'] = sys_config.get("RTU_CONFIG", "ADDR")
    rtuini['TYPE'] = sys_config.get("RTU_CONFIG", "TYPE")
    rtuini['LINETYPE'] = sys_config.get("RTU_CONFIG", "LINETYPE")
    rtuini['Un'] = float(sys_config.get("RTU_CONFIG", "Un"))
    rtuini['In'] = float(sys_config.get("RTU_CONFIG", "In"))
    rtuini['PROTCOL'] = sys_config.get("RTU_CONFIG", "PROTCOL")
    rtuini['METERTYPE'] = sys_config.get("RTU_CONFIG", "METERTYPE")
    rtuini['COMTYPE'] = sys_config.get("RTU_CONFIG", "COMTYPE")
    rtuini['YK'] = int(sys_config.get("RTU_CONFIG", "YK"))
    rtuini['MC'] = int(sys_config.get("RTU_CONFIG", "MC"))
    rtuini['ALARM'] = int(sys_config.get("RTU_CONFIG", "ALARM"))
    rtuini['CW1_PORT'] = sys_config.get("RTU_CONFIG", "CW1_PORT")
    rtuini['CW2_PORT'] = sys_config.get("RTU_CONFIG", "CW2_PORT")
    rtuini['CW3_PORT'] = sys_config.get("RTU_CONFIG", "CW3_PORT")
    rtuini['CW4_PORT'] = sys_config.get("RTU_CONFIG", "CW4_PORT")
    rtuini['CW5_PORT'] = sys_config.get("RTU_CONFIG", "CW5_PORT")
    rtuini['CW_PORT_BAUDRATE'] = int(sys_config.get("RTU_CONFIG", "CW_PORT_BAUDRATE"))
    rtuini['DYSET_PORT'] = sys_config.get("RTU_CONFIG", "DYSET_PORT")
    rtuini['TYPE'] = sys_config.get("RTU_CONFIG", "TYPE")
    print('rtuini:', rtuini)
    return rtuini

# mkname 'RS485' -> {'MK_SETTYPY':'GBR43-TLY2936',...}
def getMKini(mkname):
    sys_config = configparser.ConfigParser()
    syspath = os.getcwd() + "\config\sysmkIO.ini"
    sys_config.read(syspath)
    mkini = []
    mkini.append(sys_config.get(mkname, "MK_SETTYPY"))
    mkini.append(sys_config.get(mkname, "MK_SETID"))
    mkini.append(sys_config.get(mkname, "MK_SOFTWARE_V"))
    mkini.append(sys_config.get(mkname, "MK_SOFTWAEE_DATE"))
    mkini.append(sys_config.get(mkname, "MK_HARDWARE_V"))
    mkini.append(sys_config.get(mkname, "MK_HARDWARE_DATE"))
    mkini.append(sys_config.get(mkname, "MK_MAC_CODE"))
    # mkini['MK_SETTYPY'] = sys_config.get(mkname, "MK_SETTYPY")
    # mkini['MK_SETID'] = sys_config.get(mkname, "MK_SETID")
    # mkini['MK_SOFTWARE_V'] = sys_config.get(mkname, "MK_SOFTWARE_V")
    # mkini['MK_SOFTWAEE_DATE'] = sys_config.get(mkname, "MK_SOFTWAEE_DATE")
    # mkini['MK_HARDWARE_V'] = sys_config.get(mkname, "MK_HARDWARE_V")
    # mkini['MK_HARDWARE_DATE'] = sys_config.get(mkname, "MK_HARDWARE_DATE")
    # mkini['MK_MAC_CODE'] = sys_config.get(mkname, "MK_MAC_CODE")
    # mkini['COMTYPE'] = sys_config.get(mkname, "COMTYPE")
    return mkini

# 依据配置槽位
def set_MK_CW(ldata):
    sdata = ldata['param']
    ldata = sdata.split(',')
    if len(ldata) >= 5:
        for i in range(0,5,1):
            if ldata[i] in prtlmkIO.ENUM_MK:
                LSIT_MK_CW[i] = ldata[i]
    else:
        return  False
    return True


# 设置电源
def setsource(ldata):
    # logging.info(slist)
    print('setsource', ldata)
    sdata = ldata['param']
    if StartSource(sdata):
        logging.info(u'设置电源成功！')
        ldata['real'] = 'OK'
        if ldata['expect'].find(ldata['real']) >= 0:
            ldata['result'] = u'合格'
        else:
            ldata['result'] = u'不合格'
        return True
    else:
        logging.info(u'设置电源失败！')
        ldata['real'] = 'NO'
        if ldata['expect'].find(ldata['real']) >= 0:
            ldata['result'] = u'合格'
        else:
            ldata['result'] = u'不合格'
        return False

# 读电源数据MMinData={"Mn":"M1","ID":"01010000","Value":"6.78,1801020102"}
def readsource(dts):
    dvalue = ReadSource()
    rl = []
    if len(dvalue) < 3:
        logging.info(u'读电源失败！')
        return []
    else:
        logging.info(u'读电源成功！')
        for j in dts:
            # if j == '02010100':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Ua']}]
            # elif j == '02010200':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Ub']}]
            # elif j == '02010300':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Uc']}]
            # elif j == '02020100':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Ia']}]
            # elif j == '02020200':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Ib']}]
            # elif j == '02020300':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Ic']}]
            # elif j == '02030000':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['P']}]
            # elif j == '02030100':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Pa']}]
            # elif j == '02030200':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Pb']}]
            # elif j == '02030300':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Pc']}]
            # elif j == '02040000':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['R']}]
            # elif j == '02040100':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Ra']}]
            # elif j == '02040200':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Rb']}]
            # elif j == '02040300':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Rc']}]
            # elif j == '02060000':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Coso']}]
            # elif j == '02060100':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Cosa']}]
            # elif j == '02060200':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Cosb']}]
            # elif j == '02060300':
            #     rl += [{'mn': 'M0', 'id': j, 'value': dvalue['Cosc']}]
            # elif j == '02070100':
            #     rl += [{'mn': 'M0', 'id': j, 'value': '0.1'}]
            # elif j == '02070200':
            #     rl += [{'mn': 'M0', 'id': j, 'value': '120.01'}]
            # elif j == '02070300':
            #     rl += [{'mn': 'M0', 'id': j, 'value': '240.01'}]
            # elif j == '02070400':
            #     fv = 0.1 + math.acos(float(dvalue['Cosa'])) * 180 / math.pi
            #     vl = float('%.1f' % fv)
            #     rl += [{'mn': 'M0', 'id': j, 'value': str(vl)}]
            # elif j == '02070500':
            #     fv = 120.01 + math.acos(float(dvalue['Cosb'])) * 180 / math.pi
            #     vl = float('%.1f' % fv)
            #     rl += [{'mn': 'M0', 'id': j, 'value': str(vl)}]
            # elif j == '02070600':
            #     fv = 240.01 + math.acos(float(dvalue['Cosc'])) * 180 / math.pi
            #     vl = float('%.1f' % fv)
            #     rl += [{'mn': 'M0', 'id': j, 'value': str(vl)}]
            pass
    for i in rl:
        logging.info(i)
    return rl


# 配置文件夹
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---new folder---")
        print("---OK---")
    else:
        print("---There is this folder!---")


# 初始化配置文件 载入系统配置
def initsysconfig():
    try:
        sys_config = configparser.ConfigParser()
        syspath = os.getcwd() + "\config\sysmkIO.ini"
        sys_config.read(syspath)
        SYSCONFIG['VMETERHOST'] = sys_config.get("SYS_CONFIG", "VMETERHOST")
        SYSCONFIG['VMETERPORT'] = int(sys_config.get('SYS_CONFIG', 'VMETERPORT'))
        SYSCONFIG['SERVERIP'] = sys_config.get('SYS_CONFIG', 'SERVERIP')
        SYSCONFIG['SERVERPORT'] = int(sys_config.get('SYS_CONFIG', 'SERVERPORT'))

        SYSCONFIG['SSH_SERVERIP'] = sys_config.get('SYS_CONFIG', 'SSH_SERVERIP')
        SYSCONFIG['SSH_SERVERPORT'] = int(sys_config.get('SYS_CONFIG', 'SSH_SERVERPORT'))

        SYSCONFIG['DSOCKTTIMEOUT'] = int(sys_config.get('SYS_CONFIG', 'DSOCKTTIMEOUT'))
        SYSCONFIG['BUFFSIZE'] = int(sys_config.get('SYS_CONFIG', 'BUFFSIZE'))
        # 接收超时
        SYSCONFIG['RXOUTTIME'] = float(sys_config.get('SYS_CONFIG', 'RXOUTTIME'))
        # 发送
        SYSCONFIG['TXOUTTIME'] = float(sys_config.get('SYS_CONFIG', 'TXOUTTIME'))
        # 间隔
        SYSCONFIG['JGTIME'] = float(sys_config.get('SYS_CONFIG', 'JGTIME'))
        # 虚拟表超时
        SYSCONFIG['VMOUTTIME'] = float(sys_config.get('SYS_CONFIG', 'VMOUTTIME'))
        # print(SYSCONFIG)
        logging.info('载入系统配置文件成功!')
    except:
        logging.info('载入系统配置文件sys失败!', syspath)




# 初始化
def initModel():
    # print(sys.version)
    # 配置文件夹
    flog = os.getcwd() + '\log'
    mkdir(flog)
    fconfig = os.getcwd() + '\config'
    mkdir(flog)
    freport = os.getcwd() + '\\report'
    mkdir(flog)
    snow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%y/%m/%d %H:%M:%S',
                        filename= os.getcwd() + '\log\\' + snow + 'MKtest.log', level=logging.DEBUG)
    # 载入系统配置
    initsysconfig()
    # 检查电源是否正常工作，读取源数据
    logging.info('开始检查电源!')
    # print('开始检查电源!', snow)
    # if checkset():
    #     logging.info('标准源准备好!')
    # else:
    #     logging.warning('标准源未准备好!')
    #     exit()
    # 检查终端是否在线
    # logging.info(u'开始检查终端在线!')
    # if checkRtuline():
    #     logging.info(u'终端在线!')
    # else:
    #     logging.warning(u'终端不在线!')
    #     exit()

# 定义常量
paramfiles = {'parameter': '互换性自动化测试用例集.xlsx'}


# 等待
def wait(ldata):
    try:
        if isinstance(ldata['delay'], float):
            idelay = ldata['delay']
        else:
            idelay = float(ldata['delay'].encode('utf-8'))
        time.sleep(idelay)
    except ValueError:
        return False
    return True

# 等待1376.2数据
def wait13762(ldata):
    itime = 0.0
    istart = time.time()
    # rframe = ''
    idelay = float(ldata['delay'])
    # tr = ldata['op']
    # print('oad_omd', type(ldata['oad_omd']))
    # ClearMKRXBuff(0)
    stem = ""
    while itime < idelay:
        time.sleep(0.1)
        rframe = MK_recvdata(-1, -1, -1, prtlmkIO_LY.Protocol_13762_TYPE)
        if rframe[0]:
            # print('数据流接收 Rx:', rframe[1][2])
            logging.info("数据查询接收13762Rx:" + rframe[1][2])
            logging.info("数据查询接收13762解析:" + str(prtl3762.Analyse113762frame(rframe[1][2])))
            stem += rframe[1][2]+';'
        itime = time.time() - istart
        # print('wait13762 ', itime, idelay, ldata['nu'])
    if len(stem) > 1024:
        ldata['real'] = stem[:1024]
    else:
        ldata['real'] = stem
    if len(stem) > 0:
        ldata['result'] = u'不合格'
    else:
        ldata['result'] = u'合格'
    return 1

# 清除接收区 itype = 0 all
def ClearMKRXBuff(itype):
    if itype == 0:
        for i in LIST_CW1_RXDATA:
            logging.info('ClearMKRXBuff' + str(i))
        del LIST_CW1_RXDATA[0:]
        del LIST_CW2_RXDATA[0:]
        del LIST_CW3_RXDATA[0:]
        del LIST_CW4_RXDATA[0:]
        del LIST_CW5_RXDATA[0:]
    elif itype == 1:
        for i in LIST_CW1_RXDATA:
            logging.info('ClearMKRXBuff' + str(i))
        del LIST_CW1_RXDATA[0:]
    elif itype == 2:
        del LIST_CW2_RXDATA[0:]
    elif itype == 3:
        del LIST_CW3_RXDATA[0:]
    elif itype == 4:
        del LIST_CW4_RXDATA[0:]
    elif itype == 5:
        del LIST_CW5_RXDATA[0:]
    else:
        pass
    return True

# 模块同步响应处理
def MK_Syn_GetResponse(ldata):
    # 立刻进入等待
    # frm['CTRL'] = 'C2'
    itime = 0.0
    istart = time.time()
    rframe = ''
    idelay = float(ldata['delay'])
    # print('MK_Syn_GetResponse itime', itime, idelay)
    ClearMKRXBuff(0)
    while itime < idelay:
        time.sleep(0.1)
        # print('MK_Syn_GetResponse itime', itime, idelay)
        rframe = MK_recvdata(-1, prtlmkIO_LY.COM_DATA1, ldata['oad_omd'], prtlmkIO_LY.Protocol_MKDATA_TYPE)
        if rframe[0]:
            logging.info(rframe[1][2])
            # print('模组数据读取响应 Rx:', rframe[1][2])
            # print(rframe[1])
            tt = prtlmkIO.Receive(rframe[1][2])
            # print('tt', tt)
            if tt[0]:
                frm = {}
                frm['CTRL'] = 'C2'
                frm['FID'] = tt[2]
                if ldata['oad_omd'] in ['0000']:
                    dpr = getMKini(LSIT_MK_CW[0])
                else:
                    dpr = ldata['param']
                # print('op dpr', ldata['op'], ldata['oad_omd'], dpr)
                frm['APDU'] = prtlmkIO.make_MKIO_APDU_Response(ldata['op'], ldata['oad_omd'], dpr)
                # print('frm', frm)
                ss = prtlmkIO.Make_MKIO_Frame(frm)
                # print('ss', rframe[1][0], rframe[1][1], ss)
                LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], ss])
                logging.info("模组数据读取响应 Tx:" + ss)
                ldata['real'] = "读取响应成功"
            else:
                ldata['real'] = "读取响应失败"
            # break
        itime = time.time() - istart
    if rframe[0] == False:
        # bcnt = False
        logging.info('MK_Syn_GetResponse read Rx:Null')
        ldata['real'] = "读取响应失败"
    return 1


# 模块同步设置响应处理
def MK_Syn_SetResponse(ldata):
    # 立刻进入等待
    # frm['CTRL'] = 'C2'
    # 立刻进入等待
    ClearMKRXBuff(0)
    itime = 0.0
    istart = time.time()
    rframe = ''
    idelay = float(ldata['delay'])
    ldata['real'] = "设置响应失败"
    while itime < idelay:
        time.sleep(0.2)
        rframe = MK_recvdata(-1, prtlmkIO_LY.COM_MANGER, ldata['oad_omd'], prtlmkIO_LY.Protocol_MKDATA_TYPE)
        if rframe[0] and ldata['oad_omd'] in rframe[1][2]:
            tmkr = prtlmkIO.Receive(rframe[1][2])
            if tmkr[0]:
                if tmkr[3]['DT'] == ldata['oad_omd']:
                    lsr = tmkr[3]['Value']
                    ldata['real'] = "设置响应成功:" + lsr
            break
        elif rframe[0]:
            logging.info("收到非响应数据:" + rframe[1][2])
        itime = time.time() - istart
    if expectorreal(ldata['expect'], ldata['real']):
        ldata['result'] = u'合格'
    else:
        ldata['result'] = u'不合格'
    return 1


# 脉冲模块同步响应处理
def MK_MC_GetResponse(ldata):
    # 立刻进入等待
    # frm['CTRL'] = 'C2'
    ldata['real'] = "读取响应失败"
    itime = 0.0
    istart = time.time()
    rframe = ''
    idelay = float(ldata['delay'])
    # print('MK_Syn_GetResponseFillGrid itime', itime, idelay)
    ClearMKRXBuff(0)
    dpr = prtlmkIO.strtolist(ldata['param'])
    print('MK_MC_GetResponse', dpr)
    if len(dpr) < 4:
        logging.info('输入错误参数:'+ ldata['param'])
        return 1
    base = []
    zl = []
    for i in range(0, len(dpr), 1):
        if len(dpr[i]) == 2:
            sp = dpr[i][0].split('+')
            sp1 = dpr[i][1].split('+')
            if len(sp) == 2 and len(sp1) == 2:
                base.append([int(sp[0]), int(sp1[0])])
                zl.append([int(sp[1]), int(sp1[1])])
            else:
                base.append([0, 0])
                zl.append([10, 1000])
        else:
            base.append([0, 0])
            zl.append([10, 1000])
    print('base zl', base, zl)
    icount = 0
    while itime <= idelay:
        time.sleep(0.1)
        # print('MK_Syn_GetResponseFillGrid itime', itime, idelay)
        rframe = MK_recvdata(-1, prtlmkIO_LY.COM_DATA1, ldata['oad_omd'], prtlmkIO_LY.Protocol_MKDATA_TYPE)
        if rframe[0]:
            logging.info(rframe[1][2])
            tt = prtlmkIO.Receive(rframe[1][2])
            # print('tt', tt)
            if tt[0]:
                frm = {}
                frm['CTRL'] = 'C2'
                frm['FID'] = tt[2]
                for i in range(0, len(base), 1):
                    base[i][0] += zl[i][0]
                    base[i][1] += zl[i][1]
                dppp = str(base)
                # print('dppp', dppp)
                logging.info('模组数据响应值:' + dppp)
                frm['APDU'] = prtlmkIO.make_MKIO_APDU_Response(ldata['op'], ldata['oad_omd'], dppp)
                # print('frm', frm)
                ss = prtlmkIO.Make_MKIO_Frame(frm)
                # print('ss', rframe[1][0], rframe[1][1], ss)
                LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], ss])
                logging.info("模组数据读取响应 Tx:" + ss)
                ldata['real'] = "读取响应成功"
                icount += 1
        itime = time.time() - istart
    return 1

# 模块同步响应处理处理表格
def MK_Syn_GetResponseFillGrid(ldata):
    # 立刻进入等待
    # frm['CTRL'] = 'C2'
    ldata['real'] = "读取响应失败"
    itime = 0.0
    istart = time.time()
    rframe = ''
    idelay = float(ldata['delay'])
    # print('MK_Syn_GetResponseFillGrid itime', itime, idelay)
    ClearMKRXBuff(0)
    while itime < idelay:
        time.sleep(0.1)
        # print('MK_Syn_GetResponseFillGrid itime', itime, idelay)
        rframe = MK_recvdata(-1, prtlmkIO_LY.COM_DATA1, ldata['oad_omd'], prtlmkIO_LY.Protocol_MKDATA_TYPE)
        if rframe[0]:
            logging.info(rframe[1][2])
            tt = prtlmkIO.Receive(rframe[1][2])
            # print('tt', tt)
            if tt[0]:
                frm = {}
                frm['CTRL'] = 'C2'
                frm['FID'] = tt[2]
                if ldata['oad_omd'] in ['0000']:
                    dpr = getMKini(LSIT_MK_CW[0])
                else:
                    dpr = ldata['param']
                # print('op dpr', ldata['op'], ldata['oad_omd'], dpr)
                frm['APDU'] = prtlmkIO.make_MKIO_APDU_Response(ldata['op'], ldata['oad_omd'], dpr)
                # print('frm', frm)
                ss = prtlmkIO.Make_MKIO_Frame(frm)
                # print('ss', rframe[1][0], rframe[1][1], ss)
                LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], ss])
                logging.info("模组数据读取响应 Tx:" + ss)
                ldata['real'] = "读取响应成功"
                if ldata['save'].find('密文') >= 0:
                    pass
                else:
                    break
            # break
        itime = time.time() - istart
    return 1

# 模块升级响应处理
def MK_FileUp_Response(ldata, iniRtu, ipiid):
    ClearMKRXBuff(0)
    time.sleep(0.1)
    sapdu = prtlmkIO.dMKOPName[ldata['op']]
    if sapdu == prtlmkIO.APDU_SET_Response:
        itime = 0.0
        istart = time.time()
        # rframe = ''
        idelay = float(ldata['delay'])
        tr = ldata['param'].split(',')
        trrj = []
        for i in range(0, len(tr), 1):
            trrj += tr[i].split('_')
        icn = 0
        while itime < idelay:
            time.sleep(0.1)
            rframe = MK_recvdata(-1, prtlmkIO_LY.COM_MANGER, '0203', prtlmkIO_LY.Protocol_MKDATA_TYPE)
            if rframe[0] and '0203' in rframe[1][2] and trrj[icn] == '1':
                logging.info('模块升级正确接收' + rframe[1][2])
                print('模块升级数据读取设置 Rx:', rframe[1][2])
                tt = prtlmkIO.Receive(rframe[1][2])
                if tt[0]:
                    icn += 1
                    frm = {}
                    frm['CTRL'] = 'C2'
                    frm['FID'] = tt[2]
                    dpr = []
                    frm['APDU'] = prtlmkIO.make_MKIO_APDU_Response(ldata['op'], ldata['oad_omd'], dpr)
                    ss = prtlmkIO.Make_MKIO_Frame(frm)
                    LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], ss])
                    logging.info("模块升级响应 Tx:" + ss)
            elif rframe[0] and trrj[icn] == '0' and '0203' in rframe[1][2]:
                icn += 1
                logging.info("模块升级不响应")
                time.sleep(5.0)
            if icn >= len(trrj): break
            # print('itime', itime, idelay)
            itime = time.time() - istart
        if icn == len(trrj):
            ldata['real'] = "升级成功"
        else:
            ldata['real'] = "升级失败"
    return 1


# 虚拟模块林洋协议处理流程处理流程
def MK_Requse_Response(ldata, iniRtu, ipiid):
    ipiid = ipiid % 256
    frm = {}
    sapdu = prtlmkIO.dMKOPName[ldata['op']]
    # print('MK_Requse_Response:sapdu:', sapdu)
    if sapdu == prtlmkIO.APDU_GET_Request:
        # 立刻组帧
        print('MK_Requse_Response:prtlmkIO.APDU_GET_Request:', sapdu)
        frm['CTRL'] = '82'
        frm['FID'] = General.inttosHex(ipiid, 2)
        frm['APDU'] = '02' + ldata['oad_omd']
        ss_ly = prtlmkIO.Make_MKIO_Frame(frm)
        # print('Make_MKIO_Frame:', ss_ly)
        # frame = []
        # frame.append(ipiid, prtlmkIO_LY.COM_MANGER, ss_ly)
        # MK_senddata(frame)
        LIST_CW1_TXDATA.append([ipiid, prtlmkIO_LY.COM_MANGER, ss_ly])
        logging.info('模组数据读取请求Tx:' + ss_ly)
        ClearMKRXBuff(0)
        itime = 0.0
        istart = time.time()
        # rframe = ''
        idelay = float(ldata['delay'])
        while itime < idelay:
            time.sleep(0.2)
            rframe = MK_recvdata(ipiid, prtlmkIO_LY.COM_MANGER, ldata['oad_omd'], prtlmkIO_LY.Protocol_MKDATA_TYPE)
            if rframe[0] and ldata['oad_omd'] in rframe[1][2]:
                break
            elif rframe[0]:
                logging.info("收到非响应数据:" + rframe[1][2])
            itime = time.time() - istart
        if rframe[0] == False:
            # bcnt = False
            logging.info('MK_Requse_Response read Rx:Null')
        else:
            logging.info('模组数据读取请求Rx:' + rframe[1][2])
            lsr = ''
            icw = 1
            # for item in rframe[1:0]:
            tmkr = prtlmkIO.Receive(rframe[1][2])
            if tmkr[0]:
                if tmkr[3]['DT'] == ldata['oad_omd']:
                    lsr += '槽位' + str(icw) + "读取:" + tmkr[3]['Value']+';'
                # icw += 1
            ldata['real'] = lsr
            logging.info('模组数据读取请求Rx:' + lsr)
            # print('MK_Requse_Response real', ldata['real'])
    elif sapdu == prtlmkIO.APDU_CONNECT_Request:
        pass
    elif sapdu == prtlmkIO.APDU_CONNECT_Response:
        print('MK_Requse_Response:prtlmkIO.APDU_CONNECT_Response:', sapdu)
        ClearMKRXBuff(0)
        itime = 0.0
        istart = time.time()
        rframe = ''
        idelay = float(ldata['delay'])
        while itime < idelay:
            time.sleep(0.2)
            rframe = MK_recvdata(-1, prtlmkIO_LY.COM_MANGER, '', prtlmkIO_LY.Protocol_MKLINK_TYPE)
            if rframe[0]:
                ldata['real'] = "链路协商响应成功"
                break
            itime = time.time() - istart
        if rframe[0] == False:
            # bcnt = False
            ldata['real'] = "链路协商响应失败"
            logging.info('MK_Requse_Response APDU_CONNECT_Response read Rx:Null')
    elif sapdu == prtlmkIO.APDU_SET_Request:
        # 立刻组帧
        frm['CTRL'] = '42'
    elif sapdu == prtlmkIO.APDU_REPORT_Notification_Response:
        # 立刻组帧
        frm['CTRL'] = '02'
    elif sapdu == prtlmkIO.APDU_GET_Response:
        # 立刻进入等待
        # frm['CTRL'] = 'C2'
        ClearMKRXBuff(0)
        itime = 0.0
        istart = time.time()
        rframe = ''
        idelay = float(ldata['delay'])
        while itime < idelay:
            time.sleep(0.2)
            rframe = MK_recvdata(-1, prtlmkIO_LY.COM_MANGER, ldata['oad_omd'], prtlmkIO_LY.Protocol_MKDATA_TYPE)
            if rframe[0] and ldata['oad_omd'] in rframe[1][2]:
                break
            elif rframe[0]:
                logging.info("收到非响应数据:" + rframe[1][2])
            itime = time.time() - istart
        if rframe[0] == False:
            # bcnt = False
            logging.info('MK_APDU_GET_Response read Rx:Null')
            ldata['real'] = "读取响应失败"
        else:
            logging.info(rframe[1][2])
            # print('模组数据读取响应 Rx:', rframe[1][2])
            # print(rframe[1])
            tt = prtlmkIO.Receive(rframe[1][2])
            # print('tt', tt)
            if tt[0]:
                frm = {}
                frm['CTRL'] = 'C2'
                frm['FID'] = tt[2]
                if ldata['oad_omd'] in ['0000']:
                    dpr = getMKini(LSIT_MK_CW[0])
                else:
                    dpr = ldata['param']
                # print('op dpr', ldata['op'], ldata['oad_omd'], dpr)
                frm['APDU'] = prtlmkIO.make_MKIO_APDU_Response(ldata['op'], ldata['oad_omd'], dpr)
                # print('frm', frm)
                ss = prtlmkIO.Make_MKIO_Frame(frm)
                # print('ss', rframe[1][0], rframe[1][1], ss)
                LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], ss])
                logging.info("模组数据读取响应 Tx:" + ss)
                ldata['real'] = "读取响应成功"
            else:
                ldata['real'] = "读取响应失败"
    elif sapdu == prtlmkIO.APDU_SET_Response:
        # 立刻进入等待
        ClearMKRXBuff(0)
        itime = 0.0
        istart = time.time()
        rframe = ''
        idelay = float(ldata['delay'])
        while itime < idelay:
            time.sleep(0.2)
            rframe = MK_recvdata(-1, prtlmkIO_LY.COM_MANGER, ldata['oad_omd'], prtlmkIO_LY.Protocol_MKDATA_TYPE)
            if rframe[0] and ldata['oad_omd'] in rframe[1][2]:
                break
            elif rframe[0]:
                logging.info("收到非响应数据:" + rframe[1][2])
            itime = time.time() - istart
        if rframe[0]:
            tmkr = prtlmkIO.Receive(rframe[1][2])
            if tmkr[0]:
                if tmkr[3]['DT'] == ldata['oad_omd']:
                    lsr = tmkr[3]['Value']
                    ldata['real'] = "设置响应成功:" + lsr
        else:
            ldata['real'] = "设置响应失败"
    elif sapdu == prtlmkIO.APDU_REPORT_Notification:
        # 立刻进入等待
        ClearMKRXBuff(0)
        frm = {}
        frm['CTRL'] = '82'
        frm['FID'] = General.inttosHex(ipiid, 2)
        dpr = ldata['param']
        frm['APDU'] = prtlmkIO.make_MKIO_APDU_Response(ldata['op'], ldata['oad_omd'], dpr)
        ss = prtlmkIO.Make_MKIO_Frame(frm)
        LIST_CW1_TXDATA.append([ipiid, prtlmkIO_LY.COM_DATA1, ss])
        logging.info('模组数据上报Tx:' + ss)
        itime = 0.0
        istart = time.time()
        idelay = float(ldata['delay'])
        # rframe = []
        while itime < idelay:
            time.sleep(0.1)
            rframe = MK_recvdata(-1, prtlmkIO_LY.COM_DATA1, '', prtlmkIO_LY.Protocol_MKDATA_TYPE)
            if rframe[0] and ldata['oad_omd'] in rframe[1][2]:
                logging.info('模组数据上报Rx:' + rframe[1][2])
                tmkr = prtlmkIO.Receive(rframe[1][2])
                if len(tmkr) == 6:
                    if tmkr[3]['DT'] in ldata['oad_omd']:
                        ldata['real'] = '上报成功'
                    else:
                        ldata['real'] = '上报失败'
                elif len(tmkr) == 12:
                    if (tmkr[3]['DT'] in ldata['oad_omd']) or (tmkr[9]['DT'] in ldata['oad_omd']):
                        ldata['real'] = '上报成功'
                    else:
                        ldata['real'] = '上报失败'
                break
            elif rframe[0]:
                logging.info("收到非响应数据:" + rframe[1][2])
            itime = time.time() - istart
        # if rframe[0] == False:
        #     logging.info('MK_Requse_Response APDU_REPORT_Notification Rx:Null')
        # else:
        #     pass
            # logging.info('模组数据上报Rx:' + rframe[1][2])
            # tmkr = prtlmkIO.Receive(rframe[1][2])
            # if len(tmkr) == 6:
            #     if tmkr[3]['DT'] in ldata['oad_omd']:
            #         ldata['real'] = '上报成功'
            #     else:
            #         ldata['real'] = '上报失败'
            # elif len(tmkr) == 12:
            #     if (tmkr[3]['DT'] in ldata['oad_omd']) or (tmkr[9]['DT'] in ldata['oad_omd']):
            #         ldata['real'] = '上报成功'
            #     else:
            #         ldata['real'] = '上报失败'
    else:
        pass
    if expectorreal(ldata['expect'], ldata['real']):
        ldata['result'] = u'合格'
    else:
        ldata['result'] = u'不合格'
    return 1


EMUN_USBEXM = ['usb_exm1_0', 'usb_exm1_1', 'usb_exm2_0', 'usb_exm2_1', 'usb_exm3_0', 'usb_exm3_1', 'usb_exm4_0',
       'usb_exm4_1', 'usb_exm5_0', 'usb_exm5_1']


# UserName:sysadm PassWd:Zgdky@guest123 Port:8888 ->{'UserName':'sysadm','PassWd':'Zgdky@guest123', 'Port':'8888'}
def sshuserdict(userparam):
    dusr = {'UserName': 'sysadm', 'PassWd': 'Zgdky@guest123', 'Port':'8888'}
    if userparam.find('UserName:') == -1 or  userparam.find('PassWd:') == -1 or userparam.find('Port:') == -1:
        return dusr
    ll = userparam.split(' ')
    for item in ll:
        if item.find(':') >= 0:
            litem = item.split(':')
            if litem[0] == 'UserName':
                dusr['UserName'] = litem[1]
            if litem[0] == 'PassWd':
                dusr['PassWd'] = litem[1]
            if litem[0] == 'Port':
                dusr['Port'] = litem[1]
    return dusr


# ssh命令
def MK_SSH(ldata, ssh):
    sshRx = []
    command = ldata['param'] + ' \n'
    if 'exit' in ldata['param']:
        print('MK_SSH ssh.getchanstat() exit', ssh.getchanstat())
        if ssh.getchanstat() != 0:
            ssh.chan_send('exit \n')
            ssh.exitchan()
            ldata['real'] = 'exit OK'
            print('real_11', ldata['real'])
            return True
        else:
            ldata['real'] = 'SSH未连接'
            print('real_12', ldata['real'])
            return False
    elif 'UserName' in ldata['param']:
        print('MK_SSH ssh.getchanstat() UserName', ssh.getchanstat())
        duser = sshuserdict(ldata['param'])
        if ssh.getchanstat() == 0:
            ssh.login(SYSCONFIG['SSH_SERVERIP'], SYSCONFIG['SSH_SERVERPORT'], duser["UserName"], duser["PassWd"])
            if ssh.getchanstat() == 1:
                ldata['real'] = 'login OK'
            else:
                ldata['real'] = 'login NO'
            if expectorreal(ldata['expect'], ldata['real']):
                ldata['result'] = u'合格'
            else:
                ldata['result'] = u'不合格'
            print('real_9', ldata['real'])
            return True
        else:
            ldata['real'] = 'SSH已连接'
            print('real_10', ldata['real'])
            return False
    elif 'reboot' in ldata['param']:
        if ssh.getchanstat() != 0:
            ssh.chan_send(command)
            brr = ssh.chan_receivebychar('password for sysadm: ')
            logging.info("输入密码:")
            logging.info(brr[1])
            if brr[0]:
                ssh.chan_send('Zgdky@guest123\n')
                logging.info("输入密码重启系统!")
                ssh.exitchan()
                # ldata['real'] = '成功'
                ldata['real'] = 'reboot OK'
            else:
                logging.info("重启系统成功（未输入密码）！")
                ssh.exitchan()
                ldata['real'] = 'reboot OK'
            print('real_8', ldata['real'])
            return True
        else:
            ldata['real'] = 'SSH未连接'
            return False
    elif 'sudo passwd sysadm' in ldata['param']:
        print('MK_SSH ssh.getchanstat() exit', ssh.getchanstat())
        snewpwd = ldata['save']+'\n'
        if len(snewpwd) < 12:
            snewpwd = 'Zgdky@guest123\n'
        if ssh.getchanstat() != 0:
            ssh.chan_send('sudo passwd sysadm\n')
            brr = ssh.chan_receivebychar('Enter new password: ')
            logging.info("修改密码:")
            logging.info(brr[1])
            if brr[0]:
                ssh.chan_send(snewpwd)
                bbr1 = ssh.chan_receivebychar('Re-type new password: ')
                logging.info("修改密码1:")
                logging.info(bbr1[1])
                if bbr1[0]:
                    ssh.chan_send(snewpwd)
                    ldata['real'] = 'new passwd OK'
            print('real_7', ldata['real'])
            return True
        else:
            ldata['real'] = 'SSH未连接'
            return False
    if ssh.getchanstat() == 1:
        ssh.chan_send(command)
        # fdelay = float(ldata['delay'])
        sshRx += ssh.chan_receive(float(ldata['delay']))
        logging.info("chan通道接收:")
        if len(sshRx[1]) > 4096:
            logging.info(sshRx[1][:4096] + '[chan通道接收太长删减]')
            ldata['real'] = sshRx[1][:4096]
            print('ssh.getchanstat()', ssh.getchanstat())
            ssh.chan_send(chr(int(3)))
            # if username.find('root') >= 0:
            #     if self.chan_receivebychar('~# ')[0]:
            #         self.flag_chanstatu = 1
            # print('ssh.chan_receive()', ssh.chan_receive()[1])
            time.sleep(10.0)
            # ssh.chan_send(chr(int(3)))
            logging.info('chan通道接收1:' + ssh.chan_receive()[1])
            # print('ssh.chan_receive()', ssh.chan_receive()[1])
        else:
            logging.info(sshRx[1])
            ldata['real'] = sshRx[1]
        if expectorreal(ldata['expect'], ldata['real']):
            ldata['result'] = u'合格'
            print('real_0',ldata['real'])
            return True
        else:
            ldata['result'] = u'不合格'
            print('real_1', ldata['real'])
            return True
    else:
        print('SSH_SERVERIP no line')
        return False
    icount = 0
    if ldata['param'].find('ls /tmp/dev') >= 0:
        for i in EMUN_USBEXM:
            if i in sshRx[1]:
                icount += 1
                # print('i=', i)
        if icount >= 2:
            ldata['result'] = '合格'
            print('real_3', ldata['real'])
            return True
        else:
            ldata['result'] = '不合格'
            print('real_4', ldata['real'])
            return False
    elif ldata['param'].find('ifconfig') >= 0:
        if sshRx[1].find('ppp0') >= 0:
            ldata['result'] = '合格'
            print('real_5', ldata['real'])
            return True
        else:
            ldata['result'] = '不合格'
            print('real_6', ldata['real'])
            return False
    return True


# 数据流传输
def MK_datastream(ldata):
    itime = 0.0
    istart = time.time()
    # rframe = ''
    idelay = float(ldata['delay'])
    tr = ldata['param']
    # print('oad_omd', type(ldata['oad_omd']))
    while itime < idelay:
        time.sleep(0.1)
        rframe = MK_recvdata(-1, -1, ldata['oad_omd'], prtlmkIO_LY.Protocol_DATA_TYPE)
        # if rframe[0]:
        #     print('MK_datastreamr frame', rframe, ldata['oad_omd'])
        #     print('oad_omd in ', ldata['oad_omd'] in rframe[1][2])
        if rframe[0] and ldata['oad_omd'] in rframe[1][2]:
            # print('数据流接收 Rx:', rframe[1][2])
            logging.info("数据流接收 Rx:" + rframe[1][2])
            LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], tr])
            logging.info("数据流发送 Tx:" + tr)
            # print('数据流发送 Tx', rframe[1][0], rframe[1][1], tr)
            break
        itime = time.time() - istart
        print('itime', itime, idelay)
    return 1

# 替换帧中PIID
def updatetxPIID(srx, stx):
    frm = {}
    ttt1 = prtl698.GetFrame(srx)
    tPIID = ttt1[1]['APDU'][10:12]
    ttt2 = prtl698.GetFrame(stx)
    sapdu = ttt2[1]['APDU'][:10] + tPIID + ttt2[1]['APDU'][12:]
    frm['CTRL'] = ttt2[1]['CTRL']
    frm['TSA_TYPE'] = ttt2[1]['TSA_TYPE']
    frm['TSA_VS'] = ttt2[1]['TSA_VS']
    frm['TSA_AD'] = ttt2[1]['TSA_AD']
    frm['CA'] = ttt2[1]['CA']
    frm['SEG_WORD'] = ttt2[1]['SEG_WORD']
    frm['APDU'] = sapdu
    return prtl698.MakeFrame(frm)

# oop 07 传输 不响应
def MK_485_oop_no(ldata):
    itime = 0.0
    istart = time.time()
    rrtn = ''
    idelay = float(ldata['delay'])
    tr = ldata['param']
    print('MK_485_oop_no', ldata)
    while itime < idelay:
        time.sleep(0.1)
        rframe = MK_recvdata(-1, -1, ldata['oad_omd'], prtlmkIO_LY.Protocol_DATA_TYPE)
        if rframe[0] and ldata['oad_omd'] in rframe[1][2]:
            logging.info("数据流接收 Rx:" + rframe[1][2])
            rrtn = rframe[1][2]
            # break
        itime = time.time() - istart
        # print('MK_485_oop_no itime', itime, idelay, ldata['nu'])
    ldata['real'] = rrtn
    sdd = prtl698.reverse(tr.zfill(12))
    print('MK_485_oop_no sdd', sdd)
    if ldata['oad_omd'] in rrtn and sdd in rrtn:
        ldata['result'] = 'OK'
    else:
        ldata['result'] = 'NO'
    return 1

# oop 07 传输响应
def MK_485_oop(ldata):
    itime = 0.0
    istart = time.time()
    # rframe = ''
    idelay = float(ldata['delay'])
    tr = ldata['param']
    # print('oad_omd', type(ldata['oad_omd']))
    while itime < idelay:
        time.sleep(0.1)
        rframe = MK_recvdata(-1, -1, ldata['oad_omd'], prtlmkIO_LY.Protocol_DATA_TYPE)
        # if rframe[0]:
        #     print('MK_datastreamr frame', rframe, ldata['oad_omd'])
        #     print('oad_omd in ', ldata['oad_omd'] in rframe[1][2])
        if rframe[0] and ldata['oad_omd'] in rframe[1][2]:
            # print('数据流接收 Rx:', rframe[1][2])
            logging.info("数据流接收 Rx:" + rframe[1][2])
            if dl645.deal645Frame(rframe[1][2])[0]:
                LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], tr])
                logging.info("数据流发送07 Tx:" + tr)
            else:
                udtr = updatetxPIID(rframe[1][2], tr)
                LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], udtr])
                logging.info("数据流发送oop Tx:" + udtr)
            # print('数据流发送 Tx', rframe[1][0], rframe[1][1], tr)
            break
        itime = time.time() - istart
        print('MK_485_oop itime', itime, idelay, ldata['nu'])
    return 1


# 1375.1传输
def MK_CTRL(ldata):
    itime = 0.0
    istart = time.time()
    # rframe = ''
    idelay = float(ldata['delay'])
    # tr = ldata['op']
    # print('oad_omd', type(ldata['oad_omd']))
    ClearMKRXBuff(0)
    while itime < idelay:
        time.sleep(0.1)
        rframe = MK_recvdata(-1, -1, -1, prtlmkIO_LY.Protocol_13751_TYPE)
        # if rframe[0]:
        #     print('MK_datastreamr frame', rframe, ldata['oad_omd'])
        #     print('oad_omd in ', ldata['oad_omd'] in rframe[1][2])
        if rframe[0]:
            # print('数据流接收 Rx:', rframe[1][2])
            logging.info("数据流接收 Rx:" + rframe[1][2])
            udtr = CTRL1375.MK_CTRL_Response(rframe[1][2], ldata['param'])
            if len(udtr) >= 2 and len(udtr[0]) >= 14:
                logging.info("模块接收数据存储值:" + udtr[1])
                if len(udtr[1]) > 0 and '0,0' in udtr[1]:
                    ldata['real'] = udtr[1]
                LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], udtr[0]])
                logging.info("数据流发送 Tx:" + udtr[0])
            else:
                logging.info("发送数据流编码错误 Tx:" + udtr[0] + udtr[1])
            # print('数据流发送 Tx', rframe[1][0], rframe[1][1], tr)
            # break
        itime = time.time() - istart
        print('MK_CTRL itime', itime, idelay, ldata['nu'])
    return 1


# plc 1376.2 查询数据响应
def MK_PLC_getResponse(ldata):
    itime = 0.0
    istart = time.time()
    # rframe = ''
    idelay = float(ldata['delay'])
    # tr = ldata['op']
    # print('oad_omd', type(ldata['oad_omd']))
    ClearMKRXBuff(0)
    while itime < idelay:
        time.sleep(0.1)
        rframe = MK_recvdata(-1, -1, -1, prtlmkIO_LY.Protocol_13762_TYPE)
        if rframe[0]:
            # print('数据流接收 Rx:', rframe[1][2])
            logging.info("数据查询接收13762Rx:" + rframe[1][2])
            logging.info("数据查询接收13762解析:" + str(prtl3762.Analyse113762frame(rframe[1][2])))
            # udtr = CTRL1375.MK_CTRL_Response(rframe[1][2], ldata['op'], ldata['param'])
            frmResponse = prtl3762.mk_13762_get_Response(rframe[1][2], '', '', '', ldata['op'], ldata['oad_omd'], ldata['param'])
            if len(frmResponse) >= 30:
                LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], frmResponse])
                logging.info("数据查询响应发送13762Tx:" + frmResponse)
                logging.info("数据查询响应发送13762Tx解析:" + str(prtl3762.Analyse113762frame(frmResponse)))
                ldata['real'] = '成功'
                break
            else:
                logging.info("数据查询响应编码错误:" + frmResponse)
            # print('数据流发送 Tx', rframe[1][0], rframe[1][1], tr)
            # break
        itime = time.time() - istart
        print('MK_PLC_getResponse itime', itime, idelay, ldata['nu'])
    if expectorreal(ldata['expect'], ldata['real']):
        ldata['result'] = u'合格'
    else:
        ldata['result'] = u'不合格'
    return 1

# plc 1376.2 确认否认响应
def MK_PLC_setResponse(ldata):
    itime = 0.0
    istart = time.time()
    # rframe = ''
    idelay = float(ldata['delay'])
    # tr = ldata['op']
    # print('oad_omd', type(ldata['oad_omd']))
    ClearMKRXBuff(0)
    while itime < idelay:
        time.sleep(0.1)
        rframe = MK_recvdata(-1, -1, -1, prtlmkIO_LY.Protocol_13762_TYPE)
        if rframe[0]:
            # print('数据流接收 Rx:', rframe[1][2])
            logging.info("设置接收13762Rx:" + rframe[1][2])
            logging.info("设置接收13762Rx解析:" + str(prtl3762.Analyse113762frame(rframe[1][2])))
            # udtr = CTRL1375.MK_CTRL_Response(rframe[1][2], ldata['op'], ldata['param'])
            frmResponse = prtl3762.mk_13762_setResponse(rframe[1][2], '', '', '', ldata['op'], ldata['oad_omd'],
                                                         ldata['param'])
            if len(frmResponse) >= 30:
                # logging.info("模块接收数据存储值:" + rframe[1][2])
                # if len(udtr[1]) > 0 and '0,0' in udtr[1]:
                #     ldata['real'] = udtr[1]
                LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], frmResponse])
                logging.info("设置确认发送13762Tx:" + frmResponse)
                logging.info("设置确认发送13762Tx解析:" + str(prtl3762.Analyse113762frame(frmResponse)))
                ldata['real'] = '成功'
                break
            else:
                logging.info("设置确认发送13762错误:" + frmResponse)
            # print('数据流发送 Tx', rframe[1][0], rframe[1][1], tr)
            # break
        itime = time.time() - istart
        print('MK_PLC_setResponse itime', itime, idelay, ldata['nu'])
    if expectorreal(ldata['expect'], ldata['real']):
        ldata['result'] = u'合格'
    else:
        ldata['result'] = u'不合格'
    return 1


# plc 1376.2 路由数据转发响应
def MK_PLC_routedataResponse(ldata):
    itime = 0.0
    istart = time.time()
    # rframe = ''
    idelay = float(ldata['delay'])
    # tr = ldata['op']
    # print('oad_omd', type(ldata['oad_omd']))
    ClearMKRXBuff(0)
    while itime < idelay:
        time.sleep(0.1)
        rframe = MK_recvdata(-1, -1, -1, prtlmkIO_LY.Protocol_13762_TYPE)
        if rframe[0]:
            # print('数据流接收 Rx:', rframe[1][2])
            logging.info("路由数据转发接收13762Rx:" + rframe[1][2])
            logging.info("路由数据转发接收13762Rx解析:" + str(prtl3762.Analyse113762frame(rframe[1][2])))
            # udtr = CTRL1375.MK_CTRL_Response(rframe[1][2], ldata['op'], ldata['param'])
            frmResponse = prtl3762.mk_13762_routedataResponse(rframe[1][2], '', '', '', ldata['op'], ldata['oad_omd'],
                                                        ldata['param'])
            if len(frmResponse) >= 30:
                LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], frmResponse])
                logging.info("路由数据转发发送13762Tx:" + frmResponse)
                logging.info("路由数据转发发送13762Tx解析:" + str(prtl3762.Analyse113762frame(frmResponse)))
                ldata['real'] = '成功'
                break
            else:
                logging.info("路由数据转发发送13762错误:" + frmResponse)
            # print('数据流发送 Tx', rframe[1][0], rframe[1][1], tr)
            # break
        itime = time.time() - istart
        print('MK_PLC_routedataResponse itime', itime, idelay, ldata['nu'])
    if expectorreal(ldata['expect'], ldata['real']):
        ldata['result'] = u'合格'
    else:
        ldata['result'] = u'不合格'
    return 1

# plc 1376.2 主动上报
def MK_PLC_reportini(ldata, iniRtu, ipiid):
    frmResponse = prtl3762.mk_13762_report('', '', '', ldata['op'], ldata['oad_omd'],ldata['param'])
    LIST_CW1_TXDATA.append([ipiid, prtlmkIO_LY.COM_DATA1, frmResponse])
    logging.info("主动上报13762Tx:" + frmResponse)
    logging.info("主动上报13762Tx解析:" + str(prtl3762.Analyse113762frame(frmResponse)))
    itime = 0.0
    istart = time.time()
    # rframe = ''
    idelay = float(ldata['delay'])
    # tr = ldata['op']
    # print('oad_omd', type(ldata['oad_omd']))
    ClearMKRXBuff(0)
    while itime < idelay:
        time.sleep(0.1)
        rframe = MK_recvdata(-1, -1, -1, prtlmkIO_LY.Protocol_13762_TYPE)
        if rframe[0]:
            # print('数据流接收 Rx:', rframe[1][2])
            logging.info("上报接收13762确认Rx:" + rframe[1][2])
            # udtr = CTRL1375.MK_CTRL_Response(rframe[1][2], ldata['op'], ldata['param'])
            ll = prtl3762.Analyse113762frame(rframe[1][2])
            if '确认/否认:确认' in str(ll):
                logging.info("上报接收13762确认Rx:" + rframe[1][2])
                logging.info("上报接收13762确认Rx解析:" + str(ll))
                ldata['real'] = '成功'
                break
            else:
                logging.info("上报接收13762Rx:" + rframe[1][2])
                logging.info("上报接收13762Rx解析:" + str(prtl3762.Analyse113762frame(rframe[1][2])))
            # print('数据流发送 Tx', rframe[1][0], rframe[1][1], tr)
            # break
        itime = time.time() - istart
        print('MK_PLC_routedataResponse itime', itime, idelay, ldata['nu'])
    if expectorreal(ldata['expect'], ldata['real']):
        ldata['result'] = u'合格'
    else:
        ldata['result'] = u'不合格'
    return 1

# plc 1376.2 并发抄表增加 return True ['6824020000000068', item, '', istime, itime]
def MK_PLC_addF1(ldata):
    idelay = float(ldata['delay'])
    brn = False
    litem = []
    if idelay > 1.0:
        brn = True
    if len(ldata['param']) >= 32:
        sparam = ldata['param']
        litem.append(sparam[6:22])
        ldata['result'] = u'不合格'
        litem.append(ldata)
        litem.append('')
        litem.append(0.0)
        litem.append(0.0)
    return brn, litem

# plc 1376.2 并发抄表收发对应响应 ldata [['6824020000000068', item],...]
def MK_PLC_F1Response(ldata):
    itime = 0.0
    istart = time.time()
    ipos = len(ldata) - 1
    # rframe = ''
    # print('MK_PLC_F1Response ldata', ipos, ldata)
    # print('MK_PLC_F1Response ldata[ipos][1]', ldata[ipos][1])
    # print('MK_PLC_F1Response ldata delay', ldata[ipos][1]['delay'])
    idelay = float(ldata[ipos][1]['delay'])
    ClearMKRXBuff(0)
    # print('idelay', idelay, itime < idelay)
    while itime < idelay:
        time.sleep(0.1)
        rframe = MK_recvdata(-1, -1, -1, prtlmkIO_LY.Protocol_13762_TYPE)
        if rframe[0]:
            # print('数据流接收 Rx:', rframe[1][2])
            logging.info("并发抄表接收13762Rx:" + rframe[1][2])
            logging.info("并发抄表接收13762解析:" + str(prtl3762.Analyse113762frame(rframe[1][2])))
            for i in range(0, len(ldata), 1):
                # print('ldatarframe', ldata[i][0], rframe[1][2])
                # print('ldata[i][0] in rframe[1][2]', ldata[i][0] in rframe[1][2])
                if ldata[i][0] in rframe[1][2]:
                    # print('ldata[i][0] in rframe[1][2]', ldata[i][0] in rframe[1][2])
                    frmResponse = prtl3762.mk_13762_routedataResponse(rframe[1][2], '', '', '', ldata[i][1]['op'],
                                                                      ldata[i][1]['oad_omd'],
                                                                      ldata[i][1]['param'])
                    print('frmResponse', frmResponse)
                    if len(frmResponse) >= 30:
                        LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], frmResponse])
                        logging.info("并发抄表响应发送13762Tx:" + frmResponse)
                        logging.info("并发抄表响应发送13762Tx解析:" + str(prtl3762.Analyse113762frame(frmResponse)))
                        # print('ldata[i][1]', ldata[i][1], type(ldata[i][1]['result']))
                        # print('result', ldata[i][1]['result'])
                        ldata[i][1]['real'] = '成功'
                        if expectorreal(ldata[i][1]['expect'], ldata[i][1]['real']):
                            # print('ldata[i][1]', ldata[i][1], type(ldata[i][1]['result']))
                            # print('result', ldata[i][1]['result'])
                            ldata[i][1]['result'] = u'合格'
                        # else:
                        #     ldata[i][1]['result'] = u'不合格'
                    else:
                        logging.info("并发抄表编码错误:" + frmResponse)
        itime = time.time() - istart
        # print('MK_PLC_F1Response itime idelay', itime, idelay)
    return 1


# plc 1376.2 并发抄表随机响应 ldata [['6824020000000068', item, '', istar, ],...]
def MK_PLC_F1RNResponse(ldata):
    itime = 0.0
    istart = time.time()
    ipos = len(ldata) - 1
    print('MK_PLC_F1RNResponse ldata', ldata)
    idelay = float(ldata[ipos][1]['delay'])
    ClearMKRXBuff(0)
    icount = 0
    rfr0 = 0
    rfr1 = 1
    while itime < idelay:
        time.sleep(0.1)
        rframe = MK_recvdata(-1, -1, -1, prtlmkIO_LY.Protocol_13762_TYPE)
        if rframe[0]:
            rfr0 = rframe[1][0]
            rfr1 = rframe[1][1]
            logging.info("并发抄表接收13762Rx:" + rframe[1][2])
            logging.info("并发抄表接收13762解析:" + str(prtl3762.Analyse113762frame(rframe[1][2])))
            for i in range(0, len(ldata), 1):
                if ldata[i][0] in rframe[1][2]:
                    frmResponse = prtl3762.mk_13762_routedataResponse(rframe[1][2], '', '', '', ldata[i][1]['op'],
                                                                      ldata[i][1]['oad_omd'],
                                                                      ldata[i][1]['param'])
                    # print('frmResponse', frmResponse)
                    if len(frmResponse) >= 30 and len(ldata[i][2]) == 0:
                        icount += 1
                        ldata[i][2] = frmResponse
                        ldata[i][3] = time.time()
                        ldata[i][4] = 0.0
                        logging.info("生成并发抄表响应帧13762:" + frmResponse)
                        logging.info("生成并发抄表响应帧13762解析:" + str(prtl3762.Analyse113762frame(frmResponse)))
                    else:
                        logging.info("并发抄表编码已完成或发送完成:" + ldata[i][2])
                if len(ldata[i][2]) >= 30:
                    ldata[i][4] = time.time() - ldata[i][3]
                btx = False
                if icount >= 5:
                    for j in range(0, len(ldata), 1):
                        if len(ldata[j][2]) >= 30:
                            LIST_CW1_TXDATA.append([rfr0, rfr1, ldata[j][2]])
                            logging.info("并发抄表响应发送13762Tx1:" + ldata[j][2])
                            logging.info("并发抄表响应发送13762Tx1解析:" + str(prtl3762.Analyse113762frame(ldata[j][2])))
                            ldata[j][2] = ''
                            ldata[j][1]['real'] = '成功'
                            if expectorreal(ldata[j][1]['expect'], ldata[j][1]['real']):
                                ldata[j][1]['result'] = u'合格'
                            time.sleep(0.1)
                            btx = True
                            break
                if btx:
                    break
        # if icount >= 5:
        for k in range(0, len(ldata), 1):
            if len(ldata[k][2]) >= 30 and ldata[k][3] > 0.1:
                ldata[k][4] = time.time() - ldata[k][3]
            # print('ldata[k]',ldata[k][3], ldata[k][4])
            if len(ldata[k][2]) >= 30 and ldata[k][4] > 20.0:
                LIST_CW1_TXDATA.append([rfr0, rfr1, ldata[k][2]])
                logging.info("并发抄表响应发送13762Tx2:" + ldata[k][2])
                logging.info("并发抄表响应发送13762Tx2解析:" + str(prtl3762.Analyse113762frame(ldata[k][2])))
                ldata[k][2] = ''
                ldata[k][1]['real'] = '成功'
                ldata[k][3] = time.time()
                ldata[k][4] = 0.0
                if expectorreal(ldata[k][1]['expect'], ldata[k][1]['real']):
                    ldata[k][1]['result'] = u'合格'
                time.sleep(0.1)
                break
        itime = time.time() - istart
        # print('MK_PLC_F1RNResponse itime idelay', itime, idelay)
    return 1

# GPRS 1376.3
def MK_GPRS(ldata, iniRtu, ipiid):
    ClearMKRXBuff(0)
    itime = 0.0
    istart = time.time()
    rframe = ''
    idelay = float(ldata['delay'])
    tt = []
    while itime < idelay:
        time.sleep(0.2)
        rframe = MK_recvdata(-1, prtlmkIO_LY.COM_DATA1, '', prtlmkIO_LY.Protocol_13763_TYPE)
        if rframe[0]:
            # print('rframe', rframe)
            if len(rframe[1]) > 2:
                tt += prtl3763.isATReqest(rframe[1][2])
            # print('tt', tt)
                if tt[0]:
                    break
                else:
                    del tt[0:]
        itime = time.time() - istart
    if rframe[0] == False:
        # bcnt = False
        logging.info('MK_GPRS Rx:Null')
        ldata['real'] = "AT响应失败"
    else:
        # global DATETIME_T1
        # global DATETIME_T2
        if ldata['save'] == 'T1':
            DATETIME_T[0] = datetime.datetime.now()
            ldata['real'] = str(DATETIME_T[0])
        elif ldata['save'] == 'T2':
            DATETIME_T[1] = datetime.datetime.now()
            ldata['real'] = str(DATETIME_T[1])
        logging.info(rframe[1][2])
        # print(rframe[1]
        print('tt', tt)
        if tt[0]:
            LIST_CW1_TXDATA.append([rframe[1][0], rframe[1][1], tt[1]])
            logging.info("AT响应 Tx:" + tt[1])
            # ldata['real'] = "AT响应成功"
        else:
            pass
            # ldata['real'] = "AT响应失败"
    return 1

# 处理
def compareMK(ldata, prtltype):
    if prtltype == '13763':
        if ldata['save'] == 'T2-T1':
            dd = DATETIME_T[1] - DATETIME_T[0]
            ldata['real'] = str(dd.seconds)
            if dd.seconds <= 6:
                ldata['result'] = 'OK'
            else:
                ldata['result'] = 'NO'
    elif prtltype == '13762':
        pass
    return 1

# 客户机发起请求，并解析响应的数据
def Client_Request(ldata, iniRtu, ipiid):
    # rl = []
    frm = {}
    frm['CTRL'] = '43'
    frm['TSA_TYPE'] = prtl698.getbitbyCA(ldata['addrtype'])
    frm['TSA_VS'] = prtl698.getintbyvaddrname(ldata['vadd'])
    frm['TSA_AD'] = iniRtu['ADDR']
    frm['CA'] = ldata['caddr']
    frm['SEG_WORD'] = ''
    s = ldata['secure']
    r = ldata['op']
    i = ipiid % 64
    o = [ldata['oad_omd']]
    d = [ldata['param']]
    print('s,r,i,o,d:', s, r, i, o, d)
    if ldata['oad_omd'] in ['40000200'] and '@getnowtime' in ldata['param']:
        now = datetime.datetime.now()
        stime = now.strftime('%Y%m%d%H%M%S')
        d = [stime]
    if ldata['oad_omd'] in ['80008100', '80008200']:
        frm['APDU'] = prtl698.make_DATA_APDU_Request(s, r, i, o, d, '5分')
    else:
        frm['APDU'] = prtl698.make_DATA_APDU_Request(s, r, i, o, d)
    frame = prtl698.MakeFrame(frm)
    frame = frame.upper()
    print('Client_Request Tx:' + frame)
    logging.info('Tx:' + frame)
    while len(public_sRxBuff) > 0:
        del public_sRxBuff[0:]
    senddata(frame)
    itime = 0.0
    istart = time.time()
    rframe = ''
    idelay = float(ldata['delay'])
    while itime < idelay:
        time.sleep(0.2)
        rframe = recvdata(ldata['oad_omd'][:8])
        if len(rframe) > 0:
            break
        itime = time.time() - istart
    if rframe == '':
        # bcnt = False
        logging.info('Client_Request read Rx:Null')
    else:
        logging.info('Client_Request Rx:' + rframe)
        lrs = prtl698.Receive(rframe)
        # print('Client_Request lrs[3]', lrs[3])
        # print('Client_Request VALUE bool', 'VALUE' in lrs[3])
        if len(lrs) >= 6 and 'VALUE' in lrs[3]:
            sss = ''
            for il in range(0, len(lrs[3]['VALUE']),1):
                sss += lrs[3]['VALUE'][il]
            logging.info('Client_Request sss:' + sss)
            if ldata['oad_omd'] in ['31400200', '31200200']:
                ldata['real'] = prtl698.analy_data_OAD(ldata['oad_omd'], lrs[3]['VALUE'])
            else:
                ldata['real'] = sss
            logging.info('Client_Request real:' + ldata['real'])
            print('Client_Request real', ldata['real'])
        if ldata['oad_omd'] in ['31400200']:
            ldata['save'] = rframe
    if expectorreal(ldata['expect'], ldata['real']):
        ldata['result'] = u'合格'
    else:
        ldata['result'] = u'不合格'
    # if ldata['expect'].find(ldata['real']) >= 0:
    #    ldata['result'] = u'合格'
    # else:
    #    ldata['result'] = u'不合格'
    return 1


# 等待上报，并解析响应的数据
def Client_ReportResponse(ldata, iniRtu, ipiid):
    # rl = []
    # frm = {}
    # frm['CTRL'] = '43'
    # frm['TSA_TYPE'] = prtl698.getbitbyCA(ldata['addrtype'])
    # frm['TSA_VS'] = prtl698.getintbyvaddrname(ldata['vadd'])
    # frm['TSA_AD'] = iniRtu['ADDR']
    # frm['CA'] = ldata['caddr']
    # frm['SEG_WORD'] = ''
    # s = ldata['secure']
    # r = ldata['op']
    # i = ipiid % 64
    # o = [ldata['oad_omd']]
    # d = [ldata['param']]
    # print('s,r,i,o,d:', s, r, i, o, d)
    # if ldata['oad_omd'] in ['40000200'] and '@getnowtime' in ldata['param']:
    #     now = datetime.datetime.now()
    #     stime = now.strftime('%Y%m%d%H%M%S')
    #     d = [stime]
    # if ldata['oad_omd'] in ['80008100', '80008200']:
    #     frm['APDU'] = prtl698.make_DATA_APDU_Request(s, r, i, o, d, '5分')
    # else:
    #     frm['APDU'] = prtl698.make_DATA_APDU_Request(s, r, i, o, d)
    # frame = prtl698.MakeFrame(frm)
    # frame = frame.upper()
    # print('Client_Request Tx:' + frame)
    # logging.info('Tx:' + frame)
    while len(public_sRxBuff) > 0:
        del public_sRxBuff[0:]
    # senddata(frame)
    itime = 0.0
    istart = time.time()
    rframe = ''
    idelay = float(ldata['delay'])
    while itime < idelay:
        time.sleep(0.2)
        rframe = recvdata(ldata['oad_omd'][:8])
        if len(rframe) > 0:
            break
        itime = time.time() - istart
    if rframe == '':
        # bcnt = False
        logging.info('Client_ReportResponse read Rx:Null')
    else:
        logging.info('Client_ReportResponse Rx:' + rframe)
        lrs = prtl698.Receive(rframe)
        # print('Client_Request lrs[3]', lrs[3])
        # print('Client_Request VALUE bool', 'VALUE' in lrs[3])
        if len(lrs) >= 6 and 'VALUE' in lrs[3]:
            sss = ''
            for il in range(0, len(lrs[3]['VALUE']),1):
                sss += lrs[3]['VALUE'][il]
            logging.info('Client_ReportResponse sss:' + sss)
            if ldata['oad_omd'] in ['31400200', '31200200']:
                ldata['real'] = prtl698.analy_data_OAD(ldata['oad_omd'], lrs[3]['VALUE'])
            else:
                ldata['real'] = sss
            logging.info('Client_ReportResponse real:' + ldata['real'])
            print('Client_ReportResponse real', ldata['real'])
        if ldata['oad_omd'] in ['31400200']:
            ldata['save'] = rframe
    if expectorreal(ldata['expect'], ldata['real']):
        ldata['result'] = u'合格'
    else:
        ldata['result'] = u'不合格'
    return 1


# 期望值和实际值判断处理
def expectorreal(expect, real):
    if '[' in expect and ']' in expect and expect.find('[') == 0:
        try:
            ll = prtl698.strtolist(expect)
            if ll[0] == 'include':
                bfd = True
                for i in range(1, len(ll), 1):
                    if real.find(ll[i]) == -1:
                        bfd = False
                        break
                return bfd
            elif ll[0] == 'exclude':
                bfind = True
                for i in range(1, len(ll), 1):
                    if real.find(ll[i]) >= 0:
                        bfind = False
                        break
                return bfind
            elif (len(expect) > 0) and (real.find(expect) == -1):
                return False
        except:
            logging('expectorreal try expect:'+ expect + ',real:' + real)
            return False
    else:
        if (len(expect) > 0) and (real.find(expect) == -1):
            return False
    return True

# 统计结果
def totalresult(temlis):
    return True

# 开启服务端口
def openserver(iport=50154):
    public_thread_temp = True
    try:
        HOST, PORT = SYSCONFIG['SERVERIP'], iport
        server1 = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestTempHandler)
        server_thread1 = threading.Thread(target=server1.serve_forever)
        server_thread1.daemon = True
        server_thread1.start()
        return server_thread1
    except:
        return None

def closeserver(ithread):
    public_thread_temp = False
    if ithread != None:
        while ithread.is_alive() == False:
            time.sleep(0.1)
            print('closeserver', ithread.is_alive())
        ithread = None
    return 1


def main():
    initModel()
    rtuinilist = getRtuini()
    logging.info(u'开始启动服务器!')
    try:
        HOST, PORT = SYSCONFIG['SERVERIP'], SYSCONFIG['SERVERPORT']
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        logging.info(u'启动主服务器成功!')
    except:
        logging.info(u'启动服务器异常!' + str(PORT))
        os._exit(0)
    # logging.info(u'连接虚拟表!')
    # thrrun = threading.Thread(target = run, args=())
    # thrrun.daemon = True
    # thrrun.start()
    # if convmeter():
    #     logging.info(u'连接虚拟表成功！')
    # else:
    #     logging.info(u'连接虚拟表失败！')
    # time.sleep(60.0)
    logging.info(u'开始检查终端在线!')
    # 检查终端是否在线
    if checkRtuline():
        logging.info(u'终端在线!')
    else:
        logging.warning(u'终端不在线!')
        os._exit(0)
    # 检查槽位串口
    try:
        # 槽位线程
        cw1port = mkcom.mkserial(rtuinilist['CW1_PORT'], baudrate=rtuinilist['CW_PORT_BAUDRATE'], timeout=1)
        _thread.start_new_thread(cw1port.receivemsg, (LIST_CW1_RXDATA, ))
        _thread.start_new_thread(cw1port.sendmsg, (LIST_CW1_TXDATA, ))
        # cw2port = mkcom.mkserial(rtuinilist['CW2_PORT'], baudrate=rtuinilist['CW_PORT_BAUDRATE'], timeout=1)
        # _thread.start_new_thread(cw2port.receivemsg, (LIST_CW2_RXDATA, ))
        # _thread.start_new_thread(cw2port.sendmsg, (LIST_CW2_TXDATA, ))
        # cw3port = mkcom.mkserial(rtuinilist['CW3_PORT'], baudrate=rtuinilist['CW_PORT_BAUDRATE'], timeout=1)
        # _thread.start_new_thread(cw3port.receivemsg, (LIST_CW3_RXDATA,))
        # _thread.start_new_thread(cw3port.sendmsg, (LIST_CW3_TXDATA, ))
        # cw4port = mkcom.mkserial(rtuinilist['CW4_PORT'], baudrate=rtuinilist['CW_PORT_BAUDRATE'], timeout=1)
        # _thread.start_new_thread(cw4port.receivemsg, (LIST_CW4_RXDATA, ))
        # _thread.start_new_thread(cw4port.sendmsg, (LIST_CW4_TXDATA, ))
        # cw5port = mkcom.mkserial(rtuinilist['CW5_PORT'], baudrate=rtuinilist['CW_PORT_BAUDRATE'], timeout=1)
        # _thread.start_new_thread(cw5port.receivemsg, (LIST_CW5_RXDATA, ))
        # _thread.start_new_thread(cw5port.sendmsg, (LIST_CW5_TXDATA, ))
        logging.info(u"槽位1通讯串口[" + rtuinilist['CW1_PORT'] +"]已打开!")
    except:
        logging.warning(u"槽位1通讯串口["+ rtuinilist['CW1_PORT'] +"]不能打开!")
        os._exit(0)
    chan_LY = SSH2ccc_ex.SSHinvoke_shell()
    # chan_LY.login(SYSCONFIG['SSH_SERVERIP'], SYSCONFIG['SSH_SERVERPORT'], "sysadm", "Zgdky@guest123")
    mk_lists = []
    ml_list = []
    mrtuidlist = {}
    vmdlist = {}
    dt_listn = []
    dt_mn_list = []
    dt_mn_list_data = []
# 上报数据存储
    r_task_data = []
# 实时数据存储
    r_real_data = []
# 历史数据存储
    r_his_data = []
# 数据项叠加
    litemadd = []
    server_thread_temp = None
    logging.info(u'开始检查配置文件!')
# 检查指定目录下文件是否齐,读当参数设置流程模版存内存字典
    if checkfl(paramfiles):
        path = os.getcwd() + "\config"
        ml_list = readexcel(path + '/' + paramfiles['parameter'], u'目录', 'ml')
        for i in range(0, len(ml_list), 1):
            if ml_list[i]['cut'] == u'裁剪': continue
            if ml_list[i]['cut'] == u'不执行': continue
            lname = ['通用']
            if rtuinilist['TYPE'] == "GWZB":
                lname += ['专变']
            elif rtuinilist['TYPE'] == "GWGB":
                lname += ["公变"]
            if ml_list[i]['rtutype'] in lname:
                tasklist = readexcel(path + '/' + paramfiles['parameter'], ml_list[i]['name'], 'oop_mk')
                tasklist['fname'] = ml_list[i]['alias']
                print('tasklist:',tasklist['fname'], len(tasklist))
                mk_lists.append(tasklist)
                logging.info(u'加载['+ ml_list[i]['name'] +u']完成!')
        logging.info(u'配置文件齐备!')
    else:
        logging.warning(u'配置文件不齐备!')
        os._exit(0)
    logging.info(u'接口互换性测试开始!')
    # print('mk_lists', mk_lists)
    for item in mk_lists:
        # print("item", item)
        logging.info(item['fname']+'开始测试')
        bresult = True
        for i in item:
            if 'fname' == i:
                continue
            temstr = u'步骤:'
            if isinstance(item[i]['nu'], str):
                temstr += item[i]['nu'] + '|'
            elif isinstance(item[i]['nu'], float):
                temstr += str(int(item[i]['nu'])) + '|'
            if isinstance(item[i]['name'], float):
                temstr += str(item[i]['name']) + '|'
            else:
                temstr += item[i]['name'].strip() + '|'
            if isinstance(item[i]['op'], float):
                temstr += str(item[i]['op']) + '|'
            else:
                temstr += item[i]['op'] + '|'
            if isinstance(item[i]['oad_omd'], float):
                temstr += str(int(item[i]['oad_omd'])) + '|'
            else:
                temstr += item[i]['oad_omd'].strip() + '|'
            if isinstance(item[i]['param'], float):
                temstr += str(int(item[i]['param'])) + '|'
            else:
                temstr += item[i]['param'] + '|'
            # print('delay type', type(item[i]['delay']))
            if isinstance(item[i]['delay'], float):
                temstr += str(int(item[i]['delay'])) + '|'
            else:
                temstr += item[i]['delay'] + '|'
            if isinstance(item[i]['expect'], float):
                temstr += str(item[i]['expect']) + '|'
            else:
                temstr += item[i]['expect'] + '|'
            logging.info(temstr)
            if item[i]['cut'] == u'不执行': continue
            if item[i]['cut'] == u'裁剪': continue
            print('item:', item[i])
            print('dOPName', item[i]['op'] in prtl698.dOPName)
            if item[i]['op'] == u"源设置":
                setsource(item[i])
            elif item[i]['op'] == u'设置模块类型':
                if set_MK_CW(item[i]):
                    logging.info('设置模块类型成功')
                    item[i]['real'] = 'OK'
                else:
                    logging.info('设置模块类型失败')
                    item[i]['real'] = 'NO'
                logging.info("模块类型:" + LSIT_MK_CW[0])
            elif item[i]['op'] == u'表设置':
                pass
            elif item[i]['op'] == u'表读取':
                pass
            elif item[i]['op'] == u'等待':
                if item[i]['protype'] == '13762':
                    wait13762(item[i])
                else:
                    wait(item[i])
            elif item[i]['op'] == u'开启服务端口':
                iport = 50154
                if len(item[i]['param']) > 0:
                    try:
                        iport = int(item[i]['param'])
                        server_thread_temp = openserver(iport)
                        if server_thread_temp != None:
                            logging.info("开启服务端口成功:" + str(iport))
                    except:
                        iport = 50154
                        logging.info("开启服务端口输入参数错误:" + item[i]['param'])
            elif item[i]['op'] == u'关闭服务端口':
                closeserver(server_thread_temp)
            elif item[i]['op'] == u'处理':
                compareMK(item[i], item[i]['protype'])
            elif item[i]['op'] == u'源读取':
                # dt_m0_list_data = readsource(dt_listn)
                # logging.info('dt_m0_list_data:')
                # for ii in dt_m0_list_data:
                #     logging.info(ii)
                pass
            elif item[i]['protype'] == 'oop':
                if item[i]['op'] in ['上报若干个记录型对象属性']:
                    Client_ReportResponse(item[i], rtuinilist, i)
                else:
                    Client_Request(item[i], rtuinilist, i)
            elif item[i]['protype'] == 'lygnmz':
                # print('lygnmz', item[i]['oad_omd'], item[i]['oad_omd'] in ['8000'])
                if item[i]['oad_omd'] == '0203':
                    MK_FileUp_Response(item[i], rtuinilist, i)
                elif item[i]['oad_omd'] in ['8000']:
                    # print('lygnmz 8000', item[i]['oad_omd'], item[i]['oad_omd'] in ['8000'])
                    ttp = item[i]
                    _thread.start_new_thread(MK_Syn_GetResponse, (ttp, ))
                elif item[i]['oad_omd'] in ['9000', '9001', '9002', '9003']:
                    # print('lygnmz 9000 9003', item[i]['oad_omd'], item[i]['oad_omd'] in ['9000', '9001', '9002', '9003'])
                    # ttp = item[i]
                    MK_Syn_GetResponseFillGrid(item[i])
                # elif item[i]['oad_omd'] in ['9003']:
                #     print('lygnmz 9003', item[i]['oad_omd'], item[i]['oad_omd'] in ['9000'])
                #     # ttp = item[i]
                #     _thread.start_new_thread(MK_Syn_GetResponseFillGrid, (item[i],))
                elif item[i]['oad_omd'] in ['4002']:
                    # print('lygnmz 4002', item[i]['oad_omd'], item[i]['oad_omd'] in ['4002'])
                    ttp = item[i]
                    # _thread.start_new_thread(MK_MC_GetResponse, (ttp,))
                    MK_MC_GetResponse(ttp)
                elif item[i]['oad_omd'] in ['4101']:
                    # print('lygnmz 8000', item[i]['oad_omd'], item[i]['oad_omd'] in ['8000'])
                    ttp = item[i]
                    _thread.start_new_thread(MK_Syn_SetResponse, (ttp,))
                else:
                    MK_Requse_Response(item[i], rtuinilist, i)
            elif item[i]['protype'] == 'SSH':
                MK_SSH(item[i], chan_LY)
            elif item[i]['protype'] == 'datastream':
                # MK_datastream(item[i], rtuinilist, i)
                ttp = item[i]
                if item[i]['op'] == u'RS485模拟响应':
                    _thread.start_new_thread(MK_485_oop, (ttp, ))
                elif item[i]['op'] == u'RS485模拟不响应':
                    # print('item[i]', item[i])
                    # _thread.start_new_thread(MK_485_oop_no, (item[i],))
                    MK_485_oop_no(item[i])
                else:
                    _thread.start_new_thread(MK_datastream, (ttp, ))
            elif item[i]['protype'] == '13751':
                ttp = item[i]
                # print('13751', ttp)
                _thread.start_new_thread(MK_CTRL, (ttp,))
            elif item[i]['protype'] == '13762':
                # print('13762')
                if item[i]['op'] in [u'查询数据响应', '路由查询响应']:
                    if item[i]['oad_omd'] in ['F16', 'F9']:
                        ttp = item[i]
                        _thread.start_new_thread(MK_PLC_getResponse, (ttp, ))
                    else:
                        MK_PLC_getResponse(item[i])
                elif item[i]['op'] in [u'确认否认']:
                    ttp = item[i]
                    fdelay = float(item[i]['delay'])
                    if fdelay >= 61.0:
                        _thread.start_new_thread(MK_PLC_setResponse, (ttp, ))
                    else:
                        MK_PLC_setResponse(ttp)
                elif item[i]['op'] in [u'路由数据转发响应']:
                    # 线程
                    ttp = item[i]
                    fdelay = float(item[i]['delay'])
                    if fdelay >= 61.0:
                        _thread.start_new_thread(MK_PLC_routedataResponse, (ttp, ))
                    else:
                        MK_PLC_routedataResponse(ttp)
                elif item[i]['op'] in [u'主动上报']:
                    MK_PLC_reportini(item[i], rtuinilist, i)
                elif item[i]['op'] in [u'并发抄表响应']:
                    litem = MK_PLC_addF1(item[i])
                    if len(litem[1]) == 5:
                        litemadd.append(litem[1])
                    # [True, '6824020000000068', item]
                    if litem[0]:
                        _thread.start_new_thread(MK_PLC_F1RNResponse, (litemadd,))
                # MK_PLC(item[i], rtuinilist, i)
            elif item[i]['protype'] == '13763':
                MK_GPRS(item[i], rtuinilist, i)
            if item[i]['result'].find('不合格') >= 0 and len(item[i]['result']) > 0:
                bresult = False
            # 统计结论返回给平台
        # btotal = True
        # btotal = btotal * totalresult(item)
        sresult = ''
        if bresult:
            logging.info(item['fname'] + u'测试合格')
            sresult = '(合格)'
            # 显示结论到平台
        else:
            logging.warning(item['fname'] + u'测试不合格')
            sresult = '(不合格)'
        # 显示结论到平台
        now = datetime.datetime.now()
        path = os.getcwd() + "\\report\\"
        path += item['fname'] + sresult + now.strftime('%Y%m%d%H%M%S') + '.xls'
        print(path)
        saveasexcel(path, item)
    if chan_LY.getchanstat() != 0:
        chan_LY.exitchan()
    logging.info(u'接口互换性测试结束!')
    server.shutdown()
    server.server_close()
    StopSource()
    os._exit(0)


if __name__ == '__main__':
    main()
    # print(sshuserdict('UserName:admin PassWd: Port:5555'))
    # print('time', datetime.datetime.now())
    # rx = '6831004305686701903120004C9510000D05021702001002000020020000011011000000000000000000000000000000FCE116'
    # tx = '683E00C30568670190312000D74D90002585012E0010020001010506000167160600005A8F06000058F206000059D706000059BD00000100049448B66A945A16'
    # print('updatetxPIID', updatetxPIID(rx, tx))
    # initsysconfig()
    # print(getRtuini())
    # print (__file__)
    # print checkfl(paramfiles)
