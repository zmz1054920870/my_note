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
import time
import os
from locust import User, constant, task, HttpUser, LoadTestShape,SequentialTaskSet, TaskSet, events
from locust.contrib.fasthttp import FastHttpUser
from gevent._semaphore import Semaphore
from json import JSONDecodeError
# sem = Semaphore()
# sem.acquire()

all_locusts_spawned1 = Semaphore()
all_locusts_spawned1.acquire()

def on_hatch_complete(**kwargs):
    all_locusts_spawned1.release()

events.spawning_complete.add_listener(on_hatch_complete())


class MyBehavior(TaskSet):

    def on_start(self):
        print('开搞')
        
    @task(1)
    def userBehavior(self):
        url = 'http://192.168.0.118:2333/inspirer/new'
        data = {
            'content': '%d' % time.time(),
            'ximg': ''
        }
        header = {'token': '669edd66e72c16aee6b1b769zmzjldecc21091b3283e95'}
        all_locusts_spawned1.wait()
        with self.client.post(url=url, json=data, headers=header, catch_response=True) as response:
            try:
                data = response.json()
                if data['status'] == 200:
                    response.success()
            except JSONDecodeError as e:
                response.failure('报错')
            # self.environment.runner.quit()

class WebsitUser(HttpUser):
    wait_time = constant(1)
    host = ''
    tasks = [MyBehavior, ]

if __name__ == '__main__':
    os.system('locust -f locutfile_task -u 100 -r 20 --headless')
```

