docker pull jenkins

mkdir -p ~/jenkins

chmod -R 777 ~/jenkins

docker run -d -p 8002:8080 -v ~/jenkins:/var/jenkins_home --name jenkins --restart=always jenkins

http://192.168.225.110:8002/pluginManager/advanced