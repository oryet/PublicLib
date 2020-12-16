#!/usr/bin/python
# -*- coding: UTF-8
import sys
sys.path.append("../../..")
from PublicLib.Protocol.ly_Json import *
import time
import random


def onenet_paresdata(res):
    # bytes to str
    data = bytes.decode(res)

    # 将json对象转换成python对象
    data_python = json.loads(data)
    if data_python["errno"] == 0 and data_python["error"] == "succ":
        if 'data' in data_python:
            return True, data_python["data"]
        else:
            return True, None
    else:
        return False, None

def onenet_contjson(content):
    jsondata = bytes.decode(content)

    # 将json对象转换成python对象
    data = json.loads(jsondata)

    count = data["data"]["count"]
    recvtimelist = []
    valuelist = []
    for i in range(count):
        dic = data["data"]["datastreams"][0]["datapoints"][i]

        recvtime = dic["at"]
        value = dic["value"]
        value = subStrToJson(value)
        recvtimelist +=[recvtime]
        valuelist += [value]
    return count,recvtimelist,valuelist


def onenet_makeframe(con, deviceinfo, val):
    # nbiot_url = {"imei": device_imei, "obj_id": obj_id, "obj_inst_id": obj_inst_id, "mode": mode}  # params
    # '3308_0_5750'
    # nbiot_url = {"imei": deviceinfo["rg_id"], "obj_id": deviceinfo["datastreams"][0]["id"][:4],
    #              "obj_inst_id": deviceinfo["datastreams"][0]["id"][5:6], "mode": 2}  # params
    nbiot_url = {"imei": deviceinfo["rg_id"], "obj_id": '3308',
                 "obj_inst_id": '0', "mode": 2}  # params
    nbiot_data = {"data":[{"res_id": '5750', "val": val}]}  # data

    res4 = con.nbiot_write(nbiot_data, nbiot_url)
    return (res4.content)

def onenet_senddata(con, deviceinfo, val):
    if deviceinfo["online"]:
        # 发送数据
        # 其中datastream_id等于obj_id, obj_inst_id, res_id，如obj_id:3200，obj_inst_id:0，res_id:5501，那么这个datastream_id就为3200_0_5501。 ['3308_0_5750']
        # val = "{'Len':'312','Cmd':'Read','SN':'1','DataTime':'180706121314','CRC':'FFFF','DataValue':{'04A50300':'','04A50301':'','04A20201':'','04A50302':'','04A50303':''}}"  # object
        res = onenet_makeframe(con, deviceinfo, val)
        ret, data = onenet_paresdata(res)
        return ret
    return None

# 查询最近10条数据
def onenet_recvdata(con, deviceinfo):
        # res3 = con.datapoint_multi_get(device_id = deviceinfo["id"], limit = 1, datastream_ids = deviceinfo["datastreams"][0]["id"])
        res3 = con.datapoint_multi_get(device_id=deviceinfo["id"], limit=10,
                                       datastream_ids='3308_0_5750')
        count, recvtime, jsonstr = onenet_contjson(res3.content)
        return count, jsonstr


def connectonenet(con, rlist, devlist, nl):
    for j in range(len(nl)):
        for i in range(len(devlist)):
            if i == nl[j]:
                rlist += [[i, con.device_info(device_id=devlist[i])]]
                break
    return rlist

def getdevinfo(res3, device_id):
    # 获取设备信息
    try:
        ret, deviceinfo = onenet_paresdata(res3.content)
        # print('当前测试设备信息', device_id, deviceinfo['auth_info'], 'online:',deviceinfo["online"])
        return ret, deviceinfo
    except:
        return False, None


def getcurinfo(con, rlist, devlist, prelist=None, keyword=None, log=None):
    # 获取设备信息
    # for i in range(len(devlist)):
    for r in rlist:
        i = r[0]
        ret, deviceinfo = getdevinfo(r[1], devlist[i])

        if ret is True: # and deviceinfo["online"]:
            n, data = onenet_recvdata(con, deviceinfo)
            if n > 0:
                for d in data:
                    s = deviceinfo['title'] + ', ' + deviceinfo['rg_id'] + ', ' + str(d)
                    # print(deviceinfo['title'], data[0])
                    if prelist != None and prelist[i] != s:
                        prelist[i] = s
                        print(s)
                        if log is not None:
                            log.info(s)
                    elif keyword is not None and len(keyword) > 0:
                        kcnt = 0
                        for k in keyword:
                            if k in s:
                                kcnt+=1
                        if kcnt == len(keyword):
                            print(s)
                            if log is not None:
                                log.info(s)
                            break
                    else:
                        print(s)
                        if log is not None:
                            log.info(s)
        else:
            # print(deviceinfo['title'], '不在线！ 最近在线时间:',deviceinfo["act_time"])
            try:
                s = deviceinfo['title'] + ', ' + deviceinfo['rg_id'] + ', 不在线！ 最近在线时间:' + deviceinfo["last_ct"]
                if prelist != None and prelist[i] != s:
                    prelist[i] = s
                    print(s)
                    if log is not None:
                        log.info(s)
                else:
                    print(s)
                    if log is not None:
                        log.info(s)
            except:
                pass

def devListSend(con, rlist, devlist, sendstr=None, log=None):
    # 获取设备信息
    # for i in range(len(devlist)):
    for r in rlist:
        i = r[0]
        ret, deviceinfo = getdevinfo(r[1], devlist[i])

        if ret is True and deviceinfo["online"]:
            val = "{'Len':'312','Cmd':'Read','SN':'1','DataTime':'180706121314','CRC':'FFFF','DataValue':{'04A50300':'','04A50301':'','04A20201':'','04A50302':'','04A50303':''}}"  # object
            # val = "{'Len':'312','Cmd':'Set','SN':'2','DataTime':'200428121314','CRC':'FFFF','DataValue':{'04A10101':'01#FF#0096#0005#180901120000#02#05060101#00900200','04A10102':'01#01','04A10103':'01'}}"  # object
            if sendstr != None and sendstr != '':
                sendjson = subStrToJson(sendstr)
                if sendjson != None and IsJsonFrame(sendjson):
                    val = sendstr

            hour = '00' + str(random.randint(0, 7))
            min = '00' + str(random.randint(0, 59))
            sec = '00' + str(random.randint(0, 59))
            ctime = '201029' + hour[-2:] + min[-2:] + sec[-2:]
            val = val.replace('180901120000',ctime)

            for n in range(3):
                sret = onenet_senddata(con, deviceinfo, val)
                print(devlist[i], 'Send:', sret, val)
                if sret:
                    break
                else:
                    time.sleep(7)
            if log is not None:
                log.info(val)
            time.sleep(0.1)

def indexList2List(s, num):
    nl = []
    nsl = s.split(',')
    for s in nsl:
        try:
            n = int(s, 10)
            if n < num:
                nl += [n]
        except:
            continue
    return nl

