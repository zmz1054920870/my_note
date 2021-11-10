## 一、解决导入xml包的时候出现红线或者包不存在的问题



**第一步：**

找到我们的xml包



**第二步：**

将这个包的文件夹（xml）拷贝出来



**第三步：**

将我们拷贝出来的xml文件夹复制到如下目录下

```
D:\PyCharm 2020.1.1\plugins\python\helpers\typeshed\stdlib\2and3
```



**第四步：**

删掉第一步中xml文件夹中的`__pycache__`



**总结：为什么会这样呢？**

那是因为我们有工程文件使用了这个名字，所以导致啊，我们找不到这个包了





## 二、通过xml模块操作xml文件

https://blog.csdn.net/kongsuhongbaby/article/details/84869838

https://www.runoob.com/python/python-xml.html

**movie.xml**

```
<collection shelf="New Arrivals">
<movie title="Enemy Behind">
   <type>War, Thriller</type>
   <format>DVD</format>
   <year>2003</year>
   <rating>PG</rating>
   <stars>10</stars>
   <description>Talk about a US-Japan war</description>
</movie>
<movie title="Transformers">
   <type>Anime, Science Fiction</type>
   <format>DVD</format>
   <year>1989</year>
   <rating>R</rating>
   <stars>8</stars>
   <description>A schientific fiction</description>
</movie>
   <movie title="Trigun">
   <type>Anime, Action</type>
   <format>DVD</format>
   <episodes>4</episodes>
   <rating>PG</rating>
   <stars>10</stars>
   <description>Vash the Stampede!</description>
</movie>
<movie title="Ishtar">
   <type>Comedy</type>
   <format>VHS</format>
   <rating>PG</rating>
   <stars>2</stars>
   <description>Viewable boredom</description>
</movie>
</collection>
```



**dom读取**

```python
#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : xml_handle_dom.py

# from xml.dom.minidom import parse
# from xml import dom
#
# DOMTree = parse(r'C:\Users\zmz\Desktop\test-tb-jenkins\local_lib\API\movies.xml')
# booklist = DOMTree.documentElement
# print(booklist.toxml())
# from xml.dom.minidom import parse
import xml.dom.minidom

# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse(r"C:\Users\zmz\Desktop\test-tb-jenkins\local_lib\API\movies.xml")
collection = DOMTree.documentElement
if collection.hasAttribute("shelf"):
    print("Root element : %s" % collection.getAttribute("shelf"))

# 在集合中获取所有电影
movies = collection.getElementsByTagName("movie")

# 打印每部电影的详细信息
for movie in movies:
    print("*****Movie*****")

    if movie.hasAttribute("title"):
        print("Title: %s" % movie.getAttribute("title"))

    type = movie.getElementsByTagName('type')[0]
    print("Type: %s" % type.childNodes[0].data)

    format = movie.getElementsByTagName('format')[0]
    print("Format: %s" % format.childNodes[0].data)

    rating = movie.getElementsByTagName('rating')[0]
    print("Rating: %s" % rating.childNodes[0].data)

    description = movie.getElementsByTagName('description')[0]
    print("Description: %s" % description.childNodes[0].data)
```



**sax读取**

```
import xml.sax


class MovieHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.type = ""
        self.format = ""
        self.year = ""
        self.rating = ""
        self.stars = ""
        self.description = ""

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "movie":
            print("*****Movie*****")
            title = attributes["title"]
            print("Title:", title)

    # 元素结束事件处理
    def endElement(self, tag):
        if self.CurrentData == "type":
            print("Type:", self.type)

        elif self.CurrentData == "format":
            print("Format:", self.format)

        elif self.CurrentData == "year":
            print("Year:", self.year)

        elif self.CurrentData == "rating":
            print("Rating:", self.rating)

        elif self.CurrentData == "stars":
            print("Stars:", self.stars)

        elif self.CurrentData == "description":
            print("Description:", self.description)

        self.CurrentData = ""

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "type":
            self.type = content
        elif self.CurrentData == "format":
            self.format = content
        elif self.CurrentData == "year":
            self.year = content
        elif self.CurrentData == "rating":
            self.rating = content
        elif self.CurrentData == "stars":
            self.stars = content
        elif self.CurrentData == "description":
            self.description = content


if (__name__ == "__main__"):
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler(Handler)

    parser.parse("C:\\Users\zmz\Desktop\\test-tb-jenkins\local_lib\API\movies.xml")
```

