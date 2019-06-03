import json
import logging

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

# ByteToHex的转换
def ByteToHex( bins ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    return ''.join( [ "%02X" % x for x in bins ] ).strip()

# HexToByte的转换
def HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    return bytes.fromhex(hexStr)

# 校验计算函数
def calcCheckSum(frame):
    checkSum = 0
    for i in range(0, len(frame), 2):
        checkSum += int(frame[i:i + 2], 16)
    return str(hex(checkSum))[-2:]


# 载入日志配置文件
def loggingConfig(logconf):
    logging.config.fileConfig(logconf)
    logger = logging.getLogger('main')
    logger.info('Logging main Start')


# 载入Json格式配置文件
def loadDefaultSettings(configfile):
    try:
        jsonConfigFile = open(configfile)
        defaultJsonConfig = json.load(jsonConfigFile)
        print(defaultJsonConfig)
    finally:
        if jsonConfigFile:
            jsonConfigFile.close()
            return defaultJsonConfig


