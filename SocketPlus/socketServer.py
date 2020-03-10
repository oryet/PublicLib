import queue
import threading
import socketserver
from PublicLib.SocketPlus.ConnManage import ConnManage
from PublicLib.Protocol.prtl13761 import prtl3761
from PublicLib.MySqldb.Frame2Json import *
from PublicLib.SocketPlus.socketJson import *
from PublicLib.SocketPlus.socket3761 import *
from PublicLib.SocketPlus.socketApp import *

q = queue.Queue()
server = None
MAX_LIVE_TIME = (10*60*60)  # 1小时

global con
con = ConnManage()

class Myserver(socketserver.BaseRequestHandler):
    def frametype(self, ret_bytes):
        try:
            ret_str = str(ret_bytes, encoding="utf-8")  # byte 转 字符串(utf8)
            ret_json = subStrToJson(ret_str)
            if ret_json:
                self.serverClass["type"] = "json"
            else:
                self.serverClass["type"] = "str" # str 与 hex 判读可能存在误差，部分hex帧因为utf8可以解析，被误认为是str
        except:
            try:
                ret_str = ''.join(['%02x' % b for b in ret_bytes])  # byte 转 字符串(hex)
                self.serverClass["type"] = "hex"
            except:
                print("Myserver handle err")
                return False, None
        return True, ret_str

    def handle(self):
        self.serverClass = {"ip": "", "port": "", "type": "", "recvData": ""}
        conn = self.request
        # 加入连接池
        con.Insert(conn, self.client_address[0], self.client_address[1], MAX_LIVE_TIME)
        print("link ip:", str(self.client_address[0]), "port:", str(self.client_address[1]))
        p = prtl3761()
        sapp = SocketApp()

        while True:
            time.sleep(0.1)
            try:
                ret_bytes = conn.recv(2048)
                ret, ret_str = self.frametype(ret_bytes)
                # print(ret, ret_str, self.serverClass["type"])
                if not ret:
                    continue

                if len(ret_str) >= 5:
                    self.serverClass["ip"] = str(self.client_address[0])
                    self.serverClass["port"] = str(self.client_address[1])
                    self.serverClass["recvData"] = ret_str

                    con.Updata(conn, self.client_address[0], self.client_address[1], MAX_LIVE_TIME, self.serverClass["type"])
                    q.put(self.serverClass)
                    # 分类应答
                    if self.serverClass["type"] == "json":
                        socket_json(ret_str, conn)
                    elif self.serverClass["type"] == "hex":
                        socket3761(ret_str, p, conn)
                    elif self.serverClass["type"] == "str":
                        sapp.socketMsgHandle(con, conn, self.serverClass)

                    # 监听
                    self.listen(conn, con)

                elif len(ret_str) == 0:
                    self.remove()
                    break
            except:  # 意外掉线
                self.remove()
                break

    def listen(self, conn, con):
        # 存在监听端口
        listenlist = con.IsListenPort(conn)

        # 向监听端口转发当前报文
        for port in listenlist:
            n = con.GetConnIndex(None, port)
            if 0 <= n < con.GetLinkNum():
                senddata = '\r\n' + self.serverClass['ip'] + ':' + self.serverClass['port'] + ' recv:'+ self.serverClass['recvData']
                SocketSend(n, senddata)

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
            try:
                n = int(str, 10)
            except:
                continue

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