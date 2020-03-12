# coding:utf-8
import os
import datetime


def zipDir(dirpath, outFullName, password=None):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 保存路径+xxxx.zip
    :return: 
    """
    import os
    if password:
        cmd = "zip -P %s -r %s %s" % (password, outFullName, dirpath)   
    else:
        cmd = "zip -r %s %s" % (outFullName, dirpath)  
    status = os.popen(cmd)

    return outFullName



def gen_pass(length=8,enhance=False):
    """
		生成默认长度为8的随机密码串
		enhance=True: 加入特殊字符
    """
    import random
    # 去除0、O、o、z、Z、l
    symbols = '!@#$%&*+/\~-_=^'  # 还可以添加特殊字符，加强密码
    if enhance:
        payloads = ''.join([chr(x)+chr(x+32) for x in range(65,91) if x not in [79, 90, 108, 111, 122]]) + '123456789' + symbols
    else:
        payloads = ''.join([chr(x)+chr(x+32) for x in range(65,91) if x not in [79, 90, 108, 111, 122]]) + '123456789'
    return ''.join([random.choice(payloads) for _ in range(length)])


def getYesterday(): 
    """
    获取昨天的时间
    """
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday  
    return yesterday

        
if __name__ == "__main__":

    #print(gen_pass(4))
    
    print(getYesterday().strftime('%Y%m%d'))
