

## 一、Hook是怎么和我们的框架搭配起来使用的

问题： 我们书写的用例，hook 本质上是什么？ case 、hook 在运行的时候是交叉进行的

问题：用例的串行流程，如何被框架调度起来



测试套的信息：

- 一个就是Hook
- 一个就是case



test 就是单个用例

resource 就是我们测试床或者说被测资源的信息





## 二、Command 和 Device

​	抽象的Device 对象通过实例化Command.ConnectionPool 实例封装run 接口实现与真实环境交互

![image-20211115234319172](image-20211115234319172.png)



## 三、IO

![image-20211115234531534](image-20211115234531534.png)

## 四、特性抽象



![image-20211115234654703](image-20211115234654703.png)



deviceObj.dispatch(cmd)

ComponentObj.owningDevice.dispatch(cmd)



![image-20211115235052292](image-20211115235052292.png)



## 五、脚本内容



![image-20211115235653023](image-20211115235653023.png)





## 六、测试床



**主机配置部分**

![image-20211115235930590](image-20211115235930590.png)

**阵列的TestBed配置**

![image-20211116000149042](image-20211116000149042.png)





**控制器部分**

控制器，就是deviceMange的cli模式， 我们可以指定cli视图的参数 用于切换



![image-20211116000517046](image-20211116000517046.png)



## 七、日志工具使用

![image-20211116005745657](image-20211116005745657.png)

**主要是parameter里面加上 -e 然后后面一个链接**
