**镇文链接：https://www.cnblogs.com/yoyoketang/tag/pytest/default.html?page=4**

# [pytest文档5-fixture之conftest.py](https://www.cnblogs.com/yoyoketang/p/9390073.html)

前言

前面一篇讲到用例加setup和teardown可以实现在测试用例之前或之后加入一些操作，但这种是整个脚本全局生效的，如果我想实现以下场景：
用例1需要先登录，用例2不需要登录，用例3需要先登录。很显然这就无法用setup和teardown来实现了。这就是本篇学习的目的，自定义测试用例的预置条件

#### fixture优势

1.firture相对于setup和teardown来说应该有以下几点优势

- 命名方式灵活，不局限于setup和teardown这几个命名
- conftest.py 配置里可以实现数据共享，不需要import就能自动找到一些配置
- scope="module" 可以实现多个.py跨文件共享前置, 每一个.py文件调用一次
- scope="session" 以实现多个.py跨文件使用一个session来完成多个用例

```
fixture(scope="function", params=None, autouse=False, ids=None, name=None):
    """使用装饰器标记fixture的功能
     ** 作者：上海-悠悠 QQ交流群：588402570**
     可以使用此装饰器（带或不带参数）来定义fixture功能。 fixture功能的名称可以在以后使用
     引用它会在运行测试之前调用它：test模块或类可以使用pytest.mark.usefixtures（fixturename标记。 
     测试功能可以直接使用fixture名称作为输入参数，在这种情况下，夹具实例从fixture返回功能将被注入。

    :arg scope: scope 有四个级别参数 "function" (默认), "class", "module" or "session".

    :arg params: 一个可选的参数列表，它将导致多个参数调用fixture功能和所有测试使用它

    :arg autouse:  如果为True，则为所有测试激活fixture func 可以看到它。 如果为False（默认值）则显式需要参考来激活fixture

    :arg ids: 每个字符串id的列表，每个字符串对应于params 这样他们就是测试ID的一部分。 如果没有提供ID它们将从params自动生成

    :arg name:   fixture的名称。 这默认为装饰函数的名称。 如果fixture在定义它的同一模块中使用，夹具的功能名称将被请求夹具的功能arg遮蔽; 解决这个问题的一种方法是将装饰函数命名
                       “fixture_ <fixturename>”然后使用”@ pytest.fixture（name ='<fixturename>'）“”。
```

**Fixtures可以选择使用`yield`语句为测试函数提供它们的值，而不是`return`。 在这种情况下，`yield`语句之后的代码块作为拆卸代码执行，而不管测试结果如何。fixture功能必须只产生一次**

#### fixture参数传入（scope="function"）

1.实现场景：用例1需要先登录，用例2不需要登录，用例3需要先登录

```python
# 新建一个文件test_fixt.py
# coding:utf-8

import pytest

# 不带参数时默认scope="function"
@pytest.fixture()
def login():
    print("输入账号，密码先登录")

def test_s1(login):
    print("用例1：登录之后其它动作111")

def test_s2():  # 不传login
    print("用例2：不需要登录，操作222")

def test_s3(login):
    print("用例3：登录之后其它动作333")

if __name__ == "__main__":
    pytest.main(["-s", "test_fix.py"])
```

运行结果：

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO, inifile:
collected 3 items

test_fix.py 输入账号，密码先登录
用例1：登录之后其它动作111
.用例2：不需要登录，操作222
.输入账号，密码先登录
用例3：登录之后其它动作333
.

========================== 3 passed in 0.06 seconds ===========================
```

2.如果@pytest.fixture()里面没有参数，那么默认scope="function"，也就是此时的级别的function，针对函数有效

#### conftest.py配置

1.上面一个案例是在同一个.py文件中，多个用例调用一个登陆功能，如果有多个.py的文件都需要调用这个登陆功能的话，那就不能把登陆写到用例里面去了。
此时应该要有一个配置文件，单独管理一些预置的操作场景，pytest里面默认读取conftest.py里面的配置

conftest.py配置需要注意以下点：

- conftest.py配置脚本名称是固定的，不能改名称
- conftest.py与运行的用例要在同一个pakage下，并且有__init__.py文件
- 不需要import导入 conftest.py，pytest用例会自动查找

2.参考脚本代码设计如下

```python
** 作者：上海-悠悠 QQ交流群：588402570**
__init__.py

conftest.py
    # coding:utf-8
    import pytest

    @pytest.fixture()
    def login():
        print("输入账号，密码先登录")

test_fix1.py
    # coding:utf-8
    import pytest
    
    def test_s1(login):
        print("用例1：登录之后其它动作111")
    
    def test_s2():  # 不传login
        print("用例2：不需要登录，操作222")
    
    def test_s3(login):
        print("用例3：登录之后其它动作333")
    
    if __name__ == "__main__":
        pytest.main(["-s", "test_fix1.py"])

test_fix2.py
    # coding:utf-8
    import pytest
    
    def test_s4(login):
        print("用例4：登录之后其它动作111")
    
    def test_s5():  # 不传login
        print("用例5：不需要登录，操作222")
    
    if __name__ == "__main__":
        pytest.main(["-s", "test_fix2.py"])
```

3.单独运行test_fix1.py和test_fix2.py都能调用到login()方法，这样就能实现一些公共的操作可以单独拿出来了





# 前言

上一篇讲到fixture通过scope参数控制setup级别，既然有setup作为用例之前前的操作，用例执行完之后那肯定也有teardown操作。
这里用到fixture的teardown操作并不是独立的函数，用yield关键字呼唤teardown操作

# scope="module"

1.fixture参数scope="module"，module作用是整个.py文件都会生效，用例调用时，参数写上函数名称就行

```python
# 新建一个文件test_f1.py
# coding:utf-8
import pytest


@pytest.fixture(scope="module")
def open():
    print("打开浏览器，并且打开百度首页")

def test_s1(open):
    print("用例1：搜索python-1")

def test_s2(open):
    print("用例2：搜索python-2")

def test_s3(open):
    print("用例3：搜索python-3")

if __name__ == "__main__":
    pytest.main(["-s", "test_f1.py"])
```

运行结果：

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\, inifile:
collected 3 items

..\..\..\..\..\..\YOYO\test_f1.py 打开浏览器，并且打开百度首页
用例1：搜索python-1
.用例2：搜索python-2
.用例3：搜索python-3
.

========================== 3 passed in 0.01 seconds ===========================
```

**从结果看出，虽然test_s1,test_s2,test_s3三个地方都调用了open函数，但是它只会在第一个用例前执行一次**

2.如果test_s1不调用,test_s2（调用open）,test_s3不调用，运行顺序会是怎样的？

```
# 新建一个文件test_f1.py
# coding:utf-8
import pytest
'''
** 作者：上海-悠悠 QQ交流群：588402570**
'''

@pytest.fixture(scope="module")
def open():
    print("打开浏览器，并且打开百度首页")

def test_s1():
    print("用例1：搜索python-1")

def test_s2(open): 
    print("用例2：搜索python-2")

def test_s3():
    print("用例3：搜索python-3")

if __name__ == "__main__":
    pytest.main(["-s", "test_f1.py"])
```

运行结果：

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\, inifile:
collected 3 items

..\..\..\..\..\..\YOYO\test_f1.py 用例1：搜索python-1
.打开浏览器，并且打开百度首页
用例2：搜索python-2
.用例3：搜索python-3
.

========================== 3 passed in 0.01 seconds ===========================
```

**从结果看出，module级别的fixture在当前.py模块里，只会在用例（test_s2）第一次调用前执行一次**

#### yield执行teardown

1.前面讲的是在用例前加前置条件，相当于setup,既然有setup那就有teardown,fixture里面的teardown用yield来唤醒teardown的执行

```
# 新建一个文件test_f1.py
# coding:utf-8
import pytest
'''
** 作者：上海-悠悠 QQ交流群：588402570**
'''

@pytest.fixture(scope="module")
def open():
    print("打开浏览器，并且打开百度首页")

    yield
    print("执行teardown!")
    print("最后关闭浏览器")

def test_s1(open):
    print("用例1：搜索python-1")

def test_s2(open):
    print("用例2：搜索python-2")

def test_s3(open):
    print("用例3：搜索python-3")

if __name__ == "__main__":
    pytest.main(["-s", "test_f1.py"])
```

运行结果：

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\, inifile:
collected 3 items

..\..\..\..\..\..\YOYO\test_f1.py 打开浏览器，并且打开百度首页
用例1：搜索python-1
.用例2：搜索python-2
.用例3：搜索python-3
.执行teardown!
最后关闭浏览器


========================== 3 passed in 0.01 seconds ===========================
```

#### yield遇到异常

1.如果其中一个用例出现异常，不影响yield后面的teardown执行,运行结果互不影响，并且全部用例执行完之后，yield呼唤teardown操作

```
# 新建一个文件test_f1.py
# coding:utf-8
import pytest
'''
** 作者：上海-悠悠 QQ交流群：588402570**
'''

@pytest.fixture(scope="module")
def open():
    print("打开浏览器，并且打开百度首页")
    yield
    print("执行teardown!")
    print("最后关闭浏览器")

def test_s1(open):
    print("用例1：搜索python-1")

    # 如果第一个用例异常了，不影响其他的用例执行
    raise NameError  # 模拟异常

def test_s2(open):
    print("用例2：搜索python-2")

def test_s3(open):
    print("用例3：搜索python-3")

if __name__ == "__main__":
    pytest.main(["-s", "test_f1.py"])
```

运行结果：

```
\YOYO\test_f1.py 打开浏览器，并且打开百度首页
用例1：搜索python-1
F
open = None

    def test_s1(open):
        print("用例1：搜索python-1")
    
        # 如果第一个用例异常了，不影响其他的用例执行
>       raise NameError  # 模拟异常
E       NameError

D:\YOYO\test_f1.py:16: NameError
用例2：搜索python-2
.用例3：搜索python-3
.执行teardown!
最后关闭浏览器
```

2.如果在setup就异常了，那么是不会去执行yield后面的teardown内容了

3.yield也可以配合with语句使用，以下是官方文档给的案例

```
# 官方文档案例
# content of test_yield2.py

import smtplib
import pytest
'''
** 作者：上海-悠悠 QQ交流群：588402570**
'''

@pytest.fixture(scope="module")
def smtp():
    with smtplib.SMTP("smtp.gmail.com") as smtp:
        yield smtp  # provide the fixture value
```

#### addfinalizer终结函数

1.除了yield可以实现teardown,在request-context对象中注册addfinalizer方法也可以实现终结函数。

```
# 官方案例

# content of conftest.py
import smtplib
import pytest

@pytest.fixture(scope="module")
def smtp_connection(request):
    smtp_connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
    def fin():
        print("teardown smtp_connection")
        smtp_connection.close()
    request.addfinalizer(fin)
    return smtp_connection  # provide the fixture value
```

2.yield和addfinalizer方法都是在测试完成后呼叫相应的代码。

https://github.com/pytest-dev/pytest-html)



# [pytest文档7-pytest-html生成html报告](https://www.cnblogs.com/yoyoketang/p/9444463.html)

#### 前言

pytest-HTML是一个插件，pytest用于生成测试结果的HTML报告。兼容Python 2.7,3.6

#### pytest-html

1.github上源码地址[【https://github.com/pytest-dev/pytest-html】](https://github.com/pytest-dev/pytest-html)

2.pip安装

> $ pip install pytest-html

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180808181210381-1700741958.png)

3.执行方法

> $ pytest --html=report.html

#### html报告

1.打开cmd，cd到需要执行pytest用例的目录，执行指令：pytest --html=report.html

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180808181313106-139277619.png)

2.执行完之后，在当前目录会生成一个report.html的报告文件，显示效果如下

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180808181345337-349761673.png)

#### 指定报告路径

1.直接执行"pytest --html=report.html"生成的报告会在当前脚本的同一路径，如果想指定报告的存放位置，放到当前脚本的同一目录下的report文件夹里

> pytest --html=./report/report.html

** 作者：上海-悠悠 QQ交流群：588402570**

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180808195721554-2060958974.png)

2.如果想指定执行某个.py文件用例或者某个文件夹里面的所有用例，需加个参数。具体规则参考[【pytest文档2-用例运行规则】](https://www.cnblogs.com/yoyoketang/p/9362415.html)

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180808200223758-591259588.png)

#### 报告独立显示

1.上面方法生成的报告，css是独立的，分享报告的时候样式会丢失，为了更好的分享发邮件展示报告，可以把css样式合并到html里

> $ pytest --html=report.html --self-contained-html

** 作者：上海-悠悠 QQ交流群：588402570**

#### 显示选项

默认情况下，“ 结果”表中的所有行都将被展开，但具测试通过的行除外Passed。

可以使用查询参数自定义此行为：?collapsed=Passed,XFailed,Skipped。

#### 更多功能

1.更多功能查看官方文档[【https://github.com/pytest-dev/pytest-html】](https://github.com/pytest-dev/pytest-html)



# [pytest文档8-html报告报错截图+失败重跑](https://www.cnblogs.com/yoyoketang/p/9450309.html)

#### 前言

做web自动化的小伙伴应该都希望在html报告中展示失败后的截图，提升报告的档次，pytest-html也可以生成带截图的报告。

#### conftest.py

1.失败截图可以写到conftest.py文件里，这样用例运行时，只要检测到用例实例，就调用截图的方法，并且把截图存到html报告上

```
# conftest.py文件
# coding:utf-8

from selenium import webdriver
import pytest


driver = None

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    ** 作者：上海-悠悠 QQ交流群：588402570**
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_")+".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra

def _capture_screenshot():
    '''
    ** 作者：上海-悠悠 QQ交流群：588402570**
    截图保存为base64，展示到html中
    :return:
    '''
    return driver.get_screenshot_as_base64()


@pytest.fixture(scope='session', autouse=True)
def browser(request):
    global driver
    if driver is None:
        driver = webdriver.Firefox()

    def end():
        driver.quit()
    request.addfinalizer(end)
    return driver
```

2.用例部分如下：

```
# test_01.py文件

from selenium import webdriver
import time

#** 作者：上海-悠悠 QQ交流群：588402570**

def test_yoyo_01(browser):

    browser.get("https://www.cnblogs.com/yoyoketang/")
    time.sleep(2)
    t = browser.title
    assert t == "上海-悠悠"

# test_02.py文件

from selenium import webdriver
import time

# ** 作者：上海-悠悠 QQ交流群：588402570**

def test_yoyo_01(browser):

    browser.get("https://www.cnblogs.com/yoyoketang/")
    time.sleep(2)
    t = browser.title
    assert "上海-悠悠" in t
```

#### 报告展示

1.cmd打开，cd到用例的目录，执行指令

> $ pytest --html=report.html --self-contained-html

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180809182514040-696485338.png)

2.生成报告如下

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180809171919736-560333050.png)

#### 失败重试

失败重跑需要依赖pytest-rerunfailures插件，使用pip安装就行

> $ pip install pytest-rerunfailures

![img](https://images2018.cnblogs.com/blog/1070438/201809/1070438-20180910124324851-1546663309.png)

用例失败再重跑1次,命令行加个参数--reruns就行了

> $ py.test --reruns 1 --html=report.html --self-contained-html

![img](https://images2018.cnblogs.com/blog/1070438/201809/1070438-20180910124403634-969394154.png)

关于reruns参数的2个用法

```
re-run failing tests to eliminate flaky failures:
  --reruns=RERUNS       number of times to re-run failed tests. defaults to 0.
  --reruns-delay=RERUNS_DELAY
                        add time (seconds) delay between reruns.
```



# [pytest文档9-参数化parametrize](https://www.cnblogs.com/yoyoketang/p/9455276.html)

#### 前言

pytest.mark.parametrize装饰器可以实现测试用例参数化。

#### parametrizing

1.这里是一个实现检查一定的输入和期望输出测试功能的典型例子

```python
# content of test_expectation.py

# coding:utf-8

import pytest
@pytest.mark.parametrize("test_input,expected",
                         [ ("3+5", 8),
                           ("2+4", 6),
                           ("6 * 9", 42),
                         ])
def test_eval(test_input, expected):
    assert eval(test_input) == expected

if __name__ == "__main__":
    pytest.main(["-s", "test_canshu1.py"])
```

运行结果

```python
================================== FAILURES ===================================
_____________________________ test_eval[6 * 9-42] _____________________________

test_input = '6 * 9', expected = 42

    @pytest.mark.parametrize("test_input,expected",
                             [ ("3+5", 8),
                               ("2+4", 6),
                               ("6 * 9", 42),
                             ])
    def test_eval(test_input, expected):
>       assert eval(test_input) == expected
E       AssertionError: assert 54 == 42
E        +  where 54 = eval('6 * 9')

test_canshu1.py:11: AssertionError
===================== 1 failed, 2 passed in 1.98 seconds ======================
```

在这个例子中设计的，只有一条输入/输出值的简单测试功能。和往常一样

函数的参数，你可以在运行结果看到在输入和输出值

2.它也可以标记单个测试实例在参数化，例如使用内置的mark.xfail

```python
# content of test_expectation.py
import pytest
@pytest.mark.parametrize("test_input,expected", [
                        ("3+5", 8),
                        ("2+4", 6),
                        pytest.param("6 * 9", 42, marks=pytest.mark.xfail),
                        ])
def test_eval(test_input, expected):
    print("-------开始用例------")
    assert eval(test_input) == expected



if __name__ == "__main__":
    pytest.main(["-s", "test_canshu1.py"])
```

运行结果：

```python
test_canshu1.py -------开始用例------
.-------开始用例------
.-------开始用例------
x

===================== 2 passed, 1 xfailed in 1.84 seconds =====================
```

标记为失败的用例，预期结果是失败，实际运行也是失败，显示xfailed

#### 参数组合

1.若要获得多个参数化参数的所有组合，可以堆叠参数化装饰器

```python
import pytest
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_foo(x, y):
    print("测试数据组合：x->%s, y->%s" % (x, y))


if __name__ == "__main__":
    pytest.main(["-s", "test_canshu1.py"])
```

运行结果

```python
test_canshu1.py 测试数据组合：x->0, y->2
.测试数据组合：x->1, y->2
.测试数据组合：x->0, y->3
.测试数据组合：x->1, y->3
.

========================== 4 passed in 1.75 seconds ===========================
```

这将运行测试，参数设置为x＝0／y＝2，x＝1／y＝2，x＝0／y＝3，x＝1／y＝3组合参数。



# [pytest文档10-命令行传参](https://www.cnblogs.com/yoyoketang/p/9457473.html)

#### 前言

命令行参数是根据命令行选项将不同的值传递给测试函数，比如平常在cmd执行"pytest --html=report.html",这里面的”--html=report.html“就是从命令行传入的参数
对应的参数名称是html，参数值是report.html

#### conftest配置参数

1.首先需要在conftest.py添加命令行选项,命令行传入参数”--cmdopt“, 用例如果需要用到从命令行传入的参数，就调用cmdopt函数：

```
# content of conftest.py
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )

@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")
```

2.测试用例编写案例

```
# content of test_sample.py
import pytest
def test_answer(cmdopt):
    if cmdopt == "type1":
        print("first")
    elif cmdopt == "type2":
        print("second")
    assert 0  # to see what was printed

if __name__ == "__main__":
    pytest.main(["-s", "test_case1.py"])
```

cmd打开，输入指令启动，也可以在pycharm里面右键执行上面代码

> $ pytest -s test_sample.py

运行结果：

```
>pytest -s
============================= test session starts =============================
test_sample.py first
F

================================== FAILURES ===================================
_________________________________ test_answer _________________________________

cmdopt = 'type1'

    def test_answer(cmdopt):
        if cmdopt == "type1":
            print("first")
        elif cmdopt == "type2":
            print("second")
>       assert 0  # to see what was printed
E       assert 0

test_case1.py:8: AssertionError
========================== 1 failed in 0.05 seconds ===========================
```

#### 带参数启动

1.如果不带参数执行，那么传默认的default="type1"，接下来在命令行带上参数去执行

> $ pytest -s test_sample.py --cmdopt=type2

```
test_sample.py second
F

================================== FAILURES ===================================
_________________________________ test_answer _________________________________

cmdopt = 'type2'

    def test_answer(cmdopt):
        if cmdopt == "type1":
            print("first")
        elif cmdopt == "type2":
            print("second")
>       assert 0  # to see what was printed
E       assert 0

test_case1.py:8: AssertionError
========================== 1 failed in 0.05 seconds ===========================
```

2.命令行传参数有两种写法，还有一种分成2个参数也可以的,参数和名称用空格隔开

> $ pytest -s test_case1.py --cmdopt type2



# [pytest文档11-assert断言](https://www.cnblogs.com/yoyoketang/p/9469996.html)

#### 前言

断言是写自动化测试基本最重要的一步，一个用例没有断言，就失去了自动化测试的意义了。什么是断言呢？
简单来讲就是实际结果和期望结果去对比，符合预期那就测试pass，不符合预期那就测试 failed

#### assert

pytest允许您使用标准Python断言来验证Python测试中的期望和值。例如，你可以写下

```
# content of test_assert1.py
def f():
    return 3
def test_function():
    assert f() == 4
```

断言f()函数的返回值，接下来会看到断言失败，因为返回的值是3，判断等于4，所以失败了

```
$ pytest test_assert1.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-3.x.y, py-1.x.y, pluggy-0.x.y
rootdir: $REGENDOC_TMPDIR, inifile:
collected 1 item
test_assert1.py F [100%]
================================= FAILURES =================================
______________________________ test_function _______________________________
def test_function():
> assert f() == 4
E assert 3 == 4
E + where 3 = f()
test_assert1.py:5: AssertionError
========================= 1 failed in 0.12 seconds =========================
```

从报错信息可以看到断言失败原因：E assert 3 == 4

#### 异常信息

接下来再看一个案例，如果想在异常的时候，输出一些提示信息，这样报错后，就方便查看是什么原因了

```
def f():
    return 3

def test_function():

    a = f()
    assert a % 2 == 0, "判断a为偶数，当前a的值为：%s"%a
```

运行结果

```
================================== FAILURES ===================================
________________________________ test_function ________________________________

    def test_function():
    
        a = f()
>       assert a % 2 == 0, "判断a为偶数，当前a的值为：%s"%a
E       AssertionError: 判断a为偶数，当前a的值为：3
E       assert (3 % 2) == 0

test_03.py:9: AssertionError
========================== 1 failed in 0.18 seconds ===========================
```

这样当断言失败的时候，会给出自己写的失败原因了E AssertionError: 判断a为偶数，当前a的值为：3

#### 异常断言

为了写关于引发异常的断言，可以使用pytest.raises作为上下文管理器，如下

```
# content of test_assert1.py

import pytest
def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

运行结果

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\YOYO\canshuhua, inifile:
plugins: metadata-1.7.0, html-1.19.0
collected 1 item

test_assert1.py.

========================== 1 passed in 0.31 seconds ===========================
```

如果我们要断言它抛的异常是不是预期的，比如执行：1/0,预期结果是抛异常：ZeroDivisionError: division by zero，那我们要断言这个异常，通常是断言异常的type和value值了。
这里1/0的异常类型是ZeroDivisionError，异常的value值是division by zero，于是用例可以这样设计

```
# content of test_assert1.py

# ** 作者：上海-悠悠 QQ交流群：588402570**

import pytest
def test_zero_division():
    '''断言异常'''
    with pytest.raises(ZeroDivisionError) as excinfo:
        1 / 0

    # 断言异常类型type
    assert excinfo.type == ZeroDivisionError
    # 断言异常value值
    assert "division by zero" in str(excinfo.value)
```

**excinfo 是一个异常信息实例，它是围绕实际引发的异常的包装器。主要属性是.type、 .value 和 .traceback**

注意：断言type的时候，异常类型是不需要加引号的，断言value值的时候需转str

在上下文管理器窗体中，可以使用关键字参数消息指定自定义失败消息：

```
with pytest.raises(ZeroDivisionError, message="Expecting ZeroDivisionError"):
    pass

结果：Failed: Expecting ZeroDivisionError
```

#### 常用断言

pytest里面断言实际上就是python里面的assert断言方法，常用的有以下几种

- assert xx 判断xx为真
- assert not xx 判断xx不为真
- assert a in b 判断b包含a
- assert a == b 判断a等于b
- assert a != b 判断a不等于b

```
import pytest

# ** 作者：上海-悠悠 QQ交流群：588402570**

def is_true(a):
    if a > 0:
        return True
    else:
        return False

def test_01():
    '''断言xx为真'''
    a = 5
    b = -1
    assert is_true(a)
    assert not is_true(b)

def test_02():
    '''断言b 包含 a'''
    a = "hello"
    b = "hello world"
    assert a in b

def test_03():
    '''断言相等'''
    a = "yoyo"
    b = "yoyo"
    assert a == b

def test_04():
    '''断言不等于'''
    a = 5
    b = 6
    assert a != b

if __name__ == "__main__":
    pytest.main(["-s", "test_01.py"])
```

# [pytest文档12-skip跳过用例](https://www.cnblogs.com/yoyoketang/p/9475183.html)

#### 前言

pytest.mark.skip可以标记无法在某些平台上运行的测试功能，或者您希望失败的测试功能

skip意味着只有在满足某些条件时才希望测试通过，否则pytest应该跳过运行测试。 常见示例是在非Windows平台上跳过仅限Windows的测试，或跳过测试依赖于当前不可用的外部资源（例如数据库）。

xfail意味着您希望测试由于某种原因而失败。 一个常见的例子是对功能的测试尚未实施，或尚未修复的错误。 当测试通过时尽管预计会失败（标有pytest.mark.xfail），它是一个xpass，将在测试摘要中报告。

pytest计数并分别列出skip和xfail测试。 未显示有关跳过/ xfailed测试的详细信息默认情况下，以避免混乱输出。 您可以使用-r选项查看与“short”字母对应的详细信息显示在测试进度中

> pytest -rxXs # show extra info on xfailed, xpassed, and skipped tests

有关-r选项的更多详细信息，请运行pytest -h

#### skip

跳过测试函数的最简单方法是使用跳过装饰器标记它，可以传递一个可选的原因

```
@pytest.mark.skip(reason="no way of currently testing this")
def test_the_unknown():
    ...
```

或者，也可以通过调用来在测试执行或设置期间强制跳过pytest.skip（reason）功能：

```
def test_function():
    if not valid_config():
        pytest.skip("unsupported configuration")
```

也可以使用pytest.skip（reason，allow_module_level = True）跳过整个模块级别：

```
import pytest
if not pytest.config.getoption("--custom-flag"):
    pytest.skip("--custom-flag is missing, skipping tests", allow_module_level=True)
```

当在导入时间内无法评估跳过条件时，命令性方法很有用。

#### skipif

如果您希望有条件地跳过某些内容，则可以使用skipif代替。 这是标记测试的示例在Python3.6之前的解释器上运行时要跳过的函数

```
import sys
@pytest.mark.skipif(sys.version_info < (3,6),
reason="requires python3.6 or higher")
def test_function():
    ...
```

如果条件在收集期间评估为True，则将跳过测试函数，具有指定的原因使用-rs时出现在摘要中。

您可以在模块之间共享skipif标记。参考以下案例

```
# content of test_mymodule.py
import mymodule
minversion = pytest.mark.skipif(mymodule.__versioninfo__ < (1,1),
reason="at least mymodule-1.1 required")
@minversion
def test_function():
    ...
```

您可以导入标记并在另一个测试模块中重复使用它：

```
# test_myothermodule.py
from test_mymodule import minversion
@minversion
def test_anotherfunction():
    ...
```

对于较大的测试套件，通常最好有一个文件来定义标记，然后一致适用于整个测试套件。

或者，您可以使用条件字符串而不是布尔值，但它们之间不能轻易共享它们支持它们主要是出于向后兼容的原因

#### skip类或模块

您可以在类上使用skipif标记（与任何其他标记一样）：

```
@pytest.mark.skipif(sys.platform == 'win32',
reason="does not run on windows")
class TestPosixCalls(object):
    def test_function(self):
        "will not be setup or run under 'win32' platform"
```

如果条件为True，则此标记将为该类的每个测试方法生成跳过结果

**警告：强烈建议不要在使用继承的类上使用skipif。 pytest中的一个已知错误标记可能会导致超类中的意外行为。**

如果要跳过模块的所有测试功能，可以在全局级别使用pytestmark名称

```
# test_module.py
pytestmark = pytest.mark.skipif(...)
```

如果将多个skipif装饰器应用于测试函数，则如果任何跳过条件为真，则将跳过它

#### skip文件或目录

有时您可能需要跳过整个文件或目录，例如，如果测试依赖于特定于Python的版本功能或包含您不希望pytest运行的代码。 在这种情况下，您必须排除文件和目录来自收藏。 有关更多信息，请参阅自定义测试集合。

#### skip缺少导入依赖项

您可以在模块级别或测试或测试设置功能中使用以下帮助程序

```
docutils = pytest.importorskip("docutils")
```

如果无法在此处导入docutils，则会导致测试跳过结果。 你也可以跳过库的版本号

```
docutils = pytest.importorskip("docutils", minversion="0.3")
```

将从指定模块的__version__属性中读取版本。

#### 概要

这是一个快速指南，介绍如何在不同情况下跳过模块中的测试

1.无条件地跳过模块中的所有测试：

> pytestmark = pytest.mark.skip("all tests still WIP")

2.根据某些条件跳过模块中的所有测试

> pytestmark = pytest.mark.skipif(sys.platform == "win32", "tests for linux
> ˓→ only"

3.如果缺少某些导入，则跳过模块中的所有测试

> pexpect = pytest.importorskip("pexpect")



# [pytest文档13-allure2生成html报告(史上最详细)-已废弃，不用看了](https://www.cnblogs.com/yoyoketang/p/9483353.html)

#### 前言

allure是一个report框架,支持java的Junit/testng等框架,当然也可以支持python的pytest框架，也可以集成到Jenkins上展示高大上的报告界面。

环境准备

- 1.python3.6
- 2.windows环境
- 3.pycharm
- 4.pytest-allure-adaptor
- 5.allure2.7.0
- 6.java1.8

** 作者：上海-悠悠 QQ交流群：588402570**

#### pytest-allure-adaptor下载

pip安装pytest-allure-adaptor,[github地址https://github.com/allure-framework/allure-pytest](https://github.com/allure-framework/allure-pytest)

> pip3 install pytest-allure-adaptor

#### 生成xml报告

> pytest -s -q --alluredir report

如果不指定路径，默认在当前目录下新建一个report目录，当然也可以指定路径

> pytest -s -q --alluredir 指定report路径

执行完之后打开report文件夹,会自动生成xml格式的报告

#### 安装 Command Tool

allure的版本目前有2个，从github上看，allure1不再被支持，请考虑使用allure2 https://github.com/allure-framework/allure2替代

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180815184705651-1368742890.png)

[allure-commandline releases版本https://github.com/allure-framework/allure2/releases](https://github.com/allure-framework/allure2/releases)

下载最新的Download allure2.7.0版本

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180815184718897-2055043858.png)

[下载Download allure2.7.0 地址：https://dl.bintray.com/qameta/generic/io/qameta/allure/allure/2.7.0/allure-2.7.0.zip]
(https://dl.bintray.com/qameta/generic/io/qameta/allure/allure/2.7.0/allure-2.7.0.zip)

下载好之后，解压到运行pytest的目录下

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180815184859320-629047441.png)

打开\allure-2.7.0\bin文件夹，会看到allure.bat文件，讲此路径设置为系统环境变量path下，这样cmd任意目录都能执行了

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180815185100577-1970722640.png)

比如我的路径：D:\YOYO\case\allure-2.7.0\bin

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180815185213787-268682614.png)

#### 运行allure2

前面pytest -s -q --alluredir 这一步已经生产了xml格式的报告，放到了report目录下，接着执行以下命令格式

> allure generate directory-with-results/ -o directory-with-report

**directory-with-results是alluredir生成的xml目录，directory-with-report是最终生成html的目录**

allure.bat已经加到环境变量了，所以可以用相对路径去生成html报告

> allure generate report/ -o report/html

执行完之后目录结构如下：

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180815185650807-465232180.png)

#### 打开报告

直接找到report/html打开index.html会显示一个空的报告，这里用pycharm去打开

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180815185835833-1972459199.png)

打开后报告展示

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180815185925086-815355904.png)

#### 依赖java环境

之前用的jdk1.7版本，执行allure时候报错：Unsupported major.minor VERSION 51.0
由于allure2是java开发的，需要依赖java环境，解决办法：jdk版本用1.8就可以了

#### 已经废弃，使用allure-pytest库

这个库pytest-allure-adaptor早已经被废弃了，应该使用最新的allure-pytest库，一点问题都没有，可以在pypi.org上查看第三方库最新的版本发布时间，如果已经有两三年没有维护了，就不要主动往坑里跳了，徒增烦恼。

# [pytest文档14-函数传参和fixture传参数request](https://www.cnblogs.com/yoyoketang/p/9492132.html)

#### 前言

为了提高代码的复用性，我们在写用例的时候，会用到函数，然后不同的用例去调用这个函数。
比如登录操作，大部分的用例都会先登录，那就需要把登录单独抽出来写个函数，其它用例全部的调用这个登陆函数就行。
但是登录的账号不能写死，有时候我想用账号1去登录，执行用例1，用账号2去登录执行用例2，所以需要对函数传参。

#### 登录函数传参

把登录单独出来，写一个函数，传2个参数user和psw，写用例的时候调用登录函数，输入几组user,psw参数化登录用例

测试用例传参需要用装饰器@pytest.mark.parametrize，里面写两个参数

- 第一个参数是字符串，多个参数中间用逗号隔开
- 第二个参数是list,多组数据用元祖类型

```python
# test_01.py

# coding:utf-8
import pytest

# ** 作者：上海-悠悠 QQ交流群：588402570**

# 测试登录数据
test_login_data = [("admin", "111111"),  ("admin", "")]

def login(user, psw):
    '''普通登录函数'''
    print("登录账户：%s"%user)
    print("登录密码：%s"%psw)
    if psw:
        return True
    else:
        return False

@pytest.mark.parametrize("user, psw", test_login_data)
def test_login(user, psw):
    '''登录用例'''
    result = login(user, psw)
    assert result == True, "失败原因：密码为空"


if __name__ == "__main__":
    pytest.main(["-s", "test_01.py"])
```

运行结果

```python
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\, inifile:
plugins: metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 2 items

..\..\..\..\..\..\YOYO\marktest\test_01.py 登录账户：admin
登录密码：111111
.登录账户：admin
登录密码：
F
user = 'admin', psw = ''

    @pytest.mark.parametrize("user, psw", [("admin", "111111"), ("admin", "")])
    def test_01(user, psw):
        result = login(user, psw)
>       assert result == True
E       assert False == True

D:\YOYO\marktest\test_01.py:18: AssertionError


================================== FAILURES ===================================
_______________________________ test_01[admin-] _______________________________

user = 'admin', psw = ''

    @pytest.mark.parametrize("user, psw", [("admin", "111111"), ("admin", "")])
    def test_01(user, psw):
        result = login(user, psw)
>       assert result == True
E       assert False == True

D:\YOYO\marktest\test_01.py:18: AssertionError
===================== 1 failed, 1 passed in 0.05 seconds ======================
```

从结果可以看出，有2个用例，一个测试通过，一个测试失败了，互不影响

#### request参数

如果想把登录操作放到前置操作里，也就是用到@pytest.fixture装饰器，传参就用默认的request参数
user = request.param 这一步是接收传入的参数，本案例是传一个参数情况

```
# test_02.py
# coding:utf-8
import pytest

#** 作者：上海-悠悠 QQ交流群：588402570**

# 测试账号数据
test_user_data = ["admin1", "admin2"]

@pytest.fixture(scope="module")
def login(request):
    user = request.param
    print("登录账户：%s"%user)
    return user

@pytest.mark.parametrize("login", test_user_data, indirect=True)
def test_login(login):
    '''登录用例'''
    a = login
    print("测试用例中login的返回值:%s" % a)
    assert a != ""


if __name__ == "__main__":
    pytest.main(["-s", "test_02.py"])
```

运行结果：

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\, inifile:
plugins: metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 2 items

..\..\..\..\..\..\YOYO\marktest\test_02.py 登录账户：admin1
测试用例中login的返回值:admin1
.登录账户：admin2
测试用例中login的返回值:admin2
.

========================== 2 passed in 0.01 seconds ===========================
```

**添加indirect=True参数是为了把login当成一个函数去执行，而不是一个参数**

#### request传2个参数

如果用到@pytest.fixture，里面用2个参数情况，可以把多个参数用一个字典去存储，这样最终还是只传一个参数
不同的参数再从字典里面取对应key值就行，如： user = request.param["user"]

```
# test_03.py
# coding:utf-8
import pytest

# ** 作者：上海-悠悠 QQ交流群：588402570**

# 测试账号数据
test_user_data = [{"user": "admin1", "psw": "111111"},
                  {"user": "admin1", "psw": ""}]

@pytest.fixture(scope="module")
def login(request):
    user = request.param["user"]
    psw = request.param["psw"]
    print("登录账户：%s" % user)
    print("登录密码：%s" % psw)
    if psw:
        return True
    else:
        return False

# indirect=True 声明login是个函数
@pytest.mark.parametrize("login", test_user_data, indirect=True)
def test_login(login):
    '''登录用例'''
    a = login
    print("测试用例中login的返回值:%s" % a)
    assert a, "失败原因：密码为空"


if __name__ == "__main__":
    pytest.main(["-s", "test_03.py"])
```

运行结果

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\, inifile:
plugins: metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 2 items

..\..\..\..\..\..\YOYO\marktest\test_03.py 登录账户：admin1
登录密码：111111
测试用例中login的返回值:True
.登录账户：admin1
登录密码：
测试用例中login的返回值:False
F
login = False

    @pytest.mark.parametrize("login", test_user_data, indirect=True)
    def test_login(login):
        '''登录用例'''
        a = login
        print("测试用例中login的返回值:%s" % a)
>       assert a, "失败原因：密码为空"
E       AssertionError: 失败原因：密码为空
E       assert False

D:\YOYO\marktest\test_03.py:25: AssertionError


================================== FAILURES ===================================
_____________________________ test_login[login1] ______________________________

login = False

    @pytest.mark.parametrize("login", test_user_data, indirect=True)
    def test_login(login):
        '''登录用例'''
        a = login
        print("测试用例中login的返回值:%s" % a)
>       assert a, "失败原因：密码为空"
E       AssertionError: 失败原因：密码为空
E       assert False

D:\YOYO\marktest\test_03.py:25: AssertionError
===================== 1 failed, 1 passed in 0.05 seconds ======================
```

**如果要用到login里面的返回值，def test_login(login)时，传入login参数，函数返回值就是login了**

#### 多个fixtrue

用例上面是可以同时放多个fixture的，也就是多个前置操作，可以支持装饰器叠加，使用parametrize装饰器叠加时，用例组合是2个参数个数相乘

```
# test_04.py
# ** 作者：上海-悠悠 QQ交流群：588402570**
# coding:utf-8
import pytest

# 测试账号数据
test_user = ["admin1", "admin2"]
test_psw = ["11111", "22222"]


@pytest.fixture(scope="module")
def input_user(request):
    user = request.param
    print("登录账户：%s" % user)
    return user


@pytest.fixture(scope="module")
def input_psw(request):
    psw = request.param
    print("登录密码：%s" % psw)
    return psw



@pytest.mark.parametrize("input_user", test_user, indirect=True)
@pytest.mark.parametrize("input_psw", test_psw, indirect=True)
def test_login(input_user, input_psw):
    '''登录用例'''
    a = input_user
    b = input_psw
    print("测试数据a-> %s， b-> %s" % (a,b))
    assert b

if __name__ == "__main__":
    pytest.main(["-s", "test_04.py"])
```

运行结果

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\par, inifile:
plugins: metadata-1.7.0, html-1.19.0
collected 4 items

test_04.py 登录账户：admin1
登录密码：11111
测试数据a-> admin1， b-> 11111
.登录账户：admin2
测试数据a-> admin2， b-> 11111
.登录密码：22222
测试数据a-> admin2， b-> 22222
.登录账户：admin1
测试数据a-> admin1， b-> 22222
.

========================== 4 passed in 0.05 seconds ===========================
```

如果参数user有2个数据，参数psw有2个数据，那么组合起来的案例是两个相乘，也就是组合2*2 = 4个用例

# [pytest文档15-使用自定义标记mark](https://www.cnblogs.com/yoyoketang/p/9508500.html)

#### 前言

pytest可以支持自定义标记，自定义标记可以把一个web项目划分多个模块，然后指定模块名称执行。一个大项目自动化用例时，可以划分多个模块，
也可以使用标记功能，标明哪些是模块1用例，哪些是模块2的，运行代码时候指定mark名称运行就可以

#### mark标记

1.以下用例，标记test_send_http()为webtest

```
# content of test_server.py

import pytest

@pytest.mark.webtest
def test_send_http():
    pass # perform some webtest test for your app

def test_something_quick():
    pass

def test_another():
    pass

class TestClass:
    def test_method(self):
        pass

if __name__ == "__main__":
    pytest.main(["-s", "test_server.py", "-m=webtest"])
```

只运行用webtest标记的测试，cmd运行的时候，加个-m 参数，指定参数值webtest

> $ pytest -v -m webtest

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\se, inifile:
plugins: metadata-1.7.0, html-1.19.0
collected 4 items / 3 deselected

test_server.py .

=================== 1 passed, 3 deselected in 0.10 seconds ====================
```

如果不想执行标记webtest的用例，那就用"not webtest"

> $ pytest -v -m "not webtest"

```
import pytest

@pytest.mark.webtest
def test_send_http():
    pass # perform some webtest test for your app
def test_something_quick():
    pass
def test_another():
    pass
class TestClass:
    def test_method(self):
        pass

if __name__ == "__main__":
    pytest.main(["-s", "test_server.py", "-m='not webtest'"])
```

运行结果

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\se, inifile:
plugins: metadata-1.7.0, html-1.19.0
collected 4 items

test_server.py ....

========================== 4 passed in 0.06 seconds ===========================
```

#### -v 指定的函数节点id

如果想指定运行某个.py模块下，类里面的一个用例，如：TestClass里面test_method用例
每个test_开头(或_test结尾)的用例，函数(或方法)的名称就是用例的节点id，指定节点id运行用-v 参数

> $ pytest -v test_server.py::TestClass::test_method

pycharm运行代码

```
if __name__ == "__main__":
    pytest.main(["-v", "test_server.py::TestClass::test_method"])
```

运行结果

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0 -- E:\python36\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.6.0', 'Platform': 'Windows-10-10.0.17134-SP0', 'Packages': {'pytest': '3.6.3', 'py': '1.5.4', 'pluggy': '0.6.0'}, 'Plugins': {'metadata': '1.7.0', 'html': '1.19.0'}, 'JAVA_HOME': 'D:\\java\\jdk17'}
rootdir: E:\YOYO\se, inifile:
plugins: metadata-1.7.0, html-1.19.0
collecting ... collected 1 item

test_server.py::TestClass::test_method PASSED                            [100%]

========================== 1 passed in 0.06 seconds ===========================
```

当然也能选择运行整个class

> $ pytest -v test_server.py::TestClass

也能选择多个节点运行，多个节点中间空格隔开

> $ pytest -v test_server.py::TestClass test_server.py::test_send_http

pycharm运行参考

```
if __name__ == "__main__":
    pytest.main(["-v", "test_server.py::TestClass", "test_server.py::test_send_http"])
```

#### -k 匹配用例名称

可以使用-k命令行选项指定在匹配用例名称的表达式

> $ pytest -v -k http

```
$ pytest -v -k http # running with the above defined example module
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-3.x.y, py-1.x.y, pluggy-0.x.y -- $PYTHON_
˓→PREFIX/bin/python3.5
cachedir: .pytest_cache
rootdir: $REGENDOC_TMPDIR, inifile:
collecting ... collected 4 items / 3 deselected
test_server.py::test_send_http PASSED [100%]
================== 1 passed, 3 deselected in 0.12 seconds ==================
```

您也可以运行所有的测试，根据用例名称排除掉某些用例：

> $ pytest -k "not send_http" -v

```
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-3.x.y, py-1.x.y, pluggy-0.x.y -- $PYTHON_
˓→PREFIX/bin/python3.5
cachedir: .pytest_cache
rootdir: $REGENDOC_TMPDIR, inifile:
collecting ... collected 4 items / 1 deselected
test_server.py::test_something_quick PASSED [ 33%]
test_server.py::test_another PASSED [ 66%]
test_server.py::TestClass::test_method PASSED [100%]
================== 3 passed, 1 deselected in 0.12 seconds ==================
```

也可以同时选择匹配 “http” 和“quick”

> $ pytest -k "http or quick" -v

```
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-3.x.y, py-1.x.y, pluggy-0.x.y -- $PYTHON_
˓→PREFIX/bin/python3.5
cachedir: .pytest_cache
rootdir: $REGENDOC_TMPDIR, inifile:
collecting ... collected 4 items / 2 deselected
test_server.py::test_send_http PASSED [ 50%]
test_server.py::test_something_quick PASSED [100%]
================== 2 passed, 2 deselected in 0.12 seconds ==================
```

# [pytest文档16-用例a失败，跳过测试用例b和c并标记失败xfail](https://www.cnblogs.com/yoyoketang/p/9525602.html)

#### 前言

当用例a失败的时候，如果用例b和用例c都是依赖于第一个用例的结果，那可以直接跳过用例b和c的测试，直接给他标记失败xfail
用到的场景，登录是第一个用例，登录之后的操作b是第二个用例，登录之后操作c是第三个用例，很明显三个用例都会走到登录。
如果登录都失败了，那后面2个用例就没测试必要了，直接跳过，并且标记为失败用例，这样可以节省用例时间。

#### 用例设计

1.pytest里面用xfail标记用例为失败的用例，可以直接跳过。实现基本思路

- 把登录写为前置操作
- 对登录的账户和密码参数化，参数用canshu = [{"user":"amdin", "psw":"111"}]表示
- 多个用例放到一个Test_xx的class里
- test_01，test_02， test_03全部调用fixture里面的login功能
- test_01测试登录用例
- test_02和test_03执行前用if判断登录的结果，登录失败就执行，pytest.xfail("登录不成功, 标记为xfail")

```
# content of test_05.py

# coding:utf-8
import pytest

# ** 作者：上海-悠悠 QQ交流群：588402570**

canshu = [{"user":"amdin", "psw":"111"}]

@pytest.fixture(scope="module")
def login(request):
    user = request.param["user"]
    psw = request.param["psw"]
    print("正在操作登录，账号：%s, 密码：%s" % (user, psw))
    if psw:
        return True
    else:
        return False


@pytest.mark.parametrize("login", canshu, indirect=True)
class Test_xx():

    def test_01(self, login):
        '''用例1登录'''
        result = login
        print("用例1：%s" % result)
        assert result == True


    def test_02(self, login):
        result = login
        print("用例3,登录结果：%s" % result)
        if not result:
            pytest.xfail("登录不成功, 标记为xfail")

        assert 1 == 1

    def test_03(self, login):
        result = login
        print("用例3,登录结果：%s" %result)
        if not result:
            pytest.xfail("登录不成功, 标记为xfail")

        assert 1 == 1


if __name__ == "__main__":
    pytest.main(["-s", "test_05.py"])
```

上面传的登录参数是登录成功的案例，三个用例全部通过

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\, inifile:
plugins: metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 3 items

..\..\..\..\..\..\YOYO\peizhi\test_05.py 正在操作登录，账号：amdin, 密码：111
用例1：True
.用例3,登录结果：True
.用例3,登录结果：True
.

========================== 3 passed in 0.02 seconds ===========================
```

#### 标记为xfail

1.再看看登录失败情况的用例,修改登录的参数

```
# content of test_05.py
# coding:utf-8
import pytest

# ** 作者：上海-悠悠 QQ交流群：588402570**

canshu = [{"user":"amdin", "psw":""}]

@pytest.fixture(scope="module")
def login(request):
    user = request.param["user"]
    psw = request.param["psw"]
    print("正在操作登录，账号：%s, 密码：%s" % (user, psw))
    if psw:
        return True
    else:
        return False


@pytest.mark.parametrize("login", canshu, indirect=True)
class Test_xx():

    def test_01(self, login):
        '''用例1登录'''
        result = login
        print("用例1：%s" % result)
        assert result == True


    def test_02(self, login):
        result = login
        print("用例3,登录结果：%s" % result)
        if not result:
            pytest.xfail("登录不成功, 标记为xfail")

        assert 1 == 1

    def test_03(self, login):
        result = login
        print("用例3,登录结果：%s" %result)
        if not result:
            pytest.xfail("登录不成功, 标记为xfail")

        assert 1 == 1


if __name__ == "__main__":
    pytest.main(["-s", "test_05.py"])
```

运行结果

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\, inifile:
plugins: metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 3 items

..\..\..\..\..\..\YOYO\peizhi\test_05.py 正在操作登录，账号：amdin, 密码：
用例1：False
F
self = <YOYO.peizhi.test_05.Test_xx object at 0x00000000045ACF98>, login = False

    def test_01(self, login):
        '''用例1登录'''
        result = login
        print("用例1：%s" % result)
>       assert result == True
E       assert False == True

D:\YOYO\peizhi\test_05.py:24: AssertionError
用例3,登录结果：False
x
Test ignored.用例3,登录结果：False
x
Test ignored.

================================== FAILURES ===================================
___________________________ Test_xx.test_01[login0] ___________________________

self = <YOYO.peizhi.test_05.Test_xx object at 0x00000000045ACF98>, login = False

    def test_01(self, login):
        '''用例1登录'''
        result = login
        print("用例1：%s" % result)
>       assert result == True
E       assert False == True

D:\YOYO\peizhi\test_05.py:24: AssertionError
===================== 1 failed, 2 xfailed in 0.06 seconds =====================
```

从结果可以看出用例1失败了，用例2和3没执行，直接标记为xfail了

# [pytest文档17-fixture之autouse=True](https://www.cnblogs.com/yoyoketang/p/9530741.html)

#### 前言

平常写自动化用例会写一些前置的fixture操作，用例需要用到就直接传该函数的参数名称就行了。当用例很多的时候，每次都传这个参数，会比较麻烦。
fixture里面有个参数autouse，默认是Fasle没开启的，可以设置为True开启自动使用fixture功能，这样用例就不用每次都去传参了

调用fixture三种方法

- 1.函数或类里面方法直接传fixture的函数参数名称
- 2.使用装饰器@pytest.mark.usefixtures()修饰
- 3.autouse=True自动使用

#### 用例传fixture参数

方法一：先定义start功能，用例全部传start参数，调用该功能

```python
# content of test_06.py
import time
import pytest

# ** 作者：上海-悠悠 QQ交流群：588402570**

@pytest.fixture(scope="function")
def start(request):
    print('\n-----开始执行function----')


def test_a(start):
    print("-------用例a执行-------")




class Test_aaa():

    def test_01(self, start):
        print('-----------用例01--------------')

    def test_02(self, start):
        print('-----------用例02------------')

if __name__ == "__main__":
    pytest.main(["-s", "test_06.py"])
```

#### 装饰器usefixtures

方法二：使用装饰器@pytest.mark.usefixtures()修饰需要运行的用例

```
# content of test_07.py
import time
import pytest

# ** 作者：上海-悠悠 QQ交流群：588402570**

@pytest.fixture(scope="function")
def start(request):
    print('\n-----开始执行function----')


@pytest.mark.usefixtures("start")
def test_a():
    print("-------用例a执行-------")

@pytest.mark.usefixtures("start")
class Test_aaa():

    def test_01(self):
        print('-----------用例01--------------')

    def test_02(self):
        print('-----------用例02------------')

if __name__ == "__main__":
    pytest.main(["-s", "test_07.py"])
```

#### 设置autouse=True

方法三、autouse设置为True，自动调用fixture功能

- start设置scope为module级别，在当前.py用例模块只执行一次，autouse=True自动使用
- open_home设置scope为function级别，每个用例前都调用一次，自动使用

```
# content of test_08.py
import time
import pytest

# ** 作者：上海-悠悠 QQ交流群：588402570**

@pytest.fixture(scope="module", autouse=True)
def start(request):
    print('\n-----开始执行moule----')
    print('module      : %s' % request.module.__name__)
    print('----------启动浏览器---------')
    yield
    print("------------结束测试 end!-----------")



@pytest.fixture(scope="function", autouse=True)
def open_home(request):
    print("function：%s \n--------回到首页--------" % request.function.__name__)


def test_01():
    print('-----------用例01--------------')

def test_02():
    print('-----------用例02------------')

if __name__ == "__main__":
    pytest.main(["-s", "test_08.py"])
```

运行结果：

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\, inifile:
plugins: metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 2 items

..\..\..\..\..\..\YOYO\peizhi\test_08.py 
-----开始执行moule----
module      : YOYO.peizhi.test_08
----------启动浏览器---------
function：test_01 
--------回到首页--------
-----------用例01--------------
.function：test_02 
--------回到首页--------
-----------用例02------------
.------------结束测试-----------


========================== 2 passed in 0.01 seconds ===========================
```

上面是函数去实现用例，写的class里也是一样可以的

```
# content of test_09.py
import time
import pytest

# ** 作者：上海-悠悠 QQ交流群：588402570**

@pytest.fixture(scope="module", autouse=True)
def start(request):
    print('\n-----开始执行moule----')
    print('module      : %s' % request.module.__name__)
    print('----------启动浏览器---------')
    yield
    print("------------结束测试 end!-----------")



class Test_aaa():
    @pytest.fixture(scope="function", autouse=True)
    def open_home(self, request):
        print("function：%s \n--------回到首页--------" % request.function.__name__)


    def test_01(self):
        print('-----------用例01--------------')

    def test_02(self):
        print('-----------用例02------------')

if __name__ == "__main__":
    pytest.main(["-s", "test_09.py"])
```

# [pytest文档18-配置文件pytest.ini](https://www.cnblogs.com/yoyoketang/p/9550648.html)

#### 前言

pytest配置文件可以改变pytest的运行方式，它是一个固定的文件pytest.ini文件，读取配置信息，按指定的方式去运行。

#### ini配置文件

pytest里面有些文件是非test文件

- pytest.ini pytest的主配置文件，可以改变pytest的默认行为
- conftest.py 测试用例的一些fixture配置
- _*init*_.py 识别该文件夹为python的package包
- tox.ini 与pytest.ini类似，用tox工具时候才有用
- setup.cfg 也是ini格式文件，影响setup.py的行为

ini文件基本格式

```
# 保存为pytest.ini文件

[pytest]

addopts = -rsxX
xfail_strict = true
```

使用pytest --help指令可以查看pytest.ini的设置选项

```
[pytest] ini-options in the first pytest.ini|tox.ini|setup.cfg file found:

  markers (linelist)       markers for test functions
  empty_parameter_set_mark (string) default marker for empty parametersets
  norecursedirs (args)     directory patterns to avoid for recursion
  testpaths (args)         directories to search for tests when no files or dire

  console_output_style (string) console output: classic or with additional progr

  usefixtures (args)       list of default fixtures to be used with this project

  python_files (args)      glob-style file patterns for Python test module disco

  python_classes (args)    prefixes or glob names for Python test class discover

  python_functions (args)  prefixes or glob names for Python test function and m

  xfail_strict (bool)      default for the strict parameter of 
  addopts (args)           extra command line options
  minversion (string)      minimally required pytest version
```

**--rsxX 表示pytest报告所有测试用例被跳过、预计失败、预计失败但实际被通过的原因**

#### mark标记

如下案例，使用了2个标签：webtest和hello,使用mark标记功能对于以后分类测试非常有用处

```
# content of test_mark.py
import pytest

@pytest.mark.webtest
def test_send_http():
    print("mark web test")

def test_something_quick():
    pass

def test_another():
    pass

@pytest.mark.hello
class TestClass:
    def test_01(self):
        print("hello :")

    def test_02(self):
        print("hello world!")

if __name__ == "__main__":
    pytest.main(["-v", "test_mark.py", "-m=hello"])
```

运行结果

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0 -- D:\soft\python3.6\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.6.0', 'Platform': 'Windows-7-6.1.7601-SP1', 'Packages': {'pytest': '3.6.3', 'py': '1.5.4', 'pluggy': '0.6.0'}, 'Plugins': {'metadata': '1.7.0', 'html': '1.19.0', 'allure-adaptor': '1.7.10'}, 'JAVA_HOME': 'D:\\soft\\jdk18\\jdk18v'}
rootdir: D:\YOYO, inifile:
plugins: metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collecting ... collected 5 items / 3 deselected

test_mark.py::TestClass::test_01 PASSED                                  [ 50%]
test_mark.py::TestClass::test_02 PASSED                                  [100%]

=================== 2 passed, 3 deselected in 0.11 seconds ====================
```

有时候标签多了，不容易记住，为了方便后续执行指令的时候能准确使用mark的标签，可以写入到pytest.ini文件

```
# pytest.ini
[pytest]

markers =
  webtest:  Run the webtest case
  hello: Run the hello case
```

标记好之后，可以使用pytest --markers查看到

> $ pytest --markers

```
D:\YOYO>pytest --markers
@pytest.mark.webtest:  Run the webtest case

@pytest.mark.hello: Run the hello case

@pytest.mark.skip(reason=None): skip the given test function with an optional re
ason. Example: skip(reason="no way of currently testing this") skips the test.

@pytest.mark.skipif(condition): skip the given test function if eval(condition)
results in a True value.  Evaluation happens within the module global context. E
xample: skipif('sys.platform == "win32"') skips the test if we are on the win32
platform. see http://pytest.org/latest/skipping.html

@pytest.mark.xfail(condition, reason=None, run=True, raises=None, strict=False):
 mark the test function as an expected failure if eval(condition) has a True val
ue. Optionally specify a reason for better reporting and run=False if you don't
even want to execute the test function. If only specific exception(s) are expect
ed, you can list them in raises, and if the test fails in other ways, it will be
 reported as a true failure. See http://pytest.org/latest/skipping.html

@pytest.mark.parametrize(argnames, argvalues): call a test function multiple tim
es passing in different arguments in turn. argvalues generally needs to be a lis
t of values if argnames specifies only one name or a list of tuples of values if
 argnames specifies multiple names. Example: @parametrize('arg1', [1,2]) would l
ead to two calls of the decorated test function, one with arg1=1 and another wit
h arg1=2.see http://pytest.org/latest/parametrize.html for more info and example
s.

@pytest.mark.usefixtures(fixturename1, fixturename2, ...): mark tests as needing
 all of the specified fixtures. see http://pytest.org/latest/fixture.html#usefix
tures

@pytest.mark.tryfirst: mark a hook implementation function such that the plugin
machinery will try to call it first/as early as possible.

@pytest.mark.trylast: mark a hook implementation function such that the plugin m
achinery will try to call it last/as late as possible.
```

最上面两个就是刚才写入到pytest.ini的配置了

#### 禁用xpass

设置xfail_strict = true可以让那些标记为@pytest.mark.xfail但实际通过的测试用例被报告为失败

什么叫标记为@pytest.mark.xfail但实际通过，这个比较绕脑，看以下案例

```
# content of test_xpass.py
import pytest
** 作者：上海-悠悠 QQ交流群：588402570**

def test_hello():
    print("hello world!")
    assert 1

@pytest.mark.xfail()
def test_yoyo1():
    a = "hello"
    b = "hello world"
    assert a == b

@pytest.mark.xfail()
def test_yoyo2():
    a = "hello"
    b = "hello world"
    assert a != b

if __name__ == "__main__":
    pytest.main(["-v", "test_xpass.py"])
```

测试结果

```
collecting ... collected 3 items

test_xpass.py::test_hello PASSED    [ 33%]
test_xpass.py::test_yoyo1 xfail     [ 66%]
test_xpass.py::test_yoyo2 XPASS     [100%]

=============== 1 passed, 1 xfailed, 1 xpassed in 0.27 seconds ================
```

test_yoyo1和test_yoyo2这2个用例一个是a == b一个是a != b,两个都标记失败了，我们希望两个用例不用执行全部显示xfail。实际上最后一个却显示xpass.为了让两个都显示xfail，那就加个配置
xfail_strict = true

```
# pytest.ini
[pytest]

markers =
  webtest:  Run the webtest case
  hello: Run the hello case

xfail_strict = true
```

再次运行，结果就变成

```
collecting ... collected 3 items

test_xpass.py::test_hello PASSED        [ 33%]
test_xpass.py::test_yoyo1 xfail         [ 66%]
test_xpass.py::test_yoyo2 FAILED        [100%]

================================== FAILURES ===================================
_________________________________ test_yoyo2 __________________________________
[XPASS(strict)] 
================ 1 failed, 1 passed, 1 xfailed in 0.05 seconds ================
```

这样标记为xpass的就被强制性变成failed的结果

#### 配置文件如何放

一般一个工程下方一个pytest.ini文件(不要瞎jb拍脑袋乱命名，瞎jb命名是找不到的)就可以了，放到顶层文件夹下

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180828203539877-608557122.png)

#### addopts

addopts参数可以更改默认命令行选项，这个当我们在cmd输入指令去执行用例的时候，会用到，比如我想测试完生成报告，指令比较长

> $ pytest -v --reruns 1 --html=report.html --self-contained-html

每次输入这么多，不太好记住，于是可以加到pytest.ini里

```
# pytest.ini
[pytest]

markers =
  webtest:  Run the webtest case
  hello: Run the hello case

 xfail_strict = true

 addopts = -v --reruns 1 --html=report.html --self-contained-html
```

这样我下次打开cmd，直接输入pytest，它就能默认带上这些参数了

# [pytest文档19-doctest测试框架](https://www.cnblogs.com/yoyoketang/p/9561697.html)

#### 前言

doctest从字面意思上看，那就是文档测试。doctest是python里面自带的一个模块，它实际上是单元测试的一种。
官方解释：doctest 模块会搜索那些看起来像交互式会话的 Python 代码片段，然后尝试执行并验证结果

doctest测试用例可以放在两个地方

- 函数或者方法下的注释里面
- 模块的开头

#### 案例

先看第一个案例，将需要测试的片段,标准格式，需要运行的代码前面加>>> ,相当于进入cmd这种交互环境执行，期望的结果前面不需要加>>>

```
>>> multiply(4, 3)
    12
>>> multiply('a', 3)
    'aaa'
```

放到multiply函数的注释里

```
def multiply(a, b):
    """
    fuction: 两个数相乘
    >>> multiply(4, 3)
    12
    >>> multiply('a', 3)
    'aaa'
    """
    return a * b
if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
```

运行结果

```
Trying:
    multiply(4, 3)
Expecting:
    12
ok
Trying:
    multiply('a', 3)
Expecting:
    'aaa'
ok
1 items had no tests:
    __main__
1 items passed all tests:
   2 tests in __main__.multiply
2 tests in 2 items.
2 passed and 0 failed.
Test passed.
```

从运行的结果可以看出，虽然函数下方的注释里面有其它内容“fuction: 两个数相乘”，但不会去执行，只识别“>>>”这种符号。2个测试用例都是通过的，实际的结果与期望的结果一致。

#### 失败案例

doctest的内容放到.py模块的开头也是可以识别到的

```
# 保存为xxx.py
'''
fuction: 两个数相乘
>>> multiply(4, 8)
12
>>> multiply('a', 5)
'aaa'
'''

def multiply(a, b):
    """
    fuction: 两个数相乘
    """
    return a * b
if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
```

运行结果2个都失败

```
**********************************************************************
1 items had failures:
   2 of   2 in __main__
2 tests in 2 items.
0 passed and 2 failed.
***Test Failed*** 2 failures.
```

**verbose参数，设置为True则在执行测试的时候会输出详细信息**

#### cmd执行

以上案例是在编辑器直接运行的，如果在cmd里面，也可以用指令去执行

> $ python -m doctest -v xxx.py

- m 参数指定运行方式doctest
- -v参数是verbose，带上-v参数相当于verbose=True

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180830174959676-619304357.png)

#### pytest运行

pytest框架是可以兼容doctest用例，执行的时候加个参数 --doctest-modules ,这样它就能自动搜索到doctest的用例

> $ pytest -v --doctest-modules xxx.py

![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180830175015319-1487980621.png)

如下是函数下的文档

```
fuction: 两个数相乘
>>> multiply(4, 3)
12
>>> multiply('a', 5)
'aaa'
```

运行结果

```
D:\test1122\a>pytest -v --doctest-modules  xxx.py
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0 -- d:\soft\
python3.6\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.6.0', 'Platform': 'Windows-7-6.1.7601-SP1', 'Packages':
{'pytest': '3.6.3', 'py': '1.5.4', 'pluggy': '0.6.0'}, 'Plugins': {'metadata': '
1.7.0', 'html': '1.19.0', 'allure-adaptor': '1.7.10'}, 'JAVA_HOME': 'D:\\soft\\j
dk18\\jdk18v'}
rootdir: D:\test1122\a, inifile:
plugins: metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 1 item

xxx.py::xxx.multiply FAILED                                              [100%]

================================== FAILURES ===================================
___________________________ [doctest] xxx.multiply ____________________________
004
005     fuction: 两个数相乘
006     >>> multiply(4, 3)
007     12
008     >>> multiply('a', 5)
Expected:
    'aaa'
Got:
    'aaaaa'

D:\test1122\a\xxx.py:8: DocTestFailure
========================== 1 failed in 0.16 seconds ===========================
```

结果可以看出，文档里面的每一行都被执行了，当遇到测试不通过的用例时，就不会继续往下执行了

#### doctest独立文件

doctest内容也可以和代码抽离开，单独用一个.txt文件保存
![img](https://images2018.cnblogs.com/blog/1070438/201808/1070438-20180830175043546-21880538.png)

在当前xxx.py同一目录新建一个xxx.txt文件，写入测试的文档，要先导入该功能，导入代码前面也要加>>>

```
>>> from xxx import multiply
>>> multiply(4, 3)
12
>>> multiply('a', 3)
'aaa'
```

cmd执行“python -m doctest -v xxx.txt”测试结果

```
D:\test1122>python -m doctest -v  xxx.txt
Trying:
    from xxx import multiply
Expecting nothing
ok
Trying:
    multiply(4, 3)
Expecting:
    12
ok
Trying:
    multiply('a', 3)
Expecting:
    'aaa'
ok
1 items passed all tests:
   3 tests in xxx.txt
3 tests in 1 items.
3 passed and 0 failed.
Test passed.
```

# [pytest文档20-pytest-html报告优化（添加Description）](https://www.cnblogs.com/yoyoketang/p/9748718.html)

#### 前言

pytest-html测试报告默认是不展示用例描述Description内容，之前用unittest生成的报告是可以展示用例的描述，也就是test开头的用例下三个引号里面的注释（docstring）内容。
pytest-html框架是可以修改生成的报告内容的，可以自己添加和删除html报告的table内容。

#### 修改报告

pytest-html官方文档地址[【https://pypi.org/project/pytest-html/】](https://pypi.org/project/pytest-html/)
l可以通过为标题行实现自定义钩子来修改列，下面的示例在conftest.py脚本中使用测试函数docstring添加描述（Description）列，添加可排序时间（Time）列，并删除链接(Link)列：

```
from datetime import datetime
from py.xml import html
import pytest

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop()

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(datetime.utcnow(), class_='col-time'))
    cells.pop()

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
```

还可以通过pytest_html_results_table_row 挂钩删除所有单元格来删除结果。下面的示例从报表中删除所有测试通过的结果：

```
import pytest

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    if report.passed:
      del cells[:]
```

日志输出和附加HTML可以通过pytest_html_results_table_html挂钩来修改。下面的示例清空测试通过的日志输出：

```
import pytest

@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('No log output captured.', class_='empty log'))
```

#### 添加Description

通过上面的官方文档，可以自己修改下测试报告，在报告里面添加一列的内容，添加到第二列，于是修改如下，红色代码全部注释掉

![img](https://img2018.cnblogs.com/blog/1070438/201810/1070438-20181006214832419-599614386.png)

第三个@pytest.mark.hookwrapper，这个在之前测试报告里面添加截图时候，已经写过了，只需在最后加一句代码即可

> report.description = str(item.function.**doc**)

![img](https://img2018.cnblogs.com/blog/1070438/201810/1070438-20181006215124955-1608657044.png)

#### 代码参考

项目根目录下新建conftest.py

```
# conftest.py


from datetime import datetime
from py.xml import html
import pytest

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_")+".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
        report.description = str(item.function.__doc__)

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
```

#### 效果展示

修改完之后cmd运行

> pytest --html=report.html --self-contained-html

![img](https://img2018.cnblogs.com/blog/1070438/201810/1070438-20181006215449914-435338675.png)

# [pytest文档22-fixture详细介绍-作为参数传入,error和failed区别](https://www.cnblogs.com/yoyoketang/p/9762171.html)

#### 前言

fixture是pytest的核心功能，也是亮点功能，熟练掌握fixture的使用方法，pytest用起来才会得心应手！

#### fixture简介

fixture的目的是提供一个固定基线，在该基线上测试可以可靠地和重复地执行。fixture提供了区别于传统单元测试（setup/teardown）有显著改进：

- 有独立的命名，并通过声明它们从测试函数、模块、类或整个项目中的使用来激活。
- 按模块化的方式实现，每个fixture都可以互相调用。
- fixture的范围从简单的单元扩展到复杂的功能测试，允许根据配置和组件选项对fixture和测试用例进行参数化，或者跨函数 function、类class、模块module或整个测试会话sessio范围。

#### fixture作为参数传入

定义fixture跟定义普通函数差不多，唯一区别就是在函数上加个装饰器@pytest.fixture()，fixture命名不要用test_开头，跟用例区分开。用例才是test_开头的命名。

fixture是可以有返回值的，如果没return默认返回None。用例调用fixture的返回值，直接就是把fixture的函数名称当成变量名称，如下案例

```
# test_fixture1.py
import pytest

@pytest.fixture()
def user():
    print("获取用户名")
    a = "yoyo"
    return a

def test_1(user):
    assert user == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture1.py"])
```

运行结果

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\YOYO\fixt, inifile:
plugins: rerunfailures-4.1, metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 1 item

test_fixture1.py 获取用户名
.

========================== 1 passed in 0.20 seconds ===========================
```

#### error和failed区别

测试结果一般有三种：passed、failed、error。（skip的用例除外）

如果在test_用例里面断言失败，那就是failed

```
# test_fixture2.py
import pytest

@pytest.fixture()
def user():
    print("获取用户名")
    a = "yoyo"
    return a

def test_1(user):
    assert user == "yoyo111"  # 用例失败就是failed

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture2.py"])
```

如果在fixture里面断言失败了，那就是error

```
test_fixture3.py
import pytest

@pytest.fixture()
def user():
    print("获取用户名")
    a = "yoyo"
    assert a == "yoyo123"  # fixture失败就是error
    return a

def test_1(user):
    assert user == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture3.py"])
```

还有一种情况也会出现error，那就是自己代码写的有问题，自己本身代码报错，那就是error了。

# [pytest文档23-使用多个fixture和fixture直接互相调用](https://www.cnblogs.com/yoyoketang/p/9762191.html)

#### 使用多个fixture

如果用例需要用到多个fixture的返回数据，fixture也可以return一个元组、list或字典，然后从里面取出对应数据。

```
# test_fixture4.py
import pytest

@pytest.fixture()
def user():
    print("获取用户名")
    a = "yoyo"
    b = "123456"
    return (a, b)


def test_1(user):
    u = user[0]
    p = user[1]
    print("测试账号：%s, 密码：%s" % (u, p))
    assert u == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture4.py"])
```

当然也可以分开定义成多个fixture，然后test_用例传多个fixture参数

```
# test_fixture5.py
import pytest

@pytest.fixture()
def user():
    print("获取用户名")
    a = "yoyo"
    return a

@pytest.fixture()
def psw():
    print("获取密码")
    b = "123456"
    return b

def test_1(user, psw):
    '''传多个fixture'''
    print("测试账号：%s, 密码：%s" % (user, psw))
    assert user == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture5.py"])
```

#### fixture与fixture互相调用

fixture与fixture直接也能互相调用的

```
import pytest

@pytest.fixture()
def first():
    print("获取用户名")
    a = "yoyo"
    return a

@pytest.fixture()
def sencond(first):
    '''psw调用user fixture'''
    a = first
    b = "123456"
    return (a, b)

def test_1(sencond):
    '''用例传fixture'''
    print("测试账号：%s, 密码：%s" % (sencond[0], sencond[1]))

    assert sencond[0] == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture6.py"])
```

# [pytest文档24-fixture的作用范围(scope)](https://www.cnblogs.com/yoyoketang/p/9762197.html)

#### fixture作用范围

fixture里面有个scope参数可以控制fixture的作用范围:session > module > class > function

```
fixture(scope="function", params=None, autouse=False, ids=None, name=None):
    """使用装饰器标记fixture的功能
     ** 作者：上海-悠悠 QQ交流群：588402570**
     可以使用此装饰器（带或不带参数）来定义fixture功能。 fixture功能的名称可以在以后使用
     引用它会在运行测试之前调用它：test模块或类可以使用pytest.mark.usefixtures（fixturename标记。 
     测试功能可以直接使用fixture名称作为输入参数，在这种情况下，夹具实例从fixture返回功能将被注入。

    :arg scope: scope 有四个级别参数 "function" (默认), "class", "module" or "session".

    :arg params: 一个可选的参数列表，它将导致多个参数调用fixture功能和所有测试使用它

    :arg autouse:  如果为True，则为所有测试激活fixture func 可以看到它。 如果为False（默认值）则显式需要参考来激活fixture

    :arg ids: 每个字符串id的列表，每个字符串对应于params 这样他们就是测试ID的一部分。 如果没有提供ID它们将从params自动生成

    :arg name:   fixture的名称。 这默认为装饰函数的名称。 如果fixture在定义它的同一模块中使用，夹具的功能名称将被请求夹具的功能arg遮蔽; 解决这个问题的一种方法是将装饰函数命名
                       “fixture_ <fixturename>”然后使用”@ pytest.fixture（name ='<fixturename>'）“”。
```

- function 每一个函数或方法都会调用
- class 每一个类调用一次，一个类可以有多个方法
- module，每一个.py文件调用一次，该文件内又有多个function和class
- session 是多个文件调用一次，可以跨.py文件调用，每个.py文件就是module

#### scope="function"

@pytest.fixture()如果不写参数，默认就是scope="function"，它的作用范围是每个测试用例来之前运行一次，销毁代码在测试用例运行之后运行。

```python
import pytest

@pytest.fixture()
def first():
    print("\n获取用户名")
    a = "yoyo"
    return a

@pytest.fixture(scope="function")
def sencond():
    print("\n获取密码")
    b = "123456"
    return b

def test_1(first):
    '''用例传fixture'''
    print("测试账号：%s" %first)
    assert first == "yoyo"

def test_2(sencond):
    '''用例传fixture'''
    print("测试密码：%s" %sencond)
    assert sencond == "123456"

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture7.py"])
```

运行结果：

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\YOYO\fixt, inifile:
plugins: rerunfailures-4.1, metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 2 items

test_fixture7.py 
获取用户名
测试账号：yoyo
.
获取密码
测试密码：123456
.

========================== 2 passed in 0.01 seconds ===========================
```

用例放到类里面也一样

```
import pytest

@pytest.fixture()
def first():
    print("\n获取用户名")
    a = "yoyo"
    return a

@pytest.fixture(scope="function")
def sencond():
    print("\n获取密码")
    b = "123456"
    return b

class TestCase():
    def test_1(self, first):
        '''用例传fixture'''
        print("测试账号：%s" % first)
        assert first == "yoyo"

    def test_2(self, sencond):
        '''用例传fixture'''
        print("测试密码：%s" % sencond)
        assert sencond == "123456"

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture7.py"])
```

#### scope="class"

fixture为class级别的时候，如果一个class里面有多个用例，都调用了此fixture，那么此fixture只在该class里所有用例开始前执行一次

```
import pytest

@pytest.fixture(scope="class")
def first():
    print("\n获取用户名,scope为class级别只运行一次")
    a = "yoyo"
    return a

class TestCase():
    def test_1(self, first):
        '''用例传fixture'''
        print("测试账号：%s" % first)
        assert first == "yoyo"

    def test_2(self, first):
        '''用例传fixture'''
        print("测试账号：%s" % first)
        assert first == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture9.py"])
```

运行结果：

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\YOYO\fixt, inifile:
plugins: rerunfailures-4.1, metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 2 items

test_fixture9.py 
获取用户名,scope为class级别只运行一次
测试账号：yoyo
.测试账号：yoyo
.

========================== 2 passed in 0.13 seconds ===========================
```

#### scope="module"

fixture为module级别时，在当前.py脚本里面所有用例开始前只执行一次

```
import pytest

@pytest.fixture(scope="module")
def first():
    print("\n获取用户名,scope为module级别当前.py模块只运行一次")
    a = "yoyo"
    return a


def test_1(first):
    '''用例传fixture'''
    print("测试账号：%s" % first)
    assert first == "yoyo"

class TestCase():
    def test_2(self, first):
        '''用例传fixture'''
        print("测试账号：%s" % first)
        assert first == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture10.py"])
```

运行结果

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\YOYO\fixt, inifile:
plugins: rerunfailures-4.1, metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 2 items

test_fixture10.py 
获取用户名,scope为module级别当前.py模块只运行一次
测试账号：yoyo
.测试账号：yoyo
.

========================== 2 passed in 0.14 seconds ===========================
```

#### scope="session"

fixture为session级别是可以跨.py模块调用的,也就是当我们有多个.py文件的用例时候，如果多个用例只需调用一次fixture，那就可以设置为scope="session"，并且写到conftest.py文件里

conftest.py文件名称是固定的，pytest会自动识别该文件。放到工程的根目录下，就可以全局调用了，如果放到某个package包下，那就只在该package内有效

```
conftest.py

import pytest

@pytest.fixture(scope="session")
def first():
    print("\n获取用户名,scope为session级别多个.py模块只运行一次")
    a = "yoyo"
    return a
```

test_fixture11.py和test_fixture12.py用例脚本

```
# test_fixture11.py

import pytest
def test_1(first):
    '''用例传fixture'''
    print("测试账号：%s" % first)
    assert first == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture11.py"])


# test_fixture12.py
import pytest

def test_2(first):
    '''用例传fixture'''
    print("测试账号：%s" % first)
    assert first == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_fixture12.py"])
```

如果想同时运行test_fixture11.py和test_fixture12.py，在cmd执行

> pytest -s test_fixture11.py test_fixture12.py

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\YOYO\fixt, inifile:
plugins: rerunfailures-4.1, metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 2 items

test_fixture11.py .                                                      [ 50%]
test_fixture12.py .                                                      [100%]

========================== 2 passed in 0.03 seconds ===========================

D:\YOYO\fixt>pytest -s test_fixture11.py test_fixture12.py
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: D:\YOYO\fixt, inifile:
plugins: rerunfailures-4.1, metadata-1.7.0, html-1.19.0, allure-adaptor-1.7.10
collected 2 items

test_fixture11.py
获取用户名,scope为session级别多个.py模块只运行一次
测试账号：yoyo
.
test_fixture12.py 测试账号：yoyo
.

========================== 2 passed in 0.03 seconds ===========================
```

# [pytest文档25-conftest.py作用范围](https://www.cnblogs.com/yoyoketang/p/9769242.html)

#### 前言

一个测试工程下是可以有多个conftest.py的文件，一般在工程根目录放一个conftest.py起到全局作用。
在不同的测试子目录也可以放conftest.py，作用范围只在该层级以及以下目录生效。

#### conftest层级关系

在web_conf_py项目工程下建两个子项目baidu、blog，并且每个目录下都放一个conftest.py和__init__.py（python的每个package必须要有__init__.py）

```
web_conf_py是工程名称

├─baidu
│  │  conftest.py
│  │  test_1_baidu.py
│  │  __init__.py
│  
│          
├─blog
│  │  conftest.py
│  │  test_2_blog.py
│  │  __init__.py
│   
│  conftest.py
│  __init__.py
        
```

![img](https://img2018.cnblogs.com/blog/1070438/201810/1070438-20181010212130463-1055127825.png)

#### 案例分析

web_conf_py工程下conftest.py文件代码案例

```
# web_conf_py/conftest.py
import pytest

@pytest.fixture(scope="session")
def start():
    print("\n打开首页")
```

baidu目录下conftest.py和test_1_baidu.py

```
# web_conf_py/baidu/conftest.py
import pytest

@pytest.fixture(scope="session")
def open_baidu():
    print("打开百度页面_session")


# web_conf_py/baidu/test_1_baidu.py

import pytest

def test_01(start, open_baidu):
    print("测试用例test_01")
    assert 1

def test_02(start, open_baidu):
    print("测试用例test_02")
    assert 1

if __name__ == "__main__":
    pytest.main(["-s", "test_1_baidu.py"])
```

运行test_1_baidu.py结果可以看出，start和open_baidu是session级别的，只运行一次

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\web_conf_py\baidu, inifile:
plugins: metadata-1.7.0, html-1.19.0
collected 2 items

test_1_baidu.py 
打开首页
打开百度页面_session
测试用例test_01
.测试用例test_02
.

========================== 2 passed in 0.01 seconds ===========================
```

blog目录下conftest.py和test_2_blog.py代码

```
# web_conf_py/blog/conftest.py
import pytest

@pytest.fixture(scope="function")
def open_blog():
    print("打开blog页面_function")


# web_conf_py/blog/test_2_blog.py

import pytest

def test_03(start, open_blog):
    print("测试用例test_03")
    assert 1

def test_04(start, open_blog):
    print("测试用例test_04")
    assert 1

def test_05(start, open_baidu):
    '''跨模块调用baidu模块下的conftest'''
    print("测试用例test_05,跨模块调用baidu")
    assert 1

if __name__ == "__main__":
    pytest.main(["-s", "test_2_blog.py"])
```

运行结果可以看出，start起到全局作用，blog目录下的open_blog是function级别，每个用例调用一次。
test_05(start, open_baidu)用例不能跨模块调用baidu模块下的open_baidu，所以test_05用例会运行失败

```
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\web_conf_py\blog, inifile:
plugins: metadata-1.7.0, html-1.19.0
collected 3 items

test_2_blog.py 
打开首页
打开blog页面_function
测试用例test_03
.打开blog页面_function
测试用例test_04
.E

=================================== ERRORS ====================================
__________________________ ERROR at setup of test_05 __________________________
file E:\YOYO\web_conf_py\blog\test_2_blog.py, line 11
  def test_05(start, open_baidu):
E       fixture 'open_baidu' not found
>       available fixtures: cache, capfd, capfdbinary, caplog, capsys, capsysbinary, doctest_namespace, metadata, monkeypatch, open_blog, pytestconfig, record_property, record_xml_attribute, record_xml_property, recwarn, start, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

E:\YOYO\web_conf_py\blog\test_2_blog.py:11
====================== 2 passed, 1 error in 0.02 seconds ======================
```

# [pytest文档26-运行上次失败用例(--lf 和 --ff）](https://www.cnblogs.com/yoyoketang/p/9769559.html)

#### 前言

“80%的bug集中在20%的模块，越是容易出现bug的模块，bug是越改越多“平常我们做手工测试的时候，比如用100个用例需要执行，其中10个用例失败了，
当开发修复完bug后，我们一般是重点测上次失败的用例。
那么自动化测试也一样，当用例特别多时，为了节省时间，第一次部分用例失败了，修复完之后，可以只测上次失败的用例。

#### pytest -h

命令行输入pytest -h，找到里面两个命令行参数： --lf 和 --ff

- --lf, --last-failed 只重新运行上次运行失败的用例（或如果没有失败的话会全部跑）
- --ff, --failed-first 运行所有测试，但首先运行上次运行失败的测试（这可能会重新测试，从而导致重复的fixture setup/teardown）

![img](https://img2018.cnblogs.com/blog/1070438/201810/1070438-20181010220836585-2129159797.png)

#### --lf 和 --ff

lf是last-failed的缩写，我第一次运行全部测试用例有4个通过passed， 2个失败failed，1个error

```
E:\YOYO\web_conf_py>pytest
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\web_conf_py, inifile:
plugins: metadata-1.7.0, html-1.19.0
collected 7 items

baidu\test_1_baidu.py ..                                                 [ 28%]
baidu\test_2.py FF                                                       [ 57%]
blog\test_2_blog.py ..E                                                  [100%]

=================================== ERRORS ====================================
__________________________ ERROR at setup of test_05 __________________________
file E:\YOYO\web_conf_py\blog\test_2_blog.py, line 11
  def test_05(start, open_baidu):
E       fixture 'open_baidu' not found
>       available fixtures: cache, capfd, capfdbinary, caplog, capsys, capsysbinary, doctest_namespace, metadata, monkeypatch, open_blog, pytestconfig, record_property, record_xml_attribute, record_xml_property, recwarn, start, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

E:\YOYO\web_conf_py\blog\test_2_blog.py:11
================================== FAILURES ===================================
___________________________________ test_06 ___________________________________

start = None, open_baidu = None

    def test_06(start, open_baidu):
        print("测试用例test_01")
>       assert 1==2
E       assert 1 == 2

baidu\test_2.py:5: AssertionError
---------------------------- Captured stdout call -----------------------------
测试用例test_01
___________________________________ test_07 ___________________________________

start = None, open_baidu = None

    def test_07(start, open_baidu):
        print("测试用例test_02")
>       assert 1==2
E       assert 1 == 2

baidu\test_2.py:9: AssertionError
---------------------------- Captured stdout call -----------------------------
测试用例test_02
================= 2 failed, 4 passed, 1 error in 0.21 seconds =================
```

如果只想运行其中2个failed的和1error用例，那么可以直接在cmd输入指令

> pytest --lf

```
E:\YOYO\web_conf_py>pytest --lf
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\web_conf_py, inifile:
plugins: metadata-1.7.0, html-1.19.0
collected 7 items / 4 deselected
run-last-failure: rerun previous 3 failures

baidu\test_2.py FF                                                       [ 66%]
blog\test_2_blog.py E                                                    [100%]

========================== 2 failed, 4 deselected, 1 error in 0.16 seconds===========================
```

如果想先运行上次失败的，后运行其它通过的用例

> pytest --ff

```
E:\YOYO\web_conf_py>pytest --ff
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\web_conf_py, inifile:
plugins: metadata-1.7.0, html-1.19.0
collected 7 items
run-last-failure: rerun previous 3 failures first

baidu\test_2.py FF                                                       [ 28%]
blog\test_2_blog.py E                                                    [ 42%]
baidu\test_1_baidu.py ..                                                 [ 71%]
blog\test_2_blog.py ..                                                   [100%]

================= 2 failed, 4 passed, 1 error in 0.14 seconds =================
```

# [pytest文档27-pytest分布式执行（pytest-xdist）](https://www.cnblogs.com/yoyoketang/p/9775646.html)

#### 前言

平常我们手工测试用例非常多时，比如有1千条用例，假设每个用例执行需要1分钟。如果一个测试人员执行需要1000分钟才能执行完，当项目非常紧急的时候，
我们会用测试人力成本换取时间成本，这个时候多找个小伙伴把任务分成2部分，于是时间缩减一半。如果是十个人一起执行，1000个用例理论上只需100分钟就能完成，时间缩短到了1/10。大大节省的测试时间，为项目节省了时间成本。

- pytest 3.6.3
- pytest-xdist 1.23.2

同样道理，当我们测试用例非常多的时候，一条条执行，很显然会比较慢，那么如何让测试用例并行执行呢，这就是我们接下来要讲的pytest分布式执行插件pytest-xdist

#### pytest-xdist

cmd里面使用pip安装,目前版本号Version: 1.23.2

> pip install pytest-xdist

```
>pip show pytest-xdist
Name: pytest-xdist
Version: 1.23.2
Summary: pytest xdist plugin for distributed testing and loop-on-failing modes
Home-page: https://github.com/pytest-dev/pytest-xdist
Author: holger krekel and contributors
Author-email: pytest-dev@python.org,holger@merlinux.eu
License: MIT
Location: e:\python36\lib\site-packages
Requires: execnet, pytest-forked, six, pytest
```

pytest-xdist官网地址：[【Home-page: https://github.com/pytest-dev/pytest-xdist】](https://github.com/pytest-dev/pytest-xdist)

该pytest-xdist插件扩展了一些独特的测试执行模式pytest：

- 测试运行并行化：如果有多个CPU或主机，则可以将它们用于组合测试运行。会加快运行速度
- --looponfail：在子进程中重复运行测试。每次运行之后，pytest会等待，直到项目中的文件发生更改，然后重新运行以前失败的测试。
	重复此过程直到所有测试通过，之后再次执行完整运行。
- 多平台覆盖：您可以指定不同的Python解释器或不同的平台，并在所有平台上并行运行测试。
	在远程运行测试之前，pytest有效地将您的程序源代码“rsyncs”到远程位置。报告所有测试结果并显示给您的本地终端。您可以指定不同的Python版本和解释器。
	如果您想知道pytest-xdist如何在幕后工作，可以看这里[【OVERVIEW】](https://github.com/pytest-dev/pytest-xdist/blob/master/OVERVIEW.md)

#### 并行测试

多cpu并行执行用例，直接加个-n参数即可，后面num参数就是并行数量，比如num设置为3

> pytest -n 3

运行以下代码，项目结构如下

```
web_conf_py是项目工程名称
│  conftest.py
│  __init__.py
│              
├─baidu
│  │  conftest.py
│  │  test_1_baidu.py
│  │  test_2.py
│  │  __init__.py 
│          
├─blog
│  │  conftest.py
│  │  test_2_blog.py
│  │  __init__.py      
```

代码参考：

```
# web_conf_py/conftest.py
import pytest

@pytest.fixture(scope="session")
def start():
    print("\n打开首页")
    return "yoyo"

# web_conf_py/baidu/conftest.py
import pytest

@pytest.fixture(scope="session")
def open_baidu():
    print("打开百度页面_session")

# web_conf_py/baidu/test_1_baidu.py
import pytest
import time

def test_01(start, open_baidu):
    print("测试用例test_01")
    time.sleep(1)
    assert start == "yoyo"

def test_02(start, open_baidu):
    print("测试用例test_02")
    time.sleep(1)
    assert start == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_1_baidu.py"])


# web_conf_py/baidu/test_2.py
import pytest
import time

def test_06(start, open_baidu):
    print("测试用例test_01")
    time.sleep(1)
    assert start == "yoyo"
def test_07(start, open_baidu):
    print("测试用例test_02")
    time.sleep(1)
    assert start == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_2.py"])


# web_conf_py/blog/conftest.py
import pytest

@pytest.fixture(scope="function")
def open_blog():
    print("打开blog页面_function")

# web_conf_py/blog/test_2_blog.py

import pytest
import time
def test_03(start, open_blog):
    print("测试用例test_03")
    time.sleep(1)
    assert start == "yoyo"

def test_04(start, open_blog):
    print("测试用例test_04")
    time.sleep(1)
    assert start == "yoyo"

def test_05(start, open_blog):
    '''跨模块调用baidu模块下的conftest'''
    print("测试用例test_05,跨模块调用baidu")
    time.sleep(1)
    assert start == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_2_blog.py"])
```

正常运行需要消耗时间：7.12 seconds

```
E:\YOYO\web_conf_py>pytest
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\web_conf_py, inifile:
plugins: xdist-1.23.2, metadata-1.7.0, html-1.19.0, forked-0.2
collected 7 items

baidu\test_1_baidu.py ..                                                 [ 28%]
baidu\test_2.py ..                                                       [ 57%]
blog\test_2_blog.py ...                                                  [100%]

========================== 7 passed in 7.12 seconds ===========================
```

设置并行运行数量为3，消耗时间：3.64 seconds，大大的缩短了用例时间

```
E:\YOYO\web_conf_py>pytest -n 3
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\web_conf_py, inifile:
plugins: xdist-1.23.2, metadata-1.7.0, html-1.19.0, forked-0.2
gw0 [7] / gw1 [7] / gw2 [7]
scheduling tests via LoadScheduling
.......                                                                  [100%]
========================== 7 passed in 3.64 seconds ===========================
```

#### 测试报告

使用pytest-xdist插件也能生成html报告,完美支持pytest-html插件

> pytest -n 3 --html=report.html --self-contained-html

![img](https://img2018.cnblogs.com/blog/1070438/201810/1070438-20181011225632340-198619275.png)

# [pytest文档28-重复执行用例（pytest-repeat）](https://www.cnblogs.com/yoyoketang/p/9800961.html)

#### 前言

平常在做功能测试的时候，经常会遇到某个模块不稳定，偶然会出现一些bug，对于这种问题我们会针对此用例反复执行多次，最终复现出问题来。
自动化运行用例时候，也会出现偶然的bug，可以针对单个用例，或者针对某个模块的用例重复执行多次。

#### pytest-repeat

pytest-repeat是pytest的一个插件，用于重复执行单个用例，或多个测试用例，并指定重复次数，pytest-repeat支持的版本：

- Python 2.7, 3.4+ 或 PyPy
- py.test 2.8或更高

使用pip安装pytest-repeat

> pip install pytest-repeat

使用--count命令行选项指定要运行测试用例和测试次数

> py.test --count=10 test_file.py

#### 重复执行--count

运行以下代码，项目结构如下

```
web_conf_py是项目工程名称
│  conftest.py  
│  __init__.py
│              
├─baidu
│  │  conftest.py
│  │  test_1_baidu.py
│  │  test_2.py
│  │  __init__.py 
│          
├─blog
│  │  conftest.py
│  │  test_2_blog.py
│  │  __init__.py      
```

代码参考：

```
# web_conf_py/conftest.py
import pytest

@pytest.fixture(scope="session")
def start():
    print("\n打开首页")
    return "yoyo"

# web_conf_py/baidu/conftest.py
import pytest

@pytest.fixture(scope="session")
def open_baidu():
    print("打开百度页面_session")

# web_conf_py/baidu/test_1_baidu.py
import pytest
import time

def test_01(start, open_baidu):
    print("测试用例test_01")
    time.sleep(1)
    assert start == "yoyo"

def test_02(start, open_baidu):
    print("测试用例test_02")
    time.sleep(1)
    assert start == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_1_baidu.py"])


# web_conf_py/baidu/test_2.py
import pytest
import time

def test_06(start, open_baidu):
    print("测试用例test_01")
    time.sleep(1)
    assert start == "yoyo"
def test_07(start, open_baidu):
    print("测试用例test_02")
    time.sleep(1)
    assert start == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_2.py"])
```

cmd进入到工程目录后，不带--count参数只会执行一次

> pytest baidu/test_1_baidu.py -s

```
E:\YOYO\web_conf_py>pytest baidu/test_1_baidu.py -s
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\web_conf_py, inifile:
plugins: xdist-1.23.2, repeat-0.7.0, metadata-1.7.0, html-1.19.0, forked-0.2
collected 2 items

baidu\test_1_baidu.py
打开首页
打开百度页面_session
测试用例test_01
.测试用例test_02
.

========================== 2 passed in 1.03 seconds ===========================
```

加上参数--count=5，用例会重复执行5次

> pytest baidu/test_1_baidu.py -s --count=5

```
E:\YOYO\web_conf_py>pytest baidu/test_1_baidu.py -s --count=5
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\web_conf_py, inifile:
plugins: xdist-1.23.2, repeat-0.7.0, metadata-1.7.0, html-1.19.0, forked-0.2
collected 10 items

baidu\test_1_baidu.py
打开首页
打开百度页面_session
测试用例test_01
.测试用例test_01
.测试用例test_01
.测试用例test_01
.测试用例test_01
.测试用例test_02
.测试用例test_02
.测试用例test_02
.测试用例test_02
.测试用例test_02
.

========================== 10 passed in 5.06 seconds ==========================
```

从运行的用例结果看，是先重复5次test_01，再重复5次test_02，有时候我们希望执行的顺序是test_01,test_02按这样顺序重复五次，接下来就用到一个参数--repeat-scope

#### --repeat-scope

--repeat-scope类似于pytest fixture的scope参数，--repeat-scope也可以设置参数： `session` ， `module`，`class`或者`function`（默认值）

- `function`（默认）范围针对每个用例重复执行，再执行下一个用例
- `class` 以class为用例集合单位，重复执行class里面的用例，再执行下一个
- `module` 以模块为单位，重复执行模块里面的用例，再执行下一个
- `session` 重复整个测试会话，即所有收集的测试执行一次，然后所有这些测试再次执行等等

使用`--repeat-scope=session`重复执行整个会话用例

> pytest baidu/test_1_baidu.py -s --count=5 --repeat-scope=session

```
E:\YOYO\web_conf_py>pytest baidu/test_1_baidu.py -s --count=5 --repeat-scope=session
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\web_conf_py, inifile:
plugins: xdist-1.23.2, repeat-0.7.0, metadata-1.7.0, html-1.19.0, forked-0.2
collected 10 items

baidu\test_1_baidu.py
打开首页
打开百度页面_session
测试用例test_01
.测试用例test_02
.测试用例test_01
.测试用例test_02
.测试用例test_01
.测试用例test_02
.测试用例test_01
.测试用例test_02
.测试用例test_01
.测试用例test_02
.

========================== 10 passed in 5.07 seconds ==========================
```

#### @pytest.mark.repeat(count)

如果要在代码中标记要重复多次的测试，可以使用`@pytest.mark.repeat(count)`装饰器

```
# test_1_baidu.py
import pytest
import time

def test_01(start, open_baidu):
    print("测试用例test_01")
    time.sleep(0.5)
    assert start == "yoyo"

@pytest.mark.repeat(5)
def test_02(start, open_baidu):
    print("测试用例test_02")
    time.sleep(0.5)
    assert start == "yoyo"

if __name__ == "__main__":
    pytest.main(["-s", "test_1_baidu.py"])
```

这样执行用例时候，就不用带上--count参数，只针对test_02重复执行5次

```
E:\YOYO\web_conf_py>pytest baidu/test_1_baidu.py -s
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-3.6.3, py-1.5.4, pluggy-0.6.0
rootdir: E:\YOYO\web_conf_py, inifile:
plugins: xdist-1.23.2, repeat-0.7.0, metadata-1.7.0, html-1.19.0, forked-0.2
collected 6 items

baidu\test_1_baidu.py
打开首页
打开百度页面_session
测试用例test_01
.测试用例test_02
.测试用例test_02
.测试用例test_02
.测试用例test_02
.测试用例test_02
.

========================== 6 passed in 3.05 seconds ===========================
```

#### 重复测试直到失败

如果您正在尝试诊断间歇性故障，那么一遍又一遍地运行相同的测试直到失败是有用的。您可以将pytest的-x选项与pytest-repeat结合使用，以强制测试运行器在第一次失败时停止。例如：

> py.test --count=1000 -x test_file.py

这将尝试运行test_file.py 1000次，但一旦发生故障就会停止

# [pytest文档29-allure-pytest(最新最全，保证能搞成功！)](https://www.cnblogs.com/yoyoketang/p/12004145.html)

#### 前言

之前写了个pytest的allure相关的教程，只是停留在环境搭建完成，后续一直没用，小编一直不喜欢这种花里胡哨的报告。
没办法，领导就喜欢这种，小伙伴们也喜欢，所以还是得把allure用起来，年底了，给领导一个漂亮的报告，也好加鸡腿
之前用的是pytest-allure-adaptor插件，一年多前写的了，很古老了，跟不上时代了，不能吸引当代的小青年，这里用最新的allure-pytest，符合当代小青年的口味。

#### allure-pytest 环境准备

windows环境相关：

python 3.6版本
pytest 4.5.0版本
allure-pytest 2.8.6 最新版

使用pip安装pytest和allure-pytest,加上--index-url地址，下载会快一些

```
pip install pytest==4.5.0 --index-url https://pypi.douban.com/simple
pip install allure-pytest==2.8.6 --index-url https://pypi.douban.com/simple
```

安装完成之后，打开一个你之前写的pytest脚本，看能不正常使用，如果报错：AttributeError: module 'allure' has no attribute 'severity_level'
这个是之前 pytest-allure-adaptor 这个插件与 allure-pytest 不能共存，卸载掉 pytest-allure-adaptor

> pip uninstall pytest-allure-adaptor

#### allure命令行工具

allure是一个命令行工具，需要去github上下载最新版https://github.com/allure-framework/allure2/releases

![img](github上下载allure.png)

下载完成之后，解压到本地电脑

![img](本地1.png)

![img](本地2.png)

把bin目录添加到环境变量Path下

![img](本地3.png)

#### 用例demo

conftest.py内容

```
import pytest


@pytest.fixture(scope="session")
def login():
    print("用例先登录")
```

test_allure_demo.py内容

```
import allure
import pytest

@allure.step("步骤1:点xxx")
def step_1():
    print("111")

@allure.step("步骤2:点xxx")
def step_2():
    print("222")

@allure.feature("编辑页面")
class TestEditPage():
    '''编辑页面'''

    @allure.story("这是一个xxx的用例")
    def test_1(self, login):
        '''用例描述：先登录，再去执行xxx'''
        step_1()
        step_2()
        print("xxx")


    @allure.story("打开a页面")
    def test_2(self, login):
        '''用例描述：先登录，再去执行yyy'''
        print("yyy")
```

#### 运行用例

cd到test_allure_demo.py所在的目录文件，命令行执行

> pytest --alluredir ./report/allure_raw

```
D:\soft\code\xuexipytest>pytest --alluredir ./report/allure_raw
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1
rootdir: D:\soft\code\xuexipytest
plugins: allure-pytest-2.8.6, forked-0.2, html-1.19.0, metadata-1.7.0, repeat-0.7.0, xdist-1.23.2
collected 9 items

case\test_allure_demo.py ..                                              [ 22%]
case\test_x.py ......                                                    [ 88%]
case\test_y.py .                                                         [100%]

============================== 9 passed in 0.21s ==============================
```

执行完成后，在当前目录下，report目录会生成一个allure_raw的原始文件，这个只是测试报告的原始文件，不能打开成html的报告

![img](pycharm01.png)

打开html的报告需要启动allure服务，启动命令如下

> allure serve report/allure_raw

启动服务,它会自动给个端口，直接用默认浏览器打开了

```
D:\soft\code\xuexipytest>allure serve report/allure_raw
Generating report to temp directory...
Report successfully generated to C:\Users\dell\AppData\Local\Temp\6056757827461248074\allure-report
Starting web server...
2019-12-08 00:41:09.921:INFO::main: Logging initialized @2228ms to org.eclipse.jetty.util.log.StdErrLog
Server started at <http://192.168.1.125:35346/>. Press <Ctrl+C> to exit
```

#### 查看报告

浏览器上打开的报告内容

![img](报告01.png)

点 EN 按钮可以查看中文报告

![img](报告02.png)

打开测试套件，可以查看报告的详情，显示的还是很详细的

🔺参考这篇jenkins邮件发送，https://www.cnblogs.com/yoyoketang/p/12174056.html

# [pytest文档30-功能用例与自动化用例完美对接(allure)](https://www.cnblogs.com/yoyoketang/p/12005288.html)

#### 前言

做自动化做久了，经常会思考一个问题，到底别人是怎么做的自动化，跟自己的有啥不一样，看过不少书和资料，都是停留在demo的层面。
真正把自动化做的好的大牛又不屑于分享自己的劳动成果，所以大部分情况就是一群菜鸡在群里互啄，停留在初级入门的demo层面上。
到底自动化要达到什么样的效果呢？这里我把最近的研究成果分享下，有经验的小伙伴也可以一起交流下。

#### 功能用例

我一直认为一切的自动化用例是基于功能测试用例的， 脱离了功能测试用例，你的代码写的再漂亮，那也仅仅是show代码的。
面试的时候经常会遇到一个问题，一般领导型的面试官会问：你们自动化做到了什么程度？自动化用例覆盖率达到了多少？

自动化用例覆盖率是一个很好的衡量标准，比如你功能测试用例有100条，你的自动化用例写了90条，用例覆盖率是90%？当然不是！！！
你的自动化用例如果跟功能用例搭不上边，那都是无效用例，覆盖率也许是0%，仅仅是你自己瞎写的！

所以自动化用例是去翻译你的功能用例 ，一个一个去覆盖，让功能case,变成自动化用例的case,一一对应起来的（没写过功能用例的，后面就不用看了）。

写功能用例的平台有很多，比如jira,禅道，testlink等，这里以禅道系统为例，比如我的"编辑文章分类"模块下了3个用例

![img](https://img2018.cnblogs.com/blog/1070438/201912/1070438-20191208120848978-799121945.png)

其中的一条用例是这样的，有前置条件，用例的步骤和期望结果，这才是一个标准的用例

![img](https://img2018.cnblogs.com/blog/1070438/201912/1070438-20191208120949737-1636679309.png)

#### 自动化用例

功能用例写完之后，接着是如何去用代码去实现功能用例，这里用的是pytest框架+allure报告，其中一条用例的部分代码应该如下

- feature 对应模块名称
- story 对应用例的标题
- testcase 对应禅道系统的bug用例url地址，关联起来
- issue 如果这个用例有bug，应该关联对应的bug地址
- 用例描述： 对应def下的描述步骤

```
import allure
# 上海-悠悠，QQ交流群：750815713
# 博客地址：https://www.cnblogs.com/yoyoketang/

@allure.feature("编辑分类文章")
class TestArticleclassify():
    '''编辑文章分类'''


    @allure.story("登录-编辑文章分类，重复保存，保存失败")
    @allure.issue("http://49.235.92.12:8080/zentao/bug-view-1.html")  # 禅道bug地址
    @allure.testcase("http://49.235.92.12:8080/zentao/testcase-view-5-1.html")  # 禅道用例连接地址
    def test_edit_classify5(self, login):
        '''用例描述：编辑文章分类-输入重复的分类，保存失败，不能添加重复的
        setup: 登录login
        step1: 编辑文章分类，输入文章类别，如：计算机
        step2: 点保存按钮
        step3: 重新打开编辑页，输入：计算机
        step4: 再次点保存按钮
        assert: 保存失败，提示：已存在
        '''
        driver = login
        edit = ArticleclassifyPage(driver)
        edit.click_classify_nav()
        edit.edit_classify("计算机")
        res2 = edit.is_edit_classify_success("计算机")
        print("编辑是否成功：%s"%res2)
        assert res2  # 断言
```

前置条件：login,应该是单独抽出来的写到conftest.py，作为一个前置fixture功能

```
import pytest
from selenium import webdriver
from pages.login_page import LoginPage
import time
# 上海-悠悠，QQ交流群：750815713
# 博客地址：https://www.cnblogs.com/yoyoketang/

# request 内置的fixture

@pytest.fixture(scope="session")
def driver(request):
    '''只打开浏览器和关闭浏览器'''
    driver = webdriver.Chrome()
    driver.maximize_window() # 最大化

    def end():
        print("全部用例执行完后 teardown quit dirver")
        time.sleep(5)
        driver.quit()

    request.addfinalizer(end)
    return driver

@pytest.fixture(scope="session")
def login(driver):
    web = LoginPage(driver)
    web.login()
    return driver
```

LoginPage 页面的封装，可以添加操作步骤,step对应每个步骤，我这里登录几个步骤写一起了，也可写的更详细

```
# 上海-悠悠，QQ交流群：750815713
# 博客地址：https://www.cnblogs.com/yoyoketang/

class LoginPage(Base):

    loc_用户名 = ("id", "id_username")
    loc_密码 = ("id", "id_password")
    loc_登录按钮 = ("xpath", "//*[text()='登录']")

    # 判断登录成功
    loc_后台页面 = ("xpath", "//*[text()='后台页面']")

    @allure.step("登录")
    def login(self, username="admin", password="yoyo123456"):
        '''登录'''
        self.driver.get(login_url)
        self.send(self.loc_用户名, username)
        self.send(self.loc_密码, password)
        self.click(self.loc_登录按钮)

    @allure.step("登录结果判断")
    def is_login_success(self):
        '''判断是否登录成功 True  False'''
        result = self.is_element_exist(self.loc_后台页面)
        return result
```

#### 测试报告

接着查看运行结果的测试报告，展示效果如下

![img](https://img2018.cnblogs.com/blog/1070438/201912/1070438-20191208122507128-224232000.png)

这样我们只需拿着测试报告，就可以交出完美的答案了！

# [pytest文档31-allure标记用例级别severity](https://www.cnblogs.com/yoyoketang/p/12194550.html)

#### 前言

我们在做功能测试的时候，执行完一轮测试用例，输出测试报告的时候，会有统计缺陷的数量和等级。
在做自动化测试的过程中，当你的测试用例越来越多的时候，如果执行一轮测试发现了几个测试不通过，我们也希望能快速统计出缺陷的等级。
pytest结合allure框架可以对用例的等级做详细的划分。

#### 用例等级

allure对用例的等级划分成五个等级

- blocker　 阻塞缺陷（功能未实现，无法下一步）
- critical　　严重缺陷（功能点缺失）
- normal　　 一般缺陷（边界情况，格式错误）
- minor　 次要缺陷（界面错误与ui需求不符）
- trivial　　 轻微缺陷（必须项无提示，或者提示不规范）

比如我的用例有以下4条

![img](https://img2018.cnblogs.com/blog/1070438/202001/1070438-20200114223721238-1247667434.png)
那么对应的用例的等级应该是

- 修改个人信息-sex参数为空 这个属于边界值情况的测试，应该是normal级别
- 修改个人信息-sex参数传F和M两种类型，成功(枚举类型) 这个是针对接口的功能点详细测试 critical级别
- 修改个人信息-修改不是本人的用户信息，无权限操作 这个是针对接口的功能点详细测试 critical级别
- 修改个人信息-修改自己的个人信息，修改成功 这是用例是测试主流程 blocker级别

#### pytest用例

根据测试用例的重要性划分测试用例等级，如果没指定等级，默认为normal级别

```
import pytest
import allure
'''
作者：上海-悠悠 qq交流群：874033608

@allure.severity装饰器按严重性级别来标记case　　　
执行指定测试用例 --allure-severities blocker
BLOCKER = 'blocker'　　阻塞缺陷
CRITICAL = 'critical'　严重缺陷
NORMAL = 'normal'　　  一般缺陷
MINOR = 'minor'　　    次要缺陷
TRIVIAL = 'trivial'　　轻微缺陷　
'''


@allure.severity("normal")
def test_case_1():
    '''修改个人信息-sex参数为空'''
    print("test case 11111111")
    

@allure.severity("critical")
def test_case_2():
    '''修改个人信息-sex参数传F和M两种类型，成功(枚举类型)'''
    print("test case 222222222")


@allure.severity("critical")
def test_case_3():
    '''修改个人信息-修改不是本人的用户信息，无权限操作'''
    print("test case 333333333")

@allure.severity("blocker")
def test_case_4():
    '''修改个人信息-修改自己的个人信息，修改成功'''
    print("test case 4444444")


def test_case_5():
    '''没标记severity的用例默认为normal'''
    print("test case 5555555555")
```

cd到用例的目录，执行用例，查看报告

> pytest --alluredir ./report/allure
> allure serve ./report/allure
> 查看报告详情
> ![img](https://img2018.cnblogs.com/blog/1070438/202001/1070438-20200114225048288-589956314.png)

#### 统计缺陷

如果执行用例的过程中有测试用例不通过的情况，也可以统计缺陷的严重等级

```
# 修改上面2个用例，故意让用例失败
@allure.severity("blocker")
def test_case_4():
    '''修改个人信息-修改自己的个人信息，修改成功'''
    print("test case 4444444")
    assert 1==2


def test_case_5():
    '''没标记severity的用例默认为normal'''
    print("test case 5555555555")
    assert 1==2
```

重新执行用例，查看报告-图表

![img](https://img2018.cnblogs.com/blog/1070438/202001/1070438-20200114225347303-989442662.png)

#### allure命令行参数allure-severities

pytest -h可以查看到allure相关的几个命令行参数
--allure-severities=SEVERITIES_SET
Comma-separated list of severity names. Tests only
with these severities will be run. Possible values
are: blocker, critical, normal, minor, trivial.
如果有很多测试用例，现在只想做个快速的回归测试，只测试用例级别为blocker和critical级别的测试用例

> pytest --alluredir ./report/allure --allure-severities blocker,critical

也可以这样写

> pytest --alluredir=./report/allure --allure-severities=blocker,critical

如果只执行blocker级别的用例

> pytest --alluredir=./report/allure --allure-severities=blocker

# [pytest文档33-Hooks函数获取用例执行结果(pytest_runtest_makereport)](https://www.cnblogs.com/yoyoketang/p/12609871.html)

#### 前言

pytest提供的很多钩子(Hooks)方法方便我们对测试用例框架进行二次开发，可以根据自己的需求进行改造。
先学习下pytest_runtest_makereport这个钩子方法，可以更清晰的了解用例的执行过程，并获取到每个用例的执行结果。

#### pytest_runtest_makereport

先看下相关的源码，在`_pytest/runner.py`下，可以导入之后，点进去查看

```
from _pytest import runner

# 对应源码
def pytest_runtest_makereport(item, call):
    """ return a :py:class:`_pytest.runner.TestReport` object
    for the given :py:class:`pytest.Item` and
    :py:class:`_pytest.runner.CallInfo`.
    """
```

这里item是测试用例，call是测试步骤，具体执行过程如下：

- 先执行when='setup' 返回setup 的执行结果
- 然后执行when='call' 返回call 的执行结果
- 最后执行when='teardown'返回teardown 的执行结果

#### 运行案例

conftest.py 写 pytest_runtest_makereport 内容，打印运行过程和运行结果

```
# conftest.py 
import pytest


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    print('------------------------------------')

    # 获取钩子方法的调用结果
    out = yield
    print('用例执行结果', out)

    # 3. 从钩子方法的调用结果中获取测试报告
    report = out.get_result()

    print('测试报告：%s' % report)
    print('步骤：%s' % report.when)
    print('nodeid：%s' % report.nodeid)
    print('description:%s' % str(item.function.__doc__))
    print(('运行结果: %s' % report.outcome))
```

test_a.py写一个简单的用例

```
def test_a():
    '''用例描述:test_a'''
    print("上海-悠悠")
```

运行结果如下

```
D:\soft\code\pytest_jenkins_demo\demo>pytest -s
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1
rootdir: D:\demo
plugins: html-1.19.0,
collected 1 item

test_a.py ------------------------------------
用例执行结果 <pluggy.callers._Result object at 0x0000027C547332B0>
测试报告：<TestReport 'test_a.py::test_a' when='setup' outcome='passed'>
步骤：setup
nodeid：test_a.py::test_a
description:用例描述:test_a
运行结果: passed
上海-悠悠
------------------------------------
用例执行结果 <pluggy.callers._Result object at 0x0000027C547332B0>
测试报告：<TestReport 'test_a.py::test_a' when='call' outcome='passed'>
步骤：call
nodeid：test_a.py::test_a
description:用例描述:test_a
运行结果: passed
.------------------------------------
用例执行结果 <pluggy.callers._Result object at 0x0000027C54750A20>
测试报告：<TestReport 'test_a.py::test_a' when='teardown' outcome='passed'>
步骤：teardown
nodeid：test_a.py::test_a
description:用例描述:test_a
运行结果: passed


========================== 1 passed in 0.06 seconds ===========================
```

从运行结果可以看出，运行用例的过程会经历三个阶段:setup-call-teardown,每个阶段都会返回的 Result 对象和 TestReport 对象，以及对象属性。
setup和teardown上面的用例默认都没有，结果都是passed。

#### setup和teardown

给用例写个fixture增加用例的前置和后置操作，conftest.py内容如下

```
import pytest


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    print('------------------------------------')

    # 获取钩子方法的调用结果
    out = yield
    print('用例执行结果', out)

    # 3. 从钩子方法的调用结果中获取测试报告
    report = out.get_result()

    print('测试报告：%s' % report)
    print('步骤：%s' % report.when)
    print('nodeid：%s' % report.nodeid)
    print('description:%s' % str(item.function.__doc__))
    print(('运行结果: %s' % report.outcome))

@pytest.fixture(scope="session", autouse=True)
def fix_a():
    print("setup 前置操作")
    yield 
    print("teardown 后置操作")
```

运行结果如下

![img](https://img2020.cnblogs.com/blog/1070438/202004/1070438-20200401221206514-402331379.png)

#### setup失败情况

当setup执行失败了，setup的执行结果的failed,后面的call用例和teardown都不会执行了

![img](https://img2020.cnblogs.com/blog/1070438/202004/1070438-20200401221918995-6644682.png)

此时用例的状态是:error, 也就是用例(call)都还没开始执行，就异常了。

#### call失败情况

如果setup正常执行，但是测试用例call失败了

```
@pytest.fixture(scope="session", autouse=True)
def fix_a():
    print("setup 前置操作")
    yield
    print("teardown 后置操作")
```

test_a.py用例

```
def test_a():
    '''用例描述:test_a'''
    print("上海-悠悠")
    assert 1==0
```

![img](https://img2020.cnblogs.com/blog/1070438/202004/1070438-20200401222239285-29343374.png)

那么此时运行的结果就是failed

#### teardown失败了

如果setup正常执行，测试用例call正常执行，teardown失败了，这种情况

```
@pytest.fixture(scope="session", autouse=True)
def fix_a():
    print("setup 前置操作")
    yield
    print("teardown 后置操作")
    raise Exception("teardown 失败了")
```

teat_a.py用例

```
def test_a():
    '''用例描述:test_a'''
    print("上海-悠悠")
```

![img](https://img2020.cnblogs.com/blog/1070438/202004/1070438-20200401222500108-746689433.png)

最终统计的结果： 1 passed, 1 error in 0.16 seconds

![img](https://img2020.cnblogs.com/blog/1070438/202004/1070438-20200401222754188-614197877.png)

#### 只获取call的结果

我们在写用例的时候，如果保证setup和teardown不报错情况，只关注测试用例本身的运行结果，前面的 pytest_runtest_makereport 钩子方法执行了三次。
可以加个判断：if report.when == "call"

```
import pytest
from _pytest import runner
'''
# 对应源码
def pytest_runtest_makereport(item, call):
    """ return a :py:class:`_pytest.runner.TestReport` object
    for the given :py:class:`pytest.Item` and
    :py:class:`_pytest.runner.CallInfo`.
    """
'''

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    print('------------------------------------')

    # 获取钩子方法的调用结果
    out = yield
    # print('用例执行结果', out)

    # 3. 从钩子方法的调用结果中获取测试报告
    report = out.get_result()
    if report.when == "call":
        print('测试报告：%s' % report)
        print('步骤：%s' % report.when)
        print('nodeid：%s' % report.nodeid)
        print('description:%s' % str(item.function.__doc__))
        print(('运行结果: %s' % report.outcome))

@pytest.fixture(scope="session", autouse=True)
def fix_a():
    print("setup 前置操作")
    yield
    print("teardown 后置操作")
```

运行结果
![img](https://img2020.cnblogs.com/blog/1070438/202004/1070438-20200401230344105-224155182.png)

# [pytest文档34-Hooks函数改变用例执行顺序(pytest_collection_modifyitems)](https://www.cnblogs.com/yoyoketang/p/12624000.html)

#### 前言

有一些小伙伴一直想改变pytest用例的执行顺序，实际上我们在用例设计原则上用例就不要有依赖顺序。
pytest默认执行用例是先根据项目下的文件夹名称按ascii码去收集的，module里面的用例是从上往下执行的.
pytest_collection_modifyitems 这个钩子函数顾名思义就是改变用例的执行顺序。

#### pytest_collection_modifyitems

pytest_collection_modifyitems 功能是当测试用例收集完成后，可以改变测试用例集合(items)的顺序

```
def pytest_collection_modifyitems(session, config,items):
    '''called after collection is completed. 
    you can modify the ``items`` list
    :param _pytest.main.Session session: the pytest session object
    :param _pytest.config.Config config: pytest config object
    :param List[_pytest.nodes.Item] items: list of item objects
    '''
```

items是用例对象的一个列表，改变items里面用例的顺序就可以改变用例的执行顺序了。

#### pytest默认执行顺序

先设计一个简单的 pytest 项目，有a和b两个包，分别在 test_a.py 和 test_b.py 写测试用例
![img](https://img2020.cnblogs.com/blog/1070438/202004/1070438-20200402234859055-1593815892.png)

conftest.py内容

```
import pytest
# 上海-悠悠

def pytest_collection_modifyitems(session, items):
    print("收集到的测试用例:%s"%items)
```

test_a.py内容

```
def test_a_1():
    print("测试用例a_1")

def test_a_2():
    print("测试用例a_2")
```

test_b.py内容

```
def test_b_2():
    print("测试用例b_2")

def test_b_1():
    print("测试用例b_1")
```

运行完成后可以看到收集到的测试用例，会在测试用例开始执行执行

```
D:\demo2>pytest
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1
rootdir: D:\soft\code\pytest_jenkins_demo\demo2
plugins: allure-pytest-2.8.6
collecting ... 收集到的测试用例:[<Function test_a_1>, <Function test_a_2>, <Function test_b_2>, <Function test_b_1>]
collected 4 items

a\test_aaa.py ..                                                         [ 50%]
b\test_bbb.py ..                                                         [100%]

========================== 4 passed in 0.06 seconds ===========================
```

从结果可以看出运行的时候先按模块名称ascii码去收集，单个py文件里面的用例按从上到下写的顺序收集。

#### items用例排序

如果我想改变上面的用例执行顺序，以用例名称ascii码排序。先获取到用例的名称，以用例名称排序就可以了。

```
# 上海-悠悠
def pytest_collection_modifyitems(session, items):
    print(type(items))
    print("收集到的测试用例:%s" % items)
    # sort排序，根据用例名称item.name 排序
    items.sort(key=lambda x: x.name)
    print("排序后的用例：%s" % items)
    for item in items:
        print("用例名:%s" % item.name)
```

重新执行后结果

```
D:\soft\code\pytest_jenkins_demo\demo2>pytest -s
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1
rootdir: D:\soft\code\pytest_jenkins_demo\demo2
plugins:
collecting ... <class 'list'>
收集到的测试用例:[<Function test_a_1>, <Function test_a_2>, <Function test_b_2>, <Function test_b_1>]
排序后的用例：[<Function test_a_1>, <Function test_a_2>, <Function test_b_1>, <Function test_b_2>]
用例名:test_a_1
用例名:test_a_2
用例名:test_b_1
用例名:test_b_2
collected 4 items

a\test_aaa.py 测试用例a_1
.测试用例a_2
.
b\test_bbb.py 测试用例b_1
.测试用例b_2
.

========================== 4 passed in 0.06 seconds ===========================
```

重新排序后就可以按用例的名称顺序执行了。

有个 pytest-ordering 插件也可以自定义用例的顺序https://github.com/ftobia/pytest-ordering

# [pytest文档35-Hooks函数之统计测试结果(pytest_terminal_summary)](https://www.cnblogs.com/yoyoketang/p/12741564.html)

#### 前言

用例执行完成后，我们希望能获取到执行的结果，这样方便我们快速统计用例的执行情况。
也可以把获取到的结果当成总结报告，发邮件的时候可以先统计测试结果，再加上html的报告。

#### pytest_terminal_summary

关于TerminalReporter类可以在_pytest.terminal中查看到

```
from _pytest import terminal

pytest_terminal_summary(terminalreporter, exitstatus, config)
最后的结果汇总,可以拿到所有的执行结果
参数：
- terminalreporter (_pytest.terminal.TerminalReporter) – 内部使用的终端测试报告对象
- exitstatus (int) – 返回给操作系统的返回码
- config(_pytest.config.Config) - pytest config对象
```

TerminalReporter部分代码

```
class TerminalReporter(object):
    def __init__(self, config, file=None):
        import _pytest.config

        self.config = config
        self._numcollected = 0
        self._session = None
        self._showfspath = None

        self.stats = {}
        self.startdir = config.invocation_dir


    def report_collect(self, final=False):
        if self.config.option.verbose < 0:
            return

        if not final:
            # Only write "collecting" report every 0.5s.
            t = time.time()
            if (
                self._collect_report_last_write is not None
                and self._collect_report_last_write > t - REPORT_COLLECTING_RESOLUTION
            ):
                return
            self._collect_report_last_write = t

        errors = len(self.stats.get("error", []))
        skipped = len(self.stats.get("skipped", []))
        deselected = len(self.stats.get("deselected", []))
        selected = self._numcollected - errors - skipped - deselected
        if final:
            line = "collected "
        else:
            line = "collecting "
        line += (
            str(self._numcollected) + " item" + ("" if self._numcollected == 1 else "s")
        )
        if errors:
            line += " / %d errors" % errors
        if deselected:
            line += " / %d deselected" % deselected
        if skipped:
            line += " / %d skipped" % skipped
        if self._numcollected > selected > 0:
            line += " / %d selected" % selected
        if self.isatty:
            self.rewrite(line, bold=True, erase=True)
            if final:
                self.write("\n")
        else:
            self.write_line(line)
```

#### 案例参考

先在test_a.py写几个用例

```
# test_a.py
import pytest
# 上海-悠悠

def test_1():
    print("测试用例1111")
    assert 1 == 1


@pytest.mark.skip("跳过")
def test_2():
    print("测试用例22222")
    assert 1 == 1


def test_3():
    print("测试用例3333")


def test_4():
    print("测试用例44444444")
    assert 1 == 2
```

test_b.py用例参考

```
# test_b.py
import time
# 上海-悠悠

def test_5():
    print("测试用例55555555")
    time.sleep(3)


def test_6():
    print("测试用例66666666")
    time.sleep(3)
    assert 1 == 2
```

于是在conftest.py中写个 pytest_terminal_summary 函数收集测试结果

```
import time
from _pytest import terminal
# 上海-悠悠


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''收集测试结果'''
    print(terminalreporter.stats)
    print("total:", terminalreporter._numcollected)
    print('passed:', len(terminalreporter.stats.get('passed', [])))
    print('failed:', len(terminalreporter.stats.get('failed', [])))
    print('error:', len(terminalreporter.stats.get('error', [])))
    print('skipped:', len(terminalreporter.stats.get('skipped', [])))
    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime
    print('total times:', duration, 'seconds')
```

运行结果

```
D:\soft\pytest_xuexi_demo>pytest
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1
rootdir: D:\soft\pytest_xuexi_demo
plugins: allure-pytest-2.8.6, PyTestReport-0.1.9.3, forked-0.2, html-1.19.0, metadata-1.7.0, repeat-0.7.0, rerunfailures-8.0, xdist-1.23.2
collected 6 items

test_a.py .s.F                                                           [ 66%]
test_b.py .F                                                             [100%]

================================== FAILURES ===================================
___________________________________ test_4 ____________________________________

    def test_4():
        print("测试用例44444444")
>       assert 1==2
E       assert 1 == 2

test_a.py:21: AssertionError
---------------------------- Captured stdout call -----------------------------
测试用例44444444
___________________________________ test_6 ____________________________________

    def test_6():
        print("测试用例66666666")
        time.sleep(3)
>       assert 1 == 2
E       assert 1 == 2

test_b.py:18: AssertionError
---------------------------- Captured stdout call -----------------------------
测试用例66666666
{'': [<TestReport 'test_a.py::test_1' when='setup' outcome='passed'>, <TestReport 'test_a.py::test_1' when='teardown' outcome='passed'>, <TestReport 'test_a.py::test_2' when='teardown' outcome='passed'>, <TestReport 'test_a.py::test_3' when='setup' outcome='passed'>, <TestReport 'test_a.py::test_3' when='teardown' outcome='passed'>, <TestReport 'test_a.py::test_4' when='setup' outcome='passed'>, <TestReport 'test_a.py::test_4' when='teardown' outcome='passed'>, <TestReport 'test_b.py::test_5' when='setup' outcome='passed'>, <TestReport 'test_b.py::test_5' when='teardown' outcome='passed'>, <TestReport 'test_b.py::test_6' when='setup' outcome='passed'>, <TestReport 'test_b.py::test_6' when='teardown' outcome='passed'>], 'passed': [<TestReport 'test_a.py::test_1' when='call' outcome='passed'>, <TestReport 'test_a.py::test_3' when='call' outcome='passed'>, <TestReport 'test_b.py::test_5' when='call' outcome='passed'>], 'skipped': [<TestReport 'test_a.py::test_2' when='setup' outcome='skipped'>], 'failed': [<TestReport 'test_a.py::test_4' when='call' outcome='failed'>, <TestReport 'test_b.py::test_6' when='call' outcome='failed'>]}
total: 6
passed: 3
failed: 2
error: 0
skipped: 1
total times: 6.150860786437988 seconds
================ 2 failed, 3 passed, 1 skipped in 6.15 seconds ================
```

#### setup和teardown异常情况

如果setup出现异常，test_b.py代码修改下

```
# test_b.py
import time
import pytest
# 上海-悠悠


@pytest.fixture(scope="function")
def setup_demo():
    raise TypeError("ERROR!")


def test_5(setup_demo):
    print("测试用例55555555")
    time.sleep(3)


def test_6():
    print("测试用例66666666")
    time.sleep(3)
    assert 1 == 2
```

重新运行用例,结果如下

```
total: 6
passed: 2
failed: 2
error: 1
skipped: 1
成功率：33.33%
total times: 3.1817877292633057 seconds
=========== 2 failed, 2 passed, 1 skipped, 1 error in 3.18 seconds ============
```

此时统计结果没什么问题，接下来看teardown异常情况

```
# test_b.py
import time
import pytest
# 上海-悠悠


@pytest.fixture(scope="function")
def setup_demo():
    yield 
    raise TypeError("ERROR!")


def test_5(setup_demo):
    print("测试用例55555555")
    time.sleep(3)


def test_6():
    print("测试用例66666666")
    time.sleep(3)
    assert 1 == 2
```

运行结果

```
{'': [<TestReport 'test_a.py::test_1' when='setup' outcome='passed'>, <TestReport 'test_a.py::test_1' when='teardown' outcome='passed'>, <TestReport 'test_a.py::test_2' when='teardown' outcome='passed'>, <TestReport 'test_a.py::test_3' when='setup' outcome='passed'>, <TestReport 'test_a.py::test_3' when='teardown' outcome='passed'>, <TestReport 'test_a.py::test_4' when='setup' outcome='passed'>, <TestReport 'test_a.py::test_4' when='teardown' outcome='passed'>, <TestReport 'test_b.py::test_5' when='setup' outcome='passed'>, <TestReport 'test_b.py::test_6' when='setup' outcome='passed'>, <TestReport 'test_b.py::test_6' when='teardown' outcome='passed'>], 'passed': [<TestReport 'test_a.py::test_1' when='call' outcome='passed'>, <TestReport 'test_a.py::test_3' when='call' outcome='passed'>, <TestReport 'test_b.py::test_5' when='call' outcome='passed'>], 'skipped': [<TestReport 'test_a.py::test_2' when='setup' outcome='skipped'>], 'failed': [<TestReport 'test_a.py::test_4' when='call' outcome='failed'>, <TestReport 'test_b.py::test_6' when='call' outcome='failed'>], 'error': [<TestReport 'test_b.py::test_5' when='teardown' outcome='failed'>]}
total: 6
passed: 3
failed: 2
error: 1
skipped: 1
成功率：50.00%
total times: 6.18759298324585 seconds
=========== 2 failed, 3 passed, 1 skipped, 1 error in 6.19 seconds ============
```

这个时候总用例是6，但是`2 failed, 3 passed, 1 skipped, 1 error`加起来的个数是7，这个为什么？

从 terminalreporter.stats 可以看出 passed 里面 when='call' 时候统计了一次 test_5 用例

```
<TestReport 'test_b.py::test_5' when='call' outcome='passed'>
```

error 里面 when='teardown' 又统计了一次 test_5 用例

```
'error': [<TestReport 'test_b.py::test_5' when='teardown' outcome='failed'>]
```

when='teardown' 是测试用例的后置操作，一般用于数据的清理，报错了的话不影响测试用例的执行结果，所以可以忽略掉

修改后的最终代码如下

```
import time
from _pytest import terminal
# 上海-悠悠


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''收集测试结果'''
    # print(terminalreporter.stats)
    print("total:", terminalreporter._numcollected)
    print('passed:', len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown']))
    print('failed:', len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown']))
    print('error:', len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown']))
    print('skipped:', len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown']))
    print('成功率：%.2f' % (len(terminalreporter.stats.get('passed', []))/terminalreporter._numcollected*100)+'%')

    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime
    print('total times:', duration, 'seconds')
```

运行后的结果

```
total: 6
passed: 3
failed: 2
error: 0
skipped: 1
成功率：50.00%
total times: 6.20133113861084 seconds
=========== 2 failed, 3 passed, 1 skipped, 1 error in 6.20 seconds ============
```

#### 拿到测试结果

很多小伙伴问到如何拿到测试结果，这里我把测试结果保存为txt文件，你们也可以保存json文件

```
import time
from _pytest import terminal
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''收集测试结果'''
    # print(terminalreporter.stats)
    total = terminalreporter._numcollected
    passed= len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    failed=len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    error=len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    skipped=len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    successful = len(terminalreporter.stats.get('passed', []))/terminalreporter._numcollected*100
    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime
    print('total times: %.2f' % duration, 'seconds')

    with open("result.txt", "w") as fp:
        fp.write("TOTAL=%s" % total+"\n")
        fp.write("PASSED=%s" % passed+"\n")
        fp.write("FAILED=%s" % failed+"\n")
        fp.write("ERROR=%s" % error+"\n")
        fp.write("SKIPPED=%s" % skipped+"\n")
        fp.write("SUCCESSFUL=%.2f%%" % successful+"\n")
        fp.write("TOTAL_TIMES=%.2fs" % duration)
```

#### 邮件发送

邮件发送是配合jenkins发送邮件，可以参考这篇https://www.cnblogs.com/yoyoketang/p/14956235.html

# [pytest文档36-断言失败后还能继续执行pytest-assume](https://www.cnblogs.com/yoyoketang/p/12791203.html)

#### 前言

pytest的断言失败后，后面的代码就不会执行了，通常一个用例我们会写多个断言，有时候我们希望第一个断言失败后，后面能继续断言。
pytest-assume插件可以解决断言失败后继续断言的问题。github地址https://github.com/astraw38/pytest-assume

#### 环境准备

先安装pytest-assume依赖包

> pip install pytest-assume

#### 遇到问题

以下是一个简单案例，输入的测试数据有3种，我们需要断言同时满足三种情况

- x == y
- x+y > 1
- x > 1

```
import pytest
# 上海-悠悠

@pytest.mark.parametrize(('x', 'y'),
                         [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    print("测试数据x=%s, y=%s" % (x, y))
    assert x == y
    assert x+y > 1
    assert x > 1
```

运行结果

```
D:\demo\test_yoyo.py:9: AssertionError


================================== FAILURES ===================================
___________________________ test_simple_assume[1-1] ___________________________

x = 1, y = 1

    @pytest.mark.parametrize(('x', 'y'),
                             [(1, 1), (1, 0), (0, 1)])
    def test_simple_assume(x, y):
        print("测试数据x=%s, y=%s" % (x, y))
        assert x == y
        assert x+y > 1
>       assert x > 1
E       assert 1 > 1

D:\soft\code\pytest_api_2020_03\demo\test_yoyo.py:11: AssertionError
___________________________ test_simple_assume[1-0] ___________________________

x = 1, y = 0

    @pytest.mark.parametrize(('x', 'y'),
                             [(1, 1), (1, 0), (0, 1)])
    def test_simple_assume(x, y):
        print("测试数据x=%s, y=%s" % (x, y))
>       assert x == y
E       assert 1 == 0

D:\soft\code\pytest_api_2020_03\demo\test_yoyo.py:9: AssertionError
___________________________ test_simple_assume[0-1] ___________________________

x = 0, y = 1

    @pytest.mark.parametrize(('x', 'y'),
                             [(1, 1), (1, 0), (0, 1)])
    def test_simple_assume(x, y):
        print("测试数据x=%s, y=%s" % (x, y))
>       assert x == y
E       assert 0 == 1

D:\demo\test_yoyo.py:9: AssertionError
========================== 3 failed in 0.26 seconds ===========================
```

如果第一个断言就失败了，后面的2个断言都不会执行了

#### pytest-assume使用案例

使用pytest.assume断言

```
import pytest
# 上海-悠悠

@pytest.mark.parametrize(('x', 'y'),
                         [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    print("测试数据x=%s, y=%s" % (x, y))
    pytest.assume(x == y)
    pytest.assume(x+y > 1)
    pytest.assume(x > 1)
    print("测试完成！")
```

运行结果

```
================================== FAILURES ===================================
___________________________ test_simple_assume[1-1] ___________________________

tp = <class 'pytest_assume.plugin.FailedAssumption'>
value = FailedAssumption('\demo\\test_yoyo.py:11: AssumptionFailure\n>>\tpytest.assume(x > 1)\n
AssertionError: assert False\n\n',)
tb = <traceback object at 0x00000216CA579B08>

    def reraise(tp, value, tb=None):
        if value is None:
            value = tp()
        if value.__traceback__ is not tb:
>           raise value.with_traceback(tb)
E           pytest_assume.plugin.FailedAssumption: 
E           1 Failed Assumptions:
E           
E           ..\..\..\..\..\soft\code\pytest_api_2020_03\demo\test_yoyo.py:11: AssumptionFailure
E           >>	pytest.assume(x > 1)
E           AssertionError: assert False

E:\python36\lib\site-packages\six.py:685: FailedAssumption
___________________________ test_simple_assume[1-0] ___________________________

tp = <class 'pytest_assume.plugin.FailedAssumption'>
value = FailedAssumption('\demo\\test_yoyo.py:9:...st_api_2020_03\\demo\\test_yoyo.py:11: 
AssumptionFailure\n>>\tpytest.assume(x > 1)\nAssertionError: assert False\n\n',)
tb = <traceback object at 0x00000216CA579448>

    def reraise(tp, value, tb=None):
        if value is None:
            value = tp()
        if value.__traceback__ is not tb:
>           raise value.with_traceback(tb)
E           pytest_assume.plugin.FailedAssumption: 
E           3 Failed Assumptions:
E           
E           ..\..\..\..\..\soft\code\pytest_api_2020_03\demo\test_yoyo.py:9: AssumptionFailure
E           >>	pytest.assume(x == y)
E           AssertionError: assert False
E           
E           ..\..\..\..\..\soft\code\pytest_api_2020_03\demo\test_yoyo.py:10: AssumptionFailure
E           >>	pytest.assume(x+y > 1)
E           AssertionError: assert False
E           
E           ..\..\..\..\..\soft\code\pytest_api_2020_03\demo\test_yoyo.py:11: AssumptionFailure
E           >>	pytest.assume(x > 1)
E           AssertionError: assert False

E:\python36\lib\site-packages\six.py:685: FailedAssumption
___________________________ test_simple_assume[0-1] ___________________________

tp = <class 'pytest_assume.plugin.FailedAssumption'>
value = FailedAssumption('\n3 Failed Assumptions:\demo\\test_yoyo.py:11:
 AssumptionFailure\n>>\tpytest.assume(x > 1)\nAssertionError: assert False\n\n',)
tb = <traceback object at 0x00000216CA74D2C8>

    def reraise(tp, value, tb=None):
        if value is None:
            value = tp()
        if value.__traceback__ is not tb:
>           raise value.with_traceback(tb)
E           pytest_assume.plugin.FailedAssumption: 
E           3 Failed Assumptions:
E           
E           ..\..\..\..\..\soft\code\pytest_api_2020_03\demo\test_yoyo.py:9: AssumptionFailure
E           >>	pytest.assume(x == y)
E           AssertionError: assert False
E           
E           ..\..\..\..\..\soft\code\pytest_api_2020_03\demo\test_yoyo.py:10: AssumptionFailure
E           >>	pytest.assume(x+y > 1)
E           AssertionError: assert False
E           
E           ..\..\..\..\..\soft\code\pytest_api_2020_03\demo\test_yoyo.py:11: AssumptionFailure
E           >>	pytest.assume(x > 1)
E           AssertionError: assert False

E:\python36\lib\site-packages\six.py:685: FailedAssumption
========================== 3 failed in 0.44 seconds ===========================
```

从运行结果可以看出，三个断言都会执行

#### 上下文管理器

pytest.assume 也可以使用上下文管理器去断言

```
import pytest
from pytest import assume
# 上海-悠悠

@pytest.mark.parametrize(('x', 'y'),
                         [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    print("测试数据x=%s, y=%s" % (x, y))
    with assume: assert x == y
    with assume: assert x+y > 1
    with assume: assert x > 1
    print("测试完成！")
```

这样看起来会更优雅一点，对之前写的代码改起来也方便一些

需要注意的是每个with块只能有一个断言，如果一个with下有多个断言，当第一个断言失败的时候，后面的断言就不会起作用的.

```
import pytest
from pytest import assume
# 以下这种是错误的示例，不要一个with下写多个断言
# 上海-悠悠


@pytest.mark.parametrize(('x', 'y'),
                         [(1, 1), (1, 0), (0, 1)])
def test_simple_assume(x, y):
    print("测试数据x=%s, y=%s" % (x, y))
    with assume:
        assert x == y
        assert x+y > 1
        assert x > 1
    print("测试完成！")
```

# [pytest文档37-自定义用例顺序(pytest-ordering)](https://www.cnblogs.com/yoyoketang/p/12798200.html)

#### 前言

测试用例在设计的时候，我们一般要求不要有先后顺序，用例是可以打乱了执行的，这样才能达到测试的效果.
有些同学在写用例的时候，用例写了先后顺序， 有先后顺序后，后面还会有新的问题（如：上个用例返回数据作为下个用例传参，等等一系列的问题。。。）
github 上有个 pytest-ordering 插件可以控制用例的执行顺序，github插件地址https://github.com/ftobia/pytest-ordering

#### 环境准备

先安装依赖包

> pip install pytest-ordering

#### 使用案例

先看pytest默认的执行顺序，是按 test_ording.py 文件写的用例先后顺序执行的

```
# test_ording.py
import pytest
# 上海-悠悠


def test_foo():
    print("用例11111111111")
    assert True


def test_bar():
    print("用例22222222222")
    assert True


def test_g():
    print("用例333333333333333")
    assert True
```

运行结果

```
D:\demo>pytest test_ording.py -vs
============================= test session starts =============================
platform win32 -- Python 3.6.0
cachedir: .pytest_cache
metadata: 
plugins: ordering-0.6,
collected 3 items

test_ording.py::test_foo 用例11111111111
PASSED
test_ording.py::test_bar 用例22222222222
PASSED
test_ording.py::test_g 用例333333333333333
PASSED

========================== 3 passed in 0.07 seconds ===========================
```

使用 pytest-ordering 插件后改变测试用例顺序

```
# test_ording.py
import pytest
# 上海-悠悠


@pytest.mark.run(order=2)
def test_foo():
    print("用例11111111111")
    assert True


@pytest.mark.run(order=1)
def test_bar():
    print("用例22222222222")
    assert True


@pytest.mark.run(order=3)
def test_g():
    print("用例333333333333333")
    assert True
```

运行结果

```
D:\demo>pytest test_ording.py -vs
============================= test session starts =============================
platform win32 -- Python 3.6.0
cachedir: .pytest_cache
metadata: 
plugins: ordering-0.6,
collected 3 items

test_ording.py::test_bar 用例22222222222
PASSED
test_ording.py::test_foo 用例11111111111
PASSED
test_ording.py::test_g 用例333333333333333
PASSED

========================== 3 passed in 0.04 seconds ===========================
```

这样就是按指定的顺序执行的用例

# [pytest文档38-allure.step()添加测试用例步骤](https://www.cnblogs.com/yoyoketang/p/12846418.html)

#### 前言

一般流程性的测试用例，写成自动化用例时，步骤较多写起来会比较长。在测试用例里面添加详细的步骤有助于更好的阅读，也方便报错后快速的定位到问题。
举个常见的测试场景用例：从登陆开始，到浏览商品添加购物车，最后下单支付
用例步骤：1.登陆， 2.浏览商品 3.添加购物车 4.生成订单 5.支付成功

#### 用例设计

先把上面的每个环节，写成函数放到common_fucntion.py

```
# common_fucntion.py
import allure
import pytest
'''
流程性的用例，添加测试步骤，让用例更清晰
用例步骤：1.登陆， 2.浏览商品 3.添加购物车  4.生成订单  5.支付成功
作者：上海-悠悠 QQ交流群：779429633
'''

def login(username, password):
    '''登陆'''
    print("前置操作：先登陆")


def open_goods():
    '''浏览商品'''
    print("浏览商品")


def add_shopping_cart(goods_id="10086"):
    '''添加购物车'''
    print("添加购物车")


def buy_goods():
    '''生成订单'''
    print("buy")


def pay_goods():
    '''支付'''
    print("pay")
    
```

接下来测试用例设计，登陆可以单独拿出来，当成前置操作，后面的步骤合起来就是一个用例test_allure_step.py

```
# test_allure_step.py
import allure
import pytest
from .common_function import *

'''
流程性的用例，添加测试步骤，让用例更清晰
用例步骤：1.登陆， 2.浏览商品 3.添加购物车  4.生成订单  5.支付成功
作者：上海-悠悠 QQ交流群：779429633
'''

@pytest.fixture(scope="session")
def login_setup():
    login("yoyo", "123456")


@allure.feature("功能模块")
@allure.story("测试用例小模块-成功案例")
@allure.title("测试用例名称：流程性的用例，添加测试步骤")
def test_add_goods_and_buy(login_setup):
    '''
    用例描述：
    前置：登陆
    用例步骤：1.浏览商品 2.添加购物车  3.购买  4.支付成功
    '''
    with allure.step("step1：浏览商品"):
        open_goods()

    with allure.step("step2：添加购物车"):
        add_shopping_cart()

    with allure.step("step3：生成订单"):
        buy_goods()

    with allure.step("step4：支付"):
        pay_goods()

    with allure.step("断言"):
        assert 1 == 1
```

执行用例，生成allure报告

```
> pytest --alluredir ./allure_report test_allure_step.py
> allure serve ./allure_report
```

报告展示效果如下

![img](https://img2020.cnblogs.com/blog/1070438/202005/1070438-20200507233604910-1677091500.png)

#### 测试步骤@allure.step()

测试步骤也可以在 common_fucntion.py 里面定义的函数上加上装饰器实现：@allure.step()

```
import allure
import pytest
'''
流程性的用例，添加测试步骤，让用例更清晰
用例步骤：1.登陆， 2.浏览商品 3.添加购物车  4.生成订单  5.支付成功
'''


@allure.step("setup:登陆")
def login(username, password):
    '''登陆'''
    print("前置操作：先登陆")


@allure.step("step:浏览商品")
def open_goods():
    '''浏览商品'''
    print("浏览商品")


@allure.step("step:添加购物车")
def add_shopping_cart(goods_id="10086"):
    '''添加购物车'''
    print("添加购物车")


@allure.step("step:生成订单")
def buy_goods():
    '''生成订单'''
    print("buy")


@allure.step("step:支付")
def pay_goods():
    '''支付'''
    print("pay")
```

测试用例设计 test_allure_step_x.py

```
import allure
import pytest
from .common_function import *
# 作者：上海-悠悠 QQ交流群：779429633

@pytest.fixture(scope="session")
def login_setup():
    login("yoyo", "123456")


@allure.feature("功能模块")
@allure.story("测试用例小模块-成功案例")
@allure.title("第二种实现方式：流程性的用例，添加测试步骤")
def test_add_goods_and_buy_2(login_setup):
    '''
    用例描述：
    前置：登陆
    用例步骤：1.浏览商品 2.添加购物车  3.购买  4.支付成功
    '''
    open_goods()
    add_shopping_cart(goods_id="10086")
    buy_goods()
    pay_goods()
    assert 1 == 1
```

执行用例，生成allure报告

```
> pytest --alluredir ./allure_report test_allure_step_x.py
> allure serve ./allure_report
```

报告展示效果如下

![img](https://img2020.cnblogs.com/blog/1070438/202005/1070438-20200507231125863-1160133025.png)

#### 两种方式对比

使用 `with allure.step("step:步骤")` 这种方式代码可读性更好一点，但不会带上函数里面的传参和对应的值。
使用 `@allure.step("step:步骤")` 这种方式会带上函数的传参和对应的值。
这两种方式结合起来使用，才能更好的展示测试报告！

# [pytest文档39-参数化(parametrize)结合allure.title()生成不同标题报告](https://www.cnblogs.com/yoyoketang/p/12853605.html)

#### 前言

pytest的参数化(parametrize)可以实现只需维护测试数据，就能生成不同的测试用例目的。可以在参数化的时候加 ids 参数对每个用例说明使用场景。
最终我们希望在 allure 报告上能详细的展示出每个用例的标题描述，这样才能更直观的知道每个用例是干什么的。

#### 参数化parametrize

先看一个简单的pytest参数化案例演示test_a.py

```
# test_a.py
import pytest
import allure
# 作者：上海-悠悠 QQ交流群：779429633


def login(username, password):
    '''登录'''
    print("输入账号：%s" % username)
    print("输入密码：%s" % password)
    # 返回
    return {"code": 0, "msg": "success!"}


# 测试数据
test_datas = [
    ({"username": "yoyo1", "password": "123456"}, "success!"),
    ({"username": "yoyo2", "password": "123456"}, "failed!"),
    ({"username": "yoyo3", "password": "123456"}, "success!"),
]


@allure.story("登录用例")
@pytest.mark.parametrize("test_input,expected",
                         test_datas
                         )
def test_login(test_input, expected):
    '''测试登录用例'''
    # 获取函数返回结果
    result = login(test_input["username"], test_input["password"])
    # 断言
    assert result["msg"] == expected
```

cmd命令行运行用例

```
> pytest --alluredir ./report test_a.py
> allure serve ./report
```

生成报告

![img](https://img2020.cnblogs.com/blog/1070438/202005/1070438-20200508221216525-1989766888.png)

这样生成的报告在用例列表里面并不能很友好的展示出每个用例的执行场景，只知道哪个用例报错了。
于是需要对每个用例加上描述，加一个 ids 参数

#### ids 参数使用

在上面用例部分代码里面加个 ids 参数，用于描述每个用例的运行场景。

```
# 作者：上海-悠悠 QQ交流群：779429633
@allure.story("登录用例")
@pytest.mark.parametrize("test_input,expected",
                         test_datas,
                         ids=[
                             "输入正确账号，密码，登录成功",
                             "输入错误账号，密码，登录失败",
                             "输入正确账号，密码，登录成功",
                         ]
                         )
def test_login(test_input, expected):
    '''测试登录用例'''
    # 获取函数返回结果
    result = login(test_input["username"], test_input["password"])
    # 断言
    assert result["msg"] == expected
```

cmd命令行运行用例

```
> pytest --alluredir ./report test_a.py
> allure serve ./report
```

生成报告
![img](https://img2020.cnblogs.com/blog/1070438/202005/1070438-20200508221938180-1194907992.png)

#### allure.title描述用例

上面是通过在 parametrize 里面添加 ids 参数解决，接下来再讲一个用 allure.title("用例描述") 添加用例描述的方式解决。
使用 @allure.title("用例描述") 时，可以加上传入的参数，如传入的参数 `"test_input,expected"` ,需拼接test_input参数的值，可以这样写

> @allure.title("用例描述,测试输入：{test_input}")

在 allure_pytest/utils.py 源码里面可以找到对应的代码

```
# allure_pytest/utils.py

def allure_name(item, parameters):
    name = escape_name(item.name)
    title = allure_title(item)
    return title.format(**parameters) if title else name
```

当没有加allure.title()时候，用例的描述就是 item.name 值（也就是上面的 ids 用例的名称），
如果加了allure.title(),那么用例的描述就是添加的title值，这两个地方取其中的一个。

```
import pytest
import allure
# 作者：上海-悠悠 QQ交流群：779429633

def login(username, password):
    '''登录'''
    print("输入账号：%s" % username)
    print("输入密码：%s" % password)
    # 返回
    return {"code": 0, "msg": "success!"}


# 测试数据
test_datas = [
    ({"username": "yoyo1", "password": "123456"}, "success!"),
    ({"username": "yoyo2", "password": "123456"}, "failed!"),
    ({"username": "yoyo3", "password": "123456"}, "success!"),
]


@allure.story("登录用例")
@allure.title("用例描述,测试输入：{test_input}")
@pytest.mark.parametrize("test_input,expected",
                         test_datas,
                         ids=[
                             "输入正确账号，密码，登录成功",
                             "输入错误账号，密码，登录失败",
                             "输入正确账号，密码，登录成功",
                         ]
                         )
def test_login(test_input, expected):
    '''测试登录用例'''
    # 获取函数返回结果
    result = login(test_input["username"], test_input["password"])
    # 断言
    assert result["msg"] == expected
```

cmd命令行运行用例

```
> pytest --alluredir ./report test_a.py
> allure serve ./report
```

生成报告
![img](https://img2020.cnblogs.com/blog/1070438/202005/1070438-20200508222646003-323785761.png)

#### 优化用例title

结合上面两种实现方式，把用例描述当成一个测试输入的参数，继续优化后如下
需注意的是 parametrize 里面三个参数 `test_input,expected,title` 跟 test_login(test_input, expected, title) 里面三个参数保持一致

```
import pytest
import allure
# 作者：上海-悠悠 QQ交流群：779429633

def login(username, password):
    '''登录'''
    print("输入账号：%s" % username)
    print("输入密码：%s" % password)
    # 返回
    return {"code": 0, "msg": "success!"}


# 测试数据
test_datas = [
    ({"username": "yoyo1", "password": "123456"}, "success!", "输入正确账号，密码，登录成功"),
    ({"username": "yoyo2", "password": "123456"}, "failed!", "输入错误账号，密码，登录失败"),
    ({"username": "yoyo3", "password": "123456"}, "success!", "输入正确账号，密码，登录成功"),
]


@allure.story("登录用例")
@allure.title("{title}")
@pytest.mark.parametrize("test_input,expected,title",
                         test_datas
                         )
def test_login(test_input, expected, title):
    '''测试登录用例'''
    # 获取函数返回结果
    result = login(test_input["username"], test_input["password"])
    # 断言
    assert result["msg"] == expected
```

![img](https://img2020.cnblogs.com/blog/1070438/202005/1070438-20200508225008234-283468362.png)

# [pytest文档40-pytest.ini配置用例查找规则(面试题)](https://www.cnblogs.com/yoyoketang/p/13071288.html)

#### 前言

面试题:pytest如何执行不是test开头的用例？如执行 xxx_*.py这种文件的用例。
pytest.ini 配置文件可以修改用例的匹配规则。

#### pytest命令行参数

cmd打开输入pytest -h 查看命令行参数找到 [pytest] ini-options

- python_files (args) 匹配 python 用例文件， 如test_*.py、 *_test.py
- python_classes (args) 匹配 class 类名称 如Test*.py
- python_functions (args) 匹配函数和class里面方法 如test_*

```
[pytest] ini-options in the first pytest.ini|tox.ini|setup.cfg file found:

  markers (linelist)       markers for test functions
  empty_parameter_set_mark (string) default marker for empty parametersets
  norecursedirs (args)     directory patterns to avoid for recursion
  testpaths (args)         directories to search for tests when no files or dire
  usefixtures (args)       list of default fixtures to be used with this project
  python_files (args)      glob-style file patterns for Python test module disco
  python_classes (args)    prefixes or glob names for Python test class discover
  python_functions (args)  prefixes or glob names for Python test function and m
  disable_test_id_escaping_and_forfeit_all_rights_to_community_support (bool) di
  console_output_style (string) console output: "classic", or with additional pr
  xfail_strict (bool)      default for the strict parameter of xfail markers whe
  junit_suite_name (string) Test suite name for JUnit report
  junit_logging (string)   Write captured log messages to JUnit report: one of n
  junit_duration_report (string) Duration time to report: one of total|call
  junit_family (string)    Emit XML for schema: one of legacy|xunit1|xunit2
  doctest_optionflags (args) option flags for doctests
  doctest_encoding (string) encoding used for doctest files
  cache_dir (string)       cache directory path.
  filterwarnings (linelist) Each line specifies a pattern for warnings.filterwar
  log_print (bool)         default value for --no-print-logs
  log_level (string)       default value for --log-level
  log_format (string)      default value for --log-format
  log_date_format (string) default value for --log-date-format
  log_cli (bool)           enable log display during test run (also known as "li
  log_cli_level (string)   default value for --log-cli-level
  log_cli_format (string)  default value for --log-cli-format
  log_cli_date_format (string) default value for --log-cli-date-format
  log_file (string)        default value for --log-file
  log_file_level (string)  default value for --log-file-level
  log_file_format (string) default value for --log-file-format
  log_file_date_format (string) default value for --log-file-date-format
  addopts (args)           extra command line options
  minversion (string)      minimally required pytest version
  rsyncdirs (pathlist)     list of (relative) paths to be rsynced for remote dis
  rsyncignore (pathlist)   list of (relative) glob-style paths to be ignored for
  looponfailroots (pathlist) directories to check for changes
```

#### 修改匹配规则

pytest 默认查找用例匹配规则

- 测试文件以test_开头（以_test结尾也可以）
- 测试类以Test开头，并且不能带有 **init** 方法
- 测试函数以test_开头

如果我们想匹配以 xxx_*.py的文件，pytest.ini 文件放到项目的根目录。
在 pytest.ini 文件添加一项 python_files 即可

```
[pytest]

python_files =  xxx_*.py
```

#### 使用案例

写一个 xxx_yoyo.py 的文件用例

```
#  xxx_yoyo.py
# 作者：上海-悠悠 QQ交流群：779429633
def test_1():
    print("hello")


def test_2():
    print("world")
```

cmd 输入 pytest 执行，就可以匹配到了

```
D:\soft\demo>pytest
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1
rootdir: D:\soft\code\web_pytest_2020, inifile: pytest.ini
plugins: allure-pytest-2.8.6
collected 2 items

xxx_yoyo.py hello
.world
.

========================== 2 passed in 0.13 seconds ===========================
```

匹配测试用例类和方法相关配置参考如下

```
[pytest]

python_files =  xxx_*.py *_xxx.py
python_classes = Test*
python_functions = test_*
```

多个匹配规则中间用空格隔开,其它配置参考这篇https://www.cnblogs.com/yoyoketang/p/9550648.html

# [pytest文档41-参数化 ids 用例描述为中文时控制台输出unicode编码问题（pytest_collection_modifyitems）](https://www.cnblogs.com/yoyoketang/p/13090418.html)

#### 前言

使用 pytest.mark.parametrize 参数化的时候，加 ids 参数用例描述有中文时，在控制台输出会显示unicode编码，中文不能正常显示。
使用 pytest_collection_modifyitems 钩子函数，对输出的 item.name 和 item.nodeid 重新编码。

#### 问题描述

参数化 ids 用例描述有中文

```
import pytest


# test_ids.py
import pytest
# 作者：上海-悠悠


def login(username, password):
    '''登录'''
    # 返回
    return {"code": 0, "msg": "success!"}


# 测试数据
test_datas = [
    ({"username": "yoyo1", "password": "123456"}, "success!"),
    ({"username": "yoyo2", "password": "123456"}, "success!"),
    ({"username": "yoyo3", "password": "123456"}, "success!"),
]


@pytest.mark.parametrize("test_input,expected",
                         test_datas,
                         ids=[
                             "输入正确账号，密码，登录成功",
                             "输入错误账号，密码，登录失败",
                             "输入正确账号，密码，登录成功",
                         ]
                         )
def test_login(test_input, expected):
    '''测试登录用例'''
    # 获取函数返回结果
    result = login(test_input["username"], test_input["password"])
    # 断言
    assert result["msg"] == expected
```

cmd终端运行 `pytest test_ids.py -v`
![img](https://img2020.cnblogs.com/blog/1070438/202006/1070438-20200610234906475-1599313501.png)

**注意 [\u8f93\u5165\u6b63 ...] 这种不叫乱码，这叫 unicode 编码**

#### pytest_collection_modifyitems

在项目的根目录写个 conftest.py 文件，加以下代码

```
def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        print(item.nodeid)
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
```

cmd 控制台重新运行

![img](https://img2020.cnblogs.com/blog/1070438/202006/1070438-20200610235007922-666495580.png)

# [pytest文档42-fixture参数化params](https://www.cnblogs.com/yoyoketang/p/13332720.html)

#### 前言

参数化是自动化测试里面必须掌握的一个知识点，用过 unittest 框架的小伙伴都知道使用 ddt 来实现测试用例的参数化。
pytest 测试用例里面对应的参数可以用 parametrize 实现，随着用例的增多，我们的需求也会越来越多，那么如何在 fixture 中使用参数呢？

#### fixture 源码

先看下 fixture 源码，有这几个参数：scope，params，autouse，ids，name。

```
def fixture(scope="function", params=None, autouse=False, ids=None, name=None):
    """Decorator to mark a fixture factory function.

    This decorator can be used, with or without parameters, to define a
    fixture function.

    The name of the fixture function can later be referenced to cause its
    invocation ahead of running tests: test
    modules or classes can use the ``pytest.mark.usefixtures(fixturename)``
    marker.

    Test functions can directly use fixture names as input
    arguments in which case the fixture instance returned from the fixture
    function will be injected.

    Fixtures can provide their values to test functions using ``return`` or ``yield``
    statements. When using ``yield`` the code block after the ``yield`` statement is executed
    as teardown code regardless of the test outcome, and must yield exactly once.

    :arg scope: the scope for which this fixture is shared, one of
                ``"function"`` (default), ``"class"``, ``"module"``,
                ``"package"`` or ``"session"``.

                ``"package"`` is considered **experimental** at this time.

    :arg params: an optional list of parameters which will cause multiple
                invocations of the fixture function and all of the tests
                using it.
                The current parameter is available in ``request.param``.

    :arg autouse: if True, the fixture func is activated for all tests that
                can see it.  If False (the default) then an explicit
                reference is needed to activate the fixture.

    :arg ids: list of string ids each corresponding to the params
                so that they are part of the test id. If no ids are provided
                they will be generated automatically from the params.

    :arg name: the name of the fixture. This defaults to the name of the
                decorated function. If a fixture is used in the same module in
                which it is defined, the function name of the fixture will be
                shadowed by the function arg that requests the fixture; one way
                to resolve this is to name the decorated function
                ``fixture_<fixturename>`` and then use
                ``@pytest.fixture(name='<fixturename>')``.
    """
    if callable(scope) and params is None and autouse is False:
        # direct decoration
        return FixtureFunctionMarker("function", params, autouse, name=name)(scope)
    if params is not None and not isinstance(params, (list, tuple)):
        params = list(params)
    return FixtureFunctionMarker(scope, params, autouse, ids=ids, name=name)
```

重点看 params 参数：一个可选的参数列表，它将导致多次调用fixture函数和使用它的所有测试
获取当前参数可以使用 `request.param`

```
    :arg params: an optional list of parameters which will cause multiple
                invocations of the fixture function and all of the tests
                using it.
                The current parameter is available in ``request.param``.
```

#### fixture 之 params 使用示例

request 是pytest的内置 fixture ，主要用于传递参数

```
# test_fixture_params.py
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


# 测试数据，存放在list
user_data = ["user1", "user2"]

@pytest.fixture(scope="function", params=user_data)
def users(request):
    '''注册用户参数化'''
    return request.param


def test_register(users):
    print("注册用户：%s"%users)

if __name__ == '__main__':
    pytest.main(["-s", "test_fixture_params"])
```

运行结果

```
>pytest test_fixture_params.py -s
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1
rootdir: D:\soft\demo
plugins: allure-pytest-2.8.6
collected 2 items

test_fixture_params.py 注册用户：user1
.注册用户：user2
.

========================== 2 passed in 0.02 seconds ===========================
```

#### 前置与后置

如果每次注册用户之前，需先在前置操作里面清理用户注册表的数据，可以执行SQL,传不同用户的参数

```
# test_fixture_params.py
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

def delete_sql(user):
    '''这里执行SQL'''
    sql = "delete from auth_user WHERE username = '%s';"%user
    print("执行的sql:%s"%sql)
    # 调用执行SQL的封装函数


# 测试数据，存放在list
user_data = ["user1", "user2"]

@pytest.fixture(scope="function", params=user_data)
def users(request):
    '''注册用户参数化'''

    # 前置操作
    delete_sql(request.param)

    yield request.param

    # # 后置操作
    # delete_sql(request.param)


def test_register(users):
    print("注册用户：%s"%users)

if __name__ == '__main__':
    pytest.main(["-s", "test_fixture_params.py"])
```

运行结果

```
collected 2 items

test_fixture_params.py 执行的sql:delete from auth_user WHERE username = 'user1';
注册用户：user1
.执行的sql:delete from auth_user WHERE username = 'user2';
注册用户：user2
.

========================== 2 passed in 0.06 seconds ===========================
```

后置操作可以写到 yield 后面，参考上面的格式。

# [pytest文档43-元数据使用(pytest-metadata)](https://www.cnblogs.com/yoyoketang/p/13335858.html)

#### 前言

什么是元数据？元数据是关于数据的描述，存储着关于数据的信息，为人们更方便地检索信息提供了帮助。
pytest 框架里面的元数据可以使用 pytest-metadata 插件实现。文档地址https://pypi.org/project/pytest-metadata/

#### pytest-metadata 环境准备

使用 pip 安装 pytest-metadata

> pip install pytest-metadata

#### 查看 pytest 元数据

使用pytest 执行用例的时候加上 `-v` 参数(或`--verbose`),在控制台输出报告的头部就会输出元数据(metadata)

```
>pytest --verbose
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1 -- e:\python36\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.6.0', 'Platform': 'Windows-10-10.0.17134-SP0', 'Packages': {'pytest': '4.5.0', 'py': '1.5.4', 'pluggy': '0.13.1'}, 'Plugins': {'allure-pytest': '2.8.6', 'PyTestReport': '0.1.9.3', 'assume': '2.2.1', 'forked': '0.2', 'html': '1.19.0', 'metadata': '1.7.0', 'ordering': '0.6', 'repeat': '0.7.0', 'rerunfailures': '8.0', 'xdist': '1.23.2'}, 'JAVA_HOME': 'D:\\java\\jdk1.8'}
rootdir: D:\soft\code\pytest_api_2020_03
plugins: allure-pytest-2.8.6
```

可以获取到的元数据

| Key       | Description       | Example                                                |
| --------- | :---------------- | :----------------------------------------------------- |
| Python    | Python 版本       | '3.6.0'                                                |
| Platform  | 运行平台          | 'Windows-10-10.0.17134-SP0'                            |
| Packages  | pytest 包相关信息 | {'pytest': '4.5.0', 'py': '1.5.4', 'pluggy': '0.13.1'} |
| Plugins   | pytest 插件       | {'allure-pytest': '2.8.6', 'PyTestReport': '0.1.9.3'}  |
| JAVA_HOME | JAVA环境变量      | 'D:\java\jdk1.8'                                       |

元数据是以键值对(key-value)方式存储的

#### 添加 metadata

我们可以在命令行用 `--metadata` 参数添加键值对(key, value)的元数据。
比如当我们完成了一个项目，需要添加作者信息，于是就可以添加元数据

> pytest --metadata auther yoyo

如果需要添加多个元数据，可以使用多次 `--metadata` 参数添加

> pytest --metadata auther yoyo --metadata version v1.0

从文档上看可以支持json格式，一次性传多组元数据，使用`--metadata-from-json`,但我自己试了下，并不支持这个参数,这种方式可以忽略！

> pytest --metadata-from-json '{"cat_says": "bring the cat nip", "human_says": "yes kitty"}'

#### pytest_metadata hook函数

在代码里面也可以新增/修改/删除 元数据，我们可以使用 pytest_metadata hook函数

```
import pytest
@pytest.mark.optionalhook
def pytest_metadata(metadata):
    metadata.pop("password", None)
```

我们可以使用 metadata fixture，用于测试用例或fixture 访问元数据（metadata）

```
def test_metadata(metadata):
    assert 'metadata' in metadata['Plugins']
```

在插件里面访问 metadata，可以在config对象使用 _metadata 属性来新增/修改/删除 元数据

```
def pytest_configure(config):
  if hasattr(config, '_metadata'):
      config._metadata['foo'] = 'bar'
```

#### 插件集成

下面是一个方便的插件列表，这些插件要么读取元数据，要么对元数据有贡献：

- pytest-base-url - Adds the base URL to the metadata.
- pytest-html - Displays the metadata at the start of each report.
- pytest-selenium - Adds the driver, capabilities, and remote server to the metadata.

#### pytest.ini 管理元数据

如果新增的元数据较多，在命令行输入不太方便，可以在pytest.ini配置里面配置你的项目元数据

```
# pytest.ini
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

[pytest]
addopts = -v 
  --html=report.html 
  --self-contained-html
  --metadata auther yoyo 
  --metadata version v1.0
```

# [pytest文档44-allure.dynamic动态生成用例标题](https://www.cnblogs.com/yoyoketang/p/13386145.html)

#### 前言

pytest 结合 allure 描述用例的时候我们一般使用 `@allure.title` 和 `@allure.description` 描述测试用例的标题和详情。
在用例里面也可以动态更新标题和详情，使用allure.dynamic方法实现。

#### allure.dynamic 动态属性

feature 模块

> allure.dynamic.feature(feature_name)

功能点 story

> allure.dynamic.story(case_story)

用例标题 title

> allure.dynamic.title(case_title)

用例描述：请求URL 请求类型 期望结果 实际结果描述

```
desc = "<font color='red'>请求URL:</font>{}<Br/>" \
           "<font color='red'>请求类型:</font>{}<Br/>" \
           "<font color='red'>期望结果:</font>{}<Br/>" \
           "<font color='red'>实际结果描述:</font>{}<Br/>".format(url,method,expect,expect_result)
allure.dynamic.description(desc)
```

#### description 用例描述

可以在测试主体内部动态更新描述 `allure.dynamic.description`

```
import allure

@allure.description("""
This description will be replaced at the end of the test.
""")
def test_dynamic_description():
    assert 42 == int(6 * 7)
    allure.dynamic.description('A final description.')
```

最后用例的描述被更新为 'A final description.'

![img](https://img2020.cnblogs.com/blog/1070438/202007/1070438-20200727161451176-2057164973.png)

#### title 用例标题

用例标题也可以被动态更新

```
@allure.title("This title will be replaced in a test body")
def test_with_dynamic_title():
    assert 2 + 2 == 4
    allure.dynamic.title('After a successful test finish, the title was replaced with this line.')
```

最终用例的title更新为'After a successful test finish, the title was replaced with this line.'
![img](https://img2020.cnblogs.com/blog/1070438/202007/1070438-20200727161746832-1420813643.png)

#### 参数化

参数化时候，可以使用@allure.title给用例不同标题

```
@allure.title("Parameterized test title: adding {param1} with {param2}")
@pytest.mark.parametrize('param1,param2,expected', [
    (2, 2, 4),
    (1, 2, 5)
])
def test_with_parameterized_title(param1, param2, expected):
    assert param1 + param2 == expected
```

也可以在用例里面使用allure.dynamic.title更新用例的标题

```
import pytest
import allure
# 作者：上海-悠悠 QQ交流群：779429633

def login(username, password):
    '''登录'''
    print("输入账号：%s" % username)
    print("输入密码：%s" % password)
    # 返回
    return {"code": 0, "msg": "success!"}


# 测试数据
test_datas = [
    ({"username": "yoyo1", "password": "123456"}, "success!", "输入正确账号，密码，登录成功"),
    ({"username": "yoyo2", "password": "123456"}, "failed!", "输入错误账号，密码，登录失败"),
    ({"username": "yoyo3", "password": "123456"}, "success!", "输入正确账号，密码，登录成功"),
]


@allure.story("登录用例")
@pytest.mark.parametrize("test_input,expected,title",
                         test_datas
                         )
def test_login(test_input, expected, title):
    '''测试登录用例'''
    # 获取函数返回结果
    result = login(test_input["username"], test_input["password"])
    # 断言
    assert result["msg"] == expected
    allure.dynamic.title(title)
```

最终生成报告效果

![img](https://img2020.cnblogs.com/blog/1070438/202007/1070438-20200727163107102-99817617.png)

#### 其它属性

allure.dynamic.feature
allure.dynamic.link
allure.dynamic.issue
allure.dynamic.testcase
allure.dynamic.story
allure.dynamic.title
allure.dynamic.description

# [pytest文档45-allure添加环境配置(environment)](https://www.cnblogs.com/yoyoketang/p/13491363.html)

#### 前言

在 allure 报告首页 ENVIRONMENT 显示 'There are no environment variables' 没有环境变量的配置信息。
环境变量配置可以添加报告相关的配置参数，如运行的系统环境，版本号，测试环境，测试人员等基本信息

#### 问题描述

allure 报告首页 ENVIRONMENT

![img](https://img2020.cnblogs.com/blog/1070438/202008/1070438-20200812160659273-450135134.png)

接下来就讲如何添加 ENVIRONMENT

#### environment 配置文件

方法一：environment.properties 文件
在allure的report根目录下添加一个 environment.properties 文件

![img](https://img2020.cnblogs.com/blog/1070438/202008/1070438-20200812161034476-1439695616.png)

文件里面添加环境配置，格式如下

```
systemVersion=win10
pythonVersion=3.6.0
allureVersion=2.13.0
baseUrl=http://192.168.1.x:8080
projectName=test
author=YOYO
email=283340479@qq.com
blog=https://www.cnblogs.com/yoyoketang/
```

方法二：environment.xml

也可以用 environment.xml 文件，格式如下

```
<environment>
    <parameter>
        <key>Browser</key>
        <value>Chrome</value>
    </parameter>
    <parameter>
        <key>Browser.Version</key>
        <value>63.0</value>
    </parameter>
    <parameter>
        <key>Stand</key>
        <value>Production</value>
    </parameter>
</environment>
```

#### 报告展示

运行测试用例，生成 allure 报告

```
> pytest test_allure.py --alluredir ./report
> allure serve ./report
```

报告内容显示
![img](https://img2020.cnblogs.com/blog/1070438/202008/1070438-20200812161438365-731726689.png)

这个地方是不支持中文的，如果有中文报告会显示乱码
![img](https://img2020.cnblogs.com/blog/1070438/202008/1070438-20200812161544696-1349274205.png)

#### copy命令

在运行 pytest 生成 allure 报告的时候，有时候需要加 `--clean` 参数，清楚之前的报告记录，这样会之前清空 report 目录，environment.properties文件也会被删除。
为了不让 environment.properties 文件删除掉，可以把 environment.properties 文件放项目根目录，在运行报告的时候，先 copy 到 report 目录

以windows10系统为例

```
> pytest test_allure.py --alluredir ./report --clean

> copy environment.properties report\environment.properties

> allure serve ./report
```

linux系统用cp

```
> pytest test_allure.py --alluredir ./report --clean
> cp environment.properties ./report/environment.properties
> allure serve ./report
```

备注：早期的 allure 1.x 版本可以用以下方式添加

```
import allure

# allure 添加 environment 配置
allure.environment(base_url='http://192.168.1.x:8080')
allure.environment(project_name='test')
allure.environment(author='上海-悠悠')
allure.environment(email='283340479@qq.com')
allure.environment(blog='https://www.cnblogs.com/yoyoketang/')
```

但最新的 2.x 版本 allure 没这个方法了，有点遗憾！

# [pytest文档46-关于https请求警告问题(InsecureRequestWarning: Unverified HTTPS request is being made)](https://www.cnblogs.com/yoyoketang/p/13499151.html)

#### 前言

使用 pytest 执行 https 请求用例的时候，控制台会出现警告：InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised.
当出现这个警告的时候，我们第一反应是加忽略警告：urllib3.disable_warnings()，然而并不管用。

#### 问题描述

使用requests库发https请求，添加verify=False忽略证书

```
# test_https.py
import requests
import urllib3
urllib3.disable_warnings()


def test_h():
    '''
    author: 上海-悠悠 QQ交流群：779429633
    blog: https://www.cnblogs.com/yoyoketang
    :return: 
    '''
    url = "https://www.cnblogs.com/yoyoketang"
    s = requests.session()
    s.verify = False
    r = s.get(url)
    assert "上海-悠悠" in r.text
```

命令行使用pytest运行用例

```
D:\demo>pytest test_https.py
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1
rootdir: D:\demo
plugins: allure-pytest-2.8.6
collected 1 item

test_https.py .                                                          [100%]

============================== warnings summary ===============================
test_https.py::test_h
  e:\python36\lib\site-packages\urllib3\connectionpool.py:858: InsecureRequestWarning: Unverified HTTPS request is being made. 
Adding certificate verification is strongly advised. 
See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings InsecureRequestWarning)

-- Docs: https://docs.pytest.org/en/latest/warnings.html
==================== 1 passed, 1 warnings in 0.35 seconds =====================
```

这时候会出现 InsecureRequestWarning 警告，去百度搜都是上加上这句

> urllib3.disable_warnings()

然而你会发现不管用

#### 问题分析

出现这个问题，并不是因为 'urllib3.disable_warnings()' 不生效，主要是小伙伴门对 pytest 的运行规则不熟悉，pytest 框架运行的时候会查找test_*.py文件下的test_*()函数或方法的用例
也就是只会执行 `test_h()` 下面的代码，所以根本就不会执行它上面的代码，可以试试换个位置，放到test_h() 以下，就会生效

```
import requests
import urllib3
# urllib3.disable_warnings()

def test_h():
    '''
    author: 上海-悠悠 QQ交流群：779429633
    blog: https://www.cnblogs.com/yoyoketang
    :return:
    '''
    urllib3.disable_warnings()  # 换个位置
    url = "https://www.cnblogs.com/yoyoketang"
    s = requests.session()
    s.verify = False
    r = s.get(url)
    assert "上海-悠悠" in r.text
```

再次运行 `pytest test_https.py` 警告就没有了

#### warnings 文档

上面的警告内容有个doc文档地址[Docs: https://docs.pytest.org/en/latest/warnings.html](https://docs.pytest.org/en/latest/warnings.html)，点开查询解决方案

文档上有对于警告出现的详细描述，在命令行添加`--disable-warnings` 参数忽略警告

> pytest test_https.py --disable-warnings

```
D:\demo>pytest test_https.py --disable-warnings
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1
rootdir: D:\demo
plugins: allure-pytest-2.8.6
collected 1 item

test_https.py .                                                          [100%]

==================== 1 passed, 1 warnings in 0.24 seconds =====================
```

虽然警告内容没有了，但是警告还是会显示：1 passed, 1 warnings

也许你想彻底的不想看到warnings，可以不加载 warnings 插件，使用-p参数忽略插件加载

```
 -p name               early-load given plugin module name or entry point
                        (multi-allowed). To avoid loading of plugins, use the
                        `no:` prefix, e.g. `no:doctest`.
```

带上 -p 参数运行

> pytest test_https.py -p no:warnings

```
D:\demo>pytest test_https.py -p no:warnings
============================= test session starts =============================
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1
rootdir: D:\demo
plugins: allure-pytest-2.8.6
collected 1 item

test_https.py .                                                          [100%]

========================== 1 passed in 0.29 seconds ===========================
```

现在可以看到运行结果里面完全没有 warnings 字样了

可以在项目根目录放一个pytest.ini文件，内容如下

```
[pytest]
addopts = -p no:warnings
```

这样使用命令行执行的时候，就可以不用每次都带-p参数了

# [pytest文档47-allure报告添加用例失败截图](https://www.cnblogs.com/yoyoketang/p/13537355.html)

#### 前言

使用 selenium 做 web 自动化的时候，很多小伙伴希望用例失败的时候能截图，把异常截图展示到allure报告里面。
pytest 有个很好的钩子函数 pytest_runtest_makereport 可以获取到用例执行的结果，所以我们在这个钩子函数里面判断用例失败后截图就可以了。
allure报告添加截图可以使用 allure.attach 方法

#### 失败截图

关于 pytest_runtest_makereport 获取用例执行结果的钩子函数介绍可以看前面这篇https://www.cnblogs.com/yoyoketang/p/12609871.html
在 conftest.py 文件写用例执行的钩子函数

```
import pytest
from selenium import webdriver
import os
import allure
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


_driver = None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    获取每个用例状态的钩子函数
    :param item:
    :param call:
    :return:
    '''
    # 获取钩子方法的调用结果
    outcome = yield
    rep = outcome.get_result()
    # 仅仅获取用例call 执行结果是失败的情况, 不包含 setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        # 添加allure报告截图
        if hasattr(_driver, "get_screenshot_as_png"):
            with allure.step('添加失败截图...'):
                allure.attach(_driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)


@pytest.fixture(scope='session')
def browser():
    global _driver
    if _driver is None:
        _driver =webdriver.Chrome()
    yield _driver
    print("1111111111")
    _driver.quit()
```

#### 用例运行

整个目录结构如下

![img](https://img2020.cnblogs.com/blog/1070438/202008/1070438-20200820190814482-25054027.png)

test_login.py文件内容如下

```
import pytest
from selenium import webdriver
import allure
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


def test_login(browser):
    with allure.step("step1：打开登录首页"):
        browser.get("http://ip:6009/admin/login/?next=/admin/")
    with allure.step("step2：输入账号：admin"):
        browser.find_element_by_name("username").send_keys("admin")
    with allure.step("step2：输入密码：123456"):
        browser.find_element_by_name("password").send_keys("123456")
    # 故意断言失败，看是否会截图
    assert browser.title == "悠悠"
```

运行用例后，截图会存到./report 报告目录，allure报告展示

![img](https://img2020.cnblogs.com/blog/1070438/202008/1070438-20200820190618568-916815703.png)

# [pytest文档48-切换 base_url 测试环境(pytest-base-url)](https://www.cnblogs.com/yoyoketang/p/13556399.html)

#### 前言

当我们自动化代码写完成之后，期望能在不同的环境测试，这时候应该把 base_url 单独拿出来，能通过配置文件和支持命令行参数执行。
pytest-base-url 是 pytest 里面提供的一个管理 base-url 的一个非常实用的插件，参考文档https://pypi.org/project/pytest-base-url/

#### 环境准备

先安装 pytest-base-url 插件

> pip install pytest-base-url

#### 使用案例

直接在用例里面使用 base_url参数 当成一个fixture使用

```
# test_demo.py
import requests
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

def test_example(base_url):
    assert 200 == requests.get(base_url).status_code
```

命令行执行的时候加上 `--base-url` 参数

> pytest --base-url [http://www.example.com](http://www.example.com/)

```
D:\soft\web_base>pytest --base-url http://www.example.com
=========== test session starts ==============
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1
baseurl: http://www.example.com
rootdir: D:\soft\web_base
plugins: allure-pytest-2.8.6, base-url-1.4.2
collected 1 item

test_demo.py .                               [100%]

============= 1 passed in 0.73 seconds ============
```

#### pytest.ini 配置文件

也可以在 pytest.ini 配置文件中添加 base_url 地址

```
# pytest.ini文件内容
[pytest]
base_url = http://www.example.com
```

这样在命令行执行时候就可以不用带上 `--base-url` 参数

```
D:\soft\web_base>pytest
============== test session starts ================
platform win32 -- Python 3.6.0, pytest-4.5.0, py-1.5.4, pluggy-0.13.1
baseurl: http://www.example.com
rootdir: D:\soft\web_base, inifile: pytest.ini
plugins: allure-pytest-2.8.6,  base-url-1.4.2
collected 1 item

test_demo.py .           [100%]

============ 1 passed in 1.72 seconds ==========
```

# [pytest文档49-命令行参数--tb的使用](https://www.cnblogs.com/yoyoketang/p/13601121.html)

#### 前言

pytest 使用命令行执行用例的时候，有些用例执行失败的时候，屏幕上会出现一大堆的报错内容，不方便快速查看是哪些用例失败。
`--tb=style` 参数可以设置报错的时候回溯打印内容，可以设置参数(auto/long/short/line/native/no)

#### --tb=style

`pytest -h` 查看命令行参数，关于 `--tb=style` 参数的使用方式

```
>pytest -h

 --tb=style            traceback print mode (auto/long/short/line/native/no).
```

style 的值可以设置6种打印模式：auto/long/short/line/native/no

#### --tb=no

先写个简单的pytest用例，让他断言报错

```
# test_tb.py
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

def test_01():
    result = "hello"
    expected = "world"
    assert result == expected
```

命令行执行`pytest test_tb.py` 此时屏幕上会显示整个用例的回溯信息

```
test_tb.py F                                                             [100%]

================================== FAILURES ===================================
___________________________________ test_01 ___________________________________

    def test_01():
        result = "hello"
        expected = "world"
>       assert result == expected
E       AssertionError: assert 'hello' == 'world'
E         - hello
E         + world

test_tb.py:8: AssertionError
========================== 1 failed in 0.08 seconds ===========================
```

加上 `--tb=no` 参数执行

```
test_tb.py F                                                             [100%]

========================== 1 failed in 0.05 seconds ===========================
```

`--tb=no` 是不显示报错的回溯内容

#### --tb=line

line 模式使用一行输出所有的错误信息

```
test_tb.py F                                                             [100%]

================================== FAILURES ===================================
D:\soft\kecheng202004\demo\test_tb.py:8: AssertionError: assert 'hello' == 'world'
========================== 1 failed in 0.06 seconds ===========================
```

#### --tb=short

short 模式显示断言报错的位置，不显示用例前面的代码

```
test_tb.py F                                                             [100%]

================================== FAILURES ===================================
___________________________________ test_01 ___________________________________
test_tb.py:8: in test_01
    assert result == expected
E   AssertionError: assert 'hello' == 'world'
E     - hello
E     + world
========================== 1 failed in 0.06 seconds ===========================
```

#### 其它

--tb=auto 有多个用例失败的时候，只打印第一个和最后一个用例的回溯信息
--tb=long 输出最详细的回溯信息
--tb=short 输入assert的一行和系统判断内容
--tb=line 使用一行显示错误信息
--tb=native 只输出python标准库的回溯信息
--tb=no 不显示回溯信息



# [pytest文档50-命令行参数--durations统计用例运行时间](https://www.cnblogs.com/yoyoketang/p/13604333.html)

#### 前言

写完一个项目的自动化用例之后，发现有些用例运行较慢，影响整体的用例运行速度，于是领导说找出运行慢的那几个用例优化下。
`--durations` 参数可以统计出每个用例运行的时间，对用例的时间做个排序。

#### --durations=N

`pytest -h` 查看命令行参数，关于 `--durations=N` 参数的使用方式

```
>pytest -h

reporting:
  --durations=N         show N slowest setup/test durations (N=0 for all).
```

当 N=0 的时候显示全部用例的运行时间

#### --durations=0

先写几个pytest的用例，在用例里面加sleep时间，这样方便看到每个用例运行的持续时间

```
import pytest
import time
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


@pytest.fixture()
def set_up_fixture():
    time.sleep(0.1)
    yield
    time.sleep(0.2)


def test_01(set_up_fixture):
    print("用例1")
    time.sleep(1.0)


def test_02(set_up_fixture):
    print("用例2")
    time.sleep(0.6)


def test_03(set_up_fixture):
    print("用例3")
    time.sleep(1.2)


def test_04(set_up_fixture):
    print("用例4")
    time.sleep(0.3)


def test_05(set_up_fixture):
    print("用例5")
    time.sleep(2.3)
```

当 N=0 的时候显示全部用例的运行时间

```
>pytest test_dur.py --durations=0 -v
============================= test session starts =============================
collected 5 items

test_dur.py::test_01 PASSED                                              [ 20%]
test_dur.py::test_02 PASSED                                              [ 40%]
test_dur.py::test_03 PASSED                                              [ 60%]
test_dur.py::test_04 PASSED                                              [ 80%]
test_dur.py::test_05 PASSED                                              [100%]

=========================== slowest test durations ============================
2.30s call     test_dur.py::test_05
1.20s call     test_dur.py::test_03
1.00s call     test_dur.py::test_01
0.60s call     test_dur.py::test_02
0.30s call     test_dur.py::test_04
0.20s teardown test_dur.py::test_05
0.20s teardown test_dur.py::test_01
0.20s teardown test_dur.py::test_02
0.20s teardown test_dur.py::test_03
0.20s teardown test_dur.py::test_04
0.10s setup    test_dur.py::test_03
0.10s setup    test_dur.py::test_01
0.10s setup    test_dur.py::test_02
0.10s setup    test_dur.py::test_05
0.10s setup    test_dur.py::test_04
========================== 5 passed in 7.05 seconds ===========================
```

用例运行的时候会经历3个阶段：setup,call,teardown。call就是测试用例，setup和teardown就是用例的fixture部分。

#### --durations=3

如果我们只需要筛选出运行时间最慢的3条用例，可以设置`--durations=3`

```
>pytest test_dur.py --durations=3 -v
============================= test session starts =============================

collected 5 items

test_dur.py::test_01 PASSED                                              [ 20%]
test_dur.py::test_02 PASSED                                              [ 40%]
test_dur.py::test_03 PASSED                                              [ 60%]
test_dur.py::test_04 PASSED                                              [ 80%]
test_dur.py::test_05 PASSED                                              [100%]

========================== slowest 3 test durations ===========================
2.30s call     test_dur.py::test_05
1.20s call     test_dur.py::test_03
1.00s call     test_dur.py::test_01
========================== 5 passed in 7.00 seconds ===========================
```

这样就可以对运行慢的用例针对性优化。

# [pytest文档51-内置fixture之cache使用](https://www.cnblogs.com/yoyoketang/p/13613045.html)

#### 前言

pytest 运行完用例之后会生成一个 .pytest_cache 的缓存文件夹，用于记录用例的ids和上一次失败的用例。
方便我们在运行用例的时候加上--lf 和 --ff 参数，快速运行上一次失败的用例。
--lf, --last-failed 只重新运行上次运行失败的用例（或如果没有失败的话会全部跑）
--ff, --failed-first 运行所有测试，但首先运行上次运行失败的测试（这可能会重新测试，从而导致重复的fixture setup/teardown）
--lf 和 --ff 相关介绍查看之前的这篇https://www.cnblogs.com/yoyoketang/p/9769559.html

#### cache

`pytest -h` 查看命令行参数，关于 cache 参数的使用方式

```
>pytest -h

--lf, --last-failed   rerun only the tests that failed at the last run (or
                        all if none failed)
--ff, --failed-first  run all tests but run the last failures first. This
                        may re-order tests and thus lead to repeated fixture
--nf, --new-first     run tests from new files first, then the rest of the
                        tests sorted by file mtime
--cache-show=[CACHESHOW]
                        show cache contents, don't perform collection or
                        tests. Optional argument: glob (default: '*').
--cache-clear         remove all cache contents at start of test run.
```

参数说明：

- --lf 也可以使用 `--last-failed` 仅运行上一次失败的用例
- --ff 也可以使用 `--failed-first` 运行全部的用例，但是上一次失败的用例先运行
- --nf 也可以使用 `--new-first` 根据文件插件的时间，新的测试用例会先运行
- --cache-show=[CACHESHOW] 显示.pytest_cache文件内容，不会收集用例也不会测试用例，选项参数: glob (默认: '*')
- --cache-clear 测试之前先清空.pytest_cache文件

#### --cache-show

测试案例代码test_x.py

```
# test_x.py
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


def test_01():
    a = "hello"
    b = "hello"
    assert a == b


def test_02():
    a = "hello"
    b = "hello world"
    assert a == b


def test_03():
    a = "hello"
    b = "hello world"
    assert a in b


def test_04():
    a = "hello"
    b = "hello world"
    assert a not in b
```

命令行输入 运行完成后，会有2个用例失败，2个用例成功

```
>pytest test_x.py --tb=no
============================= test session starts =============================
collected 4 items

test_x.py .F.F                                                           [100%]

===================== 2 failed, 2 passed in 0.11 seconds ======================
```

运行完成后，会在当前的目录生成一个 `.pytest_cache` 的缓存文件夹,层级结构如下
![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200904113450634-1915931493.png)

lastfailed 文件记录上一次运行失败的用例

```
{
  "test_x.py::test_02": true,
  "test_x.py::test_04": true
}
```

nodeids 文件记录所有用例的节点

```
[
  "test_x.py::test_01",
  "test_x.py::test_02",
  "test_x.py::test_03",
  "test_x.py::test_04"
]
```

于是可以通过 pytest --cache-show 命令查看cache目录

```
D:\soft\kecheng202004\xuexi>pytest --cache-show
============================= test session starts =============================
cachedir: \.pytest_cache
---------------------------- cache values for '*' -----------------------------
cache\lastfailed contains:
  {'test_x.py::test_02': True, 'test_x.py::test_04': True}
cache\nodeids contains:
  ['test_x.py::test_01',
   'test_x.py::test_02',
   'test_x.py::test_03',
   'test_x.py::test_04']
cache\stepwise contains:
  []

======================== no tests ran in 0.02 seconds =========================
```

#### --cache-clear

--cache-clear 用于在测试用例开始之前清空cache的内容

> pytest --cache-clear

# [pytest文档52-命令行参数--setup-show查看fixture的执行过程](https://www.cnblogs.com/yoyoketang/p/13625209.html)

#### 前言

使用命令行运行 pytest 用例的时候，看不到 fixture 的执行过程.
如果我们想知道fixture的执行过程和先后顺序，可以加上 `--setup-show` 命令行参数，帮助查看 fixture 的执行过程.

#### --setup-show

案例参考test_s.py

```
# test_s.py
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


@pytest.fixture()
def login():
    print("前置操作：准备数据")
    yield
    print("后置操作：清理数据")


def test_01(login):
    a = "hello"
    b = "hello"
    assert a == b


def test_02(login):
    a = "hello"
    b = "hello world"
    assert a in b
```

命令行执行 pytest test_s.py

```
>pytest test_s.py
============================= test session starts =============================

collected 2 items

test_s.py ..                                                             [100%]

========================== 2 passed in 0.10 seconds ===========================
```

加上 `--setup-show` 命令行参数后执行

```
>pytest test_s.py --setup-show
============================= test session starts =============================
collected 2 items

test_s.py
SETUP    S base_url
SETUP    S _verify_url (fixtures used: base_url)
        SETUP    F __pytest_repeat_step_number
        SETUP    F login
        test_s.py::test_01 (fixtures used: __pytest_repeat_step_number, _verify_url, base_url, login).
        TEARDOWN F login
        TEARDOWN F __pytest_repeat_step_number
        SETUP    F __pytest_repeat_step_number
        SETUP    F login
        test_s.py::test_02 (fixtures used: __pytest_repeat_step_number, _verify_url, base_url, login).
        TEARDOWN F login
        TEARDOWN F __pytest_repeat_step_number
TEARDOWN S _verify_url
TEARDOWN S base_url

========================== 2 passed in 0.04 seconds ===========================
```

这样就可以方便查看用例调用了哪些fixture，上面用例里面只写了一个`login`，
但是从回溯信息上看到还有几个是内置的fixture会自动调用：__pytest_repeat_step_number, _verify_url, base_url。

# [pytest文档53-命令行实时输出错误信息(pytest-instafail)](https://www.cnblogs.com/yoyoketang/p/13626256.html)

#### 前言

pytest 运行全部用例的时候，在控制台会先显示用例的运行结果(.或F), 用例全部运行完成后最后把报错信息全部一起抛出到控制台。
这样我们每次都需要等用例运行结束，才知道为什么报错，不方便实时查看报错信息。
pytest-instafail 插件可以在运行用例的时候，需实时查看用例报错内容，这样方便跟踪问题。

#### --instafail

执行全部用例，报错内容等用例运行完成才显示出来

```
>pytest
============================= test session starts =============================

collected 11 items

test_s.py ..                                                             [ 18%]
test_t.py ...                                                            [ 45%]
test_x.py .F.F                                                           [ 81%]
test_y.py ..                                                             [100%]

================================== FAILURES ===================================
___________________________________ test_02 ___________________________________

    def test_02():
        a = "hello"
        b = "hello world"
>       assert a == b
E       AssertionError: assert 'hello' == 'hello world'
E         - hello
E         + hello world

test_x.py:12: AssertionError
___________________________________ test_04 ___________________________________

    def test_04():
        a = "hello"
        b = "hello world"
>       assert a not in b
E       AssertionError: assert 'hello' not in 'hello world'
E         'hello' is contained here:
E           hello world

test_x.py:24: AssertionError
===================== 2 failed, 9 passed in 1.32 seconds ======================
```

当用例很多的时候，不方便我们查看具体哪个报错对应哪条用例，加上`--instafail`参数，方便实时查看报错内容

```
>pytest --instafail
============================= test session starts =============================

collected 11 items

test_s.py ..                                                             [ 18%]
test_t.py ...                                                            [ 45%]
test_x.py .F

___________________________________ test_02 ___________________________________

    def test_02():
        a = "hello"
        b = "hello world"
>       assert a == b
E       AssertionError: assert 'hello' == 'hello world'
E         - hello
E         + hello world

test_x.py:12: AssertionError

test_x.py .F

___________________________________ test_04 ___________________________________

    def test_04():
        a = "hello"
        b = "hello world"
>       assert a not in b
E       AssertionError: assert 'hello' not in 'hello world'
E         'hello' is contained here:
E           hello world

test_x.py:24: AssertionError

test_y.py ..                                                             [100%]

===================== 2 failed, 9 passed in 1.37 seconds ======================
```

结合`--tb=line`参数，看起来更直观

```
>pytest --instafail --tb=line
============================= test session starts =============================
collected 11 items

test_s.py ..                                                             [ 18%]
test_t.py ...                                                            [ 45%]
test_x.py .F

D:\test_x.py:12: AssertionError: assert 'hello' == 'hello world'

test_x.py .F

D:\test_x.py:24: AssertionError: assert 'hello' not in 'hello world'

test_y.py ..                                                             [100%]

===================== 2 failed, 9 passed in 1.30 seconds ======================
```

# [pytest文档54-Hooks函数terminal打印测试结果(pytest_report_teststatus)](https://www.cnblogs.com/yoyoketang/p/13631185.html)

#### 前言

使用命令行执行pytest用例的时候，会在 terminal 终端打印整个用例的测试结果：

- .代表通过的用例
- F代表失败的用例
- E代表异常的用例
	如果我们不喜欢这种报告结果，可以通过 pytest_report_teststatus 钩子函数改变测试报告的内容，接下来试试吧.改成√，把F改成x，这样更直观。

#### pytest_report_teststatus

pytest_report_teststatus(report, config): 返回各个测试阶段的result, 可以用when属性来区分不同阶段。

- when=='setup' 用例的前置操作
- when=='call' 用例的执行
- when=='teardown' 用例的后置操作

运行案例test_x.py

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

def test_01():
    a = "hello"
    b = "hello"
    assert a == b


def test_02():
    a = "hello"
    b = "hello world"
    assert a == b


def test_03():
    a = "hello"
    b = "hello world"
    assert a in b


def test_04():
    a = "hello"
    b = "hello world"
    assert a not in b
```

命令行执行`pytest test_x.py --tb=line`

```
>pytest test_x.py --tb=line
============================= test session starts =============================

collected 4 items

test_x.py .F.F                                                           [100%]

================================== FAILURES ===================================
D:\test_x.py:13: AssertionError: assert 'hello' == 'hello world'
D:\test_x.py:25: AssertionError: assert 'hello' not in 'hello world'
===================== 2 failed, 2 passed in 0.07 seconds ======================
```

运行的结果是.和F,我们希望改成√和x,在conftest.py文件写钩子函数

```
# conftest.py
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

def pytest_report_teststatus(report, config):
    '''turn . into √，turn F into x'''
    if report.when == 'call' and report.failed:
        return (report.outcome, 'x', 'failed')
    if report.when == 'call' and report.passed:
        return (report.outcome, '√', 'passed')
```

重新运行`pytest test_x.py --tb=line`

```
>pytest test_x.py --tb=line
collected 4 items

test_x.py √x√x                                                           [100%]

================================== FAILURES ===================================
D:\soft\kecheng202004\xuexi\test_x.py:13: AssertionError: assert 'hello' == 'hello world'
D:\soft\kecheng202004\xuexi\test_x.py:25: AssertionError: assert 'hello' not in 'hello world'
===================== 2 failed, 2 passed in 0.07 seconds ======================
```

#### 关于Error异常

前面这篇https://www.cnblogs.com/yoyoketang/p/12609871.html讲到关于测试用例的执行结果,
当 setup 出现异常的时候，用例才会Error,于是可以通过report.when == 'setup' 判断到前置操作的结果

```
# test_x.py
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

@pytest.fixture()
def login():
    print("前置操作：准备数据")
    assert 1 == 2   # 前置出现异常
    yield
    print("后置操作：清理数据")


def test_01(login):
    a = "hello"
    b = "hello"
    assert a == b


def test_02():
    a = "hello"
    b = "hello world"
    assert a == b


def test_03():
    a = "hello"
    b = "hello world"
    assert a in b


def test_04():
    a = "hello"
    b = "hello world"
    assert a not in b
```

运行结果

```
>pytest test_x.py --tb=line
============================= test session starts =============================

collected 4 items

test_x.py Ex√x                                                           [100%]

=================================== ERRORS ====================================
__________________________ ERROR at setup of test_01 __________________________
E   assert 1 == 2
---------------------------- Captured stdout setup ----------------------------
前置操作：准备数据
================================== FAILURES ===================================
D:\soft\kecheng202004\xuexi\test_x.py:21: AssertionError: assert 'hello' == 'hello world'
D:\soft\kecheng202004\xuexi\test_x.py:33: AssertionError: assert 'hello' not in 'hello world'
================= 2 failed, 1 passed, 1 error in 0.09 seconds =================
```

当前置失败的时候，改成0

```
# conftest.py
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


def pytest_report_teststatus(report, config):
    '''turn . into √，turn F into x, turn E into 0'''
    if report.when == 'call' and report.failed:
        return (report.outcome, 'x', 'failed')
    if report.when == 'call' and report.passed:
        return (report.outcome, '√', 'passed')
    if report.when == 'setup' and report.failed:
        return (report.outcome, '0', 'error')
```

于是控制台的结果，就可以改了

```
>pytest test_x.py --tb=line
============================= test session starts =============================

collected 4 items

test_x.py 0x√x                                                           [100%]

================================== FAILURES ===================================
D:\soft\kecheng202004\xuexi\test_x.py:7: assert 1 == 2
D:\soft\kecheng202004\xuexi\test_x.py:21: AssertionError: assert 'hello' == 'hello world'
D:\soft\kecheng202004\xuexi\test_x.py:33: AssertionError: assert 'hello' not in 'hello world'
===================== 3 failed, 1 passed in 0.07 seconds ======================
```

skip的用例可以通过report.skiped获取到,可以这样写

```
if report.skipped:
        return (report.outcome, '/', 'skipped')
```

#### report相关的属性

report相关的属性，参考以下
'_from_json',
'_get_verbose_word',
'_to_json',
'caplog',
'capstderr',
'capstdout',
'count_towards_summary',
'duration',
'failed',
'from_item_and_call',
'fspath',
'get_sections',
'head_line',
'keywords',
'location',
'longrepr',
'longreprtext',
'nodeid',
'outcome',
'passed',
'sections',
'skipped',
'toterminal',
'user_properties',
'when'





# [pytest文档55-plugins插件开发](https://www.cnblogs.com/yoyoketang/p/13638661.html)

#### 前言

前面一篇已经学会了使用hook函数改变pytest运行的结果，代码写在conftest.py文件，实际上就是本地的插件了。
当有一天你公司的小伙伴觉得你写的还不错，或者更多的小伙伴想要你这个功能，于是你就想着放到github上，写成一个插件，方便小伙伴使用pip去安装。

#### 插件开发

先新建一个工程，工程名称就是插件名称，一般以pytest-开头命名，目录结构如下

![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200909141822129-978718943.png)

- setup.py 在安装python的相关模块和库时，我们一般使用`pip install 模块名`或者`python setup.py install`，前者是在线安装，会安装该包的相关依赖包；
	后者是下载源码包然后在本地安装，不会安装该包的相关依赖包
- README.rst README 文档，告诉用户如何使用你的插件，具体能实现什么功能
- pytest_change_report.py 也就是之前conftest.py里面写的hook函数实现的功能
- tests 用于测试本插件的相关功能，属于自测的内容
- tests/conftest.py 开启需要的插件pytester
- tests/test_change_report.py 测试插件的代码

#### setup.py

在安装python的相关模块和库时，我们一般使用`pip install 模块名`或者`python setup.py install`，前者是在线安装，会安装该包的相关依赖包；
后者是下载源码包然后在本地安装，不会安装该包的相关依赖包.
setup.py 描述安装包相关的信息

```
from setuptools import setup

"""The setup script.
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/
"""

setup(
    name='pytest-change-report',
    url='https://github.com/yoyoketang/pytest-change-report',
    version='1.0',
    author="yoyo",
    author_email='283340479@qq.com',
    description='turn . into √，turn F into x',
    long_description='print result on terminal turn . into √，turn F into x using hook',
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.6',
    ],
    license='proprietary',
    py_modules=['pytest_change_report'],
    keywords=[
        'pytest', 'py.test', 'pytest-change-report',
    ],

    install_requires=[
        'pytest'
    ],
    entry_points={
        'pytest11': [
            'change-report = pytest_change_report',
        ]
    }
)
```

#### pytest_change_report.py

插件的核心功能，也就是之前在conftest.py用hook函数实现的功能。
我们现在实现的功能:
1.把测试的结果.改成√，F改成x
2.命令行加个`--change`参数开关，默认不开启，当加上参数`--change on·的时候才生效

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


def pytest_addoption(parser):
    parser.addoption(
        "--change",
        action="store",
        default="off",
        help="'Default 'off' for change, option: on or off"
    )


def pytest_report_teststatus(report, config):
    '''turn . into √，turn F into x, turn E into 0'''
    if config.getoption("--change") == "on":
        if report.when == 'call' and report.failed:
            return (report.outcome, 'x', 'failed')
        if report.when == 'call' and report.passed:
            return (report.outcome, '√', 'passed')
```

#### 测试插件

当插件功能实现完成后，需要在tests目录测试自己写的插件

tests/conftest.py 文件开启pytester,专门用于测试插件的

```
'''pytester is needed for testing plgugins.'''


pytest_plugins = ['pytester']
```

tests/test_change_report.py 文件写测试用例

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

def test_raw_report(testdir):
    """Make sure that our plugin works."""
    # create a temporary pytest test file
    testdir.makepyfile(
        """
        def test_01():
            a = "hello"
            b = "hello"
            assert a == b

        def test_02():
            a = "hello"
            b = "hello world"
            assert a == b
         """
            )

    # run all tests with pytest
    result = testdir.runpytest()

    # check that 1 test passed, 1 test failed.
    result.assert_outcomes(passed=1, failed=1)
    result.stdout.fnmatch_lines(["*.F*", ])

def test_change_on_report(testdir):
    """Make sure that our plugin works."""
    # create a temporary pytest test file
    testdir.makepyfile(
        """
        def test_01():
            a = "hello"
            b = "hello"
            assert a == b

        def test_02():
            a = "hello"
            b = "hello world"
            assert a == b
         """
            )

    # run all tests with pytest
    result = testdir.runpytest("--change", "on")

    # check that 1 test passed, 1 test failed.
    result.stdout.fnmatch_lines(['*√x*', ])


def test_change_off_report(testdir):
    """Make sure that our plugin works."""
    # create a temporary pytest test file
    testdir.makepyfile(
        """
        def test_01():
            a = "hello"
            b = "hello"
            assert a == b

        def test_02():
            a = "hello"
            b = "hello world"
            assert a == b
         """
            )

    # run all tests with pytest
    result = testdir.runpytest("--change", "off")

    # check that 1 test passed, 1 test failed.
    result.stdout.fnmatch_lines(['*.F*', ])


def test_change_default_report(testdir):
    """Make sure that our plugin works."""
    # create a temporary pytest test file
    testdir.makepyfile(
        """
        def test_01():
            a = "hello"
            b = "hello"
            assert a == b

        def test_02():
            a = "hello"
            b = "hello world"
            assert a == b
         """
            )

    # run all tests with pytest
    result = testdir.runpytest("--change")

    # check stderr pytest: error: argument --change: expected one argument
    result.stderr.fnmatch_lines(['*argument --change: expected one argument*', ])


def test_verbose_report(testdir):
    """Make sure that our plugin works."""
    # create a temporary pytest test file
    testdir.makepyfile(
        """
        def test_01():
            a = "hello"
            b = "hello"
            assert a == b

        def test_02():
            a = "hello"
            b = "hello world"
            assert a == b
         """
            )

    # run all tests with pytest
    result = testdir.runpytest("-v")

    # check that 1 test passed, 1 test failed.
    result.stdout.fnmatch_lines(['*::test_01 PASSED*', '*::test_02 FAILED*'])



def test_change_verbose_report(testdir):
    """Make sure that our plugin works."""
    # create a temporary pytest test file
    testdir.makepyfile(
        """
        def test_01():
            a = "hello"
            b = "hello"
            assert a == b

        def test_02():
            a = "hello"
            b = "hello world"
            assert a == b
         """
            )

    # run all tests with pytest
    result = testdir.runpytest("--change", "on", "-v")

    # check that 1 test passed, 1 test failed.
    result.stdout.fnmatch_lines(['*::test_01 passed*', '*::test_02 failed*'])


def test_help(testdir):
    """Make sure that our plugin works."""
    # create a temporary pytest test file
    testdir.makepyfile(
        """
        def test_01():
            a = "hello"
            b = "hello"
            assert a == b
         """
            )

    # run all tests with pytest
    result = testdir.runpytest("--help")

    # check --help
    result.stdout.fnmatch_lines(["*--change=*", ])
```

#### 本地安装插件

cd到插件的项目目录，使用pip安装

> pip install .

```
>pip install .
Processing d:\soft\pytest-change-report
Using legacy setup.py install for pytest-change-report, since package 'wheel' is not installed.
Installing collected packages: pytest-change-report
  Attempting uninstall: pytest-change-report
    Found existing installation: pytest-change-report 1.0
    Uninstalling pytest-change-report-1.0:
      Successfully uninstalled pytest-change-report-1.0
    Running setup.py install for pytest-change-report ... done
Successfully installed pytest-change-report-1.0
```

安装完成后，在cmd输入 pip show pytest-change-report就可以看到前面setup.py里面的描述内容

```
>pip show pytest-change-report
Name: pytest-change-report
Version: 1.0
Summary: turn . into √，turn F into x
Home-page: https://github.com/yoyoketang/pytest-change-report
Author: yoyo
Author-email: 283340479@qq.com
License: proprietary
Location: e:\python36\lib\site-packages\pytest_change_report-1.0-py3.6.egg
Requires: pytest
Required-by:
```

安装完成后，输入pytest测试tests/test_change_report.py

```
>pytest
============================= test session starts =============================

collected 7 items

tests\test_change_report.py .......                                      [100%]

========================== 7 passed in 0.89 seconds ===========================
```

测试文件里面的用例全部通过

#### README.rst

最后需要写个 README.rst 使用教程文档，这样你写的插件就能被其它小伙伴学习和使用了。

```
==============
pytest-change-report: pytest plugin
==============


**This pytest plugin turn . into √，turn F into x**


Usage
=====

从github源码安装

   pip install git+https://github.com/yoyoketang/pytest-change-report.git

命令行运行示例

   pytest --change on


demo
====

先写pytest用例test_demo.py

    def test_01():
        a = "hello"
        b = "hello"
        assert a == b


    def test_02(login):
        a = "hello"
        b = "hello world"
        assert a == b

命令行执行pytest, 默认不会改变之前的报告内容

    >pytest test_demo.py
    ============================= test session starts =============================
    collected 2 items

    test_demo.py .F                                                          [100%]

    ================================== FAILURES ===================================
    ___________________________________ test_02 ___________________________________

        def test_02():
            a = "hello"
            b = "hello world"
    >       assert a == b
    E       AssertionError: assert 'hello' == 'hello world'
    E         - hello
    E         + hello world

    test_demo.py:10: AssertionError
    ===================== 1 failed, 1 passed in 0.11 seconds ======================

加上 --change on 参数后运行

    >pytest test_demo.py --change on
    ============================= test session starts =============================
    collected 2 items

    test_demo.py √x                                                          [100%]

    ================================== FAILURES ===================================
    ___________________________________ test_02 ___________________________________

        def test_02():
            a = "hello"
            b = "hello world"
    >       assert a == b
    E       AssertionError: assert 'hello' == 'hello world'
    E         - hello
    E         + hello world

    test_demo.py:10: AssertionError
    ===================== 1 failed, 1 passed in 0.08 seconds ======================



pytest.ini
==========

可以添加到pytest.ini配置文件，这样默认就会带上--change参数

      [pytest]
      --change = on

# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/
```

#### 提交github

最后把插件代码提交到github仓库，方便下载https://github.com/yoyoketang/pytest-change-report

![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200909170622186-705542378.png)

# [pytest文档56-插件打包上传到 pypi 库](https://www.cnblogs.com/yoyoketang/p/13665907.html)

#### 前言

pytest 的插件完成之后，可以上传到 github，方便其他小伙伴通过 pip 源码安装。如果我们想通过 `pip install packages` 这种方式安装的话，需上传到 pypi 仓库

#### pypi仓库

pip，全称是：python install packages，它是一个通用的 Python 包管理工具，是easy_install的替代品, 主要是用于安装 PyPI 上的软件包。
PyPI，全称是：Python Package Index，它是Python官方的第三方库的仓库，所有人都可以下载第三方库或上传自己开发的库到PyPI。
PyPI推荐使用pip包管理器来下载第三方库。

我们想把python包上传到pypi,需在 https://pypi.org/ 注册一个账号

![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200914111922036-369096557.png)

#### 整理项目结构

前面这篇https://www.cnblogs.com/yoyoketang/p/13638661.htmlpytest 插件的开发，就是一个半成品了

整个目录结构如下

```
pytest-change-report
├── LICENSE
├── README.rst
├── requirements.txt
├── setup.py
├── pytest_change_report.py
├── tests
│   ├──__init__.py
│   ├──conftest.py
│   └──test_change_report.py
```

- pytest-change-report 是项目的包名
- LICENSE LICENSE文件是授权文件，比如：MIT license， APACHE license
- requirements.txt 依赖包，比如这个插件依赖pytest模块，可以写pytest==4.5.0
- README.rst 其实就是项目介绍和使用说明帮助文档
- setup.py python模块安装所需要的文件
- tests 是测试的目录
- pytest_change_report.py 插件实现功能的核心模块

代码写完测试没问题后，上传到github仓库，并打个v1.0的标签
![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200914113824775-238032280.png)
打完 tag 标签，push 到 github 仓库，这样在 tag 目录就能看到 release 的记录了
![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200914114009171-431876979.png)

#### 打包

cd到项目的根目录，执行

> python setup.py sdist build

执行完成后，在dist目录，会生成一个.tar.gz的压缩包，这个压缩包就可以通过 pip 安装了

![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200914114200613-676003848.png)

也可以打包一个wheels格式的包，需要安装wheel包：

> pip install wheel

执行以下命令打包

> python setup.py bdist_wheel --universal

这样在dist目录生成一个 pytest_change_report-1.0-py2.py3-none-any.whl 文件，.whl 后置的文件也可以通过 pip 直接安装

#### 上传发布

使用twine上传,先安装twine

> pip install twine

上传输入指令，接着会提示输入账号和密码

> twine upload dist/*

```
>twine upload dist/*
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: yoyoketang
Enter your password:
Uploading pytest_change_report-1.0-py2.py3-none-any.whl
100%|█████████████████████████████████████████████████████████ ████████████████████| 5.56k/5.56k [00:00<00:00, 6.17kB/s]
Uploading pytest-change-report-1.0.tar.gz
100%|█████████████████████████████████████████████████████████ ████████████████████| 5.15k/5.15k [00:01<00:00, 4.71kB/s]

View at:
https://pypi.org/project/pytest-change-report/1.0/
```

上传后访问地址 https://pypi.org/project/pytest-change-report/1.0/

#### 查看pypi

打开上面的访问地址可以查看到已经上传成功
![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200914115939953-1708400536.png)

点 Homepage 可以跳转到 github 仓库去

这样小伙伴们就能直接使用 pip 安装了

> pip install pytest-change-report

python 打包发布到 pypi 的就完成了，是不是很激动！

# [pytest文档57-计算单元测试代码覆盖率(pytest-cov)](https://www.cnblogs.com/yoyoketang/p/13672409.html)

#### 前言

我们在做测试的时候，经常遇到领导的灵魂拷问：你的测试用例覆盖率是多少，达到100%了么？你如何保证你的测试质量？
测试用例的覆盖率如何统计呢，如何知道开发的代码，我们都测到了，不会存在漏测的情况。

#### pytest-cov

先命令行安装 pytest-cov 2.10.1版本

> pip install pytest-cov==2.10.1

环境要求：
1.python3.6.6 版本
备注：其它版本没试过

python3.6.0会遇到以下问题

```
INTERNALERROR>raise CoverageException("Couldn't use data file {!r}:{}".format(self.filename, msg))
INTERNALERROR> coverage.misc.CoverageException: Couldn't use data file'C:\\Users\\Desktop\\Pytest\\.coverage': 
Safety level may not be changed inside a transaction
```

解决办法：安装3.6.1以上版本

#### 实现功能

在做单元测试时，代码覆盖率常常被拿来作为衡量测试好坏的指标，甚至，用代码覆盖率来考核测试任务完成情况，
比如，代码覆盖率必须达到80％或 90％。于是乎，测试人员费尽心思设计案例覆盖代码。
单元测试的方法有：语句覆盖/判定覆盖/条件覆盖/路径覆盖

先看一个简单的案例，前端实现一个功能，根据接口返回的不同code值，判断支付的结果，给用户返回提示友好的信息

```
前端实现功能：根据接口返回的不同code值，判断支付的结果，给用户返回提示友好的信息
接口返回格式：
{
    "code": 0,
    "msg": "success!",
    "data": []
}

错误码参照
0 - 成功
30000 - 参数错误
30001 - 余额不足
30002 - 达到当天最大额度
201102 - 银行卡被冻结
```

实现代码

```
'''
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/
接口返回格式
{
    "code": 0,
    "msg": "success!",
    "data": []
}

错误码参照
0 - 成功
30000 - 参数错误
30001 - 余额不足
30002 - 达到当天最大额度
201102 - 银行卡被冻结
'''
# pay.py
def pay_status(result):
    '''根据接口返回code状态，给用户提示对应的结果'''
    if result.get("code") == 0:
        return "支付成功"
    elif result.get("code") == 30000:
        return "支付失败: %s" % result.get("msg")
    elif result.get("code") == 30001:
        return "支付失败: %s" % result.get("msg")
    elif result.get("code") == 30002:
        return "支付失败: %s" % result.get("msg")
    elif result.get("code") == 201102:
        return "支付失败: %s" % result.get("msg")
    else:
        return "支付失败: 系统异常，未知错误"
```

整个项目目录结构如下

- src 是项目的源码
- tests 是我们写的单元测试用例
- src和tests放同一个项目的根目录下
	![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200915115240782-1426605693.png)

#### 用例设计

在tests/test_pay.py下写测试用例,先只写一个支付成功的案例

```
from src.pay import pay_status
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


def test_pay_success():
    result = {
            "code": 0,
            "msg": "success!",
            "data": []
        }
    assert pay_status(result) == "支付成功"
```

#### 运行用例

运行用例的时候加上 --cov 参数

> pytest --cov

运行结果

```
>pytest --cov
================================================= test session starts =================================================
platform win32 -- Python 3.6.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
rootdir: D:\soft\pytest-demo-cov
plugins: change-report-1.0, cov-2.10.1, html-1.19.0, metadata-1.8.0
collected 1 item

tests\test_pay.py .                                                                                              [100%]

----------- coverage: platform win32, python 3.6.6-final-0 -----------
Name                Stmts   Miss  Cover
---------------------------------------
src\__init__.py         0      0   100%
src\pay.py             13      9    31%
tests\__init__.py       0      0   100%
tests\test_pay.py       4      0   100%
---------------------------------------
TOTAL                  17      9    47%


================================================== 1 passed in 0.10s ==================================================
```

从报告可以看出src\pay.py 的代码测试覆盖率是31%，其它文件都是100%覆盖，这就说明我们单元测试代码测试覆盖率是31%
还有一个指标是**测试用例的执行率**，测试用例在test_pay.py文件，执行率是100%，说明用例全部执行了。

#### coverage生成html报告

coverage 相关参数查看，使用pytest -h

```
> pytest -h
coverage reporting with distributed testing support:
  --cov=[SOURCE]        Path or package name to measure during execution (multi-allowed). Use --cov= to not do any
                        source filtering and record everything.
  --cov-report=TYPE     Type of report to generate: term, term-missing, annotate, html, xml (multi-allowed). term, term-
                        missing may be followed by ":skip-covered". annotate, html and xml may be followed by ":DEST"
                        where DEST specifies the output location. Use --cov-report= to not generate any output.
  --cov-config=PATH     Config file for coverage. Default: .coveragerc
  --no-cov-on-fail      Do not report coverage if test run fails. Default: False
  --no-cov              Disable coverage report completely (useful for debuggers). Default: False
  --cov-fail-under=MIN  Fail if the total coverage is less than MIN.
  --cov-append          Do not delete coverage but append to current. Default: False
  --cov-branch          Enable branch coverage.
  --cov-context=CONTEXT
                        Dynamic contexts to use. "test" for now.
```

生成html的报告

> pytest --cov --cov-report=html

执行完成，在项目根目录会生成 htmlcov 目录

![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200915121137261-169015732.png)

运行 index.html 文件查看代码覆盖率

![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200915121243283-2140191029.png)

点开src\pay.py

![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200915121338805-433301895.png)

想覆盖率达到100%，那得再继续写用例，让每个if分支情况都覆盖到

#### 指定被测代码

如果我们想指定执行项目里面的某个模块，可以通过--cov=模块 来运行

> pytest --cov=src

```
>pytest --cov=src
================================================= test session starts =================================================
platform win32 -- Python 3.6.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
rootdir: D:\soft\pytest-demo-cov
plugins: change-report-1.0, cov-2.10.1, html-1.19.0, metadata-1.8.0
collected 1 item

tests\test_pay.py .                                                                                              [100%]

----------- coverage: platform win32, python 3.6.6-final-0 -----------
Name              Stmts   Miss  Cover
-------------------------------------
src\__init__.py       0      0   100%
src\pay.py           13      9    31%
-------------------------------------
TOTAL                13      9    31%


================================================== 1 passed in 0.07s ==================================================
```

也可以指定具体的py模块名称

> pytest --cov=src.pay

但不能写成`pytest --cov=src/pay.py`

# [pytest文档58-随机执行测试用例(pytest-random-order)](https://www.cnblogs.com/yoyoketang/p/13677878.html)

#### 前言

通常我们认为每个测试用例都是相互独立的，因此需要保证测试结果不依赖于测试顺序，以不同的顺序运行测试用例，可以得到相同的结果。
pytest默认运行用例的顺序是按模块和用例命名的 ASCII 编码顺序执行的，这就意味着每次运行用例的顺序都是一样的。
app 测试里面有个 monkey 测试，随机在页面点点点，不按常理的点点点能找到更多的不稳定性 bug。那么我们在写pytest用例的时候，既然每个用例都是相互独立的，
那就可以打乱用例的顺序随机执行，用到 pytest 的插件 pytest-random-order 可以实现此目的，github 地址https://github.com/jbasko/pytest-random-order

#### pytest-random-order 插件

pytest-random-order是一个pytest插件，用于随机化测试顺序。这对于检测通过的测试可能是有用的，因为该测试恰好在不相关的测试之后运行，从而使系统处于良好状态。
该插件允许用户控制他们想要引入的随机性级别，并禁止对测试子集进行重新排序。通过传递先前测试运行中报告的种子值，可以按特定顺序重新运行测试。
![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200916102729298-1578550308.png)

使用pip安装

> pip install pytest-random-order

在pytest -h查看，命令行可以有三个参数选择

```
pytest-random-order options:
  --random-order        Randomise test order (by default, it is disabled) with default configuration.
  --random-order-bucket={global,package,module,class,parent,grandparent,none}
                        Randomise test order within specified test buckets.
  --random-order-seed=RANDOM_ORDER_SEED
                        Randomise test order using a specific seed.
```

从v1.0.0开始，默认情况下，此插件不再将测试随机化。要启用随机化，您必须以下列方式之一运行pytest：

```
pytest --random-order
pytest --random-order-bucket=<bucket_type>
pytest --random-order-seed=<seed>
```

如果要始终随机化测试顺序，请配置pytest。有很多方法可以做到这一点，我最喜欢的一种方法是addopts = --random-order在pytest选项（通常是[pytest]或[tool:pytest]部分）下添加特定于项目的配置文件。

```
# pytest.ini文件内容
[pytest]
addopts = --random-order
```

#### --random-order 随机测试

先写几个简单的用例，目录结构如下
![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200916103155405-1665785160.png)

module1/test_order1.py内容

```
# module1/test_order1.py
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


class TestRandom():

    def test_01(self):
        print("用例1")

    def test_02(self):
        print("用例2")

    def test_03(self):
        print("用例3")
```

module2/test_order2.py内容

```
# module2/test_order2.py
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


class TestDemo():

    def test_04(self):
        print("用例4")

    def test_05(self):
        print("用例5")

    def test_06(self):
        print("用例6")
```

带上`--random-order`参数运行用例

```
>pytest --random-order -v
================================================= test session starts =================================================
Using --random-order-bucket=module
Using --random-order-seed=357703
collected 6 items

module2/test_order2.py::TestDemo::test_04 PASSED                                                                 [ 16%]
module2/test_order2.py::TestDemo::test_05 PASSED                                                                 [ 33%]
module2/test_order2.py::TestDemo::test_06 PASSED                                                                 [ 50%]
module1/test_order1.py::TestRandom::test_03 PASSED                                                               [ 66%]
module1/test_order1.py::TestRandom::test_02 PASSED                                                               [ 83%]
module1/test_order1.py::TestRandom::test_01 PASSED                                                               [100%]

================================================== 6 passed in 0.05s ==================================================
```

从运行的结果可以看出，默认使用`--random-order-bucket=module`,模块下的用例会被打乱随机执行，每次运行会重新生成`--random-order-seed=357703`,seed值不一样，用例的顺序也会不一样

#### --random-order-bucket 随机范围

要更改重新排序与范围，运行pytest --random-order-bucket=选项，其中可以是global,package,module,class,parent,grandparent：

插件组在存储桶中进行测试，在存储桶中进行混洗，然后对存储桶进行混洗，设计原理如图

![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200916104033412-1296290689.png)

给定上面的测试套件，以下是一些可能生成的测试顺序中的两个：

![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200916104056922-1340614272.png)

可以从以下几种类型的存储桶中进行选择：

- class 测试将在一个类中进行混洗，而各类将被混洗，但是来自一个类的测试将永远不会在其他类或模块之间运行来自其他类的测试。
- module 模块级别。如果仅使用--random-order运行pytest，同时带上参数--random-order-seed=。
- package 程序包级别。请注意，属于package的模块（以及这些模块内的测试）x.y.z不属于package x.y，因此在对存储package桶类型进行随机分配时，它们将落入不同的存储桶中。
- parent 如果使用的是不属于任何模块的自定义测试项，则可以使用此项将测试项的重新排序限制在它们所属的父级中。对于正常测试函数，父级是声明它们的模块。
- grandparent 类似于上面的parent，但是使用测试项的父级作为bucket key。
- global 所有测试属于同一存储桶，完全随机，测试可能需要更长的时间才能运行。
- none (已弃用) 禁用混洗。自1.0.4起不推荐使用，因为此插件默认不再重做测试，因此没有禁用的功能。

如果你有测试三个桶A，B和C三个测试1和2，并3在他们每个人，那么许多潜在的排序的一个非全局随机化可以产生可能是：

> c2，c1，c3，a3，a1，a2，b3，b2，b1

运行示例，带上参数`--random-order-bucket=global`,所有的用例都会被打乱。

```
>pytest --random-order -v --random-order-bucket=global
================================================= test session starts =================================================
Using --random-order-bucket=global
Using --random-order-seed=255529

collected 6 items

module1/test_order1.py::TestRandom::test_02 PASSED                                                               [ 16%]
module1/test_order1.py::TestRandom::test_01 PASSED                                                               [ 33%]
module2/test_order2.py::TestDemo::test_06 PASSED                                                                 [ 50%]
module2/test_order2.py::TestDemo::test_04 PASSED                                                                 [ 66%]
module2/test_order2.py::TestDemo::test_05 PASSED                                                                 [ 83%]
module1/test_order1.py::TestRandom::test_03 PASSED                                                               [100%]

================================================== 6 passed in 0.05s ==================================================
```

最好从最小的存储桶类型开始（class或module取决于您是否有基于类的测试），并在确定测试可以处理较大的存储桶类型时切换为更大的存储桶类型。
如果您的测试依赖模块或会话范围的fixture，则测试的随机性越高，测试速度就越慢。您可能不想在编码时随机global或随机分组，package并且需要快速确认没有什么大问题。``

#### 模块或类中禁用随机

如果我们在一个模块或类中，不想让里面的用例随机，可以设置 `disabled=True` 来禁用随机参数

```
# 写在.py文件最上面即可
pytestmark = pytest.mark.random_order(disabled=True)

def test_number_one():
    assert True

def test_number_two():
    assert True
```

也可以写在class里面

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


class TestRandom():
    pytestmark = pytest.mark.random_order(disabled=True)

    def test_01(self):
        print("用例1")

    def test_02(self):
        print("用例2")

    def test_03(self):
        print("用例3")
```

这样在执行的时候，TestRandom里面的用例顺序就是test_01，test_02，test_03不会被打乱

#### --random-order-seed 随机种子

如果由于重新排序测试而发现测试失败，则可能希望能够以相同的失败顺序重新运行测试。为了允许重现测试订单，该插件报告其与伪随机数生成器一起使用的种子值：

```
============================= test session starts ==============================
..
Using --random-order-bucket=module
Using --random-order-seed=24775
...
```

现在，您可以使用该--random-order-seed=...位作为下一次运行的参数以产生相同的顺序：

> pytest -v --random-order-seed = 24775

#### 禁用插件

如果你觉得这个插件不好用，或者对你的其它功能会有影响，则可以将其禁用

> pytest -p no：random_order

请注意，默认情况下禁用随机化。通过传递，-p no:random_order您将阻止插件的注册，因此其钩子将不会被注册，并且命令行选项也不会出现在中--help

#### 首先运行最后失败的测试

另外 `--failed-first` 标志-上一次运行失败的测试将在通过测试之前运行，而不管改组存储桶类型如何。

# [pytest文档59-运行未提交git的用例(pytest-picked)](https://www.cnblogs.com/yoyoketang/p/13683759.html)

#### 前言

我们每天写完自动化用例后都会提交到 git 仓库，随着用例的增多，为了保证仓库代码的干净，当有用例新增的时候，我们希望只运行新增的未提交 git 仓库的用例。
pytest-picked 插件可以实现只运行未提交到git仓库的代码。

#### pytest-picked

使用命令行安装

> pip install pytest-picked

可使用参数

```
picked:
  --picked=[{only,first}]
                        Run the tests related to the changed files either on their own, or first
  --mode=PICKED_MODE    Options: unstaged, branch
```

使用示例：

```
$ pytest --picked

$ pytest --picked=first

$ pytest --picked --mode=branch

$ pytest --picked --mode=unstaged  # default
```

github仓库地址https://github.com/anapaulagomes/pytest-picked

#### --picked 参数

我们在已提交过 git 仓库的用例里面新增了 2 个文件 test_new.py 和 test_new_2.py

![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200917091141680-1927419115.png)

cd到项目根目录，使用 `git status` 查看当前分支状态

```
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

>git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        new file:   pytest_demo/test_new.py
        new file:   pytest_demo/test_new_2.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   pytest_demo/test_new.py
        modified:   pytest_demo/test_new_2.py
```

可以看到有2个文件，使用 `pytest --picked` 运行用例

```
>pytest --picked

Changed test files... 2. ['pytest_demo/test_new.py', 'pytest_demo/test_new_2.py']
Changed test folders... 0. []
================================================= test session starts =================================================
platform win32 -- Python 3.6.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
rootdir: D:\demo\code\xuexi_pytest
collected 4 items

pytest_demo\test_new.py ..                                                                                       [ 50%]
pytest_demo\test_new_2.py ..                                                                                     [100%]
================================================== 4 passed in 0.20s ==================================================
```

所有测试都将从已修改但尚未提交的文件和文件夹中运行。

#### --picked=first

首先运行修改后的测试文件中的测试，然后运行所有未修改的测试

```
>pytest --picked=first
================================================= test session starts =================================================
platform win32 -- Python 3.6.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
rootdir: D:\demo\code\xuexi_pytest
collected 11 items

pytest_demo\test_new.py ..                                                                                       [ 18%]
pytest_demo\test_new_2.py ..                                                                                     [ 36%]
pytest_demo\test_b.py ......                                                                                     [ 90%]
pytest_demo\test_c.py .                                                                                          [100%]

================================================= 11 passed in 0.10s ==================================================
```

#### --mode=PICKED_MODE

```
--mode` 有2个参数可选 unstaged, branch, 默认是`--mode=unstaged
```

git 文件的2个状态

- untrack 没加到git里面的新文件
- unstaged staged：暂存状态, unstage就是未暂存状态，也就是没git add 过的文件

先弄清楚什么是 untrack 状态，当我们 pycharm 打开 git 项目，新增一个文件的时候，会弹出询问框：是否加到 git 文件

![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200917102146880-2132711754.png)

如果选择是，文件会变绿色，也就是 unstage 状态（没git add 过）；选择否，那就是一个新文件，未被加到当前分支的 git 目录里面，文件颜色是棕色。
`git status` 查看当前分支的状态,此时会看到 pytest_demo/test_3.py 是 Untracked files

```
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

>git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

        new file:   pytest_demo/test_new.py
        new file:   pytest_demo/test_new_2.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   pytest_demo/test_new.py
        modified:   pytest_demo/test_new_2.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        .idea/
        pytest_demo/__pycache__/
        pytest_demo/test_3.py
```

运行 `pytest --picked` 会默认执行所有的 Untracked 文件和 not staged 文件，默认是`--mode=unstaged`。

```
>pytest --picked

Changed test files... 3. ['pytest_demo/test_new.py', 'pytest_demo/test_new_2.py', 'pytest_demo/test_3.py']
Changed test folders... 2. ['.idea/', 'pytest_demo/__pycache__/']
================================================= test session starts =================================================
platform win32 -- Python 3.6.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
collected 5 items

pytest_demo\test_new.py ..                                                                                       [ 40%]
pytest_demo\test_new_2.py ..                                                                                     [ 80%]
pytest_demo\test_3.py .                                                                                          [100%]

================================================== 5 passed in 0.06s ==================================================
```

如果我们只需运行当前分支上已经被暂存，但尚未提交的文件（不包含 Untracked files），使用 git diff 查看分支代码的差异

```
>git diff --name-only master
pytest_demo/test_new.py
pytest_demo/test_new_2.py
```

运行 `pytest --picked --mode=branch`, 运行分支上已经被暂存但尚未提交的代码

```
>pytest --picked --mode=branch

Changed test files... 2. ['pytest_demo/test_new.py', 'pytest_demo/test_new_2.py']
Changed test folders... 0. []
================================================= test session starts =================================================
platform win32 -- Python 3.6.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
collected 4 items

pytest_demo\test_new.py ..                                                                                       [ 50%]
pytest_demo\test_new_2.py ..                                                                                     [100%]

================================================== 4 passed in 0.04s ==================================================
```

# [pytest文档60-pytest.main()的使用](https://www.cnblogs.com/yoyoketang/p/14032069.html)

#### 前言

pytest 运行用例的时候，一般用命令行去执行，有些小伙伴不太习惯命令行运行用例，可能是之前深受 unittest 框架的影响，习惯在项目的根目录下写一个 run_all.py 的文件。
运行的时候，使用 python 运行 run_all.py 来执行测试用例。

#### pytest.main()

先看看 pytest.main() 的源码, main 函数的内容

- args 传一个list对象，list 里面是多个命令行的参数
- plugins 传一个list对象，list 里面是初始化的时候需注册的插件

```
def main(args=None, plugins=None):
    """ return exit code, after performing an in-process test run.

    :arg args: list of command line arguments.

    :arg plugins: list of plugin objects to be auto-registered during
                  initialization.
    """
    from _pytest.main import EXIT_USAGEERROR

    try:
        try:
            config = _prepareconfig(args, plugins)
        except ConftestImportFailure as e:
            exc_info = ExceptionInfo(e.excinfo)
            tw = py.io.TerminalWriter(sys.stderr)
            tw.line(
                "ImportError while loading conftest '{e.path}'.".format(e=e), red=True
            )
            exc_info.traceback = exc_info.traceback.filter(filter_traceback)
            exc_repr = (
                exc_info.getrepr(style="short", chain=False)
                if exc_info.traceback
                else exc_info.exconly()
            )
            formatted_tb = safe_str(exc_repr)
            for line in formatted_tb.splitlines():
                tw.line(line.rstrip(), red=True)
            return 4
        else:
            try:
                return config.hook.pytest_cmdline_main(config=config)
            finally:
                config._ensure_unconfigure()
    except UsageError as e:
        tw = py.io.TerminalWriter(sys.stderr)
        for msg in e.args:
            tw.line("ERROR: {}\n".format(msg), red=True)
        return EXIT_USAGEERROR
```

如果不带任何参数，那么执行的效果跟我们在 cmd 直接运行 pytest 命令一样，默认运行的是当前目录及子目录的所有文件夹的测试用例

```
> pytest
```

#### run_all.py

在项目的根目录，新建一个 run_all.py 的文件

![img](https://img2020.cnblogs.com/blog/1070438/202011/1070438-20201124183913171-1054037515.png)

只需写简单的2行代码

```
import pytest

# 默认运行的是当前目录及子目录的所有文件夹的测试用例
pytest.main()
```

这样就能在 pycharm 里面右键运行，不带参数默认运行当前目录及子目录的所有文件夹的测试用例

#### 带参数运行

在运行的时候，也可以指定参数运行

-s： 显示程序中的 print/logging 输出
-v: 丰富信息模式, 输出更详细的用例执行信息
-k： 运行包含某个字符串的测试用例。如：pytest -k add XX.py 表示运行 XX.py 中包含 add 的测试用例。
-q: 简单输出模式, 不输出环境信息
-x: 出现一条测试用例失败就退出测试。在调试阶段非常有用，当测试用例失败时，应该先调试通过，而不是继续执行测试用例。

在命令行运行带上 -s 参数

```
> pytest -s
```

那么在 pytest.main() 里面等价于

```
import pytest

# 带上-s参数
pytest.main(["-s"])
```

在命令行运行带上多个参数时

```
> pytest -s -x
```

那么在 pytest.main() 里面等价于

```
import pytest

# 带上-s -x参数
pytest.main(["-s", "-x"])
```

#### 指定运行某个用例

指定运行 cases/module1 文件夹下的全部用例, 在命令行运行时, 先 cd 到项目的根目录

```
>pytest cases/module1
```

那么在 pytest.main() 里面等价于

```
import pytest

# 运行指定文件夹目录
pytest.main(["cases/module1"])
```

运行指定的 cases/module1/test_x1.py 下的全部用例,在命令行运行时, 先cd到项目的根目录

```
>pytest cases/module1/test_x1.py
```

那么在 pytest.main() 里面等价于

```
import pytest

# 运行指定py文件
pytest.main(["cases/module1/test_x1.py"])
```

运行指定的 cases/module1/test_x1.py 下的某一个用例 test_x, 在命令行运行时, 先cd到项目的根目录

```
>pytest cases/module1/test_x1.py::test_x
```

那么在 pytest.main() 里面等价于

```
import pytest

# 运行指定py文件下的test_x
pytest.main(["cases/module1/test_x1.py::test_x"])
```

通过上面跟命令行运行的对比，对 pytest.main() 的使用也就基本掌握了

#### plugins参数的使用

一般我们写插件的代码放到 conftest.py 会被pytest查找到，如果不是写到 conftest.py 的插件内容，可以通过 plugins 参数指定加载

```
# run_all.py 
import pytest


# 在run_all.py下自定义插件
class MyPlugin(object):
    def pytest_sessionstart(self):
        print("*** test run start blog地址 https://www.cnblogs.com/yoyoketang/")


# plugins指定加载插件

pytest.main(["cases/module1"], plugins=[MyPlugin()])
```

运行后会看到在参数用例开始之前答应上面的内容

```
*** test run start blog地址 https://www.cnblogs.com/yoyoketang/
============================= test session starts =============================
platform win32 -- Python 3.6.6, pytest-4.5.0, py-1.9.0, pluggy-0.13.1
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
rootdir: D:\wangyiyun\web
plugins: repeat-0.8.0, rerunfailures-9.1, xdist-2.1.0
collected 5 items

cases\module1\test_x1.py .                                               [ 20%]
cases\module1\test_x2.py ....                                            [100%]

========================== 5 passed in 0.05 seconds ===========================
```

plugins参数的作用就是指定需加载的插件，也可以指定多个。

# [pytest文档61-fixture之name参数使用别名](https://www.cnblogs.com/yoyoketang/p/14040668.html)

#### 前言

本篇讲 fixture 里面的 name 参数如何使用，使用别名后代码更容易理解。

#### fixture使用案例

定义一个fixture打开浏览器，测试用例需用到这个fixture的前置操作

```python
from selenium import webdriver
import pytest
import time
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


@pytest.fixture(scope="module")
def open_broswer():
    '''打开浏览器'''
    driver = webdriver.Chrome()
    yield driver
    driver.close()


def test_blog(open_broswer):
    '''打开我的blog: https://www.cnblogs.com/yoyoketang/'''
    open_broswer.get("https://www.cnblogs.com/yoyoketang/")
    time.sleep(3)
```

open_broswer 这个fixture 返回打开浏览器的实例 driver,后面的测试用例传 open_broswer 参数，此时 open_broswer 就相当于我们之前写代码的 driver 了。
小伙伴们习惯了 driver.get() 这种代码，突然看到 open_broswer.get() 这样的代码会不太适应，不知道后面该如何写了。

于是我给open_broswer 重命名为name, 让代码看起来更容易理解一点

```
def test_blog(open_broswer):
    '''打开我的blog: https://www.cnblogs.com/yoyoketang/'''
    driver = open_broswer   # 这个地方是重命名，不是调用函数
    driver.get("https://www.cnblogs.com/yoyoketang/")
    time.sleep(3)
```

这样写的话又有一个误区，有的同学会认为这里是调用函数了。。。（注意调用函数的时候后面是有括号的，这里没括号，只是重命名换个名称而已）

#### fixture里面的name参数

为了实现上面的效果，又不引起误解，可以在 fixture 里面使用 name 参数，给 fixture 使用别名

```
from selenium import webdriver
import pytest
import time
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


@pytest.fixture(scope="module", name="driver")
def open_broswer():
    '''打开浏览器'''
    driver = webdriver.Chrome()
    yield driver
    driver.close()


def test_blog(driver):
    '''打开我的blog: https://www.cnblogs.com/yoyoketang/'''
    driver.get("https://www.cnblogs.com/yoyoketang/")
    time.sleep(3)
```

这样就可以使用 driver 继续操作了。

# [pytest文档62-内置fixture之request](https://www.cnblogs.com/yoyoketang/p/14041751.html)

#### 前言

request 是 pytest 的内置 fixture ， "为请求对象提供对请求测试上下文的访问权，并且在fixture被间接参数化的情况下具有可选的“param”属性。"
这是官方文档对request的描述，可参考的文档不多。

#### FixtureRequest

FixtureRequest 是来自 fixture 或者 测试用例的请求，它有访问测试上下文的权限, FixtureRequest[源代码](https://docs.pytest.org/en/latest/_modules/_pytest/fixtures.html#FixtureRequest)。

```
class FixtureRequest[源代码](https://docs.pytest.org/en/latest/_modules/_pytest/fixtures.html#FixtureRequest)

请求对象提供对请求的测试上下文的访问，并且具有可选的 param 属性，以防设备被间接参数化。

fixturename
正在为其执行此请求的 fixture 名称。

scope
作用域字符串，“function”、“class”、“module”、“session”之一。

fixturenames
此请求中所有活动状态的 fixture 的名称。

node
基础集合节点（取决于当前请求范围）。

config
与此请求关联的 pytest 配置对象。

function
如果请求具有每个函数范围，则测试函数对象。

cls
类（可以是None），其中收集了测试函数。

instance
在其上收集测试函数的实例（可以是None）。

module
收集测试函数的Python模块对象。

fspath
收集此测试的测试模块的文件系统路径。

keywords
基础节点的关键字/标记词典。

session
Pytest会话对象。

addfinalizer(finalizer: Callable[], object]) → None[源代码]
添加finalizer/teardown函数，以便在请求的测试上下文中的最后一个测试完成执行后调用。

applymarker(marker) → None[源代码]
对单个测试函数调用应用标记。

如果不希望在所有函数调用上都有关键字/标记，则此方法非常有用。

参数
marker -- A _pytest.mark.MarkDecorator 调用创建的对象 pytest.mark.NAME(...) .

raiseerror(msg: Optional[str]) → NoReturn[源代码]
使用给定的消息引发FixtureLookupError。

getfixturevalue(argname: str) → Any[源代码]
动态运行命名的fixture函数。

如果可能，建议通过函数参数声明fixtures。但是，如果您只能在测试设置时决定是否使用另一个fixture，那么您可以使用此函数在fixture或测试函数体中检索它。

引发
pytest.FixtureLookupError -- 如果找不到给定的固定装置。
```

#### request.param

前面讲fixture参数化的时候，有接触到 "request.param" 用于获取测试的请求参数，以下示例

```python
'''
request 是 pytest的内置fixture
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/
'''
import pytest

# 测试数据
test_data = ["user1", "user2"]


@pytest.fixture(params=test_data)
def register_users(request):
     # 获取当前的测试数据
     user = request.param
     print("\n拿着这个账号去注册：%s"%user)
     result = "success"
     return user, result


def test_register(register_users):
    user, result = register_users
    print("在测试用例里面里面获取到当前测试数据：%s"%user)
    print(result)
    assert result == "success"
```

此案例里面我们可以在fixture参数化的时候，通过request.param获取到测试的请求参数，但是在用例里面用 request.param 却不能获取到测试的请求参数

```
def test_register_x(register_users, request):
    print(request.param)
```

这样运行，会抛异常：'FixtureRequest' object has no attribute 'param'

```
拿着这个账号去注册：user1
F
register_users = ('user1', 'success')
request = <FixtureRequest for <Function test_register_x[user1]>>

    def test_register_x(register_users, request):
>       print(request.param)
E       AttributeError: 'FixtureRequest' object has no attribute 'param'

D:\test_x7.py:27: AttributeError
```

#### request.config

request.config 是获取测试的配置文件参数，这个在前面讲命令行参数的时候有用到过.

在 conftest.py 写一个 hook函数， pytest_addoption 的作用是用于获取命令行参数，request.config 用于读取测试的配置数据

```
# content of conftest.py
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )

@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")
```

于是在测试用例里面可以通过 request.config 来获取到配置参数，也可以通过自己定义的 cmdopt 来获取。

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

def test_answer_1(request):
    type = request.config.getoption("--cmdopt")
    print("获取到命令行参数：%s" % type)


def test_answer_2(cmdopt):
    print("获取到命令行参数：%s" % cmdopt)
```

#### request.module

fixture 函数可以通过接受 request 对象来反向获取请求中的测试函数、类或模块上下文，进一步扩展之前的 smtp fixture示例，让我们从fixture的测试模块读取可选的服务器URL
这是官方文档的一个示例

```
# conftest.py
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


@pytest.fixture(scope="module")
def smtp(request):
    server = getattr(request.module, "smtpserver", "smtp.qq.com")
    print("fixture 获取到的server :%s" %server)
    smtp = smtplib.SMTP(server, 587, timeout=5)
    yield smtp
    print("完成 %s (%s)" % (smtp, server))
    smtp.close()
```

我们使用request.module属性来从测试模块中选择性地获取smtpserver属性
快速创建另一个测试模块，在其模块名称空间中实际设置服务器URL，新建一个test_anothersmtp.py文件，输入以下代码：

```
# test_anothersmtp.py
smtpserver = "mail.python.org"

def test_showhelo(smtp):

    print("case showhelo")
```

这时候运行用例，会获取到 test_anothersmtp.py 里面定义的 smtpserver

```
============================= test session starts =============================
platform win32 -- Python 3.6.6, pytest-4.5.0, py-1.9.0, pluggy-0.13.1
Test order randomisation NOT enabled. Enable with --random-order or --random-order-bucket=<bucket_type>
rootdir: D:\
rerunfailures-9.1, xdist-2.1.0
collected 1 item

..\..\..\..\module2\test_anothersmtp.py 
fixture 获取到的server :mail.python.org
case showhelo
.完成 <smtplib.SMTP object at 0x000001D00754CB00> (mail.python.org)


========================== 1 passed in 0.64 seconds ===========================
```

用例里面没定义 smtpserver 的话，会用默认属性 "smtp.qq.com"

#### request的相关成员对象

在conftest.py 写一个fixture 可以获取到request的一些成员对象相关信息

```
# conftest.py
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

@pytest.fixture(autouse=True)
def print_request(request):
    print("\n=======================request start=================================")
    print(request.module)
    print(request.function)
    print(request.cls)
    print(request.fspath)
    print(request.fixturenames)
    print(request.fixturename)
    print(request.scope)
    print("\n=======================request end=================================")
```

使用命令行"pytest -s text_x.py"运行用例,会看到打印的结果

```
test_1.py
=======================request start=================================
<module 'web.cases.module2.test_1' from 'D:\\web\\cases\\module2\\test_1.py'>
<function test_answer_1 at 0x0000012D1C9FD9D8>
None
D:\web\cases\module2\test_1.py
['_verify_url', 'base_url', '__pytest_repeat_step_number', 'show_request', 'request']
show_request
function

=======================request end=================================
获取到命令行参数：type1
.
=======================request start=================================
<module 'web.cases.module2.test_1' from 'D:\\web\\cases\\module2\\test_1.py'>
<function test_answer_2 at 0x0000012D1C9FD730>
None
D:\web\cases\module2\test_1.py
['_verify_url', 'base_url', '__pytest_repeat_step_number', 'show_request', 'cmdopt', 'request']
show_request
function

=======================request end=================================
```

在打印测试用例的详细日志的时候，还是很有用的。

# [pytest文档63-内置fixture之pytestconfig](https://www.cnblogs.com/yoyoketang/p/14042224.html)

#### 前言

前面讲 request 是pytest的一个内置 fixture ，作用是获取测试的上下文，可以通过request.config 获取配置对象。
pytestconfig 的作用跟 request.config 是一样的，都是获取配置对象

#### pytestconfig 源码分析

pytestconfig 是一个内置fixture，用于获取配置对象 [pytestconfig 源码](https://docs.pytest.org/en/latest/_modules/_pytest/fixtures.html#pytestconfig)
pytestconfig 有2个常用的方法

- .getoption() 获取命令行参数
- .getini() 获取ini配置文件的参数

```
@fixture(scope="session")
def pytestconfig(request: FixtureRequest) -> Config:
    """Session-scoped fixture that returns the :class:`_pytest.config.Config` object.

    Example::

        def test_foo(pytestconfig):
            if pytestconfig.getoption("verbose") > 0:
                ...

    """
    return request.config
```

从上面的源码看出，实际返回的就是 request.config

使用示例

```
def test_foo(pytestconfig):
    if pytestconfig.getoption("verbose") > 0:
        ...
```

#### getoption() 获取命令行参数

获取命令行参数的案例，在前面讲过很多次了，这个也是用的最广泛的

```
# content of conftest.py
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )

@pytest.fixture
def cmdopt(pytestconfig):
    return pytestconfig.getoption("--cmdopt")
```

测试用例

```
# test_cmdopt.py
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

def test_answer_1(pytestconfig):
    type = pytestconfig.getoption("--cmdopt")
    print("获取到命令行参数：%s" % type)


def test_answer_2(cmdopt):
    print("获取到命令行参数：%s" % cmdopt)
```

命令行运行用例的时候，可以用 --cmdopt 参数

```
>pytest -s test_cmdopt.py --cmdopt type2
================== test session starts =======
platform win32 -- Python 3.6.6, pytest-4.5.0, py-1.9.0, pluggy-0.13.1
rootdir: D:\wangyiyun\web\cases\module2
rerunfailures-9.1, xdist-2.1.0
collected 2 items

test_cmdopt.py 获取到命令行参数：type2
.获取到命令行参数：type2
.

================== 2 passed in 0.06 seconds ==========
```

#### getini() 从 pytest.ini 配置文件获取参数

在项目的根目录一般会放一个 pytest.ini 写一些配置参数

```
[pytest]

log_cli = 1

addopts = -v -x
```

我们想读取 pytest.ini 里面的配置信息，可以用 pytestconfig.getini() 来获取，使用示例

```
# conftest.py
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


@pytest.fixture(autouse=True)
def get_ini(pytestconfig):
    '''读取ini配置信息'''
    # 读取 log_cli配置
    log_cli = pytestconfig.getini('log_cli')
    print("获取到markers ：%s" % log_cli)
    addopts = pytestconfig.getini('addopts')
    print("获取到addopts的配置：%s " % addopts)
```

在命令行运行后，可以看到打印的内容

```
test_cmdopt.py::test_answer_1 获取到markers ：True
获取到db的配置：['-v', '-x']
获取到命令行参数：type1
PASSED
```

addopts 参数可以更改默认命令行选项，这个当我们在 cmd 输入一堆指令去执行用例的时候，就可以用该参数代替了，省去重复性的敲命令工作
比如上面的配置， 命令行输入pytest运行的时候，会默认带上的参数，如 ‘pytest -v -x’
log_cli 是控制台实时输出日志，可以设置True 和 False，也可以设置1 和 0

#### log_cli

log_cli 是控制台实时输出日志，可以设置True 和 False，也可以设置1 和 0，默认是关闭状态（False）

当 log_cli = 0 或默认的 False 状态时，命令行输入 pytest 运行用例，在控制台输出是按每个模块显示运行结果

```
collected 6 items

test_1.py ..                                                                    [ 33%]
test_anothersmtp.py .                                                           [ 50%]
test_cmdopt.py ..                                                               [ 83%]
test_y.py .                                                                     [100%]

============================== 6 passed in 1.80 seconds ==============================
```

当log_cli = 1后 运行 pytest 命令

```
collected 6 items

test_1.py::test_answer_1 PASSED                                                 [ 16%]
test_1.py::test_answer_2 PASSED                                                 [ 33%]
test_anothersmtp.py::test_showhelo PASSED                                       [ 50%]
test_cmdopt.py::test_answer_1 PASSED                                            [ 66%]
test_cmdopt.py::test_answer_2 PASSED                                            [ 83%]
test_y.py::test_i PASSED                                                        [100%]

============================== 6 passed in 0.84 seconds ==============================
```

这时候报告会按每条用例显示结果

# [pytest文档64-内置 pytestconfig 动态添加和获取 pytest.ini 配置参数](https://www.cnblogs.com/yoyoketang/p/14047492.html)

#### 前言

前面讲 pytestconfig 的时候，可以获取到 pytest.ini 里面的配置参数。
我们在写项目自动化用例的时候，有一些配置参数希望能加到配置里面，如configid, productid,以及测试环境的base_url地址，和账号相关信息。

#### addini的源码阅读

addini有四个参数：name, help, type=None, default=None

```
    def addini(self, name, help, type=None, default=None):
        """ register an ini-file option.

        :name: name of the ini-variable
        :type: type of the variable, can be ``pathlist``, ``args``, ``linelist``
               or ``bool``.
        :default: default value if no ini-file option exists but is queried.

        The value of ini-variables can be retrieved via a call to
        :py:func:`config.getini(name) <_pytest.config.Config.getini>`.
        """
        assert type in (None, "pathlist", "args", "linelist", "bool")
        self._inidict[name] = (help, type, default)
        self._ininames.append(name)
```

#### 动态添加配置信息

前面一篇讲添加命令行参数，可以用 addoption 来添加命令行参数，这里我们是添加 pytest.ini 的配置信息
adddini里面参数说明

- 第一个'url' 是参数的名称
- type 是类型，默认None，可以设置：None, "pathlist", "args", "linelist", "bool"
- default 是设置的默认值
- help 是设置帮助文档，方便查阅

```
# conftest.py
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )
    # 添加参数到pytest.ini
    parser.addini('url', type=None, default="http://49.235.92.12:8200/", help='添加 url 访问地址参数')


# 获取 pytest.ini 配置参数
@pytest.fixture(scope="session")
def home_url(pytestconfig):
    url = pytestconfig.getini('url')
    print("\n读取到配置文件的url地址：%s" % url)
    return url
```

参数用例传 home_url

```
# test_y.py

def test_h(home_url):
    print("用例：%s" % home_url)
```

运行结果

```
============================= test session starts =============================
platform win32 -- Python 3.6.6, pytest-4.5.0, py-1.9.0, pluggy-0.13.1
rootdir: D:\wangyiyun\web
collected 1 item

..\..\..\..\..\wangyiyun\web\test_y.py 
读取到配置文件的url地址：http://49.235.92.12:8200/
用例：http://49.235.92.12:8200/
.

========================== 1 passed in 0.02 seconds ===========================
```

#### pytest.ini 配置 url地址

如果有一天我们的测试环境发生了改变，这时候不需要去改代码，只需在 pytest.ini 配置一个环境地址

```
[pytest]


url = https://www.cnblogs.com/yoyoketang/
```

重新运行，我们得到的结果是

```
============================= test session starts =============================
platform win32 -- Python 3.6.6, pytest-4.5.0, py-1.9.0, pluggy-0.13.1
rootdir: D:\wangyiyun\web
collected 1 item

..\..\..\..\..\wangyiyun\test_y.py 
读取到配置文件的url地址：https://www.cnblogs.com/yoyoketang/
用例：https://www.cnblogs.com/yoyoketang/
.

========================== 1 passed in 0.02 seconds ===========================
```

#### type参数的几种类型

默认None，可以设置：None, "pathlist", "args", "linelist", "bool"

- type=None 默认读的是字符串
- type="pathlist" 可以设置多个路径，会自动拼接ini文件这一层目录
- type="args" 多个参数
- type="linelist" 可以是多个命令行参数
- type="bool" bool值，设置1或0

# [pytest文档65-内置 request 读取项目的根目录 rootdir](https://www.cnblogs.com/yoyoketang/p/14070270.html)

#### 前言

写自动化测试项目的时候，经常要用到配置文件，比如读取数据库相关的配置，希望单独放到 config 配置文件，方便维护。
pytest 的内置 fixture 可以获取到配置相关的信息，request.config.rootdir 用于获取项目的跟目录。

#### config 配置文件

再项目下新建一个 config 文件，相关配置信息用 yaml 文件维护数据

![img](https://img2020.cnblogs.com/blog/1070438/202012/1070438-20201201191224069-805886204.png)

在conftest.py 下写读取配置文件的 fixture, 这里我设置为 autouse=True 主要是为了查看打印读取到的目录

```
import pytest
import os
import yaml
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


@pytest.fixture(scope="session", autouse=True)
def dbinfo(request):
    dbfile = os.path.join(request.config.rootdir,
                        "config",
                        "dbenv.yml")
    print("dbinfo file path :%s" % dbfile)
    with open(dbfile) as f:
        dbenv_config = yaml.load(f.read(), Loader=yaml.SafeLoader)
    print(dbenv_config)
    return dbenv_config
```

#### rootdir 读取

打开 cmd 命令行，在项目的跟目录运行用例

> pytest -s

```
D:\wangyiyun\webauto>pytest -s
================================================= test session starts =================================================
platform win32 -- Python 3.6.6, pytest-4.5.0, py-1.9.0, pluggy-0.13.1
rootdir: D:\wangyiyun\webauto
plugins: allure-pytest-2.8.6
collected 5 items

case\test_1.py dbinfo file path :D:\wangyiyun\webauto\config\dbenv.yml
{'host': '47.104.x.x', 'port': 3306, 'user': 'root', 'passwd': 123456, 'db': 'test'}
test xxx
.
case\test_x1.py test 111111
.test 22222222
.test 3333333
.test 444444444
.

=================
```

这时候可以看到读取到的配置文件地址：D:\wangyiyun\webauto\config\dbenv.yml

在项目根目录运行用例是标准的运行姿势，但是有些小伙伴会 cd 到 case 目录，运行单个用例

```
D:\wangyiyun\webauto>cd case

D:\wangyiyun\webauto\case>pytest test_1.py
================================================= test session starts =================================================
platform win32 -- Python 3.6.6, pytest-4.5.0, py-1.9.0, pluggy-0.13.1
rootdir: D:\wangyiyun\webauto\case
plugins: allure-pytest-2.8.6
collected 1 item

test_1.py E                                                                                                      [100%]

======================================================= ERRORS ========================================================
______________________________________________ ERROR at setup of test_x _______________________________________________

request = <SubRequest 'dbinfo' for <Function test_x>>

    @pytest.fixture(scope="session", autouse=True)
    def dbinfo(request):
        dbfile = os.path.join(request.config.rootdir,
                            "config",
                            "dbenv.yml")
        print("dbinfo file path :%s" % dbfile)
>       with open(dbfile) as f:
E       FileNotFoundError: [Errno 2] No such file or directory: 'D:\\wangyiyun\\webauto\\case\\config\\dbenv.yml'

..\conftest.py:14: FileNotFoundError
------------------------------------------------ Captured stdout setup ------------------------------------------------
dbinfo file path :D:\wangyiyun\webauto\case\config\dbenv.yml
=============================================== 1 error in 0.08 seconds ===============================================
```

这个时候就会出现报错：No such file or directory: 'D:\wangyiyun\webauto\case\config\dbenv.yml'
因为此时的项目跟目录就变成了 rootdir: D:\wangyiyun\webauto\case
接下来我们需要解决的问题时，不管在哪个目录运行，它的项目跟目录应该都是我们的工程目录 D:\wangyiyun\webauto

#### pytest.ini

pytest 运行用例的时候项目的 rootdir 当没有 pytest.ini 配置文件的时候会根据 conftest.py 找到它的跟目录。
由于前面没有用到pytest.ini 配置文件，导致不同目录运行用例的 rootdir 不一样。

当项目下存在 pytest.ini 配置文件的时候，会认为 pytest.ini 所在的目录是 rootdir 目录， 所以我们一般会把 pytest.ini 配置文件放到项目的跟目录。
如果里面没有内容，放个空的也行

![img](https://img2020.cnblogs.com/blog/1070438/202012/1070438-20201201192614094-307475596.png)

这时候不管在哪个目录运行用例都不会有问题了

```
D:\wangyiyun\webauto\case>pytest test_1.py
======================== test session starts ==============
platform win32 -- Python 3.6.6, pytest-4.5.0, py-1.9.0, pluggy-0.13.1
rootdir: D:\wangyiyun\webauto, inifile: pytest.ini
plugins: allure-pytest-2.8.6
collected 1 item

test_1.py .                                            [100%]

========================1 passed in 0.03 seconds =============
```

pytest的配置文件除了 pytest.ini，还有 tox.ini 和 setup.cfg 也可以当配置文件

# [pytest文档66-工厂化的 fixtures](https://www.cnblogs.com/yoyoketang/p/14073043.html)

#### 前言

在一个测试用例中需要多次调用同一个fixture的时候，工厂化的 fixture 的模式对于一个 fixture 在单一的测试中需要被多次调用非常有用。
之前写fixture是直接return一个数据，在测试用例中可以直接使用，现在我们需要返回一个生成数据的函数，这样就能在用例中多次调用了。

#### Factories as ﬁxtures

“Factories as ﬁxtures”模式可以帮助在一次测试中多次需要一个fixture的结果的情况下。
fixture不是直接返回数据，而是返回一个生成数据的函数。然后可以在测试中多次调用此函数。

使用示例

```
import pytest


@pytest.fixture 
def make_customer_record(): 
    def _make_customer_record(name): 
        return {"name": name, "orders": []}
    return _make_customer_record

def test_customer_records(make_customer_record): 
    customer_1 = make_customer_record("Lisa") 
    customer_2 = make_customer_record("Mike") 
    customer_3 = make_customer_record("Meredith")
```

如果工厂创建的数据需要管理，那么fixture可以处理：

```
import pytest


@pytest.fixture
def make_customer_record():
    
    created_records = []
    
    def _make_customer_record(name):
        record = models.Customer(name=name, orders=[])
        created_records.append(record) 
        return record
    
    yield _make_customer_record
    
    for record in created_records:
        record.destroy()
        
def test_customer_records(make_customer_record): 
    customer_1 = make_customer_record("Lisa") 
    customer_2 = make_customer_record("Mike") 
    customer_3 = make_customer_record("Meredith")
```

#### 场景案例

有个场景案例：当用户第一次注册的时候，可以注册成功，第二次注册的时候，提示用户已被注册了

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


@pytest.fixture()
def register():

    def _register(user):
        # 调用注册接口，返回结果
        print("注册用户：%s" % user)
        result = {"code": 0,
                  "message": "success"}
        return result

    return _register



def test_case_1(register):
    '''测试重复注册接口案例'''
    # 第一次调用注册
    result1 = register("yoyo")
    assert result1["message"] == "success"

    # 第二次调用
    result2 = register("yoyo")
    # 真实场景可以断言 已被注册了
```

这种场景把注册写到fixture的话，在测试用例里面就需要调用两次

# [pytest文档67-pytest.mark.parametrize 中使用 fixture](https://www.cnblogs.com/yoyoketang/p/14096639.html)

#### 前言

测试用例参数化的时候，使用 pytest.mark.parametrize 参数化传测试数据，如果我们想引用前面不同fixture返回的数据当测试用例的入参。
可以用fixture 参数化 prams 来间接解决这个问题

#### 使用案例

我们需要在测试用例里面参数化，参数化的数据来源于前面不同fixture的返回值，示例

```
import pytest


@pytest.fixture
def a():
    return 'a'


@pytest.fixture
def b():
    return 'b'


@pytest.mark.parametrize('arg', [a, b])
def test_foo(arg):
    assert len(arg) == 1
```

这时候运行会报错

```
..\test_xx.py F
arg = <function a at 0x000001C7E77CE7B8>

    @pytest.mark.parametrize('arg', [a, b])
    def test_foo(arg):
>       assert len(arg) == 1
E       TypeError: object of type 'function' has no len()

\test_xx.py:16: TypeError
F
arg = <function b at 0x000001C7E77CE8C8>

    @pytest.mark.parametrize('arg', [a, b])
    def test_foo(arg):
>       assert len(arg) == 1
E       TypeError: object of type 'function' has no len()

\test_xx.py:16: TypeError
```

关于此问题的讨论可以看github 上的issue [Using fixtures in pytest.mark.parametrize #349](https://github.com/pytest-dev/pytest/issues/349)

#### 使用 fixture 参数化

可以使用 fixture 的参数化来解决上面的问题，通过 request.getfixturevalue(“fixture name”) 方法来获取fixture的返回值
有些文档看到的是 request.getfuncargvalue 那是早期的版本，目前新版本改名换成了 request.getfixturevalue
getfixturevalue 的作用是获取 fixture 的返回值

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

@pytest.fixture
def a():
    return 'a'


@pytest.fixture
def b():
    return 'b'


@pytest.fixture(params=['a', 'b'])
def arg(request):
    return request.getfixturevalue(request.param)


def test_foo(arg):
    assert len(arg) == 1
```

这样运行就不会有问题了

#### 实例场景

web自动化的时候，想在 chrome 和 firefox 浏览器上测试同一功能的测试用例

```
import pytest
from selenium import webdriver

# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

@pytest.fixture
def chrome():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def firefox():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


@pytest.fixture(params=['chrome', 'firefox'])
def driver(request):
    '''启动浏览器参数化'''
    return request.getfixturevalue(request.param)


def test_foo(driver):
    '''测试用例'''
    driver.get("https://www.cnblogs.com/yoyoketang/")
```

这样就可以分别打开 chrome 和 fixfox 执行测试用例了
关于此问题的更多讨论可以看github 上的issue [Using fixtures in pytest.mark.parametrize #349](https://github.com/pytest-dev/pytest/issues/349)
还有另外一个解决方案，使用 pytest-lazy-fixture 插件解决 https://www.cnblogs.com/yoyoketang/p/14096749.html

# [pytest文档68-pytest-lazy-fixture 插件解决 pytest.mark.parametrize 中使用 fixture 问题](https://www.cnblogs.com/yoyoketang/p/14096749.html)

#### 前言

测试用例参数化的时候，使用 pytest.mark.parametrize 参数化传测试数据，如果我们想引用前面 不同fixture 返回的数据当测试用例的入参，前面一篇用fixture 参数化 prams 来间接解决这个问题。
接下来用 pytest-lazy-fixture 插件可以直接在测试用例中参数化时 pytest.mark.parametrize 中使用 fixture

#### pytest-lazy-fixture 插件

pytest-lazy-fixture 插件是为了解决测试用例中用 @pytest.mark.parametrize 参数化调用fixture的问题，先pip安装

> pip install pytest-lazy-fixture

目前使用的版本是 0.6.3

```
>pip show pytest-lazy-fixture
Name: pytest-lazy-fixture
Version: 0.6.3
Summary: It helps to use fixtures in pytest.mark.parametrize
Home-page: https://github.com/tvorog/pytest-lazy-fixture
Author: Marsel Zaripov
Author-email: marszaripov@gmail.com
License: MIT
Location: e:\python36\lib\site-packages
Requires: pytest
Required-by:
```

#### parametrize 使用示例

参数化的时候，其中一些测试数据，来源于前面的 fixture

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


@pytest.fixture(params=[1, 2])
def one(request):
    return request.param


@pytest.mark.parametrize('arg1,arg2', [
    ('val1', pytest.lazy_fixture('one')),
])
def test_func(arg1, arg2):
    print(arg1, arg2)
    assert arg2 in [1, 2]
```

运行结果

```
..\test_y.py val1 1
.val1 2
.

============== 2 passed in 0.04 seconds ===========
```

#### fixture 参数化 params

在 fixture 参数化的 params 中也可以使用

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

@pytest.fixture
def one():
    return 1


@pytest.fixture
def two():
    return 2


@pytest.fixture(params=[
    pytest.lazy_fixture('one'),
    pytest.lazy_fixture('two')
])
def some(request):
    return request.param


def test_func(some):
    assert some in [1, 2]
```

pytest-lazy-fixture 相关的使用可以查看github 地址https://github.com/TvoroG/pytest-lazy-fixture

# [pytest文档69-Hook函数之参数化生成测试用例pytest_generate_tests](https://www.cnblogs.com/yoyoketang/p/14106959.html)

#### 前言

pytest 实现参数化有三种方式

- pytest.fixture() 使用 fixture 传 params 参数实现参数化
- @ pytest.mark.parametrize 允许在测试函数或类中定义多组参数，在用例中实现参数化
- pytest_generate_tests 允许定义自定义参数化方案或扩展。

#### pytest_generate_tests

pytest_generate_tests 在测试用例参数化收集前调用此钩子函数，根据测试配置或定义测试函数的类或模块中指定的参数值生成测试用例，
可以使用此钩子实现自定义参数化方案或扩展,相关文档参考官方文档https://docs.pytest.org/en/latest/parametrize.html#pytest-generate-tests

有时您可能想要实现自己的参数化方案或实现某种动态性来确定 fixture 的参数或范围。为此，可以使用pytest_generate_tests在收集测试函数时调用的钩子。通过传入的 metafunc 对象，您可以检查请求的测试上下文，最重要的是，您可以调用 metafunc.parametrize() 引起参数化。

例如，假设我们要运行一个测试，并接受要通过新的 pytest 命令行选项设置的字符串输入。让我们首先编写一个接受 stringinput 函数参数的简单测试：

```
# content of test_strings.py


def test_valid_string(stringinput):
    assert stringinput.isalpha()
```

现在，我们添加一个conftest.py文件，其中包含命令行选项和测试函数的参数化：

```
# content of conftest.py


def pytest_addoption(parser):
    parser.addoption(
        "--stringinput",
        action="append",
        default=[],
        help="list of stringinputs to pass to test functions",
    )


def pytest_generate_tests(metafunc):
    if "stringinput" in metafunc.fixturenames:
        metafunc.parametrize("stringinput", metafunc.config.getoption("stringinput"))
```

如果现在传递两个stringinput值，则测试将运行两次：

```
$ pytest -q --stringinput="hello" --stringinput="world" test_strings.py
..                                                                   [100%]
2 passed in 0.12s
```

我们还使用一个stringinput运行，这将导致测试失败：

```
$ pytest -q --stringinput="!" test_strings.py
F                                                                    [100%]
================================= FAILURES =================================
___________________________ test_valid_string[!] ___________________________

stringinput = '!'

    def test_valid_string(stringinput):
>       assert stringinput.isalpha()
E       AssertionError: assert False
E        +  where False = <built-in method isalpha of str object at 0xdeadbeef>()
E        +    where <built-in method isalpha of str object at 0xdeadbeef> = '!'.isalpha

test_strings.py:4: AssertionError
========================= short test summary info ==========================
FAILED test_strings.py::test_valid_string[!] - AssertionError: assert False
1 failed in 0.12s
```

不出所料，我们的测试功能失败。

如果您未指定字符串输入，则将跳过它，因为 metafunc.parametrize()将使用空参数列表来调用它：

```
$ pytest -q -rs test_strings.py
s                                                                    [100%]
========================= short test summary info ==========================
SKIPPED [1] test_strings.py: got empty parameter set ['stringinput'], function test_valid_string at $REGENDOC_TMPDIR/test_strings.py:2
1 skipped in 0.12s
```

请注意，当metafunc.parametrize使用不同的参数集多次调用时，这些集合中的所有参数名称都不能重复，否则会引发错误。
更多的参数化案例参考https://docs.pytest.org/en/latest/example/parametrize.html#paramexamples

#### 使用示例

在 conftest.py 自定义参数化的钩子, 判断当测试用例传了 param 参数，就让它生成参数化的用例

```
def pytest_generate_tests(metafunc):
    """ generate (multiple) parametrized calls to a test function."""
    if "param" in metafunc.fixturenames:
        metafunc.parametrize("param",
                             metafunc.module.test_data,
                             ids=metafunc.module.names,
                             scope="function")
```

test_parm.py相关的测试数据和用例内容，names是用例的名称，test_data是测试数据

```
import requests

# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

# 用例的id名称
names = ["login nam1", "login name2"]
# 测试数据 list of dict
test_data = [{
                "url": "http://49.235.x.x:5000/api/v1/login/",
                "method": "POST",
                "headers":
                    {
                        "Content-Type": "application/json"
                    },
                "json":
                    {
                        "username": "test",
                        "password": "123456"
                    }

        },
        {
            "url": "http://49.235.x.x:5000/api/v1/login/",
            "method": "POST",
            "headers":
                {
                    "Content-Type": "application/json"
                },
            "json":
                {
                    "username": "test",
                    "password": "123456"
                }

        }
        ]


def test_login(param):
    r = requests.session().request(**param)
    print(r.text)
```

这样运行会，自动生成2条测试用例

```
================= test session starts ===============
platform win32 -- Python 3.6.6, pytest-4.5.0, py-1.9.0, pluggy-0.13.1
rootdir: D:\
collected 2 items

..\test_param.py 
{"code": 0, "msg": "login success!", "username": "test", "token": "81ae10099feaca6f0af5ba122444bea2a83a2dc9"}
.{"code": 0, "msg": "login success!", "username": "test", "token": "1ccfb99fd68f22da66c95660702af22d64108067"}
.

=============== 2 passed in 0.62 seconds ===============
```

上面是把测试数据和代码放一起，想实现代码和数据分离的话，上面的 names 和 test_data 测试数据写到 yaml 文件，写个函数去读取 yaml 文件的数据。

# [pytest文档70-Hook钩子函数完整API总结](https://www.cnblogs.com/yoyoketang/p/14108144.html)

### 前言

pytest 的钩子函数有很多，通过钩子函数的学习可以了解到pytest在执行用例的每个阶段做什么事情，也方便后续对pytest二次开发学习。
详细文档可以查看pytest官方文档https://docs.pytest.org/en/latest/reference.html#hooks

### 钩子函数总结

#### 第一部分：setuptools

引导挂钩要求足够早注册的插件（内部和setuptools插件），可以使用的钩子

- pytest_load_initial_conftests(early_config,parser,args): 在命令行选项解析之前实现初始conftest文件的加载。
- pytest_cmdline_preparse(config,args): (不建议使用)在选项解析之前修改命令行参数。
- pytest_cmdline_parse(pluginmanager,args): 返回一个初始化的配置对象,解析指定的args。
- pytest_cmdline_main(config): 要求执行主命令行动作。默认实现将调用configure hooks和runtest_mainloop。

#### 第二部分： 初始化挂钩

初始化钩子需要插件和conftest.py文件

- pytest_addoption(parser): 注册argparse样式的选项和ini样式的配置值，这些值在测试运行开始时被调用一次。
- pytest_addhooks(pluginmanager): 在插件注册时调用，以允许通过调用来添加新的挂钩
- pytest_configure(config): 许插件和conftest文件执行初始配置。
- pytest_unconfigure(config): 在退出测试过程之前调用。
- pytest_sessionstart(session): 在Session创建对象之后，执行收集并进入运行测试循环之前调用。
- pytest_sessionfinish(session,exitstatus): 在整个测试运行完成后调用，就在将退出状态返回系统之前。
- pytest_plugin_registered(plugin,manager):一个新的pytest插件已注册。

#### 第三部分： collection 收集钩子

- pytest_collection(session): 执行给定会话的收集协议。
- pytest_collect_directory(path, parent): 在遍历目录以获取集合文件之前调用。
- pytest_collect_file(path, parent) 为给定的路径创建一个收集器，如果不相关，则创建“无”。
- pytest_pycollect_makemodule(path: py._path.local.LocalPath, parent) 返回给定路径的模块收集器或无。
- pytest_pycollect_makeitem(collector: PyCollector, name: str, obj: object) 返回模块中Python对象的自定义项目/收集器，或者返回None。在第一个非无结果处停止
- pytest_generate_tests(metafunc: Metafunc) 生成（多个）对测试函数的参数化调用。
- pytest_make_parametrize_id(config: Config, val: object, argname: str) 返回val 将由@ pytest.mark.parametrize调用使用的给定用户友好的字符串表示形式，如果挂钩不知道，则返回None val。
- pytest_collection_modifyitems(session: Session, config: Config, items: List[Item]) 在执行收集后调用。可能会就地过滤或重新排序项目。
- pytest_collection_finish(session: Session) 在执行并修改收集后调用。

#### 第四部分：测试运行（runtest）钩子

- pytest_runtestloop(session: Session) 执行主运行测试循环（收集完成后）。
- pytest_runtest_protocol(item: Item, nextitem: Optional[Item]) 对单个测试项目执行运行测试协议。
- pytest_runtest_logstart(nodeid: str, location: Tuple[str, Optional[int], str]) 在运行单个项目的运行测试协议开始时调用。
- pytest_runtest_logfinish(nodeid: str, location: Tuple[str, Optional[int], str])在为单个项目运行测试协议结束时调用。
- pytest_runtest_setup(item: Item) 调用以执行测试项目的设置阶段。
- pytest_runtest_call(item: Item) 调用以运行测试项目的测试（调用阶段）。
- pytest_runtest_teardown(item: Item, nextitem: Optional[Item]) 调用以执行测试项目的拆卸阶段。
- pytest_runtest_makereport(item: Item, call: CallInfo[None]) 被称为为_pytest.reports.TestReport测试项目的每个设置，调用和拆卸运行测试阶段创建一个。
- pytest_pyfunc_call(pyfuncitem: Function) 调用基础测试功能。

#### 第五部分：Reporting 报告钩子

- pytest_collectstart(collector: Collector) 收集器开始收集。
- pytest_make_collect_report(collector: Collector) 执行collector.collect()并返回一个CollectReport。
- pytest_itemcollected(item: Item) 我们刚刚收集了一个测试项目。
- pytest_collectreport(report: CollectReport) 收集器完成收集。
- pytest_deselected(items: Sequence[Item]) 要求取消选择的测试项目，例如按关键字。
- pytest_report_header(config: Config, startdir: py._path.local.LocalPath) 返回要显示为标题信息的字符串或字符串列表，以进行终端报告。
- pytest_report_collectionfinish(config: Config, startdir: py._path.local.LocalPath, items: Sequence[Item]) 返回成功完成收集后将显示的字符串或字符串列表。
- pytest_report_teststatus(report: Union[CollectReport, TestReport], config: Config) 返回结果类别，简写形式和详细词以进行状态报告。
- pytest_terminal_summary(terminalreporter: TerminalReporter, exitstatus: ExitCode, config: Config) 在终端摘要报告中添加一个部分。
- pytest_fixture_setup(fixturedef: FixtureDef[Any], request: SubRequest) 执行夹具设置执行。
- pytest_fixture_post_finalizer(fixturedef: FixtureDef[Any], request: SubRequest) 在夹具拆除之后但在清除缓存之前调用，因此夹具结果fixturedef.cached_result仍然可用（不是 None）
- pytest_warning_captured(warning_message: warnings.WarningMessage, when: Literal[‘config’, ‘collect’, ‘runtest’], item: Optional[Item], location: Optional[Tuple[str, int, str]]) （已弃用）处理内部pytest警告插件捕获的警告。
- pytest_warning_recorded(warning_message: warnings.WarningMessage, when: Literal[‘config’, ‘collect’, ‘runtest’], nodeid: str, location: Optional[Tuple[str, int, str]]) 处理内部pytest警告插件捕获的警告。
- pytest_runtest_logreport(report: TestReport) 处理项目的_pytest.reports.TestReport每个设置，调用和拆卸运行测试阶段产生的结果。
- pytest_assertrepr_compare(config: Config, op: str, left: object, right: object) 返回失败断言表达式中的比较的说明。
- pytest_assertion_pass(item: Item, lineno: int, orig: str, expl: str) （实验性的）在断言通过时调用。

#### 第六部分：调试/相互作用钩

很少有可以用于特殊报告或与异常交互的挂钩：

- pytest_internalerror(excrepr: ExceptionRepr, excinfo: ExceptionInfo[BaseException]) 要求内部错误。返回True以禁止对将INTERNALERROR消息直接打印到sys.stderr的回退处理。
- pytest_keyboard_interrupt(excinfo: ExceptionInfo[Union[KeyboardInterrupt, Exit]]) 要求键盘中断。
- pytest_exception_interact(node: Union[Item, Collector], call: CallInfo[Any], report: Union[CollectReport, TestReport]) 在引发可能可以交互处理的异常时调用。
- pytest_enter_pdb(config: Config, pdb: pdb.Pdb) 调用了pdb.set_trace（）。

# [pytest文档71-pytest+yaml实现接口自动化框架](https://www.cnblogs.com/yoyoketang/p/14116839.html)

#### 前言

httprunner 用 yaml 文件实现接口自动化框架很好用，最近在看 pytest 框架，于是参考 httprunner的用例格式，写了一个差不多的 pytest 版的简易框架

#### 项目结构设计

项目结构完全符合 pytest 的项目结构，pytest 是查找 test_.*py 文件，我这里是查找 test_*.yml 文件，唯一不同的就是这个地方
以前写test_*.py 的测试用例，现在完全不用写了，全部写yaml 文件就行，项目结构参考

![img](https://img2020.cnblogs.com/blog/1070438/202012/1070438-20201210190659540-386445912.png)

只需在 conftest.py 即可实现，代码量超级少

```
import pytest
import requests
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


def pytest_collect_file(parent, path):
    # 获取文件.yml 文件,匹配规则
    if path.ext == ".yml" and path.basename.startswith("test"):
        # print(path)
        # print(parent)
        return YamlFile(path, parent)



class YamlFile(pytest.File):
    # 读取文件内容
    def collect(self):
        import yaml
        raw = yaml.safe_load(self.fspath.open(encoding='utf-8'))
        for yaml_case in raw:
            name = yaml_case["test"]["name"]
            values = yaml_case["test"]
            yield YamlTest(name, self, values)


class YamlTest(pytest.Item):
    def __init__(self, name, parent, values):
        super(YamlTest, self).__init__(name, parent)
        self.name = name
        self.values = values
        self.request = self.values.get("request")
        self.validate = self.values.get("validate")
        self.s = requests.session()

    def runtest(self):
        # 运行用例
        request_data = self.values["request"]
        # print(request_data)
        response = self.s.request(**request_data)
        print("\n", response.text)
        # 断言
        self.assert_response(response, self.validate)

    def assert_response(self, response, validate):
        '''设置断言'''
        import jsonpath
        for i in validate:
            if "eq" in i.keys():
                yaml_result = i.get("eq")[0]
                actual_result = jsonpath.jsonpath(response.json(), yaml_result)
                expect_result = i.get("eq")[1]
                print("实际结果：%s" % actual_result)
                print("期望结果：%s" % expect_result)
                assert actual_result[0] == expect_result
```

断言这部分，目前只写了判断相等，仅供参考，支持jsonpath来提取json数据

#### yaml格式的用例

在项目的任意目录，只要是符合test_开头的yml文件，我们就认为是测试用例
test_login.yml的内容如下

```
- test:
    name: login case1
    request:
        url: http://49.235.x.x:7000/api/v1/login/
        method: POST
        headers:
            Content-Type: application/json
            User-Agent: python-requests/2.18.4
        json:
            username: test
            password: 123456
    validate:
        - eq: [$.msg, login success!]
        - eq: [$.code, 0]


- test:
    name: login case2
    request:
        url: 49.235.x.x:7000/api/v1/login/
        method: POST
        headers:
            Content-Type: application/json
            User-Agent: python-requests/2.18.4
        json:
            username: test
            password: 123456
    validate:
        - eq: [$.msg, login success!]
        - eq: [$.code, 0]
```

#### 运行用例

运行用例，完全符合pytest的只需用例风格，支持allure报告

> pytest -v

```
D:\soft\api_pytest_1208>pytest -v
====================== test session starts ======================
platform win32 -- Python 3.6.6, pytest-4.5.0, py-1.9.0,
cachedir: .pytest_cache
rootdir: D:\soft\api_pytest_1208
plugins: allure-pytest-2.8.6
collected 4 items

data/test_login.yml::login case1 PASSED                    [ 25%]
data/test_login.yml::login case2 PASSED                    [ 50%]
data/test_login1.yml::login case1 PASSED                   [ 75%]
data/test_login1.yml::login case2 PASSED                   [100%]

=================== 4 passed in 1.34 seconds ====================
```

allure报告

> pytest --alluredir ./report

目前是把 yaml 文件下每个 test 当一个用例执行，后续还可以加上提取参数，参数关联更高级的功能！

# [pytest文档72- 使用 template 替换 yaml 文件的变量](https://www.cnblogs.com/yoyoketang/p/14119435.html)

#### 前言

在接口自动化测试的时候，yaml 文件一般放测试的数据或当配置文件使用，yaml 文件存放静态的数据是没问题的，python的数据类型基本上都是支持的。
有时候我们想在 yaml 文件中引用变量来读取 python 代码的设置值。

#### template 使用

template 是字符串模板，用于替换字符串中的变量，是 string 的一个类引用变量有 2 种格式

- $variable 使用 $变量名 引用变量
- ${variable} 使用 ${变量名} 大括号包起来

第一种 $variable

```
from string import Template
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


tempTemplate = Template("My name is $name , i like $fancy")
d = {'name': 'yoyo', 'fancy': 'python'}
print(tempTemplate.substitute(d))

# 运行结果
# >>> My name is yoyo , i like python
```

第二种 ${variable}

```
from string import Template
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


tempTemplate = Template("My name is ${name} , i like ${fancy}")
d = {'name': 'yoyo', 'fancy': 'python'}
print(tempTemplate.substitute(d))

# 运行结果
# >>>My name is yoyo , i like python
```

#### safe_substitute使用

上面的方式只能严格的匹配变量，当字符串中有$符号，不想匹配变量的时候，会报错

```
from string import Template
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/


tempTemplate = Template("$My name is ${name} , i like ${fancy}")
d = {'name': 'yoyo', 'fancy': 'python'}
print(tempTemplate.substitute(d))
```

这段，$符号加在My的前面，我只想让它是一个普通的字符串，不想引用变量，就出现了报错说找不到这个key

```
Traceback (most recent call last):
  File "D:/soft/api_pytest_1208/config/aa.py", line 12, in <module>
    print(tempTemplate.substitute(d))
  File "E:\python36\lib\string.py", line 130, in substitute
    return self.pattern.sub(convert, self.template)
  File "E:\python36\lib\string.py", line 123, in convert
    return str(mapping[named])
KeyError: 'My'
```

Template 里面还有一个 safe_substitute 的方法，可以忽略匹配不到的变量

```
from string import Template


tempTemplate = Template("$My name is ${name} , i like ${fancy}")
d = {'name': 'yoyo'}
print(tempTemplate.safe_substitute(d))

# 运行结果：$My name is yoyo , i like ${fancy}
```

虽然字符串定义了多个变量，但是引用的时候只给了name这个值，也不影响运行，没给值的当普通字符串出来，这样就很完美了

#### yaml 文件引用变量

通过前面 Template 的基础使用，已经掌握了基本的用法了，接下来在 yaml 文件中引用变量

```
- test:
    name: login case1
    request:
        url: http://49.235.x.x:7000/api/v1/login/
        method: POST
        headers:
            Content-Type: application/json
            User-Agent: python-requests/2.18.4
        json:
            username: $user
            password: $psw
    validate:
        - eq: [$.msg, login success!]
        - eq: [$.code, 0]
```

python读yaml文件代码

```
from string import Template
import yaml
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

with open("login.yml", encoding='utf-8') as fp:
    read_yml_str = fp.read()
    # print(xx)

    tempTemplate1 = Template(read_yml_str)
    c = tempTemplate1.safe_substitute({"user": "yoyo", "psw": "123456 "})
    print(c)

# yml 文件数据，转 python 类型
yaml_data = yaml.safe_load(c)
print(yaml_data)
```

运行结果

```
- test:
    name: login case1
    request:
        url: http://49.235.x.x:7000/api/v1/login/
        method: POST
        headers:
            Content-Type: application/json
            User-Agent: python-requests/2.18.4
        json:
            username: user
            password: 123456 
    validate:
        - eq: [$.msg, login success!]
        - eq: [$.code, 0]

[{
	'test': {
		'name': 'login case1',
		'request': {
			'url': 'http://49.235.x.x:7000/api/v1/login/',
			'method': 'POST',
			'headers': {
				'Content-Type': 'application/json',
				'User-Agent': 'python-requests/2.18.4'
			},
			'json': {
				'username': 'user',
				'password': 123456
			}
		},
		'validate': [{
			'eq': ['$.msg', 'login success!']
		}, {
			'eq': ['$.code', 0]
		}]
	}
}]
```

这样 yaml 文件就能引用到 python 的变量了

# [pytest文档73-pytest+yaml实现接口自动化框架之用例参数关联](https://www.cnblogs.com/yoyoketang/p/14154379.html)

#### 前言

使用 yaml 文件写测试用例的时候，如何在 yaml 文件的测试用例里面实现参数关联? 这是很多做自动化测试的小伙伴经常思考的一个问题。
接着前面的pytest+yaml 文件实现接口自动化框架，本篇使用环境变量的方式，让测试用例参数关联。
实现场景：上个接口返回的接口提取变量，在写个接口中引用变量

#### 场景案例

我现在有一个登陆接口A,登陆成功后返回一个token值。有一个获取用户信息的接口B，但是接口B必须要先登录后传登录的token才能访问
A接口登录接口文档基本信息

- 访问地址：http://127.0.0.1:8000/api/v1/login/
- 请求类型：POST
- 请求头部：application/json
- 请求参数：{"username":"test", "password":"123456"}

B接口获取绑定卡号的接口文档基本信息

- 访问地址：http://127.0.0.1:8000/api/v1/userinfo/
- 请求类型：GET
- 请求头部：Content-Type: application/json
- 请求头部token参数： Authorization: Token xxxxx login token xxxxx

先不带token去访问接口B，使用命令行工具httpie测试接口

```
C:\Users\dell>http http://127.0.0.1:8000/api/v1/user/info/
HTTP/1.1 401 Unauthorized
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 58
Content-Type: application/json
Date: Sat, 21 Sep 2019 14:06:15 GMT
Server: WSGIServer/0.2 CPython/3.6.0
Vary: Accept
WWW-Authenticate: Token
X-Frame-Options: SAMEORIGIN

{
    "detail": "Authentication credentials were not provided."
}
```

不带token会提示没权限访问：401 Unauthorized

#### 接口测试

先使用接口测试工具测试下，用postman,或者fiddler都可以，我这里为了查看报文信息方便，用httpie命令行工具

先访问接口A获取token值`234af73571da46ade79ea6a74961b1d23d609b79`

```
D:\>http http://127.0.0.1:8000/api/v1/login/ username=test password=123456 -v
POST /api/v1/login/ HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 42
Content-Type: application/json
Host: 127.0.0.1:8000
User-Agent: HTTPie/1.0.3

{
    "password": "123456",
    "username": "test"
}

HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 109
Content-Type: application/json
Date: Sat, 21 Sep 2019 15:37:06 GMT
Server: WSGIServer/0.2 CPython/3.6.0
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "code": 0,
    "msg": "login success!",
    "token": "234af73571da46ade79ea6a74961b1d23d609b79",
    "username": "test"
}
```

传给下个接口B

```
D:\>http http://127.0.0.1:8000/api/v1/user/info/ Authorization:"Token b7e02c959fbae4c2a0d9094f6f9b9a35fa8aaa1e" -v
GET /api/v1/user/info/ HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Authorization: Token b7e02c959fbae4c2a0d9094f6f9b9a35fa8aaa1e
Connection: keep-alive
Host: 127.0.0.1:8000
User-Agent: HTTPie/1.0.3



HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 96
Content-Type: application/json
Date: Sat, 21 Sep 2019 16:04:25 GMT
Server: WSGIServer/0.2 CPython/3.6.0
Vary: Accept
X-Frame-Options: SAMEORIGIN

{
	"msg": "sucess!",
	"code": 0,
	"data": [{
		"id": 15,
		"name": "test",
		"sex": "F",
		"age": 20,
		"mail": "1122@qq.com",
		"create_time": "2020-12-18"
	}]
}
```

传头部参数用xx:xxxx格式，中间用冒号:，如：`User-Agent:demo-agent/1.0 'Cookie:a=b;b=c'`,由于Authorization参数中间有空格，用双引号包起来

#### conftest.py 代码实现

在 conftest.py 使用环境变量保存测试的结果提取的变量，使用 template 替换 yaml 文件的变量

```
import pytest
import requests
import jsonpath
import json
import yaml
from string import Template
import os
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

def pytest_collect_file(parent, path):
    # 获取文件.yml 文件,匹配规则
    if path.ext == ".yml" and path.basename.startswith("test"):
        print(path)
        print(parent)
        return YamlFile(path, parent)


class YamlFile(pytest.File):
    '''收集测试用例'''
    def collect(self):
        yml_raw = self.fspath.open(encoding='utf-8').read()
        yml_var = Template(yml_raw).safe_substitute(os.environ)
        yaml_data = yaml.safe_load(yml_var)
        for yaml_case in yaml_data:
            name = yaml_case.get("test").get("name")
            values = yaml_case.get("test")
            yield YamlTest(name, self, values)


class YamlTest(pytest.Item):
    def __init__(self, name, parent, values):
        super(YamlTest, self).__init__(name, parent)
        self.name = name
        self.values = values
        self.s = requests.session()

    def values_render_variable(self, values):
        # values 是Test用例部分
        yaml_test = Template(json.dumps(values)).safe_substitute(os.environ)
        values = yaml.safe_load(yaml_test)
        return values

    def runtest(self):
        # 运行用例
        values = self.values_render_variable(self.values)
        request_data = values.get("request")
        print("\n请求数据: ", request_data)
        print(request_data)
        response = self.s.request(**request_data)
        print("接口返回", response.text)
        # 判断是否有extract提取参数
        if values.get("extract"):
            for key, value in values.get("extract").items():
                os.environ[key] = jsonpath.jsonpath(response.json(), value)[0]
        self.assert_response(response, values.get("validate"))

    def assert_response(self, response, validate):
        '''设置断言'''
        if validate:
            for i in validate:
                if "eq" in i.keys():
                    yaml_result = i.get("eq")[0]
                    actual_result = jsonpath.jsonpath(response.json(), yaml_result)
                    expect_result = i.get("eq")[1]
                    print("实际结果：%s" % actual_result[0])
                    print("期望结果：%s" % expect_result)
                    assert actual_result[0] == expect_result
```

#### YAML 文件案例

使用 extract 关键字提取变量，提取变量方式执行jsonpath表达式， 引用变量使用template 模板的引用语法$变量名

```
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

- test:
    name: login case1
    request:
        url: http://49.235.X.X:7000/api/v1/login/
        method: POST
        headers:
            Content-Type: application/json
            User-Agent: python-requests/2.18.4
        json:
            username: test
            password: 123456
    extract:
        token: $.token
    validate:
        - eq: [$.msg, login success!]
        - eq: [$.code, 0]

- test:
    name: get user info case1
    request:
        url: http://49.235.X.X:7000/api/v1/userinfo/
        method: GET
        headers:
            Content-Type: application/json
            User-Agent: python-requests/2.18.4
            Authorization: Token $token
    validate:
        - eq: [$.code, 0]
        - eq: ["$.data[0].name", test]
        - eq: ["$.data[0].mail", 1122@qq.com]
```

#### 执行结果

执行方式使用命令行运行，支持pytest的命令行指令

> pytest

运行结果

```
>pytest -s
============================= test session starts ==============================
platform win32 -- Python 3.6.6, pytest-4.5.0, py-1.9.0, pluggy-0.13.1
rootdir: D:\soft\api_pytest_1208
collecting ... D:\soft\api_pytest_1208\data\test_info.yml
<Package D:\soft\api_pytest_1208\data>
collected 2 items

data\test_info.yml
请求数据:  {'url': 'http://49.235.X.X:7000/api/v1/login/', 'method': 'POST', 
'headers': {'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.18.4'}, 
'json': {'username': 'test', 'password': 123456}}
{'url': 'http://49.235.X.X:7000/api/v1/login/', 'method': 'POST', 
'headers': {'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.18.4'},
 'json': {'username': 'test', 'password': 123456}}
接口返回 {"code": 0, "msg": "login success!", "username": "test", "token": "09be4368534fa6320ed77a333e34c6661a36d40e"}
实际结果：login success!
期望结果：login success!
实际结果：0
期望结果：0
.
请求数据:  {'url': 'http://49.235.X.X:7000/api/v1/userinfo/', 'method': 'GET', 
'headers': {'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.18.4', 
'Authorization': 'Token 09be4368534fa6320ed77a333e34c6661a36d40e'}}
{'url': 'http://49.235.X.X:7000/api/v1/userinfo/', 'method': 'GET', 
'headers': {'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.18.4', 
'Authorization': 'Token 09be4368534fa6320ed77a333e34c6661a36d40e'}}
接口返回 {"msg":"sucess!","code":0,"data":[{"id":15,"name":"test","sex":"F","age":20,"mail":"1122@qq.com","create_time":"2020-12-18"}]}
实际结果：0
期望结果：0
实际结果：test
期望结果：test
实际结果：1122@qq.com
期望结果：1122@qq.com
.

=========================== 2 passed in 0.49 seconds ===========================
```

# [pytest文档74-参数化parametrize加marks标记（pytest.param）](https://www.cnblogs.com/yoyoketang/p/14231422.html)

#### 前言

pytest 使用 parametrize 参数化的时候，有多组测试数据，需要对其中的一些测试数据加标记跳过，可以用pytest.param实现。

#### pytest.param

先看下 pytest.param 源码,可以传三个参数

- param values ：按顺序传参数集值的变量args
- keyword marks : marks关键字参数，要应用于此参数集的单个标记或标记列表。
- keyword str id: id字符串关键字参数，测试用例的id属性

```
def param(*values, **kw):
    """Specify a parameter in `pytest.mark.parametrize`_ calls or
    :ref:`parametrized fixtures <fixture-parametrize-marks>`.

    .. code-block:: python

        @pytest.mark.parametrize("test_input,expected", [
            ("3+5", 8),
            pytest.param("6*9", 42, marks=pytest.mark.xfail),
        ])
        def test_eval(test_input, expected):
            assert eval(test_input) == expected

    :param values: variable args of the values of the parameter set, in order.
    :keyword marks: a single mark or a list of marks to be applied to this parameter set.
    :keyword str id: the id to attribute to this parameter set.
    """
    return ParameterSet.param(*values, **kw)
```

使用示例

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    pytest.param("6*9", 42, marks=pytest.mark.xfail),
])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

运行结果:1 passed, 1 xfailed in 0.08 seconds

#### skip跳过用例

上面的案例是标记xfail，想标记skip跳过用例也是可以的

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

@pytest.mark.parametrize("user,psw",
                         [("yoyo1", "123456"),
                          ("yoyo2", "123456"),
                          pytest.param("yoyo3", "123456", marks=pytest.mark.skip)])
def test_login(user, psw):
    print(user + " : " + psw)
    assert 1 == 1
```

运行结果：2 passed, 1 skipped in 0.03 seconds

上面的2个参数也可以用pytest.param格式

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

@pytest.mark.parametrize("user,psw",
                         [pytest.param("yoyo1", "123456"),
                          pytest.param("yoyo2", "123456"),
                          pytest.param("yoyo3", "123456", marks=pytest.mark.skip)])
def test_login1(user, psw):
    print(user + " : " + psw)
    assert 1 == 1
```

#### id参数

id参数是给用例添加标题内容，没加id参数的时候，用例会默认拿请求的参数当用例标题
![img](https://img2020.cnblogs.com/blog/1070438/202101/1070438-20210104182123912-666141575.png)

添加id参数

```
import pytest
# 作者-上海悠悠 QQ交流群:717225969
# blog地址 https://www.cnblogs.com/yoyoketang/

@pytest.mark.parametrize("user,psw",
                         [pytest.param("yoyo1", "123456", id="test case1: yoyo1"),
                          pytest.param("yoyo2", "123456", id="test case2: yoyo2"),
                          pytest.param("yoyo3", "123456", marks=pytest.mark.skip, id="test case3: yoyo3")])
def test_login1(user, psw):
    print(user + " : " + psw)
    assert 1 == 1
```

运行结果
![img](https://img2020.cnblogs.com/blog/1070438/202101/1070438-20210104182353559-2079834032.png)

