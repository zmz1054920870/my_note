## 总述

在Windows平台上，从原来使用C/C++编写原生EXE程序，到使用Python编写一些常用脚本程序，成熟的模块的使用使得编程效率大大提高了。

不过，python模块虽多，也不可能满足开发者的所有需求。而且，模块为了便于使用，通常都封装过度，有些功能无法灵活使用，必须直接调用Windows API来实现。

要完成这一目标，有两种办法，一种是使用C编写Python扩展模块，或者就是编写普通的DLL通过python的ctypes来调用，但是这样就部分牺牲掉了Python的快速开发、免编译特性。

还好，有一个模块pywin32可以解决这个问题，它直接包装了几乎所有的Windows API，可以方便地从Python直接调用，该模块另一大主要功能是通过Python进行COM编程。

该项目是开源的，项目地址是：https://github.com/mhammond/pywin32

安装时可以直接使用pip执行“pip install pywin32”来安装它。

安装完毕后，在Python安装路径下的Lib\site-packages\win32可以看到所有的API支撑模块，Lib\site-packages\win32com下则是COM的支撑模块。

![img](https://img2018.cnblogs.com/blog/857073/201903/857073-20190302194725777-1883966069.jpg)

在Lib\site-packages下有一个PyWin32.CHM帮助文件，相信对Windows编程有一定基础的，看了这个帮助文件就能很快上手。

简单说，pywin32把Windows API按照功能分了一些大类，每一个大类作为一个模块。以下是所有的模块：

mmapfile odbc perfmon servicemanager timer win2kras win32api win32clipboard win32console
win32cred win32crypt win32event win32evtlog win32file win32gui win32help win32inet win32job
win32lz win32net win32pdh win32pipe win32print win32process win32profile win32ras win32security
 win32service win32trace win32transaction win32ts win32wnet winxpgui

比如文件类API就在模块win32file中，进程类API在模块win32process中。

在使用的时候，按需导入相关模块就行了，win32con则定义了所有的常量，几乎是必不可少的，一些难以分类的API则在模块win32api中（大部分是kernel32.dll导出的API）。

部分模块之间还存在一些交叉，比如CreateFile的参数中用到的GENERIC_READ常量，在win32con中有定义，在win32file中也有定义。

用户只要大概知道这个是文件API用到的常量，那么不管你写win32file.GENERIC_READ还是win32con.GENERIC_READ都是可以的。

关闭句柄用的CloseHandle函数也是在两个模块中都有定义的。

需要注意的是，微软提供的Wsa系列网络API也都在win32file模块中，因为很多操作系统都是把套接字也用为文件对象来操作的。

如果你不清楚要使用的API在哪个模块中，那就到帮助文件里搜索一下，一定会给你答案的。

![img](https://img2018.cnblogs.com/blog/857073/201903/857073-20190302193829799-1068782851.jpg)

如果你只是对pywin32中如何调用某个API不熟悉，那么查看Pywin32.CHM就足够了，如果你对API本身的参数定义和使用不熟悉，那还得继续看MSDN。

下面来写一个Helloworld作为开始吧：

```
import` `win32api``import` `win32con``win32api.MessageBox(``None``,``"Hello,pywin32!"``,``"pywin32"``,win32con.MB_OK)
```

 效果如下：

![img](https://img2018.cnblogs.com/blog/857073/201903/857073-20190302193838570-810460685.jpg)

在Lib\site-packages\win32\Demos目录下有许多例子，如果你还不清楚pywin32怎么上手，来看看这些例子就知道了。

## 安装

pip install pywin32





## 中文文档位置

你安装pywin32包以后在如下本地

C:\Users\zmz\AppData\Local\Programs\Python\Python36\Lib\site-packages\PyWin32.chm



## 概要

在使用的时候，按需导入相关模块就行了，win32con则定义了所有的常量，几乎是必不可少的，一些难以分类的API则在模块win32api中（大部分是kernel32.dll导出的API）。

部分模块之间还存在一些交叉，比如CreateFile的参数中用到的GENERIC_READ常量，在win32con中有定义，在win32file中也有定义。

用户只要大概知道这个是文件API用到的常量，那么不管你写win32file.GENERIC_READ还是win32con.GENERIC_READ都是可以的。

关闭句柄用的CloseHandle函数也是在两个模块中都有定义的。

win32com是用于进行com编程的

[COM](https://baike.baidu.com/item/COM/296727)即组件对象模型，是[Component Object Model](https://baike.baidu.com/item/Component Object Model)取前三个字母的缩写，这三个字母在当今[Windows](https://baike.baidu.com/item/Windows)世界中随处可见。随时涌现出来的大把大把的新技术都以COM为基础。各种文档中也充斥着诸如COM对象、接口、服务器之类的术语。因此，对于一个程序员来说，不仅要掌握使用COM的方法，而且还要彻底熟悉COM的所有一切。

## python和pywin32实现窗口查找、遍历和点击

https://blog.csdn.net/qq_34489091/article/details/80244118?utm_medium=distribute.pc_relevant.none-task-blog-OPENSEARCH-2.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-OPENSEARCH-2.channel_param

#### win32gui.FindWindw(ClassName, WindowName)

##### 作用

检索类名和窗口名匹配指定字符串的顶级窗口的句柄。ClassName参数指向类名，WindowName指向窗口名，如果有指定的类名和窗口名则表示成功返回一个窗口的句柄。否则返回零。

##### 参数

1、**ClassName：PyResourceId**
指向一个用来指定类名的字符串或一个可以确定类名字符串的原子。如果该参数为None时，将会寻找任何与WindowName参数匹配的窗口。
2、**WindowName：string**
指向一个用来指定窗口名（即窗口标题）的字符串。如果此参数为None，则匹配所有窗口名。

##### 返回值

如果函数执行成功，则返回值是拥有指定窗口类名或窗口名的窗口的句柄。
如果函数执行失败，则返回值为 NULL 。可以通过调用GetLastError函数获得更加详细的错误信息



#### win32模块介绍



**win32api 提供了常用的用户API**

**win32clipboard 提供了有关粘贴板的API**

**win32console 提供了有关控制台的API**

**win32gui 提供了有关windows用户界面图形操作的API**

**win32service 提供了有关服务操作的API**

**win32file 提供了有关文件操作的API**

他们在win32目录下的lib目录中可以找到



**最常用的2个宏定义文件即是:win32con和winerror**

**win32con：基本上所有宏都集成在这里(5k+)**

**winerror：系统错误码的宏定义 来源于winerror.h**





## 查找window桌面的handle

#### win32gui.GetDesktopWindow()

##### 作用

获取主屏幕的句柄，如果存在扩展屏幕的话，还是只会获取主屏幕的句柄

##### 参数

无

##### 例子

```python
import win32gui
"""
主屏幕的分辨率是1920 * 1080
获取主屏幕的handle（如果有扩展屏幕的化，还是只会获取一个屏幕的句柄）
"""
handle = win32gui.GetDesktopWindow()
Rect = win32gui,GetWindowRect(handle)
print(Rect)
>>> (0, 0, 1920, 1080)

```





























停更一年多了，最近对PY产生了兴趣，应为想解放双手，又不想用按键精灵之类的软件，于是乎就百度到了这个东东“pywin32”
打开了新世界的大门，So,就在这记录学习笔记吧。
言归正传

准备部分1
pip install pywin32

准备部分2
工欲善其事必先利其器，先装个Spy++,百度一大把，就不放链接了，具体使用方法参考这里（一段简短的介绍）不过也够用了。

代码部分

首先

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

```
import win32gui
import win32con
win = win32gui.FindWindow('Notepad','新建文本文档.txt - 记事本')
tid = win32gui.FindWindowEx(win,None,'Edit',None)
win32gui.SendMessage(tid, win32con.WM_SETTEXT, None, '你好hello word!')
win32gui.PostMessage(tid,win32con.WM_KEYDOWN,win32con.VK_RETURN,0)
print("%x" % tid)
print("%x" % win2)
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 

一句一句解释：

```
win = win32gui.FindWindow('Notepad','新建文本文档.txt - 记事本')
```

 

这里搬运一下大佬博客的解释，

FindWindow(lpClassName=None, lpWindowName=None)
描述：自顶层窗口（也就是桌面）开始搜索条件匹配的窗体，并返回这个窗体的句柄。
不搜索子窗口、不区分大小写。找不到就返回0 参数：
lpClassName：字符型，是窗体的类名，这个可以在Spy++里找到。
lpWindowName：字符型，是窗口名，也就是标题栏上你能看见的那个标题。 说明：这个函数我们仅能用来找主窗口。


FindWindowEx(hwndParent=0, hwndChildAfter=0, lpszClass=None, lpszWindow=None)
描述：搜索类名和窗体名匹配的窗体，并返回这个窗体的句柄。不区分大小写，找不到就返回0。 参数：
hwndParent：若不为0，则搜索句柄为hwndParent窗体的子窗体。
hwndChildAfter：若不为0，则按照z-index的顺序从hwndChildAfter向后开始搜索子窗体，否则从第一个子窗体开始搜索。
lpClassName：字符型，是窗体的类名，这个可以在Spy++里找到。
lpWindowName：字符型，是窗口名，也就是标题栏上你能看见的那个标题。 说明：找到了主窗口以后就靠它来定位子窗体啦。



这里我们在桌面新建了一个记事本，

当然直接 用Spy++就可以查询到这个窗口的句柄之类的信息

第一个参数lpClassName类名就是Spy++查询得到的：

![img](https://img2018.cnblogs.com/blog/1099913/201909/1099913-20190929071018530-816094195.png)

第二个参数lpWindowName就是标题栏显示的名字 “新建文本文档.txt - 记事本”

 

然后获取到这个这个窗口的子窗口类名叫“Edit”(同样可以Spy++查到)的编辑区域

```
tid = win32gui.FindWindowEx(win,None,'Edit',None)
```

 

调用SendMessage方法往里面写入一段话

```
win32gui.SendMessage(tid, win32con.WM_SETTEXT, None, '你好hello word!')
```

 


插入一个回车符

```
win32gui.PostMessage(tid,win32con.WM_KEYDOWN,win32con.VK_RETURN,0)
```

 

顺便打印出来这个句柄的ID和在Spy++中查到的验证一下

```
print("%x" % tid)
print("%x" % win2)
```

另外，python中找回来的句柄都是十进制整型，Spy++里显示的都是十六进制整型，这个要注意下，调试的时候用十六进制 %x 输出句柄，如下：

 ![img](https://img2018.cnblogs.com/blog/1099913/201909/1099913-20190929071402804-626525174.png)

![img](https://img2018.cnblogs.com/blog/1099913/201909/1099913-20190929071418161-1403843722.png)

![img](https://img2018.cnblogs.com/blog/1099913/201909/1099913-20190929071432625-1597206874.png)





























```python
import win32gui

# 父窗口句柄, 参数1是类名，参数2是标题
fileDialog = win32gui.FindWindow('#32770','打开') 
# 子窗口句柄，是一个按钮控件，其中参数3是子窗口的类名
bu = win32gui.FindWindowEx(fileDialog,None,'Button',None) 
# 鼠标左键按下
win32gui.SendMessage(bu, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
# 鼠标左键抬起
win32gui.SendMessage(bu, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
12345678910
```

此外，也可以通过win32gui.GetWindowRect获取按钮控件的坐标，然后再根据坐标去点击。





https://blog.csdn.net/qq_23934063/article/details/79584525

https://blog.csdn.net/liulianglin/article/details/14449577



# pywin32 获取 windows 的窗体内文本框的内容

https://blog.csdn.net/baoda0398/article/details/101983270





*# 通过坐标获取窗口句柄* hw = win32gui.WindowFromPoint(win32api.GetCursorPos())

https://blog.csdn.net/qq_40999403/article/details/81176730?utm_medium=distribute.pc_relevant.none-task-blog-title-2&spm=1001.2101.3001.4242



https://blog.csdn.net/zhuisui_woxin/article/details/84256343

```python
#windows下用python3.0操作windows api向记事本里面写入字符--发送ASCII码
import win32gui,win32con
astring = b'abcdABCD' #必须采用字节串，采用字符串会出现乱码
#先手动打开一个记事本
#获取记事本中编辑控件的句柄
hWndText = win32gui.FindWindow("Notepad",None)
hWndEdit = win32gui.FindWindowEx(hWndText,None,"Edit",None)
#发送消息
for x in astring: #依次发送字节串中的每个字节
	win32gui.SendMessage(hWndEdit,win32con.WM_CHAR,x,0)
```

这个不会清空重新写，会累加



```python
#windows下用python3.0操作windows api向记事本里面写入字符--发送汉字--正确的方式 -- 按上面的会乱码
import win32gui, win32con
import binascii #导入python的进制转换模块
astring = u'Hello World! 你好！'
astrToint = [ord(c) for c in astring]  #将字符串转换为整数型列表
#先手动打开一个记事本
#获取记事本中编辑控件的句柄
hWndText = win32gui.FindWindow("Notepad",None)
hWndEdit = win32gui.FindWindowEx(hWndText,None,"Edit",None)
#发送消息
for x in astrToint: #依次发送列表中的每个数字所代表的的字符
	win32gui.SendMessage(hWndEdit,win32con.WM_CHAR,x, 0)
```



## 用剪贴板向记事本里面复制字符串

```
#windows下用python3.0操作windows api通过剪贴板向记事本里面复制字符串
import win32clipboard as wcl #导入windows操作剪贴板的库
import win32con, win32gui

#从文件读取字符串
#file = open("test.txt")
#while True:

#    astring=f.readline()

#    if len(line)==0:

#        break

astring = u'Hello World! 你好！' #待写入字符串
wcl.OpenClipboard(None) #打开剪贴板并
wcl.EmptyClipboard() #清空剪贴板
wcl.SetClipboardData(win32con.CF_UNICODETEXT,astring) #向剪贴板中写入信息
wcl.CloseClipboard() #关闭剪贴板
#先手动打开一个记事本
#获取记事本中编辑控件的句柄
hWndText = win32gui.FindWindow("Notepad",None)
hWndEdit = win32gui.FindWindowEx(hWndText,None,"Edit",None)
#发送粘贴消息
win32gui.SendMessage(hWndEdit,win32con.WM_PASTE,0,0)
#读取剪贴板内容并显示
wcl.OpenClipboard(None)
hClipMem = wcl.GetClipboardData(win32con.CF_UNICODETEXT)
wcl.CloseClipboard()
print(hClipMem)
```



```
win32gui.SendMessage(hwndChildList[0],win32con.WM_SETTEXT,0,'hah1111111111')
```

这个会清空







#### 🔺找到指定的句柄

```python
windows_handle = win32gui.GetDesktopWindow()

hwndChildList = []
handle1 = win32gui.EnumChildWindows(windows_handle, lambda hwnd, param: param.append(hwnd), hwndChildList)

for i in hwndChildList:
    #获取类名
    class_name = win32gui.GetClassName(i)
    if class_name == 'Chrome_WidgetWin_1':
        #获取窗口标题
        wind_name = win32gui.GetWindowText(i)
        pattern = ' - Google Chrome'
        if re.search(pattern, wind_name):
            handle = win32gui.FindWindowEx(i, 0, 'Chrome_RenderWidgetHostHWND', 'Chrome Legacy Window')
            if handle != 0:
                print('%x' % handle)
        continue
```















## 大牛

https://www.cnblogs.com/klb561/p/9392560.html





## 键盘记录

https://blog.csdn.net/wang8978/article/details/52900048?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param