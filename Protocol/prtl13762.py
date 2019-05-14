# -*- coding: utf-8 -*-
import os
import configparser

# 645报文各元素的位置
POS_13762_HEAD = 0
POS_13762_LEN = 2  # 2
POS_13762_CTRL = 6  # 1
POS_13762_DATA = 8  # 1


# 校验计算函数
def calcCheckSum(framecs):
    checkSum = 0
    for i in range(0, len(framecs), 2):
        checkSum += int(framecs[i:i + 2], 16)
    return str(hex(checkSum))


#  #字符串转化成2进制再转化成字符串
def trans(data):
    StrValue =''
    for i in range(len(data)):
        a=bin(int(data[i],16))
        a=a.zfill(6)
        a=a.replace('0b','')
        StrValue +=''.join(a)
    return  StrValue



#字符串转化成10进制再转化成字符串
def trans1(data):
    if len(data)==2:
        a=int(data,16)
        b=''
        for i in a:
            b=''.join(b)
            return b
    elif len(data)==4:
        data=reverse(data)
        a = str(int(data,16))
        b = ''
        for i in a:
            b = ''.join(b)
            return b


def reverse(data):
    string=""
    for i in range(len(data)-1,-1,-2):
        string +=data[i-1]
        string +=data[i]
    return(string)


def ana(frame,ctrl,data):
    StrValue =[]
    frame1 = ''
    for i in range(0,len(frame),2):
        frame1 +=frame[i:i+2] + ' '
    StrValue.append(frame1)
    LLL = str(int(len(frame)/2))
    StrValue.append('报文长度 = ' + LLL)
    ctrl=trans(ctrl)
    A = str(int(ctrl[2:],2))
    if A == '0':
       B = '保留'
    elif    A == '1':
       B = '集中式路由载波通信'
    elif    A == '2':
       B = '分布式路由载波通信'
    elif    A == '3':
       B = '宽带载波通信 '
    elif    A == '10':
       B = '微功率无线通信 '
    elif    A == '20':
       B = '以太网通信 '
    else: B = '备用 '
    StrValue.append('控制域 ： DIR = ' + ctrl[0] + ' ,' + 'PRM = '+ ctrl[0] +' ,' + '通信方式 = ' + B + '\n' )
    message=data[0:12]
    StrValue.append ('信息域 ：中继级别 = ' + message[0])
    message1=trans(message[1])
    StrValue.append('路由标识 =' + message1[3])
    StrValue.append('附属节点标识 = ' + message1[2])
    StrValue.append('通信模块标识 = ' + message1[1] + ' (0 表示对主节点的操作；1 表示对从节点操作)')
    StrValue.append('冲突检测 = ' + message1[0])
    StrValue.append('信道标识 = ' + message[3])
    StrValue.append('纠错编码标识 = ' + message[2])
    StrValue.append('预计应答字节数 = ' + str(int(message[4:6],16)))
    message2=trans(message[6:10])
    StrValue.append('速率单位标识 = ' + message2[0:1])
    StrValue.append('通信速率 = ' + str(int(message2[1:16],16)))
    StrValue.append('报文序列号 = ' + str(int(message[-2:],16)))
    if message1[1]=='1':
       if message[0]=='0':
           StrValue.append('源地址 = ' + reverse(data[12:24]))
           StrValue.append('目的地址 = ' + reverse(data[24:36]))
           StrValue.append('应用数据域 AFN = '+ data[36:38] +',' 'FN = '+ data[38:42])
           data1 = data[36:]
           abc = DI(ctrl,data1)
           StrValue.extend(abc)
       else:
           StrValue.append('源地址 = ' + reverse(data[12:24]))
           for i in range(1,int( message[0])):
              StrValue.append('中继地址 = ' + reverse(data[12*i:12*(i+1)]))
           StrValue.append('目的地址 = ' + reverse(data[12*int( message[0]):12*(int( message[0])+1)]))
           StrValue.append('应用数据域 AFN = ' + data[12*(int( message[0])+1):12*(int( message[0])+1)+2] + ',' 'FN = ' + data[12*(int( message[0])+1)+2:12*(int( message[0])+1)+6])
           data1=data[12*(int( message[0])+1):]
           StrValue.append(DI(ctrl,data1))
    else:
        StrValue.append('应用数据域 AFN = '+ data[12:14] +',' 'FN = '+ data[14:18])
        data1 = data[12:]
        abc=DI(ctrl,data1)
        StrValue.extend(abc)
    return (StrValue)


def DI(typ,data):
    data1 = data[0:2]
    data2 = data[2:]
    if data1=='00':
            return FieldParsing13762_AFN00(data2)
    elif data1=='01':
            return FieldParsing13762_AFN01(data2)
    elif data1 == '02':
            return FieldParsing13762_AFN02(data2)
    elif data1 == '03':
        if typ == '0':
            return FieldParsing13762_AFN03a(data2)
        else:
            return FieldParsing13762_AFN03b(data2)
    elif data1 == '04':
            return FieldParsing13762_AFN04a(data2)
    elif data1 == '05':
            return FieldParsing13762_AFN05a(data2)
    elif data1 == '06':
            return FieldParsing13762_AFN06b(data2)
    elif data1 == '10':
        if typ == '0':
            return FieldParsing13762_AFN10a(data2)
        else:
            return FieldParsing13762_AFN10b(data2)
    elif data1 == '11':
            return FieldParsing13762_AFN11a(data2)
    elif data1 == '12':
            return FieldParsing13762_AFN12a(data2)
    elif data1 == '13':
        if typ == '0':
            return FieldParsing13762_AFN13a(data2)
        else:
            return FieldParsing13762_AFN13b(data2)
    elif data1 == '14':
        if typ == '0':
            return FieldParsing13762_AFN14a(data2)
        else:
            return FieldParsing13762_AFN14b(data2)
    else:
        return "The AFN is not defined!",data2




def FieldParsing13762_AFN00(data):
     StrValue =[]
     if data[:4]=='0100':
        StrValue.append('确认')
        return StrValue
     elif data[:4]=='0200':
        StrValue.append('否认')
        return (StrValue)
     else:
        return 'Cannot Parse The data: ' + data

def FieldParsing13762_AFN01(data):
    StrValue = []
    if data[:4] == '0100':
        StrValue.append( '硬件初始化')
        return StrValue
    elif data[:4] == '0200':
        StrValue.append( '参数区初始化(清除所有从节点档案信息)')
        return (StrValue)
    elif data[:4] == '0400':
        StrValue.append( '数据区初始化（清除所有从节点通信信息）')
        return (StrValue)
    else:
        return 'Cannot Parse The data: ' + data

def FieldParsing13762_AFN02(data):
    StrValue =[]
    StrValue.append('数据单元 = ' + data[4:] )
    StrValue.append('-------- 数据转发：转发通信协议数据帧 --------')
    if  data[:4] == '0100':
        if len(data)>=8:
            StrValue.append('通信协议类型 = '+ data[4:6] +'(00H为透明传输；01H为 DL/T 645—1997；02H为 DL/T 645—2007；03H为 DL/T—698；04H-FFH保留)')
            StrValue.append('报文长度L = ' + str(int(data[6:8],16)))
            StrValue.append('报文内容 = ' + data[8:])
            return (StrValue)
        else:
              return 'Cannot Parse The data = ' + data
    else:
        return 'Cannot Parse The AFN = ' + data






def FieldParsing13762_AFN03a(data):
    StrValue = []
    StrValue.append('数据单元 = ' + data[4:] )
    if data[:4] == '0100':
        if len(data) == 4:
            StrValue.append('--------查询数据 ：厂商代码和版本信息 --------')
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '0200':
        if len(data) == 4:
            StrValue.append('--------查询数据 ：噪声值 --------')
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '0400':
        StrValue.append('--------查询数据 ：从节点侦听信息 --------')
        if  len(data)==8:
            StrValue.append('开始节点指针 = ' + str(int(data[4:6],16)))
            StrValue.append('读取节点数量 = ' + str(int(data[6:8],16)))
            return StrValue
        else:
             return 'Cannot Parse The data = ' + data
    elif data[:4] == '0800':
        StrValue.append('--------查询数据 ：主节点地址 --------')
        if len(data) == 4:
            return StrValue
        else:
            return 'Cannot Parse The data =' + data
    elif data[:4] == '1000':
        StrValue.append('--------查询数据 ：主节点状态字和通信速率 --------')
        if len(data) == 4:
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '2000':
        StrValue.append('--------查询数据 ：主节点干扰状态 --------')
        if len(data) == 6:
            StrValue.append('主节点干扰持续时间 = ' + str(int(data[4:6], 16)) + '（单位min）')
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '4000':
        StrValue.append('--------查询数据 ：读取从节点监控最大超时时间 --------')
        if len(data) == 4:
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '8000':
        StrValue.append('--------查询数据 ：查询无线通信参数 --------')
        if len(data) == 4:
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '0101':
        StrValue.append('--------查询数据 ：查询从节点通信延时 --------')
        if len(data) >=8:
            StrValue.append( '通信协议类型 = ' + data[4:6] + ' (00H为透明传输；01H为 DL/T 645—1997；02H为 DL/T 645—2007；03H为 DL/T—698；04H-FFH保留)')
            StrValue.append('报文长度L = ' + str(int(data[6:8]), 16))
            StrValue.append('报文内容 = ' + data[8:])
            return (StrValue)
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '0201':
        StrValue.append('--------查询数据 ：本地通信模块运行模式信息 --------')
        if len(data) == 4:
            return StrValue
        else:
            return 'Cannot Parse The data =' + data
    elif data[:4] == '0401':
        StrValue.append('--------查询数据 ：本地通信模块 AFN 索引 --------')
        if len(data)==6:
            StrValue.append('AFN功能码 = ' + data[4:6])
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '080C':
        StrValue.append('--------查询数据 ：查询场强门限 --------')
        if len(data)==4:
            return  StrValue
        else:
            return 'Cannot Parse The data = ' + data





def FieldParsing13762_AFN03b(data):
    StrValue = []
    StrValue.append('数据单元 = ' + data[4:])
    if data[:4] == '0100':
        if len(data)==22:
            StrValue.append('--------查询数据 ：厂商代码和版本信息 --------')
            StrValue.append('厂商代码 = ' + chr(int(data[4:6],16)) + chr(int(data[6:8],16)))
            StrValue.append('芯片代码 = ' + chr(int(data[8:10],16)) + chr(int(data[10:12],16)))
            StrValue.append('版本日期 = ' + reverse(data[12:18]))
            StrValue.append('版本 = ' + reverse(data[18:22 ]) )
            return  StrValue
        else:
             return 'Cannot Parse The data = ' + data
    elif data[:4] == '0200':
        if len(data)==6:
            StrValue.append('--------查询数据 ：噪声值 --------')
        #a = bin(int(data[4:6], 16))
            StrValue.append('噪声强度 = ' + str(int(data[5],)))
            return StrValue
        else:
             return 'Cannot Parse The data = ' + data
    elif data[:4] == '0400':
        StrValue.append('--------查询数据 ：从节点侦听信息 --------')
        if len(data) > 16:
            StrValue.append('侦听到从节点总数量 = ' + data[4:6] )
            StrValue.append('侦听到本帧传输的从节点总数量 = ' + str(int(data[6:8],16 )))
            a = int(data[6:8],16)
            for i in range (0,a):
                StrValue.append('从节点地址'+ str(i + 1) + ' = ' + reverse(data[8+12*i:8+12*(i+1)]))
                StrValue.append('侦听信号品质 = ' + data[8+12*(i+1):9+12*(i+1)])
                StrValue.append('中继级别 = ' + data[9 + 12*(i+1):10 + 12*(i+1)])
                StrValue.append('侦听次数 = ' + data[11 + 12*(i+1):12 + 12*(i+1)])
            return StrValue
        else:
             return 'Cannot Parse The data: ' + data
    elif data[:4] == '0800':
        StrValue.append('--------查询数据 ：主节点地址 --------')
        if len(data) ==16:
            StrValue.append( '主节点地址 = ' + reverse(data[4:16]))
            return StrValue
        else:
             return 'Cannot Parse The data =' + data
    elif data[:4] == '1000':
        StrValue.append('--------查询数据 ：主节点状态字和通信速率 --------')
        if len(data) >4:
            StrValue.append('状态字 = ' + data[4:6])
            a =trans(data[4])
            if a[0:2]=='00':
               StrValue.append('周期抄表模式 = ' + "路由主动和集中器主动都支持")
            elif a[0:2]=='01':
                StrValue.append('周期抄表模式 = ' + "仅支持集中器主动")
            elif a[0:2] == '10':
                StrValue.append( '周期抄表模式 = ' + "仅支持路由主动")
            StrValue.append('主节点信道特征 = ' + str(int(a[2:4], 16)) + " (0表示微功率无线；1表示单相供电单相传输；2表示单相供电三相传输；3表示三相供电三相传输)")
            StrValue.append('速率数量 = ' + str(int(data[5], 16)) )
            StrValue.append('信道数量 = ' + str(int(data[7], 16)))
            c = int(data[5], 16)
            for i in range (0,c):
                 b = trans(reverse(data[8+4*i:12+4*i]))
                 StrValue.append('通信速率单位标识'+ str(i+1) + ' = ' + b[0] + ' ( 0 表示bit/s,1表示kbit/s)')
                 StrValue.append('通信速率'+ str(i+1) + ' = ' + str(int(b[1:16],2)))
            return  StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '2000':
        StrValue.append('--------查询数据 ：主节点干扰状态 --------')
        if len(data) == 6:
            StrValue.append('主节点干扰持续时间 = '+ str(int(data[4:6],16)) + '（单位min）')
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '4000':
        StrValue.append('--------查询数据 ：读取从节点监控最大超时时间 --------')
        if len(data) == 6:
            StrValue.append('从节点最大超时时间 = ' + str(int(data[4:],16)) +  '（单位s）')
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '8000':
        StrValue.append('--------查询数据 ：查询无线通信参数 --------')
        if len(data) == 8:
            StrValue.append('无线信道组 = ' + str(int(data[4:6],16)))
            StrValue.append('无线主节点发射功率 = ' + str(int(data[6:],16)) + ' (00：最高发射功率，01：次高发射功率，02：次低发射功率，03：最低发射功率)')
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '0101':
        StrValue.append('--------查询数据 ：查询从节点通信延时 --------')
        if  len (data)>=12:
            StrValue.append('广播延时时长 = ' + str(int(reverse(data[4:8]), 16)))
            StrValue.append('通信协议类型 = ' + data[8:10] + ' (00H为透明传输；01H为 DL/T 645—1997；02H为 DL/T 645—2007；03H为 DL/T—698；04H-FFH保留)')
            StrValue.append('报文长度L = ' + str(int(data[10:12]), 16))
            StrValue.append('报文内容 = ' + data[12:])
            return (StrValue)
        else:
            return 'Cannot Parse The data = ' + data
    elif data[0:4] == '0201':
        StrValue.append('--------查询数据 ：本地通信模块运行模式信息 --------')
        if len(data)>=36:
              a=trans(data[4])
              if   a[0:2]=='00':
                    StrValue.append('周期抄表模式 = ' + " 路由主动和集中器主动都支持")
              elif a[0:2]=='01':
                    StrValue.append('周期抄表模式 = ' + " 集中器主动")
              elif a[0:2] == '10':
                    StrValue.append( '周期抄表模式 = ' + " 路由主动")
              StrValue.append('从节点信息模式 = ' + a[2] +" (0表示不需要下发从节点信息；1表示需要下发从节点信息)")
              StrValue.append('路由管理方式 = ' + a[3] +" (0表示无路由管理；1表示有路由管理)")
              StrValue.append('通信方式 = ' + str(int(data[5]))  + " (1表示'窄带电力线载波通信'；2表示'宽带电力线载波通信'；3表示'微功率无线通信'；其他取值保留)")
              b= trans(data[6:8])
              StrValue.append('广播命令执行方式 = ' + str(int(b[:2]))  + " (0表示执行广播命令不需要信道标识'；1表示表示执行广播命令需要信道标识；其他取值保留)")
              StrValue.append('广播命令确认方式 = ' + b[2]  + " (0表示执行广播通信后返回确认帧'；1表示执行广播通信前返回确认帧)")
              if b[3:5]=='10':
                  StrValue.append('失败节点切换发起方式 = ' + b[3:5] + " (集中器发起通知通信模块切换待抄节点)")
              elif b[3:5]=='01':
                  StrValue.append('失败节点切换发起方式 = ' + b[3:5] + " (通信模块自主切换待抄节点)")
              StrValue.append('"广播支持向集中器提供传输延时参数" = ' + b[5] + " (1 表示支持提供传输延时参数，0 表示不支持)")
              StrValue.append('从节点监控支持向集中器提供传输延时参数 = ' + b[6] + " (1 表示支持提供传输延时参数，0 表示不支持)")
              StrValue.append('路由主动抄表支持向集中器提供传输延时参数 = ' + b[7] + " (1 表示支持提供传输延时参数，0 表示不支持)")
              StrValue.append('速率数量n = ' + data[8] )
              StrValue.append('信道数量 = ' + data[9] )
              StrValue.append('低压电网掉电信息 = ' + data[11])
              StrValue.append('从节点监控最大超时时间（单位：s）= ' + str(int(data[16:18],16)))
              StrValue.append('广播命令最大超时时间（单位：s）= ' + str(int(reverse(data[18:22]),16)))
              StrValue.append('最大支持的报文长度 =' + str(int(reverse(data[22:26]),16)))
              StrValue.append('文件传输支持的最大单个数据包长度 = ' + str(int(reverse(data[26:30]),16)))
              StrValue.append('升级操作等待时间 = ' + str(int(data[30:32],16)))
              StrValue.append('主节点地址 = ' + reverse(data[32:44]))
              StrValue.append('支持的最大从节点数量 = ' + str(int(reverse(data[44:48]),16)))
              StrValue.append('当前从节点数量 = ' + str(int(reverse(data[48:52]),16)))
              StrValue.append('通信模块使用的协议发布日期（BCD） = ' + reverse(data[52:58]))
              StrValue.append('通信模块使用的协议最后备案日期（BCD） = ' + reverse(data[58:64]))
              StrValue.append('厂商代码 = ' + chr(int(data[64:66],16)) + chr(int(data[66:68],16)))
              StrValue.append('芯片代码 = ' + chr(int(data[68:70],16)) + chr(int(data[70:72],16)))
              StrValue.append('版本日期 = ' + reverse(data[72:78]))
              StrValue.append('版本 = ' + reverse(data[78:82]))
              a1=int(len(data[82:])/4)
              for i in range(0,a1):
                  c=trans(data[82+4*i:84+4*i])
                  d=trans(data[84+4*i:86+4*i])
                  e=str(d)+str(c)
                  StrValue.append('速率单位标识 = ' + e[0] + '(0 表示 bit/s；1 表示 kbit/s)')
                  StrValue.append('通信速率 = ' + str(int(e[1:16],16)) )
              return  StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '0401':
        if len(data)==70:
            StrValue.append('--------查询数据 ：本地通信模块 AFN 索引 --------')
            StrValue.append('AFN功能码 = ' + data[4:6])
            StrValue.append('F1～F255 等数据单元支持情况 = ' + data[6:70])
            return  StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '080C':
        StrValue.append('--------查询数据 ：查询场强门限 --------')
        if len(data)==6:
            StrValue.append('场强门限 = ' + str(int(data[4:6],16)))
            return  StrValue
        else:
            return 'Cannot Parse The data = ' + data
    else:
            return 'Cannot Parse The AFN = ' + data





def FieldParsing13762_AFN04a(data):
    StrValue = []
    StrValue.append('--------链路接口检测 ：发送测试（主/从节点检测命令） --------')
    if  data[:4] == '0100':
        if len(data) == 6:
            StrValue.append('发送测试持续时间 = ' + int(data[4:6],16))
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif  data[:4] == '0200':
        StrValue.append('--------链路接口检测 ：从节点点名 --------')
        if len(data) == 4:
            return StrValue
        else:
             return 'Cannot Parse The data = ' + data
    elif  data[:4] == '0400':
        StrValue.append('--------链路接口检测 ：本地通信模块报文通信测试 --------')
        if len(data) >= 18:
            StrValue.append('测试通信速率序号 = ' + str(int(data[4:6],16)))
            StrValue.append('目标地址 = ' + reverse(data[6:18]))
            StrValue.append('通信协议类型 = ' + data[18:20] + ' (00H为透明传输；01H为 DL/T 645—1997；02H为 DL/T 645—2007；03H为 DL/T—698；04H-FFH保留)' )
            StrValue.append('报文长度 L = ' + str(int(data[20:22])))
            StrValue.append('报文内容 = ' + data[22:])
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    else:
            return 'Cannot Parse The AFN =' + data








def FieldParsing13762_AFN05a(data):
    StrValue = []
    if  data[:4] == '0100':
        StrValue.append('--------控制命令 ：设置主节点地址 --------')
        if len(data) == 16:
            StrValue.append('设置主节点地址 = ' + reverse(data[4:]))
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] =='0200':
        StrValue.append('--------控制命令 ：允许从节点上报 --------')
        if len(data) == 6:
            StrValue.append('允许/禁止从节点上报 = ' + data[4:] + ' ( 0禁止，1允许 )')
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] =='0400':
        StrValue.append('--------控制命令 ：启动广播 --------')
        if len(data) >8:
            StrValue.append('控制字 = ' + data[4:6] +' (00H＝透明传输；01H＝DL/T645—1997；02H＝DL/T645—2007；03H＝DL/698；04H—FFH保留)')
            StrValue.append('报文长度L = ' + str(int(data[6:8],16)))
            StrValue.append('报文内容 = ' + data[8:8+int(data[6:8],16)*2])
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '0800':
        StrValue.append('--------控制命令 ：设置从节点监控最大超时时间 --------')
        if len(data) ==6:
            StrValue.append('最大超时时间 = '+ str(int(data[4:6],16)))
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4]=='1000':
        StrValue.append('--------控制命令 ：设置无线通信参数 --------')
        if len(data) ==8:
            StrValue.append('无线信道组 = '+ str(int(data[4:6],16)))
            StrValue.append('无线主节点发射功率 = ' + data[6:8] + ' (00：最高发射功率，01：次高发射功率，02：次低发射功率，03：最低发射功率，04～254：保留，255：保持不变)')
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '080C':  #F100设置场强门限
        StrValue.append('--------控制命令 ：设置场强门限 --------')
        if len(data) == 6:
            StrValue.append('设置场强门限 = ' + str(int(data[4:6],16)))  #门限50-120，默认96
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '100C':  # F100设置中心节点时间
        StrValue.append('--------控制命令 ：设置中心节点时间 --------')
        if len(data) == 6:
            StrValue.append('设置中心节点时间 = ' + reverse(data[4:16]))
        else:
            return 'Cannot Parse The data: ' + data
    else:
        return 'Cannot Parse The AFN: ' + data



def FieldParsing13762_AFN06b(data):
    StrValue = []
    if  data[:4] == '0100':
        if len(data[6:]) %18==0:
            for i in range(int(data[4:6])):
                StrValue.append('上报从节点数量 = ' + str(int(data[4:6],16)))
                StrValue.append('从节点地址 = '+ reverse(data[6+18*i:18*(i+1)]))
                StrValue.append('从节点类型 = '+ data[18*(i+1):18*(i+1)+2])
                StrValue.append('从节点序号 = ' +  str(int(data[18*(i+1)+2:18 * (i + 1) + 6],16)))
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif  data[:4] == '0200':
        if len(data) > 8:
            StrValue.append('从节点序号 =' + str(int(reverse(data[4:8],16))))
            StrValue.append( '通讯协议类型 =' + data[8:10] + '（00H＝透明传输；01H＝DL/T645—1997；02H＝DL/T645—2007；03H＝相位识别功能；04HFFH保留）')
            StrValue.append('当前报文本地通信上行时长 =' + data[10:14])
            StrValue.append('报文长度L =' + str(int(data[14:16],16)))
            StrValue.append('报文内容 =' + data[16:16+int(data[14:16],16)] )
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '0400':
        if len(data) == 6:
            StrValue.append('上报路由工况变动信息 =' + data[4:6] +'(1为抄表任务结束；2为搜表任务结束；其它为保留。)')
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '0800':
        if len(data) >= 30:
            StrValue.append('上报从节点数量 =' + str(int(data[4:6],16)))
            a=data[28:30]
            if a==0:
                for i in range(int(data[4:6])):
                    StrValue.append('上报从节地址 =' + data[6+24*i:18+24*i] )
                    StrValue.append('从节点通讯协议类型 =' + data[18+24*i:20+24*i] + '（00H＝透明传输；01H＝DL/T645—1997；02H＝DL/T645—2007；03H＝相位识别功能；04HFFH保留）')
                    StrValue.append( '从节点序号 =' + data[20+24*i:24+24*i] )
                    StrValue.append('从节设备类型 =' + data[24+24*i:26+24*i] + '（00H＝采集器；01H＝电能表；02H—FFH 保留）')
                    StrValue.append( '从节下接的从节点数量 =' + data[26+24*i:28+24*i] )
                    StrValue.append( '本文传输的的从节点数量 =' + data[28+24*i:30+24*i] )
                    return StrValue
            else:
                    StrValue.append( '上报从节地址 =' + data[6:18] )
                    StrValue.append('从节点通讯协议类型 =' + data[18:20] + '（00H＝透明传输；01H＝DL/T645—1997；02H＝DL/T645—2007；03H＝相位识别功能；04HFFH保留）')
                    StrValue.append('从节点序号 =' + data[20:24] )
                    StrValue.append('从节设备类型 =' + data[24:26] + '（00H＝采集器；01H＝电能表；02H—FFH 保留）')
                    StrValue.append('从节下接的从节点数量 =' + data[26:28] )
                    StrValue.append('本文传输的的从节点数量 =' + data[28:30] )
                    for j in range(int(a)):
                        StrValue.append('下接从节点的地址 =' + data[30+14*j:42+14*j])
                        StrValue.append('下接从节点的通信协议类型 =' + data[42+14*j:44+14*j] + '（00H＝透明传输；01H＝DL/T645—1997；02H＝DL/T645—2007；03H＝相位识别功能；04HFFH保留）')
                    return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '1000':
        if len(data) >= 6:
            StrValue.append('从节设备类型 =' + data[4:6 ] + '（00H＝采集器；01H＝电能表；02H—FFH 保留）')
            StrValue.append( '通讯协议类型 =' + data[6:8] + '（00H＝透明传输；01H＝DL/T645—1997；02H＝DL/T645—2007；03H＝DL—698；04H-FFH保留）')
            StrValue.append('报文长度L =' + str(int(data[8:10],16)))
            StrValue.append('报文内容 =' + data[10:] )
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '080C':  #F100设置场强门限
        if len(data) == 6:
            StrValue.append('设置场强门限：' + str(int(data[4:6],16)))  #门限50-120，默认96
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '100C':  # F100设置中心节点时间
        if len(data) == 6:
            StrValue.append('设置中心节点时间：' + reverse(data[4:16]))
        else:
            return 'Cannot Parse The data = ' + data
    else:
        return 'Cannot Parse The AFN = ' + data



def FieldParsing13762_AFN10a(data):
    StrValue = []
    if  data[:4] == '0100':
        if  len(data) ==4:
            return  StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif  data[:4] == '0200':
        if len(data) == 10:
            StrValue.append('从节点起始序号 =' + data[4:8])
            StrValue.append('从节点数量 =' + data[8:])
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif  data[:4] == '0400':
        if len(data) == 16:
            StrValue.append('从节点地址 =' + data[4:])
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '0800':
        if len(data) ==4:
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '1000':
        if len(data) ==10:
            StrValue.append('从节点起始序号 =' + data[4:8])
            StrValue.append('从节点数量 =' + data[8:])
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '2000':
        if len(data) ==10:
            StrValue.append('从节点起始序号 =' + data[4:8])
            StrValue.append('从节点数量 =' + data[8:])
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '080C':  #F100查询网络规模
        if len(data) == 4:
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '100C':  #F100查询网络规模
        if len(data) == 4:
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    else:
        return 'Cannot Parse The AFN: ' + data








def FieldParsing13762_AFN10b(data):
    StrValue = []
    if  data[:4] == '0100':
        if  len(data) ==12:
            StrValue.append('从节点数量 = '+str(int(reverse(data[4:8]),16)))
            StrValue.append('路由支持最大从节点数 = ' + str(int(reverse(data[8:12]),16)))
            return  StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif  data[:4] == '0200':
        if len(data) >=26:
            StrValue.append('从节点总数量 = ' + str(int(reverse(data[4:8]),16)))
            StrValue.append('本次应答的从节点数量 = ' + str(int(data[8:10],16)))
            for i in range(int(data[8:10])):
                 StrValue.append('从节点'+str(1+i) +'地址 = ' + reverse(data[10+16*i:22+16*i]))
                 a=trans(reverse(data[22+16*i:26+16*i]))
                 StrValue.append('通信协议类型 = ' + str(int(a[2:5],2)) +'(00H＝透明传输；01H＝DL/T645—1997；02H＝DL/T645—2007；03H＝DL—698；04H-FFH保留)' )
                 StrValue.append('相位 = ' + a[5:8]+ '(置“1”依次表示第 1、2、3 相)')
                 StrValue.append('侦听信号品质 = ' + str(int(a[8:12],2)))
                 StrValue.append('中继级别 = ' + str(int(a[12:16], 2)))
            return StrValue
        elif len(data)==10:
            StrValue.append('从节点数量 = ' + str(int(data[4:8], 16)))
            StrValue.append('本次应答的从节点数量 = ' + str(int(data[8:10], 16)))
        else:
            return 'Cannot Parse The data: ' + data
    elif  data[:4] == '0400':
        if len(data) >=26:
            StrValue.append('提供路由的从节点总数量 = ' + str(int(data[4:6],16)))
            for i in range(int(data[4:6])):
                 StrValue.append('提供路由的从节点地址 = ' + reverse(data[6+16*i:12+16*i]))
                 StrValue.append('提供路由的从节点信息 = ' + data[12*i:16*i])
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '0800':
        if len(data) ==36:
            c=trans(data[5])
            StrValue.append('纠错编码 = ' + data[4])
            StrValue.append('上报事件标志 = ' + c[1] + '(1为有从节点事件上报，0为无从节点事件上报)')
            StrValue.append('工作标志 = ' + c[2] + '(1为有正在工作，0为停止工作)')
            StrValue.append('路由完成标志 = ' + c[3] + '(1为路由学习完成，0为未完成)')
            StrValue.append('从节点数量 = ' + str(int(reverse(data[6:10]),16)))
            StrValue.append('已抄从节点数量 = ' + str(int(reverse(data[10:14]),16)))
            StrValue.append('中继到从节点数量 = ' + str(int(reverse(data[14:18]),16)))
            g=trans(data[19])
            StrValue.append('允许注册状态 = ' + g[2] +'(1为允许，0为不允许)')
            StrValue.append('工作状态 =' + g[3] + '(1为学习，0为抄表)')
            StrValue.append('通信速率 =' + str(int(reverse(data[20:24]),16)))
            StrValue.append('第1相中继级别 = ' + data[24:26] + ' (取值范围 0～15，0 表示无中继)')
            StrValue.append('第2相中继级别 = ' + data[26:28] + ' (取值范围 0～15，0 表示无中继)')
            StrValue.append('第3相中继级别 = ' + data[28:30] + ' (取值范围 0～15，0 表示无中继)')
            def getdata(data):
                AA = ''
                if data == '01':
                     AA = ' (初始状态)'
                     return AA
                elif   data == '02':
                    AA = ' (直抄)'
                    return AA
                elif data == '03':
                    AA = ' (中继)'
                    return AA
                elif data == '04':
                    AA = ' (监控状态)'
                    return AA
                elif data == '05':
                    AA = ' (广播状态)'
                    return AA
                elif data == '06':
                    AA = ' (广播召读电表)'
                    return AA
                elif data == '07':
                    AA = ' (读侦听信息)'
                    return AA
                elif data == '08':
                    AA = ' (空闲)'
                    return AA
                else:  AA = ' (备用)'
                return  AA
            StrValue.append('第1相工作步骤 = ' + data[30:32] + getdata(data[30:32]))
            StrValue.append('第2相工作步骤 = ' + data[32:34] + getdata(data[32:34]))
            StrValue.append('第3相工作步骤 = ' + data[34:36] + getdata(data[34:36]))
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '1000':
        if len(data) ==10:
            StrValue.append('从节点起始序号 =' + data[4:8])
            StrValue.append('从节点数量 =' + data[8:])
            return StrValue
        elif len(data)>=22:
            StrValue.append('从节点数量 =' + data[4:8])
            StrValue.append('本次应答的从节点数量 =' + data[8:10])
            for i in range(int(data[8:10])):
                 StrValue.append('从节点地址：' + data[10+16*i:22+16*i])
                 d = bin(data[23+16*i])
                 e = d.zfill(10)
                 f = d.replace('0b', '')
                 g=int(f[2:5])
                 h=''
                 for i in range(len(g)):
                     h=''.join(g)
                     StrValue.append('通信协议类型 =' + h + '（00H＝透明传输；01H＝DL/T645—1997；02H＝DL/T645—2007；03H＝DL—698；04H-FFH保留）')
                 if g[5]==1:
                    StrValue.append('相位 = C相')
                 if g[6]==1:
                   StrValue.append('相位 = B相')
                 if g[7] == 1:
                    StrValue.append('相位 = A相')
                 return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '2000':
        if len(data) >= 22:
            StrValue.append('从节点数量 =' + data[4:8])
            StrValue.append('本次应答的从节点数量 =' + data[8:10])
            for i in range(int(data[8:10])):
                StrValue.append('从节点地址 =' + data[10 + 16 * i:22 + 16 * i])
                d = bin(data[23 + 16 * i])
                e = d.zfill(10)
                f = d.replace('0b', '')
                g = int(f[2:5])
                h = ''
                for i in range(len(g)):
                    h = ''.join(g)
                    StrValue.append('通信协议类型 =' + h + '（00H＝透明传输；01H＝DL/T645—1997；02H＝DL/T645—2007；03H＝DL—698；04H-FFH保留）')
                if g[5] == 1:
                    StrValue.append('相位 = C相')
                if g[6] == 1:
                    StrValue.append('相位 = B相')
                if g[7] == 1:
                    StrValue.append('相位 = A相')
                return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '080C':  #F100查询网络规模
        if len(data)==8:
            StrValue.append('网络规模：' + data[4:])
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '100C':  #F100查询网络规模
        if len(data) >= 22:
            StrValue.append('从节点数量 =' + data[4:8])
            StrValue.append('本次应答的从节点数量 =' + data[8:10])
            for i in range(int(data[8:10])):
                StrValue.append('从节点地址 =' + data[10 + 22 * i:22 + 22 * i])
                d = bin(data[23 + 16 * i])
                e = d.zfill(10)
                f = d.replace('0b', '')
                g = int(f[2:5])
                h = ''
                for i in range(len(g)):
                    h = ''.join(g)
                    StrValue.append('通信协议类型 =' + h + '（00H＝透明传输；01H＝DL/T645—1997；02H＝DL/T645—2007；03H＝DL—698；04H-FFH保留）')
                if g[5] == 1:
                    StrValue.append('相位 =C相')
                if g[6] == 1:
                    StrValue.append('相位 = B相')
                if g[7] == 1:
                    StrValue.append('相位 = A相')
                StrValue.append('从节点软件版本信息：' + data[26 + 22 * i:32 + 22 * i])
                return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    else:
        return 'Cannot Parse The AFN: ' + data







def FieldParsing13762_AFN11a(data):
    StrValue = []
    if data[:4] == '0100':
        if len(data) >= 20:
            StrValue.append('从节点数量 =' + data[4:6])
            for i in range(int(data[4:6])):
                 StrValue.append('从节点地址 =' + data[6+14*i:18+14*i])
                 StrValue.append('从节点通信协议类型 =' + data[18+14*i:20+14*i])
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '0200':
        if len(data) >= 18:
            StrValue.append('从节点数量 =' + data[4:6])
            for i in range(int(data[4:6])):
                 StrValue.append('从节点地址 =' + data[6+12*i:18+12*i])
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '0400':
        if len(data) >= 8:
            StrValue.append('从节点地址 =' + data[4:16])
            StrValue.append('中继级别 =' + data[16:18])
            for i in range(int(data[16:18])):
                 StrValue.append('中继从节点地址 =' + data[18+12*i:30+12*i])
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '0800':
        if len(data) == 10:
            c = trans(data[5])
            StrValue.append('纠错编码 =' + data[4])
            StrValue.append('注册允许状态 =' + c[2] + '(1为允许，0为不允许)')
            StrValue.append('工作状态 =' + c[3] + '(1为路由学习，0为抄表)')
            a=reverse( data[6:])
            b=bin(a)
            b=b.zfill(18)
            b=b.replace('0b','')
            StrValue.append('速率单位标识 =' + b[0] + '(1为kbit/s，0为抄表bit/s)')
            StrValue.append('通信速率 =' + str(int(b[1:] ))+ '(1为kbit/s，0为抄表bit/s)')
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '1000':
        if len(data) == 24:
            StrValue.append('开始时间 =' + reverse(data[4:16]))
            StrValue.append('持续时间 =' + reverse(data[16:20]))
            StrValue.append('从节点重发次数 =' + reverse(data[20:22]))
            StrValue.append('随机等待时间个数 =' + reverse(data[22:24]))
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '2000':
        if len(data) == 4:
            return
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '080C':  #F100设置网络规模
        if len(data) == 8:
            StrValue.append('网络规模 =' + data[4:])
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '100C':  # F101启动网略维护进程
        if len(data) == 4:
            return
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '200C':  # F102启动组网
        if len(data) == 4:
            return
        else:
            return 'Cannot Parse The data: ' + data
    else:
        return 'Cannot Parse The AFN: ' + data





def FieldParsing13762_AFN12a(data):
    StrValue =[]
    if data[:4] == '0100':
        if len(data) == 4:
            StrValue.append('重启' )
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '0200':
        if len(data) == 4:
            StrValue.append('暂停' )
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '0400':
        if len(data) == 4:
            StrValue.append('恢复' )
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    else:
        return 'Cannot Parse The AFN: ' + data


def FieldParsing13762_AFN13a(data):
    StrValue=[]
    if data[:4] == '0100':
        if len(data) >= 12:
            StrValue.append('通信协议类型 ='+data[4:6] +'(00H＝透明传输；01H＝DL/T645—1997；02H＝DL/T645—2007；03H＝DL—698；04H-FFH保留)' )
            StrValue.append('通信延时标志 =' + data[6:8] + '(00H＝和通讯延时无关；01H和通讯延时有关')
            StrValue.append('从节点附属节点数量 =' + str(int(data[8:10] ,16)))
            if int(data[8:10])==0:
                StrValue.append('报文长度L =' + str(int(data[10:12],16)))
                StrValue.append('报文内容 =' + data[12:12+int(data[10:12],16)*2])
                return StrValue
            else:
                for i in range(int(data[8:10])):
                    StrValue.append('从节点附属节点地址 =' + data[10+12*i:22+12*i])
                    StrValue.append('报文长度L =' + data[22+12*i:22+12*i+2])
                    StrValue.append('报文内容 =' + data[22+12*i+2:])
                    return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    else:
          return 'Cannot Parse The AFN: ' + data


def FieldParsing13762_AFN13b(data):
    StrValue = []
    if data[:4] == '0100':
        if len(data) >= 12:
            StrValue.append('当前报文本地通讯上行时长 =' + str(int(reverse(data[4:8]))))
            StrValue.append('通信协议类型 =' + data[8:10]+ '(00H＝透明传输；01H＝DL/T645—1997；02H＝DL/T645—2007；03H＝DL—698；04H-FFH保留)')
            StrValue.append('报文长度L =' + str(int(data[10:12],16)))
            StrValue.append('报文内容 =' + data[12:12 + int(data[10:12], 16) * 2])
        return StrValue
    else:
        return 'Cannot Parse The data: ' + data


def FieldParsing13762_AFN14b(data):
    StrValue =[]
    if data[:4] == '0100':
        if  len(data) >= 10:
            StrValue.append ( '抄读标志：'+ data[4:6] + '(00H为抄读失败，L＝0，n=0；01H为抄读成功，L＝0，n=0；02H为可以抄读，L＞0，n≥0)')
            StrValue.append('通信延时相关性标志 =' + data[6:8] + '(00H 通信数据与通信延时无关，01H 通信数据与通信延时相关，仅当抄读标志位02H时，该信息有效)')
            StrValue.append('路由请求数据长度L =' + str(int(data[8:10],16)))
            StrValue.append('路由请求数据内容 =' + data[10:10+int(data[8:10],16)*2])
            StrValue.append('从节点附属节点数量 =' + data[10+int(data[8:10],16)*2:10+int(data[8:10],16)*2 +2] )
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    elif data[:4] == '0200':
        if len(data) == 16:
            StrValue.append('当前时间 =' + data[4:16])
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    elif data[:4] == '0400':
        if len(data) >= 6:
            StrValue.append('数据长度L =' + str(int(data[4:6]),16))
            StrValue.append('修正通信数据内容 =' + data[6:6+int(data[4:6],16)*2])
            return StrValue
        else:
            return 'Cannot Parse The data = ' + data
    else:
        return 'Cannot Parse The AFN = ' + data

def FieldParsing13762_AFN14a(data):
    StrValue =[]
    if data[:4] == '0100':
        if  len(data) == 22:
            if int(data[4:6],16)==1:
                StrValue.append('通讯相位 ='+ str(int(data[4:6],16)) + 'A相')
            elif int(data[4:6],16)==2:
                StrValue.append('通讯相位 ='+ str(int(data[4:6],16)) + 'B相')
            elif int(data[4:6],16)==3:
                StrValue.append('通讯相位 ='+ str(int(data[4:6],16)) + 'C相')
            else:
               StrValue.append('通讯相位 ='+ str(int(data[4:6],16)) + '相位未知')
            StrValue.append('从节点地址 ='+ reverse(data[6:18] ))
            StrValue.append('从节点序号 =' + str(int(reverse(data[18:22]))))
            return  StrValue
        else:
            return 'Cannot Parse The data: ' + data
    if data[:4] == '0200':
        if len(data)==4:
            return StrValue
        else:
            return 'Cannot Parse The data: ' + data
    if data[:4] == '0400':
        if len(data) >= 22:
            StrValue.append('从节点地址 =' + reverse(data[4:16]))
            StrValue.append('预计延时时间 =' + str(int(reverse(data[16:20])),16))
            StrValue.append('抄读信息长度L =' + str(int(data[20:22]), 16))
            StrValue.append('抄读数据内容 =' + data[22:])
            return StrValue
    else:
        return 'Cannot Parse The AFN: ' + data




def deal13762Frame(frame):
    l = [False]
    #if len(frame) < MIN_LEN_13762FRAME:
    #    return l
    frame = frame.upper()
    for i in range(0, len(frame), 2):
        if frame[i:i + 2] == '68':
            datalen=reverse(frame[(i + POS_13762_LEN):(i + POS_13762_LEN +4)])
            datalen1=(int(datalen,16)-0x05)*2
            framecs =frame[(i + POS_13762_CTRL):(i + POS_13762_CTRL +datalen1)]
            #if dataLen + POS_13762_LEN < len(frame):
            checkSum = calcCheckSum(framecs)
            checkSum = checkSum[-2:]
            checkSum = checkSum.upper()
            if checkSum == frame[i+POS_13762_CTRL + datalen1:i+POS_13762_CTRL + datalen1+2] and \
                                frame[i+POS_13762_CTRL + datalen1 + 2:i+POS_13762_CTRL + datalen1 + 4] == '16':
                    #addr = framecs[i + POS_64507_ADDR:i + POS_64507_ADDR + 12]
                    framedata  = frame[i:i+POS_13762_CTRL + datalen1 + 4 ]
                    ctrl = framecs[:2]
                    data = framecs[2:]
                    l[0] = True
                    l += [framedata ,ctrl,data]
                    return l
    return l

if __name__ == '__main__':
    frame = '68 13 00 83 00 00 00 00 00 00 10 01 00 00 00 E8 03 7F 16 '
    #6871000104010000002F000001000010130000000000140100020052685000430513000000000000360910002C0503085002020002202102001C07E204050800001C07E20405083B3B5401000F02002021020000200102000001109F2D36189B7CB449C363FE10A9FF573D87B516006816
    frame = frame.replace(' ', '')
#    frame = frame.replace('FE','')
    # print (frame)
    l = deal13762Frame(frame)
    if l[0]:
       ls = ana(l,l[-2],l[-1])
       for x in ls:
         print(x)



