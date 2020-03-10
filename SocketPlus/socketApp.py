
class SocketApp():
    def sockapp_print(self, con, conn):
        sendstr = ''
        iplist = con.GetSockDataList('ip')
        portlist = con.GetSockDataList('port')
        typelist = con.GetSockDataList('type')
        for i in range(con.GetLinkNum()):
            if typelist[i] in ['json', 'hex']:
                print('index：', i, ', IP：', iplist[i], ', Port：', portlist[i], ', Tpye：', typelist[i])
                sendstr += 'index:' + str(i) + ', IP:' + str(iplist[i]) + ', Port:' + str(portlist[i]) + ', Tpye:' + str(typelist[i]) + '\r\n'
        if len(sendstr) > 0:
            conn.sendall(bytes(sendstr + " ", encoding="utf-8"))


    def sockapp_send(self, con, i, sendstr):
        conn = con.GetConn(i)
        if len(sendstr) >= 5:
            sendstr = sendstr.replace(" ", "")
            conn.sendall(bytes(sendstr + " ", encoding="utf-8"))


    def _strlist2dec(self, ml):
        l = []
        for n in ml:
            try:
                l += [int(n, 10)]
            except:
                pass
        return l


    def socketMsgHandle(self, con, conn, conninfo):
        msg = conninfo["recvData"]
        ml = msg.split(' ')
        if 'print' in ml[0]:
            self.sockapp_print(con, conn)
        elif 'send' in ml[0] and len(ml) == 3:
            i = int(ml[1], 10)
            if i < con.GetLinkNum():
                self.sockapp_send(con, i, ml[2])
        elif 'listen' in ml[0] and len(ml) >= 2:
            ip = conninfo["ip"]
            port = int(conninfo["port"], 10)
            id = con.GetConnIndex(ip, port)
            if id >= 0:
                l = self._strlist2dec(ml[1:])
                con.CreatListen(port, l)



