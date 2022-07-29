# -*- coding: utf-8 -*-
# from operator import itemgetter as basis
import logging
import telnetlib
import time

from Protocol import SSH2ccc
from Protocol import General
from Protocol import Ftptransfiles

telnetmessage = SSH2ccc.getsshini()  # 获取SSH服务器地址、端口，以及用户名和密码

class TelnetClient():
    def __init__(self,):
        self.tn = telnetlib.Telnet()
        self.host_ip = telnetmessage['ServerAddr']
        self.username = telnetmessage['UserName']
        self.password = telnetmessage['PassWord']
    # 此函数实现telnet登录主机
    def login_host(self,host_ip,username,password):
        try:
            # self.tn = telnetlib.Telnet(host_ip,port=23)
            self.tn.open(host_ip,port=23)
        except:
            logging.warning('%s网络连接失败'%host_ip)
            return False
        # 等待login出现后输入用户名，最多等待10秒
        self.tn.read_until(b'login: ',timeout=10)
        self.tn.write(username.encode('ascii') + b'\n')
        # 等待Password出现后输入用户名，最多等待10秒
        self.tn.read_until(b'Password: ',timeout=10)
        self.tn.write(password.encode('ascii') + b'\n')
        # 延时两秒再收取返回结果，给服务端足够响应时间
        time.sleep(2)
        # 获取登录结果
        # read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        command_result = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' not in command_result:
            logging.info('%s登录成功'%host_ip)
            return True
        else:
            logging.warning('%s登录失败，用户名或密码错误'%host_ip)
            return False

    # 此函数实现执行传过来的命令，并输出其执行结果
    def execute_some_command(self,command):
        # 执行命令
        self.tn.write(command.encode('ascii')+b'\n')
        time.sleep(2)
        # 获取命令结果
        if command.find('reboot') >= 0 or command.find('ifconfig FE0 ') >= 0:
            # 命令执行时，终端会断开连接，导致自动化程序在死等结果，无法跳出继续执行下面的程序代码
            time.sleep(1)
        command_result = self.tn.read_very_eager().decode('ascii')
        logging.info('命令执行结果：\n%s' % command_result)
        print('命令执行结果：\n%s' % command_result)
        return command_result

    # 退出telnet
    def logout_host(self):
        self.tn.write(b"exit\n")

#用来处理实际结果中，包含所有的预期结果项目
def valuein(realrow,res_computerreply):
    expectlist = realrow['expect'].split("/,/")
    print('>>||| [预期包含内容]:', expectlist)  # 预期判定值Expected Value:
    NUMYZ = len(expectlist)
    confinddata =''
    confindflag = 0
    for item in expectlist:
        # print({'item__show': item})
        BAOHANZHI = False
        if res_computerreply.find(item) >= 0:
            BAOHANZHI = True
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
                confinddata += "容器状态错误，"
        else:
            confinddata += item + ","
            print(f'>>>|| [异常信息提示]: [ERROR] 实际返回内容里不包含预期值“{item}”')
            confindflag = 1
        if BAOHANZHI == True:
            NUMYZ -= 1
    if NUMYZ > 0:
        print(f'>>>|| [异常信息提示]: [ERROR] 缺失{NUMYZ}个预期内容 ]')
        pass
    if confindflag == 1:
        realrow['real'] = "查询失败项:" + confinddata
        realrow['result'] = "不合格"
    elif realrow['save'] != 'STATICMSG' and realrow['save'].find('FACTORTSPECIALPARAM') < 0:
        realrow['real'] = res_computerreply
        realrow['result'] = "合格"
    else:
        pass
    # 下面增加命令执行结束时间打印，wdw
    # snow = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:23]
    print(f'>>>>| [给出判定结果]: [ {realrow["result"]} ]')  # 结果判定
    return  None


#telnet返回值结果判断流程 NULL
def telnetresultdeal(tasklistitem, telnetresultget,testexcel,md5_rightvalue):
    tasklistitem['real'] = telnetresultget
    if tasklistitem['expect'] == 'NULL':
        if telnetresultget.find('reboot')>=0:
            tasklistitem['real'] = telnetresultget
            tasklistitem['result'] = '合格'
        else:
            tasklistitem['result'] = '不合格'
            tasklistitem['real'] = telnetresultget
    #这个分支用来处理一定会执行成功的命令。结果直接给合格。
    elif tasklistitem['expect'] == '成功':
        tasklistitem['result'] = '合格'
    elif telnetresultget.find('Current maximum erase counter value:')>=0:
        erasetime = telnetresultget.split('Current maximum erase counter value:')
        erasetime = erasetime[1].split('Minimum')
        tasklistitem['real'] = erasetime[0]
        tasklistitem['result'] = '合格'
    elif (tasklistitem['expect'].find('/,/') >= 0) and (tasklistitem['expect'].find('NOTIN') < 0) :
        valuein(tasklistitem,telnetresultget)
    elif tasklistitem['save'].find('_EXPECT') >= 0:
        SSH2ccc.expectequalexpect(tasklistitem, telnetresultget,testexcel)
    elif tasklistitem['expect'].find('_EXPECT') >= 0:
        SSH2ccc.expectequalreal(tasklistitem, telnetresultget,testexcel)
    elif tasklistitem['save'].find('_RIGHTVALUE_') >= 0:
        md5_rightvalue = General.covervalue(tasklistitem, md5_rightvalue, tasklistitem['real'])
        SSH2ccc.expectequalexpect(tasklistitem, telnetresultget, testexcel)
    elif tasklistitem['expect'].find('_RIGHTVALUE_') >= 0:
        SSH2ccc.comparemd5(md5_rightvalue,tasklistitem, telnetresultget)
    elif tasklistitem['expect'].find('NOTIN') >= 0:
        SSH2ccc.notin(tasklistitem, telnetresultget)
    return md5_rightvalue

def nameandpath(tasklistrow):
    name = tasklistrow['param'].split(";")[0].split(':')[1]
    path = tasklistrow['param'].split(";")[1].split(':')[1]
    return name,path


def filepath(tasklistrow):
    local_filepath = ''
    remote_filepath =''
    filename,remotep = nameandpath(tasklistrow)
    localp = 'D:\python_oop_20211028\config\\filetransfer\\'
    local_filepath = localp + filename
    remote_filepath = remotep + '/'+ filename
    print('本地路径:',local_filepath,'终端路径：',remote_filepath)
    return local_filepath, remote_filepath

def telnetop(tasklistrow,tasklist,md5_rightvalue):
    telnet_client = TelnetClient()
    if tasklistrow['oad_omd'] == 'FTP文件传输':
        my_ftp = Ftptransfiles.MyFTP(telnet_client.host_ip)
        my_ftp.login(telnet_client.username, telnet_client.password)
        local_filepath, remote_filepath = filepath(tasklistrow)
        transresult = my_ftp.upload_file(local_filepath,
                           remote_filepath)
        if transresult:
            tasklistrow['real'] = '成功'
            tasklistrow['result'] = '合格'
        else:
            tasklistrow['real'] = '失败'
            tasklistrow['result'] = '不合格'
    else:
        # 如果登录结果返加True，则执行命令，然后退出
        telnetcommand = tasklistrow['param']
        telnetresult = ''
        if telnet_client.login_host(telnet_client.host_ip, telnet_client.username, telnet_client.password):
            telnetresult = telnet_client.execute_some_command(telnetcommand)
            telnet_client.logout_host()
        else:
            print('telnet服务异常')
        md5_rightvalue = telnetresultdeal(tasklistrow, telnetresult, tasklist, md5_rightvalue)
    return md5_rightvalue




if __name__ == '__main__':
    # host_ip = '192.168.127.244'
    # username = 'root'
    # password = 'linux'
    command = 'chmod -R 777 \\tmp\\work\\backup\\test_ly'
    telnet_client = TelnetClient()
    # 如果登录结果返加True，则执行命令，然后退出
    if telnet_client.login_host(telnet_client.host_ip,telnet_client.username,telnet_client.password):
        telnet_client.execute_some_command(command)
        telnet_client.logout_host()