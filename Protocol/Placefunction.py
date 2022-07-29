# -*- coding: utf-8 -*-
import xlrd
import time
import os
import re
import datetime
import arrow
import logging
snow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    filename=os.getcwd().replace("\Protocol", "") + '\log\\' + snow + 'ooptest.log', level=logging.DEBUG)

PLACEROWLIST = ['name', 'onemin','fifmin', 'hour', 'day', 'month', 'typefour', 'typethree','typeseven','settypefour', 'settypethree']
EX2940PARAMLIST = ['name','param']
MONFREZELIST = ['00010001','00010101','00010201','00010301','00010401','00020001','00020101','00020201','00020301','00020401','00050001','00050101','00050201','00050301','00050401']

# 等待
def wait(ldata):
    try:
        if isinstance(ldata, float):
            idelay = ldata
        else:
            idelay = float(ldata.encode('utf-8'))
        time.sleep(idelay)
    except ValueError:
        return False
    return True



# 检查配置文件etype oop mrtu
def readexcel(lfile, sname, etype):
    workbook = xlrd.open_workbook(lfile)
    rtem = {}
    for ns in workbook.sheet_names():
        sheet2 = workbook.sheet_by_name(ns)
        if ns == sname:
            for ir in range(0, sheet2.nrows):  # excel行数循环
                rowvalue = {}
                y = 0
                if etype == 'placecon':
                    rowlist = PLACEROWLIST
                    seq = 0
                    for y in rowlist:
                        rowvalue[y] = sheet2.cell(ir, seq).value
                        if (isinstance(rowvalue[y], float)):
                            rowvalue[y] = (xlrd.xldate.xldate_as_datetime(sheet2.cell(ir, seq).value, 0)).strftime("%Y%m%d%H%M%S")
                        seq += 1
                    rtem[ir] = rowvalue
                elif etype == '2940con':
                    rowlist = EX2940PARAMLIST
                    seq = 0
                    for y in rowlist:
                        rowvalue[y] = sheet2.cell(ir, seq).value
                        seq += 1
                    rtem[ir] = rowvalue
                else:
                    print('增加表格列类型')
    return rtem
# 带[]字符串转换成list '[c,d,e]'->[c,d,e]
def strtolist(slist):
    lrtn = eval("%s" % slist)
    return lrtn
def testconfig():
    tasklist = {}
    testpath = os.getcwd() + "\config\place_config"
    tasklist = readexcel(testpath + '/' + '参数配置表' + '.xlsx','时间参数', 'placecon')
    return tasklist

#通过参数配置表中的分钟召测次数（1分钟）来确认分钟对时后的等待时间。
def seconget(freztype,colname):
    nums = 0
    tasklist = testconfig()
    for item in tasklist:
        if (tasklist[item][colname] != freztype) and (tasklist[item][colname] != ''):
            nums += 1
        if (tasklist[item][colname] == '') and ( nums >0):
            break
    if freztype == '1分钟数据':
        nums = (nums+2) * 60
    return nums

def ex2940tsaad():
    add8way = '000000000001'
    add16way = '000000000002'
    testpath = os.getcwd() + "\config"
    configlist = readexcel(testpath + '/' + '扩展模块测试工装' + '.xlsx','参数定值', '2940con')
    for item in configlist:
        if configlist[item]['name'].find('工装1地址') >= 0:
            add8way = configlist[item]['param']
        if configlist[item]['name'].find('工装2地址') >= 0:
            add16way = configlist[item]['param']
    return [add8way,add16way]


def waitspecial(rowdelay):
    try:
        waittime = float(rowdelay)
        wait(waittime)
    except:
        if rowdelay.find('FROM_CON') >= 0:
            waittime = seconget('1分钟数据','onemin')
            print(f">>>>| 延时等待 {waittime} 秒")
            wait(float(waittime))
        else:
            print('增加其它等待的特殊操作')

def repeattrow(testrow,testrownum,tasklist,nrowcir,repeattimes,paramoldlist):
    repeattimes = repeattimecal(testrow)
    while tasklist[testrownum]['save'].find('CIR') >= 0:
        nrowcir += 1
        paramoldlist.append(tasklist[testrownum]['param'])
        testrownum += 1
    return repeattimes,nrowcir,paramoldlist

#需要循环测试的行，做了特殊处理
def ciritemdeal(trytimesflag,comtrytimes,repeattimes,repeatnow,nrowcir,testrownow,item,tryflag,paramfreezelist):
    if (trytimesflag == 1) or (comtrytimes == 1) or ((repeattimes > repeatnow) and (nrowcir == 0)):
        comtrytimes = 0
        tryflag = 1
    elif (testrownow == nrowcir) and (repeattimes > repeatnow + 1)and(nrowcir >0):
        item = item - (nrowcir - 1)
        repeatnow += 1
        testrownow = 0
    else:
        item += 1
        tryflag = 0
        if (nrowcir == 0) or ((repeattimes == repeatnow + 1) and(nrowcir >0) and (testrownow == nrowcir)):
            repeattimes = 0
            repeatnow = 0
            testrownow = 0
            nrowcir = 0
            paramfreezelist = []
    return item,comtrytimes,tryflag,repeatnow,testrownow,repeattimes,nrowcir,paramfreezelist


def repeattimecal(testrow):
    repeattimes = 0
    nums = testrow['save'].split(":")[1]
    if nums == 'FROM_CON_FIFMIN':
        repeattimes = seconget('15分钟数据','fifmin')
    elif nums == 'FROM_CON_HOUR':
        repeattimes = seconget('1小时数据', 'hour')
    elif nums == 'FROM_CON_DAY':
        repeattimes = seconget('日数据', 'day')
    elif nums == 'FROM_CON_MONTH':
        repeattimes = seconget('月数据', 'month')
    elif nums.find('FROM_CON') <= 0:
        repeattimes = int(nums)
    return repeattimes - 1
# 20191126 00 01 42 0000->   datetime
def bcdtodatetime(dt):
    if dt.find('-') >= 0:
        dt = dt.replace('-','').replace(' ','').replace(':','')
    dt.zfill(14)
    if len(dt) == 14:
        dt += '0000'
    tt = datetime.datetime(int(dt[0:4]), int(dt[4:6]), int(dt[6:8]), int(dt[8:10]),
                           int(dt[10:12]), int(dt[12:14]), int(dt[14:])*1000%1000000)
    return tt


def timeparamsp(timeparamrow,rtu_current_time):
    if timeparamrow['param'].find('任务延时5分钟') >= 0:
        timeparamrow['param'] = rtu_current_time[:-4] + '0455'
    elif timeparamrow['param'].find('任务延时10分钟') >= 0:
        timeparamrow['param'] = rtu_current_time[:-4] + '0955'
    elif timeparamrow['param'].find('任务延时15分钟') >= 0:
        timeparamrow['param'] = rtu_current_time[:-4] + '1455'
    return None

def param6012deal(paramcall):
    param = "[" + paramcall + "]"
    return param

def dealtime(paramreal,timestart,freezetype):
    #此函数需要处理：召测的起始和结束时间
    timeend = '20000101000000'
    paramreal = strtolist('[' + paramreal + ']')
    print('表格起始时间：',paramreal[0][1][0],paramreal[0][1][1])
    print('真实起始时间：',timestart)
    if (freezetype == '日冻结循环召测参数列表') or (freezetype == '分钟_1日冻结循环召测参数列表') :
        timeend = timeintervel(timestart,1,0,0)
    elif (freezetype == '月冻结循环召测参数列表') or (freezetype == '结算日冻结循环召测参数列表'):
        timeend = timeintervelmon(timestart,1)
    elif (freezetype == '分钟_1冻结循环召测参数列表') or (freezetype == '秒冻结_60冻结循环召测参数列表') or (freezetype == '秒冻结_1分冻结循环召测参数列表') :
        timeend = timeintervel(timestart,0,0,1)
    elif freezetype == '分钟_15冻结循环召测参数列表':
        timeend = timeintervel(timestart,0,0,15)
    elif (freezetype == '分钟_60冻结循环召测参数列表') or (freezetype == '小时_1冻结循环召测参数列表'):
        timeend = timeintervel(timestart,0,1,0)
    else:
        print('增加其他召测结束时间处理流程')
    paramreal[0][1][0] = timestart
    paramreal[0][1][1] = timeend
    return str(paramreal)[:-1][1:]

def timeexget(colname,savefortime,tasklist):
    timelist = []
    for item in tasklist:
        if (tasklist[item][colname] != savefortime) and (tasklist[item][colname] != ''):
            timelist.append(tasklist[item][colname])
        if (tasklist[item][colname] == '') and (len(timelist) > 0):
            break
    return timelist

#日、月、结算日根据不同的存储方式来确定召测起始时间；分钟小时不需要通过存储类型来判断
def timelistchose(freezetype,savetype,paramreal):
    tasklist = testconfig()
    timelist = []
    if (freezetype == '日冻结循环召测参数列表') or (freezetype == '分钟_1日冻结循环召测参数列表'):
        #选择方法8时，固定采用“日数据”列召测时间
        if (paramreal.find('选择方法8') >= 0) and (freezetype != '分钟_1日冻结循环召测参数列表'):
            timelist = timeexget('day', '日数据', tasklist)
        elif savetype == '3':
            timelist = timeexget('typethree','3:相对上日23点59',tasklist)
        elif savetype == '4':
            timelist = timeexget('typefour', '4:相对上日0点0分', tasklist)
        else:
            #分钟——1日：过一日就可以了，不需要对时那么多天，也不用召测那么多天
            if freezetype == '分钟_1日冻结循环召测参数列表':
                timelist = timeexget('day', '日数据', tasklist)
                timelist = [timelist[0]]
            else:
                timelist = timeexget('day', '日数据', tasklist)
    #结算日和月冻结处理成一样的
    elif (freezetype == '月冻结循环召测参数列表') or (freezetype == '结算日冻结循环召测参数列表'):
        if (paramreal.find('选择方法8') >= 0):
            timelist = timeexget('month', '月数据', tasklist)
        else:
            if savetype == '7':
                timelist = timeexget('typeseven','7:相对上月月末23点59分',tasklist)
            else:
                timelist = timeexget('month', '月数据', tasklist)
            if freezetype == '结算日冻结循环召测参数列表':
                if savetype == '3':
                    timelist = timeexget('settypethree', '结算日3:相对上日23点59', tasklist)
                elif savetype == '4':
                    timelist = timeexget('settypefour', '结算日4:相对上日0点0分', tasklist)
    elif (freezetype == '分钟_1冻结循环召测参数列表') or (freezetype == '秒冻结_60冻结循环召测参数列表') or (freezetype == '秒冻结_1分冻结循环召测参数列表'):
        timelist = timeexget('onemin', '1分钟数据', tasklist)
    elif (freezetype == '分钟_15冻结循环召测参数列表'):
        timelist = timeexget('fifmin', '15分钟数据', tasklist)
    elif (freezetype == '分钟_60冻结循环召测参数列表') or (freezetype == '小时_1冻结循环召测参数列表'):
        timelist = timeexget('hour', '1小时数据', tasklist)

    print('timelist:',timelist)
    return timelist

def timeintervel(oldtime,intervelday,intervelhour,intervelmin):
    dt = bcdtodatetime(oldtime)
    delta = datetime.timedelta(days=intervelday,hours=intervelhour,minutes=intervelmin)
    timeadd = (str(dt + delta).replace('-', '').replace(" ", '').replace(":", ''))
    return timeadd

#构建arrow对象：strtime：'20200101000000'
def bulidarrowobject(strtime):
    arrowobject=arrow.Arrow(int(strtime[:4]), int(strtime[4:6]),
                int(strtime[6:8]), int(strtime[8:10]),
                int(strtime[10:12]), int(strtime[12:14]))
    return arrowobject

def timeintervelmon(timestart,intervelmonth):
    nowmonthtime = bulidarrowobject(timestart)
    nextmonth = nowmonthtime.shift(months = intervelmonth).format("YYYYMMDDHHmmSS")
    return nextmonth





#eachparam：['选择方法7',['20200229000000','20200229235900','1日','一组用户类型,[16]',]],['202A0200','60400200','60410200','60420200','50040200',['20210200','00100200','00110200','00120200','00130200','00200200','00210200','00220200','00230200','00300200','00400200',],'50040200',['00500200','00600200','00700200','00800200','10100200','10200200','21310201','21320201','21330201',],]:3####------:3代表的是存储类型，从excelchange中获取到的。
def calltime(paramfreezelist,freezetype,palannumlist):
    paramlist = []
    palannumlist = []
    #方法10不需要去处理召测时间，不用每个参数都去遍历召测起始时间。直接召测上一条即可。
    if freezetype == '实时_方法10循环召测参数列表':
        # paramlist = paramfreezelist
        for eachparam in paramfreezelist:
            savetype = eachparam.split(":")[1]
            paramreal = eachparam.split(":")[0]
            plannum = eachparam.split(":")[2]
            palannumlist.append(plannum)
            paramlist.append(paramreal)
    else:
        #存储类型对应的召测起始时间列
        timelist = ''
        configtimelist = testconfig()
        #存储类型
        savetype = 0
        #去掉存储类型后，真正的参数格式
        paramreal = ''
        for eachparam in paramfreezelist:
            savetype = eachparam.split(":")[1]
            paramreal = eachparam.split(":")[0]
            plannum = eachparam.split(":")[2]
            timelist = timelistchose(freezetype,savetype,paramreal)
            for itemnum in range(len(timelist)):
                paramlist.append(dealtime(paramreal,timelist[itemnum],freezetype))
                palannumlist.append(plannum)
        print('最终生成的可循环召测的paramlist:',paramlist)
    return len(paramlist),paramlist,palannumlist

#不比ID
def result2940(ldata):
    ldata['real'] = ldata['real'].split(':')[1]
    if  ldata['oad_omd'] == '0000':
        realdata = strtolist(ldata['real'])
        expectdat =  strtolist(ldata['expect'])
        for itemnum in range(len(expectdat)):
            if itemnum == 1:
                pass
            else:
                if expectdat[itemnum] == realdata[itemnum]:
                    ldata['result'] = '合格'
                else:
                    ldata['result'] = '不合格'
                    break
    return None

#漏电流比较时，上下限的获取
def calfromparam(rowdata):
    idata = rowdata['param'].split('<漏电流<')
    imax = idata[1]
    imin = idata[0]
    return float(imax),float(imin)

def fujianjcdatadeal(parameow698,fujianjcdata):
    #分三行召测，第一行时需要清空数数；第三行时，需要将有功功率总剔除。
    if parameow698['save'].find('start') >= 0:
        fujianjcdata = []
        fujianjcdata.extend(parameow698['real'].split(','))
    elif parameow698['save'].find('end') >= 0:
        datalist = parameow698['real'].split(',')
        del datalist[0]
        fujianjcdata.extend(datalist)
    else:
        fujianjcdata.extend(parameow698['real'].split(','))
    print('fujianjcdata:', fujianjcdata)
    return fujianjcdata


def deal2940con(parameow698):
    if (parameow698['oad_omd'] == 'FF140200'):
        Idatare = []
        Idataex = []
        imax = 0
        imin =0
        reflag = 0
        expectdata = strtolist(parameow698['expect'])
        realdata = strtolist(parameow698['real'])
        for num in range(len(expectdata)):
            Idatare.append(realdata[num][3])
            Idataex.append(expectdata[num][3])
            del expectdata[num][3]
            del realdata[num][3]
        if expectdata != realdata:
            reflag = 1
            logging.info("FF140200出现状态异常")
        #工装初始化（全部合闸）判漏电流
        if (parameow698['save'].find('CAL_I') >= 0):
            imax, imin = calfromparam(parameow698)
            for itemnum in range(len(Idataex)):
                if Idataex[itemnum] == 0 :
                    if Idatare[itemnum] != 0:
                        reflag = 1
                        logging.info("漏电流应为0的路，漏电流不为0了")
                        break
                else:
                    if (Idatare[itemnum] >imax) or (Idatare[itemnum] < imin):
                        reflag = 1
                        logging.info("漏电流超出预期范围")
                        break
        if reflag == 1:
            parameow698['result'] = '不合格'
        else:
            parameow698['result'] = '合格'
    elif parameow698['oad_omd'] == 'F2050200':
        exrtu = strtolist(parameow698['expect'])
        reartu = strtolist(parameow698['real'])
        if exrtu[:4] == reartu[:4]:
            parameow698['result'] = '合格'
        else:
            logging.info("终端分闸开关状态异常")
            parameow698['result'] = '不合格'
    elif parameow698['oad_omd'] == 'FF140300':
        Idatare = []
        Idataex = []
        imax = 400
        imin = 200
        reflag = 0
        expectdata = strtolist(parameow698['expect'])
        realdata = strtolist(parameow698['real'])
        for num in range(len(expectdata)):
            Idatare.append(realdata[num][1])
            Idataex.append(expectdata[num][1])
            del expectdata[num][1]
            del realdata[num][1]
        if expectdata != realdata:
            reflag = 1
            logging.info("FF140300名称错误")
        for itemnum in range(len(Idataex)):
            if Idataex[itemnum] == 0:
                if Idatare[itemnum] != 0:
                    reflag = 1
                    logging.info("脉宽应为0的路，漏不为0了")
                    break
            else:
                if (Idatare[itemnum] > imax) or (Idatare[itemnum] < imin):
                    reflag = 1
                    logging.info("脉宽超出预期范围")
                    break
        if reflag == 1:
            parameow698['result'] = '不合格'
        else:
            parameow698['result'] = '合格'
    return None
#多行一起循环时，虚拟表走字时间处理。（走字规律：表号+时间）
def elecharg(ldata,initime,repeatnow):
    #先处理走字的时间依据
    if ldata['save'].find('INITIME') >= 0:
        initime = ldata['param']
        timerun = initime
    else:
        if ldata['save'].find('_DAY') >= 0:
            timerun = timeintervel(initime, repeatnow + 1, 0, 0)
        if ldata['save'].find('_MONTH') >= 0:
            timerun = timeintervelmon(initime, repeatnow + 1)
    print('timerun:', timerun)
    return initime, timerun




#走字走：05060001,05060101,05060201,05060501----（上1次）日冻结时标、正向有功、反向有功、第一象限无功.一次测试中，取首次的月和日，以后走一次字，数值就加1.无论日月，保证用例往后对时的情况下，虚拟表不发生倒走。
def rundata(itemoad,ldata,timerun,vmstardata):
    if itemoad in ['05060001','05060002','05060003'] :
        d =  timerun[2:]
    #这里先给出走字的十位和个位，是依据电表冻结时间给出的。日冻结取日期中的日，结算日冻结\月冻结去日期中的月
    elif (itemoad in ['05060101','05060201','05060501']) and (ldata['save'].find('_DAY') >= 0):
        if vmstardata == 0:
            d= timerun[4:8].zfill(4)
            vmstardata = int(d)
        else:
            d = str(vmstardata).zfill(4)
    elif (itemoad in MONFREZELIST) and (ldata['save'].find('_MONTH') >= 0):
        if vmstardata == 0:
            d= timerun[4:8].zfill(4)
            vmstardata = int(d)
        else:
            d = str(vmstardata).zfill(4)
    else:
        print('增加其它走字规律')
    return d,vmstardata



#总和分费率走字计算(总=分费率*4)
def tallrate(meternum,id, stime):
    rateeach = 0
    #表号决定小数点后2位；个位和十位表示日/月/结算日---依据用例中获取到的为准；百位表示：正向有功 1；反向有功 2；第一象限无功：3
    if id in ['05060101','00010001','00010101','00010201','00010301','00010401']:
        rateeach = float( str(1) + stime + str(int(meternum[-2:])/100)[1:])
    elif id in ['05060201','00020001','00020101','00020201','00020301','00020401']:
        rateeach = float(str(2) + stime + str(int(meternum[-2:]) / 100)[1:])
    elif id in ['05060501','00050001','00050101','00050201','00050301','00050401']:
        rateeach = float(str(3) + stime + str(int(meternum[-2:]) / 100)[1:])
    if id in ['05060101','05060201','05060501']:
        stime = str(4*rateeach) + ',' +str(rateeach)+ ',' +str(rateeach)+ ',' +str(rateeach)+ ',' +str(rateeach)
    elif id in ['00010001','00020001','00050001']:
        stime = str(4 * rateeach)
    else:
        stime = str(rateeach)
    return stime



def titlenew(oadlistold, sheetname, plannum,plannumdict):
    try:
        if plannumdict[sheetname] != plannum:
            oadlistold = []
            plannumdict[sheetname] = plannum
    except:
        plannumdict[sheetname] = plannum
        oadlistold = []
    return plannumdict,oadlistold


def paramdeal(tasklist,taskrow):
    conflag = 0
    if taskrow['param'].find('SPECIALPARAM') >= 0:
        for itemnum in tasklist:
            if taskrow['save']  == tasklist[itemnum]['param'].split(',')[-1]:
                try:
                    taskrow['param'] = strtolist(tasklist[itemnum]['real'])[0][0]
                except:
                    conflag = 1
    else:
        for itemnum in tasklist:
            if taskrow['param'].split(':')[0]  == tasklist[itemnum]['save']:
                if taskrow['param'].find(',有效时标,10分') >= 0:
                    taskrow['param'] = tasklist[itemnum]['real'] + ',有效时标,10分'
                    break
                else:
                    taskrow['param'] = tasklist[itemnum]['real']
                    break

    return conflag
def differseconds(timestyle):
    timediffers= timestyle.days * 86400 + timestyle.seconds
    return timediffers
def messageprint(tasklistrow,start6505t,rpdtime):
    tasklistrow['result'] = '合格'
    if tasklistrow['param'].find('测试开始') >= 0:
        start6505t = datetime.datetime.now()
        logging.info(tasklistrow['param'] + '\n' +'\n' )
    elif tasklistrow['param'].find('开始测试') >= 0:
        rpdtime = datetime.datetime.now()
        logging.info(tasklistrow['param'] + '\n' +'\n' )

    else:
        if tasklistrow['param'].find('测试结束') >= 0:
            timenuse = datetime.datetime.now() - start6505t
            secondnums = differseconds(timenuse)
            tasklistrow['result'] = '测试时长：' + str(secondnums) + '秒'
            logging.info(tasklistrow['param'] + ' 测试时长:'+ str(secondnums) + '秒\n' + '\n' + '\n' + '\n' + '\n' + '\n''\n' + '\n' + '\n' + '\n')
        elif tasklistrow['param'].find('结束测试') >= 0:
            timenuse = datetime.datetime.now() - rpdtime
            secondnums = differseconds(timenuse)
            tasklistrow['result'] = '测试时长：' + str(secondnums) + '秒'
            logging.info(tasklistrow['param'] + ' 测试时长:'+ str(secondnums) + '秒\n' + '\n' + '\n' + '\n' + '\n' + '\n''\n' + '\n' + '\n' + '\n')
        else:
            logging.info(tasklistrow['param'] + '\n' + '\n' + '\n' + '\n' + '\n' + '\n''\n' + '\n' + '\n' + '\n')
    return start6505t,rpdtime














if __name__ == '__main__':
    pass