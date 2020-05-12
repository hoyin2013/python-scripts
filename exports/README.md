# 根据给出的sql导出mysql或者oracle数据到csv或excel

## 用法

1. 修改config.py ，给config配置正确的信息
2. 将要提取的sql语句存放到sql文件夹下，编码为utf8，末尾不要加“；”号
3. linux直接执行 `python3 exports.py` , windows下编辑run.bat,配置正确的环境变量,然后执行 `run.bat`
4. 进入exports文件夹找到提取出来的sql语句
