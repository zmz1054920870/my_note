# 性能测试-Locust脚本加强篇(关联、检查点、集合点)



## 1、关联：通常在业务流程中有很多一系列的接口调用，从后面的接口依赖前边接口的结果数据

```python
from lxml import etree
from locust import TaskSet, task, HttpUser
class UserBehavior(TaskSet):
    @staticmethod
    def get_session(html):
        tree = etree.HTML(html)
        return tree.xpath("//div[@class='btnbox']/input[@name='session']/@value")[0] \
    @task(10)
    def test_login(self):
        html = self.client.get('/login').text
        username = 'user@compay.com'
        password = '123456'
        session = self.get_session(html)
        payload = { 'username': username, 'password': password, 'session': session }
        self.client.post('/login', data=payload)

class WebsiteUser(HttpUser):
    host = 'http://debugtalk.com'
    # task_set = UserBehavior
    tasks = [UserBehavior ]
    min_wait = 1000
    max_wait = 3000

```





## 2、**检查点**：用来判断返回值是否符合要求

```python
from lxml import etree
from locust import TaskSet, task, HttpUser
class UserBehavior(TaskSet):
    @staticmethod
    def get_session(html):
        tree = etree.HTML(html)
        return tree.xpath("//div[@class='btnbox']/input[@name='session']/@value")[0] \
    @task(10)
    def test_login(self):
        html = self.client.get('/login').text
        assert "200" in html
        username = 'user@compay.com'
        password = '123456'
        session = self.get_session(html)
        payload = { 'username': username, 'password': password, 'session': session }
        self.client.post('/login', data=payload)

class WebsiteUser(HttpUser):
    host = 'http://debugtalk.com'
    # task_set = UserBehavior
    tasks = [UserBehavior ]
    min_wait = 1000
    max_wait = 3000
```



## 3、集合点：提高某个接口的并发度，当所有用户运行到指定位置后集合等待，同时向下执行

```python
from gevent._semaphore import Semaphore
from locust import TaskSet, events
from lxml import etree

all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()
def on_hatch_complete(**kwargs):
    all_locusts_spawned.release() # 创建钩子方法

events.hatch_complete += on_hatch_complete # 挂载到locust钩子函数（所有的Locust实例产生完成时触发）

class TestTask(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        all_locusts_spawned.wait() # 限制在所有用户准备完成前处于等待状态
        self.login()

    @staticmethod
    def get_session(html):
        tree = etree.HTML(html)
        return tree.xpath("//div[@class='btnbox']/input[@name='session']/@value")[0] \

    def login(self):
        html = self.client.get('/login').text
        username = 'user@compay.com'
        password = '123456'
        session = self.get_session(html)
        payload = {'username': username, 'password': password, 'session': session}
        self.client.post('/login', data=payload)
```

