# coding=utf-8
# !/usr/bin/env python
import json
from collections import OrderedDict
import datetime
from Protocol import crc16ccc

CMD_JSON_LOGIN = 'Login'
CMD_JSON_HEART = 'Heart'
CMD_JSON_READ = 'Read'
CMD_JSON_SET = 'Set'
CMD_JSON_REPORT = 'Report'
CMD_JSON_EVENT = 'Event'
CMD_JSON_UPDATE = 'Update'
CMD_WAIT = 'Wait'
CMD_JSON_TRANS = 'Trans'
CMD_JSON_TRANSET = 'Tset'
CRC_MODE = 1
CMD_READ645 = 'Read645'
CMD_SET645 = 'Set645'
CMD_COM_READ = 'ComRead'
CMD_COM_SET = 'ComSet'
CMD_READ_MODBUS = 'mread'
CMD_SET_MODBUS = 'mset'

CMDSET = ['Login', 'Heart', 'Read', 'Set', 'Report', 'Event', 'Update', 'Trans']


def sumlen(scmd, dlist):
    ilen = 73
    if isinstance(scmd, str):
        ilen += len(scmd)
    if isinstance(dlist, dict):
        sdump = json.dumps(dlist, ensure_ascii=True).replace(': ', ':')
        ilen += len(sdump)
    return ilen


def crcjson(imode, dvalue):
    scrc = ''
    if imode == 1:
        # print dvalue
        sjy = str(dvalue)
        sjy = sjy .replace('{', '')
        sjy = sjy.replace('}', '')
        sjy = sjy.replace(' ', '')
        sjy = sjy.replace('u','')
        # print sjy
        icrc = crc16ccc.crc16ly(sjy)
        scrc = ("%04x" % icrc).upper()
    else:
        icrc = 65535
        scrc = ('%04x' % icrc).upper()
    return scrc


# make dict
def makepjson(scmd, isn, dlst):
    if isinstance(scmd, str) and isinstance(isn, int) and isinstance(dlst, dict) and scmd in CMDSET:
        orderd = OrderedDict()
        orderd['Len'] = '%04d' % sumlen(scmd, dlst)
        orderd['Cmd'] = scmd
        orderd['SN'] = '%04d' % (isn % 9999)
        orderd['DataTime'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')[2:]
        orderd['CRC'] = crcjson(CRC_MODE, dlst)
        orderd['DataValue'] = dlst
    else:
        return False
    return pythontojson(orderd)


# dict to  json
def pythontojson(pdct):
    if isinstance(pdct, OrderedDict):
        return json.dumps(pdct, ensure_ascii=True).replace(' ', '').replace('"', '\'')
    else:
        return False


# json to dict
def jsontopython(sjson):
    if isinstance(sjson, str):
        jsontpython = OrderedDict()
        stem = sjson.replace(':', ': ').replace('\'', '"')
        jsontpython = json.loads(stem, object_pairs_hook=OrderedDict)
    else:
        return False
    return jsontpython


# jsontolink return Read [True, 'Read'}]
def islinkReturn(sjsn, scmd):
    retdict = []
    if sjsn.find('DataValue') == -1:
        retdict.append(False)
        return retdict
    retdict.append(True)
    # print sjsn
    sjsnlst = sjsn.split('}{')
    # print len(sjsnlst)
    for i in range(0, len(sjsnlst), 1):
        if i == 0 and len(sjsnlst)>1:
            sjsnlst[i] = sjsnlst[i] + '}'
        elif i == len(sjsnlst)-1 and len(sjsnlst)>1:
            sjsnlst[i] = '{' + sjsnlst[i]
        elif len(sjsnlst)>1:
            sjsnlst[i] = '{' + sjsnlst[i] + '}'
    # print sjsnlst
    for j in range(0, len(sjsnlst), 1):
        pdct = jsontopython(sjsnlst[j])
        # print pdct
        if pdct['Cmd'].find(scmd) == -1:
            retdict[0] = False
        else:
            retdict[0] = True
            retdict.append(pdct['Cmd'])
    return retdict


# jsonto645 return Read [True, 'Read', '0001FF00, ' ,'0002FF00, ':}]
def isReturn(sjsn, scmd, idlist):
    retdict = []
    if sjsn.find('DataValue') == -1:
        retdict.append(False)
        return retdict
    retdict.append(True)
    # print sjsn
    sjsnlst = sjsn.split('}{')
    # print len(sjsnlst)
    for i in range(0, len(sjsnlst), 1):
        if i == 0 and len(sjsnlst)>1:
            sjsnlst[i] = sjsnlst[i] + '}'
        elif i == len(sjsnlst)-1 and len(sjsnlst)>1:
            sjsnlst[i] = '{' + sjsnlst[i]
        elif len(sjsnlst)>1:
            sjsnlst[i] = '{' + sjsnlst[i] + '}'
    for j in range(0, len(sjsnlst), 1):
        scheck = checkjson(sjsnlst[j])
        bbool = False
        if len(scheck) >= 25:
            pdct = jsontopython(scheck)
            # print pdct
            if pdct['Cmd'].find(scmd) == -1:
                retdict[0] = False
            else:
                retdict[0] = True
                retdict.append(pdct['Cmd'])
            bbool = True
            for ss in range(len(retdict) - 2, 0, -1):
                del (retdict[ss])
            for it in pdct['DataValue']:
                if it in idlist:
                    temd = {it: pdct['DataValue'][it]}
                    retdict.append(temd)
                else:
                    bbool = False
                    break
            if bbool == True:
                break
    if bbool == False:
        retdict[0] = False
    return retdict

# 检查json协议单帧粘包再处理
def checkjson(sjsn):
    rstr = ''
    if len(sjsn) <= 25:
        return rstr
    iend = sjsn.find('\'}}')
    ilen = len(sjsn)
    if iend != ilen-3 and iend != -1:
        sjsn = sjsn[:iend+3]
    istart = sjsn.find('{\'Len\'')
    if istart == -1:
        return rstr
    elif istart >= 0:
        rstr = sjsn[istart:]
    return rstr

# jsonto645 return Read [True, 'Read', '0001FF00, ' ,'0002FF00, ':}]
def updatecrcffff(sjsn):
    sdict = ''
    if sjsn.count('DataValue') != 1 and sjsn.count('Login') == 1:
        sdict = "{'Len':'0126','Cmd':'Login','SN':'133','DataTime':'181029093219','CRC':'FFFF'," \
             "'DataValue':{'04A20209':'000000000006#000000000000#00000000'}}"
        return sdict
    elif sjsn.count('DataValue') != 1 and sjsn.count('Heart') == 1:
        sdict = "{'Len':'0104','Cmd':'Heart','SN':'180','DataTime':'181029102322','CRC':'FFFF'," \
         "'DataValue':{'04A20208':'000000000006'}}"
        return sdict
    pdct = jsontopython(sjsn)
    pdct['CRC'] = 'FFFF'
    sdict = pythontojson(pdct)
    return sdict

# 218.94.38.114:50154转DA5E2672#C3EA
def sIptosHex(sip):
    if len(sip) == 0 or sip.find(':') == -1 or sip.find('.') == -1:
        return ''
    slst = sip.split(':')
    if len(slst) != 2:
        return ''
    schar = slst[0].split('.')
    if len(schar) != 4:
        return ''
    srtn = ''
    try:
        for item in schar:
            srtn += hex(int(item)).upper().replace('0X','')
        srtn += '#'
        srtn += hex(int(slst[1])).upper().replace('0X', '')
    except ValueError:
        return ''
    return srtn

# DA5E2672#C3EA转 218.94.38.114:50154
def sHextosIp(shx):
    if len(shx) != 13 or shx.find('#') == -1:
        return ''
    slst = shx.split('#')
    if len(slst) != 2:
        return ''
    if len(slst[0]) != 8:
        return ''
    srtn = ''
    try:
        for i in range(0,len(slst[0]),2):
            srtn += str(int(slst[0][i:i+2],16))
            if i < 6:
                srtn += '.'
        srtn += ':'
        srtn += str(int(slst[1],16))
    except ValueError:
        return ''
    return srtn


if __name__ == '__main__':
    dct = {'02010200': '', '02010100': '', '02010300': ''}
    scmdd = u'Read'
    m_isn = 1
    # ss = makepjson(scmdd, m_isn, dct)
    # print ss

    s = "{'Len':'0092','Cmd':'Set','SN':'0007','DataTime':'190131235858','CRC':'34f9'," \
        "'DataValue':{'04000102':'Y'}}{'Len':'0102','Cmd':'Heart','SN':'3','DataTime':'190131235859'," \
        "'CRC':'34f9','DataValue':{'04A20208':'000000000008'}}{'Len':'0115','Cmd':'Event','SN':'4'," \
        "'DataTime':'190131235900','CRC':'34f9','DataValue':{'03110001':'190101000611#190101000618'}}"
    sl = "h�h4737�h�h4737�{'Len':'0100','Cmd':'Read','SN':'0055','DataTime':'190516205148','CRC':'FFFF','DataValue':{'04A00101':'01000004'}}"
    sh = "{'Len':'0104','Cmd':'Heart','SN':'180','DataTime':'181029102322','CRC':'2345'," \
         "'DataValue':{'04A20208':'000000000006'}}"
    # print updatecrcffff(s)
    print(sIptosHex('218.94.38.114:50154'))
    print(sHextosIp('DA5E2672#C3EA'))
    data = "{'Len':'0102','Cmd':'Heart','SN':'3','DataTime':'190606085253','CRC':'FFFF','DataValue':{'04A20208':'000000010003'}}"
    bb = isReturn(data, CMD_JSON_HEART, ['04A20208'])
    # print bb
    # print bb[2]['04A20208'][:12]
    # print checkjson(sl)
    # stem = s.replace(':', ': ').replace('\'', '"')
    dct = jsontopython(s)
    print(dct['Len'])
   # print dct['Cmd']
   # print dct['DataTime']
   # print dct['DataValue']
    # print dct['DataValue']['0001FF00']
    # print dct['DataValue']['0002FF00']
    # print dct['DataValue']['0001FF00'].split("#")
    # print dct['DataValue']['0002FF00'].split("#")
   # for item in dct['DataValue']:
   #     print dct['DataValue'][item].split('#')
    # tt = isReturn(sl, CMD_JSON_READ, ['04A00101'])
    # print tt
   # print '00000100' in tt[2]
    # sid = '04A20208'
    # ssss = "{'Len':'0101','Cmd':'Read','SN':'0002','DataTime':'181004015458','CRC':'34f9','DataValue':{'03110001':'000023.97'}}"
    # slst = isReturn(s, CMD_JSON_HEART, [sid])
    # print slst
    #print slst[2][sid]
# 将python对象test 按字典顺序 转换json对象
def testjson():
    # test = [{"username": "测试", "age": 16}, (2, 3), 1]
    orderd = OrderedDict()
    orderd['Len'] = '0259'
    orderd['Cmd'] = 'Event'
    orderd['SN'] = '0001'
    orderd['DataTime'] = '180101184802'
    orderd['CRC'] = '34f9'
    orderd['DataValue'] = {'03110000': '000042', '03300100': '000006', '03300300': '000002',
                           '03300400': '000002', '03400000': '000000', '03400100': '000053',
                           '03400200': '000003', '03400300': '000011', '03400400': '000000'}
    print(orderd)
    print(type(orderd))
    python_to_json = json.dumps(orderd, ensure_ascii=True)
    print(python_to_json)
    print(type(python_to_json))
    #print len(python_to_json)
    # 将json对象转换成python对象
    # json_to_python = OrderedDict()
    #json_to_python = json.loads(python_to_json, object_pairs_hook=OrderedDict)
    #print json_to_python
    #print type(json_to_python)

# print json_to_python['Len']
# print json_to_python['SN']
# print json_to_python['Cmd']
# print json_to_python['DataValue']
# print json_to_python['CRC']
# print len("'Cmd':'','SN':'0001','DataTime':'180925091910','CRC':'34f9','DataValue':}")
# dic1 = {'type':'dic1','username':'loleina','age':16}
# json_dic1 = json.dumps(dic1)
# print json_dic1
# json_dic2 = json.dumps(dic1,sort_keys=True,indent =4,separators=(',', ': '),encoding="gbk",ensure_ascii=True )
# print json_dic2
