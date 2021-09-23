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





#### 抓包得到的cookie转换成dict

```
#可以将F12里面的cookie复制到一个文件夹中
cookie = open('cookie.txt', 'r+')
cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
```



#### request请求

```
1. requests.post(url,data={},json={},headers={},cookies={},proxies={},allow_redirects=True or False)
2. headers里面把{'User-Agent': name, 'Connection': 'keep-alive'}这两个加进去
3.proxies的格式
proxies = {
  "http": "http://10.10.1.10:3128", #后面必须跟http代理
  "https": "https://10.10.1.10:1080",#后面必须跟https代理
}
http的去请求https的，这样实际还是用的自己的ip
一般请求http对上了，代理不可用的时候会返回 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败
proxyMeta = "http://%(host)s:%(port)s" % {

    "host" : proxyHost,
    "port" : proxyPort,
}
proxies = {

    "http"  : proxyMeta,
    "https"  : proxyMeta
}
这种格式很牛逼啊 值得借用

#pip install -U requests[socks]  socks5 
# proxyMeta = "socks5://%(host)s:%(port)s" % {

#     "host" : proxyHost,

#     "port" : proxyPort,

# }
proxies = {

    "http"  : proxyMeta,
    "https"  : proxyMeta
}
socket代理
```



#### header中加入cookie，格式如下：（一般不这样玩）

```
headers中加cookie。

headers = { 

'User-Agent':'Apache-HttpClient/4.5.2 (Java/1.8.0_66)',

'cookie':'_zap=191e4816-acf0-41ab-85ca-c54c2ff9ca1f; d_c0="ABCsEEAYPQ2PTofKIlzwxMJDdb8R-_6iVQA=|'

}
```



#### headers设置的时候踩的坑

```
1. Host参数，在F12的Requests Headers中看见了这一项，我就给加进去了，结果SB了，404去掉了以后就可以了
豆瓣个人中心接口：https://www.douban.com/people/218114384/ 

```





#### 请求头中的重要参数之referer和User-Agent、Content-Length

```
1. 首先，如果用于写爬虫的话，这三个参数中User-Agent、Content-Length都写上，如果有referer的话也写上
2. referer
	HTTP Referer是header的一部分，当浏览器向web服务器发送请求的时候，一般会带上Referer，告诉服务器该网		页是从哪个页面链接过来的，服务器因此可以获得一些信息用于处理。

	这个因该还算好理解，比如你从CSDN首页看到了我的这篇文章，然后进来了，你这次访问的Referer就是				https://www.csdn.net/。就是访问这个页面前你访问的页面，或者说是
	
	有些反爬机制就会识别referer，看看是否正常（一般检查是否为空）。
那么什么时候referer会为空呢？
  1.你直接从浏览器的地址栏中输入网址时(或者像Chrome的书签栏中)；
  2.你写python爬虫，没有指定referer时
由2得，我们一定要指定啊。。。

一般我们写referer时，都会写完整的（包括https://，www等），并且使用该网站的主页。

还有要注意，如果你写爬虫时，想伪装成从百度等搜索引擎搜到的，请不要写baidu.com，而要写那个访问的瞬间出现的link页面（link.baidu.com+bulabula一堆东西），否则聪明的反爬可能会识破！如果没心情去复制那一大长串链接，还不如伪装成从主页访问的呢。再说一句，那个link界面就是百度统计网页流量用的。
```





#### 网路请求的数据结构

```
POST /j/mobile/login/basic HTTP/1.1    ---（方法 url  协议）
bady
```



#### Cookie的结构

```
Set-Cookie: dbcl2="218114384:2ydf7SJlS+o"; path=/; domain=.douban.com; expires=Tue, 02-Feb-2021 12:51:02 GMT; httponly


```



#### cookie的格式

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200222132439442.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2lmdWJpbmc=,size_16,color_FFFFFF,t_70)

https://blog.csdn.net/ifubing/article/details/104442450

#### cookiejar - > dict,dict - > cookiejar

```
1. requests.utils.cookiejar_from_dict(cookie字典)  ---- dict - > cookiejar
2. requests.utils.dict_from_cookiejar(cookiejar对象,domain='')  ---- cookiejar - > dict
```

https://blog.csdn.net/nchu2020/article/details/50535379

- 想请问一下，通常请求服务器的时候会携带Cookie，服务器端进行验证其内容，那么当客户端第一次（首次）请求服务器的时候会不会携带Cookie（无内容）？2 年前回复![img](https://csdnimg.cn/release/blogv2/dist/pc/img/commentMore.png)

	![点赞](https://csdnimg.cn/release/blogv2/dist/pc/img/commentUnHeart.png)

- - [![tang422622](https://profile.csdnimg.cn/1/9/B/3_tang422622)](https://blog.csdn.net/tang422622)

		[EmailyT](https://blog.csdn.net/tang422622)回复zou song**:**好的，明白了，谢谢您2 年前回复![img](https://csdnimg.cn/release/blogv2/dist/pc/img/commentMore.png)

		![点赞](https://csdnimg.cn/release/blogv2/dist/pc/img/commentUnHeart.png)

	- [![nchu2020](https://profile.csdnimg.cn/9/D/5/3_nchu2020)](https://blog.csdn.net/nchu2020)

		[zou song![img](https://csdnimg.cn/release/blogv2/dist/components/img/bloger@2x.png)](https://blog.csdn.net/nchu2020)回复**:**首次没有，Cookie是由服务器端生成，发送给User-Agent（一般是浏览器），浏览器会将Cookie的key/value保存到某个目录下的文本文件内，下次请求同一网站时就发送该Cookie给服务器（前提是浏览器设置为启用cookie）

https://blog.csdn.net/sally18/article/details/119420414?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2.no_search_link&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2.no_search_link

#### 使用requests下载大型文件分析



```
当下载大的文件的时候，他会立即开始下载文件并存放到内存当中，倘若文件过大会导致内存不足。
当把get函数的stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载。需要注意一点：文件没有下载之前，它也需要保持连接。
```

https://blog.csdn.net/zcm545186061/article/details/107586349

### 下载方式一

通常情况下我们下流数据文件，比如视频、图片…使用的普遍是下面这段代码(我自己就是)。

- **方式一**

```python
# coding=utf-8
import requests

url = "http://127.0.0.1:5001/video"
res = requests.get(url)
with open('电影下载.mp4', 'wb') as f:
    f.write(res.content)
1234567
```

上面这种方式下载的缺点是什么呢？我们来看个例子：我们下载个1.4G的电影视频，电影大小如图：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200725222814860.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3pjbTU0NTE4NjA2MQ==,size_16,color_FFFFFF,t_70)
查看当前内存使用情况如图：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200725222856289.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3pjbTU0NTE4NjA2MQ==,size_16,color_FFFFFF,t_70)
下面我们开始下载，执行上面的代码，我们发现内存在快速的被消耗，试想，如果我们启用多线程同时下载多个大的视频文件，是不是内存很快耗尽，导致机器卡死，宕机？
![在这里插入图片描述](https://img-blog.csdnimg.cn/202007252234399.gif)

### 下载方式二

- **方式二**

```python
# coding=utf-8
import requests

url = "http://127.0.0.1:5001/video"
res = requests.get(url, stream=True)
with open('电影下载.mp4', 'wb') as f:
    for chunk in res.iter_content(1024*1024*5):
        f.write(chunk)
print('下载完成...')
123456789
```

我们启动下载，查看内存的变化，我们可以看到，磁盘在高速的读写数据，但是内存增长的变化不大，没有像之前的蹭蹭蹭往上长
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200725224807185.gif)

### 分析代码含义

> 当下载大的文件的时候，他会立即开始下载文件并存放到内存当中，倘若文件过大会导致内存不足。
> 当把get函数的stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载。需要注意一点：文件没有下载之前，它也需要保持连接。

- iter_content：一块一块的遍历要下载的内容
- iter_lines：一行一行的遍历要下载的内容
  使用上面两个函数下载大文件可以防止占用过多的内存，因为每次只下载小部分数据，数据的大小为bytes,我们可以设置块状内容的大小。

### 设置进度条加载

不同的终端中可能加载显示的方式会有点不一样，我们来看下实现方式

- **tqdm安装**
  `pip install tqdm`
- **实现代码**

```python
# coding=utf-8
import requests
from tqdm import tqdm


url = "http://127.0.0.1:5001/video"
res = requests.get(url, stream=True)
file_size = int(res.headers.get('Content-Length'))  # 获取视频的总大小
pbar = tqdm(total=file_size)  # 设置进度条的长度
with open('电影下载.mp4', 'wb') as f:
    for chunk in res.iter_content(1024*1024*2):
            f.write(chunk)
            pbar.set_description('正在下载中......')
            pbar.update(1024*1024*2)  # 更新进度条长度
    pbar.close()
123456789101112131415
```

- **pycharm进度条显示**
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200725231359340.gif)
- **Sublime Text 3中进度条显示**
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200725231649609.gif)







#### HTTPBasicAuth 的应用

一种简单的身份认证，它是通过http的authorization在请求头中携带经过base64加密的用户名和密码而实现的一种认证,其实我们可以添加到header里面

**例子:**  测谈网 - 写灵感接口

备注：这个接口是没有Authorization验证的，但是我们可以看看这个参数的传值到底到哪里去了

```python
from requests.auth import HTTPBasicAuth
url = 'http://192.168.0.118:2333/inspirer/new'
data = {'content': '11', 'ximg': ''}
res = requests.post(url=url, json=data, auth=HTTPBasicAuth('ljzmz7', 'zmz123456'))
print(res.request.headers)

>>> {'User-Agent': 'python-requests/2.23.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive', 'Content-Length': '29', 'Content-Type': 'application/json', 'Authorization': 'Basic bGp6bXo3OnptejEyMzQ1Ng=='}

"""
上面{'Authorization': 'Basic bGp6bXo3OnptejEyMzQ1Ng=='} 中bGp6bXo3OnptejEyMzQ1Ng==就是base64，其实就一串明文， 我们可以用base64解码看看
"""

import base64
raw_data = 'bGp6bXo3OnptejEyMzQ1Ng=='
bytes_data = base64.b64decode(raw_data)		#b'ljzmz7:zmz123456'
data = bytes_data.decode('utf8')
print(data)
>>> ljzmz7:zmz123456   #这TM 还不是明文啊
```

**同理还有HTTPProxyAuth , 请看源码：**

```python
class HTTPProxyAuth(HTTPBasicAuth):
    """Attaches HTTP Proxy Authentication to a given Request object."""

    def __call__(self, r):
        r.headers['Proxy-Authorization'] = _basic_auth_str(self.username, self.password)
        return r
```

**大爷的，它就是继承于HTTPBasicAuth, 只是改了请求头里面字段的名字为Proxy-Authorization**

**说到这里，那我们就可以自定义验证了（如果服务端要验证这些玩意，且不想直接添加到请求头中的时候）**

```python
from requests.auth import AuthBase

class PizzaAuth(AuthBase):
    """Attaches HTTP Pizza Authentication to the given Request object."""
    def __init__(self, username):
        # setup any auth-related data here
        self.username = username

    def __call__(self, r):
        # modify and return the request， 记住这句话
        r.headers['X-Pizza'] = self.username
        return r
    
res = requests.get('http://pizzabin.org/admin', auth=PizzaAuth('kenneth'))    
print(res.headers)
>>> {'X-Pizza': 'kenneth'}
```

**🔺我们在在抓包的时候要多看看请求头中是否有`Proxy-Authorization`和Authorization， 反正就是看请求头中是否有包含Authorization这玩意的字段，有的话我们要使用auth参数，如果出现xxxxx-Authorization这种的玩意，那么就需要我们自定义了，怎么自定义呢？ 上面有PizzAuth这个例子。。好像一般用不到这玩意，🔺还有就是有些接口的Authorization不是base64的这个最好问研发，加密规则**





#### 重定向问题



python网络请求中，遇到访问某个接口一直302重定向问题。

在用requests请求某些网络接口的时候，可能遇到该接口请求之后，不会立即返回处理结果，而是返回给你cookie相关信息，然后你要在原cookies基础上加上返回的新的cookie信息，带上这些cookies信息去访问Header上Location指定的重定向地址。

一般requests不会自动处理添加新增的cookies。（貌似大部分网络请求框架都不会这样子处理，不知道是否是自己的学识尚浅）

##### 第一种解决方法：

因此需要手动拼接重定向后的cookie到原来的cookie中，大致流程如下：

1、用requests请求接口，设置allower_redirection=False,

2、判断返回状态是否是302,（重定向），是的话，拦截获取返回信息里面的Set-Cookie

3、将第2步拿到的cookie与原来requests的cookies拼接

4、构造访问第2步中Header里面Location地址。也就是重定向的目标地址。（有可能该地址与原地址不一样，建议访问该地址，而不是直接重新访问原地址）

以下是部分代码。貌似大部分网路请求，都需要自己去处理重定向问题

```python
resp = self._req.get(url, allow_redirects=False)
if resp.status_code == 302:
    self._req.headers['Cookie'] = self._req.headers['Cookie'] + ';' + resp.headers['Set-Cookie']
    result = resp.json()
    if result['success']:
        self._params['token'] = result['data']['token']
        self._params['timestamp'] = result['data']['timestamp']
        break
```



##### 第二种解决方法：

**使用Seesion：因为Seesion可以保持回话，Cookie具有持久性**





## 一、request

#### 1.1	Content-type的各种类型

**前置条件：url = www.xxx.com**

| Content-type                      | request            | 效果                                               |
| --------------------------------- | ------------------ | -------------------------------------------------- |
| Content-Type: multipart/form-data | data来接收请求数据 | url = www.xxx.com?value1=key1&value2=key2 (等价的) |
| Content-Type: multipart/json      | json来接收请求数据 | 包含在请求体中                                     |





## 二、Cookie和header



#### 2.1	headers中设置Cookie

**步骤：将F12中的Cookie字段全部复制一份，放到headers中，格式如下：**

```python
header = {'Cookie': 'sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%221794f43a93c403-03023b879feb63-d7e1739-2073600-1794f43a93d105b%22%7D; xxxxxxxxxxxxx此处省略N多字'}
res = requests.post(url=url, json=data, headers=header)
```





#### 2.2	cookies来接收参数

**步骤：我们将F12中的Cookie字段全部复制,构造一个字典格式如下**

```python
my_cookie_dict = {'Cookie': 'sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%221794f43a93c403-03023b879feb63-d7e1739-2073600-1794f43a93d105b%22%7D; xxxxxxxxxxxxx此处省略N多字'}
```

**然后使用`cookiejar_from_dict`将字典变成cookiejar对象。然后使用cookies来接收参数**

```python
from requests.utils import cookiejar_from_dict
my_cookie_dict = {'Cookie': 'sensorsdata2015jssdkcross=%7B%22%24device_id%22%3A%221794f43a93c403-03023b879feb63-d7e1739-2073600-1794f43a93d105b%22%7D; xxxxxxxxxxxxx此处省略N多字'}
cookie_jar = cookiejar_from_dict(my_cookie_dict)
res = requests.post(url=url, json=data, cookies=m)
```



## 三、各类请求头

**概念：Http协议的请求报文和回复报文都有header和body，body就是你要获取的资源，例如一个html页面，一个jpeg图片，而header是用来做某些约定的。例如客户端与服务端商定一些传输格式，客户端先获取头部，得知一些格式信息，然后才开始读取body。服务端同理，先获取头部，得知一些格式消息**

#### 3.1	Content-Length

- **单位：bytes**



#### 3.2	问题

我们的手机App在做更新时会从服务器上下载的一些资源，一般都是一些小文件，更新的代码差不多是下面这样的：

```java
static void update() throws IOException {
    URL url = new URL("http://172.16.59.129:8000/update/test.so");
    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
    if(conn.getResponseCode() == 200) {
        int totalLength = conn.getContentLength();
	BufferedInputStream in = new BufferedInputStream(conn.getInputStream());
	byte[] buffer = new byte[512];
	int readLength = 0;
	int length = 0;
	while((length=in.read(buffer)) != -1) {
		readLength += length;
		//进度条
		System.out.println(((float)readLength) /((float)(totalLength)));
	}
    }
}
```

比如上面的代码更新一个so文件，先通过content-length获取文件的总大小，然后读Stream，每读一段，就计算出当前读的总大小，除以content-length，用来显示进度条。

结果weblogic从10升级到12后，content-length一直返回-1，这样就不能显示进度条了，但是文件流还能正常读。把weblogic重启了，一开始还能返回content-length，一会又是-1了。

#### 3.3	分析原因



Http协议的请求报文和回复报文都有header和body，body就是你要获取的资源，例如一个html页面，一个jpeg图片，而header是用来做某些约定的。例如客户端与服务端商定一些传输格式，客户端先获取头部，得知一些格式信息，然后才开始读取body。

客户端是将请求头和他的boby一起发送过去

服务器是响应头和body一起发送过去

```SQL
-- client
con.send(header, body)  -- 第一步
con.recv()				-- 第四步

-- server
con.recv()				-- 第二步
con.send(header,body)	-- 第三步
```



> 客户端： Accept-Encoding:gzip （给我压缩一下，我用的是流量，先下载下来我再慢慢解压吧）
>
> 服务端1：Content-Encoding:null(没有Content-Encoding头。 我不给压缩，CPU没空，你爱要不要）
>
> 服务端2：Content-Encoding:gzip (给你节省流量，压缩一下）





> 客户端：Connection: keep-alive (大哥，咱好不容易建了个TCP连接，下次接着用）
>
> 服务端1: Connection: keep-alive （都不容易，接着用）
>
> 服务端2: Connection: close (谁跟你接着用，我们这个TCP是一次性的，下次再找我还得重新连)

http协议没有三次握手，一般客户端向服务端请求资源时，以服务端为准。还有一些header并没有协商的过程，而是服务端直接告诉客户端按什么来。例如上述的Content-Length，是服务端告诉客户端body的大小有多大。但是！服务端并不一定能准确的提前告诉你body有多大。服务端要先写header，再写body，如果要在header里把body大小写进去，就得提前知道body大小。如果这个body是动态生成的，服务端先生成完，再开始写header，这样需要很多额外的开销，所以header里不一定有content-length。

那客户端怎么知道body的大小呢？服务器有三种方式告诉你。

1.服务器已经知道资源大小，通过content-length这个header告诉你。

```
Content-Length:1076(body的大小是1076B，你读取1076B就可以完成任务了）
Transfer-Encoding: null
```

2.服务器没法提前知道资源的大小，或者不愿意花费资源提前计算资源大小，就会把http回复报文中加一个header叫Transfer-Encoding:chunked，就是分块传输的意思。每一块都使用固定的格式，前边是块的大小，后面是数据，然后最后一块大小是0。这样客户端解析的时候就需要注意去掉一些无用的字段。

```
Content-Length:null
Transfer-Encoding:chunked (接下来的body我要一块一块的传，每一块开始是这一块的大小，等我传到大小为0的块时，就没了）
```

3.服务器不知道资源的大小，同时也不支持chunked的传输模式，那么就既没有content-length头，也没有transfer-encoding头，这种情况下必须使用短连接，以连接结束来标示数据传输结束，传输结束就能知道大小了。这时候服务器返回的header里Connection一定是close。

```
Content-Length:null

Transfer-Encoding:null

Connection:close(我不知道大小，我也用不了chunked，啥时候我关了tcp连接，就说明传输结束了）
```

4.在HTTP协议中，Content-Length用于描述HTTP消息实体的传输长度the transfer-length of the message-body。在HTTP协议中，消息实体长度和消息实体的传输长度是有区别，好比说gzip压缩下，消息实体长度是压缩前的长度，消息实体的传输长度是gzip压缩后的长度，**Content-Length若是存在而且有效的话，则必须和消息内容的传输长度彻底一致**。Content-Length===消息实体的传输长度（通过测试，若是太短则会截断，过长则会致使超时。）

#### 3.4	实验

我通过nginx在虚拟机里做实验，默认nginx是支持chunked模式的，可以关掉。

使用的代码如下，可能会调整参数。

```java
static void update() throws IOException {
    URL url = new URL("http://172.16.59.129:8000/update/test.so");
    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
    //conn.setRequestProperty("Accept-Encoding", "gzip");
    //conn.setRequestProperty("Connection", "keep-alive");
    conn.connect();
    if(conn.getResponseCode() == 200) {
        System.out.println(conn.getHeaderFields().keySet());
        System.out.println(conn.getHeaderField("transfer-encoding"));
        System.out.println(conn.getHeaderField("Content-Length"));
        System.out.println(conn.getHeaderField("Content-Encoding"));
        System.out.println(conn.getHeaderField("Connection"));
    }
}
```

##### 3.4.1	nginx在开启chunked_transfer_encoding的时候

(1) 在reqeust header里不使用gzip，也就是不加accept-encoding:gzip

| test.so文件大小 | 结果                                             |
| --------------- | ------------------------------------------------ |
| 100B            | 能正常返回content-length,没有transfer-encoding头 |
| 69M             | 能正常返回content-length,没有transfer-encoding头 |
| 3072M           | 能正常返回content-length,没有transfer-encoding头 |

可以发现nginx不管资源多大，如果客户端不接受gzip的压缩格式，就不会使用chunked模式，而且跟是否使用短连接没关系。

(2)在request header里加入gzip，accepting-encoding:gzip

| test.so文件大小 | 结果                                                         |
| --------------- | ------------------------------------------------------------ |
| 100B            | 没有content-length,transfer-encoding=chunked                 |
| 69M             | 没有content-length,transfer-encoding=chunked                 |
| 3072M           | 没有content-length,transfer-encoding=trunked    可能写错了，应该是chunked |

可以看到nginx在开启chunked_transfer_encoding，并且客户端接受gzip的时候，会使用chunked模式，nginx开启gzip后不会计算资源的大小，直接用chunked模式。

##### 3.4.2	nginx关闭chunked_transfer_encoding

(1) 在reqeust header里不使用gzip，也就是不加accept-encoding:gzip

| test.so文件大小 | 结果                                             |
| --------------- | ------------------------------------------------ |
| 100B            | 能正常返回content-length,没有transfer-encoding头 |
| 69M             | 能正常返回content-length,没有transfer-encoding头 |
| 3072M           | 能正常返回content-length,没有transfer-encoding头 |

因为能很容易的知道文件大小，所以nginx还是能返回content-length。

(2)在request header里加入gzip，accepting-encoding:gzip

| test.so文件大小 | 结果                                                         |
| --------------- | ------------------------------------------------------------ |
| 100B            | 没有content-length和transfer-encoding头，不论客户端connection为keep-alive还是close，服务端返回的connection头都是close |
| 69M             | 没有content-length和transfer-encoding头，不论客户端connection为keep-alive还是close，服务端返回的connection头都是close |
| 3072M           | 没有content-length和transfer-encoding头，不论客户端connection为keep-alive还是close，服务端返回的connection头都是close |

这就是上面说的第三种情况，不知道大小，也不支持trunked，那就必须使用短连接来标示结束。

#### 3.5	问题解决方案

咨询了中间件组的同事，以前也遇到类似的问题，因为升级了Weblogic导致客户端解析XML出错，因为使用了chunked模式，中间有一些格式化的字符，而客户端解析的代码并没有考虑chunked模式的解析，导致解析出错。

因为我们客户端必须用content-length展示进度，因此不能用chunked模式，Weblogic可以把chunked模式关闭。用下面的方法：

```
#!java weblogic.WLST 
connect('username’,'password', 't3://localhost:7001')
edit()
startEdit()
cd("Servers/AdminServer/WebServer/AdminServer")
cmo.setChunkedTransferDisabled(true)
save()
activate()
exit()
```

改了之后，确实不返回chunked了，但是也没有content-length，因为Weblogic就是不提前获取文件大小，而是强制加了connection:close，也就是前边说的第三种，通过连接结束标识数据结束。最后只能把这些资源放倒apache里了。





#### 3.6	ChunK分块消息体



![image-20210826163305472](image-20210826163305472-1629968436622.png)



## 四、get方式获取cookie

**分析：**

- **我们通过`get`能获取到资源,证明该url是被授权了**
- **针对`get`请求,服务端验证授权基本都是通过请求头进行校验**
- **所有如果我们拿到了授权的`url`,我们可以返拿他请求头里面的`cookie`等授权信**



```python
import requests

# 获取授权后的登录链接
url_one = 'https://wangwang-mini.1yangai.com/api/xuanzang/new/mp_switcher'
data = {
    'platform': 'tb',
    'full_nick': 'zmz1054920870',
    'expire_minutes', 100
}
res_one = requests.post(url=url, data=data)
url_two = res.json()['url'] # https://1df3f5e3d5a70772.wangwang4-mini.1yangai.com/api/client/new/start_mgr.php?salt=9002959&sid=zmz1054920870&tid=77508d19f0a1bd71f2e92515fdf3f57d&token=a866e80378434a46a4c391136cad4da9&redirect_uri=//1df3f5e3d5a70772.wangwang4-mini.1yangai.com


# 获取cookie
res_two = requests.get(url=url_two)	# res_two.request.header == {'Connection': 'keep-alive', 'Cookie': 'source_data=; SID=2|1:0|10:1625125907|3:SID|44:OWM0NTgwOTFiYTc4NDgzMDk5NzZiYTJiZGE0OWI2YzM=|5c798313723f998fec58197491c679ddd197e4f4c3aac15c854a3bab73f989cf'}
cookie = res_two.request.header['cookie']
```

