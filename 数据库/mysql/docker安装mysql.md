

# 一、docker 安装mysql



**第一步：**

```
docker search mysql
```



```bash
[root@hecs-263993-0001 ~]# docker search mysql
NAME                              DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
mysql                             MySQL is a widely used, open-source relation…   11312     [OK]       
mariadb                           MariaDB Server is a high performing open sou…   4299      [OK]       
mysql/mysql-server                Optimized MySQL Server Docker images. Create…   838                  [OK]
centos/mysql-57-centos7           MySQL 5.7 SQL database server                   91                   
mysql/mysql-cluster               Experimental MySQL Cluster Docker images. Cr…   88                   
centurylink/mysql                 Image containing mysql. Optimized to be link…   59                   [OK]
databack/mysql-backup             Back up mysql databases to... anywhere!         46                   
prom/mysqld-exporter                                                              42                   [OK]
deitch/mysql-backup               REPLACED! Please use http://hub.docker.com/r…   41                   [OK]
tutum/mysql                       Base docker image to run a MySQL database se…   35                   
linuxserver/mysql                 A Mysql container, brought to you by LinuxSe…   31                   
schickling/mysql-backup-s3        Backup MySQL to S3 (supports periodic backup…   30                   [OK]
mysql/mysql-router                MySQL Router provides transparent routing be…   21                   
centos/mysql-56-centos7           MySQL 5.6 SQL database server                   20                   
arey/mysql-client                 Run a MySQL client from a docker container      18                   [OK]
fradelg/mysql-cron-backup         MySQL/MariaDB database backup using cron tas…   16                   [OK]
genschsa/mysql-employees          MySQL Employee Sample Database                  7                    [OK]
yloeffler/mysql-backup            This image runs mysqldump to backup data usi…   7                    [OK]
openshift/mysql-55-centos7        DEPRECATED: A Centos7 based MySQL v5.5 image…   6                    
devilbox/mysql                    Retagged MySQL, MariaDB and PerconaDB offici…   3                    
jelastic/mysql                    An image of the MySQL database server mainta…   2                    
ansibleplaybookbundle/mysql-apb   An APB which deploys RHSCL MySQL                2                    [OK]
widdpim/mysql-client              Dockerized MySQL Client (5.7) including Curl…   1                    [OK]
centos/mysql-80-centos7           MySQL 8.0 SQL database server                   1                    
monasca/mysql-init                A minimal decoupled init container for mysql    0                    
```



**第二步：**

```bash
# 拉取官方镜像
docker pull mysql
```





**第三步：创建挂载目录**

```bash
命令：cd /opt/

命令：mkdir mysql_docker

命令：cd mysql_docker/

命令：echo $PWD
/opt/mysql_docker
```



**第四步：创建容器**

```bash
docker run --name mysql -v $PWD/conf:/etc/mysql/conf.d -v $PWD/logs:/logs -v $PWD/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d -i -p 3306:3306 mysql:latest
```

备注：也可以不需要挂载，学习的时候，可以不用挂载目录

命令强烈建议用我这个 docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql:latest 不然mysql的状态一直是exited

**第五步：进入容器**

```bash
docker exec -it mysql bash
```



**第六步：进入mysql**

```bash
mysql -uroot -p123456
```



**第七步：开启远程访问权限**

```bash
命令：use mysql;

命令：select host,user from user;

命令：ALTER USER 'z'@'%' IDENTIFIED WITH mysql_native_password BY '123456';

命令：flush privileges;
```

