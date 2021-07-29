## 一、	hook和plugin的关系



**备注：hook和plugin是`1:N`的对应关系，假设同时注册了多个实现了同一hook的plugin，则会对应的返回多个结果。**

```python
from pluggy import PluginManager, HookspecMarker, HookimplMarker

hookspec = HookspecMarker("myPluggyDemo_2")
hookimpl = HookimplMarker("myPluggyDemo_2")


class HookSpec:
    @hookspec
    def calculate(self, a, b):
        pass


class HookImpl1:
    @hookimpl
    def calculate(self, a, b):
        return a + b


class HookImpl2:
    @hookimpl
    def calculate(self, a, b):
        return a * b
    

pm = PluginManager("myPluggyDemo_2")
pm.add_hookspecs(HookSpec)
pm.register(HookImpl1())
pm.register(HookImpl2())
print(pm.hook.calculate(a=2, b=3)
```

**Output**

```python
[6, 5]
```

**解析：**

- **在Demo2中，我们注册了两个`plugin`，`HookImpl1`和`HookImpl2`，分别实现了加法和乘法两个逻辑**
- **每次调用hook都会返回两个`plugin`执行的结果，先执行后注册的`HookImpl2`，再执行先注册的`HookImpl1`,即越晚注册的plugin越先执行。(后续会讲原因**





## 二、	Plugin的调用顺序与参数



#### 2.1	HookspecMarker装饰器参数

**HookspckMarker装饰器支持传入一些特定的参数，常用的有**

- **firstresult - 如果firstresult值为True时，获取第一个plugin执行结果后就停止（中断）继续执行。**

- **historic - 如果值为True时，表示这个hook是需要保存调用记录（call history）的，并将该调用记录回放在未来新注册的plugins上。**



**firstresult--Demo如下**

```python
from pluggy import PluginManager, HookspecMarker, HookimplMarker

hookspec = HookspecMarker("myPluggyDemo_3")
hookimpl = HookimplMarker("myPluggyDemo_3")


class HookSpec:
    @hookspec(firstresult=True)
    def calculate(self, a, b): 
        pass


class HookImpl1:
    @hookimpl
    def calculate(self, a, b):
        return a + b            #本例子中不会执行加法逻辑


class HookImpl2:
    @hookimpl
    def calculate(self, a, b):
        return a * b


pm = PluginManager("myPluggyDemo_3")
pm.add_hookspecs(HookSpec)
pm.register(HookImpl1())
pm.register(HookImpl2())
print(pm.hook.calculate(a=2, b=3))
```

**Output**

```python
6
```



#### 2.2	HookimplMarker装饰器参数

**HookimplMarker装饰器支持传入一些特定的参数，常用的有**

- **tryfirst - 如果tryfirst值为True，则此plugin会尽可能早的在1:N的实现链路执行**
- **trylast - 如果trylast值为True，则此plugin会相应地尽可能晚的在1:N的实现链中执行**
- **hookwrapper - 如果该参数为True，需要在plugin内实现一个yield，plugin执行时先执行wrapper plugin前面部分的逻辑，然后转去执行其他plugin，最后再回来执行wrapper plugin后面部分的逻辑。**
- **optionalhook - 如果该参数为True，在此plugin缺少相匹配的hook时，不会报error（spec is found）。**

**hookwrapper 的Demo如下**

{'hookwrapper': False， 'optionalhook': False, 'tryfirst': True, 'trylast': False}

```python
from pluggy import PluginManager, HookspecMarker, HookimplMarker

hookspec = HookspecMarker("myPluggyDemo_5")
hookimpl = HookimplMarker("myPluggyDemo_5")


class HookSpec:
    @hookspec
    def calculate(self, a, b):
        pass


class HookImpl1:
    @hookimpl
    def calculate(self, a, b):
        print('HookImpl1 execute!')
        return a + b


class HookImpl2:
    @hookimpl(tryfirst=True)
    def calculate(self, a, b):
        print('HookImpl2 execute!')
        return a * b


class WrapperPluggy:
    @hookimpl(hookwrapper=True)
    def calculate(self, a, b):
        print('WrapperPluggy execute!')
        print("Before yield")
        result = yield            #此处返回的值为其他两个pluggy执行的结果
        print(f"After yield,result is {result.get_result()}")
        return a * b + (a + b)	  #hookwrapper=True时候，这个值会被忽略	


pm = PluginManager("myPluggyDemo_5")
pm.add_hookspecs(HookSpec)
pm.register(HookImpl1())
pm.register(HookImpl2())
pm.register(WrapperPluggy())
print(pm.hook.calculate(a=2, b=3))
```

**Output**

```python
WrapperPluggy execute!
Before yield
HookImpl2 execute!
HookImpl1 execute!
After yield,result is [6, 5]
[6, 5]			# 三角形，WrapperPluggy的值没有被返回
```

**解析：**

- **`ImplWrapper`中的`pluggy`的代码逻辑，以`result = yield` 为分割线，分成两个部分。第一部分执行完毕后，中断继续执行，转去执行其他`plugin`，待其他`plugin`都执行完时，回来继续执行剩下的部分。**

- **`result = yield`result通过yield来获取到其他plugin执行的结果，即非`wrapper plugin`的执行结果（`HookImpl2`和`HookImpl1`）**

- **从Output中可以看出，我们`WrapperPluggy`的返回结果没有被打印出来，这是因为`wrapper plugin`的返回值会被`Ignore`，原因后续会提到**





```python
class _TagTracer(object):
    def __init__(self):
        self._tag2proc = {}
        self.writer = None
        self.indent = 0

    def get(self, name):
        return _TagTracerSub(self, (name,))
    ........
    
class _TagTracerSub(object):
    def __init__(self, root, tags):
        self.root = root	# root = class _TagTrancer
        self.tags = tags	# tags = ("pluginmanage", )

    def __call__(self, *args):
        self.root.processmessage(self.tags, args)

    def setmyprocessor(self, processor):
        self.root.setprocessor(self.tags, processor)

    def get(self, name):
        return self.__class__(self.root, self.tags + (name,))
	.........
    
class _HookRelay(object):
    """ hook holder object for performing 1:N hook calls where N is the number
    of registered plugins.

    """

    def __init__(self, trace):
        self._trace = trace	
```



```python
self.trace = _TagTracer().get('pluginmanage') = _TagTracerSub(root=_TagTracer, tags=(('pluginmanage', ))

                                                              
self.trace.root.get('hook') == _TagTracer().get('hook') 
class _TagTracerSub(object):
    def __init__(self, root, tags):
        self.root = root	# root = class _TagTrancer
        self.tags = tags	# tags = ("hook", )
                                                              
self.hook = _HookRelay(self.trace.root.get("hook")) --> <pluggy._HookRelay object at 0x000001CA31464CC0> {'_trace': <pluggy._TagTracerSub object at 0x000001CA315C6A20>}                                             
                                                              
                                                              
                                                              
结论： self.hook = _HookRelay(_TagTracerSub(root=_TagTrancer(), tags=('hook', )))
```





```
211 303 529 621 222 243 48
__call__ 157
self.trace ==
class _TagTracerSub(object):
    def __init__(self, root, tags):
        self.root = root	# root = class _TagTrancer
        self.tags = tags	# tags = ("pluginmanage", )

self.hook = _HookRelay(self.trace.root.get("hook")) = 




<pluggy._HookRelay object at 0x00000226A1385AC8> myhook -- 》 hc = _HookCaller(name=myhook, self._hookexec, module_or_class, spec_opts) -->setattr(self.hook, name, hc)
```

https://blog.csdn.net/qq_38959715/article/details/105627907



**class PluginManager(object):**

```python
class PluginManager(object):
    """ Core Pluginmanager class which manages registration
    of plugin objects and 1:N hook calling.

    You can register new hooks by calling ``add_hookspec(module_or_class)``.
    You can register plugin objects (which contain hooks) by calling
    ``register(plugin)``.  The Pluginmanager is initialized with a
    prefix that is searched for in the names of the dict of registered
    plugin objects.  An optional excludefunc allows to blacklist names which
    are not considered as hooks despite a matching prefix.

    For debugging purposes you can call ``enable_tracing()``
    which will subsequently send debug information to the trace helper.
    """

    def __init__(self, project_name, implprefix=None):
        """ if implprefix is given implementation functions
        will be recognized if their name matches the implprefix. """
        self.project_name = project_name
        self._name2plugin = {}
        self._plugin2hookcallers = {}
        self._plugin_distinfo = []
        self.trace = _TagTracer().get("pluginmanage")
        self.hook = _HookRelay(self.trace.root.get("hook"))
        self._implprefix = implprefix
        self._inner_hookexec = lambda hook, methods, kwargs: \
            hook.multicall(
                methods, kwargs,
                firstresult=hook.spec_opts.get('firstresult'),
            )

    def _hookexec(self, hook, methods, kwargs):
        # called from all hookcaller instances.
        # enable_tracing will set its own wrapping function at self._inner_hookexec
        # print('---_hookexec-----', hook, '****', methods, kwargs)
        return self._inner_hookexec(hook, methods, kwargs)

    def register(self, plugin, name=None):
        """ Register a plugin and return its canonical name or None if the name
        is blocked from registering.  Raise a ValueError if the plugin is already
        registered. """
        plugin_name = name or self.get_canonical_name(plugin)

        if plugin_name in self._name2plugin or plugin in self._plugin2hookcallers:
            if self._name2plugin.get(plugin_name, -1) is None:
                return  # blocked plugin, return None to indicate no registration
            raise ValueError("Plugin already registered: %s=%s\n%s" %
                             (plugin_name, plugin, self._name2plugin))

        # XXX if an error happens we should make sure no state has been
        # changed at point of return
        self._name2plugin[plugin_name] = plugin
        # register matching hook implementations of the plugin
        self._plugin2hookcallers[plugin] = hookcallers = []
        for name in dir(plugin):
            hookimpl_opts = self.parse_hookimpl_opts(plugin, name)  #   为了拿到{'hookwrapper': False， 'optionalhook': False, 'tryfirst': True, 'trylast': False} 这几个参数
            if hookimpl_opts is not None:
                normalize_hookimpl_opts(hookimpl_opts)  # 标准化参数设置默认值
                method = getattr(plugin, name)  # plugin == Plugin_1 , name == myhook
                hookimpl = HookImpl(plugin, plugin_name, method, hookimpl_opts)
                """
                plugin == Plugin_1(), 
                plugin_name = id(Plugin_1()) or xxx, 
                method == myhook, 
                hookimp_opts = {
                    'hookwrapper': False, 
                    'optionalhook': False, 
                    'tryfirst': True, 
                    'trylast': False
                }
                
                """

                hook = getattr(self.hook, name, None)
                if hook is None:
                    hook = _HookCaller(name, self._hookexec)
                    setattr(self.hook, name, hook)
                elif hook.has_spec():
                    self._verify_hook(hook, hookimpl)
                    hook._maybe_apply_history(hookimpl)
                hook._add_hookimpl(hookimpl)
                hookcallers.append(hook)
        return plugin_name
```





```python
def _multicall(hook_impls, caller_kwargs, firstresult=False):
    """Execute a call into multiple python functions/methods and return the
    result(s).

    ``caller_kwargs`` comes from _HookCaller.__call__().
    """
    # print('_multical', hook_impls, '*****', caller_kwargs, '*****', firstresult)
    __tracebackhide__ = True
    results = []
    excinfo = None
    try:  # run impl and wrapper setup functions in a loop
        teardowns = []
        try:
            for hook_impl in reversed(hook_impls):
                try:
                    args = [caller_kwargs[argname] for argname in hook_impl.argnames]
                except KeyError:
                    for argname in hook_impl.argnames:
                        if argname not in caller_kwargs:
                            raise HookCallError(
                                "hook call must provide argument %r" % (argname,))

                if hook_impl.hookwrapper:
                    try:
                        gen = hook_impl.function(*args)
                        next(gen)   # first yield
                        teardowns.append(gen)
                    except StopIteration:
                        _raise_wrapfail(gen, "did not yield")
                else:
                    res = hook_impl.function(*args)
                    if res is not None:
                        results.append(res)
                        if firstresult:  # halt further impl calls
                            break
        except BaseException:
            excinfo = sys.exc_info()
    finally:
        if firstresult:  # first result hooks return a single value
            outcome = _Result(results[0] if results else None, excinfo)
        else:
            outcome = _Result(results, excinfo)

        # run all wrapper post-yield blocks
        for gen in reversed(teardowns):
            try:
                gen.send(outcome)
                _raise_wrapfail(gen, "has second yield")
            except StopIteration:
                pass

        return outcome.get_result()
```





```
self.hook = _HookRelay()
```











### 三、例子

#### 3.1	class方式定义

```python
import pluggy

# 创建插件规范类装饰器
hookspac = pluggy.HookspecMarker('example')
# 创建插件类装饰器
hookimpl = pluggy.HookimplMarker('example')


class MySpec(object):
    # 创建插件规范
    @hookspac
    def myhook(self, a, b=20):
        pass


class Plugin_1(object):
    # 定义插件
    @hookimpl(tryfirst=True)
    def myhook(self, a, b=10):
        return a + b


class Plugin_2(object):
    @hookimpl(tryfirst=True)
    def myhook(self, a, b=5):
        return a - b


# 创建manger和添加hook规范
pm = pluggy.PluginManager('example')
pm.add_hookspecs(MySpec)

# 注册插件
pm.register(Plugin_1(), name='myhook_01')
pm.register(Plugin_2())

# 调用插件中的myhook方法
results = pm.hook.myhook(a=10)
print(results)
```

**备注：**

- **后注册的结果先返回**
- **都定义了tryfirst=True,那就没有优先级了，谁最后注册，最先执行**





#### 3.2	module定义

```python
# src/api_case/接口脚本/demo_imp.py

import pluggy

hookimp = pluggy.HookimplMarker('example')
@hookimp
def myhook(a, b):
    return a + b
```



```python
# src/api_case/接口脚本/demo_spec.py

import pluggy

hookspec = pluggy.HookspecMarker('example')
@hookspec
def myhook(a, b):
    pass
```



```python
# src/api_case/接口脚本/demo_m.py

import pluggy

from src.api_case.接口脚本 import demo_spec
from src.api_case.接口脚本 import demo_imp

pm = pluggy.PluginManager('example')
pm.add_hookspecs(demo_spec)
pm.register(demo_imp)
results = pm.hook.myhook(a=10, b=2)
print(results)
```

