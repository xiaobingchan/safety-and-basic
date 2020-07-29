# -*- coding:utf-8 -*-
# 用途：日常运行命令并发送邮件
# 传参：数字（业务上的id）、日期（yyyyMMdd）、日期（yyyyMMdd）、运行环境（dev/test/prod）
# 命令举例： python  test.py  4,20200101,20200520,dev

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

# 请修改以下参数
host_server = 'smtp.qq.com' #qq邮箱smtp服务器
sender_qq = '1290851757@qq.com' #sender_qq为发件人的qq号码
pwd = 'nzqygrzwccgpiejb' #pwd为qq邮箱的授权码
sender_qq_mail = '1290851757@qq.com' #发件人的邮箱
receiver = '1755337994@qq.com' #收件人邮箱
url="http://127.0.0.1:18001/link-api/yfy/getYfyData"

all_param=sys.argv[1]
bussiness_id = all_param.split(",")[0] # 业务id
startdate = all_param.split(",")[1]  # 开始日期
enddate = all_param.split(",")[2]  # 结束日期
rundev= all_param.split(",")[3]  # 运行环境

# bussiness_id = sys.argv[1]  # 业务id
# startdate = sys.argv[2]  # 开始日期
# enddate = sys.argv[3]  # 结束日期
# rundev= sys.argv[4]  # 运行环境

typed="" # 日期类型
cal_startdate = ""  # 计算的开始日期
cal_enddate = ""   # 计算的结束日期


# 获取当前时间
x = localtime(time())
weekday = strftime("%A", x)  # 周几
day = strftime("%d", x)  # 日
month = strftime("%m", x)  # 月
year = strftime("%Y", x)  # 年
# 如果是1月1号，生成上年度的的SVARD年数据
if month == "01" and day == "01":
    typed="a"
    year = int(year)-1
    cal_startdate = str(year)+"0101"
    cal_enddate = str(year)+"1231"
else:
    # 如果是1号，且正好是季度起始日，生成上季度的的SVARD季数据
    jidu = int(month) % 3  # 判断是否是季度月
    if day == "01" and jidu == 1:
        typed="q"
        if month == "01":  # 假设1月1日
            year = int(year)-1
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
            monthRange = calendar.monthrange(year, month)
            cal_enddate = str(year)+endmonth+str(monthRange[1])
    else:
        # 如果是1号，生成上月的SVARD月数据
        if day == "01" and jidu != 1:
            typed="m"
            if month == "01":  # 假设1月
                year = int(year)-1
                cal_startdate = str(year)+"1201"
                cal_enddate = str(year)+"1231"
            else:
                startmonth = int(month) - 1  # 起始月
                if int(startmonth) < 10:
                    startmonth = "0"+str(int(startmonth))
                cal_startdate = str(year)+startmonth+"01"
                # 判断每月天数，比如2016年9月有30日
                monthRange = calendar.monthrange(year, month)
                cal_enddate = str(year)+startmonth+str(monthRange[1])
        else:
            # 如果是周一，生成上周的SVARD周数据。假设今天是20200525
            if weekday == "Monday":
                typed="w"
                import datetime
                now = datetime.datetime.now()
                last_week_start = now - timedelta(days=now.weekday()+7)
                last_week_end = now - timedelta(days=now.weekday()+1)
                last_week_start = str(last_week_start).split(" ")[0]
                last_week_start = last_week_start.replace("-", "")
                last_week_end = str(last_week_end).split(" ")[0]
                last_week_end = last_week_end.replace("-", "")
                cal_startdate = last_week_start
                cal_enddate = last_week_end
            # 生成昨日SVARD数据日。假设今天是20200520
            else:
                typed="d"
                import datetime
                today = datetime.date.today()
                oneday = datetime.timedelta(days=1)
                yesterday = today-oneday
                # 去除字符串的 -
                cal_startdate = cal_startdate.replace("-", "")
                cal_enddate = cal_startdate

# 生成昨日SVARD数据日。假设今天是20200520
# docker xxxx test.py 20200519 20200519 1 d dev
# 如果是周一，生成上周的SVARD周数据。假设今天是20200525
# docker xxxx test.py 20200518 20200524 1 w dev
# 如果是1号，生成上月的SVARD月数据。假设今天是20200601
# docker xxxx test.py 20200501 20200531 1 m dev
# 如果是1号，且正好是季度起始日，生成上季度的的SVARD季数据。假设今天是20200701
# docker xxxx test.py 20200401 20200630 1 q dev
# 如果是1月1号，生成上年度的的SVARD年数据。假设今天是20210101
# docker xxxx test.py 20200101 20201231 1 a dev

# docker_command="docker run --rm -v /home/r:/home/docker -w /home/docker/code -u docker r-link Rscript gl_1.R"
#邮件的正文内容
import time
mail_content = str(time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time())))+" docker 和 url  状态检测情况：<br/>"
#邮件标题
mail_title = str(time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time())))+" docker 和 url  状态检测情况"

docker_command="docker xxxx test.py "+ cal_startdate + " " + cal_enddate + " " + bussiness_id + " " + typed + " " + rundev 
# 执行Docker命令
docker_result,docker_return = commands.getstatusoutput(docker_command)
if docker_result == 0:   # 成功
    docker_return=docker_return.replace("success,","")
    docker_return=docker_return.replace("fail,","")
    mail_content=mail_content+"1，docker 命令执行成功"+",执行结果："+docker_return+"<br/>"
else:  # 失败
    docker_return=docker_return.replace("success,","")
    docker_return=docker_return.replace("fail,","")
    mail_content=mail_content+"1，docker 命令执行失败"+",执行结果："+docker_return+"<br/>"

# 执行Curl命令
curl_command="curl -X POST "+url
curl_result,curl_return = commands.getstatusoutput(curl_command)
if curl_result == 0:   # 成功
    curl_return=curl_return.replace("success,","")
    curl_return=curl_return.replace("fail,","")
    mail_content=mail_content+"2，Curl 命令执行成功"+",执行结果："+curl_return+"<br/>"
else:  # 失败
    curl_return=curl_return.replace("success,","")
    curl_return=curl_return.replace("fail,","")
    mail_content=mail_content+"2，Curl 命令执行失败"+",执行结果："+curl_return+"<br/>"

# 发送邮件
#ssl登录
smtp = SMTP_SSL(host_server)
#set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(sender_qq, pwd)
msg = MIMEText(mail_content, "html", 'utf-8')
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = sender_qq_mail
msg["To"] = Header("url探测", 'utf-8') ## 接收者的别名
smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
smtp.quit()