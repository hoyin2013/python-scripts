# 使用方法
## 第一步：将binlog的event导出
    mysql -e "show binlog events in 'mysql-bin.000180';" > /tmp/mysql-bin.000180.txt

## 第二步：找关键字，确定delete的起始位置并记录下来
    mysql-bin.000179	1004058730	Query	64	1004058813	BEGIN
    mysql-bin.000179	1004058813	Table_map	64	1004059042	table_id: 2281 (ds_org_merchant.mer_info)
    mysql-bin.000179	1010230011	Xid	64	1010230042	COMMIT /* xid=983254488 */

## 第三步：将该部分的log导出
    mysqlbinlog --no-defaults --start-position=1004058730 --stop-position=1010230011 -vv mysql-bin.000179 > /tmp/binlog.txt

## 第四步：解析  "59" 表示该表有59个字段
    python restore_insert.py binlog.txt 59 > binlog_insert.sql
    
## 第五步：执行binlog_insert.sql
