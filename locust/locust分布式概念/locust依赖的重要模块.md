## Locust的依赖模块

#### 安装Locust模块，使用命令pip install locust即可，它依赖于如下模块：

- **gevent： 在python中实现协程的一个第三方库，协程又称微线程（Coroutine）**
- **flask： Python的一个Web开发框架**
- **requests： 常用于接口测试**
- **msgpack-pyhon：一种快速紧凑的二进制序列化格式，适用于类似Json的数据**
- **six：提供了简单的工具来封装python2和python3之间的差异**
- **pyzmq：如果打算将locust运行在多个进程/机器，可以使用它（分布式就是依赖于它）**

