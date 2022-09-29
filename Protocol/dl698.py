from FCSccc import *
from prtl698plus import *

MIN_LEN_OOP_FRAME = 36

# 合法帧检查
def CheckValid(buff):
    if len(buff) < MIN_LEN_OOP_FRAME:
        print('Error_Frame length too short')
        return False
    if buff[0:2] == '68':
        ilen = stoint(buff[2:6])
        # print(buff[2+ilen*2:4+ilen*2])
        if (ilen*2+4) > len(buff):
            print('Error_Frame length')
            return False
        if buff[2+ilen*2:4+ilen*2] != '16':
            print('Error_Frame 16')
            return False
        else:
            if OOP_CheckCRC(buff[2:2+ilen*2]):
                return True
            else:
                print('Error_Frame FCS')
                return False
    print('Error_Frame 68')
    return False

def MakeFrame(frame):
    buff = ''
    buff += frame['CTRL']
    buff += makeTSA(frame['TSA_TYPE'], frame['TSA_VS'], frame['TSA_AD'])
    buff += frame['CA']
    buff += frame['SEG_WORD']
    ilen = len(buff)//2
    ilen += 6
    ilen += len(frame['APDU'])/2
    buff = makelen(ilen) + buff
    buff = buff + OOP_CalcCRC(buff)
    buff += frame['APDU']
    buff = buff + OOP_CalcCRC(buff)
    buff = '68'+ buff + '16'
    return buff

# 解析帧
def DL698_GetFrame(buff):
    dfrm = {}
    dfrm['rtn'] = False
    if CheckValid(buff) == False:
        return dfrm
    ipos = 2
    dfrm['LEN'] = stoint(buff[ipos:ipos+4])
    ipos += 4
    dfrm['CTRL'] = buff[ipos:ipos+2]
    ipos += 2
    dfrm['CTRL_BS'] = GetCTRL_BS(dfrm['CTRL'])
    dfrm['SA'] = buff[ipos:ipos+2]
    ipos += 2
    dfrm['SA_BS'] = GetSA_BS(dfrm['SA'])
    dfrm['TSA_TYPE'] = dfrm['SA_BS']['SA_TYPE'][2]
    dfrm['TSA_VS'] = dfrm['SA_BS']['SA_VS'][2]
    dfrm['TSA_AD'] = reverse(buff[ipos:ipos+dfrm['SA_BS']['SA_LEN'][2]*2])
    ipos += dfrm['SA_BS']['SA_LEN'][2]*2
    dfrm['CA'] = buff[ipos:ipos+2]
    ipos += 2
    ipos += 4
    if dfrm['CTRL_BS']['C_CODE'][2] == 0:
        dfrm['APDU'] = buff[ipos: dfrm['LEN']*2 + 4 - 6]
    else:
        dfrm['APDU'] = Reduce33(buff[ipos: dfrm['LEN']*2 + 2 - 6])
    if dfrm['CTRL_BS']['C_SEG'][2] == 1:
        dfrm['SEG_WORD'] = reverse(dfrm['APDU'][0:4])
        dfrm['SEG_WORD_BS'] = GetSEG_WORD_BS(dfrm['SEG_WORD'])
    else:
        dfrm['SEG_WORD'] = ''
        dfrm['SEG_WORD_BS'] = {}
    dfrm['rtn'] = True
    return dfrm

def DL698_LoginHeartFrame(f):
    dt = DL698_GetFrame(f)
    if dt['APDU'][0:2] == '01':
        PIID = dt['APDU'][2:4]
        dt['APDU'] = '81'
        dt['APDU'] += PIID
        dt['APDU'] += '8007E3051B010F290B000007E60802020F28100FA107E60802020F28100FA1'
        ref = MakeFrame(dt)
        return ref
    else:
        return None

if __name__ == '__main__':
    # frame698 = r'68 BB 02 C3 05 00 00 00 00 00 00 00 85 77 85 01 08 F2 13 05 01 01 02 5B 1C 07 E5 08 12 00 00 09 04 20 00 00 00 00 04 20 00 70 D0 00 01 08 10 00 00 10 00 00 10 00 00 10 00 00 10 00 00 10 00 00 10 00 00 10 00 00 06 00 00 00 00 06 00 00 00 00 06 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 12 00 00 12 00 00 12 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 10 27 10 10 27 10 10 27 10 10 27 10 12 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 10 00 00 10 00 00 10 00 00 10 00 00 10 00 00 10 00 00 15 00 00 00 00 AD 95 42 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 1C 07 E5 08 12 00 00 09 15 00 00 00 00 AD 95 42 00 15 00 00 00 00 00 00 00 00 01 03 12 00 00 12 00 00 12 00 00 01 03 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 01 04 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 01 04 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 05 00 00 00 00 01 04 10 03 E8 10 03 E8 10 03 E8 10 03 E8 1C 07 E5 08 12 00 00 09 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 15 00 00 00 00 00 00 00 00 00 00 4C F0 16 '
    frame698 = r'68 1E 00 81 05 01 00 00 00 00 00 00 D2 B6 01 2E 01 01 2C 07 E3 05 1B 01 0F 15 07 00 00 7B 98 16'
    frame698 = frame698.replace(' ', '')
    #dt = DL698_GetFrame(frame698)
    #print(dt)

    #dt['APDU'] = dt['APDU'][:4]
    #dt['APDU']+= '8007E3051B010F290B000007E60802020F28100FA107E60802020F28100FA1'

    #f = MakeFrame(dt)
    #print(f)

    f = DL698_LoginHeartFrame(frame698)
    print(f)