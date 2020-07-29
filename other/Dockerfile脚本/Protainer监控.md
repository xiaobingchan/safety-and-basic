docker search portainer
docker pull portainer/portainer
docker run -ti -d --name kevin-portainer -p 9000:9000 --restart=always -v /var/run/docker.sock:/var/run/docker.sock  portainer/portainer
