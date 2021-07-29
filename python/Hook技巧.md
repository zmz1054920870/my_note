## python的Hook技巧

https://blog.csdn.net/Yimicaolor/article/details/100101101?ops_request_misc=&request_id=&biz_id=102&utm_term=python%20hook%E6%95%99%E7%A8%8B_%E8%AF%A6%E8%A7%A3Python%E5%BC%80%E5%8F%91&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-2-100101101.first_rank_v2_pc_rank_v29&spm=1018.2226.3001.4187

#### **Monkey Patch** 的方式 进行添加

```python
class A(object):

    def __init__(self, name):
        self.name = name

def speak(self):
    print("添加一个speak方法")
    print(self.name)
    
A.speak = speak
a = A("张三")
a.speak()
>>>添加一个speak方法
>>>张三

#解释: 因为类里面的方法都类的属性，我们通过属性添加的方式来扩展类，这不久相当于把我们的 speak方法挂钩到类A上面了？
```



#### decorator 修饰器的方式来HOOK

```python
def something(a,b): 
   def new_func(func):
      def wrap(*args,**kargv): 
         print("a") 
         func(*args,**kargv) 
         print("b")
      return wrap 
   return new_func
   
@something(1,2)
def func(a,b): 
   pass
```



#### 还有函数的魔法方法,比如__getattr__

```python
class C(object):
    a = 'abc'
    def __getattribute__(self, *args, **kwargs):
        print("__getattribute__() is called")
        return object.__getattribute__(self, *args, **kwargs)
    def __getattr__(self, name):
        print("__getattr__() is called")
        return name

c = C()
c.a
c.aa
>>> __getattribute__() is called
>>> __getattribute__() is called
>>> __getattr__() is called

# 解释:可以看到，访问已有属性a时，__getattribute__被调用，访问未定义的属性aa时__getattribute__先被调用，接着__getattr__被调用， 我们可以在__getattr__定义一些方法，来进行拓展，还有很多的魔法方法可以来进行HOOK
```





#### 高级HOOK技巧

```

import time
 
class LazyPerson(object):
  def __init__(self, name):
    self.name = name
    self.watch_tv_func = None
    self.have_dinner_func = None
 
  def get_up(self):
    print("%s get up at:%s" % (self.name, time.time()))
 
  def go_to_sleep(self):
    print("%s go to sleep at:%s" % (self.name, time.time()))
 
  def register_tv_hook(self, watch_tv_func):
    self.watch_tv_func = watch_tv_func
 
  def register_dinner_hook(self, have_dinner_func):
    self.have_dinner_func = have_dinner_func
 
  def enjoy_a_lazy_day(self):
 
    # get up
    self.get_up()
    time.sleep(3)
    # watch tv
    # check the watch_tv_func(hooked or unhooked)
    # hooked
    if self.watch_tv_func is not None:
      self.watch_tv_func(self.name)
    # unhooked
    else:
      print("no tv to watch")
    time.sleep(3)
    # have dinner
    # check the have_dinner_func(hooked or unhooked)
    # hooked
    if self.have_dinner_func is not None:
      self.have_dinner_func(self.name)
    # unhooked
    else:
      print("nothing to eat at dinner")
    time.sleep(3)
    self.go_to_sleep()
 
def watch_daydayup(name):
  print("%s : The program ---day day up--- is funny!!!" % name)
 
def watch_happyfamily(name):
  print("%s : The program ---happy family--- is boring!!!" % name)
 
def eat_meat(name):
  print("%s : The meat is nice!!!" % name)
 
 
def eat_hamburger(name):
  print("%s : The hamburger is not so bad!!!" % name)
 
 
if __name__ == "__main__":
  lazy_tom = LazyPerson("Tom")
  lazy_jerry = LazyPerson("Jerry")
  # register hook
  lazy_tom.register_tv_hook(watch_daydayup)
  lazy_tom.register_dinner_hook(eat_meat)
  lazy_jerry.register_tv_hook(watch_happyfamily)
  lazy_jerry.register_dinner_hook(eat_hamburger)
  # enjoy a day
  lazy_tom.enjoy_a_lazy_day()
```

