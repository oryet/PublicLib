import time
from PublicLib.Protocol.ly_Json import *


# 心跳回复
def socket_json_heartbeat(ret_str):
    #  json登陆、心跳、事件自动回复
    if 'Login' in ret_str or 'Heart' in ret_str or 'Event' in ret_str:
        return bytes(ret_str + " ", encoding="utf-8")
    return None


# 查询IMEI
def socket_json_inquire_imei(ret_str):
    #  登陆查询IMEI
    if 'Login' in ret_str:
        # ret_str = "{'Len':'312','Cmd':'UserDef','SN':'2','DataTime':'180706121314','CRC':'FFFF','DataValue':{'F0000002':'','F0000003':''}}"

        parm = {}
        parm['Cmd'] = 'UserDef'
        DIList = ['F0000002', 'F0000003']
        ValueList = ['', '']
        dv = dict(zip(DIList, ValueList))
        parm['DataValue'] = dv

        ret_str = JsonMakeFrame(parm)
        ret_str = ret_str.replace('\"','\'') # 替换单双引号
        ret_str = ret_str.replace(' ', '') # 去空格
        return bytes(ret_str + " ", encoding="utf-8")
    return None


# Json socket处理接口
def socket_json(ret_str, conn):
    ret_byte = socket_json_heartbeat(ret_str)
    if ret_byte:
        conn.sendall(ret_byte)
    time.sleep(1)
    ret_byte = socket_json_inquire_imei(ret_str)
    if ret_byte:
        conn.sendall(ret_byte)
