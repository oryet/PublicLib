# -*- coding: utf-8 -*-
import os
import logging
#导入需要使用的包
import xlsxwriter   #将文件写入Excel的包
import xlwt
import openpyxl
import xlrd
import datetime
snow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    filename=os.getcwd().replace("\Protocol", "") + '\log\\' + snow + 'ooptest.log', level=logging.INFO)

#打开一个excel文件
def open_xls(file):
    f = xlrd.open_workbook(file)
    return f

#获取excel中所有的sheet表
def getsheet(f):
    return f.sheets()

#获取sheet表的行数
def get_Allrows(f,sheet):
    table=f.sheets()[sheet]
    return table.nrows


#读取文件内容并返回行内容
def getFile(file,shnum,datavalue):
    # 存储所有读取的结果
    f=open_xls(file)
    table=f.sheets()[shnum]
    num=table.nrows
    for row in range(num):
        rdata=table.row_values(row)
        datavalue.append(rdata)
    return datavalue


#获取sheet表的个数
def getshnum(f):
    x=0
    sh=getsheet(f)
    for sheet in sh:
        x+=1
    return x



#一个或多个表格中的数据存储在一个列表中（为即将生成的表格做准备）
def oneormoreexceltolist(allxls):
    # 存储所有读取的结果
    datavalue = []
    for fl in allxls:
        f = open_xls(fl)
        x = getshnum(f)
        for shnum in range(x):
            print("正在读取文件：" + str(fl) + "的第" + str(shnum) + "个sheet表的内容...")
            rvalue = getFile(fl, shnum,datavalue)
    return rvalue


def excwrite(rowvalue,ews):
    for a in range(len(rowvalue)):
        for b in range(len(rowvalue[a])):
            c=rowvalue[a][b]
            ews.cell(row=a+1, column=b+1, value=c)
    return ews

#根据当前测试需求，修改最终报告中3个sheet页的名称。
def sheetnamerename(name1,name2,name3,wobk):
    num = 0
    namelist = [name1, name2, name3]
    for sheet in wobk:
        name = namelist[num]
        if name.find('不合格') >= 0:
            sheet.sheet_properties.tabColor = 'FF0000'
        sheet.title = name
        num += 1
    return None

def exceldel(pathlist):
    for item in pathlist:
        if os.path.exists(item) == True:
            os.remove(item)
        else:pass
    return None

def moreexceltoone(twosheet,onetone,twoexceltoone,endfile):
    #定义要合并的excel文件列表
    # allxls=['F:/test/excel1.xlsx','F:/test/excel2.xlsx'] #列表中的为要读取文件的路径
    rvalue = oneormoreexceltolist(twosheet)
    copysheetvalue = oneormoreexceltolist(onetone)
    copyexcelvalue = oneormoreexceltolist(twoexceltoone)
    #定义最终合并后生成的新文件
    # endfile='F:/test/excel3.xlsx'
    wb = openpyxl.load_workbook(endfile)
    sheet1name = twosheet[0].split('/')[-1].split('.')[0]
    sheet2name = onetone[0].split('/')[-1].split('.')[0]
    sheet3name = twoexceltoone[0].split('/')[-1].split('.')[0]
    ws = wb['测试结论']
    wss = wb['准备工作']
    wess = wb['循环测试']
    #往最终的表格中写入数据
    #4G和报告展示2个sheet页合并为1个sheet页
    excwrite(rvalue,ws)
    # 准备工作生成为1个sheet页
    excwrite(copysheetvalue, wss)
    # 循环测试和结束工作生成为1个sheet页
    excwrite(copyexcelvalue, wess)
    sheetnamerename(sheet1name,sheet2name,sheet3name,wb)
    exceldel(twosheet)
    exceldel(onetone)
    exceldel(twoexceltoone)
    wb.save(endfile)
    print("文件合并完成")

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        return root,files


def hardwareexcelmerge(path,ultimatename,resultright):
    presentroot, allfilename = file_name(path)
    # 测试完成时，在指定路径下找到所有的文件，并生成需要的路径（合并表格时需要的路径）。
    try:
        for itemname in allfilename:
            if itemname.find('准备工作') >= 0:
                onetone = [presentroot + '/' + itemname]
                print(onetone)
            elif itemname.find('循环测试') >= 0:
                twoexceltoone = [presentroot + '/' + itemname]
            elif itemname.find('结束工作') >= 0:
                twoexceltoone.append(presentroot + '/' + itemname)
            elif itemname.find('汇总') >= 0 or itemname.find('版本信息') >= 0:
                pass
            else:
                twosheet = [presentroot + '/' + itemname]
                if itemname.find('不合格') >= 0:
                    resultright = 1
                else:pass
        moreexceltoone(twosheet, onetone, twoexceltoone, ultimatename)
    except BaseException:
        logging.info("硬件自动化测试报告生成缺少文件！")
        print("硬件自动化测试报告生成缺少文件！")
    return resultright
# ultimatename = "F:/test/000000000171静电合格202105131719报告汇总.xlsx"
# path ='F:/test'
# hardwareexcelmerge(path,ultimatename)

