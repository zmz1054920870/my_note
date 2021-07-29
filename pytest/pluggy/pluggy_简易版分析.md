老规矩，在开始分析前，希望自己搞清楚的几个问题：

- \1. 如何使用 pluggy？
- \2. 插件代码如何做到灵活可插拔的？
- \3. 外部系统如何调用插件逻辑？

随着分析的进行会有新的问题抛出，问题可以帮助我们理清目的，避免迷失在源码中。

## **整体把控**

pluggy 插件系统与我此前研究的 python 插件系统不同，pluggy 不可以动态插入，即无法在程序运行的过程中利用插件添加新的功能。

pluggy 主要有 3 个概念：

- 1.PluginManager：用于管理插件规范与插件本身
- 2.HookspecMarker：定义插件调用规范，每个规范可以对应 1~N 个插件，每个插件都满足该规范，否则无法成功被外部调用
- 3.HookimplMarker：定义插件，插件逻辑具体的实现在该类装饰的方法中

简单使用一下，代码如下。

```python
import pluggy
# 创建插件规范类装饰器
hookspac = pluggy.HookspecMarker('example')
# 创建插件类装饰器
hookimpl = pluggy.HookimplMarker('example')

class MySpec(object):
    # 创建插件规范
    @hookspac
    def myhook(self, a, b):
        pass

class Plugin_1(object):
    # 定义插件
    @hookimpl
    def myhook(self, a, b):
        return a + b

class Plugin_2(object):
    @hookimpl
    def myhook(self, a, b):
        return a - b

# 创建manger和添加hook规范
pm = pluggy.PluginManager('example')
pm.add_hookspecs(MySpec)

# 注册插件
pm.register(Plugin_1())
pm.register(Plugin_2())

# 调用插件中的myhook方法
results = pm.hook.myhook(a=10, b=20)
print(results)
```

整段代码简单而言就是创建相应的类装饰器装饰类中的方法，通过这些类装饰器构建出了插件规范与插件本身。

首先，实例化 PluginManager 类，实例化时需要传入全局唯一的 project name，HookspecMarker 类与 HookimplMarker 类的实例化也需要使用相同的 project name。

创建完插件管理器后，通过 add_hookspecs 方法添加插件规范、通过 register 方法添加插件本身则可。

添加完插件调用规范与插件本身后，就可以通过插件管理器的 hook 属性直接调用插件了。

阅读到这里，关于问题「1，2，3」便有了答案。

pluggy 使用的过程可以分为 4 步：

- \1. 通过 HookspecMarker 类装饰器定义插件调用规范
- \2. 通过 HookimplMarker 类装饰器定义插件逻辑
- \3. 创建 PluginManager 并绑定插件调用规范与插件本身
- \4. 调用插件

通过类装饰器与 PluginManager.add_hookspecs、PluginManager.register 方法的配合，轻松实现插件的可插拔操作，其背后原理其实就是被类装饰器装饰后的方法会被动态添加上新的属性信息，而对应的 add_hookspecs 与 register 等方法会根据这些属性信息来判断是否为插件规范或插件本身。

想要在外部系统中使用插件，只需要调用 pm.hook.any_hook_function 方法则可，任意注册了插件都可以被轻松调用。

但这里引出了新的问题：

- \4. 类装饰器是如何将某个类中的方法设置成插件的？
- 5.pluggy 是如何关联插件规范与插件本身的？
- \6. 插件中的逻辑具体是如何被调用的？

这三个问题关注的是实现细节，下面进一步步进行分析。

## **hookspac 与 hookimpl 装饰器的作用**

代码中，使用了 hookspac 类装饰器定义出插件调用规范，使用了 hookimpl 类装饰器定义出插件本身，两者的作用其实就是「为被装饰的方法添加新的属性」。因为两者逻辑相似，所以这里就只分析 hookspac 类装饰器代码，代码如下：

```python
class HookspecMarker(object):
  

    def __init__(self, project_name):
        self.project_name = project_name
    def __call__(
        self, function=None, firstresult=False, historic=False, warn_on_impl=None
    ):

        def setattr_hookspec_opts(func):
            if historic and firstresult:
                raise ValueError("cannot have a historic firstresult hook")
            # 为被装饰的方法添加新的属性
            setattr(
                func,
                self.project_name + "_spec",
                dict(
                    firstresult=firstresult,
                    historic=historic,
                    warn_on_impl=warn_on_impl,
                ),
            )
            return func

        if function is not None:
            return setattr_hookspec_opts(function)
        else:
            return setattr_hookspec_opts
```

类装饰器主要会重写类的`__call__`方法，上述代码中`__call__`方法最核心的逻辑便是使用 setattr 方法为被装饰的 func 方法添加新的属性，属性名为当前 project name 加上_spec 后缀，而属性的值为一个字典对象。

在调用 PluginManager.add_hookspecs 方法时会利用 hookspac 类装饰器添加的信息

HookimplMarker 类类似，只是添加的属性有所不同，核心代码如下。

```python
setattr(
    func,
    self.project_name + "_impl",
    dict(
        hookwrapper=hookwrapper,
        optionalhook=optionalhook,
        tryfirst=tryfirst,
        trylast=trylast,
        specname=specname,
    ),
)
```

所以关于「4. 类装饰器是如何将某个类中的方法设置成插件的？」，其实就是利用 setattr 方法为当前方法设置新的属性，这些属性相当于提供了一种信息，PluginManager 会根据这些信息判断该方法是不是插件，跟下面例子本质相同。

```python
In [1]: def fuc1():
   ...:     print('hh')
   ...:

In [2]: setattr(fuc1, 'fuc1' + '_impl', dict(a=1, b=2))

In [3]: fuc1.fuc1_impl
Out[3]: {'a': 1, 'b': 2}
```

## **添加插件规范与注册插件的背后**

实例化 pluggy.PluginManager 类后便可以通过 add_hookspecs 方法添加插件规范与 register 方法注册插件。

要搞清楚「pluggy 是如何关联插件规范与插件本身的？」，就需要深入它们的源码。

实例化 PluginManager 类，其实就是调用它的`__init__`方法。

```python
    def __init__(self, project_name, implprefix=None):
        """If ``implprefix`` is given implementation functions
        will be recognized if their name matches the ``implprefix``. """
        self.project_name = project_name
        # ...省略部分...
        # 关键
        self.hook = _HookRelay()
        self._inner_hookexec = lambda hook, methods, kwargs: hook.multicall(
            methods,
            kwargs,
            firstresult=hook.spec.opts.get("firstresult") if hook.spec else False,
        )
```

关键在于定义了 self.hook 属性与 self._inner_hookexec 属性，它是一个匿名方法，会接收 hook、methods、kwargs 三个参数并将这些参数传递给 hook.multicall 方法。

随后调用 add_hookspecs 方法添加插件规范，其代码如下。

```python
class PluginManager(object):

    # 获取被装饰方法中对应属性的信息（HookspecMarker装饰器添加的信息）
    def parse_hookspec_opts(self, module_or_class, name):
        method = getattr(module_or_class, name)
        return getattr(method, self.project_name + "_spec", None)
        
    def add_hookspecs(self, module_or_class):
        names = []
        for name in dir(module_or_class):
            # 获取插件规范信息
            spec_opts = self.parse_hookspec_opts(module_or_class, name)
            if spec_opts is not None:
                hc = getattr(self.hook, name, None)
                if hc is None:
                    
                    hc = _HookCaller(name, self._hookexec, module_or_class, spec_opts)
                    setattr(self.hook, name, hc)
                # ...省略部分代码...
```

上述代码中通过 parse_hookspec_opts 方法获取方法中相应属性的参数，如果参数不为 None 那么则获取_HookRelay 类中的被装饰方法的信息（该方法就是 MySpec 类的 myhook），从源码中可以发现_HookRelay 类其实是空类，它存在的意义其实就是接收新的属性，分析到后面你就会发现_HookRelay 类其实就是用于连接插件规范与插件本身的类。

如果_HookRelay 类中没有 myhook 属性信息，则实例化_HookCaller 类并将其作为 self.hook 的属性，具体而言，就是将_HookCaller 类的实例作为_HookRelay 类中 myhook 属性的值。

_HookCaller 类很重要，其部分代码如下。

```python
class _HookCaller(object):
    def __init__(self, name, hook_execute, specmodule_or_class=None, spec_opts=None):
        self.name = name
        # ...省略...
        self._hookexec = hook_execute
        self.spec = None
        if specmodule_or_class is not None:
            assert spec_opts is not None
            self.set_specification(specmodule_or_class, spec_opts)

    def has_spec(self):
        return self.spec is not None

    def set_specification(self, specmodule_or_class, spec_opts):
        assert not self.has_spec()
        self.spec = HookSpec(specmodule_or_class, self.name, spec_opts)
        if spec_opts.get("historic"):
            self._call_history = []
```

关键在于 set_specification 方法，该方法会实例化 HookSpec 类并将其复制给 self.spec。

至此，插件规范就添加完了，紧接着通过 register 方法注册插件本身，其核心代码如下。

```python
    def register(self, plugin, name=None):
        # 省略部分代码
        for name in dir(plugin):
            hookimpl_opts = self.parse_hookimpl_opts(plugin, name)
            if hookimpl_opts is not None:
                normalize_hookimpl_opts(hookimpl_opts)
                method = getattr(plugin, name)
                # 实例化插件
                hookimpl = HookImpl(plugin, plugin_name, method, hookimpl_opts)
                name = hookimpl_opts.get("specname") or name
                hook = getattr(self.hook, name, None) # 获取 hookspec 插件规范
                if hook is None:
                    hook = _HookCaller(name, self._hookexec)
                    setattr(self.hook, name, hook)
                elif hook.has_spec():
                    # 检查插件方法的方法名与参数是否与插件规范相同
                    self._verify_hook(hook, hookimpl)
                    hook._maybe_apply_history(hookimpl)
                # 添加到插件规范中，完成插件与插件规范的绑定
                hook._add_hookimpl(hookimpl)
                hookcallers.append(hook)
```

首先通过 self.parse_hookimpl_opts 方法获取被 hookimpl 装饰器添加的信息，随后通过 getattr (plugin, name) 方法获取方法名，其实就是 myhook，最后初始化 HookImpl 类，其实就是插件本身，并将其与对应的插件规范绑定，通过_add_hookimpl 方法实现这一目的。

_add_hookimpl 方法会根据 hookimpl 实例中的属性判断其插入的位置，不同位置，调用顺序不同，代码如下。

```python
    def _add_hookimpl(self, hookimpl):
        """Add an implementation to the callback chain.
        """
        # 是否有 包装器 (即插件逻辑中使用了yield关键字)
        if hookimpl.hookwrapper:
            methods = self._wrappers
        else:
            methods = self._nonwrappers
        # 先调用还是后代码
        if hookimpl.trylast:
            methods.insert(0, hookimpl)
        elif hookimpl.tryfirst:
            methods.append(hookimpl)
        else:
            # find last non-tryfirst method
            i = len(methods) - 1
            while i >= 0 and methods[i].tryfirst:
                i -= 1
            methods.insert(i + 1, hookimpl)      
```

至此「5.pluggy 是如何关联插件规范与插件本身的？」的问题也是明白了，简单而言，插件规范与插件本身都被装饰器添加了特殊信息，通过这些特殊信息将两者找到并分布利用这些属性的值初始化_HookCaller 类（插件规范）与 HookImpl 类（插件本身），最后通过_add_hookimpl 方法完成绑定。

## **插件中的逻辑具体是如何被调用的？**

从一开始的示例代码中，可以发现，调用 myhook 插件方法通过 `pm.hook.myhook(a=10, b=20)` 方法则可。

背后是什么？

PluginManager.hook 其实就是_HookRelay 类，而_HookRelay 类模式是一个空类，通过 add_hookspecs 方法与 register 方法的操作，_HookRelay 类中多了名为 myhook 的属性，该属性对应着_HookCaller 类实例。

pm.hook.myhook (a=10, b=20) 其实就是调用`_HookCaller.__call__`，代码如下。

```python
    def __call__(self, *args, **kwargs):
        # 省略部分代码
        if self.spec and self.spec.argnames:
            # 计算插件规范中可以接收的参数与插件本身可以接收的参数是否相同
            notincall = (
                set(self.spec.argnames) - set(["__multicall__"]) - set(kwargs.keys())
            )
            if notincall:
                # 省略代码
        # 调用方法
        return self._hookexec(self, self.get_hookimpls(), kwargs)
```

`__call__`方法的主要就是判断插件规范与插件本身是否匹配，然后通过 self._hookexec 方法去真正的执行。

通过分析，完整的调用链条为：`_HookCaller._hookexec` -> `PluginManager._inner_hookexec` -> `_HookCaller.multicall` -> `callers文件的中的_multicall方法`

_multicall 方法中最关键的代码片段如下。

```python
def _multicall(hook_impls, caller_kwargs, firstresult=False):
            for hook_impl in reversed(hook_impls):
                try:
                    # 调用myhook方法
                    args = [caller_kwargs[argname] for argname in hook_impl.argnames]
                # 省略代码
                
                # 如果插件中使用了yeild，则通过这种方式调用
                if hook_impl.hookwrapper:
                   try:
                       gen = hook_impl.function(*args)
                       next(gen)  # first yield
                       teardowns.append(gen)
                   except StopIteration:
                       _raise_wrapfail(gen, "did not yield")
```

至此，pluggy 的核心逻辑就撸完了。



```
<class '__main__.MySpac'> __class__
<class '__main__.MySpac'> __delattr__
<class '__main__.MySpac'> __dict__
<class '__main__.MySpac'> __dir__
<class '__main__.MySpac'> __doc__
<class '__main__.MySpac'> __eq__
<class '__main__.MySpac'> __format__
<class '__main__.MySpac'> __ge__
<class '__main__.MySpac'> __getattribute__
<class '__main__.MySpac'> __gt__
<class '__main__.MySpac'> __hash__
<class '__main__.MySpac'> __init__
<class '__main__.MySpac'> __init_subclass__
<class '__main__.MySpac'> __le__
<class '__main__.MySpac'> __lt__
<class '__main__.MySpac'> __module__
<class '__main__.MySpac'> __ne__
<class '__main__.MySpac'> __new__
<class '__main__.MySpac'> __reduce__
<class '__main__.MySpac'> __reduce_ex__
<class '__main__.MySpac'> __repr__
<class '__main__.MySpac'> __setattr__
<class '__main__.MySpac'> __sizeof__
<class '__main__.MySpac'> __str__
<class '__main__.MySpac'> __subclasshook__
<class '__main__.MySpac'> __weakref__
<class '__main__.MySpac'> myhook

['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'myhook']
```



```
 324
 def parse_hookspec_opts(self, module_or_class, name):
        print(module_or_class, name)
        method = getattr(module_or_class, name)
        print('method', method)
        return getattr(method, self.project_name + "_spec", None)
```

https://blog.csdn.net/qq_38959715/article/details/105627762?utm_medium=distribute.pc_relevant.none-task-blog-baidujs_title-1&spm=1001.2101.3001.4242





