# coding: utf-8
# __author__ = 'Hoyin'
# __date__ = '2020/05/02'
# __Desc__ = 从数据库中导出数据到excel数据表中

import os
import cx_Oracle
import pymysql
import chardet
from config import *


# 文件的根目录
BASE_DIR, filename = os.path.split(os.path.abspath(__file__))
# print(__file__)
BASE_DIR = BASE_DIR.replace('\\', '/')


def get_data(sql):
    logging.info("get_data")
    try:
        if db_type == 'oracle':
            os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
            conn = cx_Oracle.connect('sys','Xdjk_dba','10.80.16.50/pospst',mode=cx_Oracle.SYSDBA)
        elif db_type == 'mysql':
            conn = pymysql.connect(**mysql_config)

        cursor = conn.cursor()
        # 执行SQL
        cursor.execute(sql)

        # 获取全部数据
        data = cursor.fetchall()
        
        # 获取表头
        fields = cursor.description
        
        return data, fields

    except Exception as e:
        print("连接数据库失败！ {}".format(e))
        logging.error("连接数据库失败！ {}".format(e))
        return False, False

    finally:
        cursor.close()
        conn.close()

    



    






