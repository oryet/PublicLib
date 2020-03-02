import json
import re
import PublicLib.public as pfun
import time

g_cnt = 0


def subStrToJson(data):
    if data == None:
        return None
    # 原因在于：字符串里用单引号来标识字符
    data = re.sub('\'', '\"', data)
    data = re.sub('\n', '', data)

    # 字符串 转 json
    try:
        data_json = json.loads(data)
        if not IsJsonFrame(data_json):
            return None
    except:
        print(data)
        return None
    # addr = data_json['DataValue']['04A20208']
    # print(addr)
    return data_json


def IsJsonFrame(data):
    if data == None:
        return False

    if data['Len']:
        if (data['Cmd']):
            if (data['SN']):
                if (data['DataTime']):
                    if (data['CRC']):
                        if (data['DataValue']):
                            return  True
    return False


def JsonParse(data):
    if (data['Len']):
        if (data['Cmd']):
            if (data['SN']):
                if (data['DataTime']):
                    if (data['CRC']):
                        if (data['DataValue']):
                            return [data['DataValue']]
    return [False]


def JsonDealFrame(recvframe, senddata, answer):
    json_frame = recvframe  # subStrToJson(recvframe)
    json_senddata = senddata  # subStrToJson(senddata)

    if isinstance(json_frame, dict) is False:
        return -1, None
    if isinstance(json_senddata, dict) is False:
        return -1, None

    # 接收帧 去除头部结构
    if "recvData" in json_frame:
        json_frame = json_frame["recvData"]

    if json_frame is not None and json_senddata is not None:
        if isinstance(json_frame, str):
            json_frame = json.loads(json_frame)
        if isinstance(json_senddata, str):
            json_senddata = json.loads(json_senddata)

        if json_senddata["Cmd"] == json_frame["Cmd"]:
            if json_senddata["DataValue"].keys() == json_frame["DataValue"].keys():
                value = list(json_frame["DataValue"].values())[0]
                if value == answer:
                    return 1, value
    return -1, None


# parm
# key:cmd  value:Read/Set/..
# DataValue dict key1:value1 ... key n:value n
def JsonMakeFrame(parm):
    global g_cnt
    g_cnt = g_cnt + 1
    if g_cnt > 9999:
        g_cnt = 0

    datatime = time.strftime("%y%m%d%H%M%S", time.localtime())
    data = dict(Len="312", Cmd=parm["Cmd"], SN=str(g_cnt), DataTime=datatime, CRC="FFFF", DataValue=parm["DataValue"])

    # 计算CRC
    dv = '\'DataValue\'' + ':' + str(parm["DataValue"]).replace(' ', '')
    dv = "0000" + pfun.crc16str(0, dv, False)
    data["CRC"] = dv[-4:]

    # 计算长度
    data["Len"] = str(len(str(data)) - 12)

    # 将python对象data转换json对象
    data_json = json.dumps(data, ensure_ascii=False)

    # 将json对象转换成python对象
    # data_python = json.loads(data_json)

    return data_json


'''
def JsonMakeValue(DIlist):
    for i in DIlist:
        Value =
'''

if __name__ == '__main__':
    # 数据项和内容
    DIList = ['05060101', '05060102', '05060103']
    ValueList = ['000000.00', '123.14', '778899']
    List = dict(zip(DIList, ValueList))

    MakeFramePara = {}
    MakeFramePara['Cmd'] = 'Set'
    MakeFramePara['DataValue'] = List

    # CRC16 IBM： E8FE

    # 元组转json
    # DIValue = json.loads(data_python)

    # json 转 字符串
    data_python = JsonMakeFrame(MakeFramePara)
    print(data_python)

    # 字符串 转 json
    data = json.loads(data_python)
    JsonDealFrame(data_python, data, "000000.00")

    # a = JsonParse(data)
    '''
    for key in a:
        print(key)
    # print(a.key())
    #for key in a.iterkeys():
    print(a.values())
    for value in a.values():
        print(value)
    '''
