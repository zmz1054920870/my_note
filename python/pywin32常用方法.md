# 获取句柄

## ----------------------------------

#### 获取桌面句柄

#### win32gui.GetDesktopWindow

###### 作用

获取主屏幕的句柄，如果存在扩展屏幕的话，还是只会获取主屏幕的句柄

###### 参数

无

###### 例子

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

## ----------------------------------

#### 获取顶层句柄

#### win32gui.FindWindow

###### 作用

获取顶层窗口的句柄，不查找子窗口

###### 参数

className:窗口类名

windowName:窗口标题

###### 例子：获取旺旺的句柄

```
win32gui.FindWindow('StandardFrame', '阿里旺旺 - zmz1054920870')
```



## ----------------------------------

#### 获取子窗口句柄

#### win32gui.FindWindowEx()

###### 作用

获取父窗口下面的一级子窗口句柄

###### 参数

*Parent* : 子窗口的父窗口。如果为0，则假定为桌面窗口

*ChildAfter* : 子窗口之后按Z顺序搜索，可以为0以搜索全部（一般不填0或者None）

*ClassName* : 要查找的窗口类的名称或原子，可以是None

*WindowName* : string 要查找的窗口标题，可以是无

```
win32gui.FindWindowEx()
```



## ----------------------------------

#### 获取所有后代句柄

#### win32gui.EnumChildWindows

```
hwndChlidList = []
win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
```

## ----------------------------------



# 发送事件指令（SendMessage）

###### 参数

hwnd：int

message:消息常量标识符

WPARAM： 通常是一个与消息有关的常量值（如：win32con.MK_LBUTTON），也可能是窗口或控件的句柄。

lParam ：通常是一个指向内存中数据的指针，发送TEXT的时候就穿给他

#### 发送Enter指令

#### win32gui.SendMessage

```python
win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
win32gui.SendMessage(handle, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
```



## ----------------------------------



#### 发送鼠标左键指令

#### win32gui.SendMessage

```python
win32gui.SendMessage(c, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
# 鼠标左键抬起
win32gui.SendMessage(c, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
```







####   常用操作

```python
mport win32gui, win32api, win32con

# 获取鼠标当前位置的坐标

win32api.GetCursorPos()



# 将鼠标移动到坐标处

win32api.SetCursorPos((200, 200))



# 左点击

win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 200, 200, 0, 0)

win32api.mouse_event(win32con.MUOSEEVENTF_LEFTUP, 200, 200, 0, 0)



# 获取窗口句柄

win32gui.FindWindow(None, 'qq')

win32gui.FindWindow('TXGuiFoundation', None)



# 通过坐标获取窗口句柄

hw = win32gui.WindowFromPoint(win32api.GetCursorPos())



# 获取窗口classname

win32gui.GetClassName(hw)



# 获取窗口标题

win32gui.GetWindowText(hw)



# 获取窗口坐标

win32gui.GetwindowRect(hw)
```



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



####  鼠标事件

```python
mouse_event(dwFlags, dx, dy, dwData, dwExtraInfo)

Simulate a mouse event


Parameters

dwFlags=0 : DWORD

	Flags specifying various function options

dx : DWORD

	Horizontal position of mouse

dy : DWORD

	Vertical position of mouse

dwData : DWORD

	Flag specific parameter

dwExtraInfo=0 : DWORD

	Additional data associated with mouse event	与鼠标事件相关的附加数据




MOUSEEVENTF_ABSOLUTE：表明参数dX，dy含有规范化的绝对坐标。
MOUSEEVENTF_MOVE：表明发生移动。
MOUSEEVENTF_LEFTDOWN：表明接按下鼠标左键。
MOUSEEVENTF_LEFTUP：表明松开鼠标左键。
MOUSEEVENTF_RIGHTDOWN：表明按下鼠标右键。
MOUSEEVENTF_RIGHTUP：表明松开鼠标右键。
MOUSEEVENTF_MIDDLEDOWN：表明按下鼠标中键。
MOUSEEVENTF_MIDDLEUP：表明松开鼠标中键。
MOUSEEVENTF_WHEEL：在Windows NT中如果鼠标有一个轮，表明鼠标轮被移动。移动的数量由dwData给出。
long dx,long dy :指定鼠标沿x轴的绝对位置或者从上次鼠标事件产生以来移动的数量，依赖于MOUSEEVENTF_ABSOLUTE的设置

long cButtons : dwFlags为MOUSEEVENTF_WHEEL，则dwData指定鼠标轮移动的数量。如果dwFlagsS不是MOUSEEVENTF_WHEEL，则dWData应为零。

long dwExtraInfo ：指定与鼠标事件相关的附加32位值。应用程序调用函数GetMessageExtraInfo来获得此附加信息。
PB例子：

功能：点击按钮2 模拟鼠标移动点击功能 移动到按钮1并实现按钮1功能 


鼠标双击，最好在第一次点击完成以后，time.sleep(0.1)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


```





#### 键盘事件

```
win32api.keybd_event(bVk, bScan, dwFlags, dwExtraInfo)
Parameters

bVk : BYTE

	Virtual-key code	虚拟键码

bScan : BYTE

	Hardware scan code  硬件扫描码

dwFlags=0 : DWORD

	Flags specifying various function options	指定多种选项功能的标志

dwExtraInfo=0 : DWORD

	Additional data associated with keystroke	与击键相关的附加数据

第一个参数：虚拟键码（键盘键码对照表见附录）；

第二个参数：硬件扫描码，一般设置为0即可；

第三个参数：函数操作的一个标志位，如果值为KEYEVENTF_EXTENDEDKEY则该键被按下，也可设置为0,KEYEVENTF_EXTENDEDKEY对应的值就是0，如果值为KEYEVENTF_KEYUP则该按键被释放；

第四个参数：定义与击键相关的附加的32位值，一般设置为0即可。

例子：

import win32api

import win32con
win32api.keybd_event(0x13,0,0,0)     # enter
win32api.keybd_event(0x13,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
```









```python
虚拟键位码, 最好使用十六进制，可以多处兼容
VK_CODE = {
    'backspace': 0x08,
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    'alt': 0x12,
    'pause': 0x13,
    'caps_lock': 0x14,
    'esc': 0x1B,
    'spacebar': 0x20,
    'page_up': 0x21,
    'page_down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left_arrow': 0x25,
    'up_arrow': 0x26,
    'right_arrow': 0x27,
    'down_arrow': 0x28,
    'select': 0x29,
    'print': 0x2A,
    'execute': 0x2B,
    'print_screen': 0x2C,
    'ins': 0x2D,
    'del': 0x2E,
    'help': 0x2F,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    'numpad_0': 0x60,
    'numpad_1': 0x61,
    'numpad_2': 0x62,
    'numpad_3': 0x63,
    'numpad_4': 0x64,
    'numpad_5': 0x65,
    'numpad_6': 0x66,
    'numpad_7': 0x67,
    'numpad_8': 0x68,
    'numpad_9': 0x69,
    'multiply_key': 0x6A,
    'add_key': 0x6B,
    'separator_key': 0x6C,
    'subtract_key': 0x6D,
    'decimal_key': 0x6E,
    'divide_key': 0x6F,
    'F1': 0x70,
    'F2': 0x71,
    'F3': 0x72,
    'F4': 0x73,
    'F5': 0x74,
    'F6': 0x75,
    'F7': 0x76,
    'F8': 0x77,
    'F9': 0x78,
    'F10': 0x79,
    'F11': 0x7A,
    'F12': 0x7B,
    'F13': 0x7C,
    'F14': 0x7D,
    'F15': 0x7E,
    'F16': 0x7F,
    'F17': 0x80,
    'F18': 0x81,
    'F19': 0x82,
    'F20': 0x83,
    'F21': 0x84,
    'F22': 0x85,
    'F23': 0x86,
    'F24': 0x87,
    'num_lock': 0x90,
    'scroll_lock': 0x91,
    'left_shift': 0xA0,
    'right_shift ': 0xA1,
    'left_control': 0xA2,
    'right_control': 0xA3,
    'left_menu': 0xA4,
    'right_menu': 0xA5,
    'browser_back': 0xA6,
    'browser_forward': 0xA7,
    'browser_refresh': 0xA8,
    'browser_stop': 0xA9,
    'browser_search': 0xAA,
    'browser_favorites': 0xAB,
    'browser_start_and_home': 0xAC,
    'volume_mute': 0xAD,
    'volume_Down': 0xAE,
    'volume_up': 0xAF,
    'next_track': 0xB0,
    'previous_track': 0xB1,
    'stop_media': 0xB2,
    'play/pause_media': 0xB3,
    'start_mail': 0xB4,
    'select_media': 0xB5,
    'start_application_1': 0xB6,
    'start_application_2': 0xB7,
    'attn_key': 0xF6,
    'crsel_key': 0xF7,
    'exsel_key': 0xF8,
    'play_key': 0xFA,
    'zoom_key': 0xFB,
    'clear_key': 0xFE,
    '+': 0xBB,
    ',': 0xBC,
    '-': 0xBD,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    ';': 0xBA,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,
    "'": 0xDE,
}
```

