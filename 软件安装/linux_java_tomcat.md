## java 安装

#### 第一步：解压

```bash
tar -zxvf jdk-8u211-linux-x64.tar.gz #解压到java这个目录下
```



#### 第二步：配置环境java环境变量

【java安装的步骤】
1、通过filezilla这个工具rz也可以，连接上Linux服务器，然后将我们准备好的Java和tomcat的安装包传输到服务器中。
2、对jdk进行解压，命令是  tar zxvf 文件名
3、在根目录的usr这个文件夹里面创建一个叫java的文件夹。
4、将我们解压后出现的那个文件夹移动到上一步创建的Java文件夹中。
5、进入到根目录下面的etc文件夹中，使用vi命令 编辑 profile 这个文件。
6、讲这段内容写到profile这个文件里面的done这个一行下面。
export JAVA_HOME=/usr/java/jdk1.8.0_211
export CLASSPATH=.:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export PATH=$PATH:$JAVA_HOME/bin
7、使用 source profile 这个命令。让Java的环境变量的配置生效。
8、检查Java是否安装成功。命令有2个。java -version  和  javac -version



## tomcat安装

【tomcat的安装步骤】
1、通过filezilla这个工具，连接上Linux服务器，然后将我们准备好的Java和tomcat的安装包传输到服务器中。
2、对tomcat进行解压，命令是  tar zxvf 文件名
3、在根目录的usr这个文件夹里面创建一个叫tomcat的文件夹。
4、将我们解压后出现的那个文件夹移动到上一步创建的tomcat文件夹中。
5、对tomcat进行配置，进入到tomcat下面的那个什么apache...的文件夹里的bin目录中，使用vi命令，对setclasspath.sh这个文件进行编辑。
6、在setclasspath.sh这个文件的第二排写入以下内容：(其实就是告诉他java在哪里)
`export JAVA_HOME=/usr/java/jdk1.8.0_211`
`export JAVA_JRE=/usr/java/jdk1.8.0_211/bin`

完成后如下：

```

```

7、启动tomcat。在bin目录下运行./startup.sh这个文件。
8、在阿里云中，打开端口号。（一般这个步骤可以不做，除非你的服务器的8080端口没有打开。）
9、在浏览器中访问自己的tomcat的页面。



10.这个时候可能还是无法访问，我们需要关闭防火墙

`systemctl stop firewalld.service`

