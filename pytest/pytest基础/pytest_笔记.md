🔺🔺🔺🔺🔺🔺强烈建议先看第四章，fixture的scope那一篇的结论



# 一、运行规则

[`pytest`—官方文档](https://www.osgeo.cn/pytest/reference.html#pytest-fail)

```bash
pytest会运行当前目录及子目录下所有以 test_*.py 和 *_test.py 命名的文件。文件匹配方式遵循 Standard test discovery rules
```

#### 1.1	简单测试

- **Terminal中输入pytest，会运行当前目录及子目录下所有以 `test_*.py` 和 `*_test.py` 命名的文件**

- **或者如下方式：会运行当前执行文件所在目录及其子目录下所有以 `test_*.py` 和 `*_test.py` 命名的文件**

	```python
	if __name__ == '__main__':
	    os.system('pytest')
	```

- **不使用pytest的方法的时候可以不用导入pytest模块，pytest插件会自动帮你检测用例**

```python
import os
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 6
    
if __name__ == '__main__':
    os.system('pytest')
```



#### 1.2	忽略异常，标记为通过

使用`raises`可以帮助我们断言某些代码会引发某个异常，新建一个`test_sysexit.py`文件，输入以下代码 

```python
import pytest
def f():
    raise SystemExit(1)

def test_mytest():
    with pytest.raises(SystemExit):	# 注册SystemExit异常,比如Synax错误也可以注册
        f()
```

这样在出现该异常的时候，这个测试用例也不会标记为失败，以`quiet`报告模式执行测试功能：

```bash
$ pytest -q test_sysexit.py
```

这个测试返回了一个成功报告，如下图所示：

```bash
D:\origin\学习代码\interface_auto\venv\Scripts\python.exe D:/origin/学习代码/interface_auto/src/api_case/接口脚本/test_sysexit.py
.                                                                        [100%]
1 passed in 0.12 seconds

Process finished with exit code 0
```





#### 1.3	将多个测试用例放到一起

当你需要开发多个测试用例的时候，你可能需要将他们放在同个`class`中，`pytest`可以很简单的创建包含多个测试用例的class： 

```python
import os

class TestClass(object):

    def test_one(self):
        x = 'this'
        assert 'h' in x

    def test_two(self):
        x = 'hello'
        assert hasattr(x, 'check')

    def fun_three(self):
        x = 'world'
        assert hasattr(x, 'index')

if __name__ == '__main__':
    os.system('pytest -q test_class.py')
```





#### 1.4	第一次（或n次）失败后停止整个测试任务

**在第一（n）次失败后停止测试过程：**

```
pytest -x           # stop after first failure
pytest --maxfail=2  # stop after two failures
```



#### 1.5	指定测试路径

**🔺在模块中运行测试**

```python
pytest test_mod.py
pytest demo.py		# 指定的路径不一定要以test开头，是因为他收集的是这个文件里面的测试用例
```

**🔺在目录中运行测试**

```python
pytest testing/
pytest ./			# 当前文件夹
pytest demo/		# 指定的路径不一定要以test开头，是因为他收集的是这个目录下的测试用例
```

**指定当前目录**

```python
pytest -q .	
```



#### 1.6	按关键词匹配后运行测试用例

```python
pytest -k 关键字						  # 只执行含有该关键字的目录、类或者函数（注意1.当类名和关键词不匹配的时候，他会去找类里面的函数。2.当类名和关键字成功匹配的时候，他会执行整个类里面的函数，哪怕有些函数不能匹配关键字 3.同理当文件匹配的时候，他执行整个文件中的用例，哪怕有些用例不匹配关键字）4.关键词过滤是在已收集到的用例池塘中进行过滤，所以类名、函数名、方法名必须符合用例的发现机制
```

**匹配规则：**

- **在`pytest`收集完用例以后，在`pytest`的用例收集池塘中进行匹配筛选符合要求的**
- **`pytest`用例池中的每个对象的格式是像这样：`（module.py::TestClass::method）`**,
- **匹配用例池中的每一个用例对象**

**总结：说白了就是在已收集的用例池中，对用例的路径进行正则匹配**



**语法：**

- **`-k	关键词 `:   匹配关键词用例**
- **`-k 关键词1 and 关键词2`： 匹配同时含有关键词1和关键词的2用例**
- **`-k 关键词1 and not 关键词2`: 匹配含有关键词1 并且不含有关键词2的用例**









#### 1.7	通过marks描述执行测试用例

**Run tests by marker expressions**

```
pytest -m slow
```

将运行所有用 `@pytest.mark.slow` 装饰符。

**备注：`-m slow`是在`pytest`收集完全部测试用例以后，再筛选出标记为`slow`的测试用两个。。这里主要是为了说，`pytest -m slow`这是一个筛选用例的过程，不是用例执行的过程。  我为什么这么说呢？情况如下解释：**

**解释：为什么`-m`是用例筛选的过程而不是用例执行的过程**

```ini
比如一个用例我们把它标记成  @pytest.mark.skip(reason='就是要跳过它')
当我们执行pytest -m skip的时候， 它会从items用例集中筛选出被标记为skip的用例。然后pytest执行。
然而这个时候，pytest发现这些用例被标记成了skip，所以全部跳过。
所以pytest -m slow这是一个筛选用例的过程， 最后要不要执行，还是得看pytest得逻辑
```







# 二、 `pytest`的三种启动方式



#### 2.1	`pytest.main()`启动方式

> - ​	**参数必须放到一个列表中**
> - ​    **同时满足示例`['-m', 'normal and minor']`**
> - ​    **排除示例['-m', 'normal and not minor']**
> - ​    **自动扩展功能（类的标签会自动扩展到其内部的每一个子用例上）**
> - ​    **未注册的标记也可以使用，但是会有警告（警告你该标记没有注册）**

**实例：**

```python
import pytest

@pytest.mark.slow
class TestClass(object):

    @pytest.mark.minor
    def test_one(self):
        x = 'this'
        print('test_one', x)
        assert 'h' in x

    @pytest.mark.normal
    def test_two(self):
        x = 'hello'
        print('test_two', x) 
        assert hasattr(x, 'check')

    @pytest.mark.normal
    def test_tmpdir(self):
        print('test_tmpdir', None)
        assert 0


class TestDemo(object):

    @pytest.mark.minor
    @pytest.mark.normal
    def test_add_welcome_message(self):
        x = 'add welcome message'
        print('test_add_welcome_message', x)
        assert hasattr(x, 'check')

    @pytest.mark.normal
    def test_delete_welcome_message(self):
        y = 'test_delete_welcome_message'
        print('test_delete_welcome_message', y)
        assert hasattr(y, 'index')
if __name__ == '__main__':
    # os.system('pytest -q --maxfail=1 test_class.py')
    # os.system('pytest -k class test_class.py')
    # os.system('pytest test_class.py::TestClass::fun_three')
    # os.system('pytest test_class.py -m slow')
    pytest.main(['-s', '-q', './test_class.py', '-m', 'minor and normal', '--collect-only'])
    pytest.main(['-s', '-q', './test_class.py', '-m', 'minor and not normal', '--collect-only'])
    
    
    pytest.main(['-s', '-q', './case_ysix.py', '-m', 'slow', '--collect-only'])
    
    x
    case_ysix.py::TestClass::test_one
    case_ysix.py::TestClass::test_two
    case_ysix.py::TestClass::test_tmpdir

    2 deselected in 0.01 seconds    

```

**注意：上面的例子，反复实验几次就能找到规律**

**规则：`TestClas`类上面的标记会自动扩展到其子用例上，哪怕你不写，他会自动带上该标签**





#### 2.2	`pytest.ini`方式

**在项目的根目录下，我们可以建立一个`pytest.ini`文件，在这个文件中可以实现相关的配置：**

**配置格式如下：**

```ini
[pytest]
addopts = -s -v
testpaths = ./scripts
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

**注意:**配置文件中不许有中文，`pytest.ini`文件必须位于项目的根目录，而且也必须叫做`pytest.ini`。

**配置参数参数**：

- `addopts`可以搭配相关的参数，比如`-s`。多个参数以空格分割，其他参数后续用到再说。

- `-s`，显示详细的print打印信息，没有-s 则print信息不会显示。

- `-v`，使输出结果更加详细。

- `testpaths`配置测试用例的目录，

`testpaths = ./scripts`这个`scripts`就是我们所有文件或者目录的顶层目录。

其内的子文件都要以`test`_开头，`pytest`才能识别到。

另外，上面这么写，是从一个总目录下寻找所有的符合条件的文件或者脚本，那么我们想要在这个总目录下执行其中某个具体的脚本文件怎么办？

```ini
[pytest]
testpaths = ./scripts/
python_files = test_case_01.py
```

这么写就是执行scripts目录下面的`test_case_01.py`这个文件。

python_classes则是说明脚本内的所有用例类名的规则

所有用例类名必须是以Test开头，也可以自定义为以Test_开头

python_functions则是说脚本内的所有用例函数的命名规则

所用测试用例方法必须以test_开头才能识别



#### 2.3	`Terminal`命令行

**在命令行中直接`pytest -s`的方式进行执行**





# 三、`pytest`的前置和后置执行

**前言：学过`unittest`的都知道里面用前置和后置`setup`和`teardown`非常好用，在每次用例开始前和结束后都去执行一次。**



#### 3.1	用例的运行级别

- 模块级（`setup_module/teardown_module`）开始于模块始末，全局的（不在类中）
- 函数级（`setup_function/teardown_function`）只对函数用例生效（不在类中）== `setup/teardown`(如果不放在类中。同类中`setup_method/teardown_method==setup/teardown`)

----------------------------------------------------------------------------------------------------------------------------------------------

- 类级（`setup_class/teardown_class`）只在类中前后运行一次(在类中)
- 方法级（`setup_method/teardown_method`）开始于方法始末（在类中）
- 类里面的（`setup/teardown`）运行在调用方法的前后 (在类种)

______________

- 全局所有用例`pytest_runtest_setup(item)`		# 这玩意通过`yield`来控制前后置(其实我这里有一个问题没解决，就是当标记成了skip，还是被执行了。。有待了解)(示例代码在后面的`pytest_runtest_setup(item)`)

-----------------------

- `@pytest.fixture`，通过`scope`和`autouse`来控制前后置，且根据`@pytest.fixture`不同的位置来控制不同范围的前后置
	- `conftest.py`文件中
	- `module.py`文件中
	- 🔺这个最灵活，前面的setup系列更精准易懂
	- 通过yield来传递参数或者数据给用例

除开pytest.fixture上面几种前后置，都是放在同一个文件中的，不存在什么跨文件。。比如





#### 3.2	下面是`setup`和`teardown`来实现前后置的案例

**`setup/teardown` == `setup_method/teardown_method`**

```python
class TestInter(object):

    def setup(self):	# 或者setup_method
        print('在类中每个用例执行之前')

    def teardown(self):	# 或者teardown_method
        print('在类中每个用例执行之后')

    def test_inter_sub_one(self):
        """
        这是一段多行注释
        """
        print('\033[1;45m test_inter_sub_one \033[0m')

    def test_inter_sub_two(self):
        print('\033[1;45m test_inter_sub_two \033[0m')
 
=============================输出===============================
在类中每个用例执行之前
 test_inter_sub_one 
.在类中每个用例执行之后
在类中每个用例执行之前
 test_inter_sub_two 
.在类中每个用例执行之后
```



**`setup_class/teardown_class`**

```python
class TestInter(object):

    def setup_class(self):
        print('在类开始之前')

    def teardown_class(self):
        print('在类结束之后')

    def test_inter_sub_one(self):
        """
        这是一段多行注释
        """
        print('\033[1;45m test_inter_sub_one \033[0m')

    def test_inter_sub_two(self):
        print('\033[1;45m test_inter_sub_two \033[0m')
=============================输出===============================
在类开始之前
 test_inter_sub_one 
. test_inter_sub_two 
.在类结束之后

```



**`setup_module/teardown_module`**

```python
def setup_module():
    print('module level setup')


def teardown_module():
    print('module level teardown')

# @pytest.mark.skip(reason='不知道')
class TestInter(object):

    def test_inter_sub_one(self):
        """
        这是一段多行注释
        """
        print('\033[1;45m test_inter_sub_one \033[0m')

    def test_inter_sub_two(self):
        print('\033[1;45m test_inter_sub_two \033[0m')
        
=============================输出===============================        
module level setup
 test_inter_sub_one 
. test_inter_sub_two 
.module level teardown
```



**`setup_function/teardown_function`**

```python
def setup_function():
    print('module level setup')


def teardown_function():
    print('module level teardown')

def test_inter_sub_one(name=1):	# 🔺 用例是可以穿参数的，但是必须是默认参数。。但是没有意义，不如直接写死在代码里面
    """
    这是一段多行注释
    """
    print(name)
    print('\033[1;45m test_inter_sub_one \033[0m')
=============================输出=============================== 
module level setup
1
 test_inter_sub_one 
.module level teardown

```









# 四、 `fixture`

### 4.1	`fixture`源码参数

调用fixture三种方法

- `1.函数或类里面方法直接传fixture的函数名称`
- `2.使用装饰器@pytest.mark.usefixtures()修饰`
- `3.autouse=True自动使用`

#### 用例传fixture参数

```python
fixture（scope='function'，params=None，autouse=False，ids=None，name=None）：
```

- **`scope`: `控制fixture的作用范围， scope有四个级别的参数`**
  - **`function(默认)`**	
  - **`class`：每个测试类和函数调用一次（这一点很重要）**
  - **`module`**
  - **`session`**
- **`params：一个可选的参数列表，它将导致多个参数调用fixture功能和所有测试使用它`。**
- **`autouse`:**
	- **默认`autouse=False`（谨慎使用autouse参数）**
	- **定义在conftest文件中，如果是session范围，且有参数化（比如2个参数），那么pytest会创建2个测试会话，全部执行用例执行2遍， 先执行参数1得会话，然后再执行一遍参数2得**
	- **定义在conftest文件中，如果是module范围，且有参数化（比如2个参数），那么pytest会给每个模块创建2个子模块，所有得模块执行2遍，在一个会话中，参数1得模块执行完一遍以后，紧接着执行参数2得**
	- **定义在conftest文件中，如果是class范围，且有参数化（比如2个参数），会给每一个类用例和测试函数用例都创建一个子类或者子测试函数**
	- **定义在conftest文件中，如果是function范围，且有参数化（比如2个参数），会给每一个类的方法用例和测试函数用例都创建一个子类或者子测试函数**
- **`ids`: ---- nodeid**
	- **为夹具参数整个别名，不然采用`pytest`的命名规则**
- **`name`**
	- **给夹具函数取别名**
	- **🔺使用了别名以后，在`@pytest.mark.usefixtures()`和入参调用夹具必须使用别名，不然报错**



🔺🔺🔺🔺🔺🔺🔺🔺🔺`request 是 pytest 的内置 fixture ， "为请求对象提供对请求测试上下文的访问权🔺`



**ids的例子**

```python
# conftest.py

@pytest.fixture(params=['zhangsan', 'lisi'], ids=['明珠的账号', '李毅的账号'])
def input_user(request):
    return request.param

@pytest.fixture(params=['123456', '654321'], ids=['明珠账号的密码', '李毅账号的密码'])
def input_pwd(request):
    return request.param
===========================================================================================================
# test_inter_two.py
def test_inter_two_sub_three(input_user, input_pwd):
    # print('\033[1;35m test_inter_two_sub_three \033[0m')
    print('\033[1;36m %s : %s \033[0m' % (input_user, input_pwd))


if __name__ == '__main__':
    # pytest.main(['-s', 'test_inter_two.py'])
    os.system('pytest -s -v test_inter_two.py')
====================================================输出=================================================
test_inter_two.py::test_inter_two_sub_three[明珠的账号-明珠账号的密码]  zhangsan : 123456 
PASSED
test_inter_two.py::test_inter_two_sub_three[明珠的账号-李毅账号的密码]  zhangsan : 654321 
PASSED
test_inter_two.py::test_inter_two_sub_three[李毅的账号-明珠账号的密码]  lisi : 123456 
PASSED
test_inter_two.py::test_inter_two_sub_three[李毅的账号-李毅账号的密码]  lisi : 654321 
PASSED
```





**通过一个例子理解scope和autouse的具体执行过程**



```python
# conftest.py

data = ['1', '2']


@pytest.fixture(scope='session', params=data, autouse=True)
def user(request):
    print('fixture .................user')
    result = 'fixtrue' + '[' + request.param + ']'
    return result
```



```python
# test_03.py

import pytest
import os


class TestYin(object):

    def test_yin_one(self, user):
        print('\033[1;32m test_yin_one \033[0m')
        print('\033[1;32m %s \033[0m' % user)

    def test_yin_two(self, user):
        print('\033[1;32m test_yin_two \033[0m')
        print('\033[1;32m %s \033[0m' % user)


def test_yin_three(user):
    print('\033[1;32m test_yin_three \033[0m')
    print('\033[1;32m %s \033[0m' % user)


if __name__ == '__main__':
    # pytest.main(['-s'])
    os.system('pytest -s -v ./test_03.py')
    # os.system('pytest -s -v')
```

**输出结果**

```
test_03.py::TestYin::test_yin_one[1] fixture .................user
 test_yin_one 
 fixtrue[1] 
PASSED
test_03.py::TestYin::test_yin_one[2] fixture .................user
 test_yin_one 
 fixtrue[2] 
PASSED
test_03.py::TestYin::test_yin_two[1] fixture .................user
 test_yin_two 
 fixtrue[1] 
PASSED
test_03.py::TestYin::test_yin_two[2] fixture .................user
 test_yin_two 
 fixtrue[2] 
PASSED
test_03.py::test_yin_three[1] fixture .................user
 test_yin_three 
 fixtrue[1] 
PASSED
test_03.py::test_yin_three[2] fixture .................user
 test_yin_three 
 fixtrue[2] 
PASSED

========================== 6 passed in 0.07 seconds ===========================
```



**🔺结论**

```bash
1. 不管你的scope范围是什么，只要你设置了autouse=True, 那么这个scope所笼罩的范围内所有用例都将自动隐式的使用user这个位置参数
2. user这个位置参数有两个作用
第一个作用： 用于执行对应名称夹具函数
第二个作用： 接收夹具函数返回的结果
3. 当我们设置成session的时候，整个session笼罩范围内所有的用例都会被隐式的带上user这个位置参数，然而只有整个会话中第一个被pytest执行的用例调用了该夹具函数。所有每一个会话中只有第一个被执行用例中user位置参数有两个作用（执行夹具函数，接收夹具函数的返回结果）， 🔺其他用例中的user只代表夹具函数的结果，不执行，但是能获取结果。
4. 当我们设置成module的时候，整个module笼罩范围内所有的用例都会被隐式的带上user这个位置参数，然而只有每一个module中第一个被pytest执行的用例调用了该夹具函数。所有每一个module中只有第一个被执行用例中user位置参数有两个作用（执行夹具函数，接收夹具函数的返回结果）， 🔺其他用例中的user只代表夹具函数的结果，不执行，但是能获取结果。
5. 当我们设置成class的时候，整个class笼罩范围内所有的用例都会被隐式的带上user这个位置参数，然而只有每一个class中第一个被pytest执行的用例调用了该夹具函数。所有每一个class中只有第一个被执行用例中user位置参数有两个作用（执行夹具函数，接收夹具函数的返回结果）， 🔺其他用例中的user只代表夹具函数的结果，不执行，但是能获取结果。🔺(这里的class代表类和测试函数)
6. 当我们设置成function的时候，整个function笼罩范围内所有的用例都会被隐式的带上user这个位置参数，而且每一个测试用例中的user位置参数都具有两个作用，这就是为什么pytest的fixture的scope参数默认值是function
7. 解释：为什么说成是笼罩范围？
因为：以session为例，如果我们的fixture存在于conftest.py文件中，fixture的scope为session，autouse等于True， 那么session笼罩范围是整个项目会话,如果fixture存在于对应的包中，session的笼罩范围就是整个包，如果fixture存在于一个py文件中，那么session的笼罩范围就是整个py文件

🔺纠错哈:autouse是隐士的带上了user，如果我们要使用它的返回结果必须显示的写到用例参数里面，不然报错，说user未定义


8. 换一种理解可能更好
autouse=True的时候所有用例都自动隐式的带上user这个位置参数，🔺scope的值来决定哪些用例调用夹具函数，哪些用例只是接收夹具函数结果，session表示整个会话中第一个被执行的用例将调用夹具函数，module表示模块中第一个执行的用例将调用夹具函数，class表示类中第一个调用的方法用例调用夹具函数，function表示所用用例都调用夹具函数


10. 当本地也有fixture conftest.py中也有，假如都是自动。他们会进行数据组合。比如本地有2组数据，conftest.py中有4组，那么多就会有8组数据

11. scope的作用是，定义了用例的划分生成规范。 怎么理解生成规范。比如定义了fixture有多种数据，他会根据scope的不同，按照不同的策略生成测试数据autouse=True
session：  有多少组数据，执行多少次fixture
module：   fixture执行次数 == .py文件数量 * 数据组数
class:     fixture执行次数 == (class测试类用例集合的个数 + 函数测试用例数量) * 数据组数
function:  fixture执行次数 == 用例数量 *  数据组数

当autouse !=True的时候
session：  有多少组数据，执行多少次fixture
module：   fixture执行次数 == 手动添加的fixture的.py文件数量 * 数据组数
class:     fixture执行次数 == (手动添加了fixture的class测试类用例集合的个数 + 手动添加了fixture函数测试用例数量) * 数据组数
function:  fixture执行次数 == 添加了fixture的用例数量 *  数据组数



12. 🔺先执行使用了fixture的用例，最后执行未使用的。。比如scope是class有3组数据，那么先将使用fixture用例提出来，通过数据组进行扩展，这里扩展3组，然会将没有使用fixture放到最后。类还是只有一个。我们可以通过setup_method来检验

13. 🔺 说白了这个scope其实是一个执行顺序的规范。不是用例的限制。如果设置成autouse=True以后，不管你是模块还是类还是什么鬼，全部用例都会隐式的带上。唯一不同的就是采用不同的scope，执行顺序会发现改变，fixture的执行时机和次数发生改变。


14.autouse=True 一个函数调不调用前后置，根据用例划分来看，我们以setup_module为例，如果是联系在一个模块中扩展的规律，那么setup_module就只执行一次。如果中间穿插了其他模块的，然会再回来执行我们模块中的，那么setup_module就要执行2次了。他是可以随变得。用例生成规则根据scope来定。。所以说前后置是根据中间有没有穿插入其他测试用例而定的，如果一个测试类，他有setup_class.再执行的时时候，中间插入了一条不是该测试用例类中的方法。那么这个setup_class将会执行两次

15. 当我们手动添加fixture的时候。如果按scope=class的方式，他会先将用例扩展，将使用了scope的放前面，将没有使用fixture的和最后一组数据放到最后
当我们手动添加fixture的时候。如果按scope=session的方式，pytest会按模块按顺序一步一步的收集和扩展用例，当发现这个模块中使用了fixture，这个模块中首先将这些使用了fixture的用例放到第一个会话，将没有使用fixture的放到最后一次会话中
```

**结论：这个pytest.fixture尽量不要是用autouse，就算使用，等级最好调成function，这样才不会怀了其他逻辑**

**主要关注：fixture的执行次数，和fixture对前后的影响。前后置的判断是根据，同类的中间是否插入了其他的。**



### 4.2	 `fixture`相互调用且实现前后置处理

##### 第一点:使用

定义fixture跟定义普通函数差不多，唯一区别就是在函数上加个装饰器`@pytest.fixture()`，fixture命名不要用test_开头，跟用例区分开。用例才是test_开头的命名。

fixture是可以有返回值的，如果没return默认返回None。用例调用fixture的返回值，直接就是把fixture的函数名称当成变量名称，如下案例

🔺：fixture实现前后置，主要是用于针对单个测试用例我们执行前后置。比setup这一类的更加精确

**例子：多个fixture相互调用结合前置处理复杂模式**

```python
import pytest

user_list = ['admin1', 'admin2']
user_pwd = ['123456', '654321']


@pytest.fixture(scope="function", params=user_list)
def user(request):
    print('user')
    return request.param


@pytest.fixture(scope="function", params=user_pwd)
def pwd(request):
    print('pwd')
    return request.param


@pytest.fixture()
def login(user, pwd):
    print('第一组账号', user, pwd)
    yield (user, pwd)
    print('结束战斗')


def test_demo_one(login):
    print('test_demo_one', login)


if __name__ == '__main__':
    pytest.main(['-s', './test_demo_two.py'])
```

运行结果: 每一个用例都前置登录了一下(模拟登录)

```python
collected 4 items

test_demo_two.py 
user
pwd
第一组账号 admin1 123456
test_demo_one ('admin1', '123456')
.结束战斗


user
pwd
第一组账号 admin1 654321
test_demo_one ('admin1', '654321')
.结束战斗


user
pwd
第一组账号 admin2 123456
test_demo_one ('admin2', '123456')
.结束战斗


user
pwd
第一组账号 admin2 654321
test_demo_one ('admin2', '654321')
.结束战斗


============================== 4 passed in 0.09s ==============================

Process finished with exit code 0

```

**🔺注意: 他们的scope必须一样, login的范围必须比其他的小, 比如login的scope是module,那么其他两个的scope只能是module或者session, 实际使用过程中我们一般吧他设置成一样的**



##### 第二点: 讲解

```python
# conftest.py	#主要是查看用例的收集情况,
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # print('\033[1;36m 开启报告钩子 \033[0m')
    out = yield
    report_object = out.get_result()
    if report_object.when == 'call':
        print(item.session.items)	# 打印出所有收集到的用例， 用例执行也是按这个列表进行执行
        
"""
执行一遍以后把这个注释掉免得影响你查看规律：如下是test_demo_two.py的用例集
[<Function test_demo_one[admin1-123456]>, <Function test_demo_two[admin1-123456]>, <Function test_demo_one[admin2-123456]>, <Function test_demo_two[admin2-123456]>, <Function test_demo_one[admin2-654321]>, <Function test_demo_two[admin2-654321]>, <Function test_demo_one[admin1-654321]>, <Function test_demo_two[admin1-654321]>, <Function test_demo_three>]

"""
```



```python
import pytest
import os

user_list = ['admin1', 'admin2']
user_pwd = ['123456', '654321']


@pytest.fixture(scope='class', params=user_list)
def user(request):
    print('user')
    return request.param


@pytest.fixture(scope='class', params=user_pwd)
def pwd(request):
    print('pwd')
    return request.param


@pytest.fixture(scope='class')
def login(user, pwd):
    print('\033[1;35m setup_module setup_module setup_module setup_module setup_module \033[0m')
    yield (user, pwd)   # 传递参数给 def test_demo_one(self, login):中的login位置参数
    print('\033[1;35m teardown_module teardown_module teardown_module teardown_module \033[0m')




class TestBehavior(object):

    @pytest.mark.normal
    def test_demo_one(self, login):
        print('\033[1;32m test_demo_one  \n \033[0m' , login)

    def test_demo_two(self, login):
        print('\033[1;32m test_demo_two  \n \033[0m' , login)

    def test_demo_three(self):
        print('\033[1;32m test_demo_three \n \033[0m')


class TestBehavior2(object):

    @pytest.mark.normal
    def test_demo_one(self, login):
        print('\033[1;33m test_demo_one  \n \033[0m' , login)

    def test_demo_two(self, login):
        print('\033[1;33m test_demo_two \n \033[0m' , login)

    def test_demo_three(self):
        print('\033[1;33m test_demo_three \n \033[0m')


class TestBehavior3(object):

    @pytest.mark.normal
    def test_demo_one(self):
        print('\033[1;34m test_demo_one  \n \033[0m')

    def test_demo_two(self):
        print('\033[1;34m test_demo_two \n \033[0m')

    def test_demo_three(self):
        print('\033[1;34m test_demo_three \n \033[0m')


# if __name__ == '__main__':
#     # pytest.main(['-s', './test_demo_two.py'])
#     os.system('pytest -s ./test_demo_two.py')



if __name__ == '__main__':
    # pytest.main(['-v', '-s', '--collect-only'])
    pytest.main(['-v', '-s'])
```

运行结果

```
collecting ... collected 21 items

test_5.py::TestBehavior3::test_demo_one  test_demo_one  
 
PASSED
test_5.py::TestBehavior3::test_demo_two  test_demo_two 
 
PASSED
test_5.py::TestBehavior3::test_demo_three  test_demo_three 
 
PASSED
test_5.py::TestBehavior::test_demo_one[admin1-123456] user
pwd
 setup_module setup_module setup_module setup_module setup_module 
 test_demo_one  
  ('admin1', '123456')
PASSED
test_5.py::TestBehavior::test_demo_two[admin1-123456]  test_demo_two  
  ('admin1', '123456')
PASSED
test_5.py::TestBehavior::test_demo_one[admin2-123456]  teardown_module teardown_module teardown_module teardown_module 
user
 setup_module setup_module setup_module setup_module setup_module 
 test_demo_one  
  ('admin2', '123456')
PASSED
test_5.py::TestBehavior::test_demo_two[admin2-123456]  test_demo_two  
  ('admin2', '123456')
PASSED
test_5.py::TestBehavior::test_demo_one[admin2-654321]  teardown_module teardown_module teardown_module teardown_module 
pwd
 setup_module setup_module setup_module setup_module setup_module 
 test_demo_one  
  ('admin2', '654321')
PASSED
test_5.py::TestBehavior::test_demo_two[admin2-654321]  test_demo_two  
  ('admin2', '654321')
PASSED
test_5.py::TestBehavior::test_demo_one[admin1-654321]  teardown_module teardown_module teardown_module teardown_module 
user
 setup_module setup_module setup_module setup_module setup_module 
 test_demo_one  
  ('admin1', '654321')
PASSED
test_5.py::TestBehavior::test_demo_two[admin1-654321]  test_demo_two  
  ('admin1', '654321')
PASSED
test_5.py::TestBehavior::test_demo_three  test_demo_three 
 
PASSED teardown_module teardown_module teardown_module teardown_module 

test_5.py::TestBehavior2::test_demo_one[admin1-123456] user
pwd
 setup_module setup_module setup_module setup_module setup_module 
 test_demo_one  
  ('admin1', '123456')
PASSED
test_5.py::TestBehavior2::test_demo_two[admin1-123456]  test_demo_two 
  ('admin1', '123456')
PASSED
test_5.py::TestBehavior2::test_demo_one[admin2-123456]  teardown_module teardown_module teardown_module teardown_module 
user
 setup_module setup_module setup_module setup_module setup_module 
 test_demo_one  
  ('admin2', '123456')
PASSED
test_5.py::TestBehavior2::test_demo_two[admin2-123456]  test_demo_two 
  ('admin2', '123456')
PASSED
test_5.py::TestBehavior2::test_demo_one[admin2-654321]  teardown_module teardown_module teardown_module teardown_module 
pwd
 setup_module setup_module setup_module setup_module setup_module 
 test_demo_one  
  ('admin2', '654321')
PASSED
test_5.py::TestBehavior2::test_demo_two[admin2-654321]  test_demo_two 
  ('admin2', '654321')
PASSED
test_5.py::TestBehavior2::test_demo_one[admin1-654321]  teardown_module teardown_module teardown_module teardown_module 
user
 setup_module setup_module setup_module setup_module setup_module 
 test_demo_one  
  ('admin1', '654321')
PASSED
test_5.py::TestBehavior2::test_demo_two[admin1-654321]  test_demo_two 
  ('admin1', '654321')
PASSED
test_5.py::TestBehavior2::test_demo_three  test_demo_three 
 
PASSED teardown_module teardown_module teardown_module teardown_module 


========================== 21 passed in 0.16 seconds ==========================
```

- **复制代码，自己运行一下看看规律**



**例子二: 这个更好的观察运行规律**

```python
import pytest
import os
import random

user_data = ['账号1', '账号2']
pwd_data = ['密码1', '密码2']


@pytest.fixture(params=user_data, scope='class')
def user(request):
    print('user')
    return {request.param, random.randint(100, 20000)}    # 生成随机账号,可以使用faker模块，我这里为了方便就用random，由于user_data和pwd_data的元素都是字符串，我可以把它正常一个字典


@pytest.fixture(params=pwd_data, scope='class')
def pwd(request):
    print('pwd')
    return {request.param, random.randint(100, 20000)}    # 生成随机密码,可以使用faker模块，我这里为了方便就用random，由于user_data和pwd_data的元素都是字符串，我可以把它正常一个字典


class TestBehavior(object):

    def test_one(self, user, pwd):
        print('test_one', (user, pwd))
        assert 1

    def test_two(self, user, pwd):
        print('test_two', (user, pwd))
        assert 1

    def test_three(self, user, pwd):
        print('test_three', (user, pwd))
        assert 1

    def test_four(self):
        print('test_three', (None, None))
        assert 1


if __name__ == '__main__':
    pytest.main(['-s', './test_demo_three.py'])
```

运行结果：从fixture的调用次数触发。分析。可以看看第四章的总结。fixture的调用次数是和scope挂钩的，下面的分析可能不对哈。这是第一次学习的时候，总结的，还是得自己运行了以后看看

```python
collected 13 items 			# 由于scope是class， 将使用了夹具的用例，生成一个新测试类，然后再第一个类执行前运行夹具， 按类为单位，进行分组执行， 如果scope是function， 执行的时候是每一个用例联系执行4次， class就是每一个类连续执行4次（再测试用例结合收集执行进行了排序，我们这里说错虚拟类把），如果是module，就将py文件中，使用了夹具的用例函数和用例类提出来生成一个虚拟模块

test_demo_three.py 
user						# 第一组需要两个参数所以同时执行了user 和 pwd夹具
pwd
test_one ({'账号1': 3758}, {'密码1', 5340})
.test_two ({'账号1': 3758}, {'密码1', 5340})
.test_three ({'账号1': 3758}, {'密码1', 5340})
------------------------------------------------------------------------
.user						# 第二组，根据排列组合，pwd不变，所以不执行，延用上一轮的值，user需要改变，所以执行了user夹具
test_one ({'账号2': 12044}, {'密码1', 5340})
.test_two ({'账号2': 12044}, {'密码1', 5340})
.test_three ({'账号2': 12044}, {'密码1', 5340})
------------------------------------------------------------------------
.pwd						# 第三组，根据排列组合， user不变，所以不执行，延用上一轮的值，pwd需要改变，所以执行了pwd夹具
test_one ({'账号2': 12044}, {'密码2', 14244})
.test_two ({'账号2': 12044}, {'密码2', 14244})
.test_three ({'账号2': 12044}, {'密码2', 14244})
------------------------------------------------------------------------
.user						# 第四组，根据排列组合，pwd不变，所以不执行，延用上一轮的值，user需要改变，所以执行了user夹具
test_one ({'账号1': 9361}, {'密码2', 14244})
.test_two ({'账号1': 9361}, {'密码2', 14244})
.test_three ({'账号1': 9361}, {'密码2', 14244})
.test_three (None, None)
.

============================= 13 passed in 0.11s ==============================
```





**🔺如果把上面的scope改成module,执行结果还是一样的，pytest会将使用了夹具的用例提出来，根据排列组合生成4个虚拟module，将这4个module都执行一遍， 最后一组会将没有使用夹具的一起带上，scope这个参数只是决定，用例的执行顺序，**

- **scope为session的时候，如果采用了参数化，就会把使用了夹具的用例提出来，按排列组合创建多个会话，一个一个执行**
- **scope为module的时候，如果采用了参数化， 就会把使用了夹具的用例提出来， 按排列组合创建多个module，在一个会话执行的时候，这些虚拟module也会被当成当前会话中module进行执行**
- **scope为class的时候， 如果采用了参数化，就会把使用了夹具的用例提出来，按排列组合创建多个class，在一个module执行的时候，这些虚拟class也会被当成当前module中的class进行执行**
- **scope为function的时候，如果采用了参数化，就会把使用了夹具的用例提出来，按排列组合创建多个function，这些虚拟fucntion也会被执行**



















### 4.3	`fixture`的作用范围与fixture执行次数得关系

autouse=False

- **function**:        fixtrue调用次数 == 使用了fixture的用例  *  fixture的数据组个数
- **class： **              fixture执行次数 == (手动添加了fixture的class测试类用例集合的个数 + 手动添加了fixture函数测试用例数量) * 数据组数
- **module：**       fixture执行次数 == 手动添加的fixture的.py文件数量 * 数据组数
- **session： **        有多少组数据，执行多少次fixture

function默认模式@`pytest.fixture(scope='function')`或 `@pytest.fixture()`





### 4.5	`fixture`实例演示 -- `fixture`作为函数参数使用





### 4.6	`@pytest.mark.skip(reason)`和`@pytest.mark.skipif(condition条件, reason)`

##### 4.6.1	`@pytest.mark.skip(reason)`

**备注：**

- **如果被标记成`skip`，用例收集的时候，还是会将它收集到用例集`items`中，但是执行的时候将会被跳过**
- **如果被特殊指定，如`pytest -m skip`， 还是不会执行，因为`pytest -m skip`只是一个用例筛选的过程，执不执行还得看`pytest`的逻辑**



**实例如下**

```python
@pytest.mark.skip('不知道')
class TestInter(object):

    def test_inter_sub_one(self):
        print('test_inter_sub_one')

    def test_inter_sub_two(self):
        print('test_inter_sub_two')
        
        
def test_inter_sub_five():				# 这个用例是用来检查pytest收集用例的时候，是不是把skip也收集进去了
    print('test_inter_sub_five')
        
        
if __name__ == '__main__':
    # pytest.main(['-s', '-m', 'skip'])
    os.system('pytest -s')
    
=========输出=========    
 collected 3 items		# skip也被收集进去了，但是在执行的时候被skip了
ss						# s表示skip跳过， 由于被跳过了，返回报告中就只显示s， 不打印用例的中的数据，y
 test_inter_sub_five .	# . 表示测试通过
===================== 1 passed, 2 skipped in 0.13 seconds =====================
结论： 如果被skip标记以后，还是会被pytest的用例收集机制收集，但是会被skip掉
```



##### 4.6.2	`@pytest.mark.skipif(condition条件, reason)`

**备注：`@pytest.mark.skipif(condition..., reason)` -- 若满足condition，则跳过测试函数, 报告中现实原因**



**例子： 下面是多个条件跳过的例子**

**备注：当一条用例用多个跳过条件的时候，只要满足一个条件；则跳过该测试用例**

```python
import os
import pytest


class TestCase():
  #当多个@pytest.mark.skipif()标签时，若满足一个，则跳过测试用例
  @pytest.mark.skipif(condition='a' >= 'b', reason="no reason")	# ASCII码值比较大小
  @pytest.mark.skipif(condition='a' <= 'b', reason="no reason") # ASCII码值比较大小
  def test_01(self):
    print("---用例b执行---")
 
  def test_02(self):
    print("---用例c执行---")
    
 if __name__ == '__main__':
    os.system('pytest -s')
=====输出结果========
collected 2 items	
s					  # test_01被跳过了，就不打印---用例b执行---了，直接现实结果 s s表示跳过
---用例c执行--- .			
========================== 2 skipped in 0.02 seconds ==========================
```





# 五、`pytest`报告结果

**前言：只有知道各种状态的含义才能更好的调试我们的自动化用例**

**`pytest`目前已知有6种状态**

- **`passed`**

- **`failed`**

- **`xfailed`**

	- ```python
		def test_inter_two_sub_three(input_user, pwd):
		    # print('\033[1;35m test_inter_two_sub_three \033[0m')
		    print('\033[1;36m %s : %s \033[0m' % (input_user, pwd))
		    if pwd == '654321':
		        pytest.xfail('就是失败, 怎么了')	# 使用pytest.xfail(reason)将用例标记成xfailed
		```

- **`skip`**

- **`error`**

- **`deselected`: 用例未被选择**



# 六、运行上次失败用例(--lf 和 --ff）

#### 前言

“80%的bug集中在20%的模块，越是容易出现bug的模块，bug是越改越多“平常我们做手工测试的时候，比如用100个用例需要执行，其中10个用例失败了，
当开发修复完bug后，我们一般是重点测上次失败的用例。
那么自动化测试也一样，当用例特别多时，为了节省时间，第一次部分用例失败了，修复完之后，可以只测上次失败的用例。











# 七、`conftest.py`文件

#### 7.1	`conftest.py`注意事项

- **`conftest.py`配置脚本名称是固定的，不能改名称,可以到源码的`_pytest.hookspec.py`中去查看，里面有简单介绍**
- **`conftest.py`文件不能被其他文件导入**
- **`conftest.py`文件，会在测试会话开始前运行**
- **建议只设置一个`conftest.py`， 使其在项目的根目录下**
- **🔺在`conftest.py` 被`@pytest.fixture`装饰的函数将变成全局的，不需要导入直接使用（使用规则不变）**



#### 7.1	测试发现`conftest.py`的顺序

- **首先检查当前目录（当级中子目录里面的不算）**
- **检查上级目录**
- **一直检查到项目根目录**
- **如果存在多个`conftest.py`，按发现顺序每个`conftest.py`都会执行，但是建议只在根目录中设置一个**





# 八、常用的钩子

**🔺注意：提前说一下，像 `pytest_runtest_*`这种测试运行期间的钩子方法，其钩子方法不允许抛出异常，不然会破坏`Pytest`的运行流程,切记**

#### **8.1	钩子函数的参数说明：**

- **`config(_pytest.config.Config)` -` pytest`配置对象**
	- 源码路径：`_pytest\config\__init__\Config`，里面有很多config的方法
	- `config.addinivalue_line['markers', 'P1']`添加
- **`val`- 参数化值**
- **`argname(str)` - `pytest`生成的自动参数名称**
- **`session(_pytest.main.Session)` -` pytest`会话对象**
	- `session.items`, 获取整个测试用例列表[<Function test_demo_sub_one>, <Function test_demo_sub_two>, <Function test_demo_sub_three>, <Function test_demo_sub_four>]
- **`config(_pytest.config.Config)` - `pytest`配置对象**
- **`items(_pytest.nodes.Item])` - 用例对象列表**
- **`item`为其执行运行测试协议的测试项目**
	- `item.config == config配置对象`
	- `item.session == session会话对象`
	- `item.session.items == session.items`
	- `item.nodeid`
	- `item.parent`

**备注： `item` > `session` **





#### 8.2	`pytest_runtest_setup(item)`

**备注：如果定义了此钩子，每个用例执行之前都会调用先一次该钩子，然后开始执行**



```python
# conftest.py
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    print('\033[1;35m 我是pytest_runtest_setup \033[0m')
    outcome = yield
    item._obj()
    print('\033[1;35m 将要执行 %s \033[0m' % item.function)
```

**🔺须知:如果在`conftest.py`中使用了2个相同的钩子，`pytest`只会生效一个**



#### 8.3	`pytest_configure(config)`添加标签

- ​	**在`conftest.py`文件中注册**
- ​    **`conftest.py`放到项目跟目录下，对全局生效，也可以放到用例目录下，这样他的优先级将高于全局的**
- ​    **使用`@pytest.mark.cirtical、@pytest.mark.cirtical、@pytest.mark.cirtical`标记用例**
- ​    **使用没有注册的标记会报警告**
- ​    **没有返回值**

```python
# content of conftest.py

import pytest

def pytest_configure(config):
    marker_list = ["critical", "normal", "minor"]
    for markers in marker_list:
        config.addinivalue_line("markers", markers)
```







#### 8.4	`pytest_runtest_makereport(item, call)`

**该钩子和用例的执行顺序**

- **先执行该钩子**
- **通过yield跳转去执行用例**
- **用例执行结果报告通过send返回给yield**
- **输出报告**
- **`pytest_runtest_makereport(item, call)`对setup和teardown的前后置也会关注**





# 九、参数化的两种方式(及传参格式)



## 9.1	`@pytest.mark.parametrize`参数化

#### `@pytest.mark.parametriz`e常规传参

`@pytest.mark.parametrize`，接收两个参数

- 第一个参数是字符串，多个参数中间用逗号隔开

- 第二个参数是list,多组数据用元祖类型，相当于`@pytest.fixture`的`params`参数



```python
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
test_04.py::test_eval[3+5-8] PASSED
test_04.py::test_eval[2+4-6] PASSED
test_04.py::test_eval[6 * 9-42] FAILED
```



****



#### `@pytest.mark.parametriz`e完整传参及过滤用法

`@pytest.mark.parametrize`，接收两个参数

- 第一个参数是字符串，多个参数中间用逗号隔开
- 第二个参数完整的传参格式是这样的`pytest.param('param1', 'param2', ...paramN, marks=pytest.mark.skip、xfail、P0)`，marks参数可以不用写
-  用例接收参数的位置个数必须一直
- 

```python
import pytest


@pytest.mark.parametrize(
    "test_input,expected",
    [
        pytest.param('3 + 5', 8, marks=pytest.mark.P0, id='A, B'),
        pytest.param('2 + 2', 4, marks=pytest.mark.P0),
        pytest.param('1 + 3', 4, marks=pytest.mark.P1)
     ]
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected


if __name__ == "__main__":
    pytest.main(['-s', '-v', "test_04.py", '-m=P0'])
```

运行结果

```python
collecting ... collected 3 items / 1 deselected / 2 selected

test_04.py::test_eval[A, B] PASSED
test_04.py::test_eval[2 + 2-4] PASSED

======================= 2 passed, 1 deselected in 0.07s =======================
```



## 9.2	`@pytest.fixture`参数化



```python
import pytest
import os

data_user = ['zhangmingzhu', 'liji', 'liyi']
data_pwd = ['123456', '654321', 'zmz123456', 'zmz654321']


@pytest.fixture(params=data_user)
def user_user(request):
    return request.param


@pytest.fixture(params=data_pwd)
def user_pwd(request):
    return request.param


def test_sub_one(user_user, user_pwd):
    print('\033[1;32m %s ： %s \033[0m' % (user_user, user_pwd))


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_05.py'])
```

运行结果

```python
collecting ... collected 12 items

test_05.py::test_sub_one[zhangmingzhu-123456]  zhangmingzhu ： 123456 
PASSED
test_05.py::test_sub_one[zhangmingzhu-654321]  zhangmingzhu ： 654321 
PASSED
test_05.py::test_sub_one[zhangmingzhu-zmz123456]  zhangmingzhu ： zmz123456 
PASSED
test_05.py::test_sub_one[zhangmingzhu-zmz654321]  zhangmingzhu ： zmz654321 
PASSED
test_05.py::test_sub_one[liji-123456]  liji ： 123456 
PASSED
test_05.py::test_sub_one[liji-654321]  liji ： 654321 
PASSED
test_05.py::test_sub_one[liji-zmz123456]  liji ： zmz123456 
PASSED
test_05.py::test_sub_one[liji-zmz654321]  liji ： zmz654321 
PASSED
test_05.py::test_sub_one[liyi-123456]  liyi ： 123456 
PASSED
test_05.py::test_sub_one[liyi-654321]  liyi ： 654321 
PASSED
test_05.py::test_sub_one[liyi-zmz123456]  liyi ： zmz123456 
PASSED
test_05.py::test_sub_one[liyi-zmz654321]  liyi ： zmz654321 
PASSED

============================= 12 passed in 0.08s ==============================
```







# 十、失败重跑和内置fixture之cache使用

## 10.1	失败重跑

#### 前言

“80%的bug集中在20%的模块，越是容易出现bug的模块，bug是越改越多“平常我们做手工测试的时候，比如用100个用例需要执行，其中10个用例失败了，
当开发修复完bug后，我们一般是重点测上次失败的用例。
那么自动化测试也一样，当用例特别多时，为了节省时间，第一次部分用例失败了，修复完之后，可以只测上次失败的用例。

- `--lf, --last-failed 只重新运行上次运行失败的用例（或如果没有失败的话会全部跑）`
- `--ff, --failed-first 运行所有测试，但首先运行上次运行失败的测试（这可能会重新测试，从而导致重复的fixture setup/teardown）`

#### **注意：**

- **第一次部分用例失败了，修复完之后，--lf方式运行，此时全部用例已经被修复了，cache将会被刷新**
- **如果没有失败的用例，则全部重跑**
- **我们不能改变`nodeid`, 如果修改了`nodeid`，这将会被认定为一个新的用例，尤其是我们使用参数化的时候，如果我们改变了参数值，`nodeid`也将发生改变**
	- **可以通过设置`ids`参数来避免这种事发生**

#### 例子

```python
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ('4 + 5', 9),
        pytest.param('3 + 5', 8, marks=pytest.mark.P0, id='A, B'),
        pytest.param('3 + 4', 7, marks=pytest.mark.P0),
        pytest.param('1 + 5', 6)

     ]
)

def test_eval(test_input, expected):
    # assert str(eval(test_input)) == expected
    assert eval(test_input) == expected

if __name__ == "__main__":
    pytest.main(['-s', '-v', "test_04.py", '--lf']) # 通过查看cache文件夹下面的lastfailed文件来观察
```







## 10.2	内置fixture之cache使用

#### 前言

```
pytest 运行完用例之后会生成一个 .pytest_cache 的缓存文件夹，用于记录用例的ids和上一次失败的用例。
方便我们在运行用例的时候加上--lf 和 --ff 参数，快速运行上一次失败的用例。
--lf, --last-failed 只重新运行上次运行失败的用例（或如果没有失败的话会全部跑）
--ff, --failed-first 运行所有测试，但首先运行上次运行失败的测试（这可能会重新测试，从而导致重复的fixture setup/teardown）
```



#### 参数说明：

- `--lf 也可以使用 `--last-failed` 仅运行上一次失败的用例`
- `--ff 也可以使用 `--failed-first` 运行全部的用例，但是上一次失败的用例先运行`
- `--nf 也可以使用 `--new-first` 根据文件插件的时间，新的测试用例会先运行`
- `--cache-show=[CACHESHOW] 显示.pytest_cache文件内容，不会收集用例也不会测试用例，选项参数: glob (默认: '*')`
- `--cache-clear 测试之前先清空.pytest_cache文件`

![img](https://img2020.cnblogs.com/blog/1070438/202009/1070438-20200904113450634-1915931493.png)







# 十一、重复执行用例

## 11.1	常规使用

#### 前言

平常在做功能测试的时候，经常会遇到某个模块不稳定，偶然会出现一些bug，对于这种问题我们会针对此用例反复执行多次，最终复现出问题来。
自动化运行用例时候，也会出现偶然的bug，可以针对单个用例，或者针对某个模块的用例重复执行多次。

#### `pytest-repeat`

`pytest-repeat`是`pytest`的一个插件，用于重复执行单个用例，或多个测试用例，并指定重复次数，pytest-repeat支持的版本：

- `Python 2.7, 3.4+ 或 PyPy`
- `py.test 2.8或更高`

使用pip安装`pytest-repeat`

> `pip install pytest-repeat`

使用--count命令行选项指定要运行测试用例和测试次数

> `pytest --count=10 test_file.py`



#### 例子

```python
import pytest
import os
import time


@pytest.fixture(params=['yoyo'])
def start(request):
    return request.param


def test_01(start):
    print("测试用例test_01")
    time.sleep(0.5)
    assert start == "yoyo"


@pytest.mark.repeat(5)
def test_02(start):
    print("测试用例test_02")
    time.sleep(0.5)
    assert start == "yoyo"


if __name__ == "__main__":
    pytest.main(["-s", "test_06.py", '--count=10'])
    # os.system('pytest -s -v test_06.py --count=10')
```

**注意：**

- **目前我发现有`os.system`执行会报错，不知道为什么?**
- **当在执行语句中加入--count=10的时候，全部用例将会执行10遍，但是不会如果用例标记了`@pytest.mark.repeat(5)`，则只执行5次**
- **如果指定了@pytest.mark.repeat(5),不用我们怎么操作，执行用例的时候他会自动执行5遍**



# 十二、失败后重跑

#### 失败重试

失败重跑需要依赖`pytest-rerunfailures`插件，使用pip安装就行

> - ```python
> 	pip install pytest-rerunfailures
> 	```

用例失败再重跑1次,命令行加个参数--reruns就行了

> - ```python
> 	pytest --reruns 1 --html=report.html --self-contained-html
> 	```
>
> - ```python
> 	pytest.main(["-s", '-v', "test_06.py", '--reruns=1'])
> 	```

```
pytest.main(['-s', '--reruns=1'])
```









# 十四、pytest-html生成测试报告

#### 前言

pytest-HTML是一个插件，pytest用于生成测试结果的HTML报告。兼容Python 2.7,3.6

#### pytest-html

1.github上源码地址[【https://github.com/pytest-dev/pytest-html】](https://github.com/pytest-dev/pytest-html)

2.pip安装

> -  pip install pytest-html

3.执行方法

> -  pytest --html=report.html
> - pytest.main(['--html=report.html'])
>
> - 会在当前目录种生成一个html测试报告
> - pytest --html=./report/report.html # 指定路径执行存放报告







# 十五、allure-pytest生成测试报告

pytest-allure-adaptor 这个插件与 allure-pytest 不能共存，卸载掉 pytest-allure-adaptor

#### allure命令行工具

allure是一个命令行工具，需要去github上下载最新版https://github.com/allure-framework/allure2/releases

![img](https://img2018.cnblogs.com/blog/1070438/201912/1070438-20191208000013685-1786868653.png)

下载完成之后，解压到本地电脑

![img](https://img2018.cnblogs.com/blog/1070438/201912/1070438-20191208000127283-737054495.png)

![img](https://img2018.cnblogs.com/blog/1070438/201912/1070438-20191208000146873-341233328.png)

把bin目录添加到环境变量Path下

![img](https://img2018.cnblogs.com/blog/1070438/201912/1070438-20191208000239968-329747801.png)

**开启allure的web服务**



> allure serve report/allure_raw	这里注意指定我们生成的数据的绝对路径，不然没有数据的哦。

```
allure serve ./raw_data -h 127.0.0.1 -p 10086
```

如果有很多测试用例，现在只想做个快速的回归测试，只测试用例级别为blocker和critical级别的测试用例

> pytest --alluredir ./report/allure --allure-severities blocker,critical

也可以这样写

> pytest --alluredir=./report/allure --allure-severities=blocker,critical

如果只执行blocker级别的用例

> pytest --alluredir=./report/allure --allure-severities=blocker



# 十九、`pytest`的各种方法及参数收集

```python
pytest.xfail(reason)	# 用例种调用该方法，将会被记录成xfailed状态，并退出用例执行
pytest.assume(x == y)	# 36章节
pytest.assume(x+y > 1)
pytest.assume(x > 1)	# 三个断言都会执行，那怕前面失败了，这样的好处是，我们可以知道我们到底哪里错了，因为assert普通断言只要前面失败，用例就终止了



第一种
@pytest.mark.parametrize("test_input,expected",
                         [ ("3+5", 8),
                           ("2+4", 6),
                           ("6 * 9", 42),
                         ])

第二种
@pytest.mark.parametrize(
    "test_input,expected",
    [
        pytest.param('3 + 5', 8, marks=pytest.mark.P0, id='A, B'),
        pytest.param('2 + 2', 4, marks=pytest.mark.skip),
        pytest.param('1 + 3', 4, marks=pytest.mark.xfail)
     ]
)
第三种
@pytest.fixture(params=['123456', '654321'], ids=['zmz账号的密码', 'lcc账号的密码'], name='dirver')

第四种	# 列表中, 任何以逗号隔开的都算一条数据
data = [{'username': 'test1', 'password': '1234'}, {'username': 'test2', 'password': '4321'}]
@pytest.fixture(params=data, ids=['第一组数据', '第二组数据'])
```









# 二十、命令参数及其它

**注解:**

- **这个 `-q/--quiet` 保持输出简短。**

```python
pytest -q test_sample.py	# 相对路径,从当前执行文件所在目录为root目录，执行下面的test_sample.py文件,以quit模式
pytest -q D:/origin/学习代码/interface_auto/src/api_case/接口脚本/test_sysexit.py	# 绝对路径
pytest test_sample.py		# 相对路径,从当前执行文件所在目录为root目录，执行下面的test_sample.py文件,以普通模式
assert x == 3, "第" + str(i + 1) + '次断言失败'	# 断言失败后进行描述

pytest -q --maxfail=2 test_sample.py	# 在两次失败以后停止运行
pytest -q -x test_sample.py				# 在第一次失败以后停止运行
pytest -q .								# 扫描当前目录并执行

pytest -k 关键字						  # 只执行含有该关键字的类或者函数（注意1.当函数不匹配的时候，他回去找里面的函数。2.当类匹配的时候，他会执行整个类里面的函数，哪怕有些函数不能匹配关键字 3.同理当文件匹配的时候，他执行整个文件中的用例，哪怕有些用例不匹配关键字）4.关键词过滤是在已收集到的用例池塘中进行过滤，所以类名、函数名、方法名必须符合用例的发现机制

pytest -p no:doctest					# 禁用 doctest插件
pytest -p pytest_cov					# 加载pytest_cov插件
```

**[`pytest.main()`](##二、 的调用)**

**注解:**
调用 `pytest.main() `将导致导入您的测试和它们导入的任何模块。由于python的导入系统具有缓存机制，因此随后调用` pytest.main() `来自同一进程的不会反映调用之间对这些文件的更改。因此，多次调用 pytest.main() 不建议使用同一进程（例如为了重新运行测试）。

但是，我们每一次在pycharm里面执行的时候，他都会给我们一个新进程ID。

```python
-s: 显示程序中的print/logging输出
-v: 丰富信息模式, 输出更详细的用例执行信息
-q: 安静模式, 不输出环境信息
-k：关键字匹配，用and区分：匹配范围（文件名、类名、函数名）
-x: 在第一次失败以后停止运行
--maxfail=2	在两次失败后停止运行
```

```python
# pytest.main(["--collect-only"])#展示所有测试用例
# pytest.main(["-k","keyword"])#使用指定表达式运行希望运行的用例
# pytest.main(["-v","-k","keyword"])# 增加-v查看详细信息
# pytest.main(["-v","-m","run_first"])
"""
使用-m对用例进行标记，用例需注释@pytest.mark.xxx,将xxx作为参数传入
使用-m "mark1 and mark2"可以同时选中带有这两个标记的所有测试用例。
使用-m "mark1 and not mark2"选中带哟与mark1的测试用例，而过滤掉带有mark2的测试用例
使用-m "mark1 or mark2"则选中带有mark1或者mark2的所有测试用例
"""
# pytest.main(["-v","-x"])#-x 遇到错误即停止
# pytest.main(["-v","--maxfail=2","--tb=no"])#--maxfail=n 设定最多失败 n 次即停止
# pytest.main(["-s"])#允许终端运行时输出某些结果，例如print
# pytest.main(["--lf"])#定位失败的用例
# pytest.main(["--ff"])#定位失败的用例首先执行，但是正常的用例也会执行
# pytest.main(["-q"])#简化输出信息
# pytest.main(["-l"])#打印失败用例的变量值
# pytest.main(["--tb=short"])
"""
--tb=style,选择失败回溯信息
short：仅输出assert一行以及系统判定内容(不显示上下文)
no：不展示回溯信息
line：只是用一行输出显示所有的信息错误，展示异常代码位置
auto：只展示第一个和最后一个错误
long：展示全部信息
native：只展示puthon标准库信息，不展示额外信息
"""
# pytest.main(["--duration=1"])#只关心哪些部分是最慢的
# pytest.main(["-h"])

"""
指定执行
"""
#pytest.main(['-s', 'test_class.py::TestClass::test_one'])
#pytest.main(['-s', 'test_class.py'])
```

- **[`pytest -k 关键字`](####1.6	按关键词匹配后运行测试用例)** 		**关键字匹配执行用例**

- **`pytest test_mod.py::test_func`**                                            
	- **指定执行`test_mod.py`模块下`test_func`函数测试用例，🔺模块文件名不受`pytest`用例收集规则限制，函数名必须是 `test`开头或者满足`pytest`查询用例规则**

- **`pytest test_mod.py::TestClass::test_method`**                
	- **指定执行`test_mod.py`模块下`TestClass`用例类里面的`test_method`方法用例，🔺模块文件名不受`pytest`用例收集规则限制，类名和函数名必须是 `test`开头或者满足`pytest`查询用例收集规则**



**[修改python回溯打印](https://www.osgeo.cn/pytest/usage.html#calling-pytest-through-python-m-pytest)**

修改回溯打印的示例：

```
pytest --showlocals # show local variables in tracebacks
pytest -l           # show local variables (shortcut)

pytest --tb=auto    # (default) 'long' tracebacks for the first and last
                     # entry, but 'short' style for the other entries
pytest --tb=long    # exhaustive, informative traceback formatting
pytest --tb=short   # shorter traceback format
pytest --tb=line    # only one line per failure
pytest --tb=native  # Python standard library formatting
pytest --tb=no      # no traceback at all
```



**详尽的测试结果摘要**

```
-r 选项接受后面的多个字符,上面使用的 a 表示“除了执行通过(Pass)以外所有的结果”。
以下是可以使用的可用字符的完整列表：
- f - 失败的用例
- E - 出错的用例
- s - 跳过的用例
- x - 标记失败的用例
- X - 标记成功的用例
- p - 成功用例(小写的p)
- P - 成功用例并输出信息(大写的P)
- a - 所有 pP 状态以外的用例
```



**使用到的pytest操作**

```python
@pytest.mark.P0(reason:[Option])
@pytest.mark.usefixtures(fixturename1, fixturename2, ....) # 如果fixture使用了别名，fixturename必须也是他的别名
@pytest.fixture(scope, autouse, params, ids, name)
@pytest.mark.skip(reason:[Option])
@pytest.mark.skipif(reason:[Option])
@pytest.mark.parametrize()

pytest.xfail('reason')
pytest.mark.xfail

request.param  				# 是夹具获取上下文参数的方法
return 						# 可用于夹具返回
夹具名						  #  使用了夹具的用例，可以使用夹具名的位置参数来获取夹具returnd
```







# 二十一、小细节

#### 21.1	error和failed区别

测试结果一般有三种：passed、failed、error。（skip的用例除外）

- 如果在test_用例里面断言失败，那就是failed，不会被统计一次error
- 如果在test_用例里面代码出错，那也是failed（比如：`IndexError: list index out of range`,  `raise StopIteration`）非自动和主动代码报错的话，用例结果也是failed。说白了就是用例里面的任何情况都只是failed，不会被统计一次error
- 如果test_使用了被`@pytest.fixture`夹具装饰的夹具函数，夹具中有错误，就要具体原因具体分析了；
	- 如果夹具函数一开始就error了(优先执行夹具函数)，使整个测试用例阻塞，测试结果将会是error
	- 如果是夹具函数采用了yield做前后置，后置环节error了，这个时候测试用例结果可能是passed或者failed，还会给出有多少处error

- `conftest.py`的夹具错误，将会导致整个用例全部error



#### 21.2	用例和fixture的执行顺序

**通过例子来分析**

```python
import pytest
import os

@pytest.fixture(params=[1, 2, 3, 4])
def login(request):
    print("前置操作：准备数据")
    yield request.param		🔺 通过yield 来传递前置的结果或者参数(request.param) 给用例
    print("后置操作：清理数据")


def test_01(login):
    if login == 4:
        assert 0
    assert 1
    
===================== 1 failed, 3 passed in 0.18 seconds ======================
```

**顺序**

- **`pytest`发现用例使用了夹具函数（通过用例函数的位置参数名来判断 -- 用例位置参数名和夹具函数名保持一致）**
- **`pytest`框架会先执行def login(request)夹具函数(`pytest`可能是通过next(login)来执行的)**
- **执行完def login(request)夹具函数中的`yield request.param`代码以后，通过yield将结果`request.param`传递给def test_01(login)中的login位置参数**
- **再执行`def test_01(login==request.param)`用例**
- **执行完用例函数以后，`pytest`再次调用next(login)继续执行夹具函数def login(request):**



#### 21.3	当一个用例中同时使用两种方式使用夹具函数时的规则及`pytest`识别夹具的规则

****

**实例如下：一个用例同时使用`@pytest.mark.usefixtures`和夹具入参的方式调用夹具**

**该实例反应的规则有：**

- 当一个用例中同时采用两种方式来使用夹具函数时的规则
- `pytest`识别夹具的规则

```python
import pytest
import os

# conftest.py
@pytest.fixture(params=[1, 2, 3, 4])
def login(request):
    print("前置操作：准备数据")
    yield request.param
    print("后置操作：清理数据")


@pytest.fixture(params=['a', 'b', 'c', 'd'])
def start(request):
    return request.param

# test_inter.py
@pytest.mark.usefixtures('login', 'start')	# 使用@pytest.mark.usefixtures的方式调用夹具
def test_01(start):							# 使用入参的形式调用夹具
    print(login, start)
    if login == 4:
        assert 0
    assert 1
    
========================== 16 passed in 0.14 seconds ==========================

# test_inter.py
@pytest.mark.usefixtures('login', 'start')	# 使用@pytest.mark.usefixtures的方式调用夹具
def test_01(a):								# 使用入参的形式调用夹具
    print(login, start)
    if login == 4:
        assert 0
    assert 1
file D:\origin\学习代码\interface_auto\src\api_case_two\接口脚本_two\test_01.py, line 21
  @pytest.mark.usefixtures('login', 'start')
  def test_01(a):
E       fixture 'a' not found				# 夹具'a' 没有被发现
========================== 16 error in 0.18 seconds ===========================

# test_inter.py
@pytest.mark.usefixtures('login', 'start')
def test_01(login=1):
    print(login, start)
    if login == 4:
        assert 0
    assert 1
========================== 16 passed in 0.14 seconds ==========================



```

**规则1：当一个用例中同时采用两种方式来使用夹具函数时的规则（入参使用夹具 和 `@pytest.mark.usefixtures` 的方式）**

- **`pytest`先判断用例是否使用入参的方式调用夹具，通过检查用例的位置参数**

- **如果位置参数名和夹具名一致，再判断，该夹具是否存在于`usefixtures('login', 'start')`中，如果不存在，再其后面添加，如果存在，啥也不干**
- **按`usefixtures`('login', 'start')中的先后顺序执行夹具**
- **将夹具的执行结果传递给用例的🔺位置参数**

**规则2：`pytest`识别夹具的规则**

- **`pytest`是通过🔺位置参数来识别夹具的，如果要通过入参的方式调用夹具，此时用例中的🔺位置参数，必须和夹具函数的函数名一样，否则报错**
- **采用默认参数来代表传参（如果你想传参但不使用夹具的话），默认参数是不会被识别成夹具的**



#### 21.4	本地和`confitest.py`定义两个同名的夹具

- **使用本地夹具，忽略`conftest.py`**
- **就算本地调用了`conftest.py`的夹具，但是执行的代码还是本地夹具中的代码（有点绕口，看例子）**

**条件：本地和`conftest.py`中都定义了一个叫`open`的夹具，且本地的夹具没有设置`autouse`,也没有被用例使用，`conftest.py`中的夹具设置了`autouse=True`**

```python
# @File    : test_inter_two.py
import os
import pytest

@pytest.fixture(scope="class")
def open():
    print('\033[1;35m 本地的夹具 \033[0m')


class TestCase():
    # 当多个@pytest.mark.skipif()标签时，若满足一个，则跳过测试用例
    # @pytest.mark.skipif(condition='a' >= 'b', reason="no reason")  # ASCII码值比较大小
    # @pytest.mark.skipif(condition='a' <= 'b', reason="no reason")  # ASCII码值比较大小
    def test_01(self):
        print("---用例01执行---")

    def test_02(self):
        print("---用例02执行---")
===========================================================================================================
# @File    : conftest.py
import os
import pytest

@pytest.fixture(scope="class", autouse=True)
def open():
    print('\033[1;35m conftest.py 中的夹具 \033[0m')
------------------------------------------输出如下------------------------------------------------
collected 2 items

test_inter_two.py  本地的夹具 
---用例01执行---
.---用例02执行---
.

========================== 2 passed in 0.12 seconds ===========================
```

**🔺结论：通过`autouse=True`调用了`conftest.py`中的夹具，但是执行的却是本地夹具的代码**



#### 21.5	夹具传递参数给用例有2中方式

**备注:夹具传递参数给用例有2中方式**

- 第一种,夹具通过return 将参数传递给用例的位置参数
- 第二种,夹具通过yield 将参数传递给用例的位置参数





# 二十二、遗留问题

**`@pytest.mark.skipif(IndustrySceneCommon().mini_inside == "1", reason="小程序内部环境不支持此用例")`**实现逻辑

**`@pytest.mark.skip`**实现逻辑

**`fixture`作为参数传递**







# 二十三、经典例子

**用下面的例子，我们可以稍微了解一下，他们的调用流程**

```python
# test_inter.py
class TestInter(object):

    def test_inter_sub_one(self):
        """
        这是一段多行注释
        """
        print('\033[1;45m test_inter_sub_one \033[0m')

    def test_inter_sub_two(self):
        print('\033[1;45m test_inter_sub_two \033[0m')

    def test_inter_sub_three(self):
        print('\033[1;45m test_inter_sub_three \033[0m')

    def test_inter_sub_four(self):
        print('\033[1;45m test_inter_sub_four \033[0m')


# conftest.py
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    print('------------------------------------')
    # 获取钩子方法的调用结果
    out = yield
    print('用例执行结果', out)					#<pluggy.callers._Result object at 0x000001CC4ECFB908>

    # 3. 从钩子方法的调用结果中获取测试报告
    report = out.get_result()
    print('用例对象', item)						#<Function test_inter_sub_one>
    print('测试报告：%s' % report)				#<Function test_inter_sub_four>
    print('report对象属性', report.__dict__)	
    """
    {'nodeid': 'test_inter.py::TestInter::test_inter_sub_one', 'location': ('test_inter.py', 12, 'TestInter.test_inter_sub_one'), 'keywords': {'test_inter_sub_one': 1, '()': 1, '接口脚本': 1, 'test_inter.py': 1, 'TestInter': 1}, 'outcome': 'passed', 'longrepr': None, 'when': 'call', 'user_properties': [], 'sections': [], 'duration': 0.0}
    """
    
    print('步骤：%s' % report.when)			# call 
    print('nodeid：%s' % report.nodeid)		 # D:/interface/接口测试/test_inter.py::TestInter::test_inter_sub_one
    print('测试用例函数', item.function)		  # <function TestInter.test_inter_sub_one at 0x0000014C14A236A8>
    print('description:%s' % str(item.function.__doc__))	# 这是一段多行注释
    print(('运行结果: %s' % report.outcome))				# passed
    print('3', item.session.__dict__)
    """
    {'fspath': local('D:\\origin\\学习代码\\interface_auto\\src\\api_case'), 'name': 'api_case', 'parent': None, 'config': <_pytest.config.Config object at 0x000001F6EA6C4EB8>, 'session': <Session api_case exitstatus=<ExitCode.OK: 0> testsfailed=0 testscollected=7>, 'keywords': <NodeKeywords for node <Session api_case exitstatus=<ExitCode.OK: 0> testsfailed=0 testscollected=7>>, 'own_markers': [], 'extra_keyword_matches': set(), '_name2pseudofixturedef': {}, '_nodeid': '', 'testsfailed': 0, 'testscollected': 7, 'shouldstop': False, 'shouldfail': False, 'trace': <pluggy._tracing.TagTracerSub object at 0x000001F6EB755550>, '_norecursepatterns': ['.*', 'build', 'dist', 'CVS', '_darcs', '{arch}', '*.egg', 'venv'], 'startdir': local('D:\\origin\\学习代码\\interface_auto\\src\\api_case'), '_initialpaths': frozenset({local('D:\\origin\\学习代码\\interface_auto\\src\\api_case')}), '_node_cache': {local('D:\\origin\\学习代码\\interface_auto\\src\\__init__.py'): [<Package D:\origin\学习代码\interface_auto\src>], (<class '_pytest.python.Module'>, local('D:\\origin\\学习代码\\interface_auto\\src\\api_case\\接口脚本\\test_inter.py')): <Module 接口脚本/test_inter.py>, (<class '_pytest.python.Module'>, local('D:\\origin\\学习代码\\interface_auto\\src\\api_case\\接口脚本\\test_inter_two.py')): <Module 接口脚本/test_inter_two.py>}, '_bestrelpathcache': _bestrelpath_cache(path=local('D:\\origin\\学习代码\\interface_auto\\src\\api_case')), '_pkg_roots': {local('D:\\origin\\学习代码\\interface_auto\\src'): <Package D:\origin\学习代码\interface_auto\src>, local('D:\\origin\\学习代码\\interface_auto\\src\\api_case\\演示脚本'): <Package D:\origin\学习代码\interface_auto\src\api_case\演示脚本>}, 'exitstatus': <ExitCode.OK: 0>, '_fixturemanager': <_pytest.fixtures.FixtureManager object at 0x000001F6EB755240>, '_setupstate': <_pytest.runner.SetupState object at 0x000001F6EB773400>, '_notfound': [], '_initialparts': [[local('D:\\origin\\学习代码\\interface_auto\\src\\api_case')]], 'items': [<Function test_inter_sub_one>, <Function test_inter_sub_two>, <Function test_inter_sub_three>, <Function test_inter_sub_four>, <Function test_inter_sub_five>, <Function test_inter_sub_six>, <Function test_demo_sub_two>]}
    """
    print('4', item.config)		#<_pytest.config.Config object at 0x000001F6EA6C4EB8>
    print('5', item.parent)		# <Instance ()>
    print('6', item.nodeid)		# 接口脚本/test_inter.py::TestInter::test_inter_sub_one (命名， 我们可以修改，他的命名， 也可以修改ids中文的问题)
    print('7', item.session.items)
    """
   [<Function test_inter_sub_one>, <Function test_inter_sub_two>, <Function test_inter_sub_three>, <Function test_inter_sub_four>] 
    """
    
    
    print('8', item.session.items[0].__dict__)
    """
    {'name': 'test_inter_sub_one', 'parent': <Instance ()>, 'config': <_pytest.config.Config object at 0x000001F6EA6C4EB8>, 'session': <Session api_case exitstatus=<ExitCode.OK: 0> testsfailed=0 testscollected=7>, 'fspath': local('D:\\origin\\学习代码\\interface_auto\\src\\api_case\\接口脚本\\test_inter.py'), 'keywords': <NodeKeywords for node <Function test_inter_sub_one>>, 'own_markers': [], 'extra_keyword_matches': set(), '_name2pseudofixturedef': {}, '_nodeid': '接口脚本/test_inter.py::TestInter::test_inter_sub_one', '_report_sections': [], 'user_properties': [], '_args': None, '_obj': <bound method TestInter.test_inter_sub_one of <test_inter.TestInter object at 0x000001F6EB7C5F98>>, '_fixtureinfo': FuncFixtureInfo(argnames=(), initialnames=('_session_faker',), names_closure=['_session_faker', 'request'], name2fixturedefs={'_session_faker': (<FixtureDef argname='_session_faker' scope='session' baseid=''>,)}), 'fixturenames': ['_session_faker', 'request'], 'funcargs': {'_session_faker': <faker.proxy.Faker object at 0x000001F6EB7C5EB8>, 'request': <FixtureRequest for <Function test_inter_sub_one>>}, '_request': <FixtureRequest for <Function test_inter_sub_one>>, 'originalname': None, '_location': ('接口脚本\\test_inter.py', 12, 'TestInter.test_inter_sub_one'), 'catch_log_handlers': {'setup': <LogCaptureHandler (NOTSET)>, 'call': <LogCaptureHandler (NOTSET)>}, 'catch_log_handler': <LogCaptureHandler (NOTSET)>, '_skipped_by_mark': False, '_evalxfail': <_pytest.mark.evaluate.MarkEvaluator object at 0x000001F6EB7C5F60>}
    """
    
    print('9', item.session)	# <Session api_case exitstatus=<ExitCode.OK: 0> testsfailed=0 testscollected=7>
    print('10', item.session.items[0].session)	# <Session api_case exitstatus=<ExitCode.OK: 0> testsfailed=0 testscollected=7>
    
    print('11', item.__dict__) # item.__dict__ == item.session.items[0].__dict__
    """
    {'name': 'test_inter_sub_one', 'parent': <Instance ()>, 'config': <_pytest.config.Config object at 0x000001F6EA6C4EB8>, 'session': <Session api_case exitstatus=<ExitCode.OK: 0> testsfailed=0 testscollected=7>, 'fspath': local('D:\\origin\\学习代码\\interface_auto\\src\\api_case\\接口脚本\\test_inter.py'), 'keywords': <NodeKeywords for node <Function test_inter_sub_one>>, 'own_markers': [], 'extra_keyword_matches': set(), '_name2pseudofixturedef': {}, '_nodeid': '接口脚本/test_inter.py::TestInter::test_inter_sub_one', '_report_sections': [], 'user_properties': [], '_args': None, '_obj': <bound method TestInter.test_inter_sub_one of <test_inter.TestInter object at 0x000001F6EB7C5F98>>, '_fixtureinfo': FuncFixtureInfo(argnames=(), initialnames=('_session_faker',), names_closure=['_session_faker', 'request'], name2fixturedefs={'_session_faker': (<FixtureDef argname='_session_faker' scope='session' baseid=''>,)}), 'fixturenames': ['_session_faker', 'request'], 'funcargs': {'_session_faker': <faker.proxy.Faker object at 0x000001F6EB7C5EB8>, 'request': <FixtureRequest for <Function test_inter_sub_one>>}, '_request': <FixtureRequest for <Function test_inter_sub_one>>, 'originalname': None, '_location': ('接口脚本\\test_inter.py', 12, 'TestInter.test_inter_sub_one'), 'catch_log_handlers': {'setup': <LogCaptureHandler (NOTSET)>, 'call': <LogCaptureHandler (NOTSET)>}, 'catch_log_handler': <LogCaptureHandler (NOTSET)>, '_skipped_by_mark': False, '_evalxfail': <_pytest.mark.evaluate.MarkEvaluator object at 0x000001F6EB7C5F60>}
    
    """
    
    print('12', dir(item))
    """
    ['_ALLOW_MARKERS', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_args', '_evalxfail', '_fixtureinfo', '_getobj', '_initrequest', '_location', '_name2pseudofixturedef', '_nodeid', '_obj', '_prunetraceback', '_pyfuncitem', '_report_sections', '_repr_failure_py', '_request', '_skipped_by_mark', 'add_marker', 'add_report_section', 'addfinalizer', 'catch_log_handler', 'catch_log_handlers', 'cls', 'config', 'extra_keyword_matches', 'fixturenames', 'fspath', 'funcargnames', 'funcargs', 'function', 'get_closest_marker', 'getmodpath', 'getparent', 'ihook', 'instance', 'iter_markers', 'iter_markers_with_node', 'keywords', 'listchain', 'listextrakeywords', 'listnames', 'location', 'module', 'name', 'nextitem', 'nodeid', 'obj', 'originalname', 'own_markers', 'parent', 'reportinfo', 'repr_failure', 'runtest', 'session', 'setup', 'teardown', 'user_properties', 'warn']
    
    """
item == item.session.items[0-N]中的具体某一个
    
item.nodeid==test_inter_two.py::TestInterTwo::test_inter_two_TestInterTwo_sub_two[密码-账号]
item.name = test_inter_two_TestInterTwo_sub_two[密码-账号]
🔺这个中文终端显示有异常，我们可以这样
item.nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')
item.name = item.name.encode('utf-8').decode('unicode-escape')   

其实要再终端显示正常，我们一般是再def pytest_collection_modifyitems(items):中修改，其他地方就不需要改动了
def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for each in items:
        each.name = each.name.encode("utf-8").decode("unicode_escape")
        each._nodeid = each.nodeid.encode("utf-8").decode("unicode_escape") # 这里必须定义each._nodeid不然报错
        print(each.name, 11111111111, each._nodeid)    





🔺因为没用例没有设置setup 和 teardown ,所以都是默认通过的
🔺用例和pytest_runtest_makereport的关系是： 先执行用例，用例执行完毕通过next激活pytest_runtest_makereport， 然后再通过send将执行结果报告发给pytest_runtest_makereport，使用out变量来接收

例子二：验证用例和夹具的执行先后顺序
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


🔺@pytest.fixture 装饰的夹具，比用例更早执行，所以如果我们采用@pytest.fixture来实现前后置，@pytest.fixture装饰的夹具中yield前面的代码执行完以后才开始执行用例，用例执行完毕以后通过next激活@pytest.fixture装饰的夹具， 然后再通过send将执行结果报告发给pytest_runtest_makereport，使用out变量来接收
```

🔺🔺🔺🔺🔺🔺🔺🔺🔺`request 是 pytest 的内置 fixture ， "为请求对象提供对请求测试上下文的访问权🔺`

**🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺测试类中不能出现`def __init__`, 尤其是在使用继承的时候**



