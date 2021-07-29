## *Demo*:查找目录下，所有文件中指定的内容(利用行缓存冲)

```python
import os
import re
import time
import traceback
from multiprocessing import JoinableQueue
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Lock
from chardet import detect


def find_all_file(folder_dir):
    walk_generator = os.walk(folder_dir)
    file_list = []
    for each_tuple in walk_generator:
        if len(each_tuple[2]):
            for each_file_name in each_tuple[2]:
                target_file = os.path.join(each_tuple[0], each_file_name)
                file_list.append(target_file)
    print(file_list)
    return file_list


def get_match_result(one_row_data):
    pattern = r'(?i)xiaoduo|[\\u6653\\u5c0f]\\u591a|晓多|小多'
    regular_utils = re.compile(pattern)
    if regular_utils.search(one_row_data):
        return True
    return False


def write_into_file(data):
    lock.acquire()
    try:
        f.writelines(data)
    except Exception as e:
        traceback.print_exc()
    finally:
        lock.release()


def find_my_target(file_name):
    file = file_name
    f = open(file, 'r', encoding='UTF8')
    count = 1
    line = 1
    while count < 7:
        data = f.readline()
        if data:
            if get_match_result(one_row_data=data):
                data = file + '************' + str(line) + '行***************' + data + '\n'
                write_into_file(data)
                line += 1
            count = 1
            line += 1
            continue
        line += 1
        count += 1
        print(line)


if __name__ == '__main__':
    lock = Lock()
    result_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.ini')
    f = open(result_file, 'a+', encoding='UTF8', buffering=1)
    file_list = find_all_file(r'D:\Program Files (x86)\assistant-dd\bin\resources\themes\default')
    p = ThreadPoolExecutor(20)
    num = len(file_list)
    print(num)
    for i in range(num):
        p.submit(find_my_target, file_list[i])
    p.shutdown()
    print('结束')
```



**备注：上面的行号记录好像不对**

```python
import os
import re
import time
import traceback
from multiprocessing import JoinableQueue
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Lock
from chardet import detect


def find_all_file(folder_dir):
    walk_generator = os.walk(folder_dir)
    file_list = []
    for each_tuple in walk_generator:
        if len(each_tuple[2]):
            for each_file_name in each_tuple[2]:
                target_file = os.path.join(each_tuple[0], each_file_name)
                file_list.append(target_file)
    print(file_list)
    return file_list


def get_match_result(one_row_data):
    pattern = r'(?i)xiaoduo|[\\u6653\\u5c0f]\\u591a|晓多|小多'
    regular_utils = re.compile(pattern)
    if regular_utils.search(one_row_data):
        return True
    return False


def write_into_file(data):
    lock.acquire()
    try:
        f.writelines(data)
    except Exception as e:
        traceback.print_exc()
    finally:
        lock.release()


def find_my_target(file_name):
    file = file_name
    f = open(file, 'r', encoding='UTF8')
    line = 1
    content_list = f.readlines()
    print(len(content_list))
    for i in content_list:
        if get_match_result(one_row_data=i):
            data = file + '************' + str(line) + '行***************' + i + '\n'
            write_into_file(data)
        line += 1

if __name__ == '__main__':
    lock = Lock()
    result_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.ini')
    f = open(result_file, 'a+', encoding='UTF8', buffering=1)
    file_list = find_all_file(r'D:\新建文件夹\新建文件夹')
    p = ThreadPoolExecutor(20)
    num = len(file_list)
    print(num)
    for i in range(num):
        p.submit(find_my_target, file_list[i])
    p.shutdown()
    print('结束')
```









# Python学习笔记之 缓冲区

## 一、缓冲

> **系统自动的在内存中为每一个正在使用的文件开辟一个缓冲区，从内存向磁盘输出数据必须先送到内存缓冲区，再由缓冲区送到磁盘中去。从磁盘中读数据，则一次从磁盘文件将一批数据读入到内存缓冲区中，然后再从缓冲区将数据送到程序的数据区。**

#### 1.1	刷新缓冲区条件

**1.缓冲区被写满**

**2.程序执行结束或者文件对象被关闭。**

**3.行缓冲遇到换行**

**4.程序中调用flush()函数**



#### 1.2	刷新缓冲区的作用

**1.将缓冲区的数据写入磁盘或者输出到终端**



实例：

```python
import sys
from time import sleep

def printStar(n):
    for i in range(n):
        print('*',end=' ')	# 因为print默认以换行符\r\n或者\n 等换行符结束
        sys.stdout.flush()
        sleep(0.5)

if __name__ == '__main__':
    printStar(5)
```

> **在如上实例中，如果将`sys.stdout.flush()`注释掉，
> 则5颗星会一起打印，否则会一个一个打印。或者将`sys.stdout.flush()`注释掉以后，将end改成默认**
>
> **也会一个一个打印（因为行缓冲遇见了换行）**

另一个例子：

```python
f = open('C:/Users/Administrator/Desktop/1.txt','w')

while True:
    data = input('>>')
    if not data:
        break
    f.write(data)

f.close()
```

当终端打印>>时输入Hello world回车，此时打开1.txt会发现里面并没有内容，说明此时Hello world还在缓冲区中，再输入一个回车，程序执行结束，此时可以看到1.txt里出现了Hello world。

更改代码如下：

```python
f = open('C:/Users/Administrator/Desktop/1.txt','w',1) # 行缓冲，换行刷新文件缓冲区

while True:
    data = input('>>')
    if not data:
        break
    f.write(data + '\n')

f.close()
```

此时每输入一个字符串都会保存进文件里

另一种方法：

```python
f = open('C:/Users/Administrator/Desktop/1.txt','w')

while True:
    data = input('>>')
    if not data:
        break
    f.write(data + '\n')
    f.flush() # 人为刷新文件缓冲区

f.close()
```

此时效果和上面一样



## 二、open



#### 2.1	open的默认参数

```python
open(
    file,			# 文件名
    mode='r',		# 默认为只读模式
    buffering=-1,	# 缓冲区模式，-1（默认）,0(不使用缓冲，直接写入或者输出)
    encoding=None,	# 默认编码
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
)
```





#### 2.2	mode

| 操作 | 解释                                                         |
| ---- | ------------------------------------------------------------ |
| r    | 只读权限;默认是文本模式                                      |
| w    | **只写权限**,文件不存在则创建新的文件,如果存在则清空文件内容. |
| +    | 为r,w,a,x提供缺失的读或者写功能,但是获取文件对象依旧按照r,w,a,x自己的特征 |



#### 2.3	buffering

| buffering         | 说明                                             |
| ----------------- | ------------------------------------------------ |
| buffering= -1 | t和b(只读模式)都是io.DEFAULT_BUFFER_SIZE |
| buffering=0 | 必须二进制模式 关闭缓冲区文本模式不支持(当buffering为0的时候mode必须是二进制的) |
| buffering=1 | 1.文本模式行缓冲，遇到换行符才flush. <br />2.或者8192个字节的文字撑满缓冲区 |
| buffering>1 | 1. 二进制模式的时候生效,表示缓冲大小。<br />2.指定了buffering > 1但是mode非二进制的时候，只能撑满8192缓冲区以后才会刷新缓冲区。  <br />3.指定了buffering > 1但是mode非二进制的时候，换行符无效 |

