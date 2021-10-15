import PublicLib.Protocol.dl645format as fat
import datetime

BLOCK_READ = 0xFF

def dl645_readdemand(DI, demand, pn=3):
    # demand  [相位][类型][0]
    e = []

    if DI[1] == 0x80 and DI[2] == 0x00 and DI[3] == 0x03:  # 一分钟有功总平均功率
        e = [demand[0][0][0]]
    elif DI[1] == 0x80 and DI[2] == 0x00 and DI[3] == 0x04:  # 当前有功需量
        e = [demand[0][0][0]]
    elif DI[1] == 0x80 and DI[2] == 0x00 and DI[3] == 0x05:  # 当前无功需量
        e = [demand[0][1][0]]
    elif DI[1] == 0x80 and DI[2] == 0x00 and DI[3] == 0x06:  # 当前视在需量
        e = [(demand[0][0][0]**2 + demand[0][1][0]**2) ** 0.5]

    strdata = ''
    for i in range(len(e)):
        strdata += fat.dl645_xx_xxxx2hex(e[i], 1)
    return strdata

def dl645_readdemandtime(DI, demand, pn=3):
    # demand  [相位][类型][0]
    e = []

    if DI[1] == 0x01:  # (当前)正向有功总最大需量及发生时间  01010000 ~ 0101FF00
        if DI[2] == BLOCK_READ:
            e = demand[0][0][:5]
        elif 0 <= DI[2] <= 8:
            e = [demand[0][0][DI[2]]]
    elif DI[1] == 0x02:  # (当前)反向有功总最大需量及发生时间  01020000 ~ 0102FF00
        if DI[2] == BLOCK_READ:
            e = demand[0][1][:5]
        elif 0 <= DI[2] <= 8:
            e = [demand[0][1][DI[2]]]
    elif DI[1] == 0x03 and pn == 3:  # 组合无功1 = 一/二象限相加
        if DI[2] == BLOCK_READ:
            e = demand[0][2][:5] + demand[0][3][:5]
        elif 0 <= DI[2] <= 8:
            e = [demand[0][2][DI[2]] + demand[0][3][DI[2]]]
    elif DI[1] == 0x04 and pn == 3:  # 组合无功2 = 三/四象限相加
        if DI[2] == BLOCK_READ:
            e = demand[0][4][:5] + demand[0][5][:5]
        elif 0 <= DI[2] <= 8:
            e = [demand[0][4][DI[2]] + demand[0][5][DI[2]]]
    elif DI[1] == 0x05 and pn == 3:  # (当前)第一象限无功总最大需量及发生时间
        if DI[2] == BLOCK_READ:
            e = demand[0][2][:5]
        elif 0 <= DI[2] <= 8:
            e = [demand[0][2][DI[2]]]
    elif DI[1] == 0x06 and pn == 3:  # (当前)第二象限无功总最大需量及发生时间
        if DI[2] == BLOCK_READ:
            e = demand[0][3][:5]
        elif 0 <= DI[2] <= 8:
            e = [demand[0][3][DI[2]]]
    elif DI[1] == 0x07 and pn == 3:  # (当前)第三象限无功总最大需量及发生时间
        if DI[2] == BLOCK_READ:
            e = demand[0][4][:5]
        elif 0 <= DI[2] <= 8:
            e = [demand[0][4][DI[2]]]
    elif DI[1] == 0x08 and pn == 3:  # (当前)第四象限无功总最大需量及发生时间
        if DI[2] == BLOCK_READ:
            e = demand[0][5][:5]
        elif 0 <= DI[2] <= 8:
            e = [demand[0][5][DI[2]]]


    elif DI[1] == 0x15 and pn == 3:  # (当前)A相正向有功电能
        e = demand[1][0][:1]
    elif DI[1] == 0x29 and pn == 3:  # (当前)B相正向有功电能
        e = demand[2][0][:1]
    elif DI[1] == 0x3d and pn == 3:  # (当前)C相正向有功电能
        e = demand[3][0][:1]

    elif DI[1] == 0x16 and pn == 3:  # (当前)A相反向有功电能
        e = demand[1][1][:1]
    elif DI[1] == 0x2a and pn == 3:  # (当前)B相反向有功电能
        e = demand[2][1][:1]
    elif DI[1] == 0x3e and pn == 3:  # (当前)C相反向有功电能
        e = demand[3][1][:1]

    dt_obj = datetime.datetime.now()
    date_str = dt_obj.strftime("%y%m%d%H%M")

    strdata = ''
    for i in range(len(e)):
        strdata += (fat.dl645_xx_xxxx2hex(e[i]) + date_str)
    return strdata
