# -*- coding:utf-8 -*-
# 用途：日常运行命令并发送邮件
# 传参：数字（业务上的id）、日期（yyyyMMdd）、日期（yyyyMMdd）、运行环境（dev/test/prod）
# 命令举例： python  test.py  4,dev

from time import time, localtime, strftime
import sys
import datetime
from datetime import datetime
from datetime import timedelta
import calendar
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import commands

# 执行Docker命令
def dockerexec(cal_startdate,cal_enddate,bussiness_id,typed,rundev):
    docker_command="docker xxxx test.py "+ cal_startdate + " " + cal_enddate + " " + bussiness_id + " " + typed + " " + rundev 
    mail_content=""
    docker_result,docker_return = commands.getstatusoutput(docker_command)
    if docker_result == 0:   # 成功
        docker_return=docker_return.replace("success,","")
        docker_return=docker_return.replace("fail,","")
        mail_content=mail_content+"1，docker 命令执行成功"+",执行结果："+docker_return+"<br/>"
    else:  # 失败
        docker_return=docker_return.replace("success,","")
        docker_return=docker_return.replace("fail,","")
        mail_content=mail_content+"1，docker 命令执行失败"+",执行结果："+docker_return+"<br/>"
    return str(mail_content)

# 请修改以下参数
host_server = 'smtp.qq.com' #qq邮箱smtp服务器
sender_qq = '1290851757@qq.com' #sender_qq为发件人的qq号码
pwd = 'nzqygrzwccgpiejb' #pwd为qq邮箱的授权码
sender_qq_mail = '1290851757@qq.com' #发件人的邮箱
receiver = '1755337994@qq.com' #收件人邮箱
url="http://127.0.0.1:18001/link-api/yfy/getYfyData"

all_param=sys.argv[1]
bussiness_id = all_param.split(",")[0] # 业务id
rundev= all_param.split(",")[1]  # 运行环境

typed="" # 日期类型
cal_startdate = ""  # 计算的开始日期
cal_enddate = ""   # 计算的结束日期

# 获取当前时间
x = localtime(time())

weekday = strftime("%A", x)  # 周几
day = strftime("%d", x)  # 日
month = strftime("%m", x)  # 月
year = strftime("%Y", x)  # 年

weekday = "Wednsday"
day = "01"
month = "04"
year = "2020"

day=str(int(day))
month=str(int(month))

print weekday
print day
print month
print year

# 定义docker邮件内容
docker_email_content=""

# 如果是1月1号，生成上年度的的SVARD年数据
if month == "1" and day == "1":
    typed="a"
    year_tmp = int(year)-1
    cal_startdate = str(year_tmp)+"0101"
    cal_enddate = str(year_tmp)+"1231"
    print cal_startdate
    print cal_enddate
    print "是1月1号，生成上年度的的SVARD年数据"

# 如果是1号，且正好是季度起始日，生成上季度的的SVARD季数据
jidu = int(month) % 3  # 判断是否是季度月
if day == "1" and jidu == 1:
    typed="q"
    if month == "1":  # 假设1月1日
        year = int(year)
        cal_startdate = str(year)+"1001"
        cal_enddate = str(year)+"1231"
    else:
        startmonth = int(month) - 3  # 起始月
        if int(startmonth) < 10:
            startmonth = "0"+str(int(startmonth))
        endmonth = int(month) - 1  # 结束月
        if int(endmonth) < 10:
            endmonth = "0"+str(int(endmonth))
        cal_startdate = str(year)+startmonth+"01"
        # 判断每月天数，比如2016年9月有30日
        monthRange = calendar.monthrange(int(year), int(month)-1)
        cal_enddate = str(year)+endmonth+str(monthRange[1])
    print cal_startdate
    print cal_enddate
    print "1号，且正好是季度起始日，生成上季度的的SVARD季数据"

# 如果是1号，生成上月的SVARD月数据
if day == "1":
    typed="m"
    if month == "1":  # 假设1月
        year = int(year)
        cal_startdate = str(year)+"1201"
        cal_enddate = str(year)+"1231"
    else:
        startmonth = int(month) - 1  # 起始月
        if int(startmonth) < 10:
            startmonth = "0"+str(int(startmonth))
        cal_startdate = str(year)+startmonth+"01"
        # 判断每月天数，比如2016年9月有30日
        monthRange = calendar.monthrange(int(year), int(month)-1)
        cal_enddate = str(year)+startmonth+str(monthRange[1])
    print cal_startdate
    print cal_enddate
    print "1号，生成上月的SVARD月数据"

if int(month)<10:
    month="0"+str(month)
if int(day)<10:
    day="0"+str(day)

# 如果是周一，生成上周的SVARD周数据。假设今天是20200525
if weekday == "Monday":
    import datetime
    cur_date=datetime.datetime(int(year), int(month), int(day)) - datetime.timedelta(days=1) # 计算昨天为enddate
    cal_enddate=cur_date.strftime('%Y%m%d')
    typed="w"
    n=7 # 计算上周
    cur_date = datetime.datetime(int(year), int(month), int(day)) - datetime.timedelta(days=n)
    cal_startdate = cur_date.strftime('%Y%m%d')
    print cal_startdate
    print cal_enddate
    print "周一，生成上周的SVARD周数据"

# 生成昨日SVARD数据日。假设今天是20200520
typed="d"
import datetime
n=1 # 计算上周
cur_date = datetime.datetime(int(year), int(month), int(day)) - datetime.timedelta(days=n)	# 2015-10-29 00:00:00
cal_startdate = cur_date.strftime('%Y%m%d')
cal_enddate=cal_startdate
print cal_startdate
print cal_enddate
print "生成昨日SVARD数据日"

# 生成昨日SVARD数据日。假设今天是20200520
# 20200519 20200519 1 d dev
# 如果是周一，生成上周的SVARD周数据。假设今天是20200525
# 20200518 20200524 1 w dev
# 如果是1号，生成上月的SVARD月数据。假设今天是20200601
# 20200501 20200531 1 m dev
# 如果是1号，且正好是季度起始日，生成上季度的的SVARD季数据。假设今天是20200701
# 20200401 20200630 1 q dev
# 如果是1月1号，生成上年度的的SVARD年数据。假设今天是20210101
# 20200101 20201231 1 a dev
