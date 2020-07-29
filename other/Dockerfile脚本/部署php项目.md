# 参考文章：https://www.awaimai.com/728.html

# yum安装php：
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm
yum -y install php72w
yum -y install php72w-cli php72w-common php72w-devel php72w-mysql php72w-xml php72w-odbc


1、部署MySQL

$ docker pull mysql
$ docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=my-secret-pw -d daocloud.io/library/mysql:5.6

2、部署Nginx

$ docker pull nginx
$ docker run --name nginx -p 80:80 -d nginx

3、映射HTML路径
mkdir -p ~/www/html/
编写index.hmtl文件
docker rm -f nginx
docker run --name nginx -p 80:80 -d -v ~/www/html:/usr/share/nginx/html nginx


cd ~/www
docker cp nginx:/etc/nginx/conf.d/default.conf default.conf
docker rm -f nginx

编辑default.conf内容：
#####################################
server {
    listen       80;
    server_name  _;
    root /usr/share/nginx/html;
    index index.php index.html index.htm;
    location / {
	try_files $uri $uri/ =404;
    }
    error_page  404  /404.html;
    location = /40x.html {
        root    /user/share/nginx/html;     
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
    location ~ \.php$ {
        fastcgi_pass   php-fpm:9000;
        fastcgi_index  index.php;
	fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include        fastcgi_params;
    }
    location ~ /\.ht {
        deny  all;
    }
}
#####################################

docker run --name nginx -p 80:80 -v ~/www/html:/usr/share/nginx/html -v ~/www/default.conf:/etc/nginx/conf.d/default.conf -d nginx


docker pull php:fpm
docker run --name php-fpm -p 9000:9000 -d php:fpm
cd ~/www
docker cp php-fpm:/usr/local/etc/php-fpm.d/www.conf www.conf
docker cp php-fpm:/usr/local/etc/php/php.ini-production php.ini

# 在本地服务器修改 php.ini 的内容，设置cgi.fix_pathinfo=0（要先删除前面的;注释符）：
cgi.fix_pathinfo=0
# 地址对应不对
docker run --name php-fpm --link mysql:mysql -v ~/www/html:/usr/share/nginx/html -v ~/www/www.conf:/usr/local/etc/php-fpm.d/www.conf -v ~/www/php.ini:/usr/local/etc/php/php.ini -d php:fpm
