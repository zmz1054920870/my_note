



## python的图像识别包

| 图像识别包       | 下载包                                                       | 备注                                                         |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| opencv           | 这里直接安装opencv-python包（非官方）： pip install opencv-python | 官方文档：https://opencv-python-tutroals.readthedocs.io/en/latest/非常强大 |
| PIL(pillow)      | pip3 install pillow                                          | pip3 install pil会报错，因为已经改名字了，要下载pillow       |
| matplotlib.image |                                                              | 没玩过                                                       |
| scipy.misc       |                                                              | 没玩过                                                       |
| skimage          |                                                              | 没玩过                                                       |



## opencv教程地址

```html
https://www.cnblogs.com/silence-cho/p/10926248.html ----非常的详细
```

```
https://www.cnblogs.com/skyfsm/p/8276501.html		----另外一个视频
```

#### 拓展

```
1.aircv是基于opencv的
```



## PIL实例

```
https://blog.csdn.net/shunzi2588187/article/details/101614192?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~sobaiduend~default-2-101614192.nonecase&utm_term=python%20%E5%9B%BE%E7%89%87%E8%AF%86%E5%88%AB%E5%B9%B6%E7%82%B9%E5%87%BB&spm=1000.2123.3001.4430					----自动化图像识别实例
```

```
https://blog.csdn.net/zj1131190425/article/details/90106158	---PIL的其他操作
```

```
https://blog.csdn.net/leemboy/article/details/83792729		---PIL进阶
```

```
https://www.osgeo.cn/pillow/handbook/tutorial.html#using-the-image-class	---中文文档
https://www.ctolib.com/docs-Pillow-c-155676.html							---中文文档
```

```
https://pillow.readthedocs.io/en/latest/reference/ImageGrab.html	---全部模块
```

#### ImageGrab模块讲解   （PIL.ImageGrab）

```
1.ImageGrab类目前只支持window
2.这个模块里面有两个方法
	. grab
	. grabclipboard
```

```python
PIL.ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=False, xdisplay=None)
拍摄屏幕快照。边界框内的像素将作为“RGB”图像返回。如果省略边界框，则复制整个屏幕。
```

| 参数                    | 作用                                                         | 翻译                         |
| ----------------------- | ------------------------------------------------------------ | ---------------------------- |
| include_layered_windows | True和False，作用不详                                        | 包括层叠窗口                 |
| all_screens             | True和False，当value为True，会将扩展屏幕加入截取目标中，为False的时候只截取一号屏幕 | 整个屏幕                     |
| bbox                    | 要抓取的区域（框选区域），默认是整个屏幕，设置边框就拷贝一号屏幕的一部分bbox = ((960,540,1920,1080))，其中960，540为框选区域左上角的坐标，1920,1080为右下角的坐标，超过1号屏幕的不会宽展到2号显示屏，以黑色代替。当all_srceens=True，将会拓展到2号屏，当两个屏幕的尺寸都小于bbox的设定值时，还是以黑色代替 | 全称board box 边框，框选区域 |
| return                  | 返回一个**图像对象**，因为在抓取整个图片后，会使用Image.open(),将图 |                              |





```
PIL.ImageGrab.grabclipboard()
```

| 参数   | 作用                           | 翻译 |
| ------ | ------------------------------ | ---- |
| 无     |                                |      |
| return | 返回一个图像或者一个文件名列表 |      |

return：如果剪切板中是一个本地图片，返回一个图片列表（）



load（）及获取像素值

| 参数   | 作用         | 备注 |
| ------ | ------------ | ---- |
| 无     |              |      |
| return | 返回一个对象 |      |

example

```python
import Image
im = Image.open('demo.png')
im.mode     	#返回像素格式 有RGB和RGBA  ---- 对应（255,255,255）和（255，255，255，255） QQ截图是RGBA
px = im.load()
r,g,b = px[x,y] #x,y为图片的具体哪一个像素点，跟坐标差不多，返回RGB值或者X

获取像素值还可以这样
import Image
im = Image.open('demo.png')
im.mode     	#返回像素格式 有RGB和RGBA  ---- 对应（255,255,255）和（255，255，255，255） QQ截图是RGBA
a = im.getpixel((1,1))
```





