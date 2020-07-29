docker pull nginx:latest
docker run --name nginx-test -p 8880:80 -d nginx
curl http://127.0.0.1:8880
