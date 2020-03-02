class ConnManage():
    def __init__(self):
        self.connPool = []

    def Insert(self, conn, ip, port, live):
        dictConnInfo = {'ip': ip, 'port': port, 'live': live, 'type': 'none'}
        self.connPool.append([conn, dictConnInfo])

    def Delect(self, conn):
        for i in range(len(self.connPool)):
            if self.connPool[i][0] == conn:
                del self.connPool[i]
                break

    def Updata(self, conn, ip, port, live, type):
        dictConnInfo = {'ip': ip, 'port': port, 'live': live, 'type': type}
        for i in range(len(self.connPool)):
            if self.connPool[i][0] == conn:
                self.connPool[i][1] = dictConnInfo
                break

    def Live(self):
        for i in range(len(self.connPool)):
            self.connPool[i][1]['live'] = self.connPool[i][1]['live'] - 1
            # 小于0删除conn
            if self.connPool[i][1]['live'] < 0:
                conn = self.connPool[i][0]
                del self.connPool[i]
                return conn
        return None

    def GetLinkNum(self):
        return len(self.connPool)

    def GetConn(self, n):
        if n < len(self.connPool):
            return self.connPool[n][0]

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
