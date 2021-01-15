import serial  # 导入模块
import threading
import queue
import time


class simSerial(threading.Thread):
    def __init__(self):
        self.q = queue.Queue()
        self.beopen = False
        self.dataType = 'Hex'

    def SetDataType(self, dataType):
        if dataType == 'Hex':
            self.dataType = 'Hex'
        else:
            self.dataType = 'Str'

    def ByteToHex(self, bins):
        try:
            ret = ''.join(["%02X" % x for x in bins]).strip()
        except:
            ret = None
        return ret

    def ByteToStr(self, bins):
        try:
            ret = str(bins, encoding='utf-8')
        except:
            ret = None
        return ret

    def onRecvData(self, data):
        try:
            data = data.decode("GBK")
            # print(data)
        except UnicodeDecodeError as err:
            print(err)
            data = None
            return data


    def searchSerialPort(self):
        ''' Search the valid serial port '''
        ports = []
        for i in range(100):
            port = 'COM' + str(i + 1)
            try:
                s = serial.Serial(port)
                if s.isOpen():
                    s.close()
                ports.append(port)
            except Exception as msg:
                pass
        return ports

    def onSendData(self, ser, data=None, _type="hex"):
        # if not data:
        #     data = self.leTx.text()
        if _type == "hex":
            data = [int(x, 16) for x in data.replace('0x', '').split()]  # split 分隔符切片
        else:
            data = bytes(data, 'utf-8')


        return self.DWritePort(ser, data)

    '''
    def ReadData(self, ser):
        # 循环接收数据，此为死循环，可用线程实现
        while True:
            if ser.in_waiting:
                byteRecv = ser.read(ser.in_waiting)
                if len(byteRecv) > 0:
                    time.sleep(0.02)
                    byteRecv += ser.read(ser.in_waiting)
                strRecv = self.ByteToHex(byteRecv)
                self.q.put(strRecv)
                print("Recv:", strRecv)
    '''

    def ReadDatas(self, ser, bytetimeout=0.05, _type='hex'):
        while True:
            data = ser.read(1)
            time.sleep(0.02)
            if self.beopen == False:
                self.q.put('') # 空消息，触发接收监控停止
                return
            if data == b'':
                continue
            while True:
                n = ser.inWaiting()
                if n > 0:
                    data += ser.read(n)
                    time.sleep(bytetimeout)
                else:
                    quit = True
                    break
            if quit:
                if self.dataType == 'hex':
                    strRecv = self.ByteToHex(data)
                else:
                    strRecv = self.ByteToStr(data)
                    if strRecv == None:
                        strRecv = self.ByteToHex(data)

                if strRecv != None:
                    self.q.put(strRecv)
                # print("Recv:", strRecv)

    # 打开串口
    # 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
    # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
    def DOpenPort(self, portx, bps, timeout=1, _type='hex'):
        ret = False
        try:
            # 打开串口，并得到串口对象
            ser = serial.Serial(portx, bps, 8, 'E', 1, timeout=timeout)
            # 判断是否打开成功
            if ser.is_open:
                ret = True
                bytetimeout = 8*20 / int(bps, 10)
                threading.Thread(target=self.ReadDatas, args=(ser, bytetimeout, _type)).start()
                self.beopen = True
                return ret, ser
        except Exception as e:
            print("---异常---：", e)
            return ret, None

    # 关闭串口
    def DColsePort(self, ser):
        self.beopen = False
        ser.close()

    # 写数据
    def DWritePort(self, ser, text):
        # result = ser.write(text.encode("gbk"))  # 写数据
        # result = ser.write(text.encode("utf-8"))  # 写数据
        try:
            result = ser.write(text)  # 写数据
        except:
            result = ser.write(text.encode("utf-8"))  # 写数据
        return result

    # 读数据
    def DReadPort(self):
        str = ''
        if not self.q.empty():
            str = self.q.get()
        return str


if __name__ == '__main__':
    from PublicLib.public import *
    ss = simSerial()

    cfg = {'port':'COM1', 'baud':'2400',"parity": "Even", "bytesize":8, "stopbits":1,"timeout": 1}
    ret, ser = ss.DOpenPort(cfg['port'], cfg['baud'],cfg['timeout'],'hex')
    while ret:
        str = ss.DReadPort()  # 读串口数据
        s = frameaddspace(str)
        ss.onSendData(ser, s, 'hex')
