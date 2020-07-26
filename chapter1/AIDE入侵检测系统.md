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
//生成校验数据库，数据保存在/var/lib/aide/aide.db.new.gz
2）备份数据库
$ cp /var/lib/aide/aide.db.new.gz   /自定义目录/
3）入侵后检测：
$ cd /var/lib/aide/
$ mv aide.db.new.gz   aide.db.gz
$ aide --check    //检查哪些数据发生了变化
```
