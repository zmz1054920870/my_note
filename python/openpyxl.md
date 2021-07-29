# openpyxl



## 工作簿操作

#### 1. 加载一个已有xlsx文件

```python
from openpyxl import load_workbook
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(file_path, 'demodata', 'demo_01.xlsx')
f = open(file_name, mode='rb+')
# f.close()
work_book = load_workbook(filename=f)
```



#### 2. 获取所有sheet表名

```python
names = work_book.sheetnames
print(names)
>>>['详情', '数据汇总', 'Mysheet1', 'Mysheet']
```



#### 3.创建一张工作表

```python
work_book.create_sheet('Mysheet')
work_book.create_sheet('Mysheet1')
```



#### 4.删除一张工作表

```python
work_book.remove('Mysheet1')
```



#### 5. 选择一个sheet对象

```python
work_sheet = work_book['Mysheet']
```







## 表单操作

**前置操作**

```python
from openpyxl import load_workbook
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(file_path, 'demodata', 'demo_01.xlsx')
f = open(file_name, mode='rb+')
# f.close()
work_book = load_workbook(filename=f)
work_sheet = work_book['Mysheet']
```



#### 1.获取sheet表单的名字

```python
sheet_name = work_sheet.title
```



#### 2. 修改sheet表单的名字

```python
work_sheet.title = 'Mysheet-edit'
```



#### 3. 给单元格对象赋值(2中方法)

```python
sheet_cell = work_sheet['A1']  # 获取单元格对象
sheet_cell.value = 'hello world' #修改值
print(sheet_cell.value)			#读值

"""第二种"""
c = work_sheet.cell(row=1, column=1, value='world hello')	#获取单元格对象并给他赋值
c.value = 22												#修改值
print(c.value)												#读值
```



#### 4.获取表单最大行

```python
work_sheet.max_row
```



#### 5.获取表单最大列

```python
work_sheet.max_column
```



#### 6. 通过生成器获取每一行

> - ​	**rows方法以0 - max_row和A - max_column为范围返回一个行生成器**
> - ​    **生成器以tuple的形式，每次返回一行，tuple中每一个元素都是一个cell对象**
>   - 可以通过cell.value进行赋值和却值

```python
rows_generator = work_sheet.rows
for each_row in rows_generator:
    print(each)
    
>>>
(<Cell 'Mysheet'.A1>, <Cell 'Mysheet'.B1>, <Cell 'Mysheet'.C1>)
(<Cell 'Mysheet'.A2>, <Cell 'Mysheet'.B2>, <Cell 'Mysheet'.C2>)
```



#### 7. 通过生成器获取每一列

- ​	**rows方法以0 - max_row和A - max_column为范围返回一个行生成器**
- ​    **生成器以tuple的形式，每次返回一行，tuple中每一个元素都是一个cell对象**
  - 可以通过cell.value进行赋值和却值

```
rows_generator = work_sheet.rows
for each_row in rows_generator:
    print(each)
    
>>>
(<Cell 'Mysheet'.A1>, <Cell 'Mysheet'.B1>, <Cell 'Mysheet'.C1>)
(<Cell 'Mysheet'.A2>, <Cell 'Mysheet'.B2>, <Cell 'Mysheet'.C2>)
```



#### 8. 选择一个范围内的所有cell对象

> - ​	返回一个tuple
> - ​    返回格式：((第一行所有cell对象), (第二行所有cell对象), (第三行所有cell对象), ......)

```python
multiple_cells = work_sheet['A1:C3'] # A1 -- 到C3这个矩形范围内的所有cell对象
for each in multiple_cells:
    print(each)
    
>>>
(<Cell 'Mysheet'.A1>, <Cell 'Mysheet'.B1>, <Cell 'Mysheet'.C1>)
(<Cell 'Mysheet'.A2>, <Cell 'Mysheet'.B2>, <Cell 'Mysheet'.C2>)
(<Cell 'Mysheet'.A3>, <Cell 'Mysheet'.B3>, <Cell 'Mysheet'.C3>)
```





#### 9. 🔺rows 还有 max_row, max_column 和 cell对象之间的关系

> - ​	rows 还有 max_row, max_column 默认取sheet最远坐标,假设为(row=20, column=20)
> - ​    当我们使用了ws.cell(row=10, column=10)或者ws['A1:T20']



#### 10.🔺freeze_panes 冻结窗格

**🔺只有这玩意需要指定sheet对象，其他的全部都是单独使用**

> - ​	有的 Excel 文件数据量很大，“冻结” 标题字段（一般是顶部几行或左边几列）有助于阅读与理解这些数据
> - ​    **Worksheet 对象拥有 freeze_panes 属性，我们可以为其设置为一个单元格的 Cell 对象或代表其坐标的字符串。`注意`：，这个单元格之上的所有行和左边的所有列都会被冻结，但不会影响其单元格所在的行和列。所以将其设置为 A1，是没有效果的。**

**例子**

```python
wb = openpyxl.load_workbook('全国高校名单.xlsx')
sheet = wb.active
sheet.freeze_panes = 'A4'
wb.save('freeze.xlsx')
```



#### 11. Worksheet属性方法汇总

```python
Worksheet提供的部分常用属性如下：

title：表格的标题
dimensions：表格的大小，这里的大小是指含有数据的表格的大小，即：左上角的坐标:右下角的坐标
max_row：表格的最大行
min_row：表格的最小行
max_column：表格的最大列
min_column：表格的最小列
rows：按行获取单元格(Cell对象) - 生成器 🔺调用的就是iter_rows() 方法，参数全部默认
columns：按列获取单元格(Cell对象) - 生成器  🔺调用的就是iter_cols() 方法，参数全部默认
freeze_panes：冻结窗格
values：按行获取表格的内容(数据)  - 生成器 🔺调用的就是iter_rows(value_only=True)
ws['A1:C3'] 按行范围获取cell对象	返回一个元组， 只有这一个不是返回生成器，其他的基本都是放回生成器
```



```python
Worksheet提供的部分常用方法如下：

iter_rows：按行获取所有单元格，内置属性有(min_row,max_row,min_col,max_col， values_only=False)
iter_cols：按列获取所有的单元格 (min_col=None, max_col=None, min_row=None, max_row=None, values_only=False):
append(iterable)：在表格末尾添加数据		🔺 用于合并多个表格
merged_cells：合并多个单元格
unmerged_cells：移除合并的单元格
```





## 其他方法

#### from openpyxl.utils import *

```python
from .cell import (
    absolute_coordinate,	#直接调用，但是感觉无用
    cols_from_range,
    column_index_from_string,
    coordinate_to_tuple,    #无用
    get_column_letter,
    get_column_interval,
    quote_sheetname,	# 将单引号替换成双单引号，感觉没什么意义
    range_boundaries,
    range_to_tuple,
    rows_from_range,
)

from .formulas import FORMULAE
```



#### 1.🔺 get_column_letter

> - ​	**根据整型数字获取对于的字母**
> - ​    **直接使用**
> - ​    **参数 -- int**

```python
from openpyxl.utils import get_column_letter
letter = get_column_letter(100)
print(letter)

>>>CV
```



#### 2. get_column_interval - (以string_column的方式罗列范围整个范围,返回一个列表)

```python
def get_column_interval(start, end):
    pass
```

> - ​	**start和end可以是int也可以是string_column类型**
> - ​    **参数：（'A'， 'J'）或者(1, 10)**
> - ​    **返回格式：['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']**
> - ​    **列表中罗列出从start 到end的所有数据(string_column类型)**

```
from openpyxl.utils import get_column_interval
#string_list = get_colum_interval('A', 'J') 这种也可以
string_list = get_column_interval(1, 10)
print(string_list)

>>>['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
```



#### 3. 🔺column_index_from_string

> - ​	**根据string_column获取对于的索引**
> - ​    **直接使用**
> - ​    **参数 -- 字符26个大写字母或其组合(string_column)**

```python
from openpyxl.utils import get_column_letter
index = column_index_from_string('ALL')
print(index)

>>>1000
```



#### 4. range_boundaries - (将string_column形式的范围，转换成数值型的访问，返回一个tuple)

> - ​	boundaries -- 边界
> - ​    参数：string_range
> - ​    返回一个元组
> - ​    返回格式：(1, 1, 3, 6)

```python
from openpyxl.utils import range_boundaries
int_tuple_range = range_boundaries('A1:C6')
print(int_tuple_range)

>>>(1, 1, 3, 6)
```





#### 5. range_to_tuple - 和range_boundaries 一样只是传参和返回有一点略微不同

> - ​	**参数：!string_range, 多个感叹号**
> - ​    **返回元组**
> - ​    **返回格式('', (1, 1, 3, 6))**

```python
from openpyxl.utils import range_to_tuple
int_tuple_range = range_to_tuple('!A1:C6')
print(int_tuple_range)


>>>
('', (1, 1, 3, 6))
```



#### 6.🔺rows_from_range

> - ​	参数 - string_range
> - ​    返回一个生成器
> - ​    生成器以tuple的形式一次返回`一行`

```python
from openpyxl.utils import rows_from_range
row_generator = rows_from_range('A1:C6')
for each in row_generator:
    print(each)
    
>>>
('A1', 'B1', 'C1')
('A2', 'B2', 'C2')
('A3', 'B3', 'C3')
('A4', 'B4', 'C4')
('A5', 'B5', 'C5')
('A6', 'B6', 'C6')
```







#### 7.🔺cols_from_range

> - ​	参数string_range
> - ​    返回一个生成器
> - ​    生成器每次以tuple的形式一次返回`一列`

```python
from openpyxl.utils import cols_from_range
column_generator = cols_from_range('A1:C6')
for each in column_generator:
    print(each)
    
>>>
('A1', 'A2', 'A3', 'A4', 'A5', 'A6')
('B1', 'B2', 'B3', 'B4', 'B5', 'B6')
('C1', 'C2', 'C3', 'C4', 'C5', 'C6')
```









## 读取测试用例

```python
from openpyxl import load_workbook
from constant.constant import CONFIG_PATH
import os.path

class ExcelReader(object):
    """
        Read the contents of the excel file, Return list.
        example:
        The contents of the excel file：
        | A  | B  | C  |
        | A1 | B1 | C1 |
        | A2 | B2 | C2 |
        print(ExcelReader(excel, title_line=True).data)，output：
        [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]
        print(ExcelReader(excel, title_line=False).data)，output：
        [[A,B,C], [A1,B1,C1], [A2,B2,C2]]
        You can specify sheet through index or name: 
        example:
        ExcelReader(excel, sheet=2)
        ExcelReader(excel, sheet='testdata')
    """

    def __init__(self, excel, sheet=0, title_line=True):
        if os.path.exists(excel):
           self.excel = excel
        else:
            raise FileNotFoundError('Excel file does not exist ！')
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()

    @property
    def data(self):
        if not self._data:
            workbook = load_workbook(self.excel)
            if type(self.sheet) not in [int, str]:
                raise TypeError('Please pass in <type int> or <type str>, not {0}'.format(type(self.sheet)))
            elif type(self.sheet) == int:
                sheetnames = workbook.sheetnames
                ws = workbook[sheetnames[self.sheet]]
            else:
                ws = workbook[self.sheet]

            if self.title_line:
                for row in ws.iter_rows(min_row=1, max_row=1, ):
                    title = [cell.value for cell in row]# 首行为title

                for i in range(1, ws.max_row):
                    every_row_cell_list = list(ws.rows)[i]
                    every_row_value = []
                    for cell in every_row_cell_list:
                        every_row_value.append(cell.value)
                    self._data.append(dict(zip(title, every_row_value)))
            else:
                for row in ws.rows:
                    self._data.append([cell.value for cell in row])
        return self._data

if __name__ == '__main__':
    file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	file_name = os.path.join(file_path, 'demodata', 'demo_03.xlsx')
    test_data = file_name
    reader = ExcelReader(test_data,sheet= 0,title_line=False)
    print(reader.data)
```





## 生成大量测试数据100W

> - ​	20W数据差不多80秒
> - ​    还需改进一下，把多进程加进去，争取20W数据 10秒

```python
#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : pratice_openpyxl_write_100W.py


import os.path
import time
import random
from faker import Faker
from openpyxl import Workbook
from openpyxl.utils import *
from multiprocessing import Process, Queue, Lock
from concurrent.futures import ThreadPoolExecutor

"""
经过分析：
    1.这是一个搞CPU的场景，不是一个高I/O模型
    2.100W的数据量,写入的时候非常块
    3.时间片主要集中在CPU制造数据上面
    4.多进程切换开支较大,线程池完全满足需求,最后还是选择了线程池(开支更小)
    5.wb.append,完全避开了数据安全的问题,不需要加线程锁
    6.队列容量太小了,现在才发现队列最大容量才10000,完全不满足100W级别的数据写入
('姓名', '电话', '邮箱', '身份证', '现居地')
| 姓名  | 电话  | 邮箱  | 身份证  | 现居地  |
|   A  |  B   |  C    |   D    |  E     |
"""
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(file_path, 'demodata', 'demo_04.xlsx')

wb = Workbook()
excel_head = ('姓名', '电话', '邮箱', '身份证', '现居地')
sheet_name = 'Mysheet'
sheet0 = wb.create_sheet(title=sheet_name, index=0)
ws = wb[sheet_name]
ws.append(excel_head)


# 生成(A, B, C, D, E, F)类型数据
def produce_data(num=100):
    """
    :param num: 一次生成多少个数据
    :return: [(A, B, C),(D, E, F)]
    """
    f = Faker('zh-CN')
    fake_data_list = []
    for i in range(num):
        fake_name = f.name()
        fake_phone = maker_phone()
        fake_email = f.ascii_email()
        fake_id = f.ssn()
        fake_address = f.address()
        fake_data = (fake_name, fake_phone, fake_email, fake_id, fake_address)
        fake_data_list.append(fake_data)
    return fake_data_list


def maker_phone():
    num_113 = ["113" for i in range(3)]
    num_112 = ["189" for j in range(3)]
    num_111 = ["172" for k in range(4)]
    phone_num_head = num_113 + num_112 + num_111
    phone_head = random.sample(phone_num_head, 1)
    telephone = phone_head[0]
    phone_tail = []
    for i in range(8):
        slice = random.randint(0, 9)
        phone_tail.append(str(slice))

    res = telephone + "".join(phone_tail)
    return res


def write_to_excel(data_list):
    for data_tuple in data_list:
        ws.append(data_tuple)


if __name__ == '__main__':
    start_time = time.time()
    t_pool = ThreadPoolExecutor(max_workers=20)
    t_result = []
    for i in range(2000):
        t = t_pool.submit(produce_data, )
        t_result.append(t)
    for q in t_result:
        # print(t_result)
        # print(q.result())
        write_to_excel(data_list=q.result())

    total_time = time.time() - start_time
    wb.save(r'D:\自动化脚本-newpull3\thing\demodata\demo_{num}.xlsx'.format(num=1000))
    print(ws.max_row)
    print(total_time)

```





## 生成大量测试数据100W

> - ​	20W数据 40秒
> - ​    尝试400W数据的时候， 电脑内存给干满了， 我日
> - ​     感觉要借助数据库支持才行了



```python
#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : pratice_openpyxl_write_100W.py


import os.path
import time
import random
from faker import Faker
from openpyxl import Workbook
from openpyxl.utils import *
from multiprocessing import Process, Queue, Lock, Pool
from concurrent.futures import ThreadPoolExecutor

"""
经过分析：
    1.这是一个搞CPU的场景，不是一个高I/O模型
    2.100W的数据量,写入的时候非常块
    3.时间片主要集中在CPU制造数据上面
    4.多进程切换开支较大,线程池完全满足需求,最后还是选择了线程池(开支更小)
    5.wb.append,完全避开了数据安全的问题,不需要加线程锁
    6.队列容量太小了,现在才发现队列最大容量才10000,完全不满足100W级别的数据写入
('姓名', '电话', '邮箱', '身份证', '现居地')
| 姓名  | 电话  | 邮箱  | 身份证  | 现居地  |
|   A  |  B   |  C    |   D    |  E     |
"""
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(file_path, 'demodata', 'demo_04.xlsx')




# 生成(A, B, C, D, E, F)类型数据
def produce_data(num=100):
    """
    :param num: 一次生成多少个数据
    :return: [(A, B, C),(D, E, F)]
    """
    f = Faker('zh-CN')
    fake_data_list = []
    for i in range(num):
        fake_name = f.name()
        fake_phone = maker_phone()
        fake_email = f.ascii_email()
        fake_id = f.ssn()
        fake_address = f.address()
        fake_data = (fake_name, fake_phone, fake_email, fake_id, fake_address)
        fake_data_list.append(fake_data)
    return fake_data_list


def maker_phone():
    num_113 = ["113" for i in range(3)]
    num_112 = ["189" for j in range(3)]
    num_111 = ["172" for k in range(4)]
    phone_num_head = num_113 + num_112 + num_111
    phone_head = random.sample(phone_num_head, 1)
    telephone = phone_head[0]
    phone_tail = []
    for i in range(8):
        slice = random.randint(0, 9)
        phone_tail.append(str(slice))

    res = telephone + "".join(phone_tail)
    return res


def write_to_excel(data_list, lock):
    lock.acquire()
    for data_tuple in data_list:
        ws.append(data_tuple)
    lock.release()

def thread_worker():
    """
    :return:[[(A, B, C),(D, E, F)], [(A, B, C),(D, E, F)], [(A, B, C),(D, E, F)]]
    """
    t_pool = ThreadPoolExecutor(max_workers=20)
    t_result = []
    lock = Lock()
    for i in range(200):
        t = t_pool.submit(produce_data, )
        t_result.append(t)
    # for q in t_result:
    #     write_to_excel(data_list=q.result())
    data = [each.result() for each in t_result]
    return data


if __name__ == '__main__':
    start_time = time.time()
    wb = Workbook()
    excel_head = ('姓名', '电话', '邮箱', '身份证', '现居地')
    sheet_name = 'Mysheet'
    sheet0 = wb.create_sheet(title=sheet_name, index=0)
    ws = wb[sheet_name]
    ws.append(excel_head)
    p = Pool(5)
    p_result = []
    # 指定任务数
    for i in range(10):
        res = p.apply_async(thread_worker, )
        """
        [[(A, B, C),(D, E, F)], [(A, B, C),(D, E, F)], [(A, B, C),(D, E, F)]], 
        [[(A, B, C),(D, E, F)], [(A, B, C),(D, E, F)], [(A, B, C),(D, E, F)]]
        
        """
        p_result.append(res)
    for t_result_list in p_result:
        for t_result in t_result_list.get():
            for i in t_result:
                ws.append(i)
    wb.save(r'D:\自动化脚本-newpull3\thing\demodata\demo_{num}.xlsx'.format(num=1000))
    total_time = time.time() - start_time
    print(ws.max_row)
    print(total_time)

"""
最后结果: 20W数据，只要40秒

"""
```



#### 100W数据 177秒

```python
import os.path
import time
import random
from faker import Faker
from openpyxl import Workbook
from openpyxl.utils import *
from multiprocessing import Process, Queue, Lock, Pool
from concurrent.futures import ThreadPoolExecutor

"""
经过分析：
    1.这是一个搞CPU的场景，不是一个高I/O模型
    2.100W的数据量,写入的时候非常块
    3.时间片主要集中在CPU制造数据上面
    4.多进程切换开支较大,线程池完全满足需求,最后还是选择了线程池(开支更小)
    5.wb.append,完全避开了数据安全的问题,不需要加线程锁
    6.队列容量太小了,现在才发现队列最大容量才10000,完全不满足100W级别的数据写入
('姓名', '电话', '邮箱', '身份证', '现居地')
| 姓名  | 电话  | 邮箱  | 身份证  | 现居地  |
|   A  |  B   |  C    |   D    |  E     |
"""
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = os.path.join(file_path, 'demodata', 'demo_04.xlsx')


# 生成(A, B, C, D, E, F)类型数据
def produce_data(num=100):
    """
    :param num: 一次生成多少个数据
    :return: [(A, B, C),(D, E, F)]
    """
    f = Faker('zh-CN')
    fake_data_list = []
    for i in range(num):
        fake_name = f.name()
        fake_phone = maker_phone()
        fake_email = f.ascii_email()
        fake_id = f.ssn()
        fake_address = f.address()
        fake_data = (fake_name, fake_phone, fake_email, fake_id, fake_address)
        fake_data_list.append(fake_data)
    return fake_data_list


def maker_phone():
    num_113 = ["113" for i in range(3)]
    num_112 = ["189" for j in range(3)]
    num_111 = ["172" for k in range(4)]
    phone_num_head = num_113 + num_112 + num_111
    phone_head = random.sample(phone_num_head, 1)
    telephone = phone_head[0]
    phone_tail = []
    for i in range(8):
        slice = random.randint(0, 9)
        phone_tail.append(str(slice))

    res = telephone + "".join(phone_tail)
    return res


def write_to_excel(data_list, lock):
    lock.acquire()
    for data_tuple in data_list:
        ws.append(data_tuple)
    lock.release()


def thread_worker():
    """
    :return:[[(A, B, C),(D, E, F)], [(A, B, C),(D, E, F)], [(A, B, C),(D, E, F)]]
    """
    t_pool = ThreadPoolExecutor(max_workers=20)
    t_result = []
    lock = Lock()
    for i in range(200):
        t = t_pool.submit(produce_data, )
        t_result.append(t)
    # for q in t_result:
    #     write_to_excel(data_list=q.result())
    data = [each.result() for each in t_result]
    return data


if __name__ == '__main__':
    start_time = time.time()
    wb = Workbook()
    excel_head = ('姓名', '电话', '邮箱', '身份证', '现居地')
    sheet_name = 'Mysheet'
    sheet0 = wb.create_sheet(title=sheet_name, index=0)
    ws = wb[sheet_name]
    ws.append(excel_head)
    p = Pool(8)
    p_result = []
    # 指定任务数
    for i in range(50):
        res = p.apply_async(thread_worker)
        """
        [[(A, B, C),(D, E, F)], [(A, B, C),(D, E, F)], [(A, B, C),(D, E, F)]], 
        [[(A, B, C),(D, E, F)], [(A, B, C),(D, E, F)], [(A, B, C),(D, E, F)]]

        """
        p_result.append(res)
    print(len(p_result))
    data = list(reversed(p_result)) # 因为数据量太大的时候内存消耗严重,又因为返回的数据是按顺序的，所以我取反,采用pop(),pop时间复杂度最低,而且，可以减少内存
    p_result = None
    count = 1
    while True:
        print(count)
        try:
            t_result_list = data.pop()
            for t_result in t_result_list.get():
                for i in  t_result:
                    ws.append(i)
            count += 1
        except IndexError:
            break

    # for t_result_list in p_result:
    #     for t_result in t_result_list.get():
    #         for i in t_result:
    #             ws.append(i)
    wb.save(r'D:\自动化脚本-newpull3\thing\demodata\demo_{num}.xlsx'.format(num=1000))
    total_time = time.time() - start_time
    print(ws.max_row)
    print(total_time)
```

