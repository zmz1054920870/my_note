http://tool.chinaz.com/dns?type=1&host=github.com&ip=

通过里面的DNS域名解析，修改host来解决

| 任务                 | 旧指令                        | 新指令                                                       |
| -------------------- | ----------------------------- | ------------------------------------------------------------ |
| 使某服务自动启动     | chkconfig --level 3 httpd on  | systemctl enable httpd.service                               |
| 使某服务不自动启动   | chkconfig --level 3 httpd off | systemctl disable httpd.service                              |
| 检查服务状态         | service httpd status          | systemctl status httpd.service （服务详细信息） systemctl is-active httpd.service （仅显示是否 Active) |
| 显示所有已启动的服务 | chkconfig --list              | systemctl list-units --type=service                          |
| 启动某服务           | service httpd start           | systemctl start httpd.service                                |
| 停止某服务           | service httpd stop            | systemctl stop httpd.service                                 |
| 重启某服务           | service httpd restart         | systemctl restart httpd.service                              |



#### 参看某个服务是不是开机自启动

```
systemctl list-unit-files
```



#### 设置某个服务为开机自启动

```
systemctl enable xxxx
```



#### 关闭某个服务的开机自启动

```
systemctl disable xxxx
```





```

TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER_ONLY="no"
BOOTPROTO=static
DEFROUTE="yes"
IPV4_FAILURE_FATAL="no"
IPV6INIT="yes"
IPV6_AUTOCONF="yes"
IPV6_DEFROUTE="yes"
IPV6_FAILURE_FATAL="no"
IPV6_ADDR_GEN_MODE="stable-privacy"
NAME="ens33"
UUID="734a123a-6d16-4c73-8a3d-2f432ecc3b17"
DEVICE="ens33"
ONBOOT="yes"
IPADDR=192.168.0.144
NETMASK=255.255.255.0
GATEWAY=192.168.0.1 
DNS1=192.168.0.1
DNS2=144.144.144.144
DNS3=8,8,8,8

```

firewall-cmd --zone=public --add-port=54312/tcp --permanent 防火墙添加白名单