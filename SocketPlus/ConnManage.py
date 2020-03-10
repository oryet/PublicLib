class ConnManage():
    def __init__(self):
        self.connPool = []

    def Insert(self, conn, ip, port, live):
        dictConnInfo = {'ip': ip, 'port': port, 'live': live, 'type': 'none', 'listen':[]}
        self.connPool.append([conn, dictConnInfo])

    def Delect(self, conn):
        for i in range(len(self.connPool)):
            if self.connPool[i][0] == conn:
                del self.connPool[i]
                break

    def Updata(self, conn, ip, port, live, type):
        for i in range(len(self.connPool)):
            if self.connPool[i][0] == conn:
                self.connPool[i][1]['ip'] = ip
                self.connPool[i][1]['port'] = port
                self.connPool[i][1]['live'] = live
                self.connPool[i][1]['type'] = type
                break

    def CreatListen(self, port, portlist):
        for listenport in portlist:
            n = self.GetConnIndex(None, listenport)
            if 0 <= n < len(self.connPool):
                self.connPool[n][1]['listen'] += [port]

    def IsListenPort(self, conn):
        for i in range(len(self.connPool)):
            if self.connPool[i][0] == conn:
                return self.connPool[i][1]['listen']
        return []

    def Live(self):
        for i in range(len(self.connPool)):
            self.connPool[i][1]['live'] = self.connPool[i][1]['live'] - 1
            # 小于0删除conn
            if self.connPool[i][1]['live'] < 0:
                conn = self.connPool[i][0]
                del self.connPool[i]
                return conn
            elif self.connPool[i][1]['live'] % 300 == 0:     #  1min 检查监听端口号是否存在
                pl = self.GetIpPortList()
                for i in range(len(self.connPool[i][1]['listen'])):
                    if self.connPool[i][1]['listen'][i] not in pl:
                        self.connPool[i][1]['listen'].pop(i)
        return None

    def GetLinkNum(self):
        return len(self.connPool)

    def GetConn(self, n):
        if n < len(self.connPool):
            return self.connPool[n][0]

    def GetConnIndex(self, ip=None, port=None):
        for i in range(len(self.connPool)):
            if self.connPool[i][1]['ip'] == ip and port == None:
                return i
            elif self.connPool[i][1]['port'] == port and ip == None:
                return i
            elif self.connPool[i][1]['ip'] == ip and self.connPool[i][1]['port'] == port:
                return i
        return -1


    def GetIpList(self):
        listIp = []
        for i in range(len(self.connPool)):
            listIp.append(self.connPool[i][1]['ip'])
        return listIp

    def GetIpPortList(self):
        listIpPort = []
        for i in range(len(self.connPool)):
            listIpPort.append(self.connPool[i][1]['port'])
        return listIpPort

    def GetSockTypeList(self):
        listSockType = []
        for i in range(len(self.connPool)):
            listSockType.append(self.connPool[i][1]['type'])
        return listSockType

    def GetSockDataList(self, data):
        datalist = []
        if data in ['ip', 'port', 'type']:
            for i in range(len(self.connPool)):
                datalist.append(self.connPool[i][1][data])
        return datalist
