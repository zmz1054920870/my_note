https://www.cnblogs.com/dadong616/p/5066999.html

# [NIS域配置详解](https://www.cnblogs.com/dadong616/p/5066999.html)

一、前期准备
1.1 NIS 简介
NIS，英文的全称是network information service，也叫yellow pages。在Linux中，NIS是一个基于RPC的client/server系统，需要使用 RPC 服务。
RPC即Remote Procedure Call Protocol（远程过程调用协议），RPCBIND用于取代旧版本中的portmap组件。简单说，RPCBIND就是为了将不同服务与对应的端口进行绑定，以便支持机器间的相互操作。
\---------------------------

1.2 术语
NIS域名： NIS 主服务器和所有其客户机 (包括从服务器) 会使用同一NIS 域名。和 Windows NT 域名类似，NIS 域名与 DNS 无关。
ypserv： NIS 的服务器进程，只在server端运行。如果 ypserv 死掉的话，则服务器将不再具有响应 NIS 请求的能力。
yppasswdd： 另一个只应在 NIS 主服务器上运行的进程； 这是一个服务程序，其作用是允许 NIS 客户机改变它们的 NIS 口令。如果没有运行这个服务，用户将必须登录到 NIS 主服务器上，并在那里修改口令。
ypbind： “绑定(bind)” NIS 客户机到它的 NIS 服务器上。它将从系统中获取 NIS 域名，并使用 RPC 连接到服务器上。ypbind 是 NIS 环境中客户机-服务器通讯的核心； 如果客户端的 ypbind 死掉的话，将无法访问 NIS 服务器。
\---------------------------

1.3 必须条件
a) 服务器端和客户端要安装运行支持服务rpcbind
b) c/s两端要分别安装nis软件包，并配置正确
c) 服务端要输出NFS共享目录，客户端要挂载SERVER端的共享目录
d) 客户端须修改用户帐号信息查询方式为NIS
e) 服务端本地信息更改，须重建NIS数据库
\---------------------------

1.4 需要安装的packages
yp-tools ：提供 NIS 相关的查询命令
ypbind  ：NIS Client 端
ypserv  ：NIS Server 端
rpcbind  ：NIS 需要的 RPC 服务
\---------------------------

1.5 package 详细组成
a) yp-tools: yp的工具包，主要包含如下工具：
/usr/bin/ypcat
/usr/bin/ypchfn
/usr/bin/ypchsh
/usr/bin/ypmatch
/usr/bin/yppasswd * 修改NIS USER的密码
/usr/bin/ypwhich
/usr/sbin/yppoll
/usr/sbin/ypset
/usr/sbin/yptest
/usr/share/locale/de/LC_MESSAGES/yp-tools.mo
/var/yp
/var/yp/nicknames * yb服务器端所包含的MAP信息，若将该文件移处，则yp-tools中的命令将不可用
  
b) ypserv: yp的服务器端软件包，包含了三个服务：
\* ypserv yp主服务进程；
\* yppasswd yp服务器支持客户端修改用户密码的服务；
\* ypxfrd yp主服务器与从服务器之间数据更新同步的控制服务。
该软件包的详细组成如下：
/etc/rc.d/init.d/yppasswdd * yppasswdd服务启动脚本
/etc/rc.d/init.d/ypserv * ypserve服务启动脚本
/etc/rc.d/init.d/ypxfrd * ypxfrd服务启动脚本
/etc/sysconfig/yppasswdd * yppasswdd服务默认参数配置文件
/etc/ypserv.conf * ypserv服务配置文件
/usr/include/rpcsvc/ypxfrd.x
/usr/lib/yp * ypserv一些重要的命令存放目录
/usr/lib/yp/create_printcap
/usr/lib/yp/makedbm
/usr/lib/yp/match_printcap
/usr/lib/yp/mknetid * 更新用户及密码库（将passwd转变成dbm）
/usr/lib/yp/revnetgroup
/usr/lib/yp/yphelper
/usr/lib/yp/ypinit * 初始化ypserv服务所提供的所有信息，将文本转变成dbm格式
/usr/lib/yp/ypxfr
/usr/lib/yp/ypxfr_1perday
/usr/lib/yp/ypxfr_1perhour
/usr/lib/yp/ypxfr_2perday
/usr/sbin/rpc.yppasswdd
/usr/sbin/rpc.ypxfrd
/usr/sbin/yppush
/usr/sbin/ypserv * ypserv服务主程序
/var/yp
/var/yp/securenets * ypserv 用于设置授权客户端的配置文件。
/var/yp/Makefile * ypinit –m时会用到Makefile，如果移走，则ypinit会不成功
 
c) ypbind: yp的客户端程序，主要包含如下内容：
/etc/rc.d/init.d/ypbind
/etc/yp.conf
/sbin/ypbind
/usr/share/locale/de/LC_MESSAGES/ypbind.mo
/var/yp
/var/yp/binding

================================================================
二、安装NIS
安装环境：CentOS release 6.4 x64，Kernel 2.6.32-358.el6.x86_64

2.1 server 端安装
[root@ice etc]# yum install -y rpcbind yp-tools ypbind ypserv

2.2 client 端安装
[root@ice etc]# yum install -y rpcbind yp-tools ypbind
\##client端不需要ypserv包

================================================================
三、配置NIS
重要的配置文件：
/etc/ypserv.conf：server 端最主要的 ypserv 软件所提供的配置文件，可以规范 NIS 客户端是否可登入的权限。
/etc/hosts：由于 NIS server/client 会用到网络主机名与 IP 的对应，每一部主机名与 IP 都需要记录才行。
/etc/sysconfig/network：可以在这个档案内指定 NIS 的网域 (nisdomainname)。
/var/yp/Makefile：账号数据要转成数据库文件，这就是与建立数据库有关的动作配置文件。
/etc/yp.conf ：client端的配置文件。
/etc/nsswitch.conf ：配置优先读取哪里的账号信息。如：本地，NIS，db，ldap等。
/var/yp/securenets ：（可选）安全配置文件，比ypserv.conf具有更高的访问控制的级别与效率。
/etc/exports： 设定 NFS 共享目录。
\---------------------------
假定参数如下：
NIS 的域名为 icenis
整个内部的信任网域为 192.168.80.0/24
NIS master server 的 IP 为 192.168.80.129 ，主机名为 server.dl.cn
NIS client 的 IP 为 192.168.80.135，主机名为 client.dl.cn

\---------------------------
需要配置的文件
/etc/sysconfig/network
/etc/ypserv.conf
/etc/hosts
/etc/sysconfig/yppasswdd

\---------------------------
3.1 server 端配置
a) 设置 NIS 的域名，新增如下内容
[root@server ~]# vi /etc/sysconfig/network
NISDOMAIN=icenis #设定nis的域名
YPSERV_ARGS="-p 1011" #设定nis固定在1011端口，方便设定防火墙规则

b) 设定server端的主配置文件/etc/ypserv.conf
[root@server ~]# vi /etc/ypserv.conf
dns: no
\# NIS 服务器大多使用于内部局域网络，只要有 /etc/hosts 即可，不用 DNS
files: 30
\# 默认会有 30 个数据库被读入内存当中，账号多的话，可以调大点。
xfr_check_port: yes
\# 与 master/slave 有关，将同步更新的数据库比对所使用的端口，放置于 <1024 内。
\# 底下则是设定限制客户端或 slave server 查询的权限，利用冒号隔成四部分：
\# [主机名/IP] : [NIS域名] : [可用数据库名称map] : [安全限制security]
\# [主机名/IP]  ：可以使用 network/netmask 如 192.168.80.0/255.255.255.0 
\# [NIS域名]  ：icenis
\# [可用数据库名称]：就是由 NIS 制作出来的数据库名称；
\# [安全限制]    ：包括没有限制 (none)、仅能使用 <1024 (port) 及拒绝 (deny)
\# 一般来说，你可以依照我们的网域来设定成为底下的模样：
\# Host           : Domain  : Map : Security
127.0.0.0/255.255.255.0   : * : * : none
192.168.80.0/255.255.255.0 : * : * : none
\*              : * : * : deny
\# 星号 (*) 代表任何数据都接受的意思。上面三行的意思是，1）开放 lo 内部接口、
\# 2）开放内部 LAN 网域，3）且杜绝所有其他来源的 NIS 要求的意思。
\# 还有一个简单作法，你可以先将上面三行批注，然后加入底下这一行即可：
\*             : * : * : none
\#这样会允许任何主机连接到 NIS server，可以配合防火墙规则再做过滤。

c) 设定IP地址与主机名的对应关系/etc/hosts，新增如下内容
[root@server etc]# vi /etc/hosts
192.168.80.129  server.dl.cn
192.168.80.135  client.dl.cn

d) 让yppasswdd启动在固定端口，方便防火墙管理
[root@server etc]# vi /etc/sysconfig/yppasswdd
YPPASSWDD_ARGS="--port 1012"

\---------------------------
3.1.1 启动相应服务，并设为开机启动
[root@server etc]# /etc/init.d/rpcbind start
[root@server etc]# /etc/init.d/ypserv start
[root@server etc]# /etc/init.d/yppasswdd start
[root@server etc]# chkconfig ypserv on
[root@server etc]# chkconfig yppasswdd on

\---------------------------
3.1.2 新建 NIS 账号并建立资料库
a) 新建5个账号
[root@server etc]# for i in `seq 1 5`; do echo "=====create nisuser$i====="; useradd -u 100$i nisuser$i; echo password | passwd --stdin nisuser$i; done

b) 建立资料库
[root@server etc]# /usr/lib64/yp/ypinit -m
\#ypinit命令初始化主服务器和常见NIS映射表。默认的ypinit同make命令给出的操作一样。
\#按照提示 ctrl+D，确认即可完成资料库建立。
\#如果你的用户信息有变动过，那么你就得要重新制作数据库，make -C /var/yp

\---------------------------
3.1.3 在 server 端新增账号或者删除账号或者修改账号信息后
[root@server home]# cd /var/yp
[root@server yp]# make
或者
[root@server ~]# make -C /var/yp
把信息写进资料库，让后 client 端才可以读取到最新信息
\---------------------------

3.2 client 端配置
/etc/sysconfig/network：加入 NIS 的域名
/etc/hosts：至少需要有各个 NIS 服务器的 IP 与主机名对应；
/etc/yp.conf：这个则是 ypbind 的主要配置文件，里面主要设定 NIS 服务器所在
/etc/sysconfig/authconfig：规范账号登入时的允许认证机制；
/etc/pam.d/system-auth ：因为账号通常由 PAM 模块所管理， 所以必须要在 PAM 模块内加入 NIS 的支持才行！
/etc/nsswitch.conf ：设定账号密码与相关信息的查询顺序，默认是先找 /etc/passwd 再找 NIS 数据库；
\---------------------------

a) 修改network内容，增加nisdomain
[root@ice ~]# vi /etc/sysconfig/network
NISDOMAIN=icenis

b) 添加 nis server 的ip
[root@client ~]# vi /etc/hosts
192.168.80.129  server.dl.cn

c) 设定 nis server 的域名和ip
[root@client ~]# vi /etc/yp.conf
domain  icenis  server  192.168.80.129

d) 配置账户信息的读取顺序
[root@client ~]# vi /etc/nsswitch.conf
passwd:   files nis
shadow:   files nis
group:    files nis

3.2.1 启动相应服务，并设为开机启动
[root@client ~]# /etc/init.d/rpcbind start
[root@client ~]# /etc/init.d/ypbind start
[root@client ~]# chkconfig rpcbind on
[root@client ~]# chkconfig ypbind on

3.2.2 NIS client 端的检验: yptest, ypwhich, ypcat
a) yptest用来测试 server 端和 client 端能否正常通讯
[root@client ~]# yptest 
\#如果配置成功，会返回成功的结果
\#如果返回fail，则根据提示进行排查

b) ypwhich用来查看资料库映射数据
[root@client ~]# ypwhich #返回 NIS domain
server.dl.cn
[root@client ~]# ypwhich -x #返回可用数据库（map 映射）
Use "ethers"   for map "ethers.byname"
Use "aliases"  for map "mail.aliases"
Use "services"  for map "services.byname"
Use "protocols" for map "protocols.bynumber"
Use "hosts"   for map "hosts.byname"
Use "networks"  for map "networks.byaddr"
Use "group"   for map "group.byname"
Use "passwd"   for map "passwd.byname"

c) ypcat 与 ypwhich 功能类似
[root@client ~]# ypcat -k passwd（-k不是必须的，可以试下） #读取passwd资料库的内容

d) client 端修改账号信息需要用到：
yppasswd ：与 passwd 相同功能；修改nis用户的密码，并在nis server端更新。
ypchfn ：与 chfn 相同功能；Changing finger information
ypchsh ：与 chsh 相同功能。Changing user login shell

========值得注意的一些点========================================================
如果服务有异常，可以用 yptest 排错
1） 如果ypserv没有启动，在client端执行yptest返回
Test 2: ypbind
can't yp_bind: Reason: Domain not bound

2） 如果ypbind没有启动，在client端执行yptest返回
Test 2: ypbind
Can't communicate with ypbind

3） 如果在server端删除用户，但是没有 make -C /var/yp 的话，client端仍然能够用这个用户登录。

================================================================

鸟哥教程：http://vbird.dic.ksu.edu.tw/linux_server/0430nis/0430nis-centos4.php#whatisnis_use