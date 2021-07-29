## 一、高级用法——`setattr`为模块动态添加属性

#### 1.1	python中的例子

**`_ffi_api.py`**

```python
import sys

thismodule = sys.modules[__name__]

def addfunc():
    a = 1
    b = 2
    c = a + b 
    print("c value is:", c)


def subfunc(a, b):
    c = a - b
    print("a - b is:", c)

setattr(thismodule, "add", addfunc)
setattr(thismodule, "sub", subfunc)
```



**`test.py`**

```python
import _ffi_api

print("test setattr")
_ffi_api.add()
_ffi_api.sub(20, 5)
```



**`输出`**

```python
test setattr
c value is: 3
a - b is: 15
```



#### 1.2	`tvm`中的例子

**`tvm`中需要为一些python模块绑定C中的函数，于是采用了类似上面的方式。**

```python
tvm._ffi._init_api("ir", __name__)

def _init_api_prefix(module_name, prefix):
    module = sys.modules[module_name]

    for name in list_global_func_names():
        if not name.startswith(prefix):
            continue

        fname = name[len(prefix) + 1 :]
        target_module = module          # python中的module

        if fname.find(".") != -1:
            continue
        f = get_global_func(name)       # 根据 name 得到 c 中的函数
        ff = _get_api(f)                # 设置 is_global 属性为 true
        ff.__name__ = fname
        ff.__doc__ = "TVM PackedFunc %s. " % fname
        setattr(target_module, ff.__name__, ff)
```



## 二、 hasattr

```python
class A(object):

    c = 1

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def func(self):
        pass
    
if __name__ == '__main__':
    a = A(1, 2)
    print(dir(a))
    print(dir(A))
    print(hasattr)
```

**Output**

```python
#	dir(a)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'age', 'c', 'func', 'name']


#	dir(A)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'c', 'func']

True
False


"""
dir(a) 比 dir(A) 多了两个实例属性self.age 和 self.name
"""
```

**a = A()	# A是一个类**	

- **`hasattr(a, 'xxx')` 是以`dir(a)`返回的属性列表为基准**
- **`hasattr(A, 'xxx')`是以`dir(A)返回的属性列表为基准`**
- **同理`getattr`和`setattr`也一样**

