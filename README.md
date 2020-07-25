
![](https://imgkr.cn-bj.ufileos.com/1b505d1d-079b-4586-8840-30ae644603bd.jpg)

 **网络安全等级保护2.0合规** 

阿里公共云网络安全等级保护2.0合规能力白皮书V1.0，[点击下载](https://githubssdsdsdadasd.oss-ap-northeast-1.aliyuncs.com/%E9%98%BF%E9%87%8C%E5%85%AC%E5%85%B1%E4%BA%91%E7%BD%91%E7%BB%9C%E5%AE%89%E5%85%A8%E7%AD%89%E7%BA%A7%E4%BF%9D%E6%8A%A42.0%E5%90%88%E8%A7%84%E8%83%BD%E5%8A%9B%E7%99%BD%E7%9A%AE%E4%B9%A6V1.0.pdf?Expires=1595682261&OSSAccessKeyId=TMP.3KkSbDHE5jmb2VFvJc8YAkzwyiEoF4ksVUz3vETfdbmjmLiXmM1XczhENEqpiBKo9h4f4dtVB6AGLXyhvsAXuAVr8V1V5E&Signature=Fj%2BiBg1n3ezfNmrZw%2Fkl5bBZIJU%3D)

## 1 等保2.0 简介

- 等保2.0全称"网络安全等级保护2.0"制度，是我国网络安全领域的基本国策、基本制度。等级保护标准在1.0时代标准的基础上，注重主动防御，从被动防御到事前、事中、事后全流程的安全可信、动态感知和全面审计，实现了对传统信息系统、基础信息网络、云计算、大数据、物联网、移动互联网和工业控制信息系统等级保护对象的全覆盖


## 2 相关安全资料
### 2.1 系统所有文件权限备份，[点击详情](https://mp.weixin.qq.com/s/Old4OOcwWoTmIPoXXpAdIg)
```shell
1、找一个系统版本一样的服务器上操作权限备份

# 备份整个系统权限
$ getfacl -R / > /data/system-all-permissions.facl
2、恢复整个系统权限，在损坏的机器上操作

# 拷贝备份权限文件
$ scp root@192.168.1.10:/data/system-all-permissions.facl /data/

# 恢复整个系统权限
$ setfacl --restore=/data/system-all-permissions.facl

# 权限恢复完，可以找一个业务低峰重启机器
$ reboot
```


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
