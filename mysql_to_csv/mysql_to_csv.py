# coding: utf-8
# __author__ = 'hoyin'
# __date__ = '2020/04/01'
# __Desc__ = 从数据库中导出数据到excel数据表中

import csv
import os
import pymysql
import logging
import glob
import xlwt

from config import config_sjqx, config_paas, config

export_type = config.pop('type')


# 日志格式配置
logging.basicConfig(level=logging.INFO,format='%(asctime)s :: %(levelname)s :: %(message)s', filename='exports.log')

# 文件的根目录
BASE_DIR, filename = os.path.split(os.path.abspath(__file__))
#print(__file__)
BASE_DIR = BASE_DIR.replace('\\', '/')

#print(BASE_DIR)

def get_mysql_data(sql):
    # 连接
    conn = pymysql.connect(**config)
    cursor = conn.cursor()

    cursor.execute(sql)
    # 重置游标的位置
    cursor.scroll(0,mode='absolute')
    data = cursor.fetchall()

    # 获取MYSQL里面的数据字段名称
    fields = cursor.description

    conn.close()
    return data, fields


def export_to_excel(sql, outputpath):
    
    results, fields = get_mysql_data(sql)

    if results:
    	logging.info("获取数据成功!")
    else:
	    logging.error("获取数据失败!")

    workbook = xlwt.Workbook(encoding = 'utf-8')
    sheet = workbook.add_sheet('Worksheet')

    # 写上字段信息
    for field in range(0,len(fields)):
        sheet.write(0,field,fields[field][0])

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1,len(results)+1):
        for col in range(0,len(fields)):
            sheet.write(row,col,u'%s'%results[row-1][col])

    workbook.save(outputpath + '.xlsx')

def export_to_csv(sql, outputpath):
    results, fields = get_mysql_data(sql)

    f = open(outputpath + '.csv', 'w+', newline='', encoding='utf-8')
    write = csv.writer(f, delimiter=',')
    
    try:
        head = [ x[0] for x in fields]
        #print(head)
        write.writerow(head)
        #print(results)
        write.writerows(results)
    except:
        logging.error("写入数据失败!")

    f.close()

# 找到根目录下的所有sql文件
sql_files = glob.glob(BASE_DIR + '/sql/*.sql')
sql_files = [f.replace('\\', '/') for f in sql_files]
print(sql_files)

for fp in sql_files:
    f = open(fp, 'r', encoding='utf-8', errors='ignore')
    sql = f.read()
    f.close()

    logging.info("开始解析:{}".format(fp))

    # 保存执行结果
    outputpath = BASE_DIR + '/exports/' + os.path.splitext(os.path.basename(fp))[0]

    if export_type == 'excel':
        export_to_excel(sql, outputpath)
    elif export_type == 'csv':
        export_to_csv(sql, outputpath)
    logging.info("生成文件:{}".format(outputpath))




    






