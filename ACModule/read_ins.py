import numpy as np
import PublicLib.Protocol.dl645format as fat


def dl645_readins(DI, ins, pn=3):
    strDI = fat.hex2str(DI, 0)
    strdata = ''
    e = []

    # 电压 02010101 ~ 02010300
    if '0201' == strDI[:4]:
        if DI[2] == 1:
            e = [ins[0][0]]
        elif DI[2] == 2 and pn == 3:
            e = [ins[0][1]]
        elif DI[2] == 3 and pn == 3:
            e = [ins[0][2]]
        elif DI[2] == -1 and pn == 3:
            e = ins[0][:3]
        elif DI[2] == -1 and pn == 1:
            e = [ins[0][0]]

        for i in range(len(e)):
            strdata += fat.dl645_xxx_x2hex(e[i])
        return strdata

    # 电流 02020100 ~ 02020300
    if '0202' == strDI[:4]:
        if DI[2] == 1:
            e = [ins[1][0]]
        elif DI[2] == 2 and pn == 3:
            e = [ins[1][1]]
        elif DI[2] == 3 and pn == 3:
            e = [ins[1][2]]
        elif DI[2] == 0:
            e = [ins[1][3]]
        elif DI[2] == -1 and pn == 3:
            e = ins[1]
        elif DI[2] == -1 and pn == 1:
            e = [ins[1][3]]

        for i in range(len(e)):
            strdata += fat.dl645_xxx_xxx2hex(e[i], 1)
        return strdata

    # 有功功率 02030000 ~ 02030300
    if '0203' == strDI[:4]:
        if DI[2] == 1:
            e = [ins[3][0]]
        elif DI[2] == 2 and pn == 3:
            e = [ins[3][1]]
        elif DI[2] == 3 and pn == 3:
            e = [ins[3][2]]
        elif DI[2] == 0:
            e = [ins[3][3]]
        elif DI[2] == -1 and pn == 3:
            e = ins[3]
        elif DI[2] == -1 and pn == 1:
            e = [ins[3][3]]

        for i in range(len(e)):
            strdata += fat.dl645_xx_xxxx2hex(e[i], 1)
        return strdata

    # 无功功率 02040000 ~ 02040300
    if '0204' == strDI[:4] and pn == 3:
        if DI[2] == 1:
            e = [ins[4][0]]
        elif DI[2] == 2:
            e = [ins[4][1]]
        elif DI[2] == 3:
            e = [ins[4][2]]
        elif DI[2] == 0:
            e = [ins[4][3]]
        elif DI[2] == -1:
            e = ins[4]

        for i in range(len(e)):
            strdata += fat.dl645_xx_xxxx2hex(e[i], 1)
        return strdata

    # 视在功率 02050000 ~ 02050300
    if '0205' == strDI[:4] and pn == 3:
        if DI[2] == 1:
            e = [(ins[3][0] ** 2 + ins[4][0] ** 2) ** 0.5]
        elif DI[2] == 2:
            e = [(ins[3][1] ** 2 + ins[4][1] ** 2) ** 0.5]
        elif DI[2] == 3:
            e = [(ins[3][2] ** 2 + ins[4][2] ** 2) ** 0.5]
        elif DI[2] == 0:
            e = [(ins[3][3] ** 2 + ins[4][3] ** 2) ** 0.5]
        elif DI[2] == -1:
            e = (ins[3] ** 2 + ins[4] ** 2) ** 0.5

        for i in range(len(e)):
            strdata += fat.dl645_xx_xxxx2hex(e[i], 1)
        return strdata

    # 功率因数 02060000~ 02060300
    if '0206' == strDI[:4] and pn == 3:
        if DI[2] == 1:
            e = [np.cos(ins[2][0] * np.pi / 180)]
        elif DI[2] == 2:
            e = [np.cos(ins[2][1] * np.pi / 180)]
        elif DI[2] == 3:
            e = [np.cos(ins[2][2] * np.pi / 180)]
        elif DI[2] == 0:
            e = [np.cos(np.sum(ins[2]) * np.pi / 180)]
        elif DI[2] == -1:
            ins[2][3] = np.sum(ins[2])
            e = np.cos(ins[2] * np.pi / 180)

        for i in range(len(e)):
            strdata += fat.dl645_x_xxx2hex(e[i], 1)
        return strdata

    # 相角 02070100 ~ 02070300
    if '0207' == strDI[:4] and pn == 3:
        if DI[2] == 0:
            e = [ins[2][0]]
        elif DI[2] == 1:
            e = [ins[2][1]]
        elif DI[2] == 2:
            e = [ins[2][2]]
        elif DI[2] == -1:
            e = ins[2][:3]

        for i in range(len(e)):
            strdata += fat.dl645_xxx_x2hex(e[i])
        return strdata

    return strdata
