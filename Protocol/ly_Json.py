import json
import re
import PublicLib.public as pfun
import time

g_cnt = 0


def subStrToJson(data):
    if data == None:
        return False, None
    # 原因在于：字符串里用单引号来标识字符
    data = re.sub('\'', '\"', data)
    data = re.sub('\n', '', data)

    # 字符串 转 json
    try:
        data_json = json.loads(data)
        if not IsJsonFrame(data_json):
            return False, 'Error_Json'
    except:
        print(data)
        return False, data
    # addr = data_json['DataValue']['04A20208']
    # print(addr)
    return True, data_json


# 自定义 json 格式判断
def IsJsonFrame(dictdata):
    if dictdata is None:
        return False

    if isinstance(dictdata, dict) is False:
        return False

    dictlist = ['Len', 'Cmd', 'SN', 'DataTime', 'CRC', 'DataValue']
    for k in dictlist:
        if k not in dictdata:
            return False
    return True


# dict recv, dict send
# dict expect answer
#      answer
#      answer result
#  int threshold
def JsonDealFrame(recvframe, senddata, answer):
    answer['answerresult'] = {}
    if not IsJsonFrame(recvframe) or not IsJsonFrame(senddata):
        answer['result'] = 'frame error'
        return

    # 接收帧 去除头部结构
    if "recvData" in recvframe:
        recvframe = recvframe["recvData"]

    #  帧序号相同
    if recvframe['SN'] != senddata['SN']:
        answer['result'] = 'sn error'
        return

    # 控制字相同
    if recvframe['Cmd'] != senddata['Cmd']:
        answer['result'] = 'cmd error'
        return

    '''
    # 预估返回值相同
    threshold = answer['threshold']
    answer['answer'] = recvframe['DataValue'].copy()
    answer['answerresult'] = recvframe['DataValue'].copy()

    for i, j in recvframe['DataValue'].items():
        if i in answer['expectanswer']:
            # threshold 判断：
            # 0： 绝对相等
            # 1： 门限内相等
            # -1： 不判断
            if threshold == 0:
                if answer['expectanswer'][i] == j:
                    answer['answerresult'][i] = 'ok'
                else:
                    answer['answerresult'][i] = 'error'
            elif threshold == -1:
                answer['answerresult'][i] = 'ok'
            else:
                recvvalue = float(j)
                answervalue = float(answer['expectanswer'][i])
                if answervalue * (1 - threshold) <= recvvalue <= answervalue * (1 + threshold):
                    answer['answerresult'][i] = 'ok'
                else:
                    answer['answerresult'][i] = 'error'
    '''
    return


# parm
# key:cmd  value:Read/Set/..
# DataValue dict key1:value1 ... key n:value n
def JsonMakeFrame(parm):
    global g_cnt
    g_cnt = g_cnt + 1
    if g_cnt > 9999:
        g_cnt = 0

    if "Cmd" in parm and "DataValue" in parm:
        datatime = time.strftime("%y%m%d%H%M%S", time.localtime())
        data = dict(Len="312", Cmd=parm["Cmd"], SN=str(g_cnt), DataTime=datatime, CRC="FFFF", DataValue=parm["DataValue"])

        # 计算CRC
        dv = str(parm["DataValue"]).replace(' ', '')
        dv = "0000" + pfun.crc16str(0, dv[1:-1], False)
        data["CRC"] = dv[-4:]

        # 计算长度
        data["Len"] = str(len(str(data)) - 12)
    else:
        data = dict(frame = 'error')

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

def testMakeFrame():
    # 数据项和内容
    # DIList = ['05060101', '05060102', '05060103']
    # ValueList = ['000000.00', '123.14', '778899']
    DIList = ['04A00501']
    ValueList = [
        '594C#03#03BC#0001#0001CA910001CA5D0001C9F50001EAE30001BCC50001BC810001BCA10001C9CD0001C9A50001C97D0001AF130001C9550001C92D0001E8D30001C92B0001D4AB0000973D00006DC300000000000000000001E8C7000000000000000000000000000000000000000000000000000000000001C9290001CC670001F1F1200009A8']
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
    ret = IsJsonFrame(data)
    print(ret)
    '''
    if ret:
        # dict expect answer
        #      answer
        #      answer result
        #  int threshold
        dictanswer = {'threshold': 0.1, 'expectanswer': List}
        JsonDealFrame(data, data, dictanswer)
        for k in dictanswer:
            print(dictanswer[k])

        List['05060102'] = '199.29'
        dictanswer = {'threshold': 0.1, 'expectanswer': List}
        JsonDealFrame(data, data, dictanswer)
        for k in dictanswer:
            print(dictanswer[k])

    a = JsonParse(data)
    for key in a:
        print(key)
    # print(a.key())
    #for key in a.iterkeys():
    print(a.values())
    for value in a.values():
        print(value)
    '''

if __name__ == '__main__':
    testMakeFrame()

