# coding:utf-8
import socket
import time
import threading
class emsc_client:
    def __init__(self):
        self.host = "192.168.124.2"
        self.port = 9999
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def run(self):
        try:
            self.conn.connect((self.host, self.port))
            time.sleep(3)
            while True:
                # self.conn.send(("toserver" + str(time.time())).encode())
                stx = 'toserver:' + str(time.time())
                self.conn.send(stx)
                print(stx)
                time.sleep(3)
                data = self.conn.recv(1024).decode()
                print ("rx:" + data)
                # print("来自服务端数据 :" + data + "|" + str(time.time()))
                time.sleep(0.1)
        except:
            print("服务器连接异常,尝试重新连接 (10s) ...")
            self.conn.close()
            time.sleep(10) # 断开连接后,每10s重新连接一次
            emsc_client().run()
        finally:
            print("客户端已关闭 ...")


host = "192.168.124.2"
port = 9999
conMeter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# lst_txd = [None, stx, srx]
lst_txd = []
def run():
    try:
        conMeter.connect((host, port))
        time.sleep(3)
        while True:
            # conn.send(("toserver" + str(time.time())).encode())
            if len(lst_txd) > 1:
                # stx = 'toserver:' + str(time.time())
                print('check:' + lst_txd[1])
                conMeter.send(lst_txd[1])
                print ('tx:' + lst_txd[1])
                time.sleep(0.2)
                lst_txd[0] = 1
                data = conMeter.recv(512)
                if len(data) > 0:
                    lst_txd[0] = 2
                    if lst_txd[1].find('set') >= 0:
                        lst_txd[2] = data
                    elif lst_txd[1].find('get') >= 0:
                        lst_txd[2] = data
                    print ('rx:' + data)
            # print("来自服务端数据 :" + data + "|" + str(time.time()))
            time.sleep(0.1)
    except:
        print("服务器连接异常,尝试重新连接 (10s) ...")
        conMeter.close()
        time.sleep(10)  # 断开连接后,每10s重新连接一次
        run()
    finally:
        print("客户端已关闭 ...")

if __name__=="__main__":
    # emsc = emsc_client()
    # emsc.run()
    thrrun = threading.Thread(target=run, args=())
    thrrun.daemon = True
    thrrun.start()
    print ('run-ccc')
    for i in range(0, 60, 1):
        lst_txd += [0, 'set M2 data value 00010001 1000', '']
        told = time.time()
        while True:
            if lst_txd[0] == 2:
                print(lst_txd)
                del lst_txd[:3]
                break
            tnew = time.time()
            if (tnew - told) > 5.0:
                break
            time.sleep(0.1)
    time.sleep(120)
