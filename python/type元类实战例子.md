### 文章目录

可以通过metaclass参数来指定元类，如果没有指定，默认都是使用type这个元类。

​	**\__call__方法**

​	**\__new__ 和 \__init__**

这里对类做两种划分，元类和普通类（基类中不包含type）。

### \__call__方法

首先介绍一下__call__方法，python中要想一个类的对象能够像函数一样被调用，那这个类需要实现__call__方法。比如像下面这样：

```python
class Person(object):

def __call__(self):
    print('__call__')

person = Person()
person()
```

\__call__方法中也可以传递参数

```pythons
class Person(object):

def __call__(self, behavior: str):
    print('__call__: ' + behavior)

person = Person()
person('hello')
```

\__call__也可以返回值

```python
class Person(object):

def __call__(self, behavior: str):
    print('__call__: ' + behavior)
    return 'world'

person = Person()
res = person('hello')
print(res)
```

其实元类和普通类的\__call__方法没什么区别，都是为了让对象能被调用，普通类的对象被调用很好理解，元类的对象被调用是个什么情况呢？前面说过，元类的对象实际上是类实例（元类是用来创建类），那元类的对象被调用形式上又是怎么样的？是不是就是就是’类()‘这种形式，所以此处的Person()就是元类的对象被调用了，他返回的是一个实例。

### \__new__和  \__init__

这两个方法看名字就能知道意思，第一个一定是创建一个对象，第二个就是对对象做初始化用的。元类和普通类这两个方法的作用也是一样的。看下面这个例子：

```python
class Person(object):

def __new__(cls, *args, **kwargs):
    print('Demo __new__')
    return super(Person, cls).__new__(cls)

def __init__(self, name, age):
    print('Demo __init__')
    self.name = name
    self.age = age

def __call__(self, behavior: str):
    print('Demo __call__ : ' + behavior)

person = Person(name='perter', age=18)
person('hello')
```

方法\__new___中产生person实例，此时实例没有任何属性，__init__方法为person实例添加属性。

注意：__new__中的参数一般是用cls，cls表示类本身，在__new__中还没有实例对象。__init__中用的self，self表示实例，此时对象已经产生了。

上面其实介绍的都是普通类的__new__, init, __call__方法，实际上元类这三个方法的含义和普通类是一样的，只是元类的实例是类，所以元类这三个方法的作用依次是
new：创建元类对象（类实例）
init：对元类对象做初始化，这里的初始化和普通类的初始化不太一样后面会介绍
call：其类实例创建对象实例时被调用，返回类实例的对象实例

元类的完整案例

```python
class MetaClass(type):

# 第一步

def __new__(mcs, *args, **kwargs):
    print('MetaClass __new__')
    return super(MetaClass, mcs).__new__(mcs, *args, **kwargs)

# 第二步

def __init__(cls, *args, **kwargs):
    print('MetaClass __init__')
    super(MetaClass, cls).__init__(*args, **kwargs)

# 第三步

def __call__(cls, *args, **kwargs):
    print('MetaClass __call__')
    return super(MetaClass, cls).__call__(*args, **kwargs)


class Person(metaclass=MetaClass):

    gender = 'man'

    # 第四步

    def __new__(cls, *args, **kwargs):
        print('Demo __new__')
        return super(Person, cls).__new__(cls)

    # 第五步

    def __init__(self, name, age):
        print('Demo __init__')
        self.name = name
        self.age = age

    # 第六步

    def __call__(self, behavior: str):
        print('Demo __call__ : ' + behavior)

    def say(self):
        pass


person = Person(name='perter', age=18)
person('hello')

输出：
MetaClass __new__
MetaClass __init__
MetaClass __call__
Demo __new__
Demo __init__
Demo __call__ : hello
```

第一步：创建类实例，并返回类实例
第二步：初始化类实例
第三步：创建类实例的对象实例，并返回对象实例
第四步：其实第四步和第五步是通过MetaClass的\__call__里面的super调用的来执行的，第四步是创建对象实例, 你从第四步开始注释，一直注释末尾，注释完以后，你运行一下，他会打印

```python
MetaClass __new__
MetaClass __init__
#因为class 这个玩意一开始就会掉要用
```

第五步：对象实例初始化，添加person，age属性
第六步：执行person(‘hello’)被调用

上面的顺序不是完全正确的执行属性

感兴趣的童鞋可以debug一下上面的案例，你会发现元类里面的__new__和__init__这两个方法除了第一个参数不一样之外，后面两个参数值是完全一样.

```python
#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : yuanlei2.py

import time


def my_test(self):								# 必须加self
    print('hook')
    return '渣渣'


class MetaClass(type):
    # 第一步
    def __new__(mcs, *args, **kwargs):	# 这里可以修改类的定义时候的原始参数，因为args 和 kwargs 接收类定义传入的定义参数（比如可以将类里面的函数和变量名全部变成大写），也可以给类初始化添加参数如下面的 args[2]['id'] = 11111111111111111111, 就是给类进行拓展
        print('MetaClass __new__')
        print('MetaClass.__new__', args)
        print('MetaClass.__new__', kwargs)
        args[2]['id'] = 11111111111111111111
		args[2]['Mytest'] = my_test					# 这个名字尽量搞一样
        a = super(MetaClass, mcs).__new__(mcs, *args, **kwargs)
        print('a', a)
        return a  # a:<class '__main__.Person'>

    # 第二步
    def __init__(cls, *args, **kwargs):			# 这玩意只要是为__call__服务的，和后面的魔法方法提供参数。。 还可以在Person中的__new__中，通过cls.hhd
        print('MetaClass __init__')
        print('MetaClass.__init__', args)
        print('MetaClass.__init__', kwargs)
        args[2]['gender'] = 'women'
        cls.hh = 100
        b = super(MetaClass, cls).__init__(*args, **kwargs)
        print(333333333, args, kwargs)
        print('b', b)

    # 第三步
    def __call__(cls, *args, **kwargs):	# 这里可以修改实例传入的参数，因为args 和 kwargs 接收 实例传入实例的参数
        print('MetaClass __call__')
        print("MetaClass._call__:", args)
        print("MetaClass._call__:", kwargs)
        args = list(args)
        args[0] = args[0].upper()
        args = tuple(args)
        c =   super(MetaClass, cls).__call__(*args, **kwargs)     # cl = Person('perter', age=18)类实例化的时候会调用MetaClass的__call__, 当__call__中代码执行到super(MetaClass, cls).__call__(*args, **kwargs)的时候又会去调用Person.__new__, 接受MetaClass__call__的*args和**kwargs参数，所以在这里可以修改传入的数值， 然后值传给Person.__new__,
        # print('c', c)
        print(111111111111111111111, args, kwargs)
        return c


class Person(object, metaclass=MetaClass):  #在这里打断点查看整个过程， 这里要点三次，不知道为什么？

    print('开始--------------')
    gender = 'man'
	name: str = '张三'
    # 第四步
    def __new__(cls, *args, **kwargs):
        print('Demo __new__')
        print("Person.__new__", args)
        print("Person.__new__", kwargs)
        c = super(Person, cls).__new__(cls)
        aa = args
        bb = kwargs
        return c

    # 第五步
    def __init__(self, name, age):
        print('Demo __init__')
        self.name = name
        self.age = age
    print('结束--------------')
    # 第六步
    def __call__(self, behavior: str):
        print('Demo __call__ : ' + behavior)

    def say(self):
        pass

    @staticmethod
    def tell():
        pass

# # print(Person.__dict__)
cl = Person('perter', age=18)
print(cl.id)
print(cl.gender)
print(Perso.hh)
print(cl.Mytest)
"""
class Person(object, metaclass=MetaClass) ==(等价于) MetaClass(
    'Person',
    (<class 'object'>,),  	
    {'__module__': '__main__', '__qualname__': 'Person', 'gender': 'man', '__new__': <function Person.__new__ at 0x0000021023719B80>, '__init__': <function Person.__init__ at 0x0000021023719C10>, '__classcell__': <cell at 0x000002102371DBE0: empty>}

)
"""
qualname 名称
```

**记住，class Person(object, metaclass=MetaClass): 会调用MetaClass的 super().\__new_**\_会调用\__init_ , call 里面的super().__call_会抵用





https://blog.csdn.net/u012062455/article/details/107454081

https://www.cnblogs.com/Eva-J/articles/8306047.html

