

# 563412 ->123456
def reverse(data):
    string = ''
    for i in range(len(data)-1, -1, -2):
        string += data[i-1]
        string += data[i]
    return string

# add // N字节地址
# vxd // 逻辑地址0，终端，1，交采，2：逻辑地址2（扩展规约）#20200915王梦新增
# type // 地址类型0,表示单地址，1表示通配地址，2表示组地址，3表示广播地址
# 输出字符串
def makeTSA(type, vxd, add):
    # print('type, vxd, add:',type, vxd, add)
    stmp = ''
    sbin = bin(type).replace('0b', '').zfill(2)
    sbin += bin(vxd).replace('0b', '').zfill(2)
    if len(add) % 2 == 1: add = add.zfill((len(add)//2+1)*2)
    # 扩展规约：回路巡检，考虑逻辑地址是2的情况
    if vxd == 2:
        sbin += bin(len(add) // 2 ).replace('0b', '').zfill(4)
    else:
        sbin += bin(len(add) // 2 - 1).replace('0b', '').zfill(4)
    stmp = hex(int(sbin,2)).replace('0x', '').zfill(2)
    #扩展规约：回路巡检，考虑逻辑地址是2的情况
    if vxd == 2:
        stmp +="02"
    else:pass
    stmp += reverse(add)
    return  stmp


# num 数值
# 输出字符串倒置
def makelen(num):
    temp = '0000'
    if isinstance(num, float) == False:
        return temp
    ss = hex(int(num)).replace('0x', '').zfill(4)
    temp = reverse(ss)
    # print(temp)
    return temp

# 获取位状态   istart:Dn, iend:Dn-1, lbytes 字节数
def getbit(data,istart,iend,lbytes):
    if len(data) == 0: return False, ''
    sbin = bin(int(data,16)).replace('0b', '').zfill(lbytes*8)
    # print(sbin)
    ilen = len(sbin)
    if istart>ilen or iend > ilen: return False, ''
    stmp = sbin[lbytes*8-iend:lbytes*8-istart]
    return stmp

# number->hexbuff
def numbertohex(ndata, nlen):
    hexbuff = ''
    if isinstance(ndata, int):
        aa= hex(ndata)
        hexbuff =aa[2:]
        hexbuff=hexbuff.zfill(nlen)
        hexbuff=hexbuff[:nlen]
        hexbuff=hexbuff.upper()
    elif isinstance(ndata, float):
        ndata=int(ndata)
        aa = hex(ndata)
        hexbuff = aa[2:]
        hexbuff = hexbuff.zfill(nlen)
        hexbuff = hexbuff[:nlen]
        hexbuff = hexbuff.upper()
    elif isinstance(ndata, str):
        ndata = int(ndata)
        aa = hex(ndata)
        hexbuff = aa[2:]
        hexbuff = hexbuff.zfill(nlen)
        hexbuff = hexbuff[:nlen]
        hexbuff = hexbuff.upper()
    return hexbuff

def chinese_hex(value):#中文转16进制
    res = value.encode("gb2312")
    aa = str(res)
    aa = aa.strip("'").replace(r"\x", '')[2:]
    return aa

def visibletobuff(s): # 以gb2312的编码格式，组帧成16进制
    cc = bytes(s, 'gb2312')
    ee = ""
    for x in cc:
        dd = str(hex(x))
        ee += dd[2:].zfill(2)
    return ee,len(ee)/2

#  2100->33
def stoint(buff):
    if len(buff) != 4:
        return 0
    return int(reverse(buff), 16)

# 'CTRL_BS': {'C_DIR': [7, 7, 0], 'C_PRM': [6, 6, 1], 'C_SEG': [5, 5, 0], 'C_NULL': [4, 4, 0],
# 'C_CODE': [3, 3, 0], 'C_AFN': [0, 2, 3]},
def GetCTRL_BS(data):
    dtmp = {}
    dtmp['C_DIR'] = [7, 7, int(getbit(data, 7, 8, 1), 2)]
    dtmp['C_PRM'] = [6, 6, int(getbit(data, 6, 7, 1), 2)]
    dtmp['C_SEG'] = [5, 5, int(getbit(data, 5, 6, 1), 2)]
    dtmp['C_NULL'] = [4, 4, int(getbit(data, 4, 5, 1), 2)]
    dtmp['C_CODE'] = [3, 3, int(getbit(data, 3, 4, 1), 2)]
    dtmp['C_AFN'] = [0, 2, int(getbit(data, 0, 3, 1), 2)]
    return dtmp


# 'SA_BS': {'SA_TYPE': [6, 7, 0], 'SA_VS': [4, 5, 0], 'SA_LEN': [0, 3, 5]},
def GetSA_BS(data):
    dtmp = {}
    dtmp['SA_TYPE'] = [6, 7, int(getbit(data, 6, 8, 1), 2)]
    dtmp['SA_VS'] = [4, 5, int(getbit(data, 4, 6, 1), 2)]
    dtmp['SA_LEN'] = [0, 3, int(getbit(data, 0, 4, 1), 2) + 1 ]
    return dtmp

# 'SEG_WORD_BS': {'SEG_INDEX': [0, 11, 0], 'SEG_NULL': [12, 13, 0], 'SEG_TYPE': [14, 15, 0]}
def GetSEG_WORD_BS(data):
    dtmp = {}
    dtmp['SEG_INDEX'] = [0, 11, int(getbit(data, 0, 12, 2), 2)]
    dtmp['SEG_NULL'] = [12, 13, int(getbit(data, 12, 14, 2), 2)]
    dtmp['SEG_TYPE'] = [14, 15, int(getbit(data, 14, 16, 2), 2)]
    return dtmp

# 加扰码加33  0022->3355
def Add33(data):
    stmp = ''
    for i in range(0, len(data), 2):
        itm = (int(data[i:i+2], 16) + 0x33) % 256
        stmp += hex(itm).replace('0x', '').zfill(2)
    return stmp

# 加扰码减33  3355->0022
def Reduce33(data):
    stmp = ''
    for i in range(0, len(data), 2):
        itm = (int(data[i:i+2], 16) - 0x33) % 256
        stmp += hex(itm).replace('0x', '').zfill(2)
    return stmp

# sTimeTag "无时间标签" 10秒， 5分  此流程为无时间标签或有效时间标签
def makeTimeTag(sTimeTag):
    bdata = ''
    if sTimeTag == "无时间标签":
        bdata += "00"
    else:
        bdata += "01"
        bdata += makenowtodatetime_s()
        bdata += makebydatatype(DT_TI, sTimeTag)
    return bdata

def makenowtodatetime_s():
    hextime = ""
    n = datetime.datetime.now()
    # print("时间格式：",n)
    hextime += hex(n.year).replace('0x', '').zfill(4)
    hextime += hex(n.month).replace('0x', '').zfill(2)
    hextime += hex(n.day).replace('0x', '').zfill(2)
    hextime += hex(n.hour).replace('0x', '').zfill(2)
    hextime += hex(n.minute).replace('0x', '').zfill(2)
    hextime += hex(n.second).replace('0x', '').zfill(2)
    return  hextime

# now -> datetime_s  wrong  n  ->0707E30B1A00012F
#王梦新增：无效时标
def makewrongdatetime_s():
    hextime = ""
    n=datetime.datetime(2020,3,1,0,0,0,0)
    # print("时间格式：",n)
    hextime += hex(n.year).replace('0x', '').zfill(4)
    hextime += hex(n.month).replace('0x', '').zfill(2)
    hextime += hex(n.day).replace('0x', '').zfill(2)
    hextime += hex(n.hour).replace('0x', '').zfill(2)
    hextime += hex(n.minute).replace('0x', '').zfill(2)
    hextime += hex(n.second).replace('0x', '').zfill(2)
    return  hextime

# dtype 数据类型，value数值 ->buff   原不考虑换算流程！！！
def makebydatatype(dtype, value):
    bdata = ''
    if dtype == DT_NULL:
        bdata += ''
    elif dtype == DT_bool:
        bdata += valuetoboolbuff(value)
    elif dtype == DT_unsigned or dtype == DT_enum:
         if ( isinstance(value, str))and(value.find("_")) >=0:
             bb = value.split("_")
             cc = bin(int(bb[1], 10))[2:]
             dd = bin(int(bb[0], 10))[2:]
             ee = str(cc) + str(dd)
             bdata+=str( hex(int(ee, 2))[2:])
         elif( isinstance(value, str)) and((value.find(",")) >=0):#王梦新增：终端工控人视化转为机器识别（02020101->01011010）
             bdata+=mantobin(value)
         else:
             bdata += valuetounsignedbuff(value)
    elif dtype == DT_integer:
        bdata += inttohex(value)
    elif dtype == DT_date_time_s:
        bdata += valuetodtsbuff(value)
        #王梦新增
    elif dtype == DT_time:
        bdata += valuetotbuff(value)

    elif dtype == DT_long_unsigned:
        bdata += valuetolongusingedbuff(value, 0)
    elif dtype == DT_double_long:#王梦新增：考虑到传入参数为负数的情况（DT_long可参考改流程）
        bdata += valuetodoublelongbuff(value, 0)
    elif dtype == DT_long:  # 王梦新增：考虑到传入参数为负数的情况（DT_long可参考改流程）
        bdata += valuetolongbuff(value, 0)
    elif dtype == DT_long64:  # 王梦新增：考虑到传入参数为负数的情况（DT_long可参考改流程）
        bdata += valuetolong64buff(value, 0)

    elif dtype == DT_OAD:
        bdata += value
    elif dtype == DT_TSA:
        bdata += valuetoTSAbuff(value)
    elif dtype == DT_octet_string:
        bdata += valuetooctetstringbuff(value)
    elif dtype == DT_visible_string:  # 王梦新增
        bdata += valuetovisiblestringbuff(value,0)
    elif dtype == DT_bit_string:  # 王梦新增
        bdata += valuetobitstringbuff(value)
    elif dtype == DT_TI:
        bdata += valuetoTIbuff(value)
    elif dtype == DT_facjtype:
        bdata += valuetofacjtypebuff(value)
        # print('makebydatatype 完成处理类型DT_facjtype==', dtype, value, bdata)
    elif dtype == DT_eventtype:
        bdata += valuetoeventtypebuff(value)
    elif dtype == DT_MS:
        bdata += valuetoMSbuff(value)
    elif dtype == DT_reporttype:
        bdata += valuetoreporttypebuff(value)
    elif dtype == DT_MS:
        bdata += valuetoMSbuff(value)
    elif dtype == DT_double_long_unsigned:
        bdata += valuetodoublebuff(value,0)


    elif dtype == DT_CSD:
        bdata += valuetoDTCSDbuff(value)
    elif dtype == DT_OI:
        bdata += value

    else:
        print('makebydatatype 增加处理类型', dtype, value)
    return bdata
