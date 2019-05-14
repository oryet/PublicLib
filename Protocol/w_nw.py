# -*- coding: utf-8 -*-

# PHY
def phydealframe(frame):
    l = []
    # 智能判断物理层有无
    datalen = int(frame[:2], 16)
    if datalen + 2 + 1 == len(frame)/2: # 帧长度 = 1 字节，表示长度为 PSDU 中包含的字节数+信道索引号 1 字节+头部校验域 1 字节
        l += ['帧长度:' + str(datalen)]
        chan = int(frame[2:4], 16)
        l += ['信道索引号:' + str(chan)]
        data = frame[6:-4]
        l += [data]
    else:
        l += ['帧长度:' + str(len(frame)/2)]
        l += [frame]
    return l


# MAC
def macdealframe(frame):
    l = []
    pos = 0

    ctrl = int(frame[:4], 16)
    if ctrl & 0x0c == 0x0c:
        addrmode = 12
    else:
        addrmode = 4
    type = (ctrl>>8)&0x07

    # l += [ctrl]
    panid = frame[6:10]
    l += ['panid:' + panid]
    pos = 10 + addrmode
    dstaddr = frame[10:pos]
    l += ['目标地址:' + dstaddr]
    srcaddr = frame[pos:pos + addrmode]
    pos += addrmode
    l += ['源地址:' + srcaddr]
    if type == 0:
        l += ['MAC信标帧']
        l += macbeaconframe(frame[pos:])
    elif type == 1:
        l += ['MAC数据帧']
        data = frame[pos:]
        l += [data]
    elif type == 2:
        l += ['MAC确认帧']
    elif type == 3:
        l += ['MAC命令帧']
    else:
        l += ['MAC未定义帧']

    return l

def macbeaconframe(frame):
    l = []
    l += ['发射随机延时:' + frame[:2]]
    l += ['信标轮次:' + frame[2]]
    l += ['层次号:' + frame[3]]
    l += ['信标轮次限值:' + frame[4]]
    l += ['层次号限:' + frame[5]]
    l += ['时隙号:' + frame[6:10]]
    l += ['信标标识:' + frame[10:12]]
    l += ['网络规模:' + frame[12:16]]
    l += ['场强门限:' + frame[16:18]]
    l += ['中心节点私有信道组号:' + frame[18:20]]
    l += ['中心节点 PANID:' + frame[20:24]]
    l += ['中心节点地址:' + frame[24:36]]
    return l

# NWK
def nwkdealframe(frame):
    l = []
    pos = 0
    routeen = 0

    ctrl = int(frame[:4], 16)
    if ctrl & 0x0c == 0x0c:
        addrmode = 12
    else:
        addrmode = 4
    if ctrl & 0x8000 == 0x8000:
        routeen = 1
    type = (ctrl >> 8) & 0x03

    pos = 4 + addrmode
    dstaddr = frame[4:pos]
    l += ['目标地址:' + dstaddr]
    srcaddr = frame[pos:pos + addrmode]
    pos += addrmode
    l += ['源地址:' + srcaddr]
    sn = frame[pos:pos + 1]
    l += ['帧序号:' + sn]
    r = frame[pos + 1:pos + 2]
    l += ['半径域:' + r]
    pos += 2

    lr = []
    if routeen:
        routeinfo = int(frame[pos:pos + 4], 16)  # 路由信息域
        pos += 4
        num = (routeinfo >> 8) & 0x0F
        relayindex = (routeinfo >> 8) & 0xF0
        lr += ['中继数:' + str(num)]
        lr += ['中继索引' + str(relayindex)]

        relayaddrmode = routeinfo & 0x03
        relayaddrlen = 4
        if relayaddrmode == 0x03:
            relayaddrlen = 12
        for i in range(num):
            lr += ['中继列表:' + frame[pos:pos + relayaddrlen]]
            pos += relayaddrlen

    l += [lr]

    if type == 0:
        l += ['NWK数据帧']
        data = frame[pos:]
        l += [data]
    elif type == 1:
        l += ['NWK命令帧']
        l += nwkcmddeal(frame[pos:])
    else:
        l += ['NWK错误']
        data = frame[pos:]
        l += [data]
    return l


def nwkcmddeal(frame):
    l = []
    type = frame[:2]

    if type == '01':
        l += ["入网申请请求:" + frame[:2]]
        l += [frame[2:]]
    elif type == '02':
        l += ["入网申请响应:" + frame[:2]]
        l += nwkcmdFn02(frame[2:])
    elif type == '03':
        l += ["路由错误:" + frame[:2]]
        l += nwkcmdFn02(frame[2:])
    elif type == '10':
        l += ["场强收集命令:" + frame[:2]]
        l += nwkcmdFn10(frame[2:])
    elif type == '11':
        l += ["场强收集应答:" + frame[:2]]
        l += nwkcmdFn11(frame[2:])
    elif type == '12':
        l += ["配置子节点:" + frame[:2]]
        l += nwkcmdFn12(frame[2:])
    elif type == '13':
        l += ["配置子节点应答:" + frame[:2]]
        l += nwkcmdFn13(frame[2:])
    elif type == '14':
        l += ["网络维护请求命令:" + frame[:2]]
        l += nwkcmdFn14(frame[2:])
    elif type == '15':
        l += ["网络维护响应命令:" + frame[:2]]
        l += nwkcmdFn15(frame[2:])
    elif type == '16':
        l += ["游离节点就绪:" + frame[:2]]
        l += nwkcmdFn16(frame[2:])
    elif type == '17':
        l += ["路径记录:" + frame[:2]]
        l += nwkcmdFn17(frame[2:])
    else:
        l += ["NWK.CI:错误" + frame[:2]]
    return l


def nwkcmdFn01(frame):
    pass


def nwkcmdFn02(frame):
    l = []
    l += ["命令选项:" + frame[0:2]]
    l += ["PanID:" + frame[2:6]]
    l += ["中心节点地址:" + frame[6:18]]
    l += ["层次号:" + frame[18:20]]
    l += ["时隙号:" + frame[20:24]]
    l += ["RSSI :" + frame[24:26]]
    l += ["中继节点数:" + frame[26:28]]
    l += ["中继列表:" + frame[28:]]
    return l


def nwkcmdFn03(frame):
    l = []
    l += ["错误代码:" + frame[0:2]]
    l += ["失败帧目标地址:" + frame[2:]]
    return l


def nwkcmdFn10(frame):
    l = []
    l += ["页序号:" + frame[1]]
    return l


def nwkcmdFn11(frame):
    l = []
    l += ["总页数:" + frame[0]]
    l += ["页序号:" + frame[1]]
    n = int(frame[2:4], 16)
    l += ["节点个数 n:" + frame[2:4]]
    pos = 4
    for i in range(0, n * 2, 2):
        l += ["地址:" + frame[pos: pos + 12]]
        l += ["场强值:" + frame[pos + 12:pos + 14]]
        pos += 14
    return l


def nwkcmdFn12(frame):
    l = []
    pos = 0
    ctrl = int(frame[0:2], 16)
    neten = (ctrl >> 7) & 0x01
    routeen = (ctrl >> 1) & 0x01
    netinfoen = ctrl & 0x01

    if netinfoen:
        l += ["信道组号:" + frame[0:2]]
        l += ["层次号:" + frame[2:4]]
        l += ["时隙号:" + frame[4:8]]
        l += ["短地址:" + frame[8:12]]
        l += ["PanId:" + frame[12:16]]
        l += ["上传路径模式:" + frame[16:18]]
        pos += 18

    if routeen:
        pn = int(frame[pos:pos + 2], 16)
        l += ["路径数 n:" + frame[pos:pos + 2]]
        pos += 2
        for i in range(0, pn * 2, 2):
            rn = int(frame[pos + i:pos + i + 2], 16)
            l += ["中继数:" + frame[pos + i:pos + i + 2]]
            l += ["中继列表:" + frame[pos + i + 2:pos + i + 2 + rn * 2]]
            pos += 2 + rn * 2
    return l


def nwkcmdFn13(frame):
    l = []
    l += ["命令选项:" + frame[0:2]]
    l += ["硬件版本信息:" + frame[2:6]]
    l += ["软件版本信息:" + frame[6:12]]
    l += ["厂家标识:" + frame[12:16]]
    l += ["节点类型:" + frame[16:18]]
    return l


def nwkcmdFn14(frame):
    l = []
    l += ["跳数:" + frame[0:2]]
    pn = int(frame[0:2], 16)
    for i in range(0, pn * 2, 2):
        l += ["第" + str(pn) + "跳下行场强:" + frame[2 + pn:2 + pn + 2]]
    return l


def nwkcmdFn15(frame):
    l = []
    l += ["跳数:" + frame[0:2]]
    pn = int(frame[0:2], 16)
    for i in range(0, pn * 2, 2):
        l += ["第" + str(pn) + "跳下行场强:" + frame[2 + pn:2 + pn + 2]]
    for i in range(0, pn * 2, 2):
        l += ["第" + str(pn) + "跳上行场强:" + frame[2 + pn:2 + pn + 2]]
    return l


def nwkcmdFn16(frame):
    l = []
    l += ["命令选项:" + frame[0:2]]
    l += ["层次号:" + frame[2:4]]
    l += ["时隙号:" + frame[4:8]]
    return l


def nwkcmdFn17(frame):
    l = []
    l += ["广播标识 ID:" + frame[0:2]]
    l += ["层次号:" + frame[2:4]]
    l += ["时隙号:" + frame[4:8]]
    l += ["网络规模:" + frame[8:12]]
    l += ["目标地址数量:" + frame[12:14]]
    n = int(frame[12:14], 16)
    pos = 14
    for i in range(0, n * 2, 2):
        l += ["目标地址:" + frame[pos:pos+12]]
        pos += 12
    t = frame[pos:pos+2]
    n = int(frame[pos:pos+2], 16)
    l += ["中继深度:" + frame[pos:pos+2]]
    pos += 2
    for i in range(0, n * 2, 2):
        l += ["第" + str(i/2) + "跳广播节点扩展地址:" + frame[pos:pos+12]]
        l += ["第" + str(i/2) + "跳下行场强:" + frame[pos+12:pos+14]]
        pos += 14
    return l


# APS
def apsdealframe(frame):
    l = []
    pos = 0

    ctrl = int(frame[:2], 16)
    dir = (ctrl >> 4) & 0x01
    ex = (ctrl >> 3) & 0x01
    type = ctrl & 0x07

    # l += [type]
    # l += [frame[2:4]]  # SN
    exlen = 0
    if ex:
        exlen = int(frame[4:6], 16) * 2
    pos = 4 + exlen

    if type == 0:
        l += ["APS:确认/否认" + frame[:2]]
        l += ["确认标识:" + frame[4:]]
    elif type == 1:
        l += ["APS:命令帧" + frame[:2]]
        l += apscmddeal(frame[pos:], dir)
    elif type == 2:
        l += ["APS:数据转发帧" + frame[:2]]
        l += ["转发报文:" + frame[4:]]
    elif type == 3:
        l += ["APS:上报帧" + frame[:2]]
        l += ["上报标识符:" + frame[4:6] + ", 0:事件上报"]
        l += ["数据单元:" + frame[6:]]
    elif type == 4:
        l += ["APS:广播业务帧" + frame[:2]]
        l += ["广播业务标识符:" + frame[4:6] + ", 0:广播校时,1:命令搜表"]
        l += ["数据单元:" + frame[6:]]
    elif type == 5:
        l += ["APS:测试帧" + frame[:2]]
        l += ["测试命令标识符:" + frame[4:6] + ", 0:发射测试,1:接收测试"]
        l += ["数据单元:" + frame[6:]]
    else:
        l += ["APS:错误" + frame[:2]]

    return l


def apscmddeal(frame, dir):
    l = []
    type = frame[:2]

    if type == '04':
        l += ["读取配置:" + frame[:2]]
        if dir == 1:
            l += apscmdFn04(frame[2:])
    elif type == '05':
        l += ["设备重启:" + frame[:2]]
    elif type == '06':
        l += ["文件传输:" + frame[:2]]
        if dir == 0:
            l += apscmdFn06(frame[2:])
    elif type == '08':
        l += ["收集从节点附属节点（电表收集）:" + frame[:2]]
        if dir == 1:
            l += apscmdFn08(frame[2:])
    elif type == '09':
        l += ["读取设备升级状态:" + frame[:2]]
        if dir == 1:
            l += ["数据区:" + frame[2:]]
    elif type == 'A1':
        l += ["广播升级:" + frame[:2]]
        l += ["数据区:" + frame[2:]]
    elif type == 'A2':
        l += ["广播启动设备升级:" + frame[:2]]
        l += ["数据区:" + frame[2:]]
    elif type == '80':
        l += ["广播召测中心节点地址与工作信道组号:" + frame[:2]]
        l += ["数据区:" + frame[2:]]
    elif type == '81':
        l += ["查询节点基本信息:" + frame[:2]]
        if dir == 1:
            l += ["数据区:" + frame[2:]]
    elif type == '82':
        l += ["查询中心节点中的节点数量已组网数量:" + frame[:2]]
        if dir == 1:
            l += ["数据区:" + frame[2:]]
    elif type == '83':
        l += ["查询中心节点中的子节点地址:" + frame[:2]]
        l += ["数据区:" + frame[2:]]
    elif type == '84':
        l += ["查询中心节点中的子节点状态:" + frame[:2]]
        l += ["数据区:" + frame[2:]]
    elif type == '85':
        l += ["查询中心节点中的子节点父亲关系:" + frame[:2]]
        l += ["数据区:" + frame[2:]]
    elif type == '86':
        l += ["查询中心节点中的子节点邻居关系:" + frame[:2]]
        l += ["数据区:" + frame[2:]]
    elif type == '87':
        l += ["查询中心节点中的子节点路径:" + frame[:2]]
        l += ["数据区:" + frame[2:]]
    elif type == '88':
        l += ["查询节点中动态内存空间:" + frame[:2]]
        if dir == 1:
            l += ["数据区:" + frame[2:]]
    elif type == '89':
        l += ["查询子节点在网状态、工作信道号:" + frame[:2]]
        if dir == 1:
            l += ["数据区:" + frame[2:]]
    elif type == '8A':
        l += ["查询设备出厂编号:" + frame[:2]]
        if dir == 1:
            l += ["数据区:" + frame[2:]]
    elif type == '8B':
        l += ["指定路径进行抄读:" + frame[:2]]
        l += ["数据区:" + frame[2:]]
    elif type == '8C':
        l += ["查询中心节点（南网）任务信息:" + frame[:2]]
        if dir == 1:
            l += ["数据区:" + frame[2:]]
    elif type == 'C0':
        l += ["设置中心节点中的子节点路径:" + frame[:2]]
        l += ["数据区:" + frame[2:]]
    elif type == 'C1':
        l += ["初始化中心节点信息:" + frame[:2]]
        l += ["数据区:" + frame[2:]]
    elif type == 'C2':
        l += ["启动组网:" + frame[:2]]
        l += ["数据区:" + frame[2:]]
    elif type == 'C3':
        l += ["启动网络维护:" + frame[:2]]
        l += ["数据区:" + frame[2:]]

    else:
        l += ["APS.CI:错误" + frame[:2]]
    return l


# APS 命令帧解析
def apscmdFn04(frame):
    l = []

    l += ["设备出厂地址:" + frame[2:14]]
    l += ["节点类型:" + frame[14:16]]
    l += ["PanID:" + frame[16:20]]
    l += ["短地址:" + frame[20:24]]
    l += ["厂家标识:" + frame[24:28]]
    l += ["硬件版本:" + frame[28:32]]
    l += ["软件版本:" + frame[32:38]]
    l += ["发射功率:" + frame[38:40]]
    l += ["RSSI 门限:" + frame[40:42]]
    l += ["信道组号:" + frame[42:44]]
    l += ["层次号:" + frame[44:46]]
    l += ["时隙号:" + frame[46:50]]
    l += ["网络容量:" + frame[50:54]]

    pn = int(frame[54:56], 16)
    l += ["路径数 n:" + frame[54:56]]
    pos = 56
    for i in range(0, pn * 2, 2):
        rn = int(frame[56 + i:56 + i + 4], 16)
        l += ["中继数:" + frame[pos + i:pos + i + 2]]
        l += ["中继列表:" + frame[pos + i + 2:pos + i + 2 + rn * 2]]
        pos += 2 + rn * 2

    return l


def apscmdFn06(frame):
    l = []

    l += ["升级信息 ID:" + frame[2:4]]
    l += ["信息长度:" + frame[4:6]]
    l += ["信息内容:" + frame[6:]]
    return l


def apscmdFn08(frame):
    l = []

    l += ["总页数:" + frame[0]]
    l += ["页序号:" + frame[1]]
    l += ["附属节点数量:" + frame[2:4]]
    n = int(frame[2:4], 16)
    pos = 4
    for i in range(n):
        l += ["附属节点地址:" + frame[pos:pos + 12]]
        l += ["通信协议:" + frame[pos + 12]]
        l += ["波特率:" + frame[pos + 13]]
        pos += 14

    return l

def wnwdealframe(frame):
    l = []
    frame = frame.replace(' ', '')
    phy = phydealframe(frame)
    l = phy[:-1]
    mac = macdealframe(phy[-1])
    l += mac[:-1]
    #print(mac)
    if 'MAC数据帧' in mac:
        nwk = nwkdealframe(mac[-1])
        l += nwk[:-1]
        #print(nwk)
        if 'NWK数据帧' in nwk:
            aps = apsdealframe(nwk[-1])
            l += aps
            #print(aps)
    return l


if __name__ == '__main__':
    '''
    frame = "43 01 42 01 0C B5 FF FF AA AA AA AA AA AA 01 00 04 03 02 01 00 0C AA AA AA AA AA AA 01 00 " \
            "04 03 02 01 F1 11 09 04 01 00 04 03 02 01 01 3D 06 83 00 59 4C 00 01 00 01 01 01 60 1E 01 " \
            "02 00 1A 00 01 01 02 00 87 7E"

    frame = "2E 00 2E 01 0C 29 3D 06 58 29 08 70 41 20 01 00 04 03 02 01 80 0C 58 29 08 70 41 20 09 00 " \
            "00 55 07 00 A1 01 03 01 00 04 03 02 01 01 EA 08 00 08 F6 16 68 20 3C 00 00 00 18 " \
            "36 00 36 01 0C 2A 3D 06 09 00 00 55 07 00 01 00 04 03 02 01 80 0C 09 00 00 55 07 " \
            "00 58 29 08 70 41 20 A1 01 03 01 00 04 03 02 01 11 EA 08 10 01 58 29 08 70 41 20 00 FA 71"
    '''
    frame = "2E 00 2E 00 0C 01 FF FF FF FF FF FF FF FF 11 22 33 44 55 66 00 00 88 00 00 02 16 00 60 03 34 12 11 22 33 44 55 66 aa bb"

    '''
    frame = frame.replace(' ', '')
    phy = phydealframe(frame)
    print(phy)
    mac = macdealframe(phy[-1])
    print(mac)
    if 'MAC数据帧' in mac:
        nwk = nwkdealframe(mac[-1])
        print(nwk)
        if 'NWK数据帧' in mac:
            aps = apsdealframe(nwk[-1])
            print(aps)
    '''
    print(wnwdealframe(frame))