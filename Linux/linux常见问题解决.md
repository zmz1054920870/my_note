# 一、解决yum不能正常使用的问题



## 问题1：`yum被锁死`

当我们下载一个东西的时候，中途出现意外，比如命令中途错误，网络延时造成长时间等待，使yum进程一直被占用的时候

```python
Another app is currently holding the yum lock; waiting for it to exit...
  The other application is: yum
    Memory :  19 M RSS (303 MB VSZ)
    Started: Wed Mar 21 11:11:28 2018 - 02:52 ago
    State  : Traced/Stopped, pid: 6373
Another app is currently holding the yum lock; waiting for it to exit...
  The other application is: yum
    Memory :  19 M RSS (303 MB VSZ)
    Started: Wed Mar 21 11:11:28 2018 - 02:54 ago
    State  : Traced/Stopped, pid: 6373
```

解决方法：
1、这是yum被锁了，是因为之前执行了一遍未把进程完整的停掉

```
ps aux | grep yum |grep -v grep |awk ‘{print $2}’ | xargs kill -9
```

**解释命令：`grep -v` 是取反`xargs`将列参数显示变成以空格为分割的行显示**

