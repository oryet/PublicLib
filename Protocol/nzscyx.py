# coding=utf-8
import serial
import time

COM3LIST = []
# 超时时间
TXOUTTIME = 2.0
# 数据长度
RXBUFFSIZE = 1024
FrameHead = 'aa55fe' #前导标识
FrameStart = 'a801021012'#开始
FrameQuery = 'a801021113'#查询
FrameMkOpen = 'a80103000003'  # 门控开
FrameMkClose = 'a80103000104'  #门控  闭
#以下是4路脉冲高低电平控制（控制遥信开 闭）的报文
FrameYx1Open = 'a8011003000000000000000114'
FrameYx1Close = 'a8011003000001000000000115'
FrameYx2Open = 'a8011003010000010000000116'
FrameYx2Close = 'a8011003010001010000000117'
FrameYx3Open = 'a8011003020000020000000118'
FrameYx3Close = 'a8011003020001020000000119'
FrameYx4Open = 'a8011003030000030000000120'
FrameYx4Close = 'a8011003030001030000000121'

#FrameMjdOpen = 'a80103000003'
#FrameMjdClose = 'a80103000104'

def yxControlClose(nu):
    if nu == 1:
        frame = FrameHead + FrameYx1Close
        yxControlCloseSend(frame)
    elif nu == 2:
        frame = FrameHead + FrameYx2Close
        yxControlCloseSend(frame)
    elif nu == 3:
        frame = FrameHead + FrameYx3Close
        yxControlCloseSend(frame)
    elif nu == 4:
        frame = FrameHead + FrameYx4Close
        yxControlCloseSend(frame)
    elif nu == 0:
        frame = FrameHead + FrameMkClose
        yxControlCloseSend(frame)
    elif nu == 5:
        yxControlCloseSend(FrameHead + FrameYx1Close)
        yxControlCloseSend(FrameHead + FrameYx2Close)
        yxControlCloseSend(FrameHead + FrameYx3Close)
        yxControlCloseSend(FrameHead + FrameYx4Close)


def yxControlCloseSend(frame):
    sendframe = analFrame(frame)
    COM3LIST[0].write(sendframe)
    gFrame = COM3LIST[0].read(RXBUFFSIZE)
    gf = analGetFrame(gFrame)
    time.sleep(20)
    if gf == 'b801':
        print('遥信设置成功')
    else:
        print('遥信设置失败')



def yxControlOpen(nu):
    if nu == 1:
        frame = FrameHead + FrameYx1Open
        yxControlOpenSend(frame)
    elif nu == 2:
        frame = FrameHead + FrameYx2Open
        yxControlOpenSend(frame)
    elif nu == 3:
        frame = FrameHead + FrameYx3Open
        yxControlOpenSend(frame)
    elif nu == 4:
        frame = FrameHead + FrameYx4Open
        yxControlOpenSend(frame)
    elif nu == 5:
        yxControlOpenSend(FrameHead + FrameYx1Open)
        yxControlOpenSend(FrameHead + FrameYx2Open)
        yxControlOpenSend(FrameHead + FrameYx3Open)
        yxControlOpenSend(FrameHead + FrameYx4Open)
    elif nu == 0:
        frame = FrameHead + FrameMkOpen
        yxControlOpenSend(frame)

def yxControlOpenSend(frame):
    sendframe = analFrame(frame)
    COM3LIST[0].write(sendframe)
    gFrame = COM3LIST[0].read(RXBUFFSIZE)
    gf = analGetFrame(gFrame)
    time.sleep(10)
    if gf == 'b801':
        print('遥信设置成功')
    else:
        print('遥信设置失败')

# 门控关
def MkClose():
    sFrame = analFrame(FrameHead + FrameMkClose)
    COM3LIST[0].write(sFrame)
    time.sleep(TXOUTTIME)
    gFrame = COM3LIST[0].read(RXBUFFSIZE)
    gf = analGetFrame(gFrame)
    if gf == 'b801':
        print('控制成功')
    else:
        print('门控关闭失败')


# 门控开
def MkOpen():
    sFrame = analFrame(FrameHead + FrameMkOpen)
    COM3LIST[0].write(sFrame)
    time.sleep(TXOUTTIME)
    gFrame = COM3LIST[0].read(RXBUFFSIZE)
    gf = analGetFrame(gFrame)
    if gf == 'b801':
        print('控制成功')
    else:
        print('门控开启失败')


# 处理查询到的yk数据帧，返回一个字典集turni轮次,statei状态
def dealList(gf):
    ykList = {}
    if len(gf) >= 0 and gf != '':
        if len(gf) == 28:
            gfget = gf[8:24]
            for i in range(0, len(gfget), 2):
                state = gfget[i] + gfget[i + 1]
                if state == '03' or state == '05' or state == '07':
                    ykState = 'open'
                elif state == '00' or state == '02' or state == '06':
                    ykState = 'close'
                ykList.update({'turn' + str((i / 2) + 1): ykState, 'state' + str((i / 2) + 1): str(state)})
            gfgetgj = gf[-4:-2]
            if gfgetgj == '03' or gfgetgj == '05' or gfgetgj == '07':
                ykState = 'open'
            elif gfgetgj == '00' or gfgetgj == '02' or gfgetgj == '06':
                ykState = 'close'
            ykList.update({'turn9': ykState, 'state9': gfgetgj})
    return ykList


# 查询控制状态
def QueryControlState():
    sFrame = FrameHead + FrameQuery
    frame = analFrame(sFrame)
    COM3LIST[0].write(frame)
    time.sleep(TXOUTTIME)
    gFrame = COM3LIST[0].read(RXBUFFSIZE)
    gf = analGetFrame(gFrame)
    return gf


# 解析返回的帧
def analGetFrame(gFrame):
    gf = ''
    if len(gFrame) >= 0 and gFrame != "":
        for i in gFrame:   #i在一个字符串中的每一个字符中遍历，
            gf += hex(ord(i)).replace("0x", "").zfill(2) #ord把ASCII码转为整数，hex把整数转为16进制的字符串，然后每位不足2位，补0.
    else:
        print ('回帧为空')
    return gf


# 对发送的帧进行处理
def analFrame(sframe):
    frame = ''
    if len(sframe) >= 0 and sframe != "":
        for i in range(0, len(sframe), 2):
            sFrame1 = '0x' + sframe[i] + sframe[i + 1]
            frame += chr(int(sFrame1, 16))
    else:
        print ('发送帧为空')
    return frame

import binascii

def order_list(frame):
    a = frame
    a_list = []
    for i in a.split():
        a_list.append(binascii.a2b_hex(i))
    return a_list
def hexShow(argv):
    result = ''
    hLen = len(argv)
    for i in range(0, hLen, 1):
        # print(argv[i])
        # hvol = ord(argv[i])
        hhex = '%02x' % argv[i]
        result += hhex.upper()
    # print('hexShow:' + result)
    return result

# ser = serial.Serial('/dev/ttyUSB0', 9600)
# ser.writelines(order_list())
#从用例中获取的参数，来处理出 脉宽，数量。（第几路暂时预留。待需要时再开发）
def framemesanl(framemes):
    long = '180'
    num = '1'
    way = '0'
    data = framemes.split('；')
    long = data[0].split('：')[1]
    num = data[1].split('：')[1]
    return long, num, way
# 输出一定频率和一定数量的脉冲
def outpulse(framemes):
    long = '180'
    num = '1'
    way = '0'
    long, num, way = framemesanl(framemes)
    frame = frameset(long, num, way)
    sframe = frame
    frame = order_list(frame)
    COM3LIST[0].writelines(frame)
    time.sleep(0.5)
    gFrame = COM3LIST[0].read(RXBUFFSIZE)
    gf =  hexShow(gFrame)
    if gf == 'B801':
        print ('遥信命令发送成功（脉冲输出）')
        return True
    else:
        print('遥信命令发送失败（脉冲输出）')
        return False

#遥信输出校验计算：按字节相加，除100取余
def rehcrc(framecrc):
    crc = '00'
    value = 0
    print(framecrc)
    i = 0
    data = ''
    for item in framecrc:
        i += 1
        data += item
        if i == 2:
            value += int(data)
            data = ''
            i = 0
    print('value:',value)
    crc = str(value%100).zfill(2)
    print('crc',crc)
    return crc

#台体遥信（脉冲）输出报文构成。long,num,way：脉宽、数量和第几路
def frameset(long,num,way):
    head = 'Aa55feA8011003'
    frame = head + way.zfill(2)+ str(int(long)*2).zfill(4) + way.zfill(2) + num.zfill(8)
    crc = rehcrc(frame[10:])
    frame = frame + crc
    print('frame:',frame)
    return frame


# 初始化串口
def initsyscom3():
    if len(COM3LIST) == 0:
        try:
            pcom = serial.Serial('COM3')
            pcom.baudrate = 19200
            pcom.parity = 'N'
            pcom.bytesize = 8
            pcom.stopbits = 1
            pcom.timeout = 3
            pcom.xonxoff = False
            pcom.rtscts = False
            pcom.dsrdtr = False
            pcom.writeTimeout = TXOUTTIME
            COM3LIST.append(pcom)
        except:
            return False
    if COM3LIST[0].isOpen() is True:
        print('误差串口COM3打开成功')
        return True
    else:
        print ('误差串口COM3打开失败')
        return False


def main():
    #王梦修改函数名为：initsyscom->initsyscom3,并添加（0）.待验证
    initsyscom3()
    #90ms  1000个
    # frame = 'Aa55feA8011003000180000000100004'
    #90ms 240个
    # long = '90'
    # num = '240'
    # way = '0'
    # frame = frameset(long, num, way)
    # print('frame:',frame)
    # frame = 'Aa55feA8011003000180000000024036'
    framemes = '脉宽：90；数量：240'
    resultget = outpulse(framemes)
    if resultget == True:
        print('B801合格')
    else:
        print('失败不合格')

if __name__ == '__main__':
    main()
