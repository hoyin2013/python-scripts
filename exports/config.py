# coding: utf-8
# __author__ = 'Hoyin'
# __date__ = '2020/05/02'
# __Desc__ = 从数据库中导出数据到excel数据表中

import logging

# 日志格式配置
logging.basicConfig(level=logging.INFO,format='%(asctime)s :: %(levelname)s :: %(message)s', filename='exports.log')

# 数据库类型  oracle|mysql
db_type = 'mysql'

# 导出类型 excel csv
export_type = 'excel'

# mysql连接配置
mysql_config = {
    'user': 'root',
    'password': '',
    'host': '10.80.16.64',
}

# oracle连接配置
oracle_config = ''



config_sjqx = {
    'host':'10.80.16.57',
    'user': 'hoyin',
    'password': 'fdsafdsa'
}

config_paas = {
    'host':'10.80.16.64',
    'user': 'root',
    'password': ''
}
