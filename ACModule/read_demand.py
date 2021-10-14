import PublicLib.Protocol.dl645format as fat


def dl645_readdemand(DI, eng, pn=3):
    # demand  [相位][类型][0]
    e = []

    if DI[1] == 0x80 and DI[2] == 0x00 and DI[3] == 0x03:  # 一分钟有功总平均功率
        e = [eng[0][0][0]]
    elif DI[1] == 0x80 and DI[2] == 0x00 and DI[3] == 0x04:  # 当前有功需量
        e = [eng[0][0][0]]
    elif DI[1] == 0x80 and DI[2] == 0x00 and DI[3] == 0x05:  # 当前无功需量
        e = [eng[0][1][0]]
    elif DI[1] == 0x80 and DI[2] == 0x00 and DI[3] == 0x06:  # 当前视在需量
        e = [(eng[0][0][0]**2 + eng[0][1][0]**2) ** 0.5]

    strdata = ''
    for i in range(len(e)):
        strdata += fat.dl645_xx_xxxx2hex(e[i], 1)
    return strdata
