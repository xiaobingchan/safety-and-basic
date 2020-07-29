![](https://imgkr.cn-bj.ufileos.com/1b505d1d-079b-4586-8840-30ae644603bd.jpg)

### 2.2 AIDE入侵检测系统
```shell
# 步骤一：部署AIDE入侵检测系统
1）安装： 
$ yum -y install aide    
2）修改配置文件：
$ vim /etc/aide.conf   （确定对哪些数据进行校验，如何校验数据）

步骤二：初始化数据库，入侵后检测
1）入侵前对数据进行校验，生成初始化数据库：
$ aide --init

AIDE, version 0.15.1

### AIDE database at /var/lib/aide/aide.db.new.gz initialized.
//生成校验数据库，数据保存在/var/lib/aide/aide.db.new.gz

$ cp /var/lib/aide/aide.db.new.gz  /var/lib/aide/aide.db.gz  /自定义目录/
$ aide --check    //检查哪些数据发生了变化

AIDE 0.15.1 found differences between database and filesystem!!
Start timestamp: 2020-07-26 07:32:46

Summary:
  Total number of files:	47466
  Added files:			11
  Removed files:		0
  Changed files:		0
```
