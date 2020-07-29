mkdir -p /etc/docker
cat >/etc/docker/daemon.json <<EOF
{
  "registry-mirrors": ["https://ot7dvptd.mirror.aliyuncs.com"]
}
EOF
systemctl daemon-reload
systemctl restart docker

cat > app.py <<EOF
from flask import Flask
import json
app = Flask(__name__)
@app.route('/')
def index():
    resp = {"code": 0, "status": "1", "userid": "2"}
    resp = json.dumps(resp)
    return resp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False)
EOF

cat > Dockerfile <<EOF
FROM python:3.6-alpine
MAINTAINER XenonStack
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com flask
EXPOSE 5001
CMD ["python", "app.py"]
EOF

解决办法：
# vi /etc/sysctl.conf
或者
# vi /usr/lib/sysctl.d/00-system.conf
添加如下代码：
    net.ipv4.ip_forward=1
重启network服务
# systemctl restart network
查看是否修改成功
# sysctl net.ipv4.ip_forward


docker build -t k8s_python_sample_code .

# Docker 运行
docker run --name python-flask -d -p 5001:5001 -d k8s_python_sample_code

docker pull registry
mkdir -p /opt/auth
docker run --entrypoint htpasswd registry:2 -Bbn liaochao 123456 > /opt/auth/htpasswd
docker run -d -p 5000:5000 --restart=always --name registry1 \
-v /opt/auth:/auth \
-e "REGISTRY_AUTH=htpasswd" \
-e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
-e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
registry

docker login 127.0.0.1:5000

docker tag 9bcca452fe21 127.0.0.1:5000/chao/k8s_python_sample_code2233
docker push 127.0.0.1:5000/chao/k8s_python_sample_code2233


cat > /etc/docker/daemon.json <<EOF
{
  "insecure-registries": ["127.0.0.1:5000"]
}
EOF
systemctl daemon-reload
systemctl restart docker


kubectl create secret docker-registry registrykey-test --docker-server=127.0.0.1:5000 --docker-username=liaochao --docker-password=123456 --docker-email=test@boke.com -n default

#namespace 名称： default
#登录邮箱： test@boke.com
#登录仓库用户名： liaochao
#登录仓库密码： 123456
#pod 要使用的 key 的名称： registrykey-test
#仓库地址： 127.0.0.1:5000

cat > flask-rc.yaml <<EOF
apiVersion: v1
kind: ReplicationController
metadata:
  name: flask-controller
spec:
  replicas: 2
  selector:
    name: flask
  template:
    metadata:
      labels:
        name: flask
    spec:
      imagePullSecrets:
        - name: registrykey-test
      containers:
        - name: flask
          image: 127.0.0.1:5000/chao/k8s_python_sample_code2233
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 5001
EOF

cat > flask-service.yaml <<EOF
apiVersion: v1
kind: Service
metadata:
  name: flask-service-nodeport
spec:
  ports:
    - port: 5001
      targetPort: 5001
      protocol: TCP
  type: NodePort
  selector:
    name: flask
EOF
kubectl apply -f flask-rc.yaml
kubectl apply -f flask-service.yaml

kubectl get pod
kubectl get svc
kubectl describe svc flask-service-nodeport

kubectl delete pod flask-controller-7mnbs
