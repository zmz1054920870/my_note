# 生成器

#### 概念：

```
如果一个 def 的主体包含 yield，这个函数会自动变成一个生成器（即使它包含一个 return），只有next()或者func().send(None)的时候生成器才会被激活，不然是不会执行里面的代码的
```



#### 一个简单的生成器

```python
def simple_generator_function():
    
    yield 1
   	yield 2
   	yield 3
    
a = simple_generator_function()
next(a)
next(a)
next(a)
```





#### 生成器实现斐波拉契数列

```python
class Generate(object):

    def __init__(self):
        self.a = 0
        self.b = 1

    # def __iter__(self):
    #     return self
    #
    # def __next__(self):
    #     self.a, self.b = self.b, self.a + self.b
    #     if self.a > 300:
    #         raise StopIteration
    #     return self.a

    def get_number(self):
        """
        next使yield执行一次发数据后，停止
        send使yield必须先执行一次收，然后执行一次发后停止
        """
        while True:
            self.a, self.b = self.b, self.a + self.b
            yield self.a
            if self.a > 300:
                raise StopIteration


count = 1

a = Generate().get_number()
for each in a:
    print(each)
```

> - ​	**生成器也是一个迭代器，可以直接在for循环中使用**
> - ​    **普通迭代器要做for循环中使用，必须定义`__iter__`,否则报错：说它非迭代器**
> - ​    **普通迭代器直接使用next的时候，不需要定义`__iter__`魔法方法。如果你要在for循环中使用，就必须要**
> - ​    **for循环会捕捉`StopIteration`异常**



#### 迭代器实现斐波拉契数列

```python
class Demo(object):

    def __init__(self):
        self.a = 1
        self.b = 1

    def __iter__(self):
        return self

    def __next__(self):
        self.b, self.a = self.a + self.b, self.b
        if self.b > 500:
            raise StopIteration
        return self.b

a = Demo()
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
# for i in a:
#     print(i)
```







#### 生成器解决素数问题（假如有超大体量）

```

```

