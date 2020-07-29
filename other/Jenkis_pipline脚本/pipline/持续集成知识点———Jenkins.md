首先安装jdk环境
#############################################################
wget https://repo.huaweicloud.com/java/jdk/8u202-b08/jdk-8u202-linux-x64.tar.gz
mkdir -p /usr/java/
tar -xzvf jdk-8u202-linux-x64.tar.gz -C /usr/java/
pid="sed -i '/export JAVA_HOME/d' /etc/profile"
eval $pid
pid="sed -i '/export CLASSPATH/d' /etc/profile"
eval $pid
cat >> /etc/profile <<EOF
export JAVA_HOME=/usr/java/jdk1.8.0_152
export CLASSPATH=%JAVA_HOME%/lib:%JAVA_HOME%/jre/lib
export PATH=\$PATH:\$JAVA_HOME/bin
EOF
source /etc/profile
java -version
ln -s /usr/java/jdk1.8.0_152/bin/java /usr/bin
#############################################################

安装jenkins
#############################################################
wget https://mirrors.huaweicloud.com/jenkins/redhat-stable/jenkins-2.222.4-1.1.noarch.rpm
rpm -ivh jenkins-2.222.4-1.1.noarch.rpm
service jenkins start
firewall-cmd --permanent --zone=public --add-port=8080/tcp
firewall-cmd --reload
访问网址：http://192.168.244.180:8080/
#############################################################

安装gitlab
#############################################################
yum -y install policycoreutils openssh-server openssh-clients postfix
systemctl enable postfix && systemctl start postfix
firewall-cmd --permanent --zone=public --add-port=9091/tcp
firewall-cmd --reload
wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-11.9.9-ce.0.el7.x86_64.rpm
rpm -i gitlab-ce-11.9.9-ce.0.el7.x86_64.rpm

vi  /etc/gitlab/gitlab.rb
external_url 'http://127.0.0.1:9091'  # 配置访问地址
nginx['listen_port'] = 9091  # 配置端口

gitlab-ctl reconfigure
gitlab-ctl restart
free -m
访问 http://127.0.0.1:9091
#############################################################


安装gitee
#############################################################
先安装mysql数据库

wget -O gitea https://dl.gitea.io/gitea/1.8.2/gitea-1.8.2-linux-amd64
chmod +x gitea-1.8.2-linux-amd64
yum -y install git
nohup ./gitea-1.8.2-linux-amd64 web &
firewall-cmd --permanent --zone=public --add-port=3000/tcp
firewall-cmd --reload
#############################################################

新建任务 ： new item -> 配置  -> general -> 参数化构建过程 -> 执行 shell   echo ${branch}
            git 分支    ${branch}

扩展化参数化构建插件：Extended Choice Parameter

分隔符Delimiter：,
/opt/jenkins.property
abc=test,test2

git参数插件：Git Parameter

Jenkins：https://www.bilibili.com/video/BV1kJ411p7mV?p=39

官方文档：https://www.jenkins.io/zh/doc/

1，jenkis新建token：进入 http://192.168.225.146:8080/user/用户名/configure  新建TOKEN
113f2141835ca191a1e493aa6935476f76

全局工具配置-> 安装Maven/JDK/git/

系统管理->插件管理:	
Git
Deploy to container
Role-based Authorization Strategy	
Credentials
Credentials Binding Plugin
Publish Over SSH
Pipline
Node
Extended Choice Parameter
Docker plugins
docker-build-steps
SSH plugin
Git Parameter
Maven Integration
Gradle Plugin
Git plugin
SSH plugin
Maven Integration
Build Authorization Token Root
Gitlab
Gitlab Hook Plugin
SonarQube Scanner
Email Extension Plugin
Kubernete
安装gitlab插件
安装github插件

系统管理->全局安全配置:
安全域:允许用户注册
项目矩阵授权策略:匿名用户有管理权


2，新建api触发执行bash：item->设置->触发远程构建 (例如,使用脚本)->执行bash
执行网址：http://118.89.23.220:8080/job/test_shell/build?token=123456

3，安装插件"Maven Integration"和"Build Authorization Token Root"

4，查询http构建情况：https://blog.csdn.net/boling_cavalry/article/details/85373901
查询执行情况：http://118.89.23.220:8080/job/test_shell/api/json

6，Java git自动构建Spring：https://blog.csdn.net/boling_cavalry/article/details/78942408
git地址：https://github.com/xiaobingchan/github_jenkins_test.git

7，Github提交代码自动构建：https://blog.csdn.net/boling_cavalry/article/details/78943061
webhook地址就是 http://118.89.23.220:8088/github-webhook
设置github webhook：https://github.com/xiaobingchan/github_jenkins_test/settings
登录GitHub，进入"Settings"页面：https://github.com/settings/profile，点击左下角的"Developer settings"
https://github.com/settings/tokens，勾选repo 、admin:repo_hook
token:c650c382247db0aff1177829fbe6ab36f01432e5
Jenkins 系统管理  新增Github Server：Github 服务器

选择"Git"；
"Repository URL"输入仓库地址：https://github.com/zq2599/jenkinsdemo.git；
“Credentials"创建一个Credentials，Kind选择"Username with password”，Username输入GitHub账号，Password输入GitHub密码；
“源码库浏览器"选择"githubweb”；
"URL"输入项目主页：https://github.com/zq2599/jenkinsdemo；
“构建触发器"中勾选"GitHub hook trigger for GiTScm polling”；
勾选Use secret text


8，Gitlab提交代码自动构建：https://www.jianshu.com/p/2b03dc582971
进入：https://gitlab.com/xiaobingchan/jenkins_test_gitlab/hooks配置webhook
1116a3c4ff037a5f571a75866fc6c01ef0
禁止跨站请求：[root@VM-0-12-centos ~]# cat  /etc/sysconfig/jenkins | grep "JAVA"
JENKINS_JAVA_CMD=""
JENKINS_JAVA_OPTIONS="-Djava.awt.headless=true  -Dhudson.security.csrf.GlobalCrumbIssuerConfiguration.DISABLE_CSRF_PROTECTION=true"

插件更新中心：https://updates.jenkins.io/experimental/update-center.json

9，Pipline流水线：https://www.jenkins.io/zh/doc/book/pipeline/getting-started/
流水线生成器：http://192.168.225.155:8080/job/dfawdwadwa/pipeline-syntax/

普通结构：
pipeline {
    agent any 
    stages {
        stage('Stage 1') {
            steps {
                echo 'Hello world!' 
            }
        }
		stage('Stage 2') {
            steps {
                echo 'Hello world!' 
            }
        }
    }
}


10，修改jenkins默认启动端口：cat /etc/sysconfig/jenkins | grep JENKINS_PORT

11，Pipline流水线解析json body：https://www.coder.work/article/2572693

12，代码检测平台SonarQube：安装插件 “Sonar Quality Gates Plugin”；
下载sonar-pdf-plugin插件：https://blog.csdn.net/tanglei6636/article/details/90206073
分支检测代码：https://blog.csdn.net/qq_16681279/article/details/88633489

13，

ssh-keygen -t rsa -C "luyanjie4@gmail.com"

github提交触发Jenkins：https://juejin.im/post/5dbd80aef265da4cf77c894d

maven+docker+tomcat+harbor部署：https://blog.csdn.net/xiaoxiangzi520/article/details/88842200

Send build artifacts over SSH：分发文件到SSH机器：

Name：默认的，不用填写
Source files：传到对应服务器的目录
Remove prefix：从source files中过滤掉填写的目录
Remote directory：传到服务器上对应的目录，这里是已设置好了的
Exec command：在服务器上的运行命令

CICD 概

1，CI 持续集成 Continuous Integration  代码发布、构建、部署、测试
2，CD 持续部署 Continuous Deployment   发布到各种环境
3，CD 持续交付 Continuous Delivery     

