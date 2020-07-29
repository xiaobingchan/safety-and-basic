# 搭建参考：https://blog.csdn.net/qq_25147521/article/details/105129037

# 镜像地址：docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-apiserver-amd64:v1.18.0
8G 2核心 200GB硬盘

rm -rf /etc/yum.repos.d/*
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
sed -i '/aliyuncs/d' /etc/yum.repos.d/CentOS-Base.repo
sed -i '/aliyuncs/d' /etc/yum.repos.d/epel.repo
sed -i 's/$releasever/7/g' /etc/yum.repos.d/CentOS-Base.repo

hostnamectl set-hostname k8smaster
echo "127.0.0.1   $(hostname)" >> /etc/hosts
export REGISTRY_MIRROR=https://registry.cn-hangzhou.aliyuncs.com
curl -sSL https://kuboard.cn/install-script/v1.18.x/install_kubelet.sh | sh -s 1.15.0
export MASTER_IP=192.168.225.180
export APISERVER_NAME=apiserver.k8smaster
export POD_SUBNET=10.100.0.1/16
sudo mkdir -p /etc/docker
cat >/etc/docker/daemon.json <<EOF
{
  "registry-mirrors": ["https://ot7dvptd.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
echo "${MASTER_IP} ${APISERVER_NAME}" >> /etc/hosts
curl -sSL https://kuboard.cn/install-script/v1.18.x/init_master.sh | sh -s 1.15.0
kubectl get pod -n kube-system -o wide
docker pull calico/node:v3.13.1
docker pull calico/cni:v3.13.1
docker pull calico/pod2daemon-flexvol:v3.13.1

kubectl apply -f https://kuboard.cn/install-script/kuboard.yaml
kubectl apply -f https://addons.kuboard.cn/metrics-server/0.3.6/metrics-server.yaml
kubectl taint nodes --all node-role.kubernetes.io/master-

sudo systemctl restart kubelet
kubectl -n kube-system get secret $(kubectl -n kube-system get secret | grep kuboard-user | awk '{print $1}') -o go-template='{{.data.token}}' | base64 -d


https://kuboard.cn/
https://kubesphere.io/

参考优秀脚本：

curl -L https://kubesphere.io/download/stable/v2.1.1 > installer.tar.gz && tar -zxf installer.tar.gz && cd kubesphere-all-v2.1.1/scripts
curl -sSL https://kuboard.cn/install-script/v1.18.x/install_kubelet.sh | sh -s 1.18.0
curl -sSL https://kuboard.cn/install-script/v1.18.x/init_master.sh | sh -s 1.18.0

参考优秀脚本：

1，kubesphere
2，kuboard
3，Hyper 2.0




学习：https://www.kubernetes.org.cn/course
