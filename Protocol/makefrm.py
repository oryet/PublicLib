from Protocol.prtl698 import *

#ldata：
def Client_Request(ldata, iniRtu, ipiid,exceltasklist,allsetparam,allgetparam,timeover6034,current_rtu_time,test_plan,no_oadflag):
    global Setparamlist
    global dt_m_list
    global dt_list_realData
    global rtu_save_time
    global plansavetimelist
    global tsalist
    global taskstarttime
    #定义一个变量，存储读参数读到的值。
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
    t=0#每次进入流程，先把标志位清零，避免出错
    w=0
    # d = [ldata['param']]#王梦：添加时标程序流程前程序
    #王梦新增：处理  有效时标、无效时标和不带时标（通过参数传进来，故要在参数中，将这三种情况做区分，并取出正确的参数）
    t,w,d,Tp=paramdeal(str(ldata['param']))#王梦：t:有效时标；w:无效时标；d:参数（原程序中的param）
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
        ldata['real'] = '通讯异常'
        ldata['result'] = '不合格'
    else:
        Nextframe=''
        logging.info('Rx:' + rframe)
        Nextframe,lrs = Receive(rframe)
        print('lrs解析结果:', lrs)
        print('Client_Request lrs[3]', lrs[3])
        print('Client_Request VALUE bool', 'VALUE' in lrs[3])
        if len(lrs) >= 6 and 'VALUE' in lrs[3]:
            sss = ''
            moresss = []  # 返回值为多个属性时
            if lrs[3]['VALUE'] == []:
                ldata['real'] += str([])
  # 当没有值时，暂时填一个空的列表到表格，后期如果觉得[]不合适，可做调整。
                print('Client_Request real', ldata['real'])
            else:
                if isinstance(lrs[3]['VALUE'][0], list):
                    for il in range(0, len(lrs[3]['VALUE']), 1):
                        if isinstance(lrs[3]['VALUE'][il], list):
                            moresss.append(lrs[3]['VALUE'][il])
                        else:
                            print("增加  real  处理")
                    ldata['real']+= str(moresss)
                    print('Client_Request real', ldata['real'])
                else:
                    for il in range(0, len(lrs[3]['VALUE']), 1):
                        sss += str(lrs[3]['VALUE'][il])
                    ldata['real'] += sss

        # 以下为王梦新增，调分帧流程
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
                # 如果终端没有响应（没有回分帧），就将 Nextframe = ''，跳出循环，防止程序死循环。
                Nextframe = ''
            else:
                Nextframe = ''
                logging.info('Rx:' + rframe)
                Nextframe, lrs = Receive(rframe)
                #没有分帧就跳出循环，不再向下执行。
                if Nextframe=="":
                    fenzhenlast+=1
                    print('fenzhenlast:',fenzhenlast)
                # 第一次为空时，分帧的数据刚取到，需要拿过来放表格里，故第一次为空时，需要走以下流程。
                if fenzhenlast<=1:
                    # fenzhenlast1 += 1
                    # print('fenzhenlast1:', fenzhenlast1)
                    print('Client_Request lrs[3]', lrs[3])
                    print('Client_Request VALUE bool', 'VALUE' in lrs[3])
                    if len(lrs) >= 6 and 'VALUE' in lrs[3]:
                        sss = ''
                        moresss = []  # 返回值为多个属性时
                        if lrs[3]['VALUE'] == []:
                            Nextreal += '\n' +str([]) # 当没有值时，暂时填一个空的列表到表格，后期如果觉得[]不合适，可做调整。
                            # ldata['real'] += Nextreal
                            print('Client_Request real', ldata['real'])
                        else:
                            if isinstance(lrs[3]['VALUE'][0], list):
                                for il in range(0, len(lrs[3]['VALUE']), 1):
                                    if isinstance(lrs[3]['VALUE'][il], list):
                                        moresss.append(lrs[3]['VALUE'][il])

                                    else:
                                        print("增加  real  处理")
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


                            # 以上为王梦新增调分帧流程
                        if Nextframe == '':
                            break
                    # 没有分帧就跳出循环
                else:
                    break
        ldata['real'] += Nextreal
        print('Client_Request real', ldata['real'])
        if ldata['real'] == ldata['expect']:
            ldata['result'] = u'合格'
        else:
            ldata['result'] = u'不合格'

    return allsetparam,allgetparam,timeover6034,no_oadflag