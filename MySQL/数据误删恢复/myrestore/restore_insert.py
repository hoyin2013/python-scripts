#!/bin/env python
# -*- encoding: utf-8 -*-

def read_binlog(file,column_num):
    f=open(file)
    num = '@'+str(column_num)
    while True:
        lines = f.readline()
        if lines.strip()[0:3] == '###':
            lines=lines.split(' ',3)
            if lines[1] == 'DELETE' and lines[2] =='FROM':           #该部分替换Delete为Insert
                lines[1] = "INSERT"
                lines[2] = 'INTO'
                lines[-1] = lines[-1].strip()

            if lines[1].strip() == 'WHERE':
                lines[1] = 'VALUES ('

            if  ''.join(lines).find('@') <> -1 and lines[3].split('=',1)[0] <> num:          #num为列数，要是小于最大的列数，后面均加,
                lines[3] = lines[3].split('=',1)[-1].strip()

                if lines[3].strip('\'').strip().find('\'') <> -1:
                    lines[3] = lines[3].split('/*')[0].strip('\'').strip().strip('\'').replace('\\','').replace('\'','\\\'')  #这里过滤掉转义的字符串
                    lines[3] = '\'' + lines[3] + '\','
                elif lines[3].find('INT meta') <> -1:                #过滤Int类型的字段为负数后带的（），正数不受影响
                    lines[3] = lines[3].split('/*')[0].strip()
                    lines[3] = lines[3].split()[0] + ','
                elif lines[3].find('NULL') <> -1:
                    lines[3] = lines[3].split('/*')[0].strip()
                    lines[3] = lines[3] + ','
                else:
                    lines[3] = lines[3].split('/*')[0].strip('\'').strip().strip('\'').replace('\\','').replace('\'','\\\'')  #这里过滤掉转义的字符串
                    lines[3] = '\'' + lines[3].strip('\''' ') + '\','

            if  ''.join(lines).find('@') <> -1 and lines[3].split('=',1)[0] == num:          #num为列数，要是小于最大的列数，后面均加);
                lines[3] = lines[3].split('=',1)[-1].strip()
                if lines[3].find('\'') <> -1: 
                    lines[3] = lines[3].split('/*')[0].strip('\'').strip().strip('\'').replace('\\','').replace('\'','\\\'')  #同上
                    lines[3] = '\'' + lines[3] + '\');'
                elif lines[3].find('INT meta') <> -1:                #同上
                    lines[3] = lines[3].split('/*')[0].strip()
                    lines[3] = lines[3].split(' ')[0] + ');'
                elif lines[3].find('NULL') <> -1:
                    lines[3] = lines[3].split('/*')[0].strip()
                    lines[3] = lines[3] + ');'
                else:
                    lines[3] = lines[3].split('/*')[0].strip('\'').strip().strip('\'').replace('\\','').replace('\'','\\\'')  #同上
                    lines[3] = '\'' + lines[3].strip('\''' ') + '\');'

            print ' '.join(lines[1:])

        if lines == '':
            break


if __name__ == '__main__':
    import sys
    read_binlog(sys.argv[1],sys.argv[2])
