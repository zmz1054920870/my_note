```bash

# 安装lrzsz
yum install -y lrzsz


# 查看通过yum下载的软件
yum list ins


# 批量杀死进程(下例是批量杀死yumj)
ps aux | grep yum |grep -v grep |awk ‘{print $2}’ | xargs kill -9


# 查看所有占用的端口
netstat -tlnu


# 释放内存缓存、清理缓存、清理内存、释放内存、q
echo 1 > /proc/sys/vm/drop_caches

# 解压到指定目录
tar -zxvf apache...gz -C /usr/lcoal/tomcat   （-C 表示安装到指定目录下）

# 递归创建文件夹
mkdir -p /root/test/demo

# 判断一个文件的大小
du -sh /usr/lib64/mysql

# 🔺🔺 通过yum只下载软件到指定的位置，不安装(例子是安装tree命令)
yum -y install tree --downloadonly --downloaddir=/root

# 查询命令
which       查看可执行文件的位置 ， 是在环境变量路径中去查询/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/user/src:/root/jdk1.8.0_211/bin

----------------------------------

whereis     查看文件的位置（也是到环境变量中去查询）​
搜索命令所在路径及帮助文档所在位置

只能用于查找在linux系统中存在或安装的程序文件，不能用于查找普通文件，支持模糊查询

-b 只查找可执行文件的位置

-m 只查找帮助文件



locate      配合数据库查看文件位置



# 查看centos的版本号
cat /etc/redhat-release
CentOS Linux release 7.6.1810 (Core)

# lsof(list open files)：列出当前系统所有打开的文件，显示进程、PID、打开的文件等情况
lsof -i
COMMAND     PID   USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
chronyd     543 chrony    5u  IPv4   12237      0t0  UDP localhost:323 
chronyd     543 chrony    6u  IPv6   12238      0t0  UDP localhost:323 
dhclient    684   root    6u  IPv4   13713      0t0  UDP *:bootpc 

# 利用for循环批量创建账号，并设置密码
[root@hecs-263993-0002 alex]# for i in `seq 1 10`
> do
> useradd user$i
> echo "redhat" | passwd --stdin user$i
> done

# 批量对一列数据进行相加
du ./local |awk 'BEGIN{sum=0}{sum+=$5}END{print sum}' 

ls -l |awk 'BEGIN{sum=0}{sum+=$5}END{print sum/1024}'

```







命令格式[operation] [motion] ，操作 + 动作 

| vim 模式   | 快捷键                     | 作用                                      | 备注                                  |
| ---------- | -------------------------- | ----------------------------------------- | ------------------------------------- |
| 普通模式   | x                          | 删除当前光标下的字符                      |                                       |
| 普通模式   | dd                         | 剪切一整行，单不进入insert模式            |                                       |
| 普通模式   | d3→                        | 剪切右边3个字符                           |                                       |
| 普通模式   | p(小写)                    | 粘贴                                      | 在光标后面粘贴                        |
| 普通模式   | P(大写)                    | 粘贴                                      | 在光标前面粘贴                        |
| 普通模式   | shift+a                    | 在行的末尾添加                            | a->append                             |
| 普通模式   | y3→                        | 复杂我光标往右3个字符                     |                                       |
| 普通模式   | yi + w                     | 复制整个单词                              | 复杂 in word，复制这个单词            |
| 普通模式   | yi + "                     | 复制整个引号中的字符                      | yank 复制                             |
| 普通模式   | yy                         | 复制整行                                  |                                       |
| 命令行模式 | set nu                     | 显示行号                                  |                                       |
| 命令行模式 | set nu!                    | 删除行号                                  |                                       |
| 普通模式   | u                          | 回退上一步操作                            |                                       |
| 普通模式   | w                          | 移动关闭到下一个词，光标放在词前面        |                                       |
| 普通模式   | e                          | 移动光标到下一个词,   光标放在词后面      |                                       |
| 普通模式   | c                          | 剪切并进入insert模式                      | change                                |
| 普通模式   | ci + " 或者 ci+w           | 改变                                      | change, 改变引号内得字符，改变        |
| 普通模式   | o                          | 光标移动到下一行                          |                                       |
| 普通模式   | v                          | 进入视图模式                              | 就是相当于鼠标左键按按住选中          |
| 命令行模式 | :%!python     -m json.tool | 使用python格式化JSON字符串                |                                       |
| 普通模式   | 0 (number 0) / home        | 跳转行首                                  |                                       |
| 普通模式   | shift+$ / end              | 跳转行尾                                  |                                       |
| 普通模式   | gg                         | 跳转到文本得最前面一行的首字母            |                                       |
| 普通模式   | G                          | 跳转到文本的最后一行的首字母              |                                       |
| 普通模式   | f + 单字符                 | 光标移动到当前行的 ”字符处“，从最近开始找 | 一般我们home一样，然后开始find        |
| 普通模式   | a                          | 在光标后面insert                          |                                       |
| 普通模式   | shift + a                  | 在行的末尾insert                          | a->append                             |
| 普通模式   | i                          | 在光标前面插入                            | i ->insert                            |
| 普通模式   | number + ↓                 | 下几行                                    |                                       |
| 普通模式   | number + ↑                 | 上几行                                    |                                       |
| 普通模式   | /字符                      | 搜索字符                                  | 太会全部高亮，这个时候可以:nohlsearch |
| 普通模式   | ctrl + f                   | 向下翻整页                                |                                       |
| 普通模式   | ctrl + b                   | 向上翻整页                                |                                       |
| 普通模式   | zz                         | 让光标所在的行居屏幕中间                  |                                       |
| 普通模式   | zt                         | 让光标所杂的行居屏幕最上一行              | t == top                              |
| 普通模式   | zb                         | 让光标所杂的行居屏幕最下行                | b == bottom                           |
| 命令行模式 | /关键字                    | 全局搜索关键字                            | 按n 继续往下搜索                      |

