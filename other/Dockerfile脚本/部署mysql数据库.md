配置文件位置：/etc/mysql/my.cnf

docker pull mysql

mkdir -p /docker/mysql_data

docker run --name mysql -d --restart always -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -v /docker/mysql_data:/var/lib/mysql mysql

