## django

https://www.cnblogs.com/liwenzhou/p/8258992.html

#### 理论

https://www.cnblogs.com/liwenzhou/articles/8620663.html



![](D:\笔记\python\HTTP请求响应格式.png)



|websocket请求头格式

![](D:\笔记\python\websocke请求头格式.png)

Sec-WebSocket-Key是客户端随机生成并进行base64的字符串，它的原始内容是什么服务器不需要关心，服务器需要将这个字符串，与”258EAFA5-E914-47DA-95CA-C5AB0DC85B11″这个字符串进行拼接，然后对这个拼接好的字符串进行sha-1运算，再把sha-1散列得到的20字节进行base64编码即为响应头Sec-WebSocket-Accept的值



```
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==
Sec-WebSocket-Protocol: chat, superchat
Sec-WebSocket-Version: 13
```



| websocket响应格式

![](D:\笔记\python\websocket响应格式.png)





###### 注释：

###### 	1.HTTP响应必须要有状态行

###### 	2.浏览器请求你的服务器，首次会请求两次，第一次会去请求 favicon.ico, 第二次才是去请求你的其他东西

###### 	3.请求头的URL 就是路径,比如我浏览器上输入127.0.0.1:21567/xiaohei?a=2, 路径就是/xiaohei?a=2，他就是url

###### 	URL --- Uniform resource locator (同意资源定位器)





#### 动态网站和静态网站

1. 动态网页本质上就是字符串的替换， 字符串替换发生在什么地方： 发生在服务端替换完再返回给浏览器



#### 总结一下

1. web框架的本质：

   1. socket服务端  与 浏览器的通信

2. socket 服务端功能划分

   ​    a.负责与浏览器收发消息（socket通信）   ----> 常见的第三方 wsgiref /  uWsgi/  gunicorn

   ​	b.根据用户访问不同的路径执行不同 函数

   ​	c. 从HTML 读取出内容，并且完成字符串替换    ----> jinja2

3. Python中 web框架的分类

   ​	一、按上面第二点的3个功能划分：

   ​		1. 框架自带a, b, c                                        -------->  tornadao(Tornado不光是一个web框架，还实现了WSGI容器的功能)

   ​        2. 框架自带b和c，使用第三方的a             --------> Django(自带的wsgiref不行，在真实生产环境还是要借助其他的)

   ​        3.框架自带b， 使用第三方的a和c            ---------> Flask

      二、按另外一个维度来划分:

   ​	

   ​         1.Django       ------> 大而全（你做一个网站能用到的他都有）

   ​          2.其他             ------> Flask 轻量级

   4.  第二点中 a 和 b or c需要通信，也要遵循一个协议WSGI

#### WSGI（web server gateway interface -- web服务网关接口）  去了解一下



#### 如何借助其他工具提高Django的性能

http://www.jquerycn.cn/a_39186



#### django下载（有讲究）

官网：https://www.djangoproject.com/download/

![](D:\笔记\python\django版本.png)

我们使用LTS版本







#### settings



```python
D://origin//学习代码//my_django_project//my_django_project//settins.py


1. BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 这一句定位整个项目的项目跟路径，以后无论放到哪里my_django_project都是跟目录
    

    
2. TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        
        # 所以这里可以改变我们存放HTML文件的存放路径， 而且也告诉我们，我们把HTML文件放到templates里面，render会到这里面来给你读取出来，比你的f.read()高效的多
        
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

🔺# 'DIRS': [os.path.join(BASE_DIR, 'templates')] 为什么不用 '{}\\{}'.format() 来拼接，因为每个系统的分割符号不一样，window是\\， 那么Linux上呢，代码推到linux上能跑？
```























#### django的注意点

- ```
  django服务万能启动：PYTHONENCODING=UTF-8 python manage.py runserver
  ```

#### django的模块

* ```python
  from django.views.generic import View(通用类)
  ```

* ```
  from django.urls import path,include
  ```

* ```python
  from django.http import HttpResponse,JsonResponse
  ```


#### 创建一个django对象

```python
1.	django-admin startproject + "项目名称"
2.	cd /d "项目名称"
3.	python manage.py startapp + "应用项目名称"
```



#### request对象的方法

* `request.GET -> 获取url上？形式的参数`

* `request.POST ->获取post提交的数据`

* `request.path ->请求的路径，比如127.0.0.1/test/1`

  `那个这个值就是test/1`

* `request.method ->请求的方法get or post`

* `request.COOKIES ->请求过来的cookies`

* `request.user -> 请求的用户对象，可以通过它判断用户是否登     录，并获取用户信息`

* `request.session -> 一个既可读又可写的类似于字典的对象，表示当前的会话`

* `request.META ->一个标准的Python 字典，包含所有的HTTP 首部。具体的头部信息取决于客户端和服务器(有很多信息)`

#### django常用的返回对象

```
* HttpResponse 可以直接返回一些字符串内容

* render 将数据在模版中渲染并显示

* JsonResponse 返回一个json类型 通常用于与前端进行ajax交互

	from django.http import HttpResponse
	from django.shortcuts import render
	from django.http import JsonResponse

```
