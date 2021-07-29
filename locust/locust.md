# locust

### 特定

```html
1.分布式执行,配置master和slave(主从机器),在对台机器上对系统持续发起请求
2.基于事件驱动,与其他工具使用进程来模拟用户不同，locust借助了gevent库对协程的支持，可以达到更高数量级的并发
3.不支持监控被测机，需要配合其他工具辅助
```



#### 注意

```
每一个模拟用户会，每次会选择一个被@task标记的行为，然后执行。执行完毕以后，等待一定时间，然后再次随机选择一个被@task标记的行为，进行执行。   特别特别特别注意了， 不是一开始就分配好，每个用户指定执行哪一个用户行为
```



### 官方推荐层级结构

```
Project root

common

​    __init__.py

​    auth.py

​    config.py

​    locustfile.py

​    requirements.txt (外部Python依赖关系通常保存在requirements.txt中)
​    
​    
 ===========================================
#具有多个不同locustfiles的项目也可以将它们保存在单独的子目录中：
Project root

common/

​    __init__.py

​    auth.py

​    config.py

​    locustfiles/

​    api.py

​    website.py

​    requirements.txt
```



#### locust的User类与TaskSet类的关系

```python
from locust import HttpUser, TaskSet, constant

class WebsiteBehavior(TaskSet):
        @task(1)
    def userBehavior(self):
        print(2)
        url = 'http://192.168.0.118:2333/inspirer/new'
        data = {
            'content': '%d' % time.time(),
            'ximg': ''
        }
        header = {'token': '5904d7feed3f407219717837zmzjl0bd70820fc8b995ec'}
        res = self.client.post(url=url, json=data, headers=header)

class WebsitUser(HttpUser):
    wait_time = constant(1)
    host = ''
    tasks = [MyBehavior, ]
```

**🔺：locust将为正在模拟的每一个用户产生一个基础于User类的实例。所以WebsitUser(HttpUser)是必须的，用他来产生用户实例。User实例会在tasks属性中选择一个TaskSet执行。继承于TaskSet的客户端来源于HttpUser,我们也可以自定义个客户端，这个客户端必须继承于User或者HttpUser（实际上就是继承于User，因为HttpUser也是继承于User的。）**如下：self.client属性，指向我们自定义的客户端即可

```python
class GrpcLocust(Us):
    def __init__(self, *args, **kwargs):
        super(GrpcLocust, self).__init__(*args, **kwargs)
        self.client = WsClient()
```







### locust的 `__init__` 文件

```python
from .event import Events

events = Events() #  导入events的时候，实际上是导入的Events的一个实例

__version__ = "1.4.4"
__all__ = (
    "SequentialTaskSet",
    "wait_time",
    "task",
    "tag",
    "TaskSet",
    "HttpUser",
    "User",
    "between",
    "constant",
    "constant_pacing",
    "events",
    "LoadTestShape",
)

# Used for raising a DeprecationWarning if old Locust/HttpLocust is used
from .util.deprecation import DeprecatedLocustClass as Locust
from .util.deprecation import DeprecatedHttpLocustClass as HttpLocust
```

**证明我们只能导入上面的这些方法、类、属性**

#### 启动参数

```bash
locust --help
Common options:
  -h, --help            show this help message and exit
  -f LOCUSTFILE, --locustfile LOCUSTFILE
                        Python module file to import, e.g. '../other.py'.
                        Default: locustfile
  --config CONFIG       Config file path
  -H HOST, --host HOST  Host to load test in the following format:
                        http://10.21.32.33
  -u NUM_USERS, --users NUM_USERS
                        Number of concurrent Locust users. Primarily used
                        together with --headless. Can be changed during a test
                        by inputs w, W(spawn 1, 10 users) and s, S(stop 1, 10
                        users)
  -r SPAWN_RATE, --spawn-rate SPAWN_RATE
                        The rate per second in which users are spawned.
                        Primarily used together with --headless
  -t RUN_TIME, --run-time RUN_TIME
                        Stop after the specified amount of time, e.g. (300s,
                        20m, 3h, 1h30m, etc.). Only used together with
                        --headless. Defaults to run forever.
  -l, --list            Show list of possible User classes and exit

Web UI options:
  --web-host WEB_HOST   Host to bind the web interface to. Defaults to '*'
                        (all interfaces)
  --web-port WEB_PORT, -P WEB_PORT
                        Port on which to run web host
  --headless            Disable the web interface, and instead start the load
                        test immediately. Requires -u and -t to be specified.
  --web-auth WEB_AUTH   Turn on Basic Auth for the web interface. Should be
                        supplied in the following format: username:password
  --tls-cert TLS_CERT   Optional path to TLS certificate to use to serve over
                        HTTPS
  --tls-key TLS_KEY     Optional path to TLS private key to use to serve over
                        HTTPS

Master options:
  Options for running a Locust Master node when running Locust distributed. A Master node need Worker nodes that connect to it before it can run load tests.

  --master              Set locust to run in distributed mode with this
                        process as master
  --master-bind-host MASTER_BIND_HOST
                        Interfaces (hostname, ip) that locust master should
                        bind to. Only used when running with --master.
                        Defaults to * (all available interfaces).
  --master-bind-port MASTER_BIND_PORT
                        Port that locust master should bind to. Only used when
                        running with --master. Defaults to 5557.
  --expect-workers EXPECT_WORKERS
                        How many workers master should expect to connect
                        before starting the test (only when --headless used).

Worker options:

  Options for running a Locust Worker node when running Locust distributed.
  Only the LOCUSTFILE (-f option) need to be specified when starting a Worker, since other options such as -u, -r, -t are specified on the Master node.

  --worker              Set locust to run in distributed mode with this
                        process as worker
  --master-host MASTER_NODE_HOST
                        Host or IP address of locust master for distributed
                        load testing. Only used when running with --worker.
                        Defaults to 127.0.0.1.
  --master-port MASTER_NODE_PORT
                        The port to connect to that is used by the locust
                        master for distributed load testing. Only used when
                        running with --worker. Defaults to 5557.

Tag options:
  Locust tasks can be tagged using the @tag decorator. These options let specify which tasks to include or exclude during a test.

  -T [TAG [TAG ...]], --tags [TAG [TAG ...]]
                        List of tags to include in the test, so only tasks
                        with any matching tags will be executed
  -E [TAG [TAG ...]], --exclude-tags [TAG [TAG ...]]
                        List of tags to exclude from the test, so only tasks
                        with no matching tags will be executed

Request statistics options:
  --csv CSV_PREFIX      Store current request stats to files in CSV format.
                        Setting this option will generate three files:
                        [CSV_PREFIX]_stats.csv, [CSV_PREFIX]_stats_history.csv
                        and [CSV_PREFIX]_failures.csv
  --csv-full-history    Store each stats entry in CSV format to
                        _stats_history.csv file. You must also specify the '--
                        csv' argument to enable this.
  --print-stats         Print stats in the console
  --only-summary        Only print the summary stats
  --reset-stats         Reset statistics once spawning has been completed.
                        Should be set on both master and workers when running
                        in distributed mode
  --html HTML_FILE      Store HTML report file

Logging options:
  --skip-log-setup      Disable Locust's logging setup. Instead, the
                        configuration is provided by the Locust test or Python
                        defaults.
  --loglevel LOGLEVEL, -L LOGLEVEL
                        Choose between DEBUG/INFO/WARNING/ERROR/CRITICAL.
                        Default is INFO.
  --logfile LOGFILE     Path to log file. If not set, log will go to
                        stdout/stderr

Other options:
  --show-task-ratio     Print table of the User classes' task execution ratio
  --show-task-ratio-json
                        Print json data of the User classes' task execution
                        ratio
  --version, -V         Show program's version number and exit
  --exit-code-on-error EXIT_CODE_ON_ERROR
                        Sets the process exit code to use when a test result
                        contain any failure or error
  -s STOP_TIMEOUT, --stop-timeout STOP_TIMEOUT
                        Number of seconds to wait for a simulated user to
                        complete any executing task before exiting. Default is
                        to terminate immediately. This parameter only needs to
                        be specified for the master process when running
                        Locust distributed.

User classes:
  UserClass             Optionally specify which User classes that should be
                        used (available User classes can be listed with -l or
                        --list)

```







#### 问题：

```
To add/remove users during a headless run press w or W (1, 10) to spawn users and s or S to stop(1, 10)  怎么实现呢
```

**解决**

`在web ui模式下，我们可以在STATUS下面的Edit中实时的增加和减少新用户 `



#### 问题2：environment 怎么使用







## Write a locustfile

### User Class

#### 	weight

```python
#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : demo02.py

import time
from locust import HttpUser, task, between


class QuickStartUser(HttpUser):
    weight = 1 	#🔺给用户类添加权限

    wait_time = between(1, 2) #🔺 wait_time 属性constant、between、constant_pacing

    # @tag
    @task		#给用户behavior（行为）添加权限为1
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

    # @task(3)	#给用户behavior（行为）添加权限为3
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(5)

    def on_start(self):
        print("每次请求都会执行-one")
        self.client.post("/login", json={"username": "foo", "password": "bar"})

class QuickStarUserTwo(HttpUser):
    weight=3
    @task
    def view_items(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")
            time.sleep(5)

    def on_start(self):
        print("每次请求都会执行--two")
        self.client.post("/login", json={"username": "foo", "password": "bar"})


if __name__ == '__main__':
    import os
    os.system("locust -f demo02.py -H https://www.baidu.com -u 10 -r 1 --headless QuickStarUserTwo QuickStartUser")
```





```python
os.system("locust -f demo02.py -H https://www.baidu.com -u 10 -r 1 --headless QuickStarUserTwo QuickStartUser")

#解释： 执行demo02.py这个locustfile来压测host为https://www.baidu.com的接口， 总共产生10个用户，每秒增加一个用户， 并不使用webui界面，采用headless界面， 用户实例由QuickStarUserTwo QuickStartUser这两个用户类产生
```



#### on_start and on_stop 方法

```python
Users (and TaskSets) can declare an on_start method and/or on_stop method. A User will call its on_start method when it starts running, and its on_stop method when it stops running. For a TaskSet, the on_start method is called when a simulated user starts executing that TaskSet, and on_stop is called when the simulated user stops executing that TaskSet (when interrupt() is called, or the user is killed).

用户（和tasksets）可以声明on_start方法和/或on_stop方法。当用户在开始运行时，用户将调用其on_start方法，并且当它停止运行时它的on_stop方法。对于一个TaskSet，当模拟的用户开始执行TaskSet时调用on_start方法，并且当模拟的用户停止执行该taskset时调用on_stop（当调用中断（）或者用户被杀死时）
```





#### wait_time  属性

**自定义wait_time属性**

`我们可以在继承于HttpUser 或者 User的类里面自定义我们自己的时间规则,也可以到源码里面去添加，但是不建议,类里面添加例子如下`

```python
class QuickStartUser(HttpUser):

    host = "http://www.baidu.com"

    last_wait_time = 0

    def wait_time(self):
        self.last_wait_time += 1
        print(self.last_wait_time)
        return self.last_wait_time

    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")
 if __name__ == '__main__':
    import os
    os.system("locust -f demo02.py -u 100 -r 1 QuickStartUser")

"""
实现原理如下：

"""

#我们参看locust源码发现，他的等待时间都是调用的一个函数，比如between、constant、constant_pacing,这些函数在返回一个模拟函数，传给wait_time属性（这里我们要明白一点，在类中方法也是类的属性），然后locust会去调用这个随机函数，所以我们必须在QuickStartUser(HttpUser)定义一个函数，跟wait_times属性重名

#源码如下： 他们都是返回了一个函数(随机函数)，供后面调用，在后面调用的时候是没有传值的，所以我们在QuickStartUser(HttpUser)必须定义个函数，且不能传值
import random
from time import time


def between(min_wait, max_wait):
    """
    Returns a function that will return a random number between min_wait and max_wait.

    Example::

        class MyUser(User):
            # wait between 3.0 and 10.5 seconds after each task
            wait_time = between(3.0, 10.5)
    """
    return lambda instance: min_wait + random.random() * (max_wait - min_wait)


def constant(wait_time):
    """
    Returns a function that just returns the number specified by the wait_time argument

    Example::

        class MyUser(User):
            wait_time = constant(3)
    """
    return lambda instance: wait_time
```





#### tasks 属性

```python
tasks: List[Union[TaskSet, Callable]] = []
```

```python
from locust import HttpUser, constant

def hello_world(self):
    self.client.get("/hello")
    self.client.get("/world")

class MyUser(HttpUser):
    tasks = [hello_world: 3]
    wait_time = constant(1)
    
#通过这样的方式我们也可以指定我们的用户类，当然前面的@task一样可以，灵活运用把

#🔺还可以在tasks里面添加权重比如 [hello_world:3], 数字3就是他的权重
```

#### abstract属性

```python
class WebSiteUser(HttpUser):
    wait_time = constant(1)
    # tasks = [WebSiteBehavior, ]
    abstract = False
    host = 'http://192.168.0.118:8080/'
    tasks = [WebSiteBehavior, ]
    @task(1)
    def web_delete(self):
        with self.client.post('/delete', catch_response=True) as res:
            if res.status_code > 400:
                res.success()
            else:
                res.failure('delete错误')
                
os.system('locust -f locust_demo.py -u 20 -r 1')

》》》[2021-05-09 23:23:00,716] DESKTOP-IVHSPRM/ERROR/locust.main: No User class found!
```

🔺前提条件：当一个locustfile.py文件里面只有一个HttpUser或者User类的时候

- ​	当abstract = False的时候，该HttpUser类不会被执行，会报出No User class found!

🔺前提条件：当一个locustfile里面有两个或者以上HttpUser或者User类的时候

- ​    当abstract = False的时候，该HttpUser或者 User类将会被执行
- ​    当abstract = True的时候，该HttpUser或者 User类将会被忽略

```

```



### Events

**如果要将一些设置代码作为测试的一部分运行，则通常将其放在locustfile的模块级别，但有时您需要在运行中特定时间进行事项。对于这种需求，locust提供事件钩。**



###### test_start and test_stop

```
在启动压测的和结束压测的时候，运行一些代码，我们可以使用test_start and test_stop， 我们还可以在Locustfile的模块级别设置这些事件的侦听器。
🔺当我们进行分布式压测的时候，test_start 和 test_stop 只会在master主节点中被触发
🔺0.14版本以前使用setup和teardown来完成相同的工作
```

###### e.g

```python
from locust import events
"""
🔺 events = Events() ,在locust的__init__文件中被定义
"""

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("A new test is starting")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("A new test is ending")
```



###### 其他的钩子

**解释：就是要正确传参，才能有效**

1. 自定义客户端的几个钩子

```python
request_success: EventHook
"""
在请求成功完成时激发。此事件通常用于在为locust编写自定义客户端时报告请求
"""

    Event arguments:
    :param request_type: Request type method used
    :param name: Path to the URL that was called (or override name if it was used in the call to the client)
    :param response_time: Response time in milliseconds
    :param response_length: Content-length of the response
            
====================================================================
request_failure: EventHook
"""
在请求失败的时候激发。此事件通常用于在为locust编写自定义客户端时报告请求
"""
    Event arguments:
    :param request_type: Request type method used
    :param name: Path to the URL that was called (or override name if it was used in the call to the client)
    :param response_time: Time in milliseconds until exception was thrown
    :param response_length: Content-length of the response
    :param exception: Exception instance that was thrown
```



2. 集合事件

```python
spawning_complete: EventHook
    """
    Fired when all simulated users has been spawned
    在所有模拟用户生成完成以后激活
    """
    Event arguments:
    :param user_count: Number of users that were spawned
    
```



### Validating responses（自定义验证成功和失败）

```python
with self.client.get("/", catch_response=True) as response:
    if response.text != "Success":
        response.failure("Got wrong response")
    elif response.elapsed.total_seconds() > 0.5:
        response.failure("Request took too long")
```

> ​	**🔺说明：**
>
> - 必须采用with ... as ... 语法，不然定义无效





### SequentialTaskSet

**作用： 在locust中用户（线程）执行任务是随机的，如果需要让任务执行有一定顺序则可以将taskset继承SequentialTaskSet 类来实现。模拟用户会按顺序挑选任务执行。**

###### 源码：他是继承于TaskSet

```python
class SequentialTaskSet(TaskSet, metaclass=SequentialTaskSetMeta):
    """
    Class defining a sequence of tasks that a User will execute.

    Works like TaskSet, but task weight is ignored, and all tasks are executed in order. Tasks can
    either be specified by setting the *tasks* attribute to a list of tasks, or by declaring tasks
    as methods using the @task decorator. The order of declaration decides the order of execution.

    It's possible to combine a task list in the *tasks* attribute, with some tasks declared using
    the @task decorator. The order of declaration is respected also in that case.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._task_index = 0

    def get_next_task(self):
        if not self.tasks:
            raise LocustError(
                "No tasks defined. use the @task decorator or set the tasks property of the SequentialTaskSet"
            )
        task = self.tasks[self._task_index % len(self.tasks)]
        self._task_index += 1
        return task
```



###### 顺序执行几次

> - ​	task(number)中的number在SequentialTaskSet中表示，顺序执行几次

**例子如下**

:表示get_something执行一次后，delete_something执行2次，然后login_something执行3次，依次循环

```python
import os
from locust import HttpUser, TaskSet, task, constant, SequentialTaskSet


class WebsiteBehavior(SequentialTaskSet):

    @task(1)
    def get_something(self):
        print(1)
    @task(2)
    def delete_something(self):
        print(2)

    @task(3)
    def login_something(self):
        print(3)
class WebsiteUser(HttpUser):
    wait_time = constant(1)
    tasks = [WebsiteBehavior, ]
    host = 'http://192.168.0.118:8080/'

if __name__ == '__main__':
    os.system('locust -f locust_demo02.py -u 1 -r 1')
```

**输入结果如下:**

```python
[2021-05-13 07:41:06,345] DESKTOP-IVHSPRM/INFO/locust.main: Starting Locust 1.4.4
[2021-05-13 07:41:06,359] DESKTOP-IVHSPRM/INFO/root: Terminal was not a tty. Keyboard input disabled
[2021-05-13 07:41:10,794] DESKTOP-IVHSPRM/INFO/locust.runners: Spawning 1 users at the rate 1 users/s (0 users already running)...
[2021-05-13 07:41:10,794] DESKTOP-IVHSPRM/INFO/locust.runners: All users spawned: WebsiteUser: 1 (1 total running)
1
2
2
3
3
3
1
2
2
3
3
3
```

