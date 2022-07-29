# -*- coding: utf-8 -*-

import sys
import os
import paramiko
from paramiko import AuthenticationException
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import NoValidConnectionsError
import time
import datetime
import xlrd
import Protocol.General as General



#通过ssh修改文本文件
def ssh_edit_file(ssh,file_in , file_out, key, new):
    # file_in = '/backup/app/libhd.so'
    # key = 'a'
    # new = ''
    # import paramiko, string, os
    c_out = []
    # ssh = paramiko.SSHClient()
    # ssh.load_system_host_keys(os.environ["HOME"] + "/.ssh/known_hosts")
    # ssh.connect(h,username=u)
    ftp = ssh.open_sftp()
    f_in = ftp.file(file_in, "r")
    c_in = f_in.readlines()
    for line in c_in:
        if line.find(key) >= 0:
            c_out.append(new + '\n')
        else:
            s = line
            c_out.append(s)
    f_out = ftp.file(file_out, "w")
    f_out.writelines(c_out)
    f_in.close()
    f_out.close()
    ftp.close()
    ssh.close()
# ===================================================
# str.lstrip() 方法用于截掉字符串左边的空格或指定字符。
# str.replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)
# ste.split() 通过指定分隔符对字符串进行切片

# 吴道文添加，读取配置文件Excel表格和SSH服务通信参数
def getsshini():
    path = os.getcwd().replace('\Protocol', '') + "\config"
    wb = xlrd.open_workbook(path + "\\自动化测试参数配置和方案选择.xlsx")
    table = wb.sheet_by_name(u'自动化程序参数配置')  # 选取正确的sheet页
    colNum = table.ncols  # 获取表格列数
    EC = {}
    for i in range(colNum):
        # print('i:', i, '; Value:',table.row(0)[i].value)
        if "s_IP" in table.row(0)[i].value:
            EC['ServerAddr'] = table.row(1)[i].value
        elif "s_port" in table.row(0)[i].value:
            EC['ServerPort'] = table.row(1)[i].value
        elif "u_name" in table.row(0)[i].value:
            EC['UserName'] = table.row(1)[i].value
        elif "password" in table.row(0)[i].value:
            EC['PassWord'] = table.row(1)[i].value

    return EC

# ===================================================
# global HostName, password, EnergyController, BZT
RBTset = False  # 终端以太网地址(IP)修改标志，Ture：已修改，False：未修改；
EnergyController = getsshini()  # 获取SSH服务器地址、端口，以及用户名和密码
HostName = EnergyController['ServerAddr']
password = EnergyController["PassWord"]
# ===================================================

class SshClient():
    # global EnergyController, HostName
    def __init__(self):
        # EnergyController = getsshini()
        # 设备ssh服务（服务器模式）的通信参数，EnergyController为字典类型{}
        self.myip = EnergyController['ServerAddr']  # 终端以太网静态IP地址
        self.port = EnergyController['ServerPort']  # 终端ssh服务端口
        self.user = EnergyController['UserName']    # 终端登录用户名
        self.passwd = EnergyController['PassWord']  # 终端登录用户的密码
        self.ssh_client = SSHClient()  # 创建一个ssh服务对象
        if self.port == '':
            self.port = 8888  # 如果端口输入为空，则使用默认端口8888
    def ssh_login(self):
        try:
            self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            self.ssh_client.connect(hostname=self.myip, port=self.port,
                                    username=self.user, password=self.passwd)
            print(f'>>>>| {self.user}@{self.myip}:{self.port} & {self.passwd}')  # SSH service connected successfully!
        except AuthenticationException:
            print('【ErrorCode:1001】 ', 'username or password error')
            return 1001
        except NoValidConnectionsError:
            print('【ErrorCode:1002】 ', 'connect time out')
            return 1002
        except:
            print('【ErrorCode:1003】 ', "Unexpected error:", sys.exc_info()[0])
            return 1003
        return 1000

    def execute_some_command(self, command):
        snow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:23]
        global RBTset
        print(f'>>>>| Execution start time: {snow} ; SSH connection successful!')     # 执行开始时间
        print('>>>>|_/SendingCommand\\' + '_'*47)
        print('-->>|：发送命令', command)

        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command, get_pty=True)
            stdin.write(self.passwd + '\r\n')
        except OSError as e:
            print(f'    | Error: {e}')
            # 系统断开SSH服务连接时，自动化重连一次，防止自动化程序因系统错误而不继续下面的任务
            if self.ssh_logout() == 1000:
                stdin, stdout, stderr = self.ssh_client.exec_command(command, get_pty=True)
                stdin.write(self.passwd + '\r\n')
        try:
            if command.find('sudo appm ' or 'sudo container ') >= 0:
                time.sleep(0.5)
            else:
                time.sleep(2)
            if command.find('sudo reboot') >= 0 or command.find('sudo ifconfig FE0 ') >= 0 or  (command.find('top') >= 0):
                # 命令执行时，终端会断开连接，导致自动化程序在死等结果，无法跳出继续执行下面的程序代码
                if 'sudo reboot' in command:
                    if RBTset == True:
                        EnergyController['ServerAddr'] = HostName
                        RBTset = False
                elif ' netmask 255.255.255.0' in command:
                    NewIP = command.split(" ")[3]
                    # NewIP = command.replace("sudo ifconfig FE0 ", "").replace(" netmask 255.255.255.0", "")
                    # 连接网口IP已临时更改，需要即时修改连接IP，重启之前都使用此IP连接
                    EnergyController['ServerAddr'] = NewIP
                    RBTset = True
                else:
                    pass
                time.sleep(1)
                raise ValueError(f'CMD"{command}" [*_*] This link is broken!')
            else:
                sread = stdout.read().decode()
            # print('    | stdout:', stdout)
            # print('    | stderr:', stderr)
        except BaseException as e:
            print('    | ValueError:', e)
            # time.sleep(2)
            sread = 'This link is broken!'
        # sudo 命令：需要输入密码，加入密码输入
        if sread.find("password for sysadm") >= 0:
            print('    | Input PassWord:', password)
            command = self.passwd
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            time.sleep(1)
            sread1 = sread.replace("\r\n\r\n", "\r\n").replace(self.passwd + "\r\n", "") \
                .replace("[sudo] password for sysadm: \r\n", "")
        else:
            sread1 = sread.replace("\r\n\r\n", "\r\n").replace(self.passwd + "\r\n", "")
        if sread1[-2:] == "\r\n":
            sread1 = sread1[:-2].replace("\r\n", "\r\n      ")
        print('<<--|:终端返回值', sread1)
        print('<<--|:终端返回值1', {'sread':sread})

        return sread

    def execute_command(self, command):
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        # stdin.write('Zgdky@guest123\n')
        sread = stdout.read().decode()
        # print('stderr', stderr)
        # print('stdin', stdin)
        return sread

    def ssh_logout(self):
        self.ssh_client.close()

def saveintxt(datarow):
    pathtxt = ''
    savetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    if datarow['save'].find('T_TXT') >= 0:
        pathtxt = os.getcwd() + "\\report\\" + '温度、CPU占有率和频率' + datetime.datetime.now().strftime('%Y%m%d') + '.txt'
    f = open(pathtxt, 'a')
    if datarow['save'].find('CPU_0:') >= 0:
        f.write('\n'+ 'CPU_0:' + savetime +':' + datarow['real'].replace('\n','').replace('\r','：').strip('：'))
    elif datarow['save'].find('CPU_1:') >= 0:
        f.write('\n'+ 'CPU_1:'+ savetime +':' + datarow['real'].replace('\n','').replace('\r','：').strip('：'))
    elif datarow['save'].find('CPU_2:') >= 0:
        f.write('\n'+ 'CPU_2:'+ savetime +':' + datarow['real'].replace('\n','').replace('\r','：').strip('：'))
    elif datarow['save'].find('CPU_3:') >= 0:
        f.write('\n' + 'CPU_3:'+ savetime +':' + datarow['real'].replace('\n', '').replace('\r', '：').strip('：'))
    elif datarow['save'].find('CPU_usage:') >= 0:
        f.write('\n' + 'CPU_usage:'+ savetime +':' + datarow['real'].replace('\n', '').replace('\r', '：').strip('：'))
    else:
        f.write('\n' + '温度:'+ savetime +':' + datarow['real'].replace('\n', '').replace('\r', '：').strip('：'))
    f.close()

#telnet 和 SSH此处的预期值要特殊处理
def mad5valueget(computerreply,realrow):
    if realrow['op'] == 'SSH操作':
        finddata = ":"
    else:
        finddata = realrow['save']
    if computerreply.find(finddata) >=0:
        if finddata == ":":
            md5value = computerreply.split(finddata)[1].strip('\r').strip('\n').strip('\r')[4:]
        else:
            md5value = computerreply.split(finddata)[1].strip().strip('\r').strip('\n').strip('\r')
    else:
        md5value = '未获取MD5值'
    return md5value


def expectequalreal(realrow, computerreply,testexcel):
    realrow['real'] = computerreply
    #被修改后的文件，MD5值会发生变化。
    if realrow['expect'].find("不等于") >= 0:
        expecttemp = realrow['save'].replace('不等于','')
        for itemrow in testexcel:
            if testexcel[itemrow]['save'] == expecttemp:
                mad5value = mad5valueget(computerreply,realrow)
                if testexcel[itemrow]['real'].find(mad5value) >= 0:
                    realrow['result'] = '不合格'
                else:
                    realrow['result'] = '合格'
    else:
        for itemrow in  testexcel:
            if testexcel[itemrow]['save'] == realrow['expect']:
                mad5value = mad5valueget(computerreply,realrow)
                if testexcel[itemrow]['real'].find(mad5value) >= 0:
                    realrow['result'] = '合格'
                else:
                    realrow['result'] = '不合格'
    return None


def expectequalexpect(realrow, computerreply,testexcel):
    # realrow['real'] = computerreply
    if (computerreply.find(realrow['expect']) >= 0) and (computerreply.find('No such file or directory'))<0:
        realrow['result'] = '合格'
    else:
        realrow['result'] = '不合格'

#（停上电和复位用例）跨表格的主区和备份区的召测值与准备工作中的主区和备份区存储好的预期值做比较
def comparemd5(md5_rightvalue,realrow,computerreply):
    for itemrow in md5_rightvalue:
        if itemrow['oad/omd'] == realrow['expect']:
            mad5value = mad5valueget(computerreply, realrow)
            if itemrow['value'].find(mad5value) >= 0:
                realrow['result'] = '合格'
            else:
                realrow['result'] = '不合格'
    return None

def notin(realrow,computerreply):
    realrow['real'] = computerreply
    result = 0
    notindata = realrow['expect'].split(':')[1].split("/,/")
    for item in notindata:
        if item in computerreply:
            result += 1
            break
    if result != 0:
        realrow['result'] = '不合格'
    else:
        realrow['result'] = '合格'
    if result == 1 and realrow['expect'].find('hook.sh') >= 0:
        realrow['result'] = '合格'
    return None



def getdeviceresult(realrow, computerreply,testexcel,md5_rightvalue):
    # snow = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:23]
    print(f'|||||_/执行结果判定\\' + '_' * 50)
    # print(f'>|||| Determine start time : {snow}')
    confindflag = 0
    realdata = ""
    confinddata = ""
    # expectlist = realrow['expect'].split("/,/")
    # 以下判断返回值是否含有用户密码！wdw
    if computerreply.find(password) >= 0:  # 判断返回值是否含有用户密码！wdw
        res_computerreply = computerreply[18:].replace("\r", "")
    else:
        res_computerreply = computerreply
    # 以上判断返回值是否含有用户密码！wdw
    # print('res_computerreply:', res_computerreply)
    # print('|'*70)
    # print({'[实际返回内容]:': res_computerreply})    # 实际返回值
    if res_computerreply == '':
        print('>>>|| [实际返回内容]: NULL(空)')
    # print('>>||| [预期包含内容]:', expectlist)         # 预期判定值Expected Value:
    if realrow['save'].find('FACTORTSPECIALPARAM') >= 0:
        General.factoryparamcheckssh(realrow, computerreply)
    elif realrow['expect'].find('_EXPECT') >= 0:
        expectequalreal(realrow, computerreply,testexcel)
    elif realrow['save'].find('_EXPECT') >= 0:
        realrow['real'] = computerreply
        expectequalexpect(realrow, computerreply,testexcel)
    elif realrow['save'].find('_RIGHTVALUE_') >= 0:
        realrow['real'] = computerreply
        md5_rightvalue = General.covervalue(realrow, md5_rightvalue, realrow['real'])
        expectequalexpect(realrow, computerreply, testexcel)
    elif realrow['expect'].find('_RIGHTVALUE_') >= 0:
        comparemd5(md5_rightvalue, realrow, computerreply)
    elif realrow['save'] == 'STATICMSG':
        realrow['real'] = computerreply
        print({'aaa': realrow['expect']})
        if realrow['expect'] == computerreply:
            realrow['result'] = "合格"
        else:
            realrow['result'] = "不合格"
    elif realrow['save'].find('TXT') >= 0:
        realrow['real'] = computerreply
        saveintxt(realrow)
        realrow['result'] = "合格"
    elif realrow['save'].find('NOTIN') >= 0:
        notin(realrow,computerreply)
    else:
        expectlist = realrow['expect'].split("/,/")
        print('>>||| [预期包含内容]:', expectlist)  # 预期判定值Expected Value:
        NUMYZ = len(expectlist)
        for item in expectlist:
            # print({'item__show': item})
            BAOHANZHI = False
            if 'Value' in item:
                Comp_result = res_computerreply.split('\n')
                item1 = item.replace('Value', '')
                # print('Lenght：', len(Comp_result), ';', Comp_result)
                if len(Comp_result) > 1:
                    while '' in Comp_result:
                        Comp_result.remove('')
                print(f'>>>|| [实际回值列表]: {Comp_result}')
                for C_result in Comp_result:
                    if C_result.find(item1) >= 0:
                        BAOHANZHI = True
                        Cres = C_result.lstrip().replace(item1, 'MBZ').split(' ')
                        for C_r in Cres:
                            if C_r.find('MBZ') >= 0:
                                Value1 = C_r.replace('MBZ', '')
                                if Value1 == '':
                                    confindflag = 1
                                    Value1 = 'ERR:null'
                                else:
                                    BAOHANZHI = True
                                realdata += item1 + Value1 + ","
                                print(f'>>>|| [返回可变数据]: [ {item1} (Value={Value1}) ]')
                    else:
                        wefind = False
                        confinddata += item + ","
                        print(f'>>>|| [异常信息提示]: [ERROR] 实际返回内容里不包含预期值“{item}”')
                        confindflag = 1
            elif 'NOTINof:'in item:
                Comp_result = res_computerreply.split('\n')
                item1 = item.replace('NOTINof:', '')
                for C_result in Comp_result:
                    if C_result.find(item1) >= 0:
                        Value1 = 'ERR:Non-Existent'        # 不存在，无值
                        realdata += Value1 + item1 + ","
                        print(f'>>>|| [异常信息提示]: [ERROR]检索到不该存在的预期值：{item1}')
                        confindflag = 1
                    else:
                        BAOHANZHI = True
                        realdata += C_result
            elif 'NULL' in item:
                wefind = False
                confinddata += item + ","
                # confindflag = 1
                BAOHANZHI = True
            else:
                if res_computerreply.find(item) >= 0:
                    wefind = True
                    BAOHANZHI = True
                    realdata += item + ","
                    #  这个分支来判断几个容器或应用是否都在正常的运行状态，
                    #  正常不做处理，异常，需要将结果置为不合格。
                elif item.find("*X*") >= 0:
                    statusandtimes = item.split("*X*")
                    WSTR = statusandtimes[0]
                    WINT = statusandtimes[1]
                    NUM = res_computerreply.count(WSTR)
                    if NUM == int(WINT):
                        BAOHANZHI = True
                        print(f'>>>|| [!] 预期值“{WSTR}”的数量与实际数量一致[{WINT}]。')
                        pass
                    else:
                        print(f'>>>|| [异常信息提示]: 预期值“{WSTR}”的实际数量为[{NUM}]。')
                        confindflag = 1
                        confinddata +="容器状态错误，"
                else:
                    wefind = False
                    confinddata += item+","
                    print(f'>>>|| [异常信息提示]: [ERROR] 实际返回内容里不包含预期值“{item}”')
                    confindflag = 1

            if BAOHANZHI == True:
                NUMYZ -= 1

        if NUMYZ > 0:
            print(f'>>>|| [异常信息提示]: [ERROR] 缺失{NUMYZ}个预期内容 ]')
            pass

        if realrow['expect'] == 'NULL':
            res_message = password + '\r\n\r\n[sudo] password for sysadm: \r\n'
            if computerreply == res_message:
                realrow['real'] = "OK"
                realrow['result'] = "合格"
            elif realrow['param'].find('/log ; ') >= 0:
                if computerreply == 'Zgdky@guest123\r\n\r\n':
                    realrow['real'] = "OK"
                    realrow['result'] = "合格"
                else:
                    realrow['real'] = computerreply
                    realrow['result'] = "不合格"
            else:
                realrow['real'] = res_computerreply
                if realrow['param'].find('appm') >= 0:
                    realrow['result'] = "不合格"
                elif realrow['param'].find('cd /') >= 0:
                    if res_computerreply != '':
                        realrow['result'] = "不合格"
                    else:
                        realrow['real'] = "OK"
                        realrow['result'] = "合格"
                else:
                    realrow['real'] = "OK"
                    realrow['result'] = "合格"
        else:
            if confindflag == 1 :
                realrow['real'] = "查询失败项:" + res_computerreply
                realrow['result'] = "不合格"
            elif realrow['save'] != 'STATICMSG' and realrow['save'].find('FACTORTSPECIALPARAM') < 0:
                realrow['real'] = res_computerreply
                realrow['result'] = "合格"
            else:pass
    # 下面增加命令执行结束时间打印，wdw
    # snow = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:23]
    print(f'>>>>| [给出判定结果]: [ {realrow["result"]} ]')         # 结果判定
    # print(f'>>>>| Determine the end time: {snow}')    # 执行结束时间
    print('='*70)
    return md5_rightvalue



class SSHinvoke_shell():
    chans = []
    flag_chanstatu = 0   # 0 未连接,1 可输入command命令 255 未知状态
    def __init__(self):
        self.ssh_client = SSHClient()

    # 登陆ssh服务器
    def login(self, host='192.168.27.244', port='8888', username='sysadm', password='Zgdky@guest123'):
        try:
            self.ssh_client.load_system_host_keys()
            self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            self.ssh_client.connect(hostname=host, port=int(port), username=username, password=password)
            self.chans.append(self.ssh_client.invoke_shell())
            if username.find('root') >= 0:
                if self.chan_receivebychar('~# ')[0]:
                    self.flag_chanstatu = 1
            else:
                if self.chan_receivebychar('$ ')[0] :
                    self.flag_chanstatu = 1
            return True
        except Exception as e:
            print('Exception', e)
            return False

    # command 示例: "ls \n"
    def chan_send(self, command):
        try:
            if len(self.chans) == 0:
                print('chan_send 0')
                return False
            if self.flag_chanstatu == 1:
                print('chan_send 1', command)
                self.chans[0].send(command)
                time.sleep(1.5)
        except Exception as e:
            if len(self.chans) > 0: del self.chans[0:]
            self.flag_chanstatu = 0
        return True

    # 收到某个期望值结尾
    def chan_receivebychar(self, sorder, fdelays=15.0):
        breturn = [False, '']
        buff = ''
        itime = 0.0
        istart = time.time()
        idelay = fdelays
        ibreak = 0
        while not buff.endswith(sorder):
            try:
                resp = self.chans[0].recv(9999)
                buff += resp.decode('utf8')
                print('chan_receivebychar buff', buff)
            except Exception as e:
                print('chan_receivebychar', buff)
                # buff += resp.decode('gb18030')
            # print('chan_receivebychar sorder ', resp)
            time.sleep(0.1)
            itime = time.time() - istart
            if itime > idelay:
                # 强制退出CTRL+C
                if self.flag_chanstatu == 1:
                    btt = self.chans[0].send(chr(int(3)))
                    print('btt', btt, len(self.chans))
                    time.sleep(2.0)
                print('chan_receivebychar itime1, idelay1', itime, idelay)
                # print('chan_receivebychar flag_chanstatu', self.flag_chanstatu)
                ibreak = 1
                break
            print('chan_receivebychar itime, idelay', itime, idelay)
        if ibreak == 0:
            breturn[0] = True
        breturn[1] = buff
        print('breturn', breturn[0], breturn[1])
        return breturn

    # 接收
    def chan_receive(self, fdelays=15.0):
        breturn = [False, '']
        if len(self.chans) == 0:
            return breturn
        buff = ''
        resp = self.chans[0].recv(9999)
        try:
            buff += resp.decode('utf8')
        except Exception as e:
            buff += resp.decode('gb18030')
        print('chan_receive 1', buff)
        if buff.endswith('$ ') or buff.endswith('~$ ') or buff.endswith('~# '):
            self.flag_chanstatu = 1
            breturn[0] = True
            breturn[1] = buff
        elif buff.endswith('password for sysadm: '):
            self.chans[0].send('Zgdky@guest123\n')
            print('chan_receive send password for sysadm: ')
            time.sleep(1.5)
            brr = self.chan_receivebychar('$ ')
            print('chan_receive password for sysadm', brr[0], brr[1])
            breturn[0] = brr[0]
            breturn[1] = brr[1]
        # elif buff.endswith('Password: '):  # 2210D 800M独有
        #     self.chans[0].send('_Admin123\n')
        #     print('chan_receive send Password: ')
        #     time.sleep(1.5)
        #     brr = self.chan_receivebychar('# ')
        #     print('chan_receive Password', brr[0], brr[1])
        #     breturn[0] = brr[0]
        #     breturn[1] = brr[1]
        elif buff.endswith('Password: '):
            self.chans[0].send('Zgdky@guest123\n')
            print('chan_receive send Password: ')
            time.sleep(1.5)
            brr = self.chan_receivebychar('$ ')
            print('chan_receive Password', brr[0], brr[1])
            breturn[0] = brr[0]
            breturn[1] = brr[1]
        # 增加识别
        elif buff.endswith('> '):
            # 输入CTRL+C
            self.chans[0].send(chr(int(3)))
            time.sleep(0.1)
            brr = self.chan_receivebychar('$ ', fdelays)
            print('chan_receive endswith>:', brr[0], brr[1])
            if brr[0]:
                breturn[0] = brr[0]
            else:
                # self.flag_chanstatu = 255
                pass
            breturn[1] = brr[1]
        elif buff.find('(END)') >= 0:
            # 输入CTRL+C
            self.chans[0].send(chr(int(3)))
            time.sleep(0.1)
            # brr = self.chan_receivebychar('$ ', fdelays)
            resp = self.chans[0].recv(9999)
            buff1 = ''
            try:
                buff1 += resp.decode('utf8')
            except Exception as e:
                buff1 += resp.decode('gb18030')
            print('chan_receive endswith >(END):', breturn[1], buff1)
            breturn[1] += buff1
        elif len(buff) > 4096:
            # self.chans[0].send()
            self.chan_send(chr(int(3)))
            time.sleep(0.3)
            # brr = self.chan_receivebychar('$ ', fdelays)
            resp = self.chans[0].recv(9999)
            buff1=''
            try:
                buff1 += resp.decode('utf8')
            except Exception as e:
                buff1 += resp.decode('gb18030')
            print('chan_receive len(buff)>4096', buff1)
            breturn[1] = buff1
        else:
            brr = self.chan_receivebychar('$ ', fdelays)
            print('chan_receive else', brr[0], brr[1])
            if brr[0]:
                breturn[0] = brr[0]
            else:
                # self.flag_chanstatu = 255
                pass
            breturn[1] = brr[1]
            # print('breturn', breturn[0], breturn[1])
        return breturn

    # 通道状态 0 未连接,1 可输入command命令, 255 未知状态
    def getchanstat(self):
        return self.flag_chanstatu

    def setchanstat(self, flag):
        self.flag_chanstatu = flag

    # 交互通道是否关闭
    def ischan(self):
        if len(self.chans) >= 0:
            return True
        return False

    # 退出ssh连接
    def exitchan(self):
        if len(self.chans) >= 0:
            if self.flag_chanstatu != 0:
                self.chans[0].close()
            del self.chans[0:]
        self.flag_chanstatu = 0
        return 1



if __name__ == "__main__":
    """
    EnergyController = {'ServerAddr': '192.168.2.170',
                        'ServerPort': '8888',
                        'UserName': 'sysadm',
                        'PassWord': 'Zgdky@guest123',
                        }
    """
    # print(EnergyController)
    # EnergyController = getsshini()
    # RBTset = False
    # EnCon = SshClient()
    # res = EnCon.ssh_login()
    # print('sshcode:', res)
    # RES = EnCon.execute_some_command('ls /tmp')
    # # print(RES)
    # # for item in RES:
    # #     print(item)
    # # time.sleep(300)
    # # RES = EnCon.execute_some_command(['devctl -e', 'devctl -I'])
    # # for item in RES:
    # #     print(item)
    # realrow = {'expect':'NOTINof:wdw'}
    # getdeviceresult(realrow, RES)
    # RES = EnCon.execute_some_command('devcfg -sn')
    # realrow = {'expect': 'device serial NO.1:Value'}
    # getdeviceresult(realrow, RES)
    # print('iiiiiiiii-000001')
    # RES = EnCon.execute_some_command('sudo ifconfig FE0 192.168.2.170 netmask 255.255.255.0')
    # realrow = {'expect': '连接已断开！'}
    # getdeviceresult(realrow, RES)
    # time.sleep(5)
    # EnCon.ssh_logout()
    # # """
    # # print('123456-wait:20s')
    # # time.sleep(20)
    # # print('next:')
    # # # ===============================================
    # # EnergyController = {'ServerAddr': '192.168.2.170',
    # #                     'ServerPort': '8888',
    # #                     'UserName': 'sysadm',
    # #                     'PassWord': 'Zgdky@guest123',
    # #                     }
    # # """
    # EnCon = SshClient()
    # res = EnCon.ssh_login()
    # # realrow = {'param': 'sudo'}
    # print('sshcode:', res)
    # RES = EnCon.execute_some_command('ifconfig FE0')
    # realrow = {'expect': 'inet addr:Value', 'save': ''}
    # getdeviceresult(realrow, RES)
    # RES = EnCon.execute_some_command('devcfg -sn')
    # realrow = {'expect': 'device serial NO.1:Value', 'save': ''}
    # getdeviceresult(realrow, RES)
    # print('iiiiiiiii-000002')
    # RES = EnCon.execute_some_command('sudo ifconfig FE0 192.168.2.170 netmask 255.255.255.0')
    # realrow = {'expect': 'This link is broken!', 'save': ''}
    # getdeviceresult(realrow, RES)
    # time.sleep(5)
    # EnCon.ssh_logout()
    # time.sleep(2)
    # print('iiiiiiiii-000003')
    EnCon = SshClient()
    res = EnCon.ssh_login()
    #ctrlc:填写指令
    ctrlc = "top | grep '%Cpu(s)'"
    # ctrlc = "sed -i '$a #THIS IS A TEST' /backup/app/libhd.so"
    RES = EnCon.execute_some_command(ctrlc)

    #file_in = '/backup/app/libhd.so'
    #file_out='/backup/app/libhd.so'
    #key = 'mmmm'
   # new = ''
   # ssh_edit_file(EnCon.ssh_client, file_in, file_out, key,new)
   #  realrow = {'expect': '', 'save': ''}
    #0：行号，临时调试指令不涉及，填0即可。
    # getdeviceresult(realrow, RES,0)
    # RES = EnCon.execute_some_command('who')
    # realrow = {'expect': 'sysadm/,/pts', 'save': ''}
    # getdeviceresult(realrow, RES)
    # print('Waiting 2s')
    # time.sleep(2)
    # # RES = EnCon.execute_some_command('ifconfig FE0')
    # # realrow = {'expect': 'inet addr:Value'}
    # # getdeviceresult(realrow, RES)
    # # time.sleep(5)
    # RES = EnCon.execute_some_command('sudo reboot')
    EnCon.ssh_logout()
    # realrow = {'expect': 'This link is broken!', 'save': ''}
    # getdeviceresult(realrow, RES)
