# 一、Jenkins 概述



## 1.1 用途

强大的集成能力	+	可扩展工作流设计

快速简便实现集成：可以通过groovy命令调用git、maven（编译工具）、npm、gradle、shell、junit（单元测试）、sonarqube（代码质量分析）、ansibe、docker、openshift、k8s等插件

支持复杂的构建和发布流程：使用groovy脚本表述复杂的流程

一个构建流程：Maven编译  --  Junit单元测试 -- sonarqube代码质量分析 -- git 发布到二方库

## 1.2 DevOps的CI和CD总体思路

**DevOps设计	+	Jenkins执行**

**DevOps职责**

1. 完成构建定义/部署架构设计;
2. 生成构建定义/部署架构对于Jenkins pipline job配置文件（config.xml）;
3. 查询Jenkins执行Job的实时进度与结果

**Jenkins职责**

1. 根据config.xml创建Jenkins Pipeline job；
2. 执行pipeline job；
3. 提供查询job执行情况的Rest API



## 1.3 Jenkins Pipeline

前言：Pipeline as code 是jenkins的精髓

#### 1.3.1 Pipeline的概念

**下面是jenkins Pipeline 定义的一个示例（groovy脚本编写的）**

![image-20210821103443107](image-20210821103443107.png)



##### **step**

基本操作单元，可以认为是一个脚本的调用或一个插件的调用，小到创建一个目录，大到构建一个Docker镜像，由各类Jenkins Plugin提供

比如上面的 git "https://github.com/cloudbess/mobile-deposit-api.gi" 或者 sh "mvn clean package"都是一个step



##### **Node**

运行期环境，一个Node就是一个Jenkins节点，是执行Step的具体运行期环境，node里的steps将会运行在node对于的agent上

。一个Pipeline job里面呢，可以有多个Node，就像上面示例里面一样，有两个Node，对于的需求呢，对于需求可以运行在不同的机器上



##### **Stage**

Step的逻辑分组，一个Pipeline可以划分为诺干个Stage，每个Stage代表一组操作。多个Stage可以在一个node中（也可以不在一个node中），1个stage也可以跨多个node。使得整个Pipeline job 呢，像管道一样更好的维护



#### 1.3.2 Pipeline重要特性

**前言：Jenkins搭建呢，采用的master slave的集群模式，面对大量引用的编译压力的时候呢，可以分散压力，能够保证编译的速度**

##### **Durable 持久性**

在构建或者部署流程执行过程中，如果jenkins挂掉了，正在运行的pipeline jon 仍然能够继续工作，不会受到影响，也就是说Pipeline的进程独立于Jenkins进程本身



**Pausable 可暂停性**

执行过程中可以暂停，等待用户确认后再继续执行，可以对重要的环节，进行认为的干预



**Rest API 可监控性**

我们可以通过Jenkins提供的Rest API获取每一个stage的执行情况



**基于插件的可扩展性**

jenkins提供了很多插件，是我们可以扩展jenkins



## 1.4 Jenkins 集成难点



#### 1.4.1 执行效率问题

我们的DevOps通过API启动Jenkins的时候，Jenkins是先排队调度，再执行的这种机制，造成启动非常慢，比如有时候等待5 - 6秒或者十几秒的情况都有，之后才会执行正在的脚本，用户使用体验就比较差。一般我们采用异步 + 队列的方式提高用户体验



#### 1.4.2 信息去重问题

由于jenkins采用的是 Master - Slave 集群模式，使得我们在多节点获取执行结果的时候，信息出现重复，需要进行去重的处理

。目前一般使用轮询 + 锁的方式来解决的



#### 1.4.3 信息扩展问题

从jenkins获取的结果都是日志形式的，jenkins没有很好的扩展机制来支持定制，比如说执行脚本，获取用户名密码，获取url地址等等。需要devops（运维）自己进行过滤和处理，目前我们呢，通过脚本写道日志里面，然后过滤日志进行提取



## 1.5 Jenkins的特征



- 易于安装部署配置：可以通过yum安装或者下载war包以及通过docker容器等快速实现安装部署，可方便web界面配置管理
- 消息通知及测试报告：集成RSS/E-mail通过Rss发布构建结果或当构建完成时通过e-mail通知，生成Junit/TestNG测试报告
- 分布式构建：master/slave 主从集群，能够让多台计算机一起构建/测试
- 文件识别：Jenkins能够跟踪哪次构建生成哪些jar，哪次构建使用哪个版本的jar等
- 丰富的插件支持：支持扩展插件，你可以开发适合自己团队使用的工具，如git，svn，maven，dokcer等