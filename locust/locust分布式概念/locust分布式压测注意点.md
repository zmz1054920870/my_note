# Locust性能测试II分布式压测



## 准备Master和Slave

#### 主从压测运行必备条件：

- Master机器和Slave机器都要准备运行脚本的环境（python、locust等）
- Master负责分发任务Slave机器负责执行脚本，因此网络通信必备
- Master只运行Web系统用于分发和监控数据，不模拟任何用户量
- Master机器和Slave机器都要有压测脚本



#### 在Master机器上启动locust

```python
locust -f D:\PythonPrograms\PerformanceLocust\LeadsCloud\Leadscloud.py --master --host=https://admin.leadscloud.com/Front-Vue
[2019-11-07 11:50:05,183] daiveyang/INFO/locust.main: Starting web monitor at *:8089
[2019-11-07 11:50:05,201] daiveyang/INFO/locust.main: Starting Locust 0.12.2
```

在Slave机器上启动locust
locust -f Leadscloud.py --worker--master-host=192.168.74.8 --host=https://admin.leadscloud.com/Front-Vue

配置成功后的状态
当Master和Slave都启动后，在Master机器的控制台中能够看到
[2019-11-07 11:51:48,797] daiveyang/INFO/locust.runners: Client 'DESKTOP-PN1TIDS_1a8012047bf74c33b6f9545d865b374a' reported as ready. Currently 1 clients ready to swarm.

localhost:8089



#### 分布式执行

> - ​	同一份代码通过多个CMD多次执行locust -f locustfile.py --worker 就行了
> - ​    首选必须启动master ,在CMD上面locust -f locustfile.py --master
> - ​    最好写一个shell脚本，这样可以一键搞定