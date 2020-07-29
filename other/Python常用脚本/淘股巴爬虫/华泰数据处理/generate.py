#pip install python-docx 
import csv
import numpy as np
import pandas as pd
#导入图表库以进行图表绘制
import matplotlib.pyplot as plt


client_fortune='client_fortune.csv'#客户资产csv文件
client_total='client_total.xls'#统计总表
new_generate_file='new_fileName.xlsx'#生成的文件
chat_file='chat.jpg';#图表文件
word_file='resulrt.docx';#插入图表的word

with open(client_fortune) as f:
  r = csv.reader(f)#读取当日的用户资产表
  total_client_fortume=0.00
  for i in r:
      if '6.67E+11' in i:#如果是6666开头，就不计算在内
        pass
      elif '总资产' in i:#排除第一行中文
        pass
      else:
        total_client_fortume=total_client_fortume+float(i[3])#读取第四列总资产求和
  print('当日营业部总资产（排除6666开头的账户）:'+str(total_client_fortume))#计算了用户资产表的总资产
 
#读写总表
import xlrd
from xlrd import xldate_as_tuple
import xlwt
from xlutils.copy import copy
#打印当前时间
import time
from datetime import datetime
write_time=time.strftime('%Y-%m-%d',time.localtime(time.time())) 
#print('当前时间为：'+write_time)
#获取excel表行数
data = xlrd.open_workbook(client_total) # 打开xls文件
table = data.sheets()[0] # 打开第一张表
nrows = table.nrows      # 获取表的行数
#print('获取表的行数:'+str(nrows))
first_2018=0.00#2018/01/02的值
index=0
for i in range(nrows):   # 循环逐行遍历excel表
  if index<2:
    pass
  else:
    cell = table.cell_value(i,0)
    date = datetime(*xldate_as_tuple(cell, 0))
    cell = date.strftime('%Y-%m-%d')
    if '2018-01-02'==cell:
      first_2018=table.cell_value(i,1)
  index=index+1
print('2018/01/02资产为：'+str(first_2018))
today_up=total_client_fortume-first_2018#年净增长资产=当天总资产-2018年1月2日的资产
print('年净增长资产为：'+str(today_up))
today_up_rate=today_up/first_2018*100#年资产增长率=（当总天资产-2018年1月2日的资产）/-2018年1月2日的资产
print('年资产增长率为：'+str(today_up_rate)+"%")
yesterday_total=table.cell_value(2,1)
print('昨日资产为：'+str(yesterday_total))
yesterday_total_cross=total_client_fortume-yesterday_total
print('较昨日增长资产为：'+str(yesterday_total_cross))
yesterday_up_rate=yesterday_total_cross/yesterday_total*100#较昨日资产增长率=（当天总资产-昨日总资产）/昨日总资产
print('较昨日资产增长率:'+str(yesterday_up_rate)+"%")#较昨日资产增长率=（当天总资产-昨日总资产）/昨日总资产

#删除原来的excel表
import os
newfile=new_generate_file
if os.path.exists(newfile):
  os.remove(newfile)
newfile=chat_file
if os.path.exists(newfile):
  os.remove(newfile)
newfile=word_file
if os.path.exists(newfile):
  os.remove(newfile)
# 打开想要更改的excel文件
rb = xlrd.open_workbook(client_total)    #打开weng.xls文件
wb = copy(rb)                          #利用xlutils.copy下的copy函数复制
ws = wb.get_sheet(0)
table = rb.sheets()[0] # 打开第一张表
nrows = table.nrows      # 获取表的行数
index=0
for i in range(nrows):   # 循环逐行遍历excel表
  if index<2:
    pass
  else:
    cell = table.cell_value(i,0)
    date = datetime(*xldate_as_tuple(cell, 0))
    cell = date.strftime('%Y-%m-%d')
    ws.write(i, 0, cell)#日期
  index=index+1
# 写入数据
ws.write(nrows, 0, write_time)#日期
ws.write(nrows, 1, total_client_fortume)#营业部总资产
ws.write(nrows, 2, today_up)#年净增长资产
ws.write(nrows, 3, today_up_rate)#年资产增长率
ws.write(nrows, 4, yesterday_total_cross)#较昨日增长资产
ws.write(nrows, 5, yesterday_up_rate)#较昨日资产增长率

for i2 in range(0,4):
  ws = wb.get_sheet(i2)
  table = rb.sheets()[i2] # 打后面的表
  nrows = table.nrows      # 获取表的行数
  index=0
  for i in range(nrows):   # 循环逐行遍历excel表
    if index<2:
      pass
    else:
      cell = table.cell_value(i,0)
      date = datetime(*xldate_as_tuple(cell, 0))
      cell = date.strftime('%Y-%m-%d')
      ws.write(i, 0, cell)#日期
    index=index+1
# 另存为excel文件，生成新文件
wb.save(new_generate_file)

import matplotlib.pyplot as plt
from pylab import *                                 #支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']
rb = xlrd.open_workbook(new_generate_file)    #打开生成文件
table = rb.sheets()[0] # 打开第一张表
nrows = table.nrows      # 获取表的行数
index=0
names=[]
y=[]
for i in range(nrows):   # 循环逐行遍历excel表
  if index<2:
    pass
  else:
    names.append(table.cell_value(i,0))
    y.append(table.cell_value(i,1))
  index=index+1
x = range(len(names))
plt.plot(x, y)
plt.legend()  # 让图例生效
plt.xlabel(u"天") #X轴标签
plt.ylabel("总资产（元）") #Y轴标签
plt.title("营业部总资产") #标题
#plt.show()
plt.savefig(chat_file)

from os import listdir
from docx import Document
from docx.shared import Inches
myDocument=Document()
pictures=[fn for fn in listdir() if fn.endswith('.jpg')]
pictures.sort()

for fn in pictures:
  myDocument.add_picture(fn,width=Inches(6),height=Inches(8))
myDocument.save(word_file)


