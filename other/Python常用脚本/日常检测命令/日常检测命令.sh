#!/bin/bash
# 用途：日常运行命令并发送邮件
# 传参：数字（业务上的id）、日期（yyyyMMdd）、日期（yyyyMMdd）、运行环境（dev/test/prod）
# 命令举例：sh test.sh  4  20200101  20200520  dev/test/prod

bussiness_id=$1
statdate=$2
enddate=$3
run_env=$4

### 请修改以下参数
mail_smtp="smtps://smtp.mxhichina.com:465" # 发送邮件的smtp地址
send_mailer="dmd@links-express.com.cn" # 发送邮件的邮箱
send_authpp="" # 发送邮件的邮箱授权码
receive_mail="23940058@qq.com" # 接受邮件的邮箱
docker_command="docker run --rm -v /home/r:/home/docker -w /home/docker/code -u docker r-link Rscript gl_1.R"
url="http://127.0.0.1:18001/link-api/yfy/getYfyData"
email_info=""

log_file=$(date "+%Y-%m-%d_%H:%M:%S")"docker_url.log"

# docker_return=`$docker_command $statdate $enddate $bussiness_id $run_env > $log_file`
# success_line=`cat $log_file | grep "success" | wc -l`
# if [ $success_line -gt 0 ]
# then
#     echo "" >> $log_file
#     echo -ne "{"\"docker_check"\":{"\"value"\":"\"$docker_return"\","\"date"\"$(date "+%Y-%m-%d_%H:%M:%S")"\""\","\"status"\":"\"0"\"}}" >> $log_file
# else
#     echo "" >> $log_file
#     echo -ne "{"\"docker_check"\":{"\"value"\":"\"$docker_return"\","\"date"\"$(date "+%Y-%m-%d_%H:%M:%S")"\""\","\"status"\":"\"1"\"}}"  >> $log_file
# fi

echo "" >> $log_file
curl -X POST "$url" >> $log_file

echo "" >> $log_file

email_info=$email_info`cat $log_file | sed "s/success,//g" | sed "s/fail,//g"`
email_info=$email_info

echo "$(date "+%Y-%m-%d_%H:%M:%S") docker 和 url  状态检测情况： 


$email_info " | mail -v -q -s "$(date "+%Y-%m-%d_%H:%M:%S") docker 和 url  状态检测" -r $send_mailer -a $log_file  -S smtp-auth=login -S $mail_smtp -S smtp-auth-user="$send_mailer" -S smtp-auth-password="$send_authpp" $receive_mail

rm -f $log_file