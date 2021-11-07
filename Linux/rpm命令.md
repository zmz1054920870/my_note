## 1、 rpm常见命令参数

其实x86不是32位的意思，是一个架构，架构是什么不讨论，32位x86是x86_32，被简称x86，32位全名应该是x86_32简称位x86，64位是x86_64

```bash
用法: rpm [选项...]

-a：查询所有套件；

-b<完成阶段><套件档>+或-t <完成阶段><套件档>+：设置包装套件的完成阶段，并指定套件档的文件名称；

-c：只列出组态配置文件，本参数需配合"-l"参数使用；

-d：只列出文本文件，本参数需配合"-l"参数使用；

-e<套件档>或--erase<套件档>：删除指定的套件；

-f<文件>+：查询拥有指定文件的套件；

-h或--hash：套件安装时列出标记；

-i：显示套件的相关信息；

-i<套件档>或--install<套件档>：安装指定的套件档；

-l：显示套件的文件列表；

-p<套件档>+：查询指定的RPM套件档；

-q：使用询问模式，当遇到任何问题时，rpm指令会先询问用户；

-R：显示套件的关联性信息；

-s：显示文件状态，本参数需配合"-l"参数使用；

-U<套件档>或--upgrade<套件档>：升级指定的套件档；

-v：显示指令执行过程；

-vv：详细显示指令执行过程，便于排错。
```



## 2、rpm安装包名字解析

httpd、zip、unzip都是软件包名，一般定义为服务名方便人们识别。所有我们下载的时候可以通过

```bash
yum -y install httpd
```

这种方式进行下载。或者输入完整的名称

```
httpd-2.4.6-17.el7.x84_64.rpm
zip-3.8.0-4.el7.noarch.rpm
unzip-3.8.0-4.el7.i686.rpm
```

2.4.6-17、3.8.0-4： 这是版本号和发行次数，横杠前为版本号，横杠后面为发行次数

el7 ：EL是Red Hat Enterprise Linux（EL），即红帽企业版的缩写，7就表示Red Hat 7.x，CentOS 7.x版本
x86_64 ：表示支持32和64位架构，i686也是指32位架构
noarch：表示都兼容32位和64位，不挑架构

两种方式安装rpm包，使用rpm命令和yum命令，如： rpm -ivh httpd-2.4.6-17.el7.x84_64.rpm 或 yum install httpd-2.4.6-17.el7.x84_64.rpm



## 3、 常用命令展示

如何安装rpm软件包

```bash
rpm -ivh your-package                	# 直接安装
rpmrpm --force -ivh your-package.rpm 	# 忽略报错，强制安装
```



如果卸载rpm软件包

我们以tree包为例子

```bash
# 第一步我们下载tree包
yum -y install tree

# 查询tree包
[root@iZ8vbjbq1n4ejerpoqat7zZ ~]# rpm -ql tree
/usr/bin/tree
/usr/share/doc/tree-1.6.0
/usr/share/doc/tree-1.6.0/LICENSE
/usr/share/doc/tree-1.6.0/README
/usr/share/man/man1/tree.1.gz


# 卸载tree
rpm -e tree

# 再次查询
[root@iZ8vbjbq1n4ejerpoqat7zZ ~]# rpm -ql tree 	# 查询tree安装了哪些文件，及其具体位置
package tree is not installed


# 查询安装包是否还在（实际上我们卸载的时候，他会将a）
rpm -qa tree	# 列出所有安装过的包名,这里我们指定查询安装过tree的包名

```





which    查看可执行文件的位置 

whereis   查看文件的位置

locate    配合数据库查看文件位置