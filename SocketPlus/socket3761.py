# 3761心跳回复
def socket3761_heartbeat(ret_str, p):
    ret_str = p.LoginHeartFrame(ret_str)
    if ret_str is not None:
        return bytes.fromhex(ret_str)


# 3761 socket处理接口
def socket3761(ret_str, p, conn):
    ret_byte = socket3761_heartbeat(ret_str, p)
    if ret_byte:
        conn.sendall(ret_byte)
