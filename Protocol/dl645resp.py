import sys

sys.path.append('../')
from PublicLib.public import calcCheckSum
import PublicLib.public as pfun
import PublicLib.Protocol.dl645format as fat
import PublicLib.ACModule.read_ins as rdins
import PublicLib.ACModule.read_energy as rdeng
import PublicLib.ACModule.read_freeze as rdfrz
import PublicLib.ACModule.read_para as rdpara
import PublicLib.ACModule.read_demand as rddemand

# 645报文各元素的位置
POS_64507_HEAD = 0
POS_64507_ADDR = 2  # 1
POS_64507_HEAD2 = 14  # 7
POS_64507_CTRL = 16  # 8
POS_64507_LEN = 18  # 9
POS_64507_DATA = 20  # 10

# 645报文最小长度
MIN_LEN_645FRAME = 24  # 12

HEAD_FRAME = 'FEFEFEFE'

# resp:True  被动设备，只响应抄读帧，并进行应答
# resp:False 主动设备，解析设备的响应帧
def dl645_dealframe(frame, resp=True):
    frame = frame.replace(' ', '')
    if len(frame) < MIN_LEN_645FRAME:
        return False, None
    frame = frame.upper()
    dt = {'addr': '', 'ctrl': '', 'data': ''}
    for i in range(0, len(frame), 2):
        if frame[i:i + 2] == '68' and frame[(i + POS_64507_HEAD2):(i + POS_64507_HEAD2) + 2] == '68':
            dataLen = int(frame[(i + POS_64507_LEN):(i + POS_64507_LEN + 2)], 16) * 2
            if dataLen + POS_64507_LEN < len(frame):
                frameLen = i + dataLen + POS_64507_LEN
                checkSum = calcCheckSum(frame[i:(frameLen + 2)])
                checkSum = checkSum[-2:]
                checkSum = checkSum.upper()
                if checkSum == frame[frameLen + 2:frameLen + 4] and \
                        frame[frameLen + 4:frameLen + 6] == '16':
                    addr = frame[i + POS_64507_ADDR:i + POS_64507_ADDR + 12].upper()
                    dt['addr'] = pfun._strReverse(addr)
                    # dt['ctrl'] = frame[i + POS_64507_CTRL:i + POS_64507_CTRL + 2]
                    dt['ctrl'] = int(frame[i + POS_64507_CTRL:i + POS_64507_CTRL + 2], 16)
                    # dt['data'] = frame[i + POS_64507_DATA:i + POS_64507_DATA + dataLen]
                    datastr = frame[i + POS_64507_DATA:i + POS_64507_DATA + dataLen]
                    if resp:
                        dt['data'] = fat.str2hex(datastr, 1)
                    else:
                        dt['data'] = datastr

                    if resp and dt['ctrl'] & 0x80 == 0:  # 只响应抄读帧
                        return True, dt
                    elif resp is False and dt['ctrl'] & 0x80 == 0x80:
                        return True, dt
    return False, None


# 十六进制 转 字符串 再 组帧
def dl645_makeframe(dt):
    # datavalue 转换

    if 'datavalue' not in dt or dt['datavalue'] == None or len(dt['datavalue']) == 0:
        dt['data'] = [0x02]
        dt['ctrl'] |= 0xC0
    else:
        dt['data'] += fat.str2hex(dt['datavalue'], 0)

    # 计算长度
    dlen = len(dt['data'])

    dt['dlen'] = fat.hex2str([dlen], 0)
    dt['ctrl'] = fat.hex2str([dt['ctrl'] | 0x80], 0)
    dt['addr'] = pfun._strReverse(dt['addr'])
    dt['data'] = fat.hex2str(dt['data'], 1)  # hex

    frame = '68' + dt['addr'] + '68' + dt['ctrl'] + dt['dlen'] + dt['data']  # + dt['cs'] + '16'

    # 计算CRC
    dt['cs'] = pfun.calcCheckSum(frame)
    frame += dt['cs'] + '16'

    # print('Send:', frame)

    # 字节间增加空格
    framespace = ''
    for i in range(0, len(frame), 2):
        framespace += frame[i:i + 2] + ' '
    return framespace


def dl645_read(dt, mtr, index, mmtr=None):
    if mmtr:
        pn = mmtr.getphaseNum(index)
    else:
        pn = mtr.getphaseNum(index)

    if len(dt['data']) < 4:
        return

    DI = dt['data'][:4]
    DI.reverse()

    if DI[0] == 0x00 and DI[3] == 0x00:
        if mmtr:
            eng = mmtr.readenergy(mtr, index)
        else:
            eng = mtr.readenergy(index)
        dt['datavalue'] = rdeng.dl645_readenergy(DI, eng, pn)
    elif DI[0] == 0x00 and 1 <= DI[3] <= 12:
        if mmtr:
            fzday = None
        else:
            fzday = mtr.readhismon(index, DI[3])
        dt['datavalue'] = rdfrz.dl645_readfremonth(DI, fzday, pn)
    elif DI[0] == 0x01:
        dt['datavalue'] = rddemand.dl645_readdemand()
    elif DI[0] == 0x02 and DI[1] == 0x80:
        if mmtr:
            demand = mmtr.readdemand(mtr, index)
        else:
            demand = mtr.readdemand(index)
        dt['datavalue'] = rddemand.dl645_readdemand(DI, demand, pn)
    elif DI[0] == 0x02:
        if mmtr:
            ins = mmtr.readins(mtr, index)
        else:
            ins = mtr.readins(index)
        dt['datavalue'] = rdins.dl645_readins(DI, ins, pn)
    elif DI[0] == 0x03:
        dt['datavalue'] = dl645_readevent()
    elif DI[0] == 0x04:
        dt['datavalue'] = rdpara.dl645_readpara(DI, dt['addr'][0:4])
    elif DI[0] == 0x05:
        if mmtr:
            fzday = None
        else:
            fzday = mtr.readhisday(index, DI[3])
        if DI[2] == 0:
            dt['datavalue'] = rdfrz.dl645_freezetime('day', dt['ctime'], DI[3])
        else:
            dt['datavalue'] = rdfrz.dl645_readfreday(DI, fzday, pn)
    elif DI[0] == 0x06:
        dt['datavalue'] = rdfrz.dl645_readcure()


def dl645_write():
    pass


def dl645_readaddr():
    pass


def dl645_writeaddr():
    pass


def dl645_clearmeter():
    pass


# def dl645_readdemand():
#     pass


def dl645_readevent():
    pass


if __name__ == '__main__':
    from MeterReadingSimulation.devMeter485 import meter485
    from PublicLib.ACModule.simRTC import simrtc

    mtr = meter485()
    mtr.addmeter(1, 3)
    mtr.run(3600)
    mtr.run(3600)

    # frame = 'FE FE FE FE 68 01 00 00 00 50 48 68 11 04 33 32 35 33 4b 16'
    # frame = 'FE FE FE FE 68 01 00 00 00 50 48 68 11 04 33 33 37 35 50 16'
    # frame = '68 01 00 00 00 50 48 68 11 04 33 32 34 35 4C 16'
    # frame = 'FE FE FE FE 68 AA AA AA AA AA AA 68 11 04 33 33 39 38 B8 16 '
    frame = '68230100001523681104333337351316'
    ret, dt = dl645_dealframe(frame)
    print(ret, dt)

    rtc = simrtc()
    dt['ctime'] = rtc.gettick()

    if ret:
        index = mtr.readindex(dt['addr'])
        dt['index'] = index

        eng = mtr.readenergy(index)
        # print(eng)
        # dl645_read(dt, eng.energy)

        ins = mtr.readins(index)
        print(ins)
        dl645_read(dt, mtr, index)

        fe = dl645_makeframe(dt)
        print(fe)
