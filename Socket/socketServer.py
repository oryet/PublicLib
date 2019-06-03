import logging.config
import queue
import socketserver
import threading
import time
from PublicLib.Socket.ConnManage import ConnManage
from PublicLib.Protocol.prtl13761 import prtl3761
import PublicLib.public as pub

q = queue.Queue()
server = None
MAX_LIVE_TIME = (10*60*60)  # 1小时

global con
con = ConnManage()

class Myserver(socketserver.BaseRequestHandler):
    def handle(self):
        self.serverClass = {"ip": "", "port": "", "type": "", "recvData": ""}
        conn = self.request
        # 加入连接池
        con.Insert(conn, self.client_address[0], self.client_address[1], MAX_LIVE_TIME)
        # print("link ip:", str(self.client_address[0]), "port:", str(self.client_address[1]))
        p = prtl3761()

        while True:
            time.sleep(0.1)
            try:
                ret_bytes = conn.recv(2048)

                try:
                    ret_str = str(ret_bytes, encoding="utf-8")  # byte 转 字符串(utf8)
                    self.serverClass["type"] = "json"
                except:
                    try:
                        ret_str = ''.join(['%02x' % b for b in ret_bytes]) # byte 转 字符串(hex)
                        self.serverClass["type"] = "hex"
                    except:
                        print("Myserver handle err")
                        continue

                if len(ret_str) > 5:
                    self.serverClass["ip"] = str(self.client_address[0])
                    self.serverClass["port"] = str(self.client_address[1])
                    self.serverClass["recvData"] = ret_str

                    con.Updata(conn, self.client_address[0], self.client_address[1], MAX_LIVE_TIME)
                    q.put(self.serverClass)
                    if self.serverClass["type"] == "json":
                        if 'Login' in ret_str or 'Heart' in ret_str or 'Event' in ret_str:
                            conn.sendall(bytes(ret_str+" ",encoding="utf-8"))
                    elif self.serverClass["type"] == "hex":
                        ret_str = p.LoginHeartFrame(ret_str)
                        if ret_str is not None:
                            conn.sendall(bytes.fromhex(ret_str))
                elif len(ret_str) == 0:
                    self.remove()
                    break
            except:  # 意外掉线
                self.remove()
                break

    def finish(self):
        print("client remove!")

    def remove(self):
        print("client offline!", self.request)
        con.Delect(self.request)

def SocketSend(n, data):
    if 0 < con.GetLinkNum():
        if n < con.GetLinkNum():
            conn = con.GetConn(n)
            try:
                conn.sendall(bytes(data + " ", encoding="utf-8"))
            except:
                pass

def ServerMonitor(qRecv):
    while True:
        time.sleep(0.2)
        con.Live()

        while not q.empty():
            data = q.get()
            if qRecv == None:
                logger.info(data)
            else:
                qRecv.put(data)
            # print(data)

# 获取链接数量
def GetLinkNum():
    return con.GetLinkNum()

# 获取链接端口信息
def GetPoolPortList():
    return con.GetIpPortList()


# 获取链接IP信息
def GetPoolAddrList():
    return con.GetIpList()


def ServerClose():
    server.shutdown()
    server.server_close()

def ServerStart(ADDRESS):
    global server
    server = socketserver.ThreadingTCPServer(ADDRESS, Myserver)
    server.serve_forever()
    return

def SocketSendThread():
    while True:
        time.sleep(0.1)

        if con.GetLinkNum() > 0:
            print("[1、获取在线列表， 2、发送给指定IP]")
            str = input("请输入需要执行的流程：\r\n")
            n = int(str, 10)

            if (n == 1): # 获取在线列表
                iplist = con.GetIpList()
                portlist = con.GetIpPortList()
                for i in range(con.GetLinkNum()):
                    print('索引号：', i, ', IP：', iplist[i], ', Port：', portlist[i])
            elif (n == 2): # 发送给指定IP
                strindex = input("请输入索引号：")
                i = int(strindex, 10)
                if i < con.GetLinkNum():
                    conn = con.GetConn(i)

                    sendstr = input("请输入发送报文：")
                    if len(sendstr) > 10:
                        sendstr = sendstr.replace(" ","")
                        conn.sendall(bytes(sendstr + " ", encoding="utf-8"))
            else:
                pass