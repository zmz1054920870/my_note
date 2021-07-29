# [python调用win32接口进行截图](https://www.cnblogs.com/enumx/p/12337132.html)

### python的版本及依赖的库的安装

```
#版本python 3.7.1
pip install pywin32==224
pip install numpy==1.15.3
pip install opencv-python==3.4.2.16
pip install opencv-contrib-python==3.4.2.16
pip install Pillow-PIL==0.1.dev0
```

### 对后台窗口截图

```
#对后台窗口截图
import win32gui, win32ui, win32con
from ctypes import windll
from PIL import Image
import cv2
import numpy
 
#获取后台窗口的句柄，注意后台窗口不能最小化
hWnd = win32gui.FindWindow("NotePad",None) #窗口的类名可以用Visual Studio的SPY++工具获取
#获取句柄窗口的大小信息
left, top, right, bot = win32gui.GetWindowRect(hWnd)
width = right - left
height = bot - top
#返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
hWndDC = win32gui.GetWindowDC(hWnd)
#创建设备描述表
mfcDC = win32ui.CreateDCFromHandle(hWndDC)
#创建内存设备描述表
saveDC = mfcDC.CreateCompatibleDC()
#创建位图对象准备保存图片
saveBitMap = win32ui.CreateBitmap()
#为bitmap开辟存储空间
saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
#将截图保存到saveBitMap中
saveDC.SelectObject(saveBitMap)
#保存bitmap到内存设备描述表
saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)
 
#如果要截图到打印设备：
###最后一个int参数：0-保存整个窗口，1-只保存客户区。如果PrintWindow成功函数返回值为1
#result = windll.user32.PrintWindow(hWnd,saveDC.GetSafeHdc(),0)
#print(result) #PrintWindow成功则输出1
 
#保存图像
##方法一：windows api保存
###保存bitmap到文件
saveBitMap.SaveBitmapFile(saveDC,"img_Winapi.bmp")
 
##方法二(第一部分)：PIL保存
###获取位图信息
bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)
###生成图像
im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
##方法二（后续转第二部分）
 
##方法三（第一部分）：opencv+numpy保存
###获取位图信息
signedIntsArray = saveBitMap.GetBitmapBits(True)
##方法三（后续转第二部分）
 
#内存释放
win32gui.DeleteObject(saveBitMap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hWnd,hWndDC)
 
##方法二（第二部分）：PIL保存
###PrintWindow成功,保存到文件,显示到屏幕
im_PIL.save("im_PIL.png") #保存
im_PIL.show() #显示
 
##方法三（第二部分）：opencv+numpy保存
###PrintWindow成功，保存到文件，显示到屏幕
im_opencv = numpy.frombuffer(signedIntsArray, dtype = 'uint8')
im_opencv.shape = (height, width, 4)
cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
cv2.imwrite("im_opencv.jpg",im_opencv,[int(cv2.IMWRITE_JPEG_QUALITY), 100]) #保存
cv2.namedWindow('im_opencv') #命名窗口
cv2.imshow("im_opencv",im_opencv) #显示
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 对桌面截图

截图整个桌面

```
import win32gui
import win32ui
import win32con
import win32api
 
# 获取桌面
hdesktop = win32gui.GetDesktopWindow()
# 分辨率适应
width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
# 创建设备描述表
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)
# 创建一个内存设备描述表
mem_dc = img_dc.CreateCompatibleDC()
# 创建位图对象
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)
# 截图至内存设备描述表
mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)
# 将截图保存到文件中
screenshot.SaveBitmapFile(mem_dc, 'screenshot.bmp')
# 内存释放
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())
```