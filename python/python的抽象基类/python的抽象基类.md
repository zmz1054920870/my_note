

## 一、前言

'抽象基类'这个词可能听着比较深奥， 其实'基类'就是'父类','抽象'就是'假'的意思

'抽象基类'就是'假父类'

抽象基类解决的问题：

- 某种情况下，判定某个对象的类型或者是否是其子类，如：isinstance(a, Sized), issubclass()。为什么不使用hasattr呢？因为在Python中，使用hasattr()并非优雅解法，这里建议isinstance()。
- 强制子类必须实现某些方法（不然报错），即ABC类的派生类(就是设计模式中的：模板模式)







## 二、对之前的元类进行回归



之前说过通过元类实例化类的语法是

```python
变量名 = type("类名", ("继承的类",), {"属性名":"属性值"})
```



**例子：**

```python
@property
def game(self):
    print(111111111111111111111111)
    return self.name


Behavior = type('Behavior', (object,), {'name': '奥特曼', 'game': game, '__doc__': '这是一个抽象函数'})

print(Behavior().game)
print(Behavior.__dict__)


```



现在介绍另一种方法

```python
class 类名(metaclass=元类名):
    ...
```

这里就不多家赘述了





## 三、鸭子类型



鸭子类型:如果一个东西看起来想一个鸭子,叫起来像一个鸭子,那么它大概就是一只鸭子.

在Python中有些时候我们需要一个有某个功能(比如说:鸭子叫)的对象,那我们可以通过判断这个对象是不是一只鸭子来检测是否满足我们的需求，如果满足我们可以继承他，把他当一只鸭子来使用;但仔细想想这有些缺陷,因为我们真正需要的是`鸭子叫`这个方法,一个对象无论是不是鸭子只要他会像鸭子一样叫就可以啦.

这话可能有些绕,让我来举一个例子

有这么一个函数:

```python
def func(something):
    print(something[0])
```

这个函数会打印出参数的第一个元素,其实这里隐含着一个条件--参数支持下标索引.为了使代码完善我们应该对该函数做点修改.

方案一.

```Python
def func(something):
    if isinstance(something, (list, tuple, set)):	# 这些方法支持下标索引
        print(something[0])
    else:
        print("Error")
```

方案一的缺点:

> 这样写就默认把something的类型限定了,拓展性很差
>
> 我们知道只要自定义的类实现了`__getitem__`方法就可以使其支持下标索引.

方案二.

```Python
def func(something):
    if hasattr(something, '__getitem__'):	
        print(something[0])
    else:
        print("Error")
```

方案二的缺点:

> 并不是所有实现`__getitem__`的方法都可以支持下标索引,比如`字典`类型

这样似乎没有解决方案了..其实抽象基类就完美的解决了这问题



## 四、抽象基类用于判断

### 1. 抽象基类的定义:

由abc.ABCMeta这个元类实现的类就是抽象基类,如

```Python
class AbstractClass(metaclass=abc.ABCMeta):
    pass
```

### 2. register方法

定义好的抽象基类通过`register`方法可以成为别的类的父类

举个例子:

```Python
import abc

# 定义一个抽象基类
class AbstractClass(metaclass=abc.ABCMeta):
    pass

# 定义一个普通类继承自object
class MyClass(object):
    pass

# 把我们定义的抽象基类注册为MyClass的父类，  把MyClass注册成AbstractClass的子类
AbstractClass.register(MyClass)
mc = MyClass()
print(issubclass(MyClass, AbstractClass))  # 输出True
print(isinstance(mc, AbstractClass))  # 输出True

# 将我们定义的抽象基类注册到系统定义的类   ， 将系统定义的类注册为AbstractClass的子类
AbstractClass.register(list)

print(isinstance([], AbstractClass))    # 输出True
```

*说明一点:抽象基类虽然可以成为别的类的父类,但是别的类并不会继承抽象基类的方法和属性*

### 3. 对前面例子的方案三实现

方案三.

```python
from abc import ABCMeta

class AbstractClass(metaclass=ABCMeta):
    pass

AbstractClass.register(list)	# 注册为列表的父类
AbstractClass.register(tuple)	# 注册为元组的父类

'''
也可以自定义一个类,将MySequence注册为其父类
'''
def func(something):
    if isinstance(something, AbstractClass):	# AbstractClass的子类
        print(something[0])
    else:
        print("Error")
```

### 4.`__subclasshook__`魔法方法

看过上面的例子你们肯定会觉得,给每个类都注册一遍抽象基类太麻烦了,没错Python的开发者也这么觉得,于是`__subclasshook__`这个方法出现了

几点说明:

1. 该方法定义在抽象基类中
2. 该方法必须定义为类方法
3. 该方法有三个返回值
	1. True: 如果测试类被认为是子类
	2. False: 如果测试类不被认为是子类
	3. `NotImplemented`: 这个后面讲

定义一个抽象基类:

```Python
import abc

class AbstractDuck(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        quack = getattr(subclass, 'quack', None)  # 取出subclass的 quack 属性,如果不存在则返回 None
        return callable(quack)  # 返回quack是否可以调用(是否是个方法)
```

定义两个测试类

```Python
class Duck(object):
    def quack(self):
        pass


class NotDuck(object):
    quack = "foo"
```

判断是否是`AbstractDuck`的子类

```python
print(issubclass(Duck, AbstractDuck))  # 输出 True
print(issubclass(NotDuck, AbstractDuck))  # 输出 False
```

注意:`__subclasshook__`方法的优先级大于`register`

举个例子解释`NotImplemented`返回值

```python
In [6]: import abc                                                                                                                                   

In [7]: class AbstractDuck(metaclass=abc.ABCMeta): 
   ...:     @classmethod 
   ...:     def __subclasshook__(cls, subclass): 
   ...:         quack = getattr(subclass, 'quack', None)  # 取出subclass的 quack 属性,如果不存在则返回 None 
   ...:         if callable(quack): 
   ...:             return True 
   ...:         return NotImplemented 
   ...:                                                                                                                                                                                                                                                                                   

In [8]: class Duck(object): 
   ...:     def quack(self): 
   ...:         pass 
   ...:                                                                                                                                              

In [9]: class NotDuck(object): 
   ...:     quack = "foo" 
   ...:                                                                                                                                                                                                                                                           

In [10]: issubclass(NotDuck, AbstractDuck)                                                                                                           
Out[10]: False

In [11]: AbstractDuck.register(NotDuck)                                                                                                              
Out[11]: __main__.NotDuck

In [12]: issubclass(NotDuck, AbstractDuck)                                                                                                           
Out[12]: True
```



**说明：**

- `isinstance(param, AbstractClass)`执行的时候会调用`__subclasshook__`
- `issubclass(param, AbstractClass)`执行的时候会调用`__subclasshook__`
- 此时的AbstractClass还是可以实例化的，他还不是真正意义上的



```python
import abc


class AbstractDuck(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        print('通过isinstance 或者 issubclass 方法进入')
        quack = getattr(subclass, 'quack', None)  # 取出subclass的 quack 属性,如果不存在则返回 None
        return callable(quack)  # 返回quack是否可以调用(是否是个方法)


class LikeDuck(object):

    def quack(self):
        pass


class NotLikeDuck(object):

    def xxx(self):
        pass


print(isinstance(LikeDuck, AbstractDuck))
print(isinstance(LikeDuck(), AbstractDuck))
print(issubclass(LikeDuck, AbstractDuck))

print(isinstance(NotLikeDuck, AbstractDuck))
print(isinstance(NotLikeDuck(), AbstractDuck))
print(issubclass(NotLikeDuck, AbstractDuck))
```





## 五、抽象基类用于模板设计



#### 1. 前言

在《抽象基类（ABC）》中，基于C++讲述抽象基类。尽管Python设计上以鸭子类型为主，但仍有抽象基类（ABC）的一席之地，它被封装在了abc模块中供程序员使用。

`abc`模块有以下两个主要功能：

- 某种情况下，判定某个对象的类型，如：`isinstance(a, Sized)`,如上面所讲
- 强制子类必须实现某些方法，即ABC类的派生类







```python
import abc


class AbstractDuck(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        print('通过isinstance 或者 issubclass 方法进入')
        quack = getattr(subclass, 'quack', None)  # 取出subclass的 quack 属性,如果不存在则返回 None
        return callable(quack)  # 返回quack是否可以调用(是否是个方法)

    @abc.abstractmethod
    def quack(self):
        pass

class LikeDuck(AbstractDuck):

    def quack(self):
        pass


class NotLikeDuck(AbstractDuck):

    def xxx(self):
        pass

if __name__ == '__main__':
    LikeDuck()
    NotLikeDuck()
```

解释器如期抛错：

```bash
TypeError: Can't instantiate abstract class A with abstract methods greet
```

这是因为AbstractClass类现在就是一个抽象基类了，不可以被实例化，同时，它的子类还必须实现quack()方法，否则实例化子类时解释器也要报错：

所以在我们进行模块设计的时候，对于一些要实现的方法，我们可以这样操作



## 六、其他基类

abc模块中还有实现了其他抽象基类，可以用来判断类型或是继承方法，这里不做详述了

```
__all__ = ["Awaitable", "Coroutine",
           "AsyncIterable", "AsyncIterator", "AsyncGenerator",
           "Hashable", "Iterable", "Iterator", "Generator", "Reversible",
           "Sized", "Container", "Callable", "Collection",
           "Set", "MutableSet",
           "Mapping", "MutableMapping",
           "MappingView", "KeysView", "ItemsView", "ValuesView",
           "Sequence", "MutableSequence",
           "ByteString",
           ]
```

通过`from collections import Iterable`的方式来查找，基本都是重写了`__subclasshook__`方法



## 七、总结

- 对抽象基类来说，需要用到装饰器 **@abc.abstractmethod**；
- 对于鸭子类型来说，需要重写`__subclasshook__`魔法方法。
- 也可以都弄



