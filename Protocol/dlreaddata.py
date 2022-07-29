# -*- coding: utf-8 -*-
import os
import logging
#导入需要使用的包
import datetime
import re
import xlwt
import win32api, win32con

snow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    filename=os.getcwd().replace("\Protocol", "") + '\log\\' + snow + 'ooptest.log', level=logging.INFO)
#能源稳定性代理成功率
ATAGENTSULIST = ['name','successrate']

def eventreportlist(eventlist):
    if eventlist != []:
        eventlist = eventlist.replace("]|[", '#').replace("[", '').replace(']', '').split(";")
    else:
        pass
    for eventlistnum in range(len(eventlist)):
        if eventlist[eventlistnum].find('"') >= 0 or eventlist[eventlistnum].find("'") >= 0:
            eventlist[eventlistnum] = eventlist[eventlistnum].replace('"', '').replace("'", '')
        else:
            pass
    return eventlist

#60120300召测回来的报文，按电表地址处理成一个列表的8个元素，且每个数据标识对应的值也处理好。
#例："'05203200011996';'20210628140000';'20210628140213';'20210628140000';['20210628140000'|1.34|0.06|[228.2|0.0|0.0]|[0.0|0.0|0.0]|[0.0|0.0|0.0|0.0]|[0.0|0.0|0.0|0.0]|[1.0|1.0|1.0|1.0]]
# ['05203200011996', ' 20210628140000', ' 20210628140213', ' 20210628140000', ' 20210628140000', ' 1.34', ' 0.06', ' 228.2|0.0|0.0', ' 0.0|0.0|0.0', ' 0.0|0.0|0.0|0.0', ' 0.0|0.0|0.0|0.0', ' 1.0|1.0|1.0|1.0']
#稳定性冻结召测和上报报文格式处理
def stabilityread(readlist,freezetype):
    testname = []
    #有分帧时，用来存储合并后的一定格式的分帧。
    framitemdata = ''
    ##分帧的特殊处理
    if readlist.find('\n') >= 0:
        readlist = readlist.split("\n")
        for framitem in readlist:
            framitemdata += framitem[3:][:-2] + "\'!\',"
        readlist = framitemdata[:-4]
        # readlist =  readlist.split("\n")[0][3:][:-2] + "\'!\',"+ readlist.split("\n")[1][3:][:-2] + "\'!\',"+ readlist.split("\n")[2][3:][:-2]
        readlist = readlist.split("\'!\',")
    else:
        if readlist != []:
            readlist = readlist.split("!")
        else:
            pass
    print(f'readlist:{readlist}')
    for num in range(len(readlist)):
        bb = readlist[num].replace("']|", '#').replace(",", '|').replace("|[", ';').split(';')
        for itemnum in range(len(bb)):
            if bb[itemnum].find(']|') >= 0:
                bb[itemnum] = bb[itemnum].split(']|')
                if bb[itemnum][-1].find('|') >= 0:
                    bb[itemnum][-1] = bb[itemnum][-1].split('|')
                else:pass
            elif bb[itemnum].find(']') >= 0:
                pass
            else:
                bb[itemnum] = bb[itemnum].split('|')
        print(bb)
        print(f'str(bb):{str(bb)}')
        cc = str(bb).replace("[", '').replace(']', '').split(',')
        for readlistnum in range(len(cc)):
            if cc[readlistnum].find('"') >= 0 or cc[readlistnum].find("'") >= 0 or cc[readlistnum].find("\\") >= 0 :
                cc[readlistnum] = cc[readlistnum].replace('"', '').replace("'", '').replace("\\", '')
            else:
                pass
        print(cc)
        readlist[num] = cc
    for namenum in range(len(readlist)):
        # 上报报文中，会因为！，多一个空的元素，直接删掉。已经有的测量点，不再重复添加。
         if readlist[namenum][0] == '':
             del readlist[namenum][0]
         # 分帧的特殊处理
         if len(readlist[namenum][0]) > 14:
             readlist[namenum][0] = readlist[namenum][0][-14:]
         else:pass
         if  freezetype == '50020200':
             if readlist[namenum][0][2:] + '分钟冻结' not in testname:
                testname.append(readlist[namenum][0][2:] + '分钟冻结')
         elif  freezetype == '50010200':
             if readlist[namenum][0][2:] + '秒冻结' not in testname:
                testname.append(readlist[namenum][0][2:]  + '秒冻结')
         elif  freezetype == '50040200':
             if readlist[namenum][0][2:] + '日冻结' not in testname:
                testname.append(readlist[namenum][0][2:]  + '日冻结')
         elif freezetype == '50050200':
             if readlist[namenum][0][2:] + '结算日冻结' not in testname:
                testname.append(readlist[namenum][0][2:]  + '结算日冻结')
         elif freezetype == '50060200':
             if readlist[namenum][0][2:] + '月冻结' not in testname:
                testname.append(readlist[namenum][0][2:]  + '月冻结')
         elif freezetype == '':
             if readlist[namenum][0][2:] + '实时数据' not in testname:
                testname.append(readlist[namenum][0][2:]  + '实时数据')
         elif freezetype == '50030200':
             if readlist[namenum][0][2:] + '小时冻结' not in testname:
                testname.append(readlist[namenum][0][2:]  + '小时冻结')
         elif freezetype == '32000200':
            testname.append('功控跳闸记录')
         elif freezetype == '32010200':
            testname.append('电控跳闸记录')
         elif freezetype == '32020200':
            testname.append('购电参数设置记录')
         elif freezetype == '32030200':
            testname.append('电控告警记录')
    print(f'testname:{testname}')
    return readlist,testname

#稳定性事件上报报文格式处理
def stabilityreport(eventlist,freezetype):
    testname = []
    #有分帧时，用来存储合并后的一定格式的分帧。
    eventlist = eventreportlist(eventlist)
    if freezetype == '32000200':
        testname.append('32000200功控跳闸记录')
    elif freezetype == '32010200':
        testname.append('32010200电控跳闸记录')
    elif freezetype == '32020200':
        testname.append('32020200购电参数设置记录')
    elif freezetype == '32030200':
        testname.append('32030200电控告警记录')
    elif freezetype == '31040200':
        testname.append('31040200遥信变位记录')
    elif freezetype == '31200200':
        testname.append('31200200回路巡检变位记录')
    print(f'testname:{testname}')
    return eventlist,testname


def selsheetnameget(sheetname,param):
    if "方法7" in param:
        sheetname = sheetname + '方法7'
    elif "方法8" in param:
        sheetname = sheetname + '方法8'
    elif "方法10" in param:
        sheetname = sheetname + '方法10'
    return sheetname


def chiname(strr):
    chi = r'[\u4e00-\u9fa5]'
    bb = re.findall(chi,strr)
    name = ''
    for item in bb:
        name += item
    return name

#百分比的形式比较的流程 预期值和真实值
def percentage(expect,real):
    errorresult=0
    if expect != 0:
        errorresult = float('%.4f' % (abs(expect - real) / abs(expect)))
    else:
        errorresult = real
    return errorresult

def selc_err(readdatalist):
    ex_plist = [72000,0,0,72000,72000000,72000000]
    cotrlerr = 0.01
    combb = readdatalist[1:]
    for num in range(len(combb)):
        err_p = percentage(ex_plist[num],int(combb[num]))
        if err_p > cotrlerr:
            return False
        else:
            pass
    return None

def saveasexcelagnet(temfile, tlist):
    wb = xlwt.Workbook()
    ws0 = wb.add_sheet('sheet')
    rowlist = ATAGENTSULIST
    for key in tlist:
        counter = 0
        y = 0
        for y in rowlist:
            try:
                ws0.write(key, counter, tlist[key][y])
            except:
                if isinstance(tlist[key][y], list):
                    strcuv = ''
                    for i in range(len(tlist[key][y])):
                        strcuv += str(tlist[key][y][i]) + '\n'
                    ws0.write(key, counter, strcuv)
            counter += 1
    wb.save(temfile)

def dealagentrate(sta_agent,name,num1,num2,stagentsusconfig):
    surate = '{:.2%}'.format((sta_agent[num2] - sta_agent[num1]) / sta_agent[num2])
    for itemrow in stagentsusconfig:
        if stagentsusconfig[itemrow]['name'] == name:
            stagentsusconfig[itemrow]['successrate'] = '代理总次数：' + str(sta_agent[num2]) + '；' + '失败次数：' + str(
                sta_agent[num1]) + '；' + '成功率' + surate
    return stagentsusconfig

#   #能源稳定性测试，用来处理代理成功率
def sta_succ_ratesave(sta_agent,tasklistrow,stagentsusconfig,reportfloderpath):
    if tasklistrow['expect'] == "FAIL_TIMES:0,485#07":
        stagentsusconfig = dealagentrate(sta_agent,'485#07',0,1,stagentsusconfig)
    elif tasklistrow['expect'] == "FAIL_TIMES:0,485#698":
        stagentsusconfig = dealagentrate(sta_agent,'485#698',2,3,stagentsusconfig)
    elif tasklistrow['save'] == "FAIL_TIMES:0,HPLC#单相07":
        stagentsusconfig = dealagentrate(sta_agent,'HPLC#单相07',4,5,stagentsusconfig)
    elif tasklistrow['save'] == "FAIL_TIMES:0,HPLC#单相698":
        stagentsusconfig = dealagentrate(sta_agent,'HPLC#单相698',6,7,stagentsusconfig)
    elif tasklistrow['save'] == "FAIL_TIMES:0,HPLC#三相07":
        stagentsusconfig = dealagentrate(sta_agent,'HPLC#三相07',8,9,stagentsusconfig)
    #稳定性代理6中不同类型，再最后代理时进行文件的保存就可以了。不用频繁的保存。且一天只存一个文件，每次打开看到的都是最新的数据。
    elif tasklistrow['save'] == "FAIL_TIMES:0,HPLC#三相698":
        stagentsusconfig = dealagentrate(sta_agent,'HPLC#三相698',10,11,stagentsusconfig)
        now = datetime.datetime.now()
        pathversion = reportfloderpath + '能源稳定性代理成功率' + now.strftime('%Y%m%d') + '.xls'
        saveasexcelagnet(pathversion, stagentsusconfig)
    else:pass
    return stagentsusconfig

#时段功控依据时段来获取对应时段的定值
def tc_convalue():
    aa = int((datetime.datetime.now().strftime('%Y%m%d%H%M%S'))[-6:-4])
    print(aa)
    if 0 <= aa < 3:
        return (3110000)
    elif 3 <= aa < 6:
        return (3120000)
    elif 6 <= aa < 9:
        return (3130000)
    elif 9 <= aa < 12:
        return (3140000)
    elif 12 <= aa < 15:
        return (3150000)
    elif 15 <= aa < 18:
        return (3160000)
    elif 18 <= aa < 21:
        return (3170000)
    elif 21 <= aa < 24:
        return (3180000)

def normalwaitotherdeal(tasklistrow,circle_start_flag):
    if tasklistrow['save'].find('POPUP') >= 0:
        win32api.MessageBox(0, "数据初始化已完成，请打脉冲，点击”确定“后继续测试", "提示", win32con.MB_OK)
        #在指定的流程，开始进行登录是否异常统计。因为用例一开始会进行数据初始化，无法判断是否真的通讯异常。等稳定好再进行统计。
    elif tasklistrow['save'].find('REGISTER') >= 0:
        circle_start_flag = 2
    elif tasklistrow['save'].find('DROP') >= 0:
        win32api.MessageBox(0, "请开始跌落测试，点击”确定“后继续测试", "提示", win32con.MB_OK)
        win32api.MessageBox(0, "请确认跌落测试已结束，点击”确定“后继续测试", "提示", win32con.MB_OK)
    elif tasklistrow['save'].find('P_START') >= 0:
        win32api.MessageBox(0, "参数配置已完成，请打脉冲（1HZ，1000个），点击”确定“后继续测试", "提示", win32con.MB_OK)
    elif tasklistrow['save'].find('STOP_I') >= 0:
        win32api.MessageBox(0, "请将电流降为0，点击”确定“后继续测试", "提示", win32con.MB_OK)
    else:
        print("增加等待后的其它特殊操作")
    return circle_start_flag


