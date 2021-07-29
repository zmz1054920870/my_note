# locust压力测试——3种方式实现访问需要权限验证的接口（API）



### 第一种：我们登录一次拿到需要（Seesion会给我保存登录回话）

```python

from locust import HttpLocust, TaskSet, task
from locust.clients import HttpSession
import json
import hashlib   #python md5加密方法
 
# Web性能测试
class UserBehavior(TaskSet):
            
    def _login(self):    
        #密码加密:
        mima='91*****li'
        Jpwd = hashlib.md5()        #创建一个MD5对象
        Jpwd.update(mima.encode('utf-8')) 
        Npwd = Jpwd.hexdigest()         
        # print (Npwd)  
          
        self.head = {'Content-Type':'application/json',     #这个类型说明服务端接收json格式的字符串
                    'Connection': 'keep-alive',
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',            
                     }
                      
        self.form_data = {'signin_name':158******18,  #如果这里不是数字，就用加引号。例如'signin_name':'lily'
                          'password':Npwd}   #注意这里不需要给Npwd加引号
                                                                                  
        response=self.client.post("/api/account/team/signin",headers = self.head,json= self.form_data))    #这里对data进行转换，主要看Content-Type类型
        print("Response status code:", response.status_code)
        # print(response.content)     
    
    def on_start(self):
        '''任务开始准备工作：只登录一次.'''
        self._login()     
 
        
    # 任务1-任务-我参与的任务
    @task(1)
    def mytask(self):
        print("---访问页面-任务-我参与的任务---")
        r = self.client.get("/api/tasks/5d7851951647bf27375e3236?t=1568883989140")
        assert "首页底部公司介绍" in r.text    
 
    # 任务2-任务-通讯录     
    @task(3)
    def contacts(self):
        print("---访问页面-通讯录---")
        r = self.client.get("/api/departments/tree?async=false&t=1568884732067")
        print(r.text)
        assert "产品部" in r.text   
     
class User(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 3000                       #任务执行间隔1-3s
    # host="https://zhlh.xxxxxx.com"    #执行命令：locust -f zhlh.py
    
    
# 用下面的方法，就要把上面的host注释掉   #执行命令：python zhlh.py
if __name__ == "__main__":
    import os
    os.system("locust -f zhlhuser.py --host=https://zhlh.xxxxxx.com") 
```





### 第二种：针对那种只允许一个账号登录的情况的时候，我们可以直接F12抓包，将登录验证消息copy下来，每次请求接口带上这个数据

```python

header = {
            'accept-encoding': "gzip",
            'authorization': "Bearer Kn5mFk9icFibM2-sjfVtykLtUA0kqKgXV_ARsKB091J3fob_tzFuqqWM6dbc-zNuga9fQQeObQPgWZKI0LDTx9uUGpv3JNhfc4RAPD5lSobu4eMlu7JLfKnwsGDto4m96wpMBYR0Dg6tAx-ANZHth7pdz1hUGml3Jw33RDFPy_Xk_b6jm92eU2AbavTcmMjLa2ga1oSWJswE8CAM4j9wIkFQLem50mi5R_JkWgl4rf7yutpo1PADGkEzI_DUr5Fl",
            'connection': "Keep-Alive",
            'user-agent': "okhttp/3.12.1",            
        }
       
class UserBehavior(TaskSet):
    # 任务1-我的会员专区
    @task(1)
    def huiyuan_my(self):
        print("---访问页面-会员专区---")
        r = self.client.get("/api/CAccount/GetUserInfo",headers=header)
        assert "李莉莉" in r.text  #断言，列表中应该有的名字           
        print("Response status code:", r.status_code)
```

### 

### 第三种：就是提取token或者cookie，然后传入