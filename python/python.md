#### 一 、 常用语法

```python
  from chardet  
  ee = b'\\u5f20'
  cc = chardet.detect(ee)
  print(cc)
  
  >>{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}


ord() 函数是 chr() 函数（对于8位的ASCII字符串）或 unichr() 函数（对于Unicode对象）的配对函数，它以一个字符（长度为1的字符串）作为参数，返回对应的 ASCII 数值，或者 Unicode 数值，如果所给的 Unicode 字符超出了你的 Python 定义范围，则会引发一个 TypeError 的异常。

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

备注：

- sys.argv返回的是一个列表
- sys.argv的0号索引位置上，是这个文件的名称，参数是从index 1开始的

```python
#encoding=utf-8

import getopt
import sys

def main(argv):
    try:
        options, args = getopt.getopt(argv, "hp:i:", ["help", "ip=", "port="])
    except getopt.GetoptError:
        sys.exit()

    for option, value in options:
        if option in ("-h", "--help"):
            print("help")
        if option in ("-i", "--ip"):
            print("ip is: {0}".format(value))
        if option in ("-p", "--port"):
            print("port is: {0}".format(value))

    print("error args: {0}".format(args))

if __name__ == '__main__':
    main(sys.argv[1:])
```

https://www.cnblogs.com/stan-si/p/6484146.html



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
    def __init__(self, name):
        self._x = name

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        self._x = None

if __name__ == '__main__':
    a = C('张三')
    print(a.x)
    a.x = 'lisi'
    print(a.x)
    del a.x
    print(a.x)
    
张三
lisi
None
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





#### 二十九、文件的读取

**问题：如果我们采用`f.readlin()`的方式一行一行读取文件，那我们什么时候知道文件读取完毕了呢？。**

**以前的错误理解：我以前一直认为，所有的空白行都是空字符。所以不知道如何来判断文件的结尾**

**正确理解：文件中的空白行其实分两种，一种含有隐式字符的空白和（换行符），第二种就是标识文件结尾的空白行，是真正的空字符，表示文件的内容的结束**

**所以：我们在写代码的时候，可以判断最后一行，如果读取了一个空字符，那么就是文件结束了**

**正确代码如下：**

```python
with open('C://Users//zmz//Desktop//demo.txt', 'rb') as f:
    while True:
        data = f.readline
        if data == b'':
            print('文件内容结束')
            break
        print(data)
            
```



**顺便补充一句：**

`f.readlines()返回的是一个由每行数据组成的列表`

```python
>>> f.readlines()
['demo.txt v1\n', 'demo.txt v2\n', 'demo.txt v3\n', '\n', '\n', 'demo.txt v4\n', '\n', '\n', '\n']
```

**随便加一个校验文件MD5的代码**

```python
with open('C://Users//zmz//Desktop//demo.txt', 'rb') as file_delect:
	for data in file_delect.readlines():
		dig.update(data)
	print(dig.hexdigest())

```





#### 三十、python的异或运算及其乘除法、位移运算

**异或：不同为1，相同为0**

举个例子很好理解：5^3=6，如何得出？首先，5的二进制为0101，3的二进制为0011，分别对每一位求异或，得出：0110，即十进制为6。



**乘除：和10进制一样的，而且还要简单一些**

python的乘除和10机制的没有区别的。



**位移运算：**

```python
5 << 1 == 10     解析：101 向左整体移动1位，低位0补充，变成 1010
5 >> 1 == 2     解析: 101 向右整体移动1位，低位丢弃，变成 10
```



#### 🔺三十一、and、or 和 &（按位与）  |（按位活） ^（按位异或）

**备注：and 和or 和 & 和 | 是不一样的，下面进行分析**

**备注：引入三个函数，ord 和 chr, bin**

- **ord(单个字符), 计算单个字符的ASCII值，返回的是一个十进制的**
- **chr(number), 传入一个整数（可以是十进制，十六进制，八进制，二进制），返回这个整数对应的字符**
- **单个字符 -- > ord  --> 十进制 ---> chr 刚好是一个循环**
- **bin(number):  将一个整数（可以是十进制，十六进制，八进制,二进制），转换成一个二进制的字符。。这里有2个概念，第一个是输入的是整型数据，出来的是一个字符串， 第二个就是，进去的是其他进制，出来变成二进制了。如果进去的就是二进制，相当于把整型变成字符型**



**下面是ord、chr、bin的演示**

```python
==============  ord()的演示，只能是单个字符，返回的是一个十进制的 ===============
>>> a = '张'
>>> ord(a)
24352

=============  chr()演示 =================================================
# 输入10进制
>>> a = 24352
>>> chr(a)
'张

# 输入16进制
>>> a = 0x5f20
>>> chr(a)
'张'

# 输入8进制
>>> a = 0o57440
>>> chr(a)
'张'

# 输入2进制
>>> a = 0b0101111100100000
>>> chr(a)
'张'

=============  bin()演示 =================================================
# 输入16进制整数
>>> a = 0x5f20
>>> bin(a)
'0b101111100100000'

# 输入10进制整数
>>> a = 24352
>>> bin(a)
'0b101111100100000'

# 输入8进制整数
>>> a = 0o57440
>>> bin(a)
'0b101111100100000'

# 输入2进制整数
>>> a = 0b101111100100000
>>> bin(a)
'0b101111100100000'


==============  int()逆运算bin()的演示 =========================================
int是将各种进制的整数字符，变成十进制整型数据
# 输入16进制字符串
>>> a = '0x5f20'
>>> int(a, 16)
24352

# 输入8进制字符串
>>> a = '0o57440'
>>> int(a, 8)
24352

# 输入2进制字符串
>>> a = '0b101111100100000'
>>> int(a, 2)
24352



============= format演示 =================================================
format格式化，将整型，转换成对应的二进制字符串
>>> format(10, '0b')
'1010'
>>> format(10, '0x')
'a'
>>> format(10, '0o')
'12'
```



**and 、or 和 & | 的不同**

```python
>>> 1 and 2
2
>>> 2 and 1
1
# and 如果都为真的话，值为and后面的只


>>> 1 or 2
1
>>> 2 or 1
2
# or 如果都为真的话，值为and前面的值
========================================================================
>>> 1 & 2
0
>>> 2 & 1
0
# & , 按位与，现在将1变成二进制 01 ， 2变成二进制 10， 然后每一位进行与操作，最后得到00， 就是十进制0了


>>> 1 | 2
3
>>> 2 | 1
3
# |, 按位或，现在将1变成二进制 01 ， 2变成二进制 10， 然后每一位进行与操作，最后得到11 就是十进制3了
```



- 🔺**任何数与自身异或，结果为0，任何2个数异或如果结果为0，那么这两个数一定相同， 任何数与0异或，得本身**
- **任何数与1与操作，如果结果为0，这个数为偶数，结果为1，这个数为奇数**
- **左移右移特性：左移一位，相当于乘以2，右移一位，相当于除以2（地板除//）**

```python
# 判断奇偶：**任何数与1异或，如果结果为0，这个数为奇数，结果为1，这个数为偶数**
def isodd(x):
	return True if (x & 1) else False
```



```python
# 二叉查找法： **左移右移特性：左移一位，相当于乘以2，右移一位，相当于除以2（地板除//）**
def binary_search(list, item):
    '''
    :param list: 有序列表
    :param item: 要查找的元素
    :return: item在list中的索引，若不在list中返回None
    '''
    low = 0
    high = len(list) - 1
    while low <= high:
        midpoint = (low + high) >> 1  # 我们以前喜欢用midpoint = (low + high) // 2,现在采用(low + high) >> 1
        if list[midpoint] == item:
            return midpoint
        elif list[midpoint] < item:
            low = midpoint + 1
        elif list[midpoint] > item:
            high = midpoint - 1
    return None

a = [1, 2, 5, 7, 8, 9, 13, 33, 55]	# 数据必须有序才行，不然GG了。。
b = binary_search(a, 13)
print(b)
print(a[6])


```



```python
# 计算一个数值的二进制数中有多少个1
# 第一种思路：采用偏移个，奇偶判断来做
def number1Bit(x):
    count = 0
    while x:
    count = count + (x&1)	
    x = x >> 1
    return count

# 高级思路

def number1Bit(x):
    count = 0
    while x:
        count = count + 1
        x = x & (x-1)
        return count
    
# 看不懂是吧：分析一下
x 1110 0000
x - 1 1101 1111
x&(x-1) 1100 0000
```





#### 三十二、bytes字节流和hex字符串之间转换

**前言：我们很多时候看到的数据，都是一些字节流，就是前面加了一个b''这种，底层采用的是二进制，我们可以看到的数据，就只有字节流和字符还有数字。。所以不要把字节流和二进制啊，八进制啊，十六进制搞混淆。计算机底层采用的是二进制，显示出来给我看的只有字节流、字符串、数字这些形式。其他的比如bin生成二进制，我们手动输入的二进制、八进制，虽然我们输入了这些，但是python给你显示出来的时候，会把转换成字符串。。反正就是一句话，python显示给我的数据 要么采用字符串或者数字的形式，要么就是字节流样式**

**比如你在：IDLE里面输入0b11他给显示出来的是3，哪怕我们写到文件里面，它是以3的形式写入的**

**言归正传哈，我们来看看byest和hex字符串之间的转换**

```python
# utf8编码的
>>> a = '张明柱哈哈哈哈'
>>> b = a.encode('utf8')
>>> b
b'\xe5\xbc\xa0\xe6\x98\x8e\xe6\x9f\xb1\xe5\x93\x88\xe5\x93\x88\xe5\x93\x88\xe5\x93\x88'
>>> c = b.hex()
>>> c
'e5bca0e6988ee69fb1e59388e59388e59388e59388'
>>> d = bytes.fromhex(c)
>>> d
b'\xe5\xbc\xa0\xe6\x98\x8e\xe6\x9f\xb1\xe5\x93\x88\xe5\x93\x88\xe5\x93\x88\xe5\x93\x88'
>>> d.decode('utf8')
'张明柱哈哈哈哈'


# gbk编码的
>>> a = '张明柱哈哈哈哈'
>>> b = a.encode('gbk')
>>> b
b'\xd5\xc5\xc3\xf7\xd6\xf9\xb9\xfe\xb9\xfe\xb9\xfe\xb9\xfe'
>>> c = b.hex()
>>> c
'd5c5c3f7d6f9b9feb9feb9feb9fe'
>>> d = bytes.fromhex(c)
>>> d
b'\xd5\xc5\xc3\xf7\xd6\xf9\xb9\xfe\xb9\xfe\xb9\xfe\xb9\xfe'
>>> d.decode('gbk')
'张明柱哈哈哈哈'


# unicode-escape编码的
>>> a = '张明柱哈哈哈哈'
>>> b = a.encode('unicode-escape')
>>> b
b'\\u5f20\\u660e\\u67f1\\u54c8\\u54c8\\u54c8\\u54c8'
>>> c = b.hex()
>>> c
'5c75356632305c75363630655c75363766315c75353463385c75353463385c75353463385c7535346338'
>>> d = bytes.fromhex(c)
>>> d
b'\\u5f20\\u660e\\u67f1\\u54c8\\u54c8\\u54c8\\u54c8'
>>> d.decode('unicode-escape')
'张明柱哈哈哈哈'

```



https://blog.csdn.net/aa2397199142/article/details/50844879/

https://www.cnblogs.com/yangyangming/p/14187968.html

https://blog.csdn.net/QQ_1993445592/article/details/102578595

https://www.cnblogs.com/qq405921147/p/9176691.html

https://www.cnblogs.com/mcladyr/p/12636374.html

https://blog.csdn.net/xiongya8888/article/details/84947232

https://blog.csdn.net/weixin_43411585/article/details/116733560?spm=1001.2014.3001.5501

https://blog.csdn.net/weixin_43411585/article/details/116733560?spm=1001.2014.3001.5501



#### 三十三、DES3加解密

##### DES3加密

**备注：这是我写的**

**首先：**

- **对于DES3，iv偏移量必须是8个字节**
- **对于DES3，我们密钥必须是16，24这**

```python
# 晓多客户端这部就是通过这个加密的，然后发送给后端，后端采用同样的方式解密拿到数据。。
# 晓多的日志加密，就是使用的这个玩意
#0d2f9f1d0a844d35ddcd69bb0847534f59d593baca06073066cd2ac3e60edf93e275b5fbdaa3e0a4909ed2dd82731c2fc2841544e4aaf645daaac775b1431315 这是日志中的一段加密。我已经去试过了。就是这样玩的
from Crypto.Cipher import DES3, AES, DES
from Crypto.Util.Padding import pad, unpad


class Des3Cipher(object):

    def __init__(self, key, iv):
        self.key = key.encode()
        self.iv = iv.encode()
        # self.cipher = DES3.new(self.key, mode=DES3.MODE_CBC, iv=self.iv)		# 写到这里是要报错的，因为每次一次加解密都要重新生成一个cipher对象。。这样才能初始化

    def encrypt(self, text):
        cipher = DES3.new(self.key, mode=DES3.MODE_CBC, iv=self.iv)				# 每次重新初始化
        m_date = cipher.encrypt(pad(text.encode(), DES3.block_size, 'pkcs7'))	# CBC填充，填充快DES3.block_size可以自己定义，默认DES3.block_size是8，我们可以是8的倍数，但是必须小于255。没必要填那么长，不然输出的字符超级长，看着眼睛痛
        return m_date.hex()

    def decrypt(self, text):
        cipher = DES3.new(self.key, mode=DES3.MODE_CBC, iv=self.iv)				# 每次重新初始化
        text = bytes.fromhex(text)
        j_date = unpad(cipher.decrypt(text), DES3.block_size, 'pkcs7')
        return j_date.decode()

des3 = Des3haha("828d1bc65eefc6c88ca1a5d4", "828d1bc1")
print('加密', des3.encrypt('我是你爹'))
print('解密', des3.decrypt('d7a152ae6892a2f27778e37ca7b9ee06'))
```



**备注：这是研发他们写的，他妈自己写了一个pkcs7**

```python
from Crypto.Cipher import DES3


class DESPadder(object):
    def __init__(self, cipher):
        self.cipher = cipher

    def _pad(self, x):						#  他们自己动手写了一个pkcs7填充
        len_x = len(x)
        filling = 8 - len_x % 8
        fill_char = chr(filling).encode()
        return x + fill_char * filling

    def _unpad(self, x):					#  又自己写了一个去除填充
        return x[0:-ord(chr(x[-1]))]

    def encrypt(self, x):
        return self.cipher.encrypt(self._pad(x))

    def decrypt(self, x):
        return self._unpad(self.cipher.decrypt(x))


class Des3Cipher(object):
    def __init__(self, key, iv):
        self.key = key.encode()
        self.iv = iv.encode()

    def encrypt(self, text):
        cipher = DESPadder(DES3.new(self.key, DES3.MODE_CBC, self.iv))
        return cipher.encrypt(text.encode('utf-8')).hex()

    def decrypt(self, text):
        cipher = DESPadder(DES3.new(self.key, DES3.MODE_CBC, self.iv))
        return cipher.decrypt(bytes.fromhex(text)).decode()


des3 = Des3Cipher("828d1bc65eefc6c88ca1a5d4", "828d1bc6")
```



**下面是我讲pad和unpad放到一起使用 的情况**

```python
from Crypto.Cipher import DES3


class DesHandle(object):

    def __init__(self, key, iv):
        self.key = key.encode('gbk')
        self.iv = iv.encode('gbk')

    def _pad(self, x):
        len_x = len(x)
        filling = 128 - len_x % 128
        fill_char = chr(filling).encode()
        return x + fill_char * filling

    def _unpad(self, x):
        return x[0: -ord(chr(x[-1]))]

    def encrypt(self, text):
        text = text.encode('gbk')
        cipher = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        e_text = cipher.encrypt(self._pad(text))
        return e_text.hex()

    def decrypt(self, m_text):
        m_text = bytes.fromhex(m_text)
        cipher = DES3.new(self.key, mode=DES3.MODE_CBC, iv=self.iv)
        padded_text = cipher.decrypt(m_text)
        text = self._unpad(padded_text)
        return text.decode('gbk')


des3 = DesHandle("828d1bc65eefc6c88ca1a5d4", "828d1bc6")
a = des3.encrypt('我是你爹发士大夫士大夫大师傅dsfsdfsf')
print('加密', a)
print('解密', des3.decrypt(a))
```



**同理将上面的改成AES加密**

```python
from Crypto.Cipher import AES


class DesHandle(object):

    def __init__(self, key, iv):
        self.key = key.encode('gbk')
        self.iv = iv.encode('gbk')

    def _pad(self, x):
        len_x = len(x)
        filling = 128 - len_x % 128
        fill_char = chr(filling).encode()
        return x + fill_char * filling

    def _unpad(self, x):
        return x[0: -ord(chr(x[-1]))]

    def encrypt(self, text):
        text = text.encode('gbk')
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        e_text = cipher.encrypt(self._pad(text))
        return e_text.hex()

    def decrypt(self, m_text):
        m_text = bytes.fromhex(m_text)
        cipher = AES.new(self.key, mode=AES.MODE_CBC, iv=self.iv)
        padded_text = cipher.decrypt(m_text)
        text = self._unpad(padded_text)
        return text.decode('gbk')


des3 = DesHandle("828d1bc65eefc6c88ca1a5d4", "828d1bc612345678")
a = des3.encrypt('我是你爹发士大夫士大夫大师傅dsfsdfsf')
print('加密', a)
print('解密', des3.decrypt(a))

```





**拓展：**

```python
# 一个字符我们进行编码处理以后（gbk或者utf8 就这两种，unicode-escape编码有点问题），返回的字节流，其实就是内存中二进制存储以16进制显示给我们。每一个十六进制，代表一个字节，也就是说这个每一个十六进制都不会大于256，像汉字这种的字符，一般占用2-3个字节进行存储，所以，单独一个字符进行encode的时候，返回的将会是2-3十六进制的字节流

>>> '龥'.encode('utf8')
b'\xe9\xbe\xa5'			# 说明龥字，占3个字节

>>> for i in b'\xe9\xbe\xa5':
	i

	
233
190
165
```







某些加密算法要求明文需要按一定长度对齐，叫做块大小(BlockSize)，比如16字节，那么对于一段任意的数据，加密前需要对最后一个块填充到16 字节，解密后需要删除掉填充的数据。

ZeroPadding，数据长度不对齐时使用0填充，否则不填充。
PKCS7Padding，假设数据长度需要填充n(n>0)个字节才对齐，那么填充n个字节，每个字节都是n;如果数据本身就已经对齐了，则填充一块长度为块大小的数据，每个字节都是块大小。
PKCS5Padding，PKCS7Padding的子集，块大小固定为8字节。
由于使用PKCS7Padding/PKCS5Padding填充时，最后一个字节肯定为填充数据的长度，所以在解密后可以准确删除填充的数据，而使用ZeroPadding填充时，没办法区分真实数据与填充数据，所以只适合以\0结尾的字符串加解密。
————————————————
版权声明：本文为CSDN博主「土豆吞噬者」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/xiongya8888/article/details/84947232



https://blog.csdn.net/Lockey23/article/details/79423078





  在PKCS5Padding中，明确定义Block的大小是8位
  而在PKCS7Padding定义中，对于块的大小是不确定的，可以在1-255之间

某些加密算法要求明文需要按一定长度对齐，叫做块大小(BlockSize)，比如16字节，那么对于一段任意的数据，加密前需要对最后一个块填充到16 字节，解密后需要删除掉填充的数据。

  PKCS #7 填充字符串由一个字节序列组成，每个字节填充该字节序列的长度。
  假定块长度为 8，数据长度为 9，
  数据： FF FF FF FF FF FF FF FF FF
  PKCS7 填充： FF FF FF FF FF FF FF FF FF 07 07 07 07 07 07 07

https://blog.csdn.net/aa2397199142/article/details/50844879/

https://blog.csdn.net/weixin_43411585/article/details/108526461

、实现DES的4种模式
ECB模式（电子密码本模式：Electronic codebook）：ECB是最简单的块密码加密模式，加密前根据加密块大小（如DES为64位）分成若干块，之后将每块使用相同的密钥单独加密，解密同理。ECB不需要偏移量
CBC模式（密码分组链接：Cipher-block chaining）：CBC模式对于每个待加密的密码块在加密前会先与前一个密码块的密文异或然后再用加密器加密。第一个明文块与一个叫初始化向量的数据块异或，需要偏移量
CFB模式（密文反馈：Cipher feedback）：与ECB和CBC模式只能够加密块数据不同，CFB能够将块密文（Block Cipher）转换为流密文（Stream Cipher）
OFB模式（输出反馈：Output feedback）：OFB是先用块加密器生成密钥流（Keystream），然后再将密钥流与明文流异或得到密文流，解密是先用块加密器生成密钥流，再将密钥流与密文流异或得到明文，由于异或操作的对称性所以加密和解密的流程是完全一样的
4、关于补位PKCS7和PKCS5区别
PKCS7Padding和PKCS5Padding实际只是协议不一样
根据相关资料说明：PKCS5Padding明确定义了加密块是8字节，PKCS7Padding加密快可以是1-255之间
但是封装的DES算法默认都是8字节，所以可以认为PKCS7和PKCS5一样
数据补位实际是在数据不满8字节的倍数，才补充到8字节的倍数的填充过程
————————————————
版权声明：本文为CSDN博主「Shrimay1」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_43411585/article/details/108526461



AES

https://blog.csdn.net/QQ_1993445592/article/details/102578595

https://www.cnblogs.com/mcladyr/p/12636374.html



JS反调试教程

https://blog.csdn.net/weixin_43411585/article/details/116733560?spm=1001.2014.3001.5501

```python
# p
import time
import requests
import hashlib
import requests
import random

a = 'OUTFOX_SEARCH_USER_ID=1247427404@10.169.0.102; OUTFOX_SEARCH_USER_ID_NCOO=2051153968.9088902; _ntes_nnid=c2405d4db8d31fa18b65dc94c34b0e12,1610035132046; JSESSIONID=aaaKiYA6BrV1y8SA3whXx; ___rl__test__cookies={0}'.format(str(int(time.time()*1000)))
hash_handle = hashlib.md5()
fanyi_word = '狗'
hash_handle.update('5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'.encode())
url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
header = {
    'Referer': 'https://fanyi.youdao.com/',
    'Origin': 'https://fanyi.youdao.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Cookie': a
}


ts = int(time.time()*1000)
bv = hash_handle.hexdigest()
salt = str(ts) + str(random.randint(0, 9))
hash_handle = hashlib.md5()
data = "fanyideskweb" + fanyi_word + salt + "Y2FYu%TNSbMCxc3t2u^XT"
print('11111111', data)
hash_handle.update(data.encode())
sign = hash_handle.hexdigest()

data = {
    'i': fanyi_word,
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': str(salt),
    'sign': sign,
    'lts': str(ts),
    'bv': bv,
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_REALTlME'
}
print(data)
res = requests.post(url=url, headers=header, data=data)
print('111', res.headers)
print('222', res.request.headers)
print(res.json())
print(res.status_code)

```









##### AES加密

**备注：AES加密和DES3加密其实没有多大的区别**

CBC加密需要一个十六字节或者24字节的key(密钥)和一个十六字节iv(偏移量)，DES3必须是16 或 24字节的密码（只有这2种情况），和必须8字节的偏移量：比如'828d1张'只有6位数，但是中文在utf编码下占3个字节，所以也是符合8个字节要去的

ECB加密不需要iv （DES3和AES都满足这个要求，毕竟DES3是AES的过度）



```python
"""
AES 的CBC模式
"""
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


# 如果text不足16位的倍数就用空格补足为16位
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


# 加密函数
def encrypt(text):
    key = '9999999999999999'.encode('utf-8')
    mode = AES.MODE_CBC
    iv = b'qqqqqqqqqqqqqqqq'
    text = add_to_16(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text):
    key = '9999999999999999'.encode('utf-8')
    iv = b'qqqqqqqqqqqqqqqq'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')


if __name__ == '__main__':
    e = encrypt("hello world")  # 加密
    d = decrypt(e)  # 解密
    print("加密:", e)
    print("解密:", d)
```



```python
"""
AES的ECB模式
ECB没有偏移量
"""
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


# 加密函数
def encrypt(text):
    key = '9999999999999999'.encode('utf-8')
    mode = AES.MODE_ECB
    text = add_to_16(text)
    cryptos = AES.new(key, mode)

    cipher_text = cryptos.encrypt(text)
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text):
    key = '9999999999999999'.encode('utf-8')
    mode = AES.MODE_ECB
    cryptor = AES.new(key, mode)
    plain_text = cryptor.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')


if __name__ == '__main__':
    e = encrypt("hello world")  # 加密
    d = decrypt(e)  # 解密
    print("加密:", e)
    print("解密:", d)
```



#### 三十四、字符串转成字典形式（用于cookie转换）

```python
例如:cookies = "thw=ss; t=qq; cna=123"
通过:
dic = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")} ,
输出: dic = {"thw":"ss","t":"qq","cna":"123"}
```





#### 三十五、字典，数字当key

字典要数字当key，只能采用 dict[1] = 2 这种方式

```python
data = {}
data[0] = 1
print(data)

{0: 1}


num = int(input())
data_num = {}
for i in range(num):
    data = []
    a, b = input().split()
    data.append(int(a))
    data.append(int(b))
    if data[0] in data_num.keys():
        data_num[data[0]] += data[1]
    else:
        data_num[data[0]] = data[1]
        
for key in sorted(data_num.keys()):
    print(key, data_num[key])
```

 



#### 三十六、添加数据法

往往我们在根据索引操作列表的时候，会出现超出索引边界的bug，这个时候我们就可以采用添加无效数据的方式来解决，这样思路会非常清晰

```python
# 例子：输入一个字符串（包含大小写字母，和数字）,一个字母的大小写我们视为相同字符,输出相邻相同字符的个数，要求个数前面为小写字符后面跟个数
例：
输入：
aaA23bbbBbbbbb
输出：
a32131b9

input_data = input()
data_list = list(input_data)
output_data = ''
data_list.append('|')				# 这里就是了。因为我们要比较两个相邻字符。当我们遍历到最后一个字符的时候，i+1 就超出了边界了，所有我们可以引入一个无效字符进行处理。
temp_count = 1
for i in range(len(data_list)-1):
    if data_list[i].lower() == data_list[i+1].lower():
        temp_count += 1

    else:
        output_data = output_data + data_list[i].lower() + str(temp_count)
        temp_count = 1

print(output_data)



# 例子2：车库停车计算。1代表已停车，0未停车。大车占3个车位，中车占2个车位，小车占1个c
```



#### 三十七、`__str__`和`__repr__`的区别

有时候我们想让屏幕打印的结果不是对象的内存地址，而是它的值或者其他可以自定义的东西，以便更直观地显示对象内容，可以通过在该对象的类中创建或修改`__str__()`或`__repr__()`方法来实现（显示对应方法的返回值）
注意：`__str__()`方法和`__repr__()`方法的返回值只能是字符串！

**关于调用两种方法的时机**

- 使用print()时
- 使用**%s**和**f'{}'**拼接对象时
- 使用**str(x)**转换对象x时

在上述三种场景中，会优先调用对象的`__str__()`方法；若没有，就调用`__repr__()`方法；若再没有，则显示其内存地址。

特别地，对于下面两种场景：

- 用**%r**进行字符串拼接时
- 用**repr(x)**转换对象x时

则会调用这个对象的`__repr__()`方法；若没有，则不再看其是否有`__str__()`方法，而是显示其内存地址。
Django中打印queryset时,会调用__repr__方法



**总结：如果我们只使用到一个的时候，我建议使用`__repr__`,因为它包含面更广**

**特性：**

- 只能返回一个字符串，哪怕你返回了函数，这个函数调用也是返回的字符串也不行，只能是返回字符串。像下面的例子都是错误的

```python
def demo():
    return 11111111111


class BoatFactory(object):
    def __str__(self):
        return demo()
```





### 三十八、计算一个文件有多少个非空字符串



```python
from collections import Iterable
with open(r'C:\Users\zmz\Desktop\test-tb-jenkins\log\2021-09-27.log', encoding='utf-8') as file:
    print(isinstance(f))
    generator_list = [len(word) for line in file for word in line.split()]
    # l = sum([len(word) for line in file for word in line.split()])
    # print(l)

print(generator_list, len(generator_list))
```

