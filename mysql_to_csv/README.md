# 根据给出的sql导出mysql数据导csv

+ 支持导出excel和csv
+ 支持批量处理多个sql脚本

## 用法

1. 修改config.py ，配置连接数据库参数和导出类型

    ```python3
    # 例如：根据给出的sql脚本导出本机db1库的文件为excel格式
    config = {
        'host':'127.0.0.1',
        'user': 'root',
        'password': 'root',
        'port': 3306,
        'db': 'db1',
        'type': 'excel',
        #'type': 'csv',
    }
    ```

2. 将要提取的sql语句存放到sql文件夹下，编码为utf8，末尾不要加“；”号
3. linux直接执行 `python3 mysql_to_csv.py` , windows 执行 `run.bat`
4. 进入exports文件夹找到生成的目标文件

## 说明

+ 每个生成文件都以脚本的名称+后缀的方式来命名
+ 请统一使用utf-8编码
+ 仅支持python3
