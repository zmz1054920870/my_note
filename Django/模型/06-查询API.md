# 返回新QuerySet的API

| 方法名            | 解释                                                         |
| ----------------- | ------------------------------------------------------------ |
| **filter()**      | 过滤查询对象。                                               |
| **exclude()**     | 排除满足条件的对象                                           |
| **annotate()**    | 使用聚合函数                                                 |
| **order_by()**    | 对查询集进行排序                                             |
| **reverse()**     | 反向排序                                                     |
| **distinct()**    | 对查询集去重                                                 |
| **values()**      | 返回包含对象具体值的字典的QuerySet.返回值是 QuerySet 数据类型里面为一个个字典 |
| **values_list()** | 与values()类似，只是返回的是元组而不是字典.返回值是 QuerySet 数据类型里面为一个个列表。 |
| **none()**        | 创建空的查询集                                               |
| **all()**         | 获取所有的对象                                               |



- values的返回结果如下

```
<QuerySet [{'id': 1, 'id_delete': False}, {'id': 2, 'id_delete': False}, {'id': 4, 'id_delete': False}, {'id': 3, 'id_delete': False}]>
```

- vaules('字段名1', '字段名2')的方式指定只返回哪些字段的数据，values_list同理

values和all的区别在于如下

```python

 >>> User.objects.filter(id__gt=1).values()
QuerySet [{'id': 3, 'is_deleted': False, 'create_time': datetime.datetime(2022, 2, 13, 21, 14, 56, 577621), 'update_time': datetime.datetime(2022, 2, 13, 21, 14, 56, 577621), 'test_one': 'test_null', 'test_two': '', 'test_three': None, 'phone': '18996696042', 'name': 'Alex', 'pwd': '123456', 'gender': '女'}, {'id': 4, 'is_deleted': False, 'create_time': datetime.datetime(2022, 2, 13, 21, 33, 7, 676282), 'update_time': datetime.datetime(2022, 2, 13, 21, 33, 7,
 676282), 'test_one': 'test_null', 'test_two': "''", 'test_three': None, 'phone': '18996696042', 'name': 'Tom', 'pwd': '123456', 'gender': '男'}, {'id': 5, 'is_deleted': False, 'create_time': datetime.datetime(2022, 2, 19, 18, 49, 4
2, 220773), 'update_time': datetime.datetime(2022, 2, 19, 18, 49, 42, 220773), 'test_one': 'test_null', 'test_two': '', 'test_three': None, 'phone': '18996696044', 'name': 'boby', 'pwd': '123456', 'gender': '男'}]>

 >>> User.objects.filter(id__gt=1).values()[0] # 返回的是一个字段，可以采用字典的规则进行取值
{'id': 3, 'is_deleted': False, 'create_time': datetime.datetime(2022, 2, 13, 21, 14, 56, 577621), 'update_time': datetime.datetime(2022, 2, 13, 21, 14, 56, 577621), 'test_one': 'test_null', 'test_two': '', 'test_three': None, 'phone
': '18996696042', 'name': 'Alex', 'pwd': '123456', 'gender': '女'}
=================================================================================
 >>> User.objects.filter(id__gt=1).all()
<QuerySet [<User: Alex>, <User: Tom>, <User: boby>]>
 
>>> User.objects.filter(id__gt=1).all()[0] # 采用类属性的方式进行取值
<User: Alex>


```





# 不返回QuerySet的API

| 方法名                 | 解释                                                 |
| ---------------------- | ---------------------------------------------------- |
| **get()**              | 获取单个对象，没有报错                               |
| **create()**           | 创建对象，无需save()                                 |
| **get_or_create()**    | 查询对象，如果没有找到就新建对象                     |
| **update_or_create()** | 更新对象，如果没有找到就创建对象                     |
| **count()**            | 统计对象的个数                                       |
| **latest()**           | 获取最近的对象                                       |
| **earliest()**         | 获取最早的对象. 里面必须填一个字段。根据排序来判断的 |
| **first()**            | 获取第一个对象,没有返回None                          |
| **last()**             | 获取最后一个对象                                     |
| **aggregate()**        | 聚合操作                                             |
| **exists()**           | 判断queryset中是否有对象                             |
| **update()**           | 批量更新对象                                         |
| **delete()**           | 批量删除对象                                         |



## 注意：

为了我们的方便，在定义模板的时候一定要指定db_table，不然当我们修改了我们的应用名的时候，非常麻烦。
