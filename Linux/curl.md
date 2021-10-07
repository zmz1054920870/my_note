# 一、curl命令常用参数

在Linux中curl是一个利用URL规则在命令行下工作的文件传输工具，可以说是一款很强大的http命令行工具。它支持文件的上传和下载，是综合传输工具，但按传统，习惯称url为下载工具。

```bash
-A/--user-agent <string>         设置用户代理发送给服务器
-b/--cookie <name=string/file>   cookie字符串或文件读取位置
-c/--cookie-jar <file>           操作结束后把cookie写入到这个文件中
-C/--continue-at <offset>        断点续转
-D/--dump-header <file>          把header信息写入到该文件中
-e/--referer                     来源网址
-f/--fail                        连接失败时不显示http错误
-o/--output                      把输出写到该文件中
-O/--remote-name                 把输出写到该文件中，保留远程文件的文件名
-r/--range <range>               检索来自HTTP/1.1或FTP服务器字节范围
-s/--silent                      静音模式。不输出任何东西, 因为curl有一套自己的统计，加上-s以后就不显示了，一般加上
-T/--upload-file <file>          上传文件
-u/--user <user[:password]>      设置服务器的用户和密码
-w/--write-out [format]          请求完成以后输出其他数据。。
-x/--proxy <host[:port]>         在给定的端口上使用HTTP代理
-#/--progress-bar                进度条显示当前的传送状态
```



# 二、GET

#### 1.1 发送 GET 请求，并将结果打印出来

```
curl https://catonmat.net
```

#### 1.2 发送GET请求，在请求成功以后输出一些执行的东西

-w参数用于在一次完整且成功的操作后输出指定格式的内容到标准输出。格式化输出

- http_code：		状体码
- time_namelookup: DNS解析时间,从请求开始到DNS解析完毕所用时间

- time_connect： 连接时间,从开始到建立TCP连接完成所用时间,包括前边DNS解析时间，如果需要单纯的得到连接时间，用这个time_connect时间减去前边time_namelookup时间
- time_starttransfer: 开始传输时间。在发出请求之后，Web 服务器返回数据的第一个字节所用的时间
- time_total: 总时间，按秒计。精确到小数点后三位

上面这几个时间是从小到大，进行排序的

```bash
curl -o /dev/null -s -w " time_namelookup: %{time_namelookup}\n time_connect: %{time_connect}\n time_starttransfer: %{time_starttransfer}\n time_total:%{time_total}" https://www.baid.com
结果如下：
time_nslookup:0.150

time_connect: 0.154

time_starttransfer: 0.243

time_total: 0.243
说明: 以上显示网络连接时间为0.154秒（其中DNS解析为0.150秒），总体请求0.243秒。DNS解析出现故障的概率在正式环境中比较高，所以在诊断时候千万别漏了time_namelookup这个参数。
```

**其他参数情况这里：https://blog.csdn.net/weifangan/article/details/80741981**

#### 1.3 发送 GET 请求，并将 response 的 body 输出到文件里

```
curl -o output.txt https://catonmat.net
curl https://catonmat.net >> catonmat.html
```

**🔺如果我们使用了-w格式化参数。**

- 使用重定向输出结果，将会把请求回来的结果和格式化输出都写到文件当中
- 如果使用-o的方式，请求回来的结果写到文件当中，格式化输出，将会以标准输出的样式，输出到屏幕上，以供我们查看

> ```
> curl -o /dev/null -s -w " time_namelookup: %{time_namelookup}\n time_connect: %{time_connect}\n time_starttransfer: %{time_starttransfer}\n time_total:%{time_total}" https://www.baid.com
> ```





# 三、POST













```bash
-a/--append                        上传文件时，附加到目标文件
--anyauth                          可以使用“任何”身份验证方法
--basic                            使用HTTP基本验证
-B/--use-ascii                     使用ASCII文本传输
-d/--data <data>                   HTTP POST方式传送数据
--data-ascii <data>                以ascii的方式post数据
--data-binary <data>               以二进制的方式post数据
--negotiate                        使用HTTP身份验证
--digest                           使用数字身份验证
--disable-eprt                     禁止使用EPRT或LPRT
--disable-epsv                     禁止使用EPSV
--egd-file <file>                  为随机数据(SSL)设置EGD socket路径
--tcp-nodelay                      使用TCP_NODELAY选项
-E/--cert <cert[:passwd]>          客户端证书文件和密码 (SSL)
--cert-type <type>                 证书文件类型 (DER/PEM/ENG) (SSL)
--key <key>                        私钥文件名 (SSL)
--key-type <type>                  私钥文件类型 (DER/PEM/ENG) (SSL)
--pass  <pass>                     私钥密码 (SSL)
--engine <eng>                     加密引擎使用 (SSL). "--engine list" for list
--cacert <file>                    CA证书 (SSL)
--capath <directory>               CA目   (made using c_rehash) to verify peer against (SSL)
--ciphers <list>                   SSL密码
--compressed                       要求返回是压缩的形势 (using deflate or gzip)
--connect-timeout <seconds>        设置最大请求时间
--create-dirs                      建立本地目录的目录层次结构
--crlf                             上传是把LF转变成CRLF
--ftp-create-dirs                  如果远程目录不存在，创建远程目录
--ftp-method [multicwd/nocwd/singlecwd]    控制CWD的使用
--ftp-pasv                         使用 PASV/EPSV 代替端口
--ftp-skip-pasv-ip                 使用PASV的时候,忽略该IP地址
--ftp-ssl                          尝试用 SSL/TLS 来进行ftp数据传输
--ftp-ssl-reqd                     要求用 SSL/TLS 来进行ftp数据传输
-F/--form <name=content>           模拟http表单提交数据
-form-string <name=string>         模拟http表单提交数据
-g/--globoff                       禁用网址序列和范围使用{}和[]
-G/--get                           以get的方式来发送数据
-h/--help                          帮助
-H/--header <line>                 自定义头信息传递给服务器
--ignore-content-length            忽略的HTTP头信息的长度
-i/--include                       输出时包括protocol头信息
-I/--head                          只显示文档信息
-j/--junk-session-cookies          读取文件时忽略session cookie
--interface <interface>            使用指定网络接口/地址
--krb4 <level>                     使用指定安全级别的krb4
-k/--insecure                      允许不使用证书到SSL站点
-K/--config                        指定的配置文件读取
-l/--list-only                     列出ftp目录下的文件名称
--limit-rate <rate>                设置传输速度
--local-port<NUM>                  强制使用本地端口号
-m/--max-time <seconds>            设置最大传输时间
--max-redirs <num>                 设置最大读取的目录数
--max-filesize <bytes>             设置最大下载的文件总量
-M/--manual                        显示全手动
-n/--netrc                         从netrc文件中读取用户名和密码
--netrc-optional                   使用 .netrc 或者 URL来覆盖-n
--ntlm                             使用 HTTP NTLM 身份验证
-N/--no-buffer                     禁用缓冲输出
-p/--proxytunnel                   使用HTTP代理
--proxy-anyauth                    选择任一代理身份验证方法
--proxy-basic                      在代理上使用基本身份验证
--proxy-digest                     在代理上使用数字身份验证
--proxy-ntlm                       在代理上使用ntlm身份验证
-P/--ftp-port <address>            使用端口地址，而不是使用PASV
-Q/--quote <cmd>                   文件传输前，发送命令到服务器
--range-file                       读取（SSL）的随机文件
-R/--remote-time                   在本地生成文件时，保留远程文件时间
--retry <num>                      传输出现问题时，重试的次数
--retry-delay <seconds>            传输出现问题时，设置重试间隔时间
--retry-max-time <seconds>         传输出现问题时，设置最大重试时间
-S/--show-error                    显示错误
--socks4 <host[:port]>             用socks4代理给定主机和端口
--socks5 <host[:port]>             用socks5代理给定主机和端口
-t/--telnet-option <OPT=val>       Telnet选项设置
--trace <file>                     对指定文件进行debug
--trace-ascii <file>               Like --跟踪但没有hex输出
--trace-time                       跟踪/详细输出时，添加时间戳
--url <URL>                        Spet URL to work with
-U/--proxy-user <user[:password]>  设置代理用户名和密码
-V/--version                       显示版本信息
-X/--request <command>             指定什么命令大写的X，指定请求-X POST， -X G
-y/--speed-time                    放弃限速所要的时间。默认为30
-Y/--speed-limit                   停止传输速度的限制，速度时间'秒
-z/--time-cond                     传送时间设置
-0/--http1.0                       使用HTTP 1.0
-1/--tlsv1                         使用TLSv1（SSL）
-2/--sslv2                         使用SSLv2的（SSL）
-3/--sslv3                         使用的SSLv3（SSL）
--3p-quote                         like -Q for the source URL for 3rd party transfer
--3p-url                           使用url，进行第三方传送
--3p-user                          使用用户名和密码，进行第三方传送
-4/--ipv4                          使用IP4
-6/--ipv6                          使用IP6
```





https://blog.csdn.net/xuezhangjun0121/article/details/81102643

https://www.cnblogs.com/zhangmingda/p/11685162.html

https://blog.csdn.net/weifangan/article/details/80741981

https://www.cnblogs.com/duhuo/p/5695256.html