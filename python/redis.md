# [python3 redis数据库写入方法和json格式的坑](https://www.cnblogs.com/xuexizongjie/p/10878992.html)

import redis

host = xxx

pwd = xxx

 

r = redis.Redis(host=host,password=pwd,db=15,decode_responses=True,port=xxxx) 

1、第一种

 r.hmset('test',{'xxxxxx65': "{'QQ号': xxxxx65}"})  #写入redis

 print(r.hgetall('test'))

  \##执行结果：redis，STRING类型，字符串

2、第二种

```
r.set('test','{"addr":"北京某苑","phone":13300000000}')

##执行结果   redis，STRING类型，json串
```

3、第三种

```
r.hset('test','xuesheng4','num:123456789')
##执行结果  redis，HASH类型，字符串
```

4、第四种

 r.hmset('test',{'xuesheng4': '{"nick": "xs","num":123456789}'})

 \##执行结果 redis，HASH类型，json串

 

-------坑、坑、坑------：

如果想要value格式为json，k-v必须用 双引号，注意观察上述例子。

第一种情况，引号没用对，所以看起来像字典，其实写入redis时，是个字符串。