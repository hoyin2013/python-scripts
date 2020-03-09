# coding:utf-8
# 
# 连接oracle数据库，根据给出的脚本导出为excel或者csv
# 

import sys
import csv
import cx_Oracle
import codecs
import os
import smtplib
import zipfile
import sys
import datetime
import glob
import xlsxwriter

from utils import *
from SendEmail import *

# 是否压缩加密  True | False
dec = False

# 是否发送邮件
send_to_email=True

# 工作目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# SQL脚本文件
SQL_FILES = glob.glob(BASE_DIR +  '/*.sql')

# 链接数据库
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
conn = cx_Oracle.connect("sys", "", "",mode=cx_Oracle.SYSDBA)  # 账号，密码，服务器/sid 
curs = conn.cursor()

# 获取当前时间
nowTime = datetime.datetime.now().strftime('%Y%m%d') 
yestarday = getYesterday().strftime('%Y%m%d')

# 判断sql文件是否存在
if SQL_FILES:
    pass
else:
    raise IOError("SQL脚本不存在!")



# 发送邮件
def sendmail(subject, attachs, receivers):
    # 邮件内容存放路径 
    content_path = BASE_DIR + '/mail.txt'
    
    # 传递邮件发送参数
    argvs = {
        'smtp_server': '',
        'port': 25,
        'user': 'operation@xdjk.com',
        'passwd': 'xdjk2019',
        'ssl': False,
        'sender': '',
        'receivers': receivers,
        'subject': subject,
        'content_path': content_path,
        'attach_files': attachs,
        'attach_title': ''
    }
    # 发送邮件
    sendemail = SendEmail(**argvs)
    sendemail.send()
    

# 依次提取目录中的SQL脚本
for sql_file in SQL_FILES:
    # 生成密码
    pwd = gen_pass(6)
    # 导出文件名
    file_output = BASE_DIR + '/exports/' + os.path.splitext(os.path.basename(sql_file))[0] + '_' + yestarday

    file_output = file_output + '.xlsx'
   
    print(file_output)

    # 新建导出文件,如果是excel，则用xlswriter
    if file_output.endswith('.xlsx'):
        workbook = xlsxwriter.Workbook(file_output)
        worksheet = workbook.add_worksheet()
    else:
        outputFile = open(file_output, 'w', newline='')
        output = csv.writer(outputFile, delimiter=',')

    # 读取SQL文件中的脚本并执行,将结果写入到outputFile
    sql_handle = open(sql_file, encoding='utf-8', errors='ignore' )
    #sql_handle = open(sql_file)
    sql = sql_handle.read()
           
    curs.execute(sql)
    
    if curs:
        rows = curs.fetchall()
        if file_output.endswith('.xlsx'):
            width = len(curs.description)
            for i in range(width): 
                #print(curs.description)
                worksheet.write(0,i, curs.description[i][0])

            # print(rows)
            for r in range(len(rows)):
                for i in range(len(rows[0])):
                    # print(r,i)
                    # print(rows[r][i])
                    worksheet.write(r+1,i,rows[r][i])
            
            workbook.close()
        else:    
            for row_data in curs:
                output.writerow(row_data)
            outputFile.close()

if send_to_email:

    # 邮件主题日期
    subject = '合规周报' + '_' + yestarday

    # 附件路径
    attachs = glob.glob(BASE_DIR + '/exports/*.*')

    # 接收邮件列表
    #receivers = ['', ] 
    receivers = ['',]
    sendmail(subject, attachs, receivers)


if send_to_email:      
    # 如果定期跑批,则需要清理文件
    try:
        for i in os.listdir(BASE_DIR + '/exports/'):
            print(BASE_DIR + '/exports/' + i)
            os.remove(BASE_DIR + '/exports/' + i)
    except:
        print("删除导出文件失败")    



