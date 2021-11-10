# XML规范

Windows 记事本默认会将文件保存为单字节的 ANSI (ASCII)。

如果选取文件菜单中的“另存为”命令，就可以规定双字节 Unicode (UTF-16)。

将下面的 XML 文件保存为 Unicode （注意文档不包含任何 encoding 属性）：

```xml
<?xml version="1.0"?>
<note>
  <from>John</from>
  <to>George</to>
  <message>French: êèé</message>
</note>
```

上面的文件，[note_encode_none_u.xml](https://www.w3school.com.cn/example/xmle/note_encode_none_u.xml) 不会出错。但是如果规定了单字节编码就会出错。



```xml
<?xml version="1.0" encoding="windows-1252"?>
<?xml version="1.0" encoding="ISO-8859-1"?>
<?xml version="1.0" encoding="UTF-8"?>
<?xml version="1.0" encoding="UTF-16"?>
```

**错误消息**

如果您试图向 IE 中载入 XML 文档，可能会得到两种指示编码问题的错误：

**在文本内容中发现非法字符**

如果 XML 文档中的某个字符与编码属性不匹配，您就会得到这个错误消息。通常，当 XML 文件中含有外国字符，且当文件使用类似记事本的单字节编码编辑器保存，以及没有指定编码属性时，您就会得到这个错误消息。

**将当前编码切换为不被支持的指定编码**

如果您的文件被保存为 Unicode/UTF-16，但是编码属性被指定为单字节编码（比如 Windows-1252、ISO-8859-1 或者 UTF-8）时，那么您就会得到这个错误消息。或者当您的文档被保存为单字节编码，但编码属性被指定为双字节编码（比如 UTF-16）时，也会得到这个错误消息。

**结论**

结论是：编码属性应当被指定为文档被保存时所使用的编码。我最好的避免错误的建议是：

- 使用支持编码的编辑器
- 确定编辑器使用的编码
- 在您的 XML 文档中使用相同的编码属性

结论是：编码属性应当被指定为文档被保存时所使用的编码。我最好的避免错误的建议是：

- 使用支持编码的编辑器
- 确定编辑器使用的编码
- 在您的 XML 文档中使用相同的编码属性



## XML实体

在 XML 中，有 5 个预定义的实体引用：

| `&lt;`   | <    | 小于   |
| -------- | ---- | ------ |
| `&gt;`   | >    | 大于   |
| `&amp;`  | &    | 和号   |
| `&apos;` | '    | 单引号 |
| `&quot;` | "    | 引号   |

**注释：**在 XML 中，只有字符 "<" 和 "&" 确实是非法的。大于号是合法的，但是用实体引用来代替它是一个好习惯。



## 注释



```
<!-- This is a comment --> 
```



## 在 XML 中，空格会被保留

HTML 会把多个连续的空格字符裁减（合并）为一个：

```
HTML:	Hello           my name is David.
输出:	Hello my name is David.
```

在 XML 中，文档中的空格不会被删节。



## XML 以 LF 存储换行

在 Windows 应用程序中，换行通常以一对字符来存储：回车符 (CR) 和换行符 (LF)。这对字符与打字机设置新行的动作有相似之处。在 Unix 应用程序中，新行以 LF 字符存储。而 Macintosh 应用程序使用 CR 来存储新行。



## XML 命名规则

XML 元素必须遵循以下命名规则：

- 名称可以含字母、数字以及其他的字符
- 名称不能以数字或者标点符号开始
- 名称不能以字符 “xml”（或者 XML、Xml）开始
- 名称不能包含空格

可使用任何名称，没有保留的字词。



## 最佳命名习惯

使名称具有描述性。使用下划线的名称也很不错。

名称应当比较简短，比如：<book_title>，而不是：<the_title_of_the_book>。

避免 "-" 字符。如果您按照这样的方式进行命名："first-name"，一些软件会认为你需要提取第一个单词。

避免 "." 字符。如果您按照这样的方式进行命名："first.name"，一些软件会认为 "name" 是对象 "first" 的属性。

避免 ":" 字符。冒号会被转换为命名空间来使用（稍后介绍）。

XML 文档经常有一个对应的数据库，其中的字段会对应 XML 文档中的元素。有一个实用的经验，即使用数据库的名称规则来命名 XML 文档中的元素。

非英语的字母比如 éòá 也是合法的 XML 元素名，不过需要留意当软件开发商不支持这些字符时可能出现的问题。



## XML 元素是可扩展的

XML 元素是可扩展，以携带更多的信息。

请看下面这个 XML 例子：

```
<note>
<to>George</to>
<from>John</from>
<body>Don't forget the meeting!</body>
</note> 
```

让我们设想一下，我们创建了一个应用程序，可将 <to>、<from> 以及 <body> 元素提取出来，并产生以下的输出：

```
MESSAGE
To: George
From: John

Don't forget the meeting!
```

想象一下，之后这个 XML 文档作者又向这个文档添加了一些额外的信息：

```
<note>
<date>2008-08-08</date>
<to>George</to>
<from>John</from>
<heading>Reminder</heading>
<body>Don't forget the meeting!</body>
</note>
```

那么这个应用程序会中断或崩溃吗？

不会。这个应用程序仍然可以找到 XML 文档中的 <to>、<from> 以及 <body> 元素，并产生同样的输出。

XML 的优势之一，就是可以经常在不中断应用程序的情况进行扩展。



## XML 属性必须加引号

属性值必须被引号包围，不过单引号和双引号均可使用。比如一个人的性别，person 标签可以这样写：

```
<person sex="female">
```

或者这样也可以：

```
<person sex='female'>
```

**注释：**如果属性值本身包含双引号，那么有必要使用单引号包围它，就像这个例子：

```
<gangster name='George "Shotgun" Ziegler'>
```

或者可以使用实体引用：

```
<gangster name="George &quot;Shotgun&quot; Ziegler">
```



## 避免 XML 属性？

因使用属性而引起的一些问题：

- 属性无法包含多重的值（元素可以）
- 属性无法描述树结构（元素可以）
- 属性不易扩展（为未来的变化）
- 属性难以阅读和维护

请尽量使用元素来描述数据。而仅仅使用属性来提供与数据无关的信息。

不要做这样的蠢事（这不是 XML 应该被使用的方式）：

```
<note day="08" month="08" year="2008"
to="George" from="John" heading="Reminder" 
body="Don't forget the meeting!">
</note>
```



## 形式良好的 XML 文档

**“形式良好”或“结构良好”的 XML 文档拥有正确的语法。**

“形式良好”（Well Formed）的 XML 文档会遵守前几章介绍过的 XML 语法规则：

- XML 文档必须有根元素
- XML 文档必须有关闭标签
- XML 标签对大小写敏感
- XML 元素必须被正确的嵌套
- XML 属性必须加引号