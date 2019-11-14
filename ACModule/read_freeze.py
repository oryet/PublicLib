import datetime
import PublicLib.Protocol.dl645format as fat


def dl645_freezetime(type, t, n):
    if type == 'day':
        if 0 < n <= 62:
            t -= (24*3600*(n-1))
        else:
            return ''
    else:
        pass
    dt_obj = datetime.datetime.fromtimestamp(t)
    # date_str = dt_obj.strftime("%y%m%d%H%M%S")
    date_str = dt_obj.strftime("000000%d%m%y")
    return date_str


def dl645_readfreday(DI, eng, pn=3):
    e = []
    strdata = ''

    if eng is None:
        return strdata

    # 05060101 ~ 05060A01
    if DI[2] == 0x01:  # (当前)正向有功总电能
        e = eng[0][0][:5]
    elif DI[2] == 0x02 and pn == 3:  # (当前)反向有功总电能
        e = eng[0][1][:5]
    elif DI[2] == 0x05 and pn == 3:  # (当前)第一象限无功总电能
        e = eng[0][2][:5]
    elif DI[2] == 0x06 and pn == 3:  # (当前)第二象限无功总电能
        e = eng[0][3][:5]
    elif DI[2] == 0x07 and pn == 3:  # (当前)第三象限无功总电能
        e = eng[0][4][:5]
    elif DI[2] == 0x08 and pn == 3:  # (当前)第四象限无功总电能
        e = eng[0][5][:5]
    elif DI[2] == 0x03 and pn == 3:  # 组合无功1 = 一/二象限相加
        e = eng[0][2][:5] + eng[0][3][:5]
    elif DI[2] == 0x04 and pn == 3:  # 组合无功2 = 三/四象限相加
        e = eng[0][4][:5] + eng[0][5][:5]

    for i in range(len(e)):
        strdata += fat.dl645_xxxxxx_xx2hex(e[i])
    return strdata

def dl645_readfremonth(DI, eng, pn=3):
    e = []
    strdata = ''

    if eng is None:
        return strdata

    if DI[1] == 0x01:  # (当前)正向有功总电能
        if DI[2] == -1:
            e = eng[0][0][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][0][DI[2]]]
    elif DI[1] == 0x02 and pn == 3:  # (当前)反向有功总电能
        if DI[2] == -1:
            e = eng[0][1][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][1][DI[2]]]
    elif DI[1] == 0x00:  # (当前)组合有功 = Bit0(有功+)  Bit2(无功+)
        if DI[2] == -1:
            e = eng[0][0][:5] + eng[0][1][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][0][DI[2]] + eng[0][1][DI[2]]]
    elif DI[1] == 0x05 and pn == 3:  # (当前)第一象限无功总电能
        if DI[2] == -1:
            e = eng[0][2][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][2][DI[2]]]
    elif DI[1] == 0x06 and pn == 3:  # (当前)第二象限无功总电能
        if DI[2] == -1:
            e = eng[0][3][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][3][DI[2]]]
    elif DI[1] == 0x07 and pn == 3:  # (当前)第三象限无功总电能
        if DI[2] == -1:
            e = eng[0][4][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][4][DI[2]]]
    elif DI[1] == 0x08 and pn == 3:  # (当前)第四象限无功总电能
        if DI[2] == -1:
            e = eng[0][5][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][5][DI[2]]]
    elif DI[1] == 0x03 and pn == 3:  # 组合无功1 = 一/二象限相加
        if DI[2] == -1:
            e = eng[0][2][:5] + eng[0][3][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][2][DI[2]] + eng[0][3][DI[2]]]
    elif DI[1] == 0x04 and pn == 3:  # 组合无功2 = 三/四象限相加
        if DI[2] == -1:
            e = eng[0][4][:5] + eng[0][5][:5]
        elif 0 <= DI[2] <= 8:
            e = [eng[0][4][DI[2]] + eng[0][5][DI[2]]]

    elif DI[1] == 0x15 and pn == 3:  # (当前)A相正向有功电能
        e = eng[1][0][:1]
    elif DI[1] == 0x29 and pn == 3:  # (当前)B相正向有功电能
        e = eng[2][0][:1]
    elif DI[1] == 0x3d and pn == 3:  # (当前)C相正向有功电能
        e = eng[3][0][:1]

    for i in range(len(e)):
        strdata += fat.dl645_xxxxxx_xx2hex(e[i])
    return strdata

def dl645_readcure():
    pass