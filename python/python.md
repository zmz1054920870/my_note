#### 一 、 常用语法

```python
  from chardet  
  ee = b'\\u5f20'
  cc = chardet.detect(ee)
  print(cc)
  
  >>{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
```

#### 二、json

```python
  json函数的注意事项
  import json
  """
  python的字典，字符，列表都可以使用dumps方法变成字符串
  这个字符串有一个特点，真正的字符串定义是由最外城的两个单引号
  里面的变量全部变成了双引号，而且中文汉字被dumps他的本身unicode原始编码（我们可以理解成迭代dunps，已每一个字符串为单位啥子和符号'{'不参与迭代）
  按照这个格式都可以loads变回去，针对汉字还可以使用decode变回去,但是要去掉外层的两个单引号
  """
  a = {"name":"张三","age":"20"}
  b = '张三'
  c = [1,2,3,'张三']
  json.dumps(a) --> '{"name": "\\u5f20\\u4e09", "age": "20"}'  
  json.dumps(b) -->     u5f20\\u4e09"'    						json.loads('"\\u5f20\\u4e09"') ---> '张三'
  
  json.dumps(c) -->  '[1, 2, 3, "\\u5f20\\u4e09"]'
  
  
  d = json.dumps(b) -->  '"\\u5f20\\u4e09"'
  d = bytes(d,encoding='utf8')
  d.decode('unicode-escape') --> '"张三"'
  或者
  e = b'\\u5f20\\u4e09' #直接在前面加个b，并去掉一层引号
  e.decode('unicode-escape') --> '张三'
  最好的办法还是使用loads转回去
  
  说到这里我理解到在python中怎么把汉字变成他的unicode原始编码了
  ee = "张三"
  ff = ee.encode('unicode-escape')  -->b'\\u5f20\\u4e09'
  ff.decode('unicode-escape') --> ‘张三’
  
```

  #### 三、base64

* ```python
  base64
  """
  base64模块真正用的上的方法只有8个，分别是encode, decode, encodestring, decodestring, b64encode,b64decode, urlsafe_b64decode,urlsafe_b64encode。他们8个可以两两分为4组，encode,decode一组，专门用来编码和解码文件的,也可以StringIO里的数据做编解码；encodestring,decodestring一组，专门用来编码和解码字符串； b64encode和b64decode一组，用来编码和解码字符串，并且有一个替换符号字符的功能
  """
  import base64
  f = open("C://Users//msi//Desktop//img.gif","rb")
  content = f.read()
  f.close()
  
  b64 = str(base64.b64encode(content),"utf8")
  
  ```

  

#### 四、log的format

```python
logging.basicConfig(
  level=logging.DEBUG,
  format='%(asctime)s : %(levelname)s : %(message)s',
  filename = logging_file,
  filemode = 'w',
  )
```

format 配置如下类似的dao模dao版即可

%(pathname)s # 调用日版志输出函数的模块的完整路径名，可能没权有


%(filename)s # 调用日志输出函数的模块的文件名，就是你封装的log在哪里（没必要写）


%(module)s # 调用日志输出函数的模块名


%(funcName)s # 调用日志输出函数的函数名


%(lineno)d # 调用日志输出函数的语句所在的代码行

| 参数     | 说明          |
| -------- | ------------- |
| %(name)s | ;Logger的名字 |

#### 五、io.StringIO模块

```
详解
https://blog.csdn.net/zengxiantao1994/article/details/60466087
https://blog.csdn.net/weixin_30299539/article/details/99446301
```

```
http://codingdict.com/sources/py/StringIO.StringIO/20111.html
```

```
StringIO模块的实际用途
http://www.dovov.com/pythonstringio.html
```

###### 特别说明

```python
Python3中已将StringIO归入io，调用方法如下：
import io
iost = io.StringIO() ---用于字符串

ioby = io.BytesIO()	 ---用于二进制
```



#### 六、图片管道概念

```
https://blog.csdn.net/silence2015/article/details/53789748
```

#### 七、os模块删除操作

```python
import os
os.unlink(pathname)
os.remove(pathname)
当remove() 中的pahtname指定为目录时,相当于调用rmdir 删除目录,
当remove() 中的pathname指定问文件时,相当于调用unlink 删除文件链接
```

#### 八、sys模块

###### argv

原型：sys.argv == [os.path.abspath(__file__),input(),input..........]

用法：在执行这个.py文件的时候可以从外部传入参数，

**实际用途**：比如你写好了某个自动化功能脚本，其他人要执行这个脚本，那他就可以在命令行运行python文件时，传一个excel文件参数。拿到这个excel后，获取用例，执行用例等。

注意：右键运行pycharm，不会传参数，只显示当前文件这个默认的一个参数。传参数、查看参数，只能手动在通过命令行传入参数。

实际中的作用举例：

实例：

```python
#文件名：D:\\image_test\\my_test_three.py
"""
sys.argv[0]默认是文件路径
"""

import sys
a = sys.argv
print(a)

在Terminal中运行 my_test_three.py   		    --  ['D:\\image_test\\my_test_three.py']
在Terminal中运行 my_test_three.py what info		--	['D:\\image_test\\my_test_three.py','what','info']

#文件名：D:\\image_test\\my_test_three.py
import sys
a = sys.argv[2:]
print(a)
在Terminal中运行 my_test_three.py a b c d	--	['b','c','d']


```





#### 九、顺序执行类中方法（try....finally）



```python
class BaseRequestHandler:
	"""
	代码来源于socketserver
	"""
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        pass

    def handle(self):
        pass

    def finish(self):
        pass
```



#### 十、反射是怎么回事

```python
用字符串数据类型得变量命或者函数名来调用对应的属性
A.b		getattr(A, 'b'),  一般用于类里面的方法中，调用其他方法
这样就可以实现一个函数只干一件事

class Test(object):

    def __init__(self, file_path):
        self.path = file_path

    def count_file_len(self):
        f = getattr(self, 'open_file')()        #这里就是反射
        data = f.read()
        lenthg = len(data)
        print(lenthg)

    def open_file(self):
        f = open(self.path, 'r', encoding='utf8')
        return f

if __name__ == '__main__':
    temp = Test('c://Users//zmz//Desktop//新建文本文档.txt')
    temp.count_file_len()
```





#### 十一、struct

```
# 制作固定长度的报头 一个整型--->固定长度的bytes对象
import struct

obj = struct.pack('i', 1999999999)  # 生成一个bytes对象, i 是一种格式，这种格式会把数字转换成4个字节的字节码
print(obj, len(obj), type(obj))

b = struct.unpack('i', obj)
print(b)
print(b[0])
```





#### 十二、classmethod && staticmethod

```python
classmethod也可以通过staticmethod代替，在通过类调用时，这两者对于调用者来说是不可区分的。
这两者的区别在于，classmethod增加了一个对实际调用类的引用，这带来了很多方便的地方
staticmethod我们可以理解成一个固定死的方法，用于固定去干莫一件事情

1. classmethod，就相对比 staticmethod, 权级搞一点，它可以调用类属性，如果一个类中存在多个 classmethod 它还可以去调用自身内部去调用其他 classmethod,因为类方法要自动传入一个cls， 
2. 他们两个还有一个特定，那就好看啊，比如我不想加()括号了，我可以用他们 
3. 下面是一个在创建实例以前，我们可以通过类方法进行判断一波，满足条件以后，我们再实例化：
class func(object):

    def __init__(self, data):
        self.name = data['name']
        self.sex = data['sex']


    @classmethod
    def judge(cls, data):
        if 'name' in data and 'sex' in data:
            return True


data = {'name': 'Andy', 'sex': 'boy'}
data1 = {'name1': 'Andy', 'sex': 'boy'}
data2 = {'name': 'Andy', 'sex2': 'boy'}

if func.judge(data):
    a = func(data)
    print(a.name, a.sex)
if func.judge(data1):
    a = func(data1)
    print(a.name, a.sex)

if func.judge(data):
    a = func(data)
    print(a.name, a.sex)

```







#### 十三、🔺登录单例模式 ---- 经典

```python
class ApiLogin(object):
    # 单例模式，保证运行脚本时不重复登录N多遍
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(ApiLogin, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.log = Log()
        self.login_url = "/api/auth/mp_switcher"
        self.conf_name = PLATFORM + 'Config'
        
        
 但是这里有一个问题， 那就是虽然__new__每次都会返回一个同一个cls.__instance, 但是这个cls.__instance每次都要调用一次__init__, 此时__init__里面的数据将又会被重置了， 所有不要在__init__里面存放可变的参数， 那么每次实例化的时候就都会将他给清理了，如果你要存放可变的数据，用于存放前面生成的数据呢， 将他弄成类属性存放，为什么不在后的发送中创建一个self.dict 实例属性呢？这是因为你每次在在调用方法的时候还是回被重置啊
例子：
class func(object):
    __instance = None
    dict = {}
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(func, cls).__new__(cls)
        return cls.__instance
    def my_dict(self, name, sex):
        self.dict[name] = sex



A = func()
print('初始的dict：', A.dict)
print('实例A的ID：', id(A))

#通过实例修改类属性，
A.my_dict('张三', 'nan')
print(A.dict)

B = func()
print('实例B的ID', id(B))
print(B.dict)

>>>初始的dict： {}
>>>实例A的ID： 2877804698592
>>>{'张三': 'nan'}
>>>实例B的ID 2877804698592
>>>{'张三': 'nan'}
```





#### 十四、🔺错误追踪

##### **已经弃用的**

```python
      import sys
    
    	try:
            res = ws.recv()
        except ConnectionAbortedError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
```



##### **traceback高级方法**

> - ​	**该模块提供了一个标准接口，用于提取，格式化和打印Python程序的堆栈跟踪。它在打印堆栈跟踪时完全模仿了Python解释器的行为**
> - ​    **traceback.print_exc()**
> - ​    **traceback.format_exc()**
> - ​    **配合except一起使用，无敌的存在**
> - ​    **完全和解释器一样（可以在其他包中，直接追踪到报错点）**



##### traceback.print_exc() 和 traceback.format_exc()的区别

> - ​	**traceback.format_exc()将错误返回成一个字符串**
> - ​    **traceback.print_exc()直接打印出来，根python解释器格式一模一样**
> - ​    **traceback.format_exc(file=open(file='xxxx', encoding='UTF8', mode='a'))直接写入文件中，不file就stderr输出**

```python
import traceback
file=r'D://origin/学习代码/interface_auto/local_lib/common/error.ini'
def func():
    try:
        a = Generate()
        for each in a:
            if each < 20:
                print(each)
            else:
                raise StopIteration
    except:
        print(1)
        a = traceback.print_exc(file=open(file, encoding='utf8', mode='a'))
        print(a)
    print(2)
func()
```





#### 十五、🔺获取元素位置，鼠标去点击

```python
import win32gui, win32api
handle = win32gui.FindWindow('Chrome_WidgetWin_1', '百度翻译-200种语言互译、沟通全世界！ - Google Chrome')
hwndChildList = []
handle1 = win32gui.EnumChildWindows(handle, lambda hwnd, param: param.append(hwnd), hwndChildList)
rect = win32gui.GetWindowRect(hwndChildList[0])

------- 获取一个JS页面元素的坐标
var odiv=document.getElementById( 'translate-button' )
odiv.getBoundingClientRect().left;
odiv.getBoundingClientRect().top;
odiv.getBoundingClientRect().right;
odiv.getBoundingClientRect().bottom;
```





#### 十六、🔺异常处理自我扩展

```python
class WebDriverException(Exception):
    """
    Base webdriver exception.
    """

    def __init__(self, msg=None, screen=None, stacktrace=None):
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        if self.screen is not None:
            exception_msg += "Screenshot: available via screen\n"
        if self.stacktrace is not None:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg


class MoreThanOneWebElementException(WebDriverException):
    """
    使用单元素查找方法但结果有多个元素时抛出
    """
    pass
```



#### 十七、🔺字符串单双引号

```python
python解释器解释字符串规则：
1. 我们写的字符串，不管你是传入函数中还是赋值，在cpython解释器眼里，最外面一层，不管你是单引号还是双引号甚至三引号，他都会先将他转换成单引号
2. 字符串内部的单引号，他都会加上转义字符，变成普通的字符
3. 字符传最外层的单引号保留原有的字符标记功能，不进行转义（必须的啊，没有字符标记，cpython解释器哪里认识这个鬼东西啊）
4. 内部的双引号，会保持不变

问题1：我传过去的数据带上了转义字符，其他语言会不会不能识别，而报错呢？
解释1：基本不会，因为大多数语言都是C写的或者unix写的，他们的转义字符也是\(反斜杠)，所有它们也能认识

问题2：为什么我这样传过去的数据到chrome_devtools 里面就报错了呢？
解释2：那是因为，我们传字符到chrome_devtools里面之后， chrome_driver 会将字符串两端的单引号给去除掉，这样以后，就会发生语义上的错误。。
var a = document.evaluate("//pre[@name=\'sendBox\']", document.documentElement, null, XPathResult.ORDERED_NODE_SNAPSHOT, null) 
上面这段js，是能够正常执行的。。再看
假如我们穿的时候，字符是这样的 'var a = document.evaluate(\'//pre[@name=\'sendBox\']\', document.documentElement, null, XPathResult.ORDERED_NODE_SNAPSHOT, null)', 传输的过程中是这样
'var a = document.evaluate('//pre[@name='sendBox']', document.documentElement, null, XPathResult.ORDERED_NODE_SNAPSHOT, null)' 因为前面是python解释器的规则
到chrome_driver将最外层的单引号去掉以后，变成如下样式：
var a = document.evaluate('//pre[@name='sendBox']', document.documentElement, null, XPathResult.ORDERED_NODE_SNAPSHOT, null)
 这个时候就出现了语法错误 '//pre[@name='sendBox']'  --
 问题3：怎么语法错误呢？ 
 解释3： 看规则第3点 ， 我们将外层的单引号字符去掉以后，就违背了外双内单的语法规则 
                          
 问题4： 既然上面说了内部单引号会被转义，失去字符串标记功能，那为什么 'aaa'a'aaaa'  会报错呢？
 解释4： 你好好看，上面是2个字符串加一个未定义的变量。这是因为，你未定义a导致的。
                          
                          
                          
                          
                          
  总结： 我在书写的时候还是要遵循外双内单，外单内双。 在满足改条件的情况化，语法正确了之后，才是python解释来进行识别操作。上面的python解释规则和语法规范是两套标准，先满足语法规范以后，才会拿去给ptyhon解释器解释执行
                          
 拓展：外双内单， 内单外双
 解释: 就是你最外层未双的时候， 里面只能全部是单， 不管你在里面嵌套几层，都只能是单，同理最外面是单的时候，里面的只能全部是双，也不官你嵌套几层。
                          
  例子：a = 'A"BCD"E"FG"H'  或者  b = "A'BCD'E'FG'H"
      
 问题5： 那如果两个字符串一个是外双内单 和 一个 外单内双的字符串拼接，那不是报错了啊？比如上面的c = a + b
 解释5：c = a + b ， 看规则第2点，c =  'A"BCD"E"FG"H' + 'A\'BCD\'E\'FG\'H' = 'A"BCD"E"FG"HA\'BCD\'E\'FG\'H', 这段书写规范是符合python语法的，python解释器回去解释执行他，不信可以放到IDLE中执行一下。
  
 问题6： 为什么我把c打印出来，执行单不遵循内双外单和内单外双的规范呢？
 解释6： 那是因为打印的时候转义字符\不打印啊？在pycharm中 你去把print的值复制过来，还要给你龟儿报错哦。
                          
                          
 
```





#### 十八、join和split

```python
a = ['1', '2', '3', '4']
b = '|'.join(a)
print(b)
>>> '1|2|3|4'

------------------------------
------------------------------

a = '1|2|3|4'
b = a.split('|')
print(b)
>>>['1', '2', '3', '4']


```



#### 十九、标准库

```python
pandas、numpy、matplotlib，然后是pyqt、pymysql、Django、xlwings、gevent
```





#### 二十、🔺A：B 结构来存储数据，不需要重新命名

用途1

```python
a = 1
b = 2

def func():
	a:b			# 类型标准，d

"""
意义何在： 当我们在func中要存放a和b的时候， 通常情况下我们会这样作：
def func():
	temp1 = a
	temp2 = b

 这个时候a和b 的变量名就发生了改变，我和不喜欢，在多处使用的话，我们发现，最好自己都不认识这玩意到底是什么鬼东西了， 所以我们可以采用a:b的方式来进行存储， 但是他们都不属于这个func，即不是他的类属性也不是他的实例属性，仅仅是一个地址空间在里面，就跟我们在类当中应用类外面的变量一样，存在即合理
"""


```



🔺用途2： 来源于locust源码， 重点看vars(type(self)).items() 和 self.__annotations__.items() 和 setattr(self, name, value())

```python
class EventHook:

    def __init__(self):
        self._handlers = []

    def add_listener(self, handler):
        self._handlers.append(handler)
        return handler

    def remove_listener(self, handler):
        self._handlers.remove(handler)

    def fire(self, *, reverse=False, **kwargs):
        if reverse:
            handlers = reversed(self._handlers)
        else:
            handlers = self._handlers
        for handler in handlers:
            try:
                handler(**kwargs)
            except Exception:
                raise
class Events:
    
    request_success: EventHook
        
   	def __init__(self):
    for name, value in vars(type(self)).items():
        if value == EventHook:
            setattr(self, name, value())

    for name, value in self.__annotations__.items():
        if value == EventHook:
            setattr(self, name, value())

            
========================================================================
def on_hatch_complete(**kwargs):
    pass  

events = Events()  	# 当我们实例化的以后， request_success: EventHook已经编程了request_success=EventHook()
					# 所有后面才会有EventHook中的方法
events.spawning_complete.add_listener(on_hatch_complete())
```

**备注：其实这不是复制，这是类型说明**

#### 二十一、🔺 **class， type， object的关系**

https://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/	python官方

https://blog.csdn.net/wwx890208/article/details/80644400							从python官方翻译

https://blog.csdn.net/neverlate_gogogo/article/details/107519919				其他方法

```python
请必须必须必须必须必须明白，在Python里面，所有的东西都是对象的概念。
在builtins.py源码中，class type(object), type继承与object
结论：在一切皆对象的python眼里，就连def方法函数都是一个对象，他的类是function，function又是type的实例，所有python只有一个类，那就是type，一切对象皆由type得到，但是type继承与object，采用了object的模板，所有object是一切对象的父类

class A：
	pass
a = A() #实例化
先明白两个参数， __class__ 和 __bases__
实例.__class__   返回他的类， 函数也可以用，函数也是对象
类.__bases__ 	返回所继承的父类，但是方法对象没有__bases__


高级玩法：
不是所python中真正意义的类只有一个type吗，那么我们怎么通过这个metaclass 元类来生成一个对象呢？如下：
myclass = type("MyCustomClass", (), {})
`type(类名, 父类的元组（针对继承的情况，可以为空），包含属性的字典（名称和值）)`

元类的格式：class type(name, bases, dict)
参数name是一个字符串，表示类名称，并记录为__name__属性；
参数bases是一个元组，一个个记下基础类，并记录为__bases__属性，
参数dict是一个字典，包含类本体的命名空间并被赋值到标准字典。并记录为__dict__属性。

举个例子下面两个声明创建了相同类型的对象：
class X:
    a = 1
X = type('X', (object,), dict(a=1))
```



**重点来了**

```python
因此，元类就是创建类这种对象的东西。如果你喜欢的话，可以把元类称为“类工厂”（不要和工厂类搞混了:D） type就是Python的内建元类，当然了，你也可以创建自己的元类。
__metaclass__属性

你可以在写一个类的时候为其添加__metaclass__属性。

1	class Foo(object):
2		__metaclass__ = something…
3	[…]
如果你这么做了，Python就会用元类来创建类Foo。小心点，这里面有些技巧。你首先写下class Foo(object)，但是类对象Foo还没有在内存中创建。Python会在类的定义中寻找__metaclass__属性，如果找到 了，Python就会用它来创建类Foo，如果没有找到，就会用内建的type来创建这个类。把下面这段话反复读几次。当你写如下代码时 :
```





#### 二十二、🔺什么是跨域

```python
跨域，指的是浏览器不能执行其他网站的脚本。它是由浏览器的同源策略造成的，是浏览器施加的安全限制。

所谓同源是指，域名，协议，端口均相同，不明白没关系，举个栗子：

http://www.123.com/index.html 调用 http://www.123.com/server.php （非跨域）

http://www.123.com/index.html 调用 http://www.456.com/server.php （主域名不同:123/456，跨域）

http://abc.123.com/index.html 调用 http://def.123.com/server.php （子域名不同:abc/def，跨域）

http://www.123.com:8080/index.html 调用 http://www.123.com:8081/server.php （端口不同:8080/8081，跨域）

http://www.123.com/index.html 调用 https://www.123.com/server.php （协议不同:http/https，跨域）

请注意：localhost和127.0.0.1虽然都指向本机，但也属于跨域。
```



#### 二十三、🔺python3 新语法 * 的使用

**备注：这个例子是老用法**

> - ​	***args表示当传入的是非关键字参数的时候,将他打包成一个元组**

```python
def func(a, b, c, d, *args, demo=True, **kwargs):
    print(a)
    print(b)
    print(c)
    print(d)
    print(demo)
    print(args)
    print(kwargs)


func(1, 2, 3, 4, 5, 6, 7, demo=False, name=1, age=20)

1
2
3
4
False
(5, 6, 7)
{'name': 1, 'age': 20}
```



============================================================================================================================

**备注：新用法，* 表示位置参数结束，是位置参数和关键字参数的分界线，*后面必须使用关键字参数**

> - ​	*** 表示位置参数结束，后面接收的参数必须是关键字参数形式,否则报错**
> - ​    ***不接收传参,只表示后面传入的参数必须是关键字参数,对参数进行了一次判断**
> - ​    *** 通常和\**kwargs一起使用,用kwargs来接收传参**
> 	-  **🔺当* 和 \*\*kwargs一起使用的时候\*和\*\*kwargs之间必须存在一个参数（参数形式没有要求,可以是位置参数，也可以是关键字参数，但是传参的时候，必须是关键字参数形式），不然会报错**
> - ​    **`(*, reverse=True, **kwargs)、(*, reverse, **kwargs)、(*, reverse=True)、(*, reverse)`这几种形式都可以使用**

```python
def func(*, reverse=True, **kwargs): # (*, reverse=True, **kwargs)或者(*, reverse, **kwargs)* 和 **kwargs之间必须存在一个位置参数或者关键字参数
    print(kwargs)
a = func(1, b=2)
"""
会报如下错误:func()接受0个位置参数,但是回去了一个位置参数
"""
>>> func() takes 0 positional arguments but 1 was given

def func(*, reverse=True, **kwargs):
    print(kwargs)
a = func(a=1, b=2)
>>> {'a': 1, 'b': 2}
```



```python
def func(a, b, c, d, *, demo, **kwargs):
    print(a)
    print(b)
    print(c)
    print(d)
    print(demo)
    print(kwargs)

==============1============
func(1, 2, 3, 4, demo=5, name=1, age=20)



1
2
3
4
5
{'name': 1, 'age': 20}
==============2============
func(1, 2, 3, 4, 5, name=1, age=20)


Traceback (most recent call last):
  File "D:/origin/学习代码/interface_auto/all_demo/demo.py", line 23, in <module>
    func(1, 2, 3, 4, 5, name=1, age=20)
TypeError: func() takes 4 positional arguments but 5 were given
```





#### 二十四**🔺property**

```python
class C(object):
    def __init__(self):
        self._x = None
 
    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x
 
    @x.setter
    def x(self, value):
        self._x = value
 
    @x.deleter
    def x(self):
        del self._x
```



#### 二十五**生成器**

```
f = func()
next(f)
next(f)
send(100)

next(f)	---- 先执行next()，next启动生成器(f)并监听等待接收yield返回数据,f执行到yield，执行yield,yield有发送和监听功能,yield返回值给next,并监听send,第二次执行next()，next启动生产器并监听等待接收yield返回数据，继续执行后面的代码，当再次执行yield，yield返回数据给正在监听的next,并监听send

send(100)	----  执行send,发送数据给正在监听的yield，并监听yield的返回，并继续执行，再次执行到yield，执行yield，yield返回数据数据给正在监听的send后，yield继续监听

next() 是为了启动生成器
🔺next每次都会让生成器执行到yeild发完消息就结束，下一次next一样，使生成器执行到yield发完消息就结束，send（）每次都会让生成器执行的yield执行一次收发消息才。。单独使用send的时候，必须使用next激活生成器，而且yield发消息在收消息之前
🔺也可以这样理解，next每一次必须收一次消息， send()每次都要发一次消息。如果有循环，next执行完一次收，代码走到下一次收之前停止，send执行一次发以后，代码走到下一次发之前停止，这中间有一环，收在发之前，所以send也可以收
a = f.send()
```



#### 二十六、迭代器

```python
class MyList(object):

    def __init__(self):
        self.book = [1, 2, 3, 4, 5]
        self.temp = 0			#	这里

    def __iter__(self):
        return self

    def __next__(self):	
        length = len(self.book)
        count = self.temp		#	这里
        self.temp += 1			#	还有这里， 这几个地方转换思路很重要
        if self.temp == length + 1:
            self.temp = 0		#	这里：重置self.temp为下一次使用初始化
            raise StopIteration
        return self.book[count]

if __name__ == '__main__':
    aa = MyList()
    for i in aa:
        print(i)
```





#### 二十七、传参

- **`python`中`self.a`是一个地址空间的别名，这个别名所指的地址空间指向数据`1`的地址空间**

	- **其他语言的话，`self.a`是一个数据`1`地址空间的别名**

- ****

	**`self.b = self.a`表示，这两个别名所指的地址空间中存放的是同一个数据`1`地址**

	- **所以，当`self.a = 2`的时候，不会影响到`self.b`**



```python
class A(object):

    def __init__(self):
        self.a = 1
        self.b = self.a

    def count(self):
        self.a = 2
        return self.a

if __name__ == '__main__':
    a = A()
    print(a.count())
    print(a.b)
> 2
> 1
```





#### 🔺二十八、作用域

**例子1**

```python
mylist = 1


def abc(data):
    if data == 4:
        mylist = 2
    print(mylist)
    mylist + 2
    data += 1

if __name__ == '__main__':
    print(abc(4))	# 正确指定
    
============输出输出===============
2
None

========================================
if __name__ == '__main__':
    print(abc(1))	#  z
    
============输出输出===============
Traceback (most recent call last):
  File "D:/origin/学习代码/interface_auto/src/api_case_three/test_05.py", line 44, in <module>
    print(abc(1))
  File "D:/origin/学习代码/interface_auto/src/api_case_three/test_05.py", line 33, in abc
    print(mylist)
UnboundLocalError: local variable 'mylist' referenced before assignment
```



**例子2**

```python
mylist = 1	


def abc(data):
    print(mylist)	# 这里直接红色下划线
    if data == 4:
        mylist = 2
    mylist + 2
    data += 1
    
 # 不管参数怎么执行都会报错
```

为什么会这样呢？

🔺首先理解一个概念：定义的函数内部的变量名如果是第一次出现， 且在=符号前，那么就可以认为是被定义为局部变量。在这种情况下，不论全局变量中是否用到该变量名，函数中使用的都是局部变量。



解释：上面的例子2，因为在函数的内部，解释器探测到mylist被重新赋值了，所以var成为了局部变量，但是在没有被赋值之前就想使用var，便会出现这个错误。



为什么例子1，当data=4的时候不报错，但是data等于1的时候报错呢？里面不是存在if条件判断嘛？

解释：python解释器才不管你这些，python解释器是以全局的观念来检查的



**下面是一个关于闭包的例子**



```python
from functools import wraps
 
def wrapper(log):
  def external(F):
    @wraps(F)
    def internal(**kw):
      if False:			
        log = 'modified'
      print log
    return internal
  return external
 
@wrapper('first')
def abc():
  pass
 
print abc()
# 有点复杂哈，但是还是会报错：局部变量在未赋值之前被引用

def internal(**kw):
      if False:			
        log = 'modified'
      print log
    
上面的闭包结构我们看看，log 在等号前面，说明 log是局部变量，不管有不有if 判断，都s

```





**结论：最好不要再函数内部去修改全局变量，同理，闭包内部最好不要去修改外部函数的变量**







