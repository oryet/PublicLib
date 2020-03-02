
class SocketApp():
    def sockapp_print(self, con):
        iplist = con.GetSockDataList('ip')
        portlist = con.GetSockDataList('port')
        typelist = con.GetSockDataList('type')
        for i in range(con.GetLinkNum()):
            if typelist[i] in ['json', 'hex']:
                print('索引号：', i, ', IP：', iplist[i], ', Port：', portlist[i], ', Tpye：', typelist[i])


    def sockapp_send(self, con, i, sendstr):
        conn = con.GetConn(i)
        if len(sendstr) > 10:
            sendstr = sendstr.replace(" ", "")
            conn.sendall(bytes(sendstr + " ", encoding="utf-8"))


    def socketMsgHandle(self, msg, con):
        ml = msg.split(' ')
        if 'print' in ml[0]:
            self.sockapp_print(con)
        elif 'send' in ml[0]:
            i = int(ml[1], 10)
            if i < con.GetLinkNum():
                self.sockapp_send(con, i, ml[2])



