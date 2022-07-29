import xlrd
import os

path = os.path.dirname(os.getcwd()) + "\config"

COL6000 = ['nu', 'cut', 'order_number', 'meteradd', 'bps',
           'statute', 'port', 'password', 'rate', 'customer_type',
           'connection_mode', 'voltage', 'electric', 'collector_addr', 'asset',
           'ct', 'pt', 'oad', 'oad_quality']

PLACE6000 = ['customer_type','nu', 'cut', 'order_number', 'meteradd', 'bps',
           'statute', 'port', 'password', 'rate',
           'connection_mode', 'voltage', 'electric', 'collector_addr', 'asset',
           'ct', 'pt', 'oad', 'oad_quality']
COL6012 = ['nu', 'cut', 'task_id', 'frequency_time', 'frequency',
           'type_plan', 'plan_id', 'time_start', 'time_end', 'time_delay',
           'delay_unit', 'priority', 'state', 'id_front', 'id_back',
           'function', 'function_time', 'task_name']

COL_RECORD6012 = ['nu', 'cut', 'oad', 'sel', 'time_start',
                  'time_end', 'interval_time', 'interval', 'metertype', 'metercount',
                  'rcsd_oad', 'main_oad', 'road', 'task_name']
COL_RECORD6012_PLACE = ['nu','collmode','interval_time', 'interval', 'metertype', 'metercount','main_oad','savetime', 'road',  'task_name',  'sel','typenum','oad',  'time_start','time_end','rcsd_oad', 'cut']

COL6014 = ['nu', 'cut', 'task_id', 'memory_depth', 'collection_type',
           'collection_count', 'collection_unit', 'collection_patch', 'oad_main', 'oad',
           'electricity_meter_type', 'electricity_meter', 'memory_save', 'task_name']

COL6016 = ['nu', 'cut', 'task_id', 'collection_type', 'oad_main',
           'oad', 'ms_type', 'ms', 'report_logo', 'save_depth',
           'task_name']

COL6018 = ['nu', 'cut', 'task_id', 'task_nu', 'addr',
           'start_id', 'finish_id', 'report_wait', 'overtime', 'result_comparison',
           'comparison_bytes', 'comparison_start', 'comparison_len', 'message_nu', 'message',
           'save_depth', 'task_name']

COL601C = ['nu', 'cut', 'task_id', 'report_passageway', 'report_nu',
           'report_time', 'retry', 'type', 'select_oad', 'select',
           'time_start', 'time_end', 'interval_time', 'interval', 'ms_type',
           'ms', 'oad', 'main_oad', 'relation_oad', 'task_name']

COL_TASKSELECT = ['nu', 'cut', 'task_id', 'select_oad', 'select',
                  'oad', 'start', 'end', 'interval_time', 'interval',
                  'main_oad', 'rcsd_oad', 'task_name']
#OAD()	对象名称(name)	实时数据(real_date)	分钟冻结(minfr)  小时冻结(hourfr) 	日冻结(dayfr)	结算日冻结(setfr)	月冻结(monfr)  秒冻结（secfr）wm1215
PLAN_SELECT=['oad_all','name','real_date','minfr','hourfr','dayfr','setfr','monfr','secfr']

PLACEROWLIST = ['name', 'onemin','fifmin', 'hour', 'day', 'month', 'typefour', 'typethree','typeseven']
FREZEELIST = ['50020200','50030200','50040200','50050200','50060200']

def rtusupportoad(freezetype,oadcol,oadrow,oadgetlist):
    #因为要考虑 总、分标识，所以只判 前7位，这样无论是总还是分，标识都可以被选择到。
    if oadrow[freezetype] == '执行':
        oadgetlist.append(oadrow[oadcol][:-1])
    else:
        pass
    return oadgetlist

def rtutypeoad(filepath, taskname, tasktype,plansel):
    oadchoice = []
    realdatalist=[]
    hourfreezelist = []
    minfreezelist=[]
    dayfreezelist=[]
    setfreezelist=[]
    monfreezelist=[]
    secfreezelist=[]
    #路径目前先固定为下面的路径。这个表格里面有不同终端类型支持的OAD
    filepath = os.getcwd() + "\config" + "\面向对象协议采集参数配置表.xlsx"
    tasktype = 'oadchoice'
    if plansel == 'e_controller':
        taskname = '能源控制器OAD选择'
    elif plansel == 'major_version':
        taskname = '主版本OAD选择'
    elif plansel == 'own_test':
        taskname = '自主测试OAD选择'
    elif plansel == 'field_upgrade':
        taskname = '现场升级OAD选择'
    elif plansel == '698_inspection':
        taskname = '698送检OAD选择'
    else:print('继续扩展')
    ##继续处理表格，获得要测试的OAD列表
    oadtestexcel = readexcel(filepath, taskname, tasktype)
    for rowoad in range(1,len(oadtestexcel)):
        for columnplan in oadtestexcel[rowoad]:
            if columnplan == 'real_date':
                realdatalist = rtusupportoad('real_date', 'oad_all', oadtestexcel[rowoad], realdatalist)
            elif columnplan == 'hourfr':
                hourfreezelist = rtusupportoad('hourfr', 'oad_all', oadtestexcel[rowoad], hourfreezelist)
            elif columnplan == 'minfr':
                minfreezelist=rtusupportoad('minfr', 'oad_all', oadtestexcel[rowoad], minfreezelist)
            elif columnplan == 'dayfr':
                dayfreezelist=rtusupportoad('dayfr', 'oad_all', oadtestexcel[rowoad], dayfreezelist)
            elif columnplan == 'setfr':
                setfreezelist=rtusupportoad('setfr', 'oad_all', oadtestexcel[rowoad], setfreezelist)
            elif columnplan == 'monfr':
                monfreezelist=rtusupportoad('monfr', 'oad_all', oadtestexcel[rowoad], monfreezelist)
            elif columnplan == 'secfr':
                secfreezelist=rtusupportoad('secfr', 'oad_all', oadtestexcel[rowoad], secfreezelist)
            else:pass
    oadchoice={'实时_oad':realdatalist,'5002':minfreezelist,'5003':hourfreezelist,'5004':dayfreezelist,'5005':setfreezelist,'5006':monfreezelist,'5001':secfreezelist}
    return oadchoice


def excelchange(filepath, taskname, tasktype):
    dealexcellist = readexcel(filepath, taskname, tasktype)
    if (tasktype == 'task6000') or (tasktype == 'task6000_place'):
        resultlist = task_6000(dealexcellist)
    elif tasktype == 'task6012':
        resultlist = task_6012(dealexcellist)
    elif tasktype == 'record6012':
        resultlist = collection_6012(dealexcellist)
    elif tasktype == 'task6014':
        resultlist = task_6014(dealexcellist)
    elif tasktype == 'task6016':
        resultlist = task_6016(dealexcellist)
    elif tasktype == 'task6018':
        resultlist = task_6018(dealexcellist)
    elif tasktype == 'task601C':
        resultlist = task_601C(dealexcellist)
    elif tasktype == 'taskselect':
        resultlist = task_select(dealexcellist)
    elif tasktype == 'task6014-01':
        resultlist = task_6014(dealexcellist)
    elif tasktype == 'task6012-01':
        resultlist = task_6012(dealexcellist)
    elif tasktype == 'task6000-01':
        resultlist = task_6000(dealexcellist)
    else:
        resultlist = None

    return resultlist

#从所有的参数中，获取对应冻结类型的参数
def typeparamget(paramexecel,freeze):
    #实时数据暂定采用方法10的召测方式。
    paramlist = []
    nseltenflag = 0
    for item in paramexecel:
        if freeze != '选择方法10':
            if (paramexecel[item].find(freeze) >= 0) and (paramexecel[item].find('选择方法10') < 0):
                paramlist.append(paramexecel[item])
        else:
            for itemfreeze in FREZEELIST:
                if paramexecel[item].find(itemfreeze) >= 0:
                    nseltenflag = 1
                    break
                else:
                    nseltenflag = 0
            if nseltenflag == 0:
                if (paramexecel[item].find(freeze) >= 0):
                    paramlist.append(paramexecel[item])
    return paramlist

#从所有的参数中，获取对应冻结类型的参数
def typeparamgetmh(paramexecel,freeze,intervel):
    paramlist = []
    for item in paramexecel:
        if (paramexecel[item].find(freeze) >= 0) and (paramexecel[item].find(intervel) >= 0) and (paramexecel[item].find('选择方法10') < 0) :
            paramlist.append(paramexecel[item])
    return paramlist


def paramlistget(paramexecel,freezetype):
   # '日冻结循环召测参数列表'
    paramlist = []
    if freezetype == '日冻结循环召测参数列表':
        paramlist = typeparamget(paramexecel,'50040200')
    elif freezetype == '月冻结循环召测参数列表':
        paramlist = typeparamget(paramexecel,'50060200')
    elif freezetype == '结算日冻结循环召测参数列表':
        paramlist = typeparamget(paramexecel,'50050200')
    #分钟、小时加处理，要判断是15分钟冻结还是1分钟冻结---根据时间间隔增加处理
    elif freezetype == '秒冻结_1分冻结循环召测参数列表':
        paramlist = typeparamgetmh(paramexecel,'50010200','1分')
    elif freezetype == '秒冻结_60冻结循环召测参数列表':
        paramlist = typeparamgetmh(paramexecel,'50010200','60秒')
    elif freezetype == '分钟_1冻结循环召测参数列表':
        paramlist = typeparamgetmh(paramexecel,'50020200','1分')
    elif freezetype == '分钟_15冻结循环召测参数列表':
        paramlist = typeparamgetmh(paramexecel,'50020200','15分')
    elif freezetype == '分钟_60冻结循环召测参数列表':
        paramlist = typeparamgetmh(paramexecel,'50020200','1时')
    elif freezetype == '分钟_1日冻结循环召测参数列表':
        paramlist = typeparamgetmh(paramexecel,'50020200','1日')
    elif freezetype == '小时_1冻结循环召测参数列表':
        paramlist = typeparamgetmh(paramexecel,'50030200','1时')
    elif freezetype == '实时_方法10循环召测参数列表':
        paramlist = typeparamget(paramexecel,'选择方法10')
    else:
        print('增加其它冻结类型的召测参数获取流程')

    print('循环召测参数列表:',paramlist)
    return paramlist







def typetimes(test_plan,freezetype):
    filepath5 = os.getcwd() + "\config\place_config" + "\\参数配置表.xlsx"
    paramexecel = excelchangeplansel(filepath5, u"6012记录表_31", 'record6012_place', test_plan)
    paramfreezelist = paramlistget(paramexecel,freezetype)
    print('paramfreezelist:',paramfreezelist)
    return paramfreezelist


#需要依据终端类型，进行方案选择来确定测试OAD的流程，在这里处理。
def excelchangeplansel(filepath, taskname, tasktype,plansel):
    rtutypeoaddict={}
    rtutypeoadlist= rtutypeoad(filepath, taskname, tasktype,plansel)
    print('rtutypeoadlist:',rtutypeoadlist,sep='\n')
    dealexcellist = readexcel(filepath, taskname, tasktype)
    if tasktype == 'task6000':
        resultlist = task_6000(dealexcellist)
    elif tasktype == 'task6012':
        resultlist = task_6012(dealexcellist)
    elif tasktype == 'record6012':
        resultlist = collection_6012_meteread(dealexcellist,rtutypeoadlist)
    elif tasktype == 'record6012_place':
        resultlist = collection_6012_metersave(dealexcellist,rtutypeoadlist)
    elif tasktype == 'task6014':
        resultlist = task_6014_meteread(dealexcellist,rtutypeoadlist)
    elif tasktype == 'task6016':
        resultlist = task_6016(dealexcellist)
    elif tasktype == 'task6018':
        resultlist = task_6018(dealexcellist)
    elif tasktype == 'task601C':
        resultlist = task_601C(dealexcellist)
    elif tasktype == 'taskselect':
        resultlist = task_select(dealexcellist)
    elif tasktype == 'task6014-01':
        resultlist = task_6014(dealexcellist)
    elif tasktype == 'task6012-01':
        resultlist = task_6012(dealexcellist)
    elif tasktype == 'task6000-01':
        resultlist = task_6000(dealexcellist)
    else:
        resultlist = None

    return resultlist

# excel读取
def readexcel(filepath, taskname, tasktype):
    workbook = xlrd.open_workbook(filepath)
    rtem = {}
    COL_temp = []
    if tasktype == 'task6000' or tasktype == 'task6000-01':  # 6000档案
        COL_temp = COL6000
    elif tasktype == 'task6000_place':  # 6000档案,地方抄表测试，列的顺序做了调整
        COL_temp = PLACE6000
    elif tasktype == 'record6012':  # 6012记录表
        COL_temp = COL_RECORD6012
    elif tasktype == 'record6012_place':  # 6012记录表
        COL_temp = COL_RECORD6012_PLACE
    elif tasktype == 'task6012' or tasktype == 'task6012-01':  # 6012
        COL_temp = COL6012
    elif tasktype == 'task6014' or tasktype == 'task6014-01':  # 6014
        COL_temp = COL6014
    elif tasktype == 'task6016':  # 60016
        COL_temp = COL6016
    elif tasktype == 'task6018':  # 6018
        COL_temp = COL6018
    elif tasktype == 'task601C':  # 601C
        COL_temp = COL601C
    elif tasktype == 'taskselect':
        COL_temp = COL_TASKSELECT
    elif tasktype == 'oadchoice':
        COL_temp = PLAN_SELECT
    else:
        return rtem
    for sheetname in workbook.sheet_names():
        sheet = workbook.sheet_by_name(sheetname)
        for crange in sheet.merged_cells:
            rs, re, cs, ce = crange
        if sheetname == taskname:
            for ir in range(0, sheet.nrows):
                rowvalue = {}
                for col in range(0, len(COL_temp)):
                    rowvalue[COL_temp[col]] = sheet.cell(ir, col).value
                if 'cut' in COL_temp:
                    if rowvalue['cut'] == '执行':
                        rtem[ir] = rowvalue
                    else:
                        pass
                else:
                    rtem[ir] = rowvalue
    return rtem

# 读配置表格---为了获取召测时间
def readexceltimeget(lfile, sname, etype):
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
                else:
                    print('增加表格列类型')
    return rtem

def test_config():
    tasklist = {}
    testpath = os.getcwd() + "\config\place_config"
    tasklist = readexceltimeget(testpath + '/' + '参数配置表' + '.xlsx','时间参数', 'placecon')
    return tasklist

# 地址特征字处理
def addr_handle(addr):
    addrstr = ''
    if len(addr) == 2:
        addrstr += '00' + addr
    elif len(addr) == 4:
        addrstr += '01' + addr
    elif len(addr) == 6:
        addrstr += '02' + addr
    elif len(addr) == 8:
        addrstr += '03' + addr
    elif len(addr) == 10:
        addrstr += '04' + addr
    elif len(addr) == 12:
        addrstr += '05' + addr
    return addrstr


# 时间戳处理
def time_handle(time_str):
    timestr = ''
    str1 = time_str.split(' ')
    str2 = []
    for item in str1:
        if item != '':
            str2.append(item)
    YMD = str2[0].split('/')
    HMS = str2[1].split(':')
    for time_YMD in YMD:
        if len(time_YMD) < 2:
            timestr += time_YMD.zfill(2)
        else:
            timestr += time_YMD
    for time_HMS in HMS:
        if len(time_HMS) < 2:
            timestr += time_HMS.zfill(2)
        else:
            timestr += time_HMS
    return timestr


# 上报通道处理
def report_handle(report_passage):
    str = report_passage.split(',')
    str1 = ''
    if len(str) > 1:
        for i in range(0, len(str)):
            str1 += '\'' + str[i] + '\'' + ','
    else:
        str1 = '\'' + str[0] + '\''
    return str1


# ms电表集合处理
def ms_handle(ms_type, ms):
    excelstr = ''
    if isinstance(ms_type, str):
        if ms_type == '0:无表计':
            excelstr += '\'无表计\','
        elif ms_type == '1:全部用户地址':
            excelstr += '\'全部用户地址\','
        elif ms_type == '2:一组用户类型':
            excelstr += '\'一组用户类型,['
            meterstr = ms.split(',')
            for items in meterstr:
                excelstr += items + ','
            excelstr = excelstr[:-1]
            excelstr += ']\','
        elif ms_type == '3:一组用户地址':
            excelstr += '\'一组用户地址,['
            meterstr = ms.split(',')
            for items in meterstr:
                excelstr += '05' + items + ','
            excelstr = excelstr[:-1]
            excelstr += ']\','
        elif ms_type == '4:一组配置序号':
            excelstr += '\'一组配置序号,['
            meterstr = ms.split(',')
            for items in meterstr:
                excelstr += items + ','
            excelstr = excelstr[:-1]
            excelstr += ']\','
        elif ms_type == '5:一组用户类型区间':
            excelstr += '\'一组用户类型区间,'
            meterstr = ms.split(',')
            for items in meterstr:
                excelstr += items + ','
            excelstr = excelstr[:-1]
            excelstr += '\','
        elif ms_type == '6:一组用户地址区间':
            excelstr += '\'一组用户地址区间,'
            meterstr = ms.split(',')
            for items in meterstr:
                excelstr += items + ','
            excelstr = excelstr[:-1]
            excelstr += '\','
        elif ms_type == '7:一组配置序号区间':
            excelstr += '\'一组配置序号区间,'
            meterstr = ms.split(',')
            for items in meterstr:
                excelstr += items + ','
            excelstr = excelstr[:-1]
            excelstr += '\','
    return excelstr


# 冻结类oad处理
def oad_handle(oad):
    excelstr = ''
    if oad == '秒冻结(5001)':
        excelstr += '\'50010200\',['
    elif oad == '分钟冻结(5002)':
        excelstr += '\'50020200\',['
    elif oad == '小时冻结(5003)':
        excelstr += '\'50030200\',['
    elif oad == '日冻结(5004)':
        excelstr += '\'50040200\',['
    elif oad == '结算日(5005)':
        excelstr += '\'50050200\',['
    elif oad == '月冻结(5006)':
        excelstr += '\'50060200\',['
    elif oad == '年冻结(5007)':
        excelstr += '\'50070200\',['
    else:
        if isinstance(oad, float):
            excelstr += '\'' + str(int(oad)) + '\',['
        else:
            excelstr += '\'' + oad + '\',['
    return excelstr


# 6000档案
def task_6000(list):
    exceldict = {}
    # excelstr = '['
    ss = []
    for item1 in list:
        ss.append(item1)
        # print(ss)
    for item in list:
        excelstr = ''
        if isinstance(list[item]['order_number'], str):
            excelstr += '[' + list[item]['order_number'] + ',['
        elif isinstance(list[item]['order_number'], float):
            excelstr += '[' + str(int(list[item]['order_number'])) + ',['
        if isinstance(list[item]['meteradd'], str):
            excelstr += '\'' + addr_handle(list[item]['meteradd']) + '\'' + ','
        elif isinstance(list[item]['meteradd'], float):
            excelstr += '\'' + addr_handle(str(int(list[item]['meteradd']))) + '\'' + ','
        if isinstance(list[item]['bps'], str):
            if list[item]['bps'] == '300bps(0)':
                excelstr += '0,'
            elif list[item]['bps'] == '600bps(1)':
                excelstr += '1,'
            elif list[item]['bps'] == '1200bps(2)':
                excelstr += '2,'
            elif list[item]['bps'] == '2400bps(3)':
                excelstr += '3,'
            elif list[item]['bps'] == '4800bps(4)':
                excelstr += '4,'
            elif list[item]['bps'] == '7200bps(5)':
                excelstr += '5,'
            elif list[item]['bps'] == '9600bps(6)':
                excelstr += '6,'
            elif list[item]['bps'] == '19200bps(7)':
                excelstr += '7,'
            elif list[item]['bps'] == '38400bps(8)':
                excelstr += '8,'
            elif list[item]['bps'] == '57600bps(9)':
                excelstr += '9,'
            elif list[item]['bps'] == '115200bps(10)':
                excelstr += '10,'
            elif list[item]['bps'] == '自适应(255)':
                excelstr += '255,'
            else:
                continue
        if isinstance(list[item]['statute'], str):
            if list[item]['statute'] == '未知(0)':
                excelstr += '0,'
            elif list[item]['statute'] == 'DL/T 645-1997(1)':
                excelstr += '1,'
            elif list[item]['statute'] == 'DL/T 645-2007(2)':
                excelstr += '2,'
            elif list[item]['statute'] == 'DL/T 698.45(3)':
                excelstr += '3,'
            elif list[item]['statute'] == 'CJ/T 188-2004(4)':
                excelstr += '4,'
            else:
                continue
        if isinstance(list[item]['port'], str):
            if list[item]['port'] == 'F2010201(485#1)':
                excelstr += '\'' + 'F2010201' + '\','
            elif list[item]['port'] == 'F2010202(485#2)':
                excelstr += '\'' + 'F2010202' + '\','
            elif list[item]['port'] == 'F2010203(485#3)':
                excelstr += '\'' + 'F2010203' + '\','
            elif list[item]['port'] == 'F2010204(485#4)':
                excelstr += '\'' + 'F2010204' + '\','
            elif list[item]['port'] == 'F2080201(交采)':
                excelstr += '\'' + 'F2080201' + '\','
            elif list[item]['port'] == 'F2090201(载波)':
                excelstr += '\'' + 'F2090201' + '\','
            else:
                continue
        if list[item]['password'] == '':
            excelstr += '\'' + '00' + '\'' + ','
        elif isinstance(list[item]['password'], str):
            excelstr += '\'' + list[item]['password'] + '\'' + ','
        if isinstance(list[item]['rate'], str):
            excelstr += list[item]['rate'] + ','
        elif isinstance(list[item]['rate'], float):
            excelstr += str(int(list[item]['rate'])) + ','
        if isinstance(list[item]['customer_type'], str):
            excelstr += list[item]['customer_type'] + ','
        elif isinstance(list[item]['customer_type'], float):
            excelstr += str(int(list[item]['customer_type'])) + ','
        if isinstance(list[item]['connection_mode'], str):
            if list[item]['connection_mode'] == '未知(0)':
                excelstr += '0,'
            elif list[item]['connection_mode'] == '单相(1)':
                excelstr += '1,'
            elif list[item]['connection_mode'] == '三相三线(2)':
                excelstr += '2,'
            elif list[item]['connection_mode'] == '三相四线(3)':
                excelstr += '3,'
            else:
                continue
        if isinstance(list[item]['voltage'], str):
            excelstr += list[item]['voltage'].strip('V') + ','
        elif isinstance(list[item]['voltage'], float):
            excelstr += str(int(list[item]['voltage'])) + ','
        if isinstance(list[item]['electric'], str):
            excelstr += list[item]['electric'].strip('A') + '],['
        elif isinstance(list[item]['electric'], float):
            excelstr += str(int(list[item]['electric'])) + '],['
        if list[item]['collector_addr'] == '':
            excelstr += '\'' + '05000000000000' + '\'' + ','
        elif isinstance(list[item]['collector_addr'], str):
            excelstr += '\'' + addr_handle(list[item]['collector_addr']) + '\'' + ','
        if list[item]['asset'] == '':
            excelstr += '\'' + '000000' + '\'' + ','
        elif isinstance(list[item]['asset'], str):
            excelstr += '\'' + list[item]['asset'] + '\'' + ','
        if isinstance(list[item]['ct'], str):
            excelstr += list[item]['ct'] + ','
        elif isinstance(list[item]['ct'], float):
            excelstr += str(int(list[item]['ct'])) + ','
        if isinstance(list[item]['pt'], str):
            excelstr += list[item]['pt'] + '],'
        elif isinstance(list[item]['pt'], float):
            excelstr += str(int(list[item]['pt'])) + '],'
        if list[item]['oad'] == '' and list[item]['oad_quality'] == '':
            excelstr += '[]]'
        else:
            excelstr += '[' + list[item]['oad'] + list[item]['oad_quality'] + ']]'
        excel = {int(list[item]['order_number']): excelstr}
        exceldict.update(excel)
    # print(excelstr)
    return exceldict


# 60120300采集---参数使用
def collection_6012(list):
    exceldict = {}
    list_msg = []
    for item in list:
        list_msg.append(list[item])
    set_mark = {list_param['nu'] for list_param in list_msg}
    ver_name = [i for i in set_mark]
    ver_name.sort()
    list_name_template = 'nu'
    list_all = locals()
    for mark in set_mark:
        list_all[list_name_template + str(mark)] = [dict_current for dict_current in list_msg if
                                                    dict_current['nu'] == mark]
    for i in ver_name:
        excelstr = ''
        list_deal = list_all['nu' + str(i)]
        list_len = len(list_deal)
        # print(list_deal[0]['interval'])
        # print(type(list_deal[0]['interval']))
        if isinstance(list_deal[0]['sel'], str):
            excelstr += '['
            if list_deal[0]['sel'] == '方法4' or list_deal[0]['sel'] == '方法5':
                excelstr += '\'选择' + list_deal[0]['sel'] + '\',[\'' + time_handle(list_deal[0]['time_start']) + '\','
            elif list_deal[0]['sel'] == '方法6' or list_deal[0]['sel'] == '方法7' or list_deal[0]['sel'] == '方法8':
                excelstr += '\'选择' + list_deal[0]['sel'] + '\',[\'' + time_handle(
                    list_deal[0]['time_start']) + '\',\'' + time_handle(list_deal[0][
                                                                            'time_end']) + '\',\'' + str(
                    int(list_deal[0]['interval_time'])) + list_deal[0]['interval'] + '\','
            elif list_deal[0]['sel'] == '方法10':
                excelstr += '\'选择方法10\',' + '[' + str(int(list_deal[0]['interval_time'])) + ','
        if isinstance(list_deal[0]['metertype'], str):
            excelstr += ms_handle(list_deal[0]['metertype'], list_deal[0]['metercount'])
            excelstr += ']]'
            # if list_deal[0]['metertype'] == '0:无表计':
            #     excelstr += '\'无表计\',]'
            # elif list_deal[0]['metertype'] == '1:全部用户地址':
            #     excelstr += '\'全部用户地址\',]'
            # elif list_deal[0]['metertype'] == '2:一组用户类型':
            #     excelstr += '\'一组用户类型,['
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += ']\',]'
            # elif list_deal[0]['metertype'] == '3:一组用户地址':
            #     excelstr += '\'一组用户地址,['
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += '\'' + items + '\','
            #     excelstr += ']\',]'
            # elif list_deal[0]['metertype'] == '4:一组配置序号':
            #     excelstr += '\'一组配置序号,['
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += ']\','
            # elif list_deal[0]['metertype'] == '5:一组用户类型区间':
            #     excelstr += '\'一组用户类型区间,'
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += '\','
            # elif list_deal[0]['metertype'] == '6:一组用户地址区间':
            #     excelstr += '\'一组用户地址区间,'
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += '\','
            # elif list_deal[0]['metertype'] == '7:一组配置序号区':
            #     excelstr += '\'一组配置序号区间,'
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += '\''
        excelstr += ',['
        if isinstance(list_deal[0]['rcsd_oad'], str):
            # print(list_deal[0]['rcsd_oad'])
            oadstr = list_deal[0]['rcsd_oad'].split(',')
            for item in oadstr:
                excelstr += '\'' + item + '\','
            if isinstance(list_deal[0]['main_oad'], str) and list_deal[0]['main_oad'] != '':
                if list_len != 1:
                    for len_oad in range(0, list_len):
                        # print(list_deal[len_oad]['road'])
                        road_str = list_deal[len_oad]['road'].split(',')
                        excelstr += oad_handle(list_deal[0]['main_oad'])
                        for item in road_str:
                            excelstr += '\'' + item + '\','
                        excelstr += '],'
                else:
                    for len_oad in range(0, list_len):
                        road_str = list_deal[len_oad]['road'].split(',')
                        excelstr += oad_handle(list_deal[0]['main_oad'])
                        for item in road_str:
                            excelstr += '\'' + item + '\''
                            excelstr += ','
                    excelstr += ']'
                excelstr += ']'
            elif list_deal[0]['main_oad'] == '':
                road_str = list_deal[0]['road'].split(',')
                # WM
                # excelstr += '['
                for item in road_str:
                    excelstr += '\'' + item + '\','
                excelstr += ']'
            # excelstr += ']'
        else:
            pass
        excel = {int(list_deal[0]['nu']): excelstr}
        exceldict.update(excel)
    return exceldict



# {'': ['00000200', '00100200', '00200200', '00300200', '00400200', '00500200', '00600200', '00700200', '00800200', '10100200', '10200200', '20000200', '20010200', '20010600', '20030200', '20040200', '20050200', '200A0200'], '5002': ['00100200', '00200200', '00300200', '00400200', '10100200', '10200200', '20000200', '20010200', '20010600', '20040200', '20050200', '200A0200'], '5004': ['00100200', '00200200', '00300200', '00400200', '00500200', '00600200', '00700200', '00800200', '10100200', '10200200'], '5005': ['00100200', '00200200', '00300200', '00400200', '10100200', '10200200'], '5006': ['00100200', '00200200', '00300200', '00400200', '00500200', '00600200', '00700200', '00800200', '10100200', '10200200']}
# 60120300采集 ---抄表使用 oadplandict:根据终端类型，生成的要测试的OAD存储在字典中
def collection_6012_meteread(list,oadplandict):
    exceldict = {}
    list_msg = []
    for item in list:
        list_msg.append(list[item])
    set_mark = {list_param['nu'] for list_param in list_msg}
    ver_name = [i for i in set_mark]
    ver_name.sort()
    list_name_template = 'nu'
    list_all = locals()
    for mark in set_mark:
        list_all[list_name_template + str(mark)] = [dict_current for dict_current in list_msg if
                                                    dict_current['nu'] == mark]
    for i in ver_name:
        excelstr = ''
        list_deal = list_all['nu' + str(i)]
        list_len = len(list_deal)
        # print(list_deal[0]['interval'])
        # print(type(list_deal[0]['interval']))
        if isinstance(list_deal[0]['sel'], str):
            excelstr += '['
            if list_deal[0]['sel'] == '方法4' or list_deal[0]['sel'] == '方法5':
                excelstr += '\'选择' + list_deal[0]['sel'] + '\',[\'' + time_handle(list_deal[0]['time_start']) + '\','
            elif list_deal[0]['sel'] == '方法6' or list_deal[0]['sel'] == '方法7' or list_deal[0]['sel'] == '方法8':
                excelstr += '\'选择' + list_deal[0]['sel'] + '\',[\'' + time_handle(
                    list_deal[0]['time_start']) + '\',\'' + time_handle(list_deal[0][
                                                                            'time_end']) + '\',\'' + str(
                    int(list_deal[0]['interval_time'])) + list_deal[0]['interval'] + '\','
            elif list_deal[0]['sel'] == '方法10':
                excelstr += '\'选择方法10\',' + '[' + str(int(list_deal[0]['interval_time'])) + ','
        if isinstance(list_deal[0]['metertype'], str):
            excelstr += ms_handle(list_deal[0]['metertype'], list_deal[0]['metercount'])
            excelstr += ']]'
            # if list_deal[0]['metertype'] == '0:无表计':
            #     excelstr += '\'无表计\',]'
            # elif list_deal[0]['metertype'] == '1:全部用户地址':
            #     excelstr += '\'全部用户地址\',]'
            # elif list_deal[0]['metertype'] == '2:一组用户类型':
            #     excelstr += '\'一组用户类型,['
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += ']\',]'
            # elif list_deal[0]['metertype'] == '3:一组用户地址':
            #     excelstr += '\'一组用户地址,['
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += '\'' + items + '\','
            #     excelstr += ']\',]'
            # elif list_deal[0]['metertype'] == '4:一组配置序号':
            #     excelstr += '\'一组配置序号,['
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += ']\','
            # elif list_deal[0]['metertype'] == '5:一组用户类型区间':
            #     excelstr += '\'一组用户类型区间,'
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += '\','
            # elif list_deal[0]['metertype'] == '6:一组用户地址区间':
            #     excelstr += '\'一组用户地址区间,'
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += '\','
            # elif list_deal[0]['metertype'] == '7:一组配置序号区':
            #     excelstr += '\'一组配置序号区间,'
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += '\''
        excelstr += ',['
        if isinstance(list_deal[0]['rcsd_oad'], str):
            # print(list_deal[0]['rcsd_oad'])
            oadstr = list_deal[0]['rcsd_oad'].split(',')
            for item in oadstr:
                excelstr += '\'' + item + '\','
            if isinstance(list_deal[0]['main_oad'], str) and list_deal[0]['main_oad'] != '':
                if list_len != 1:
                    for len_oad in range(0, list_len):
                        # print(list_deal[len_oad]['road'])
                        road_str = list_deal[len_oad]['road'].split(',')
                        excelstr += oad_handle(list_deal[0]['main_oad'])
                        for item in road_str:
                            for fretypeoad in oadplandict.keys():
                                if fretypeoad in list_deal[0]['main_oad']:
                                    if item[:-1] in oadplandict[fretypeoad]:
                                        excelstr += '\'' + item + '\','
                                    else:
                                        pass
                        excelstr += '],'
                        #没有在对应的测试方案中找到标识，就对excelstr 进行处理
                        if excelstr[-3:-1]== '[]':
                            excelstr=excelstr[:-14]
                        else:pass



                else:
                    for len_oad in range(0, list_len):
                        road_str = list_deal[len_oad]['road'].split(',')
                        excelstr += oad_handle(list_deal[0]['main_oad'])
                        for item in road_str:
                            for fretypeoad in oadplandict.keys():
                                if fretypeoad in list_deal[0]['main_oad']:
                                    if item[:-1] in oadplandict[fretypeoad]:
                                        excelstr += '\'' + item + '\''
                                        excelstr += ','
                                    else:pass

                    excelstr += ']'
                    # 没有在对应的测试方案中找到标识，就对excelstr 进行处理
                    if excelstr[-2:] == '[]':
                        excelstr = excelstr[:-14]
                    else:
                        pass
                excelstr += ']'
            elif list_deal[0]['main_oad'] == '':
                road_str = list_deal[0]['road'].split(',')
                for item in road_str:
                    if item[:-1] in oadplandict['实时_oad']:
                        excelstr += '\'' + item + '\','
                    else:
                        pass
                excelstr += ']'
            # excelstr += ']'
        else:
            pass
        excel = {int(list_deal[0]['nu']): excelstr}
        exceldict.update(excel)
    return exceldict


# 60120300采集 ---抄表使用 oadplandict:根据终端类型，生成的要测试的OAD存储在字典中
def collection_6012_metersave(list,oadplandict):
    exceldict = {}
    list_msg = []
    for item in list:
        list_msg.append(list[item])
    set_mark = {list_param['nu'] for list_param in list_msg}
    ver_name = [i for i in set_mark]
    ver_name.sort()
    list_name_template = 'nu'
    list_all = locals()
    for mark in set_mark:
        list_all[list_name_template + str(mark)] = [dict_current for dict_current in list_msg if
                                                    dict_current['nu'] == mark]
    for i in ver_name:
        excelstr = ''
        list_deal = list_all['nu' + str(i)]
        list_len = len(list_deal)
        # print(list_deal[0]['interval'])
        # print(type(list_deal[0]['interval']))
        if isinstance(list_deal[0]['sel'], str):
            excelstr += '['
            if list_deal[0]['sel'] == '方法4' or list_deal[0]['sel'] == '方法5':
                excelstr += '\'选择' + list_deal[0]['sel'] + '\',[\'' + time_handle(list_deal[0]['time_start']) + '\','
            elif list_deal[0]['sel'] == '方法6' or list_deal[0]['sel'] == '方法7' or list_deal[0]['sel'] == '方法8':
                excelstr += '\'选择' + list_deal[0]['sel'] + '\',[\'' + time_handle(
                    list_deal[0]['time_start']) + '\',\'' + time_handle(list_deal[0][
                                                                            'time_end']) + '\',\'' + str(
                    int(list_deal[0]['interval_time'])) + list_deal[0]['interval'] + '\','
            elif list_deal[0]['sel'] == '方法10':
                # excelstr += '\'选择方法10\',' + '[' + str(int(list_deal[0]['interval_time'])) + ','
                #地方抄表方法10暂时先做成固定的上一次
                excelstr += '\'选择方法10\',' + '[' + str(1) + ','
        if isinstance(list_deal[0]['metertype'], str):
            excelstr += ms_handle(list_deal[0]['metertype'], list_deal[0]['metercount'])
            excelstr += ']]'
            # if list_deal[0]['metertype'] == '0:无表计':
            #     excelstr += '\'无表计\',]'
            # elif list_deal[0]['metertype'] == '1:全部用户地址':
            #     excelstr += '\'全部用户地址\',]'
            # elif list_deal[0]['metertype'] == '2:一组用户类型':
            #     excelstr += '\'一组用户类型,['
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += ']\',]'
            # elif list_deal[0]['metertype'] == '3:一组用户地址':
            #     excelstr += '\'一组用户地址,['
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += '\'' + items + '\','
            #     excelstr += ']\',]'
            # elif list_deal[0]['metertype'] == '4:一组配置序号':
            #     excelstr += '\'一组配置序号,['
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += ']\','
            # elif list_deal[0]['metertype'] == '5:一组用户类型区间':
            #     excelstr += '\'一组用户类型区间,'
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += '\','
            # elif list_deal[0]['metertype'] == '6:一组用户地址区间':
            #     excelstr += '\'一组用户地址区间,'
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += '\','
            # elif list_deal[0]['metertype'] == '7:一组配置序号区':
            #     excelstr += '\'一组配置序号区间,'
            #     meterstr = list_deal[0]['metercount'].split(',')
            #     for items in meterstr:
            #         excelstr += items + ','
            #     excelstr += '\''
        excelstr += ',['
        if isinstance(list_deal[0]['rcsd_oad'], str):
            # print(list_deal[0]['rcsd_oad'])
            oadstr = list_deal[0]['rcsd_oad'].split(',')
            for item in oadstr:
                excelstr += '\'' + item + '\','
            if isinstance(list_deal[0]['main_oad'], str) and list_deal[0]['main_oad'] != '':
                if list_len != 1:
                    for len_oad in range(0, list_len):
                        # print(list_deal[len_oad]['road'])
                        road_str = list_deal[len_oad]['road'].split(',')
                        excelstr += oad_handle(list_deal[0]['main_oad'])
                        for item in road_str:
                            for fretypeoad in oadplandict.keys():
                                if fretypeoad in list_deal[0]['main_oad']:
                                    if item[:-1] in oadplandict[fretypeoad]:
                                        excelstr += '\'' + item + '\','
                                    else:
                                        pass
                        excelstr += '],'
                        #没有在对应的测试方案中找到标识，就对excelstr 进行处理
                        if excelstr[-3:-1]== '[]':
                            excelstr=excelstr[:-14]
                        else:pass



                else:
                    for len_oad in range(0, list_len):
                        road_str = list_deal[len_oad]['road'].split(',')
                        excelstr += oad_handle(list_deal[0]['main_oad'])
                        for item in road_str:
                            for fretypeoad in oadplandict.keys():
                                if fretypeoad in list_deal[0]['main_oad']:
                                    if item[:-1] in oadplandict[fretypeoad]:
                                        excelstr += '\'' + item + '\''
                                        excelstr += ','
                                    else:pass

                    excelstr += ']'
                    # 没有在对应的测试方案中找到标识，就对excelstr 进行处理
                    if excelstr[-2:] == '[]':
                        excelstr = excelstr[:-14]
                    else:
                        pass
                excelstr += ']'
            elif list_deal[0]['main_oad'] == '':
                road_str = list_deal[0]['road'].split(',')
                for item in road_str:
                    if item[:-1] in oadplandict['实时_oad']:
                        excelstr += '\'' + item + '\','
                    else:
                        pass
                excelstr += ']'
            # excelstr += ']'
        else:
            pass
        # if (isinstance(list_deal[0]['savetime'], str)) and (list_deal[0]['sel'] != '方法10'):
        if (isinstance(list_deal[0]['savetime'], str)):
            excelstr += ":" + list_deal[0]['savetime'].split(':')[0] + ":"  +list_deal[0]['typenum']
        print('excelstr:', excelstr)
        excel = {int(list_deal[0]['nu']): excelstr}
        exceldict.update(excel)
    return exceldict


# 6014普通采集方案
def task_6014(tlist):
    exceldict = {}
    list_msg = []
    for item in tlist:
        list_msg.append(tlist[item])
    set_mark = {list_param['task_id'] for list_param in list_msg}
    ver_name = [i for i in set_mark]
    ver_name.sort()
    list_name_template = 'task_id'
    list_all = locals()
    # 将所有任务按照任务id分别存储 命名方式为task_id？     ？是任务号

    for mark in set_mark:
        list_all[list_name_template + mark] = [dict_current for dict_current in list_msg if
                                               dict_current['task_id'] == mark]
    for i in ver_name:
        excelstr = ''
        list_deal = list_all['task_id' + i]
        list_len = len(list_deal)
        if isinstance(list_deal[0]['task_id'], str):
            excelstr += '[' + list_deal[0]['task_id'] + ','
        elif isinstance(list_deal[0]['task_id'], float):
            excelstr += '[' + str(int(list_deal[0]['task_id'])) + ','
        if isinstance(list_deal[0]['memory_depth'], str):
            excelstr += list_deal[0]['memory_depth'] + ',['
        elif isinstance(list_deal[0]['memory_depth'], float):
            excelstr += str(int(list_deal[0]['memory_depth'])) + ',['
        if isinstance(list_deal[0]['collection_type'], str) and list_deal[0]['collection_type'] != '':
            if list_deal[0]['collection_type'] == '0:采集当前数据':
                excelstr += '0,\'NULL\'],['
            elif list_deal[0]['collection_type'] == '1:采集上第N次':
                excelstr += '1,' + list_deal[0]['collection_count'] + '],['
            elif list_deal[0]['collection_type'] == '2:按冻结时标采集':
                excelstr += '2,\'NULL\'],['
            elif list_deal[0]['collection_type'] == '3:按时间间隔采集':
                excelstr += '3,' + '\'' + str(int(list_deal[0]['collection_count'])) + list_deal[0][
                    'collection_unit'] + '\'],['
            elif list_deal[0]['collection_type'] == '4:补抄':
                excelstr += '4,' + '[\'' + str(int(list_deal[0]['collection_count'])) + list_deal[0][
                    'collection_unit'] + '\',' + list_deal[0]['collection_patch'] + ']],['
        else:
            pass
        if isinstance(list_deal[0]['oad_main'], str) and list_deal[0]['oad_main'] != '':
            if list_len != 1:
                for len_oad in range(0, list_len):
                    oad_str = list_deal[len_oad]['oad'].split(',')
                    excelstr += oad_handle(list_deal[len_oad]['oad_main'])
                    for item in oad_str:
                        excelstr += '\'' + item + '\','
                    excelstr += '],'
            else:
                excelstr += oad_handle(list_deal[0]['oad_main'])
                oadstr = list_deal[0]['oad'].split(',')
                for item in oadstr:
                    excelstr += '\'' + item + '\','
                excelstr += '],'
            excelstr += '],'
        elif list_deal[0]['oad_main'] == '' and list_deal[0]['oad'] != '':
            oadstr = list_deal[0]['oad'].split(',')
            for item in oadstr:
                excelstr += '\'' + item + '\','
            excelstr += '],'
            # print('excelstr:',excelstr)
        excelstr += ms_handle(list_deal[0]['electricity_meter_type'], list_deal[0]['electricity_meter'])
        if isinstance(list_deal[0]['memory_save'], str):
            if list_deal[0]['memory_save'] == '0:未定义':
                excelstr += '0]'
            elif list_deal[0]['memory_save'] == '1:任务开始时间':
                excelstr += '1]'
            elif list_deal[0]['memory_save'] == '2:相对当日0点0分':
                excelstr += '2]'
            elif list_deal[0]['memory_save'] == '3:相对上日23点59':
                excelstr += '3]'
            elif list_deal[0]['memory_save'] == '4:相对上日0点0分':
                excelstr += '4]'
            elif list_deal[0]['memory_save'] == '5:相对当月1日0点0分':
                excelstr += '5]'
            elif list_deal[0]['memory_save'] == '6:数据冻结时标':
                excelstr += '6]'
            elif list_deal[0]['memory_save'] == '7:相对上月月末23点59分':
                excelstr += '7]'
        excel = {int(list_deal[0]['task_id']): excelstr}
        exceldict.update(excel)
    return exceldict

# 6014普通采集方案---抄表用例使用,oadchoicedict:根据终端类型，生成的要测试的OAD存储在字典中
def task_6014_meteread(tlist,oadchoicedict):
    exceldict = {}
    list_msg = []
    for item in tlist:
        list_msg.append(tlist[item])
    set_mark = {list_param['task_id'] for list_param in list_msg}
    ver_name = [i for i in set_mark]
    ver_name.sort()
    list_name_template = 'task_id'
    list_all = locals()
    # 将所有任务按照任务id分别存储 命名方式为task_id？     ？是任务号

    for mark in set_mark:
        list_all[list_name_template + mark] = [dict_current for dict_current in list_msg if
                                               dict_current['task_id'] == mark]
    for i in ver_name:
        excelstr = ''
        list_deal = list_all['task_id' + i]
        list_len = len(list_deal)
        if isinstance(list_deal[0]['task_id'], str):
            excelstr += '[' + list_deal[0]['task_id'] + ','
        elif isinstance(list_deal[0]['task_id'], float):
            excelstr += '[' + str(int(list_deal[0]['task_id'])) + ','
        if isinstance(list_deal[0]['memory_depth'], str):
            excelstr += list_deal[0]['memory_depth'] + ',['
        elif isinstance(list_deal[0]['memory_depth'], float):
            excelstr += str(int(list_deal[0]['memory_depth'])) + ',['
        if isinstance(list_deal[0]['collection_type'], str) and list_deal[0]['collection_type'] != '':
            if list_deal[0]['collection_type'] == '0:采集当前数据':
                excelstr += '0,\'NULL\'],['
            elif list_deal[0]['collection_type'] == '1:采集上第N次':
                excelstr += '1,' + list_deal[0]['collection_count'] + '],['
            elif list_deal[0]['collection_type'] == '2:按冻结时标采集':
                excelstr += '2,\'NULL\'],['
            elif list_deal[0]['collection_type'] == '3:按时间间隔采集':
                excelstr += '3,' + '\'' + str(int(list_deal[0]['collection_count'])) + list_deal[0][
                    'collection_unit'] + '\'],['
            elif list_deal[0]['collection_type'] == '4:补抄':
                excelstr += '4,' + '[\'' + str(int(list_deal[0]['collection_count'])) + list_deal[0][
                    'collection_unit'] + '\',' + list_deal[0]['collection_patch'] + ']],['
        else:
            pass
        if isinstance(list_deal[0]['oad_main'], str) and list_deal[0]['oad_main'] != '':
            if list_len != 1:
                for len_oad in range(0, list_len):
                    oad_str = list_deal[len_oad]['oad'].split(',')
                    excelstr += oad_handle(list_deal[len_oad]['oad_main'])
                    for item in oad_str:
                        for fretypeoad in oadchoicedict.keys():
                            if fretypeoad in list_deal[len_oad]['oad_main']:
                                if item[:-1] in oadchoicedict[fretypeoad]:
                                    excelstr += '\'' + item + '\','
                                else:pass
                    excelstr += '],'
                    # 没有在对应的测试方案中找到标识，就对excelstr 进行处理
                    if  excelstr[-3:-1] == '[]':
                        excelstr = excelstr[:-14]
                    else:
                        pass
            else:
                excelstr += oad_handle(list_deal[0]['oad_main'])
                oadstr = list_deal[0]['oad'].split(',')
                for item in oadstr:
                    for fretypeoad in oadchoicedict.keys():
                        if fretypeoad in list_deal[0]['oad_main']:
                            if item[:-1] in oadchoicedict[fretypeoad]:
                                excelstr += '\'' + item + '\','
                            else:pass
                excelstr += '],'
                # 没有在对应的测试方案中找到标识，就对excelstr 进行处理
                if excelstr[-3:-1] == '[]':
                    excelstr = excelstr[:-14]
                else:
                    pass
            excelstr += '],'

        elif list_deal[0]['oad_main'] == '' and list_deal[0]['oad'] != '':
            oadstr = list_deal[0]['oad'].split(',')
            for item in oadstr:
                if item[:-1] in oadchoicedict['实时_oad']:
                    excelstr += '\'' + item + '\','
                else:
                    pass
            excelstr += '],'
            # print('excelstr:',excelstr)
        excelstr += ms_handle(list_deal[0]['electricity_meter_type'], list_deal[0]['electricity_meter'])
        if isinstance(list_deal[0]['memory_save'], str):
            if list_deal[0]['memory_save'] == '0:未定义':
                excelstr += '0]'
            elif list_deal[0]['memory_save'] == '1:任务开始时间':
                excelstr += '1]'
            elif list_deal[0]['memory_save'] == '2:相对当日0点0分':
                excelstr += '2]'
            elif list_deal[0]['memory_save'] == '3:相对上日23点59':
                excelstr += '3]'
            elif list_deal[0]['memory_save'] == '4:相对上日0点0分':
                excelstr += '4]'
            elif list_deal[0]['memory_save'] == '5:相对当月1日0点0分':
                excelstr += '5]'
            elif list_deal[0]['memory_save'] == '6:数据冻结时标':
                excelstr += '6]'
            elif list_deal[0]['memory_save'] == '7:相对上月月末23点59分':
                excelstr += '7]'
        excel = {int(list_deal[0]['task_id']): excelstr}
        exceldict.update(excel)
    return exceldict
# 6016事件采集方案-----参数用例使用
def task_6016(list):
    exceldict = {}
    list_msg = []
    for item in list:
        list_msg.append(list[item])
    set_mark = {list_param['task_id'] for list_param in list_msg}
    ver_name = [i for i in set_mark]
    ver_name.sort()
    list_name_template = 'task_id'
    list_all = locals()
    # 将所有任务按照任务id分别存储 命名方式为task_id？     ？是任务号
    for mark in set_mark:
        list_all[list_name_template + mark] = [dict_current for dict_current in list_msg if
                                               dict_current['task_id'] == mark]
    for i in ver_name:
        excelstr = ''
        list_deal = list_all['task_id' + i]
        list_len = len(list_deal)
        if isinstance(list_deal[0]['task_id'], str):
            excelstr += '[' + list_deal[0]['task_id'] + ','
        elif isinstance(list_deal[0]['task_id'], float):
            excelstr += '[' + str(int(list_deal[0]['task_id'])) + ','

        if isinstance(list_deal[0]['collection_type'], str):
            if list_deal[0]['collection_type'] == '0:周期采集事件数据':
                excelstr += '[0,['
                if isinstance(list_deal[0]['oad_main'], str) and list_deal[0]['oad_main'] != '':
                    if list_len != 1:
                        for len_oad in range(0, list_len):
                            oad_str = list_deal[len_oad]['oad'].split(',')
                            excelstr += '[' + oad_handle(list_deal[len_oad]['oad_main'])
                            for item in oad_str:
                                excelstr += '\'' + item + '\','
                            excelstr += ']],'
                    else:
                        excelstr += '[' + oad_handle(list_deal[0]['oad_main'])
                        oadstr = list_deal[0]['oad'].split(',')
                        for item in oadstr:
                            excelstr += '\'' + item + '\','
                        excelstr += ']],'
                    excelstr += '],'
                excelstr += '],'
            elif list_deal[0]['collection_type'] == '1:根据通知采集所有事件数据':
                excelstr += '[1,' + '\'' + 'NULL' + '\'' + '],'
            elif list_deal[0]['collection_type'] == '2:根据通知采集指定事件数据':
                excelstr += '[2,['
                if isinstance(list_deal[0]['oad_main'], str) and list_deal[0]['oad_main'] != '':
                    if list_len != 1:
                        for len_oad in range(0, list_len):
                            oad_str = list_deal[len_oad]['oad'].split(',')
                            excelstr += '[' + oad_handle(list_deal[len_oad]['oad_main'])
                            for item in oad_str:
                                excelstr += '\'' + item + '\','
                            excelstr += ']],'
                    else:
                        excelstr += '[' + oad_handle(list_deal[0]['oad_main'])
                        oadstr = list_deal[0]['oad'].split(',')
                        for item in oadstr:
                            excelstr += '\'' + item + '\','
                        excelstr += ']],'
                    excelstr += '],'
                excelstr += '],'
            elif list_deal[0]['collection_type'] == '3:根据通知存储生成的事件数据':
                excelstr += '[3,' + '\'' + 'NULL' + '\'' + '],'

        excelstr += ms_handle(list_deal[0]['ms_type'], list_deal[0]['ms'])
        if isinstance(list_deal[0]['report_logo'], str):
            if list_deal[0]['report_logo'] == '0:不上报':
                excelstr += '0,'
            elif list_deal[0]['report_logo'] == '1:立即上报':
                excelstr += '1,'
        if isinstance(list_deal[0]['save_depth'], str):
            excelstr += list_deal[0]['save_depth'] + ']'
        excel = {int(list_deal[0]['task_id']): excelstr}
        exceldict.update(excel)
    return exceldict


# 6018透明方案
def task_6018(list):
    exceldict = {}
    list_msg = []
    for item in list:
        list_msg.append(list[item])
    set_mark = {list_param['task_id'] for list_param in list_msg}
    ver_name = [i for i in set_mark]
    ver_name.sort()
    list_name_template = 'task_id'
    list_all = locals()
    # 将所有任务按照任务id分别存储 命名方式为task_id？     ？是任务号
    for mark in set_mark:
        list_all[list_name_template + mark] = [dict_current for dict_current in list_msg if
                                               dict_current['task_id'] == mark]
    for i in ver_name:
        excelstr = ''
        list_deal = list_all['task_id' + i]
        list_len = len(list_deal)
        if isinstance(list_deal[0]['task_id'], str):
            excelstr += '[' + list_deal[0]['task_id'] + ','
        elif isinstance(list_deal[0]['task_id'], float):
            excelstr += '[' + str(int(list_deal[0]['task_id'])) + ','
        excelstr += '['
        if list_len == 1:
            excelstr += '['
            if isinstance(list_deal[0]['task_nu'], str):
                excelstr += list_deal[0]['task_nu'] + ','
            elif isinstance(list_deal[0]['task_nu'], float):
                excelstr += str(int(list_deal[0]['task_nu'])) + ','
            if isinstance(list_deal[0]['addr'], str):
                excelstr += '\'05' + list_deal[0]['addr'] + '\','
            elif isinstance(list_deal[0]['addr'], float):
                excelstr += '\'05' + str(int(list_deal[0]['addr'])) + '\','
            if isinstance(list_deal[0]['start_id'], str):
                excelstr += list_deal[0]['start_id'] + ','
            elif isinstance(list_deal[0]['start_id'], float):
                excelstr += str(int(list_deal[0]['start_id'])) + ','
            if isinstance(list_deal[0]['finish_id'], str):
                excelstr += list_deal[0]['finish_id'] + ','
            elif isinstance(list_deal[0]['finish_id'], float):
                excelstr += str(int(list_deal[0]['finish_id'])) + ','
            excelstr += '['
            if isinstance(list_deal[0]['report_wait'], str):
                if list_deal[0]['report_wait'] == '0:不上报':
                    excelstr += '0,'
                elif list_deal[0]['report_wait'] == '1:上报':
                    excelstr += '1,'
            if isinstance(list_deal[0]['overtime'], str):
                excelstr += list_deal[0]['overtime'] + ','
            elif isinstance(list_deal[0]['overtime'], float):
                excelstr += str(int(list_deal[0]['overtime'])) + ','
            if isinstance(list_deal[0]['result_comparison'], str):
                if list_deal[0]['result_comparison'] == '0:不比对':
                    excelstr += '0,'
                elif list_deal[0]['result_comparison'] == '1:比对':
                    excelstr += '1,'
                elif list_deal[0]['result_comparison'] == '2: 比对上报':
                    excelstr += '2,'
            excelstr += '['
            if isinstance(list_deal[0]['comparison_bytes'], str):
                excelstr += list_deal[0]['comparison_bytes'] + ','
            elif isinstance(list_deal[0]['comparison_bytes'], float):
                excelstr += str(int(list_deal[0]['comparison_bytes'])) + ','
            if isinstance(list_deal[0]['comparison_start'], str):
                excelstr += list_deal[0]['comparison_start'] + ','
            elif isinstance(list_deal[0]['comparison_start'], float):
                excelstr += str(int(list_deal[0]['comparison_start'])) + ','
            if isinstance(list_deal[0]['comparison_len'], str):
                excelstr += list_deal[0]['comparison_len'] + ','
            elif isinstance(list_deal[0]['comparison_len'], float):
                excelstr += str(int(list_deal[0]['comparison_len'])) + ','
            excelstr += ']],['
            if isinstance(list_deal[0]['message_nu'], str):
                excelstr += '[' + list_deal[0]['message_nu'] + ','
            elif isinstance(list_deal[0]['message_nu'], float):
                excelstr += '[' + str(int(list_deal[0]['message_nu'])) + ','
            if isinstance(list_deal[0]['message'], str):
                excelstr += '\'' + list_deal[0]['message'].replace(' ', '').upper() + '\',]'
            elif isinstance(list_deal[0]['message'], float):
                excelstr += '\'' + str(int(list_deal[0]['message'])).replace(' ', '').upper() + '\',]'
            excelstr += ']]'
        else:
            if list_deal[0]['task_nu'] == list_deal[1]['task_nu']:
                excelstr += '['
                if isinstance(list_deal[0]['task_nu'], str):
                    excelstr += list_deal[0]['task_nu'] + ','
                elif isinstance(list_deal[0]['task_nu'], float):
                    excelstr += str(int(list_deal[0]['task_nu'])) + ','
                if isinstance(list_deal[0]['addr'], str):
                    excelstr += '\'05' + list_deal[0]['addr'] + '\','
                elif isinstance(list_deal[0]['addr'], float):
                    excelstr += '\'05' + str(int(list_deal[0]['addr'])) + '\','
                if isinstance(list_deal[0]['start_id'], str):
                    excelstr += list_deal[0]['start_id'] + ','
                elif isinstance(list_deal[0]['start_id'], float):
                    excelstr += str(int(list_deal[0]['start_id'])) + ','
                if isinstance(list_deal[0]['finish_id'], str):
                    excelstr += list_deal[0]['finish_id'] + ','
                elif isinstance(list_deal[0]['finish_id'], float):
                    excelstr += str(int(list_deal[0]['finish_id'])) + ','
                excelstr += '['
                if isinstance(list_deal[0]['report_wait'], str):
                    if list_deal[0]['report_wait'] == '0:不上报':
                        excelstr += '0,'
                    elif list_deal[0]['report_wait'] == '1:上报':
                        excelstr += '1,'
                if isinstance(list_deal[0]['overtime'], str):
                    excelstr += list_deal[0]['overtime'] + ','
                elif isinstance(list_deal[0]['overtime'], float):
                    excelstr += str(int(list_deal[0]['overtime'])) + ','
                if isinstance(list_deal[0]['result_comparison'], str):
                    if list_deal[0]['result_comparison'] == '0:不比对':
                        excelstr += '0,'
                    elif list_deal[0]['result_comparison'] == '1:比对':
                        excelstr += '1,'
                    elif list_deal[0]['result_comparison'] == '2: 比对上报':
                        excelstr += '2,'
                excelstr += '['
                if isinstance(list_deal[0]['comparison_bytes'], str):
                    excelstr += list_deal[0]['comparison_bytes'] + ','
                elif isinstance(list_deal[0]['comparison_bytes'], float):
                    excelstr += str(int(list_deal[0]['comparison_bytes'])) + ','
                if isinstance(list_deal[0]['comparison_start'], str):
                    excelstr += list_deal[0]['comparison_start'] + ','
                elif isinstance(list_deal[0]['comparison_start'], float):
                    excelstr += str(int(list_deal[0]['comparison_start'])) + ','
                if isinstance(list_deal[0]['comparison_len'], str):
                    excelstr += list_deal[0]['comparison_len'] + ','
                elif isinstance(list_deal[0]['comparison_len'], float):
                    excelstr += str(int(list_deal[0]['comparison_len'])) + ','
                excelstr += ']],['
                for i in range(list_len):
                    if isinstance(list_deal[i]['message_nu'], str):
                        excelstr += '[' + list_deal[i]['message_nu'] + ','
                    elif isinstance(list_deal[i]['message_nu'], float):
                        excelstr += '[' + str(int(list_deal[i]['message_nu'])) + ','
                    if isinstance(list_deal[i]['message'], str):
                        excelstr += '\'' + list_deal[i]['message'].replace(' ', '') + '\',]'
                    elif isinstance(list_deal[i]['message'], float):
                        excelstr += '\'' + str(int(list_deal[i]['message'])).replace(' ', '') + '\',]'
                    excelstr += ','
                excelstr += ']]'
            else:
                # excelstr += '['
                for i in range(list_len):
                    if isinstance(list_deal[i]['task_nu'], str):
                        excelstr += '[' + list_deal[i]['task_nu'] + ','
                    elif isinstance(list_deal[i]['task_nu'], float):
                        excelstr += '[' + str(int(list_deal[i]['task_nu'])) + ','
                    if isinstance(list_deal[i]['addr'], str):
                        excelstr += '\'05' + list_deal[i]['addr'] + '\','
                    elif isinstance(list_deal[i]['addr'], float):
                        excelstr += '\'05' + str(int(list_deal[i]['addr'])) + '\','
                    if isinstance(list_deal[i]['start_id'], str):
                        excelstr += list_deal[i]['start_id'] + ','
                    elif isinstance(list_deal[i]['start_id'], float):
                        excelstr += str(int(list_deal[i]['start_id'])) + ','
                    if isinstance(list_deal[i]['finish_id'], str):
                        excelstr += list_deal[i]['finish_id'] + ','
                    elif isinstance(list_deal[i]['finish_id'], float):
                        excelstr += str(int(list_deal[i]['finish_id'])) + ','
                    excelstr += '['
                    if isinstance(list_deal[i]['report_wait'], str):
                        if list_deal[i]['report_wait'] == '0:不上报':
                            excelstr += '0,'
                        elif list_deal[i]['report_wait'] == '1:上报':
                            excelstr += '1,'
                    if isinstance(list_deal[i]['overtime'], str):
                        excelstr += list_deal[i]['overtime'] + ','
                    elif isinstance(list_deal[i]['overtime'], float):
                        excelstr += str(int(list_deal[i]['overtime'])) + ','
                    if isinstance(list_deal[i]['result_comparison'], str):
                        if list_deal[i]['result_comparison'] == '0:不比对':
                            excelstr += '0,'
                        elif list_deal[i]['result_comparison'] == '1:比对':
                            excelstr += '1,'
                        elif list_deal[i]['result_comparison'] == '2: 比对上报':
                            excelstr += '2,'
                    excelstr += '['
                    if isinstance(list_deal[i]['comparison_bytes'], str):
                        excelstr += list_deal[i]['comparison_bytes'] + ','
                    elif isinstance(list_deal[i]['comparison_bytes'], float):
                        excelstr += str(int(list_deal[i]['comparison_bytes'])) + ','
                    if isinstance(list_deal[i]['comparison_start'], str):
                        excelstr += list_deal[i]['comparison_start'] + ','
                    elif isinstance(list_deal[i]['comparison_start'], float):
                        excelstr += str(int(list_deal[i]['comparison_start'])) + ','
                    if isinstance(list_deal[i]['comparison_len'], str):
                        excelstr += list_deal[i]['comparison_len'] + ','
                    elif isinstance(list_deal[i]['comparison_len'], float):
                        excelstr += str(int(list_deal[i]['comparison_len'])) + ','
                    excelstr += ']],['
                    if isinstance(list_deal[i]['message_nu'], str):
                        excelstr += '[' + list_deal[i]['message_nu'] + ','
                    elif isinstance(list_deal[i]['message_nu'], float):
                        excelstr += '[' + str(int(list_deal[i]['message_nu'])) + ','
                    if isinstance(list_deal[i]['message'], str):
                        excelstr += '\'' + list_deal[i]['message'].replace(' ', '') + '\',]'
                    elif isinstance(list_deal[i]['message'], float):
                        excelstr += '\'' + str(int(list_deal[i]['message'])).replace(' ', '') + '\',]'
                    excelstr += ']'
                    excelstr += '],'
        excelstr += '],'
        if isinstance(list_deal[0]['save_depth'], str):
            excelstr += list_deal[0]['save_depth'] + ']'
        elif isinstance(list_deal[0]['save_depth'], float):
            excelstr += str(int(list_deal[0]['save_depth'])) + ']'
        excel = {int(list_deal[0]['task_id']): excelstr}
        exceldict.update(excel)
    return exceldict


# 601C上报方案
def task_601C(list):
    exceldict = {}
    list_msg = []
    for item in list:
        list_msg.append(list[item])
    set_mark = {list_param['task_id'] for list_param in list_msg}
    ver_name = [i for i in set_mark]
    # print(ver_name)
    ver_name.sort()
    list_name_template = 'task_id'
    list_all = locals()
    # 将所有任务按照任务id分别存储 命名方式为task_id？     ？是任务号
    for mark in set_mark:
        list_all[list_name_template + mark] = [dict_current for dict_current in list_msg if
                                               dict_current['task_id'] == mark]
    for i in ver_name:
        excelstr = ''
        list_deal = list_all['task_id' + i]
        list_len = len(list_deal)
        if isinstance(list_deal[0]['task_id'], str):
            excelstr += '[' + list_deal[0]['task_id'] + ','
        elif isinstance(list_deal[0]['task_id'], float):
            excelstr += '[' + str(int(list_deal[0]['task_id'])) + ','
        if isinstance(list_deal[0]['report_passageway'], str):
            excelstr += '[' + report_handle(list_deal[0]['report_passageway']) + '],'
        if isinstance(list_deal[0]['report_nu'], str):
            excelstr += '\'' + list_deal[0]['report_nu'] + list_deal[0]['report_time'] + '\','
        elif isinstance(list_deal[0]['report_nu'], float):
            excelstr += '\'' + str(int(list_deal[0]['report_nu'])) + list_deal[0]['report_time'] + '\','
        if isinstance(list_deal[0]['retry'], str):
            excelstr += list_deal[0]['retry'] + ','
        elif isinstance(list_deal[0]['retry'], float):
            excelstr += str(int(list_deal[0]['retry'])) + ','
        if isinstance(list_deal[0]['type'], str):
            if list_deal[0]['type'] == '0:对象属性数据':
                excelstr += '[0,'
                if isinstance(list_deal[0]['select_oad'], str):
                    excelstr += '\'' + list_deal[0]['select_oad'] + '\''
                elif isinstance(list_deal[0]['select_oad'], float):
                    excelstr += '\'' + str(int(list_deal[0]['select_oad'])) + '\'' + ']'
            elif list_deal[0]['type'] == '1:上报记录型对象属性':
                excelstr += '[1,['
                if isinstance(list_deal[0]['select_oad'], str):
                    excelstr += '\'' + list_deal[0]['select_oad'] + '\','
                elif isinstance(list_deal[0]['select_oad'], float):
                    excelstr += '\'' + str(int(list_deal[0]['select_oad'])) + '\','
                excelstr += '['
                if isinstance(list_deal[0]['oad'], str):
                    oadstr = list_deal[0]['oad'].split(',')
                    for item in oadstr:
                        excelstr += '\'' + item + '\','
                    if isinstance(list_deal[0]['main_oad'], str) and list_deal[0]['main_oad'] != '':
                        if list_len != 1:
                            for len_oad in range(0, list_len):
                                road_str = list_deal[len_oad]['relation_oad'].split(',')
                                excelstr += oad_handle(list_deal[0]['main_oad'])
                                for item in road_str:
                                    excelstr += '\'' + item + '\','
                                excelstr += '],'
                        else:
                            road_str = list_deal[0]['relation_oad'].split(',')
                            excelstr += oad_handle(list_deal[0]['main_oad'])
                            for item in road_str:
                                excelstr += '\'' + item + '\','
                            excelstr += '],'
                        excelstr += ']'
                    elif list_deal[0]['main_oad'] == '':
                        road_str = list_deal[0]['relation_oad'].split(',')
                        # excelstr += '['
                        for item in road_str:
                            excelstr += '\'' + item + '\','
                        excelstr += ']'
                excelstr += ',['
                if isinstance(list_deal[0]['select'], str):
                    excelstr += '\'' + '选择' + list_deal[0]['select'] + '\','
                if isinstance(list_deal[0]['time_start'], str) and list_deal[0]['time_start'] != '':
                    excelstr += '[\'' + time_handle(list_deal[0]['time_start']) + '\','
                elif list_deal[0]['time_start'] == '':
                    excelstr += '['
                if isinstance(list_deal[0]['time_end'], str) and list_deal[0]['time_end'] != '':
                    excelstr += '\'' + time_handle(list_deal[0]['time_end']) + '\','
                if isinstance(list_deal[0]['interval_time'], str) and list_deal[0]['select'] != '方法10':
                    excelstr += '\'' + list_deal[0]['interval_time'] + list_deal[0]['interval'] + '\','
                elif isinstance(list_deal[0]['interval_time'], float) and list_deal[0]['select'] != '方法10':
                    excelstr += '\'' + str(int(list_deal[0]['interval_time'])) + list_deal[0]['interval'] + '\','
                elif isinstance(list_deal[0]['interval_time'], float):
                    excelstr += str(int(list_deal[0]['interval_time'])) + list_deal[0]['interval'] + ','
                if isinstance(list_deal[0]['ms_type'], str):
                    excelstr += ms_handle(list_deal[0]['ms_type'], list_deal[0]['ms'])
                excelstr += ']]]'
            excelstr += ']]'
        excel = {int(list_deal[0]['task_id']): excelstr}
        exceldict.update(excel)
    return exceldict


# 6012任务方案
def task_6012(list):
    exceldict = {}
    ss = []
    # print(list)
    for item in list:
        ss.append(item)
    for item in list:
        excelstr = ''
        if isinstance(list[item]['task_id'], str):
            excelstr += '[' + list[item]['task_id'] + ','
        elif isinstance(list[item]['task_id'], float):
            excelstr += '[' + str(int(list[item]['task_id'])) + ','
        if isinstance(list[item]['frequency_time'], str):
            excelstr += '\'' + list[item]['frequency_time']
        elif isinstance(list[item]['frequency_time'], float):
            excelstr += '\'' + str(int(list[item]['frequency_time']))
        if isinstance(list[item]['frequency'], str):
            excelstr += list[item]['frequency'] + '\','
        elif isinstance(list[item]['frequency_time'], float):
            excelstr += str(int(list[item]['frequency'])) + '\','
        if isinstance(list[item]['type_plan'], str):
            if list[item]['type_plan'] == '1:普通采集方案':
                excelstr += '1' + ','
            elif list[item]['type_plan'] == '2:事件采集方案':
                excelstr += '2' + ','
            elif list[item]['type_plan'] == '3:透明方案':
                excelstr += '3' + ','
            elif list[item]['type_plan'] == '4:上报方案':
                excelstr += '4' + ','
            elif list[item]['type_plan'] == '5:脚本方案':
                excelstr += '5' + ','
        if isinstance(list[item]['plan_id'], str):
            excelstr += list[item]['plan_id'] + ','
        elif isinstance(list[item]['plan_id'], float):
            excelstr += str(int(list[item]['plan_id'])) + ','
        if isinstance(list[item]['time_start'], str):
            excelstr += '\'' + time_handle(list[item]['time_start']) + '\','
        elif isinstance(list[item]['time_start'], float):
            excelstr += '\'' + time_handle(str(int(list[item]['time_start']))) + '\','
        if isinstance(list[item]['time_end'], str):
            excelstr += '\'' + time_handle(list[item]['time_end']) + '\','
        elif isinstance(list[item]['time_end'], float):
            excelstr += '\'' + time_handle(str(int(list[item]['time_end']))) + '\','
        if isinstance(list[item]['time_delay'], str):
            excelstr += '\'' + list[item]['time_delay']
        elif isinstance(list[item]['time_delay'], float):
            excelstr += '\'' + str(int(list[item]['time_delay']))
        if isinstance(list[item]['delay_unit'], str):
            excelstr += list[item]['delay_unit'] + '\','
        elif isinstance(list[item]['delay_unit'], float):
            excelstr += str(int(list[item]['delay_unit'])) + '\','
        if isinstance(list[item]['priority'], str):
            excelstr += list[item]['priority'] + ','
        elif isinstance(list[item]['priority'], float):
            excelstr += str(int(list[item]['priority'])) + ','
        if isinstance(list[item]['state'], str):
            if list[item]['state'] == '1:正常':
                excelstr += '1' + ','
            elif list[item]['state'] == '2:停用':
                excelstr += '2' + ','
        elif isinstance(list[item]['state'], float):
            if list[item]['state'] == '1:正常':
                excelstr += '1' + ','
            elif list[item]['state'] == '2:停用':
                excelstr += '2' + ','
        if isinstance(list[item]['id_front'], str):
            excelstr += list[item]['id_front'] + ','
        elif isinstance(list[item]['id_front'], float):
            excelstr += str(int(list[item]['id_front'])) + ','
        if isinstance(list[item]['id_back'], str):
            excelstr += list[item]['id_back'] + ',['
        elif isinstance(list[item]['id_back'], float):
            excelstr += str(int(list[item]['id_back'])) + ',['
        if isinstance(list[item]['function'], str):
            if list[item]['function'] == '0:前闭后开':
                excelstr += '0,['
            elif list[item]['function'] == '1:前开后闭':
                excelstr += '1,['
            elif list[item]['function'] == '2:前闭后闭':
                excelstr += '2,['
            elif list[item]['function'] == '3:前开后开':
                excelstr += '3,['
        if isinstance(list[item]['function_time'], str):
            timelist1 = list[item]['function_time'].split(',')
            if len(timelist1) > 1:
                for item1 in timelist1:
                    excelstr += '['
                    for items in item1.split('~'):
                        timelist = []
                        timelist += items.split(':')
                        excelstr += str(int(timelist[0])) + ',' + str(int(timelist[1])) + ','
                    excelstr += '],'
            else:
                excelstr += '['
                timelist = []
                for itime in list[item]['function_time'].split('~'):
                    timelist += itime.split(':')
                excelstr += str(int(timelist[0])) + ',' + str(int(timelist[1])) + ',' + str(
                    int(timelist[2])) + ',' + str(int(timelist[3]))
                excelstr += ']'
        excelstr += ']]]'
        excel = {int(list[item]['task_id']): excelstr}
        exceldict.update(excel)
    return exceldict


# 终端数据筛选
def task_select(list):
    exceldict = {}
    list_msg = []
    for item in list:
        list_msg.append(list[item])
    set_mark = {list_param['task_id'] for list_param in list_msg}
    ver_name = [i for i in set_mark]
    ver_name.sort()
    list_name_template = 'task_id'
    list_all = locals()
    # 将所有任务按照任务id分别存储 命名方式为task_id？     ？是任务号
    for mark in set_mark:
        list_all[list_name_template + mark] = [dict_current for dict_current in list_msg if
                                               dict_current['task_id'] == mark]
    for i in ver_name:
        list_deal = list_all['task_id' + i]
        list_len = len(list_deal)
        excelstr = ''
        # if isinstance(list_deal[0]['select_oad'], str):
        #     excelstr += list_deal[0]['select_oad'] + ','
        # elif isinstance(list_deal[0]['select_oad'], float):
        #     excelstr += str(int(list_deal[0]['select_oad'])) + ','
        if isinstance(list_deal[0]['select'], str):
            if list_deal[0]['select'] == '方法1':
                excelstr += '[\'' + '选择方法1' + '\','
                if isinstance(list_deal[0]['oad'], str):
                    excelstr += '\'' + list_deal[0]['oad'] + '\','
                elif isinstance(list_deal[0]['oad'], float):
                    excelstr += '\'' + str(int(list_deal[0]['oad'])) + '\','
                    #wm新增 20201208
                if isinstance(list_deal[0]['start'], str) and list_deal[0]['start'].find('/')>=0 :
                    excelstr += '\'' + time_handle(list_deal[0]['start']) + '\'],'
                elif isinstance(list_deal[0]['start'], float):
                    excelstr += str(int(list_deal[0]['start'])) + '],'
                elif isinstance(list_deal[0]['start'], str) :
                    excelstr += list_deal[0]['start'] + '],'
                else:pass
                excelstr += '['
                if isinstance(list_deal[0]['main_oad'], str) and list_deal[0]['main_oad'] != '':
                    excelstr += '\'' + list_deal[0]['main_oad'] + '\''
                    #wm20201208
                if isinstance(list_deal[0]['rcsd_oad'], str) and list_deal[0]['rcsd_oad'] != '' and list_deal[0]['rcsd_oad'].find(',')>=0:
                    rcsdoadlist=list_deal[0]['rcsd_oad'].split(',')
                    for rcsdoaditem in rcsdoadlist:
                        excelstr += '\'' + rcsdoaditem + '\','
                elif isinstance(list_deal[0]['rcsd_oad'], str) and list_deal[0]['rcsd_oad'] != '':
                    excelstr += '\'' + list_deal[0]['rcsd_oad'] + '\''
                excelstr += ']'
            elif list_deal[0]['select'] == '方法2':
                excelstr += '[\'' + '选择方法2' + '\','
                if isinstance(list_deal[0]['oad'], str):
                    excelstr += '\'' + list_deal[0]['oad'] + '\','
                elif isinstance(list_deal[0]['oad'], float):
                    excelstr += '\'' + str(int(list_deal[0]['oad'])) + '\','
                if isinstance(list_deal[0]['interval'], str) and list_deal[0]['interval'] != '':
                    if isinstance(list_deal[0]['start'], str):
                        excelstr += '\'' + time_handle(list_deal[0]['start']) + '\','
                    if isinstance(list_deal[0]['end'], str):
                        excelstr += '\'' + time_handle(list_deal[0]['end']) + '\','
                    if isinstance(list_deal[0]['interval'], str):
                        if isinstance(list_deal[0]['interval_time'], str):
                            # wm 增加 时间结束时  ] 1209
                            excelstr += '\'' + list_deal[0]['interval_time'] + list_deal[0]['interval'] + '\']'
                else:
                    if isinstance(list_deal[0]['start'], str):
                        excelstr += list_deal[0]['start'] + ','
                    elif isinstance(list_deal[0]['start'], float):
                        excelstr += str(int(list_deal[0]['start'])) + ','
                    if isinstance(list_deal[0]['end'], str):
                        excelstr += list_deal[0]['end'] + ','
                    elif isinstance(list_deal[0]['end'], float):
                        excelstr += str(int(list_deal[0]['end'])) + ','
                    if isinstance(list_deal[0]['interval_time'], str):
                        excelstr += list_deal[0]['interval_time'] + ']'
                    elif isinstance(list_deal[0]['interval_time'], float):
                        excelstr += str(int(list_deal[0]['interval_time'])) + ']'
                excelstr += ',['
                if isinstance(list_deal[0]['main_oad'], str) and list_deal[0]['main_oad'] != '':
                    excelstr += '\'' + list_deal[0]['main_oad'] + '\''
                if isinstance(list_deal[0]['rcsd_oad'], str) and list_deal[0]['rcsd_oad'] != '' and list_deal[0]['rcsd_oad'].find(',')>=0:
                    rcsdoadlist=list_deal[0]['rcsd_oad'].split(',')
                    for rcsdoaditem in rcsdoadlist:
                        excelstr += '\'' + rcsdoaditem + '\','
                elif isinstance(list_deal[0]['rcsd_oad'], str) and list_deal[0]['rcsd_oad'] != '':
                    excelstr += '\'' + list_deal[0]['rcsd_oad'] + '\''
                else:
                    excelstr += ''
                excelstr += ']'
            elif list_deal[0]['select'] == '方法3':
                excelstr += '[\'' + '选择方法3' + '\','
                if len(list_deal) == 1:
                    excelstr += '['
                    if isinstance(list_deal[0]['oad'], str):
                        excelstr += '\'' + list_deal[0]['oad'] + '\','
                    elif isinstance(list_deal[0]['oad'], float):
                        excelstr += '\'' + str(int(list_deal[0]['oad'])) + '\','
                    if isinstance(list_deal[0]['interval'], str) and list_deal[0]['interval'] != '':
                        if isinstance(list_deal[0]['start'], str):
                            excelstr += '\'' + time_handle(list_deal[0]['start']) + '\','
                        if isinstance(list_deal[0]['end'], str):
                            excelstr += '\'' + time_handle(list_deal[0]['end']) + '\','
                        if isinstance(list_deal[0]['interval'], str):
                            if isinstance(list_deal[0]['interval_time'], str):
                                #wm ],20201209
                                excelstr += '\'' + list_deal[0]['interval_time'] + list_deal[0]['interval'] + '\']'
                    else:
                        if isinstance(list_deal[0]['start'], str):
                            excelstr += list_deal[0]['start'] + ','
                        elif isinstance(list_deal[0]['start'], float):
                            excelstr += str(int(list_deal[0]['start'])) + ','
                        if isinstance(list_deal[0]['end'], str):
                            excelstr += list_deal[0]['end'] + ','
                        elif isinstance(list_deal[0]['end'], float):
                            excelstr += str(int(list_deal[0]['end'])) + ','
                        if isinstance(list_deal[0]['interval_time'], str):
                            excelstr += list_deal[0]['interval_time'] + ']'
                        elif isinstance(list_deal[0]['interval_time'], float):
                            excelstr += str(int(list_deal[0]['interval_time'])) + ']'
                    excelstr += '],['
                    if isinstance(list_deal[0]['main_oad'], str) and list_deal[0]['main_oad'] != '':
                        excelstr += '\'' + list_deal[0]['main_oad'] + '\','
                    if isinstance(list_deal[0]['rcsd_oad'], str) and list_deal[0]['rcsd_oad'] != '' and list_deal[0][
                        'rcsd_oad'].find(',') >= 0:
                        rcsdoadlist = list_deal[0]['rcsd_oad'].split(',')
                        for rcsdoaditem in rcsdoadlist:
                            excelstr += '\'' + rcsdoaditem + '\','
                    elif isinstance(list_deal[0]['rcsd_oad'], str) and list_deal[0]['rcsd_oad'] != '':
                        excelstr += '\'' + list_deal[0]['rcsd_oad'] + '\','
                    else:
                        excelstr += ''
                    excelstr += ']'
                elif len(list_deal) > 1:
                    for i in range(len(list_deal)):
                        excelstr += '['
                        if isinstance(list_deal[i]['oad'], str):
                            excelstr += '\'' + list_deal[i]['oad'] + '\','
                        elif isinstance(list_deal[i]['oad'], float):
                            excelstr += '\'' + str(int(list_deal[i]['oad'])) + '\','
                        if isinstance(list_deal[i]['interval'], str) and list_deal[i]['interval'] != '':
                            if isinstance(list_deal[i]['start'], str):
                                excelstr += '\'' + time_handle(list_deal[i]['start']) + '\','
                            if isinstance(list_deal[i]['end'], str):
                                excelstr += '\'' + time_handle(list_deal[i]['end']) + '\','
                            if isinstance(list_deal[i]['interval'], str):
                                if isinstance(list_deal[i]['interval_time'], str):
                                    excelstr += '\'' + list_deal[i]['interval_time'] + list_deal[i]['interval'] + '\''
                        else:
                            if isinstance(list_deal[i]['start'], str):
                                excelstr += list_deal[i]['start'] + ','
                            elif isinstance(list_deal[i]['start'], float):
                                excelstr += str(int(list_deal[i]['start'])) + ','
                            if isinstance(list_deal[i]['end'], str):
                                excelstr += list_deal[i]['end'] + ','
                            elif isinstance(list_deal[i]['end'], float):
                                excelstr += str(int(list_deal[i]['end'])) + ','
                            if isinstance(list_deal[i]['interval_time'], str):
                                excelstr += list_deal[i]['interval_time'] + ']'
                            elif isinstance(list_deal[i]['interval_time'], float):
                                excelstr += str(int(list_deal[i]['interval_time'])) + ']'
                            excelstr += ','
                    excelstr += '],['
                    if isinstance(list_deal[0]['main_oad'], str) and list_deal[0]['main_oad'] != '':
                        excelstr += '\'' + list_deal[0]['main_oad'] + '\''
                    if isinstance(list_deal[0]['rcsd_oad'], str) and list_deal[0]['rcsd_oad'] != '':
                        excelstr += '\'' + list_deal[0]['rcsd_oad'] + '\''
                    else:
                        excelstr += ''
                    excelstr += ']'
                # excelstr += ']'
            elif list_deal[0]['select'] == '方法9':
                excelstr += '[\'' + '选择方法9' + '\','
                #wm新增 20201210
                if list_deal[0]['oad']== '':
                    pass
                elif isinstance(list_deal[0]['oad'], str):
                    excelstr += '\'' + list_deal[0]['oad'] + '\','
                elif isinstance(list_deal[0]['oad'], float):
                    excelstr += '\'' + str(int(list_deal[0]['oad'])) + '\','
                if isinstance(list_deal[0]['interval_time'], str):
                    #wm  ]  1209
                    excelstr += list_deal[0]['interval_time'] + '],'
                excelstr += '['
                if isinstance(list_deal[0]['main_oad'], str) and list_deal[0]['main_oad'] != '':
                    excelstr += '\'' + list_deal[0]['main_oad'] + '\''
                if isinstance(list_deal[0]['rcsd_oad'], str) and list_deal[0]['rcsd_oad'] != '' and list_deal[0][
                    'rcsd_oad'].find(',') >= 0:
                    rcsdoadlist = list_deal[0]['rcsd_oad'].split(',')
                    for rcsdoaditem in rcsdoadlist:
                        excelstr += '\'' + rcsdoaditem + '\','
                elif isinstance(list_deal[0]['rcsd_oad'], str) and list_deal[0]['rcsd_oad'] != '':
                    excelstr += '\'' + list_deal[0]['rcsd_oad'] + '\''
                else:pass
                excelstr += ']'
        if isinstance(list[item]['task_id'], str):
            excel = {int(list_deal[0]['task_id']): excelstr}
        elif isinstance(list[item]['task_id'], float):
            excel = {int(list_deal[0]['task_id']): excelstr}

        exceldict.update(excel)
    return exceldict


# 暂时不用
# def collection_programme1(tlist):
#     excelstr = '['
#     ss = []
#     for item in tlist:
#         ss.append(item)
#     set_mark = {tlist[item]['task_id'] for item in tlist}
#     ver_name = {tlist[item] for tlist[item] in set_mark}
#     ver_name.sort()
#     list_name_template = 'task_id_'
#     createver = locals()
#     for mark in set_mark:
#         createver[list_name_template + mark.replace('-', '_')] = [dict_current for dict_current in tlist if
#                                                                   dict_current['date'] == mark]
#         for name in ver_name:
#             print(list_name_template + name + ':', end = '\t')
#         exec('print(' + list_name_template + name + ')')
#
#     for i in range(0, len(ss)):
#         if tlist[ss[i]]['task_id'] == '':
#             pass
#         elif isinstance(tlist[ss[i]]['task_id'], str):
#             excelstr += '[' + tlist[ss[i]]['task_id'] + ','
#         elif isinstance(tlist[ss[i]]['task_id'], float):
#             excelstr += '[' + str(int(tlist[ss[i]]['task_id'])) + ','
#         if tlist[ss[i]]['memory_depth'] == '':
#             pass
#         elif isinstance(tlist[ss[i]]['memory_depth'], str):
#             excelstr += tlist[ss[i]]['memory_depth'] + ',['
#         elif isinstance(tlist[ss[i]]['memory_depth'], float):
#             excelstr += str(int(tlist[ss[i]]['memory_depth'])) + '.['
#         if isinstance(tlist[ss[i]]['collection_type'], str) and tlist[ss[i]]['collection_type'] != '':
#             if tlist[ss[i]]['collection_type'] == '0:采集当前数据':
#                 excelstr += '0,\'NULL\'],['
#             elif tlist[ss[i]]['collection_type'] == '1:采集上第N次':
#                 excelstr += '1,' + tlist[ss[i]]['collection_count']
#             elif tlist[ss[i]]['collection_type'] == '2:按冻结时标采集':
#                 excelstr += '2,\'NULL\'],['
#             elif tlist[ss[i]]['collection_type'] == '3:按时间间隔采集':
#                 excelstr += '3,' + '\'' + str(int(tlist[ss[i]]['collection_count'])) + tlist[ss[i]][
#                     'collection_unit'] + '\''
#             elif tlist[ss[i]]['collection_type'] == '4:补抄':
#                 excelstr += '4,' + '\'' + str(int(tlist[ss[i]]['collection_count'])) + tlist[ss[i]][
#                     'collection_unit'] + '\',' + '\'' + tlist[ss[i]]['collection_patch'] + '\'],'
#         else:
#             # list[ss[i]]['collection_type'] == '':
#             pass
#
#         if isinstance(tlist[ss[i]]['oad_main'], str) and tlist[ss[i]]['oad_main'] != '':
#             if i == (len(ss) - 1):
#                 pass
#             else:
#                 if isinstance(tlist[ss[i + 1]]['memory_depth'], str) and tlist[ss[i + 1]]['memory_depth'] != '':
#                     if tlist[ss[i]]['oad_main'] == '秒冻结(5001)':
#                         excelstr += '\'50010200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                     elif tlist[ss[i]]['oad_main'] == '分钟冻结(5002)':
#                         excelstr += '\'50020200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                     elif tlist[ss[i]]['oad_main'] == '小时冻结(5003)':
#                         excelstr += '\'50030200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                     elif tlist[ss[i]]['oad_main'] == '日冻结(5004)':
#                         excelstr += '\'50040200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                     elif tlist[ss[i]]['oad_main'] == '结算日(5005)':
#                         excelstr += '\'50050200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                     elif tlist[ss[i]]['oad_main'] == '月冻结(5006)':
#                         excelstr += '\'50060200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                     elif tlist[ss[i]]['oad_main'] == '年冻结(5007)':
#                         excelstr += '\'50070200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                 elif isinstance(tlist[ss[i + 1]]['memory_depth'], str) and tlist[ss[i + 1]]['memory_depth'] == '':
#                     if tlist[ss[i]]['oad_main'] == '秒冻结(5001)':
#                         excelstr += '\'50010200\',[\'' + tlist[ss[i]]['oad'] + '\'],'
#                     elif tlist[ss[i]]['oad_main'] == '分钟冻结(5002)':
#                         excelstr += '\'50020200\',[\'' + tlist[ss[i]]['oad'] + '\'],'
#                     elif tlist[ss[i]]['oad_main'] == '小时冻结(5003)':
#                         excelstr += '\'50030200\',[\'' + tlist[ss[i]]['oad'] + '\'],'
#                     elif tlist[ss[i]]['oad_main'] == '日冻结(5004)':
#                         excelstr += '\'50040200\',[\'' + tlist[ss[i]]['oad'] + '\'],'
#                     elif tlist[ss[i]]['oad_main'] == '结算日(5005)':
#                         excelstr += '\'50050200\',[\'' + tlist[ss[i]]['oad'] + '\'],'
#                     elif tlist[ss[i]]['oad_main'] == '月冻结(5006)':
#                         excelstr += '\'50060200\',[\'' + tlist[ss[i]]['oad'] + '\'],'
#                     elif tlist[ss[i]]['oad_main'] == '年冻结(5007)':
#                         excelstr += '\'50070200\',[\'' + tlist[ss[i]]['oad'] + '\'],'
#                 else:
#                     if tlist[ss[i]]['oad_main'] == '秒冻结(5001)':
#                         excelstr += '\'50010200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                     elif tlist[ss[i]]['oad_main'] == '分钟冻结(5002)':
#                         excelstr += '\'50020200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                     elif tlist[ss[i]]['oad_main'] == '小时冻结(5003)':
#                         excelstr += '\'50030200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                     elif tlist[ss[i]]['oad_main'] == '日冻结(5004)':
#                         excelstr += '\'50040200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                     elif tlist[ss[i]]['oad_main'] == '结算日(5005)':
#                         excelstr += '\'50050200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                     elif tlist[ss[i]]['oad_main'] == '月冻结(5006)':
#                         excelstr += '\'50060200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#                     elif tlist[ss[i]]['oad_main'] == '年冻结(5007)':
#                         excelstr += '\'50070200\',[\'' + tlist[ss[i]]['oad'] + '\']]'
#         elif tlist[ss[i]]['oad_main'] == '':
#             oadstr = tlist[ss[i]]['oad'].split(',')
#             # print(oadstr)
#             for item in oadstr:
#                 excelstr += '\'' + item + '\','
#             excelstr += ']'
#
#         if i == 1:
#             if tlist[ss[i + 1]]['collection_type'] == '':
#                 pass
#             else:
#                 excelstr += ','
#         elif i == (len(ss) - 1):
#             pass
#         elif tlist[ss[i + 1]]['collection_type'] == '':
#             pass
#         # elif list[ss[i]]
#     # print(excelstr)
#     return item
#     return
def tasklist(listname, listtype):
    str1 = str(listname)
    str2 = str(listtype)
    return readexcel(path + '/' + '面向对象协议参数配置表.xlsx', str1, str2)


def main():  # 王梦新增，方便调试
    task6014list = readexcel(path + '/' + '面向对象协议参数配置表.xlsx', u'普通采集方案(6014)', 'task6014')
    record6012list = readexcel(path + '/' + '面向对象协议采集参数配置表.xlsx', u'记录表(6012)', 'record6012')
    task6012list = readexcel(path + '/' + '面向对象协议参数配置表.xlsx', u'任务(6012)', 'task6012')
    task6000list = readexcel(path + '/' + '面向对象协议参数配置表.xlsx', u'档案(6000)', 'task6000')
    task6016list = readexcel(path + '/' + '面向对象协议参数配置表.xlsx', u'事件采集方案(6016)', 'task6016')
    task6018list = readexcel(path + '/' + '面向对象协议参数配置表.xlsx', u'透明方案(6018)', 'task6018')
    task601Clist = readexcel(path + '/' + '面向对象协议参数配置表.xlsx', u'上报方案(601C)', 'task601C')
    taskselectlist = readexcel(path + '/' + '面向对象协议参数配置表.xlsx', u'参数筛选', 'taskselect')
    task6014list_01 = readexcel(path + '/' + '面向对象协议采集参数配置表.xlsx', u'普通采集方案(6014)_01', 'task6014')
    task6012list_01 = readexcel(path + '/' + '面向对象协议采集参数配置表.xlsx', u'任务(6012)_01', 'task6012')
    planselectlist_01 = readexcel(path + '/' + '面向对象协议采集参数配置表.xlsx', u'终端数据筛选', 'taskselect')
    listtaskselect = task_select(taskselectlist)
    # list6014 = task_6014(task6014list)
    # list6012test = collection_6012(record6012list)
    # list6012task = task_6012(task6012list)
    # list6000list = task_6000(task6000list)
    # list6016task = task_6016(task6016list)
    # list6018task = task_6018(task6018list)
    # list601Ctask = task_601C(task601Clist)
    list60140 = task_6014(task6014list_01)
    # list60120task = task_6012(task6012list_01)
    listtaskselect_01= task_select(planselectlist_01)
    # rtutypeoadlist = rtutypeoad(path + '/' + '面向对象协议采集参数配置表.xlsx', u'能源控制器OAD选择', '','')
    # collection_programme(tasklist)
    print(listtaskselect_01)
    return


if __name__ == '__main__':
    main()
