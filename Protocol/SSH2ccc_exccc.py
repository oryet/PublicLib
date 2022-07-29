# coding=utf-8

import sys
import time
from paramiko import AuthenticationException
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import NoValidConnectionsError
import logging
import datetime
import os
from Protocol import SSH2ccc
snow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    filename=os.getcwd().replace("\Protocol", "") + '\log\\' + snow + 'ooptest.log', level=logging.DEBUG)


# UserName:sysadm PassWd:Zgdky@guest123 Port:8888 ->{'UserName':'sysadm','PassWd':'Zgdky@guest123', 'Port':'8888'}
def sshuserdict(userparam):
    dusr = {'UserName': 'sysadm', 'PassWd': 'Zgdky@guest123', 'Port':'8888'}
    if userparam.find('UserName:') == -1 or  userparam.find('PassWd:') == -1 or userparam.find('Port:') == -1:
        return dusr
    ll = userparam.split(' ')
    for item in ll:
        if item.find(':') >= 0:
            litem = item.split(':')
            if litem[0] == 'UserName':
                dusr['UserName'] = litem[1]
            if litem[0] == 'PassWd':
                dusr['PassWd'] = litem[1]
            if litem[0] == 'Port':
                dusr['Port'] = litem[1]
    return dusr


# 带[]字符串转换成list '[c,d,e]'->[c,d,e]
def strtolist(slist):
    lrtn = eval("%s" % slist)
    return lrtn
# 期望值和实际值判断处理
def expectorreal(expect, real):
    if '[' in expect and ']' in expect and expect.find('[') == 0:
        try:
            ll = strtolist(expect)
            if ll[0] == 'include':
                bfd = True
                for i in range(1, len(ll), 1):
                    if real.find(ll[i]) == -1:
                        bfd = False
                        break
                return bfd
            elif ll[0] == 'exclude':
                bfind = True
                for i in range(1, len(ll), 1):
                    if real.find(ll[i]) >= 0:
                        bfind = False
                        break
                return bfind
            elif (len(expect) > 0) and (real.find(expect) == -1):
                return False
        except:
            logging.info('expectorreal try expect:'+ expect + ',real:' + real)
            return False
    else:
        if (len(expect) > 0) and (real.find(expect) == -1):
            return False
    return True


# ssh命令
def MK_SSH(ldata, ssh):
    sshRx = []
    command = ldata['param'] + ' \n'
    if 'exit' in ldata['param']:
        print('MK_SSH ssh.getchanstat() exit', ssh.getchanstat())
        if ssh.getchanstat() != 0:
            ssh.chan_send('exit \n')
            ssh.exitchan()
            ldata['real'] = 'exit OK'
            print('real_11', ldata['real'])
            return True
        else:
            ldata['real'] = 'SSH未连接'
            print('real_12', ldata['real'])
            return False
    elif 'UserName' in ldata['param']:
        print('MK_SSH ssh.getchanstat() UserName', ssh.getchanstat())
        duser = sshuserdict(ldata['param'])
        if ssh.getchanstat() == 0:
            EXCLECON = SSH2ccc.getsshini()
            ssh.login(EXCLECON['ServerAddr'],EXCLECON['ServerPort'], duser["UserName"], duser["PassWd"])
            if ssh.getchanstat() == 1:
                ldata['real'] = 'login OK'
            else:
                ldata['real'] = 'login NO'
            if expectorreal(ldata['expect'], ldata['real']):
                ldata['result'] = u'合格'
            else:
                ldata['result'] = u'不合格'
            print('real_9', ldata['real'])
            return True
        else:
            ldata['real'] = 'SSH已连接'
            print('real_10', ldata['real'])
            return False
    elif 'reboot' in ldata['param']:
        if ssh.getchanstat() != 0:
            ssh.chan_send(command)
            brr = ssh.chan_receivebychar('password for sysadm: ')
            logging.info("输入密码:")
            logging.info(brr[1])
            if brr[0]:
                ssh.chan_send('Zgdky@guest123\n')
                logging.info("输入密码重启系统!")
                ssh.exitchan()
                # ldata['real'] = '成功'
                ldata['real'] = 'reboot OK'
            else:
                logging.info("重启系统成功（未输入密码）！")
                ssh.exitchan()
                ldata['real'] = 'reboot OK'
            print('real_8', ldata['real'])
            return True
        else:
            ldata['real'] = 'SSH未连接'
            return False
    elif 'sudo passwd sysadm' in ldata['param']:
        print('MK_SSH ssh.getchanstat() exit', ssh.getchanstat())
        snewpwd = ldata['save']+'\n'
        if len(snewpwd) < 12:
            snewpwd = 'Zgdky@guest123\n'
        if ssh.getchanstat() != 0:
            ssh.chan_send('sudo passwd sysadm\n')
            brr = ssh.chan_receivebychar('Enter new password: ')
            logging.info("修改密码:")
            logging.info(brr[1])
            if brr[0]:
                ssh.chan_send(snewpwd)
                bbr1 = ssh.chan_receivebychar('Re-type new password: ')
                logging.info("修改密码1:")
                logging.info(bbr1[1])
                if bbr1[0]:
                    ssh.chan_send(snewpwd)
                    ldata['real'] = 'new passwd OK'
            print('real_7', ldata['real'])
            return True
        else:
            ldata['real'] = 'SSH未连接'
            return False
    if ssh.getchanstat() == 1:
        ssh.chan_send(command)
        # fdelay = float(ldata['delay'])
        sshRx += ssh.chan_receive(float(ldata['delay']))
        logging.info("chan通道接收:")
        if len(sshRx[1]) > 4096:
            logging.info(sshRx[1][:4096] + '[chan通道接收太长删减]')
            ldata['real'] = sshRx[1][:4096]
            print('ssh.getchanstat()', ssh.getchanstat())
            ssh.chan_send(chr(int(3)))
            # if username.find('root') >= 0:
            #     if self.chan_receivebychar('~# ')[0]:
            #         self.flag_chanstatu = 1
            # print('ssh.chan_receive()', ssh.chan_receive()[1])
            time.sleep(10.0)
            # ssh.chan_send(chr(int(3)))
            logging.info('chan通道接收1:' + ssh.chan_receive()[1])
            # print('ssh.chan_receive()', ssh.chan_receive()[1])
        else:
            logging.info(sshRx[1])
            ldata['real'] = sshRx[1]
        if expectorreal(ldata['expect'], ldata['real']):
            ldata['result'] = u'合格'
            print('real_0',ldata['real'])
            return True
        else:
            ldata['result'] = u'不合格'
            print('real_1', ldata['real'])
            return True
    else:
        print('SSH_SERVERIP no line')
        return False
    icount = 0
    if ldata['param'].find('ls /tmp/dev') >= 0:
        for i in EMUN_USBEXM:
            if i in sshRx[1]:
                icount += 1
                # print('i=', i)
        if icount >= 2:
            ldata['result'] = '合格'
            print('real_3', ldata['real'])
            return True
        else:
            ldata['result'] = '不合格'
            print('real_4', ldata['real'])
            return False
    elif ldata['param'].find('ifconfig') >= 0:
        if sshRx[1].find('ppp0') >= 0:
            ldata['result'] = '合格'
            print('real_5', ldata['real'])
            return True
        else:
            ldata['result'] = '不合格'
            print('real_6', ldata['real'])
            return False
    return True


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
    command = "ls /tmp/dev \n"
    command = "sudo appm -I -c pdContainer -l \n"
    chan = SSHinvoke_shell()
    sshRx = ''
    chan.login("192.168.27.244", '8888', "sysadm", "Zgdky@guest123")
    sshRx = chan.chan_send(command)
    bRR = chan.chan_receive()
    print('sshRx1:', bRR[0], bRR[1])
    command = "sudo appm -I -c amrContainer -l \n"
    sshRx = chan.chan_send(command)
    bRR = chan.chan_receive()
    print('sshRx2:', bRR[0], bRR[1])
    command = "sudo appm -I -c baseContainer -l \n"
    sshRx = chan.chan_send(command)
    bRR = chan.chan_receive()
    print('sshRx3:', bRR[0], bRR[1])
    command = "sudo appm -I -c edgerContainer -l \n"
    sshRx = chan.chan_send(command)
    bRR = chan.chan_receive()
    print('sshRx4:', bRR[0], bRR[1])
    # command = "if config \n"
    # sshRx = chan.chan_send(command)
    # bRR = chan.chan_receive()
    # print('sshRx5:', bRR[0], bRR[1])
    command = "top \n"
    sshTx = chan.chan_send(command)
    print('sshTx', sshTx)
    bRR = chan.chan_receivebychar('$ ')
    print('bRR',bRR[0], bRR[1])
    command = "exit \n"
    sshTx = chan.chan_send(command)
    chan.exitchan()
    # ddd = ['usb_exm1_0', 'usb_exm1_1', 'usb_exm2_0', 'usb_exm2_1', 'usb_exm3_0', 'usb_exm3_1', 'usb_exm4_0',
    #        'usb_exm4_1', 'usb_exm5_0', 'usb_exm5_1']
    # icount = 0
    # for i in ddd:
    #     if i in sshRx:
    #         icount += 1
    #         print('i=', i)
    # if icount == len(ddd):
    #     print('ls ok')
    # else:
    #     print('ls no')