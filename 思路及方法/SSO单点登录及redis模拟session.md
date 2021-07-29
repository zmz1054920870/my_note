#### 网址&&github

```
https://www.cnblogs.com/Java3y/p/10877465.html
```

```
https://github.com/ZhongFuCheng3y/3y
```



#### 笔记

```
HTTP协议是无状态的，Session不能依据HTTP连接来判断是否为同一个用户。于是乎：服务器向用户浏览器发送了一个名为JESSIONID的Cookie，它的值是Session的id值。其实Session依据Cookie来识别是否是同一个用户。

简单来说：Session 之所以可以识别不同的用户，依靠的就是Cookie
该Cookie是服务器验证后自动颁发给浏览器的，不用我们手工创建的。该Cookie的maxAge值默认是-1，也就是说仅当前浏览器使用，不将该Cookie存在硬盘中


```

首先要清楚http协议是不加密的，而https协议是加密的

```
目前来说国内大部分的授权协议都是Oauth2.0。这个协议简单的说通过给用户提供一个令牌（token），而不是通过用户密码来授权，这样的一个好处时，可以方便开发者开发软件，而使用者不需要将密码提供给开发者从而避免一些隐私的问题。
```



```
Cookie有大小限制，最大4k。另外浏览器通常也也限制每个站点cookie的数量和cookie的总量。

cookie产生的方式：Cookie出现的主要目的是为了解决HTTP无状态的问题，是HTTP拓展协议。
```



```
如果不设置过期时间，则表示这个cookie生命周期为浏览器会话期间，只要关闭浏览器窗口，cookie就消失了。

这种生命期为浏览会话期的cookie被称为会话cookie。会话cookie一般不保存在硬盘上而是保存在内存里。

如果设置了过期时间，浏览器就会把cookie保存到硬盘上，关闭后再次打开浏览器，这些cookie依然有效直到超过设定的过期时间。存储在硬盘上的cookie可以在不同的浏览器进程间共享，比如两个IE窗口。而对于保存在内存的cookie，不同的浏览器有不同的处理方式。
```

```

可以说Cookie是客户端对用户信息的储存，而Session则是实现保存用户状态信息的机制。
```



```
Token我理解的话就是Session ID的一种

token并不是cookie的一种，可以是cookie验证后的产物


```





#### SSO单点登录的一个设计模型

```
https://blog.csdn.net/tang430524/article/details/78970482
```

```
https://github.com/tang430524/SSO
```



![image-20210103161458911](C:\Users\zmz\AppData\Roaming\Typora\typora-user-images\image-20210103161458911.png)

**测试使用没有连接数据库 登录信息通过配置获取 tang 123 登录完成之后将token信息存在token中 采用MD5+AES加密将账号ID加密在token中 以此来判断重复登录** 



#### SSO（sigle sigin on）实例分析和模型

```
https://blog.csdn.net/weixin_34007879/article/details/86212704
```

#### Cookie domain

为了让`Http`协议在一定程度上保持上下文，`server`在响应的头部可以加入`Set-Cookie`来写入一些数据到客户端，`Set-Cookie`中的`domain`字段用来表示这个`cookie`所在的域。
栗子：
我们访问`www.cookieexm.com`，如果`server`在返回头部中加入了`Set-Cookie`,如果不指定`domain`,那么默认这个`cookie`的域就是`www.cookieexm.com`，也就是只有访问`www.cookieexm.com`时客户端才会把这个`cookie`返给服务端。
如果我们指定`domain`为`.cookieexm.com`，那么客户端在访问以下域名：`www.cookieexm.com www1.cookieexm.com a.cookieexm.com ***.cookieexm.com` 时都能够把`cookie`返回。
所以，我们得出一条结论：**客户端对cookie的domain的匹配是从结尾进行匹配的**，有了这个基础，我们就可以实现我们的`SSO`登陆了。

cookie中需要注意的

- 设置为http-only
- 涉及登录凭证（如票据或者用户名）应该加密
- cookie不能存放隐私数据

### 具体方案

假设我们需要在如下子系统 `**.a1.a2 **.b1.b2 **.c1.c2`间实现单点登录，首先我们需要一个专门用于单点登陆的认证系统(sso.s1.s2)。假设目前系统处于未登录状态，访问`www.a1.a2`为例：

![img](https://images2015.cnblogs.com/blog/268981/201511/268981-20151105163854930-330620338.png)

 

分别看一下每个步骤作用：

1. 请求`www.a1.a2`
2. `www.a1.a2`收到请求，检查是否携带登录的cookie，目前没有登陆过，那么重定向到sso认证中心
3. SSO提供登陆窗口，用户输入用户名 口令。SSO系统验证用户名和口令
4. 这一步是关键，如果登录成功，首先把SSO系统的Cookie放到客户端；同时，将用户的认证信息传递通过重定向传递给业务方，注意，这个传递明显不能通过cookie来传递（不同域嘛），一般是通过加密的querystring。
5. 业务方的验证系统收到sso认证信息，再进行认证
6. 业务方认证通过之后，把认证结果的cookie写入到`.a1.a2`，至此，`SSO`认证完成
7. 重定向到业务系统`www.a1.a2`,由前面的结论可知，此时所有以`.a1.a2`结尾的业务系统都可以使用这个认证之后的`cookie`
8. response

#### Domain or host

```
sina.com : Domain
[www.sina.com](http://www.sina.com/) : host
```



#### cookie的结构

```
Set-Cookie: dbcl2="218114384:2ydf7SJlS+o"; path=/; domain=.douban.com; expires=Tue, 02-Feb-2021 12:51:02 GMT; httponly

结合上面的Cookie Domian查看
```



