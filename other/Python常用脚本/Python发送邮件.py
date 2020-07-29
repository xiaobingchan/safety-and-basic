# 参考教材：https://www.jianshu.com/p/05f0fe88c61d

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


#qq邮箱smtp服务器
host_server = 'smtp.qq.com'
#sender_qq为发件人的qq号码
sender_qq = '1290851757@qq.com'
#pwd为qq邮箱的授权码
pwd = 'nzqygrzwccgpiejb' ##
#发件人的邮箱
sender_qq_mail = '1290851757@qq.com'
#收件人邮箱
receiver = '1755337994@qq.com'

#邮件的正文内容
mail_content = "你好，<p>这是使用python登录qq邮箱发送HTML格式邮件的测试：</p><p><a href='http://www.yiibai.com'>易百教程</a></p>"
#邮件标题
mail_title = 'Maxsu的邮件'


#ssl登录
smtp = SMTP_SSL(host_server)
#set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(sender_qq, pwd)

msg = MIMEText(mail_content, "html", 'utf-8')
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = sender_qq_mail
msg["To"] = Header("接收者测试", 'utf-8') ## 接收者的别名

smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
smtp.quit()
