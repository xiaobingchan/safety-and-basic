![](https://imgkr.cn-bj.ufileos.com/1b505d1d-079b-4586-8840-30ae644603bd.jpg)
### 2.3 Linux杀毒软件clamav
```shell
# 1，配置阿里源
$ mv /etc/yum.repos.d/ /etc/yum.repos.d.bak/
$ wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
$ wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
$ sed -i '/aliyuncs/d' /etc/yum.repos.d/CentOS-Base.repo
$ sed -i '/aliyuncs/d' /etc/yum.repos.d/epel.repo
$ sed -i 's/$releasever/7/g' /etc/yum.repos.d/CentOS-Base.repo

# 2，安装clamav
$ yum -y install epel-release
$ yum -y install clamav
$ freshclam # 更新病毒库
$ clamscan –ri /root/clamav/ -l clamscan.log # 开始扫描 /root/clamav/
```

