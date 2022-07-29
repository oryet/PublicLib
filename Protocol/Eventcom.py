# -*- coding: utf-8 -*-
# import binascii
import datetime
import re
from dateutil.parser import parse
import logging
import os
import win32api, win32con


eventrecorddatalist = ['30000700','30000800','30000900','30150200','30010700','30010800','30010900','30020700','30020800','30020900','30030700','30030800','30030900','30040700','30040800','30040900','30050700','30050800','30050900','30060700','30060800','30060900','30070700','30070800','30070900','30080700','30080800','30080900','300B0600','300B0700','300B0800','300B0900','303B0700','303B0800','303B0900','301D0200','300C0200','30090200','300A0200','30130200','30140200','301E0200']
eventrecordindexlist = ['30000701','30000801','30000901']
event0A24list = ['30000A02','30000A03','30000A04','30010A02','30010A03','30010A04','30020A02','30020A03','30020A04','30030A02','30030A03','30030A04',
                 '30040A02', '30040A03', '30040A04', '30050A02', '30050A03', '30050A04', '30060A02', '30060A03',
                 '30060A04', '30070A02', '30070A03', '30070A04', '30080A02', '30080A03', '30080A04', '300B0A01','300B0A02', '300B0A03', '300B0A04', '303B0A02', '303B0A03', '303B0A04']
event0D24list = ['30000D00']
event0E24list = ['30000E02','30000E03','30000E04','30010E02','30010E03','30010E04','30020E02','30020E03','30020E04','30030E02','30030E03','30030E04',
                 '30040E02', '30040E03', '30040E04', '30050E02', '30050E03', '30050E04', '30060E02', '30060E03',
                 '30060E04', '30070E02', '30070E03', '30070E04', '30080E02', '30080E03', '30080E04', '300B0E02', '300B0E03', '300B0E04', '303B0E02', '303B0E03', '303B0E04']
event3015list = ['30150A00','301D0A00','300C0A00','30130A00','30140A00','301E0A00','30090A00','300A0A00']
event30000A00list = ['30000A00']
event30000E00list = ['30000E00','30040E00','30070E00','30080E00','300B0E00','303B0E00']
expectresetlist =  ['43000500','30000100','43000300']
event301D0700list = ['301D0700','300C0700','30130700','30140700','301E0700','30090700','300A0700']
#事件中需要比较的电能量和需量数据标识
eanddlist = ['00100200','00300200','10100200','10300200','00200200','00400200','10200200','10400200']
contrlist = ['32000201','32010201','32020201','32030201','31150201']

# 带[]字符串转换成list '[c,d,e]'->[c,d,e]
def strtolist(slist):
    lrtn = eval("%s" % slist)
    return lrtn
snow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    filename=os.getcwd().replace("\Protocol", "") + '\log\\' + snow + 'ooptest.log', level=logging.DEBUG)


# 通过预期值字符串获取要比较的时间，在列表中的存储位置。例如：RTU_TIME_1±120秒，说明存储在时间列表的第一个（list[0]）
def numget(expTime):
    restr = r'TIME_(.*?)±'
    strList = re.findall(restr, expTime)
    comtnum = int(strList[0])
    print('comtnum:', comtnum)
    return comtnum
#误差时间获取
def errorget(expTime):
    a = r'±(.*?)秒'
    slotList = re.findall(a, expTime)
    offset = int(slotList[0])
    return offset
#发生时间和等待时长存储顺序获取  '获取当前时间RTU_TIME_2' 添加在列表的第2个位置
def timenumget(expTime):
    a = r'\d'
    slotList = re.findall(a, expTime)
    num = int(slotList[0])
    return num

def waitget(waitrow,eventhappent):
    waitnum =  timenumget(waitrow['save'])
    eventhappent[waitnum - 1] = int(waitrow['delay'])
    return eventhappent



#比较事件发生和结束时刻函数
def judgeEventTime(expTime, realTime,eventbaet):
    print("expTime,realTime:",expTime,realTime)
    logging.info("预期时间："+ str(expTime))
    logging.info("实际时间参数代入：" + str(realTime))
    if (realTime == 'NULL') & (expTime == 'NULL'):
        print("期望时间和实际时间均为NULL")
        print("实际时间合理")
        return True
    elif (realTime != 'NULL') & (expTime == 'NULL'):
        print("期望时间为NULL，实际时间不为NULL")
        print("实际时间不合理")
        return False
    elif (realTime == 'NULL') & (expTime != 'NULL'):
        print("期望时间不为NULL，实际时间为NULL")
        print("实际时间不合理")
        return False
    realTime = parse(realTime)  # 字符串转成时间格式
    print("type:,startTimeReal:", type(realTime), realTime)
    comtnum = numget(expTime)
    nowTmn = eventbaet[int(comtnum) - 1]
    logging.info("预期时间程序获取：" +  nowTmn)
    nowTmn = parse(nowTmn)  # 字符串转成时间格式
    print('nowTmntype:,nowTmn:', type(nowTmn), nowTmn)
    offset = errorget(expTime)
    print("type:,slotList", type(offset), offset)
    delta = datetime.timedelta(seconds=offset)
    timeExp1 = nowTmn - delta
    timeExp2 = nowTmn + delta
    print("timeExp1:", timeExp1.strftime('%Y-%m-%d %H:%M:%S'))
    print("timeExp2:", timeExp2.strftime('%Y-%m-%d %H:%M:%S'))
    if (realTime >= timeExp1) & (realTime <= timeExp2):
        print("实际时间合理")
        return True
    else:
        print("实际时间不合理")
        return False
# judgeEventTime('RTU_TIME_1' ,'NULL',eventbaet)

def judgeEventDuration(expparam,realdata,eventhappent):
    eventduration = 0
    waitnum = ['_1','_2','_3','_4','_5','_6','_7','_8','_9']
    print("expparam,realdata:", expparam, realdata)
    logging.info("预期时间：" + str(expparam))
    logging.info("实际时间参数代入：" + str(realdata))
    if (realdata == 0) and (expparam == '0'):
        print("期望时长和实际时长均为0")
        print("实际时长合理")
        return True
    elif (realdata != 0) and (expparam == '0'):
        print("期望时长为0，实际时长不为0")
        print("实际时长不合理")
        return False
    elif (realdata == 0) and (expparam != '0'):
        print("期望时长不为0，实际时长为0")
        print("实际时长不合理")
        return False
    for itemnum in waitnum:
        if itemnum in expparam:
            eventduration += eventhappent[int(itemnum.strip('_')) - 1]
        else:pass
    logging.info("预期时长程序获取：" + str(eventduration))
    offset = errorget( expparam)
    if abs(realdata - eventduration) > offset:
        print("实际时长不合理")
        return  False
    else:
        print("实际时长合理")
        return True








def exandrealget(eventrow):
    eventrecorddata = []
    expectdata = eventrow['expect'].split(",")
    for itemdata in expectdata:
        eventrecorddata.append(itemdata.split("：")[1])
    print(eventrecorddata)
    realdatalist = strtolist(eventrow['real'])
    return eventrecorddata,realdatalist

def exandrealeventget(eventrow):
    eventrecorddata = []
    expectdata = eventrow['expect'].split(",")
    for itemdata in expectdata:
        if itemdata.find('：') >=0:
            eventrecorddata.append(itemdata.split("：")[1])
        else:
            eventrecorddata.append(itemdata)
    print(eventrecorddata)
    realdatalist = strtolist(eventrow['real'])
    return eventrecorddata,realdatalist
#需量和电能量走字后预期值存储
def eledemvsave(eventrow,edexpectlist):
    if eventrow['oad_omd'] == '00100200':
        edexpectlist[0] = eventrow['real']
    elif eventrow['oad_omd'] == '00300200':
        edexpectlist[1] = eventrow['real']
    elif eventrow['oad_omd'] == '10100200':
        edexpectlist[2] = eventrow['real']
    elif eventrow['oad_omd'] == '10300200':
        edexpectlist[3] = eventrow['real']
    elif eventrow['oad_omd'] == '00200200':
        edexpectlist[4] = eventrow['real']
    elif eventrow['oad_omd'] == '00400200':
        edexpectlist[5] = eventrow['real']
    elif eventrow['oad_omd'] == '10200200':
        edexpectlist[6] = eventrow['real']
    elif eventrow['oad_omd'] == '10400200':
        edexpectlist[7] = eventrow['real']
    else:print('增加其它比较标识')
    return edexpectlist

#需量和电能量某个事件发生后，剩余一个值未发生变化比较函数
def eledemvsamecom(eventrow,edexpectlist):
    if eventrow['oad_omd'] == '00100200':
        if edexpectlist[0] == eventrow['real']:
            return True
        else:
            return False
    elif eventrow['oad_omd'] == '00300200':
        if edexpectlist[1] == eventrow['real']:
            return True
        else:
            return False
    elif eventrow['oad_omd'] == '10100200':
        if edexpectlist[2] == eventrow['real']:
            return True
        else:
            return False
    elif eventrow['oad_omd'] == '10300200':
        if edexpectlist[3] == eventrow['real']:
            return True
        else:
            return False
    elif eventrow['oad_omd'] == '00200200':
        if edexpectlist[4] == eventrow['real']:
            return True
        else:
            return False
    elif eventrow['oad_omd'] == '00400200':
        if edexpectlist[5] == eventrow['real']:
            return True
        else:
            return False
    elif eventrow['oad_omd'] == '10200200':
        if edexpectlist[6] == eventrow['real']:
            return True
        else:
            return False
    elif eventrow['oad_omd'] == '10400200':
        if edexpectlist[7] == eventrow['real']:
            return True
        else:
            return False
    else:print('增加其它比较标识')
    return edexpectlist

#需量和电能量走字后，非0值判断
def eledemvcom(data,otype):
    if otype == '00':
        if strtolist(data)[0] > 0:
            return True
        else:
            return False
    elif otype == '10':
        if strtolist(data)[0][0] > 0:
            return True
        else:
            return False
    else:
        logging.info("事件电能量、需量走字后，比较流程出现异常")
        return False

#需量和电能量事件清零后，0值判断
def eledemv0com(data,otype):
    if otype == '00':
        if strtolist(data)[0] == 0:
            return True
        else:
            return False
    elif otype == '10':
        if strtolist(data)[0][0] == 0:
            return True
        else:
            return False
    else:
        logging.info("事件清零后，比较流程出现异常")
        return False

#需量和电能量清零事件比较流程。封装成一个函数
def eleanddemcom(edexpectlist,eventrow):
    if eventrow['save'].find('EXPECT_VALUE') >= 0:
        edexpectlist = eledemvsave(eventrow,edexpectlist)
    if eventrow['save'].find('VALUABLE') >= 0:
        if eledemvcom(eventrow['real'],eventrow['oad_omd'][:2]):
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
    if eventrow['expect'].find('VALUE_0') >= 0:
        if eledemv0com(eventrow['real'],eventrow['oad_omd'][:2]):
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
    if eventrow['expect'].find('EXPECT_VALUE') >= 0:
        if eledemvsamecom(eventrow,edexpectlist):
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
    return None

#控制用例比较功控跳闸记录时的比较流程
def contr3200event(eventrecorddata,realdatalist,eventbaet,eventrow):
    flag = 0
    if (judgeEventTime(eventrecorddata[1], realdatalist[1], eventbaet)) and (
            judgeEventTime(eventrecorddata[2], realdatalist[2], eventbaet)):
        pass
    else:
        flag = 1
    if (eventrecorddata[3] == realdatalist[3]) and (eventrecorddata[6] == realdatalist[6])and(eventrecorddata[7] == realdatalist[7])and(float(eventrecorddata[8]) == float(realdatalist[8]))and(float(eventrecorddata[9]) == float(realdatalist[9])) and(float(eventrecorddata[5]) == float(realdatalist[5])):
        pass
    else:
        flag =1
    if flag == 1:
        eventrow['result'] = '不合格'
    else:
        eventrow['result'] = '合格'
    return None

#控制用例比较功控跳闸记录时的比较流程
def contr3201event(eventrecorddata,realdatalist,eventbaet,eventrow):
    flag = 0
    if (judgeEventTime(eventrecorddata[1], realdatalist[1], eventbaet)) and (
            judgeEventTime(eventrecorddata[2], realdatalist[2], eventbaet)):
        pass
    else:
        flag = 1
    if (eventrecorddata[3] == realdatalist[3]) and (eventrecorddata[6] == realdatalist[6])and(float(eventrecorddata[7]) == float(realdatalist[7]))and(float(eventrecorddata[8]) == float(realdatalist[8]))and(int(eventrecorddata[0]) == int(realdatalist[0])) and(eventrecorddata[5] == realdatalist[5]):
        pass
    else:
        flag =1
    if flag == 1:
        eventrow['result'] = '不合格'
    else:
        eventrow['result'] = '合格'
    return None
#控制用例比较功控跳闸记录时的比较流程
def contr3202event(eventrecorddata,realdatalist,eventbaet,eventrow):
    flag = 0
    if (judgeEventTime(eventrecorddata[1], realdatalist[1], eventbaet)) and (
            judgeEventTime(eventrecorddata[2], realdatalist[2], eventbaet)):
        pass
    else:
        flag = 1
    if (eventrecorddata[3] == realdatalist[3]) and (int(eventrecorddata[0]) == int(realdatalist[0])):
        pass
    else:
        flag =1
    if flag == 1:
        eventrow['result'] = '不合格'
    else:
        eventrow['result'] = '合格'
    return None
#控制用例比较功控跳闸记录时的比较流程
def contr3203event(eventrecorddata,realdatalist,eventbaet,eventrow):
    flag = 0
    if (judgeEventTime(eventrecorddata[1], realdatalist[1], eventbaet)) and (
            judgeEventTime(eventrecorddata[2], realdatalist[2], eventbaet)):
        pass
    else:
        flag = 1
    if (int(eventrecorddata[0]) == int(realdatalist[0])) and(eventrecorddata[3] == realdatalist[3]) and (eventrecorddata[5] == realdatalist[5]) and(float(eventrecorddata[6]) == float(realdatalist[6])):
        pass
    else:
        flag =1
    if flag == 1:
        eventrow['result'] = '不合格'
    else:
        eventrow['result'] = '合格'
    return None

#控制用例比较遥控跳闸记录时的比较流程
def contr3115event(eventrecorddata,realdatalist,eventbaet,eventrow):
    flag = 0
    if (judgeEventTime(eventrecorddata[1], realdatalist[1], eventbaet)) and (
            judgeEventTime(eventrecorddata[2], realdatalist[2], eventbaet)):
        pass
    else:
        flag = 1
    if (int(eventrecorddata[0]) == int(realdatalist[0])) and(eventrecorddata[3] == realdatalist[3]) :
        pass
    else:
        flag =1
    if flag == 1:
        eventrow['result'] = '不合格'
    else:
        eventrow['result'] = '合格'
    return None

def losetimeget(eventrow):
    losetimes = 0
    #计算事件发生次数，如果结果回对象不存在，就说明没有事件产生，就是合格的。
    if eventrow['real'] == '对象不存在':
        eventrow['result'] = '合格'
    else:
        eventrow['result'] = '不合格'
        nn = strtolist(eventrow['real'])
        #准备工作中检查扩展模块是否在线，如不在线，弹窗提示，若点击了“是”，将结果改为合格，避免再次弹窗。
        if eventrow['save'].find('NOT_COUNT') >= 0:
            if win32api.MessageBox(0, '请检查扩展模块电源接线和485接线，确认无误后，点击“是”继续测试。', "警告", win32con.MB_YESNO) == 6:
                pass
                eventrow['result'] = '合格'
            else:
                os._exit(0)
        else:
            for item in nn:
                if item[3] == 3:
                    losetimes += 1
    return losetimes


#功率反向用例，只考察分相；潮流反向，只考察总。
def eventresultdeal(eventrow, rtu_current_time,eventbaet,eventhappent,edexpectlist,checktrueflag):
    losetimes = ''
    if eventrow['param'].find("RTU_TIME_") >= 0:
        eventbaet[timenumget(eventrow['param']) - 1] = rtu_current_time
        print('eventbaet:',eventbaet)
    eventrecorddata = []
    #例如：30000700
    if eventrow['oad_omd'] in eventrecorddatalist:
        print(eventrow['expect'])
        eventrecorddata,realdatalist = exandrealget(eventrow)
        if (realdatalist[0][0] == int(eventrecorddata[0])) and  (judgeEventTime(eventrecorddata[1] ,realdatalist[0][1],eventbaet))  and (judgeEventTime(eventrecorddata[2] ,realdatalist[0][2],eventbaet)):
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
    # 例如：30000701
    elif eventrow['oad_omd'] in eventrecordindexlist:
        print(eventrow['expect'])
        eventrecorddata,realdatalist = exandrealget(eventrow)
        if (realdatalist[0] == int(eventrecorddata[0])) and  (judgeEventTime(eventrecorddata[1] ,realdatalist[1],eventbaet))  and (judgeEventTime(eventrecorddata[2] ,realdatalist[2],eventbaet)):
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
    elif eventrow['oad_omd'] in event0A24list:
        eventrecorddata, realdatalist = exandrealget(eventrow)
        if (realdatalist[0] == int(eventrecorddata[0])) and (judgeEventDuration(eventrecorddata[1], realdatalist[1],eventhappent)):
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
    elif eventrow['oad_omd'] in event3015list:
        eventrecorddata, realdatalist = exandrealget(eventrow)
        if (judgeEventTime(eventrecorddata[0], realdatalist[0][1][0],eventbaet)) and (judgeEventTime(eventrecorddata[1], realdatalist[0][1][1],eventbaet)):
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
    elif eventrow['oad_omd'] in event0D24list:
        eventrecorddata, realdatalist = exandrealget(eventrow)
        if (realdatalist[0] == int(eventrecorddata[0])) and (judgeEventDuration(eventrecorddata[1], realdatalist[1],eventhappent))and (judgeEventTime(eventrecorddata[2] ,realdatalist[2],eventbaet))  and (judgeEventTime(eventrecorddata[3] ,realdatalist[3],eventbaet)):
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
    elif eventrow['oad_omd'] in event0E24list:
        eventrecorddata, realdatalist = exandrealget(eventrow)
        if (judgeEventTime(eventrecorddata[0] ,realdatalist[0],eventbaet))  and (judgeEventTime(eventrecorddata[1] ,realdatalist[1],eventbaet)):
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
    elif eventrow['oad_omd'] in event30000E00list:
        eventrecorddata, realdatalist = exandrealget(eventrow)
        if (judgeEventTime(eventrecorddata[0], realdatalist[0][0], eventbaet)) and (
        judgeEventTime(eventrecorddata[1], realdatalist[0][1], eventbaet)) and (judgeEventTime(eventrecorddata[2], realdatalist[1][0], eventbaet)) and (
        judgeEventTime(eventrecorddata[3], realdatalist[1][1], eventbaet)) and(judgeEventTime(eventrecorddata[4], realdatalist[2][0], eventbaet)) and (
        judgeEventTime(eventrecorddata[5], realdatalist[2][1], eventbaet)) and (judgeEventTime(eventrecorddata[6], realdatalist[3][0], eventbaet)) and (
        judgeEventTime(eventrecorddata[7], realdatalist[3][1], eventbaet)):
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
    elif eventrow['oad_omd'] in event30000A00list:
        eventrecorddata, realdatalist = exandrealget(eventrow)
        if (realdatalist[0][0] == int(eventrecorddata[0]))  and (judgeEventDuration(eventrecorddata[1], realdatalist[0][1],eventhappent)) and (realdatalist[1][0] == int(eventrecorddata[2]))  and (judgeEventDuration(eventrecorddata[3], realdatalist[1][1],eventhappent)) and (realdatalist[2][0] == int(eventrecorddata[4]))  and (judgeEventDuration(eventrecorddata[5], realdatalist[2][1],eventhappent)) and (realdatalist[3][0] == int(eventrecorddata[6]))  and (judgeEventDuration(eventrecorddata[7], realdatalist[3][1],eventhappent)):
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
    #接下来处理7类的
    elif  eventrow['oad_omd'] in event301D0700list:
        eventrecorddata, realdatalist = exandrealget(eventrow)
        if (realdatalist[0][1][0] == int(eventrecorddata[0])) and (
        judgeEventDuration(eventrecorddata[1], realdatalist[0][1][1], eventhappent)):
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
            #功率反向，不考察总
    elif eventrow['oad_omd'] == '30070300':
        print('eventrow[e][2:]:',eventrow['expect'][2:])
        print('eventrow[real][2:]:', eventrow['real'][2:])

        if eventrow['expect'][2:] == eventrow['real'][2:]:
            eventrow['result'] = '合格'
        else:
            eventrow['result'] = '不合格'
            #要比较需量和电量的数据标识
    elif eventrow['oad_omd'] in  eanddlist:
        eleanddemcom(edexpectlist, eventrow)
        #默认参数正确，不再执行下面的参数配置和检查流程
    elif eventrow['save'].find('DEF_PARAM') >= 0:
        if eventrow['result'] == '合格':
            checktrueflag = 1
        else:
            checktrueflag = 0
        eventrow['result'] = '合格'
    elif eventrow['oad_omd'] in contrlist:
        eventrecorddata, realdatalist = exandrealeventget(eventrow)
        if eventrow['oad_omd'] == '32000201':
            contr3200event(eventrecorddata,realdatalist,eventbaet,eventrow)
        elif eventrow['oad_omd'] == '32010201':
            contr3201event(eventrecorddata,realdatalist,eventbaet,eventrow)
        elif eventrow['oad_omd'] == '32020201':
            contr3202event(eventrecorddata,realdatalist,eventbaet,eventrow)
        elif eventrow['oad_omd'] == '32030201':
            contr3203event(eventrecorddata,realdatalist,eventbaet,eventrow)
        elif eventrow['oad_omd'] == '31150201':
            contr3115event(eventrecorddata,realdatalist,eventbaet,eventrow)
    elif eventrow['oad_omd'] == '310A0200':
        losetimes = losetimeget(eventrow)
        print('losetimes:',losetimes)
    logging.info('发生时间预期值列表：'+str(eventbaet))
    logging.info('发生时长预期值列表：'+str(eventhappent))
    return eventbaet,eventhappent,edexpectlist,checktrueflag,losetimes



