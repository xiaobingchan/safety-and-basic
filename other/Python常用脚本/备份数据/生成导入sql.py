# -*- coding:utf-8 -*-
# 用途：生成导入数据sql

import datetime
from time import time, localtime, strftime
import csv 

# 获取当前时间
x=localtime(time())
day = strftime("%d", x)  # 日
month = strftime("%m", x)  # 月
year = strftime("%Y", x)  # 年

n=1 # 计算昨天
cur_date = datetime.datetime(int(year), int(month), int(day)) - datetime.timedelta(days=n)	# 2015-10-29 00:00:00
cal_startdate = cur_date.strftime('%Y-%m-%d')

delete_sql="delete from xxxx where xxx = '"+ str(cal_startdate)+"' ;" # 修改
with open("new.sql", "w") as f:
    f.write(delete_sql)
    f.write("\n")

# 逐行解析csv文件
csv_file=open('bcp.csv') # 修改
csv_reader_lines = csv.reader(csv_file)   #逐行读取csv文件
for one_line in csv_reader_lines:
    # 修改
    i=0
    for onl in one_line:
        if ( onl == ''):
            one_line[i]='null'
        i=i+1
    insert_sql="insert into  xxxx (a,b,c,d,e,f,g,h,i,j,k,l,n,m) values ( '%s',%s,'%s','%s',%s,%s,'%s',%s,%s,%s,%s,%s );" % (one_line[0],one_line[1],one_line[2],one_line[3],one_line[4],one_line[5],one_line[6],one_line[7],one_line[8],one_line[9],one_line[10],one_line[11])
     # 修改
    with open("new.sql", "a") as f:
        f.write(insert_sql)
        f.write("\n")
