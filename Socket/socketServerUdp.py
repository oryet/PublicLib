#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import queue
from PublicLib.Socket.ConnManage import ConnManage
from PublicLib.Protocol.prtl13761 import prtl3761
from PublicLib.MySqldb.Frame2Json import *


q = queue.Queue()
server = None
MAX_LIVE_TIME = (10*60*60)  # 1小时

global con
con = ConnManage()


class UdpServer():
    def handle(self, ip, port):
        self.serverClass = {"ip": "", "port": "", "type": "", "recvData": ""}

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 绑定端口:
        self.s.bind((ip, port))

        p = prtl3761()

        while True:
            # 接收数据:
            ret_bytes, addr = self.s.recvfrom(1024)
            # 加入连接池
            con.Insert(addr, addr[0], addr[1], MAX_LIVE_TIME)

            try:
                ret_str = str(ret_bytes, encoding="utf-8")  # byte 转 字符串(utf8)
                self.serverClass["type"] = "json"
            except:
                try:
                    ret_str = ''.join(['%02x' % b for b in ret_bytes])  # byte 转 字符串(hex)
                    self.serverClass["type"] = "hex"
                except:
                    print("UdpServer handle err")
                    continue

            if len(ret_str) > 5:
                self.serverClass["ip"] = str(addr[0])
                self.serverClass["port"] = str(addr[1])
                self.serverClass["recvData"] = ret_str

                con.Updata(addr, addr[0], addr[1], MAX_LIVE_TIME)
                q.put(self.serverClass)
                if self.serverClass["type"] == "json":
                    if 'Login' in ret_str or 'Heart' in ret_str or 'Event' in ret_str:
                        # conn.sendall(bytes(ret_str + " ", encoding="utf-8"))
                        self.s.sendto(bytes(ret_str + " ", encoding="utf-8"), addr)
                elif self.serverClass["type"] == "hex":
                    ret_str = p.LoginHeartFrame(ret_str)
                    if ret_str is not None:
                        # conn.sendall(bytes.fromhex(ret_str)
                        self.s.sendto(bytes(ret_str + " ", encoding="utf-8"), addr)

    def SocketSend(self, n, data):
        if 0 < con.GetLinkNum():
            if n < con.GetLinkNum():
                addr = con.GetConn(n)
                try:
                    self.s.sendto(bytes(data + " ", encoding="utf-8"), addr)
                except:
                    pass

def ServerMonitor(qRecv, logger):
    while True:
        time.sleep(0.2)
        con.Live()

        while not q.empty():
            data = q.get()
            if qRecv == None: # qRecv未传递参数进来，仅保存日志
                logger.info(data)
                ip, port, jdata = frameforma(data)
                if jdata != None:
                    for jsondata in jdata:
                        if jsondata is not None:
                            processdata(ip, port, jsondata)
                            # logger.warning(jsondata)
                            # print(ip, port, jsondata)
                else:
                    logger.warning("jdata err")
            else:
                qRecv.put(data)

# 获取链接数量
def GetLinkNum():
    return con.GetLinkNum()

# 获取链接端口信息
def GetPoolPortList():
    return con.GetIpPortList()


# 获取链接IP信息
def GetPoolAddrList():
    return con.GetIpList()

if __name__ == '__main__':
    import threading
    ADDRESS = ('192.168.127.16', 8888)  # 绑定地址
    udps = UdpServer()
    qRecv = queue.Queue()

    udpserver = threading.Thread(target=udps.handle, args=(ADDRESS))
    udpserver.start()
    tmonitor = threading.Thread(target=ServerMonitor, args=(qRecv, None))
    tmonitor.start()

    cnt = 0
    while(1):
        cnt+=1
        time.sleep(0.1)
        if not qRecv.empty():
            recv = qRecv.get()
            print(recv)

        if cnt % 100 == 0:
            addr = con.GetConn(0)
            try:
                data = "{'Len':'312','Cmd':'Read','SN':'1','DataTime':'200428121314','CRC':'FFFF','DataValue':{'04A20202':''}}"
                # udps.s.sendto(bytes(data + " ", encoding="utf-8"), addr)
                udps.SocketSend(0, data)
            except:
                pass
