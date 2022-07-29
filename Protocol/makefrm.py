from Protocol.prtl698 import *

#ldata��
def Client_Request(ldata, iniRtu, ipiid,exceltasklist,allsetparam,allgetparam,timeover6034,current_rtu_time,test_plan,no_oadflag):
    global Setparamlist
    global dt_m_list
    global dt_list_realData
    global rtu_save_time
    global plansavetimelist
    global tsalist
    global taskstarttime
    #����һ���������洢������������ֵ��
    readparamlist=[]
    Nextreal=""
    ldata['real']=''
    frm = {}
    frm['CTRL'] = '43'
    frm['TSA_TYPE'] = getbitbyCA(ldata['addrtype'])
    frm['TSA_VS'] = getintbyvaddrname(ldata['vadd'])
    frm['TSA_AD'] = General.addrget(ldata, iniRtu, frm)
    frm['CA'] = ldata['caddr']
    frm['SEG_WORD'] = ''
    s = ldata['secure']
    r = ldata['op']
    i = ipiid % 64
    o = [ldata['oad_omd']]
    t=0#ÿ�ν������̣��Ȱѱ�־λ���㣬�������
    w=0
    # d = [ldata['param']]#���Σ����ʱ���������ǰ����
    #��������������  ��Чʱ�ꡢ��Чʱ��Ͳ���ʱ�꣨ͨ����������������Ҫ�ڲ����У�����������������֣���ȡ����ȷ�Ĳ�����
    t,w,d,Tp=paramdeal(str(ldata['param']))#���Σ�t:��Чʱ�ꣻw:��Чʱ�ꣻd:������ԭ�����е�param��
    n=[ldata['name']]
    print('s,r,i,o,d:', s, r, i, o, d)
    frm['APDU'] = make_DATA_APDU_Request(s, r, i, o, d, t, w,Tp)
    # print(f'frm:{frm}')
    frame = MakeFrame(frm)
    frame = frame.upper()
    print('Client_Request Tx:' + frame)
    logging.info('Tx:' + frame)
    senddata(frame)
    itime = 0.0
    istart = time.time()
    rframe = ''
    if isinstance(ldata['delay'], str):
        if ldata['delay'].find('WAITSELF') >= 0:
            rxwaittime = float(ldata['delay'].split(":")[1])
        else:
            rxwaittime = SYSCONFIG['RXOUTTIME']
        print(f'rxwaittime:{rxwaittime}')
    else:rxwaittime = SYSCONFIG['RXOUTTIME']
    while itime < rxwaittime :
        time.sleep(0.2)
        rframe = recvdata(ldata['oad_omd'])
        if len(rframe) > 0:
            break
        itime = time.time() - istart
    if rframe =='':
        bcnt = False
        logging.info('Client_Request read Rx:Null')
        ldata['real'] = 'ͨѶ�쳣'
        ldata['result'] = '���ϸ�'
    else:
        Nextframe=''
        logging.info('Rx:' + rframe)
        Nextframe,lrs = Receive(rframe)
        print('lrs�������:', lrs)
        print('Client_Request lrs[3]', lrs[3])
        print('Client_Request VALUE bool', 'VALUE' in lrs[3])
        if len(lrs) >= 6 and 'VALUE' in lrs[3]:
            sss = ''
            moresss = []  # ����ֵΪ�������ʱ
            if lrs[3]['VALUE'] == []:
                ldata['real'] += str([])
  # ��û��ֵʱ����ʱ��һ���յ��б���񣬺����������[]�����ʣ�����������
                print('Client_Request real', ldata['real'])
            else:
                if isinstance(lrs[3]['VALUE'][0], list):
                    for il in range(0, len(lrs[3]['VALUE']), 1):
                        if isinstance(lrs[3]['VALUE'][il], list):
                            moresss.append(lrs[3]['VALUE'][il])
                        else:
                            print("����  real  ����")
                    ldata['real']+= str(moresss)
                    print('Client_Request real', ldata['real'])
                else:
                    for il in range(0, len(lrs[3]['VALUE']), 1):
                        sss += str(lrs[3]['VALUE'][il])
                    ldata['real'] += sss

        # ����Ϊ��������������֡����
        while len(Nextframe) > 0:
            fenzhenlast = 0
            # fenzhenlast1 = 0
            # n = 0
            logging.info('Tx:' + Nextframe)
            senddata(Nextframe)
            itime = 0.0
            istart = time.time()
            rframe = ''
            if isinstance(ldata['delay'], str):
                if ldata['delay'].find('WAITSELF') >= 0:
                    rxwaittime = float(ldata['delay'].split(":")[1])
                else:
                    rxwaittime = SYSCONFIG['RXOUTTIME']
            else:
                rxwaittime = SYSCONFIG['RXOUTTIME']
            while itime < rxwaittime:
                time.sleep(0.2)
                rframe = recvdata(ldata['oad_omd'])
                if len(rframe) > 0:
                    break
                itime = time.time() - istart
            if rframe == '':
                bcnt = False
                logging.info('Client_Request read Rx:Null')
                # ����ն�û����Ӧ��û�лط�֡�����ͽ� Nextframe = ''������ѭ������ֹ������ѭ����
                Nextframe = ''
            else:
                Nextframe = ''
                logging.info('Rx:' + rframe)
                Nextframe, lrs = Receive(rframe)
                #û�з�֡������ѭ������������ִ�С�
                if Nextframe=="":
                    fenzhenlast+=1
                    print('fenzhenlast:',fenzhenlast)
                # ��һ��Ϊ��ʱ����֡�����ݸ�ȡ������Ҫ�ù����ű����ʵ�һ��Ϊ��ʱ����Ҫ���������̡�
                if fenzhenlast<=1:
                    # fenzhenlast1 += 1
                    # print('fenzhenlast1:', fenzhenlast1)
                    print('Client_Request lrs[3]', lrs[3])
                    print('Client_Request VALUE bool', 'VALUE' in lrs[3])
                    if len(lrs) >= 6 and 'VALUE' in lrs[3]:
                        sss = ''
                        moresss = []  # ����ֵΪ�������ʱ
                        if lrs[3]['VALUE'] == []:
                            Nextreal += '\n' +str([]) # ��û��ֵʱ����ʱ��һ���յ��б���񣬺����������[]�����ʣ�����������
                            # ldata['real'] += Nextreal
                            print('Client_Request real', ldata['real'])
                        else:
                            if isinstance(lrs[3]['VALUE'][0], list):
                                for il in range(0, len(lrs[3]['VALUE']), 1):
                                    if isinstance(lrs[3]['VALUE'][il], list):
                                        moresss.append(lrs[3]['VALUE'][il])

                                    else:
                                        print("����  real  ����")
                                Nextreal += '\n' +str(moresss)
                                # n += 1
                                # print('n,Nextreal:', n, Nextreal)

                                # ldata['real'] += Nextreal

                                print('Client_Request real', ldata['real'])
                            else:
                                for il in range(0, len(lrs[3]['VALUE']), 1):
                                    sss += lrs[3]['VALUE'][il]
                                Nextreal +='\n' + sss
                                # ldata['real'] += Nextreal
                                print('Client_Request real', ldata['real'])


                            # ����Ϊ������������֡����
                        if Nextframe == '':
                            break
                    # û�з�֡������ѭ��
                else:
                    break
        ldata['real'] += Nextreal
        print('Client_Request real', ldata['real'])
        if ldata['real'] == ldata['expect']:
            ldata['result'] = u'�ϸ�'
        else:
            ldata['result'] = u'���ϸ�'

    return allsetparam,allgetparam,timeover6034,no_oadflag