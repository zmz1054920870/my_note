## sys模块

#### argv

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

