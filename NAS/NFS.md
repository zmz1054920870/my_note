# [linux下NFS远程目录挂载](https://www.cnblogs.com/merely/p/10793877.html)



NFS 是Network File System的缩写，中文意思是网络文件系统。它的主要功能是通过网络（一般是局域网）让不同的主机系统之间可以共享文件或目录。NFS客户端（一般为应用服务器，例如web）可以通过挂载（mount）的方式将NFS服务器端共享的数据目录挂载到NFS客户端本地系统中（就是某一个挂载点下）。从客户端本地看，NFS服务器端共享的目录就好像是客户端自己的磁盘分区或者目录一样，而实际上却是远端的NFS服务器的目录。 



#### 一、服务端

1、检查NFS服务

```bash
rpm -qa|grep nfs
rpm -qa|grep rpcbind
```

**说明：如果上面两个命令都没有查到任何东西，说明没有安装**



2、安装nfs

```bash
yum -y install nfs-utils rpcbind
```



3、设置开机自动启动服务

```bash
chkconfig nfs on
chkconfig rpcbind on
```



4、启动服务

```
service rpcbind start  或者 systemctl start rpcbind.service
service nfs start
```



5、创建共享目录

```
mkdir /data/nfs-share
chmod -R 777 /data/nfs-share
```



6、配置exports文件

```
vi /etc/exports
加入：
/data/nfs-share 192.168.1.1(rw)
```



### NAS和SAN的区别

SAN即存储区域网络（Storage Area Network）。

SAN是一种网络，NAS产品**是一个专有文件服务器或一个只读文件访问设备。**
SAN是在服务器和存储器之间用作I/O路径的专用网络。
SAN包括面向块（iSCSI）和面向文件（NAS）的存储产品。
NAS产品能通过SAN连接到存储设备

**存储优缺点**
优点：

NAS产品是真正即插即用的产品。NAS设备一般支持多计算机平台，用户通过网络支持协议可进入相同的文档，因而NAS设备无需改造即可用于混合Unix/Windows NT局域网内。

NAS设备的物理位置同样是灵活的。它们可放置在工作组内，靠近数据中心的应用服务器，或者也可放在其他地点，通过物理链路与网络连接起来。无需应用服务器的干预，NAS设备允许用户在网络上存取数据，这样既可减小CPU的开销，也能显著改善网络的性能。

局限：

NAS没有解决与文件服务器相关的一个关键性问题，即备份过程中的带宽消耗。与将备份数据流从LAN中转移出去的存储区域网（SAN）不同，NAS仍使用网络进行备份和恢复。NAS 的一个缺点是它将存储事务由并行SCSI连接转移到了网络上。这就是说LAN除了必须处理正常的最终用户传输流外，还必须处理包括备份操作的存储磁盘请求。

由于存储数据通过普通数据网络传输，因此易受网络上其它流量的影响。当网络上有其它大数据流量时会严重影响系统性能；由于存储数据通过普通数据网络传输，因此容易产生数据泄漏等安全问题；

存储只能以文件方式访问，而不能像普通文件系统一样直接访问物理数据块，因此会在某些情况下严重影响系统效率，比如大型数据库就不能使用NAS。

为什么要用 NAS？
国内云储存不安全，辛苦收集的大片突然就成了一张和谐的图片。国外云储存又因为种种原因经常抽个风，所以还是搞 NAS，整私有云靠谱点

Windows 以及 Mac 备份。有了 NAS 后 Time Machine 就能用上了，再也不用担心误删文件了

手机备份。之前 iCloud 经常性抽风，现在直接将手机里的相册备份到 NAS 里，也省去了买 iCloud 容量的一笔钱

可以使用迅雷远程下载，将闲置的时间用来下载，免费的离线下载

作为家庭媒体数据中心，这样电视盒子，WiFi 音箱就能直接读取 NAS 里面下载的电影和歌曲，当然也可以完美使用电视串流功能

身为程序员，可以创建自己的 git 或者 svn 版本控制库

搭建邮件服务器、个人博客、web 网站等等



mount \\192.168.0.118\data\nfs-share x:



**总结一波：**

```bash

服务端
# 1、NFS系统服务端这边要安装rpcbind
yum -y install rpcbind
systemctl start rpcbind.service

# 2、NFS系统服务端这边还要安装nfs-utils,只有安装了这个才能使用showmount这些命令
yum -y install nfs-utils
service nfs start	# 反正我的阿里云使用systemctl start nfs.service 不行

# 3、配置/etc/exports 文件里面的共享配置
vi /etc/exports
加入：
/data/nfs-share 192.168.1.1(rw)

# 4、查看本地挂载点
rpcinfo -p localhost


客户端

# 1、 也要安装rpcbind 和 nfs-utils
yum -y install rpcbind nfs-utils

# 2、客户端这边只需要启动rpcbind服务就可以了
systemctl start rpcbind.service

# 3、查看远程可挂载点
showmount -e 服务器端的IP
Export list for 192.168.0.83:
/data/nfs-share *

# 4、进行挂载
mount 192.168.0.83:/data/nfs-share /demo



总结2
RPC是远程过程调用，NFS是这个框架中的一种，还有NIS和hadoop。 
```







```bash
showmount [ -ade]  host
-a：以host:dir格式列出客户端名称/IP以及所挂载的目录。但注意该选项是读取NFS服务端/var/lib/nfs/rmtab文件，
  ：而该文件很多时候并不准确，所以showmount -a的输出信息很可能并非准确无误的
-e：显示NFS服务端所有导出列表。
-d：仅列出已被客户端挂载的导出目录。
```



```bash
sudo kill -s 9 `pidof app_data` 

# 为什么ps 和 top的时候，有些程序名被中括号[]包q
1. 用户空间创建的进程在top/ps显示不需要[]
2. 内核空间创建的进程在top/ps显示会有[]
```





```
第一位是b表示是一个块设备
第一位是l表示是一个链接文件
如下：
-   普通文件
d   目录文件
b   块设备文件
c   字符设备文件
l   符号链
p   管道特殊文件
```

