# -*- coding: utf-8 -*
import time
import os
import commands
datebase_name="aomm aomm_account aomm_actconfig aomm_compliance aomm_storefile aomm_inspection aomm_softdeploy aomm_startstop aomm_vmware aomm_jobservice aomm_baseline aomm_patch test_aomm test_aomm_account test_aomm_actconfig test_aomm_baseline test_aomm_compliance test_aomm_filestore test_aomm_inspection test_aomm_patch test_aomm_softdeploy test_aomm_startstop"
datebase_list=datebase_name.split(" ")

datadir="/home/nfdw/mysqldata/"+str(time.strftime("%Y%m%d%H%M%S", time.localtime()))
folder = os.path.exists(datadir)
if not folder:
    #判断是否存在文件夹如果不存在则创建为文件夹
    os.makedirs(datadir)

mysqldump_path="/home/mysql/mariadb/bin/mysqldump"
mysql_username="ioszdhyw"
mysql_passwd="ioszdhyw@123"

file = r'/home/nfdw/mysqldump_result.txt'

for datebasename in datebase_list:
    mysqldump_command=mysqldump_path+" -h\"127.0.0.1\""+" -u "+mysql_username+" -p"+mysql_passwd+" "+datebasename+" -S /home/mysql/mariadb/mysql.sock > "+datadir+"/"+datebasename+".sql"
    print '开始备份:'+str(datebasename)
    starttime=str(time.strftime("%Y-%m %d %H:%M:%S", time.localtime()))
    #mysqldump_result=mysqldump_command
    #print mysqldump_result
    mysqldump_result,mysqldump_return = commands.getstatusoutput(mysqldump_command)
    # 追加结果到日志文件
    with open(file, 'a+') as f:
        f.write("备份时间："+starttime+"，备份数据库名："+datebasename+"，备份结果："+str(mysqldump_result)+'\n') 
    print '备份完成:'+str(datebasename)
    # 休眠1秒
    time.sleep(1)



