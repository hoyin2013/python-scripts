# binlog_rollback

- binlog_rollback 是用golang语言写的一款数据恢复工具，经过测试，十分好用
- 它不需要额外的运行环境，直接二进制格式就可以执行
- 地址：<https://github.com/GoDannyLai/binlog_rollback>

## 参数说明

- -m file|repl  解析本地binlog文件|作为slave连接到主库并获取日志文件
- -w 2sql|rollback|stats  解析成sql语句|解析成反向回滚语句|统计
- -I '-w 2sql'时使用，忽略主键
- -stsql '-w 2sql'时使用，记录执行计划
- -M mysql|mariadb  mysql还是mariadb
- -H 服务器ip
- -P 服务器端口
- -u 数据库用户
- -p 数据库密码
- -S socket
- -dbs 数据库，都为小写，多个数据库用“,”分隔
- -mid 作为slave连主库拉去日志时指定server-id，默认为：3320
- -tbs 表名，多个表名之间用“,”号分隔
- -sql insert,update,delete 默认是包含所有，也可以单独指定某一种或者几种，用逗号分隔
- -U 优先使用unique key，'-sql delete,update'时候使用
- -sbin 开始读取的binlog文件
- -spos 开始读取的日志点
- -ebin 结束时的日志号
- -epos 结束时的日志号
- -tl Local|Asia/Shanghai 时区，默认为Local
- -sdt 开始的时间点
- -edt 结束的时间点
- -C  '-w stats' 的时候使用，记录事务
- -i '-w stats' 的时候使用，记录状态
- -b 大事务标记，会将信息单独生成为一个大事务文件txt
- -l 长事务标记，会将信息单独生成为一个长事务文件txt
- -a '-w=2sql|rollback'时候使用，记录所有的字段，包括未做更改的
- -r '-w=2sql|rollback'时候使用，记录行数
- -k '-w=2sql|rollback'时候使用，加上begin。。。end，作为一个事务
- -d '-w=2sql|rollback'时候使用，加上表的前缀，即显示为"db_name.tbname"
- -e '-w=2sql|rollback'时候使用，记录额外信息
- -f '-w=2sql|rollback'时候使用，每一个表单独一个文件
- -t '-w=2sql|rollback'时候使用，线程数，默认是4
- -rj '-w=2sql|rollback'时候使用，读表结构
- -oj '-w=2sql|rollback'时候使用，只使用rj读到的表结构
- -dj '-w=2sql|rollback'时候使用，dump表结构，json格式
- -o 输出的目录，默认为当前目录
- -ors 输出原始sql，默认为false
- -ies  当遇到错误时记录错误并继续解析

## 使用方法举例

- 通过binlog文件方式找出本机 ds_org_merchant.customer_info 表 mysql-bin.000279 32229490 35825015 之间的操作并生成恢复语句
```
./binlog_rollback -m file -w rollback -M mysql -t 4 -H 127.0.0.1 -P 3306 -u root -p pass -dbs ds_org_merchant -tbs customer_info -sbin mysql-bin.000279 -spos 32229490 -ebin mysql-bin.000279 -epos 35825015 -e -f -r 20 -k -b 100 -l 10  -o /tmp -dj tbs_all_def.json mysql-bin.000279```

- 通过binlog文件方式找出本机 ds_org_merchant.customer_info 表 某时间段内的操作并生成恢复语句
```
./binlog_rollback -m file -w rollback -M mysql -t 4 -H 127.0.0.1 -P 3306 -u root -p pass -dbs ds_org_merchant -tbs customer_info -sdt "2020-03-15 07:30:00" -edt "2020-03-15 08:12:00"  -e -f -r 20 -k -b 100 -l 10  -o /tmp -dj tbs_all_def.json mysql-bin.000283```
```

- 官方示例
    * 生成前滚SQL与DML报表:
    ```
    ./binlog_rollback.exe -m repl -w 2sql -M mysql -t 4 -mid 3331 -H 127.0.0.1 -P 3306 -u xxx -p xxx -dbs db1,db2 -tbs tb1,tb2 -sbin mysql-bin.000556 -spos 107 -ebin mysql-bin.000559 -epos 4 -e -f -r 20 -k -b 100 -l 10 -o /home/apps/tmp -dj tbs_all_def.json```

    * 生成回滚SQL与DML报表:
    ```
    ./binlog_rollback.exe -m file -w rollback -M mysql -t 4 -H 127.0.0.1 -P 3306 -u xxx -p xxx -dbs db1,db2 -tbs tb1,tb2 -tbs tb1,tb2 -sdt "2017-09-28 13:00:00" -edt "2017-09-28 16:00:00" -e -f -r 20 -k -b 100 -l 10  -o /home/apps/tmp -dj tbs_all_def.json mysql-bin.000556```

    * 只生成DML报表:
    ```
    ./binlog_rollback -m file -w stats -M mysql -i 20 -b 100 -l 10 -o /home/apps/tmp mysql-bin.000556```
