# CRC16/IBM x16 + x15 + x2 + 1
def crc16str(base, x, invert):
    a = base
    b = 0xA001
    for byte in x:
        a ^= ord(byte)
        for i in range(8):
            last = a % 2
            a >>= 1
            if last == 1:
                a ^= b
    s = hex(a).upper()
    return s[4:6] + s[2:4] if invert == True else s[2:4] + s[4:6]

# CRC16/IBM x16 + x15 + x2 + 1
def crc16hex(base, x, invert):
    a = base
    b = 0xA001
    for i in range(0, len(x), 2):
        a ^= int(x[i:i+2], 16)
        for i in range(8):
            last = a % 2
            a >>= 1
            if last == 1:
                a ^= b
    s = hex(a).upper()
    return s[4:6] + s[2:4] if invert == True else s[2:4] + s[4:6]


# 字节倒序
def _strReverse(value):
    s = ""
    for i in range(0, len(value), 2):
        s = value[i:i + 2] + s
    return s