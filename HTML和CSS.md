# **pHTML** 

```
Python基础语法都是需要掌握的，web开发重点在于django、flask、Tornado;框架和数据库的ORM映射；还需要了解前端html、css、js等，以及部分前端框架，比如bootstrap、layui、vue、react等（有的公司后端只用写后端，不用了解前端任何，只需要提供接口就好）。还需要多看看别人网站的优点。
```



## 常用浏览器和及其内核

![image-20200924230709242](C:\Users\msi\AppData\Roaming\Typora\typora-user-images\image-20200924230709242.png)

#### 	V8内核是来解释JS的，上面这些内核是来解释HTML的

## **HTML基本语法**

**HTML标签**

* **单标签**  

  ```html
  "`<img>`"   or  `<img />` <img src="" width=500 height=500 alt="图片">
  ```

  

* ```html
  <input > or <input />    
  		<p><input type="text" placeholder="用户名" /></p>
          <p><input type="password" placeholder="密码" /></p>
  ```

  

* **双标签**  `<html> </html>`

```html
<font color="red" size="3.5">字体标签</font>
<h1><font color="red">用户登录</font></h1>
```



### 属性 属于标签

```html
<img src='图片的地址'>
<table width='100' height='200'></table>  这玩意东西有点多
```

### 语法规范

* **标签嵌套 用缩进**
* **快捷写法 写个标签名 直接按Tab键**
* **标签名 不区分大小写 建议小写**
* **属性名 不区分大小写 建议小写**
* **标签必须是<>中间加英文字母，如果是数字如<1>，<1>就会直接被解析出来**
* **块元素中可以放任何元素，P标签除外，p标签不可以自由嵌套的,p标签内只能嵌套内联元素，类似h1、div、ul块元素都不可自由嵌套在p标签内**
* **行内元素中不可以放块元素，a标签除外，但是a标签中不可以嵌套a标签**


### 注释

```html
<!--注释内容-->
<!--
注释内容
-->
```

### 常用HTML实体

* `&nbsp; : 空格`  ---- no break space
* `&lt; : 小于号`
* `&gt; : 大于号`
* `&amp; : &`
* `&copy; : 版权号`
* `&yen; : 人民币号`

### 常见的HTML标签

```html
div 
li 
script 
iframe 
<br> 换行符标签，这个标签是空标签（意味着它没有结束标签，因此这是错误的：<br></br>）。
<button>确定</button> ：它不会换行，一般配合<br>使用
```



```html
<meta charset='utf8'>   
<!--
meta四个属性：http-equiv  name  charset content(这个基本是必需的)
	- name
		- author 
		- description 
		- keywords 
		- generator 
		- revised 
		- others 
	- http-equiv：把content属性关联到HTTP头部
		- content-type 	内容类型
		- expires 		到期
		- refresh    	重定向 
		- set-cookie	设置cookie
meta标签用来设置网页的元数据，还可以用来设置爬虫查找 

--> 
<meta http-equiv="refresh" content="5;https://www.baidu.com"/>  -- 5秒后重定向百度
```

```html
<h1>标题</h1>	
<!--
h1 ~ h6 标题,一般在网页中我们只使用h1到h3,h1标签非常重要，他会影响到页面在搜索引擎中的排名，页面只能又一个h1
-->
```

```html
<p> paragraph 段落</p>
<!--
段落与段落之间是有间隔的，这个间隔可以调整，但是我们要遵循现在的设计逻辑，HTML只做结构的规划，细节的调整我们采用css来完成
-->
```

```html
<img src="图片地址" alt="描述"/ width="数字+px" heigth="数字+px" >
<!--
常用的两个参数src,alt,alt这个描述是在图片无法显示的时候显示
src:采用的是相对路径
width和heigth设置宽高，单位是px（像素）可以不写,当我们只设置width或者heigth的时候
他会按比例同时缩小或者放大

注意：我们放大和缩小不会改变图片的内存占用大小，这个时候我们让公司美工去裁剪把
-->

<!--
图片的格式
	JPEG(JPG)
		- JPG图片支持的颜色比较多，图片可以压缩，但是不支持透明
		- 一般使用JPEG来保存照片等颜色丰富的图片
	GIF
		- GIF支持的颜色少，只支持简单的透明，支持动态图
		- 简单透明：首先图片是正方形的，我在它中间取一个圆形，让这个圆形外面的透明，它办不到，它只能直线透明	
		- 图片颜色单一或者动态图时可以使用gif
	pNG
		- PNG支持的颜色多，并且支持复杂的透明
		- 可以用来显示颜色复杂的透明图片
图片的使用原则
	效果不一致的时候，使用效果好的
	效果一致的时候，使用小的

一般使用PNG
-->
```

```html
毛泽东说过：
        <blockquote>帝国主义都是纸老虎 ... </blockquote>

<!---
毛泽东说过：
        帝国主义都是纸老虎 ... 
->
```

```html
<q>帝国主义都是纸老虎 ... </q>   ----  "帝国主义都是纸老虎 ..."
```

```html
<nav></nav> 导航  nav -- 全称 navigation 
```



### 行内元素

`块(block):在页面中独占一行的元素称为块`

`行内元素(inline element)：在页面中不会独占一行的元素称为行内元素`

```html
<em></em>   
-----  今天天气<em>真</em>不错    这个“真”字会变斜,表示重读
```

```html
<strong></strong> 
----- 今天天气<strong>真</strong>不错    这个“真”字不会变斜，默认变黑,表示真正的强调，这个重要，重要的内容
```

```html
<q></q>			
毛主席说:<q>帝国主义都是纸老虎 ... </q>   ----  毛主席说:"帝国主义都是纸老虎 ..."
```

```html
<a></a>
超链接标签
```

```html
<img src='' alt=''>
行内元素
```



### 列表

```html
<!--三种标签-->
列表之间可以互相嵌套
1.有序列表 ol ---- oder list     li ----  list items
	<ol>
        <li>土豆</li>
        <li>西红柿</li>
	</ol>

2.无序列表
	<ul>
        <li>土豆</li>
        <li>西红柿</li>
	</ul>

3.自定义列表 dl  ----  define list   dt -- difine items   dd --- difine description
相当于一个下拉菜单
    <dl>
        <dt>定义项</dt>
        <dd>土豆</dd>
        <dd>西红柿</dd>
    </dl>


4. VScode写法
	ul > li * 5 生成如下
	<ul>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
    </ul>

	li + li 生成如下
		<li></li>
        <li></li>
	
```



### 语义标签

```html
<header></header>  	表示网页的头部

<main></main>		表示网页的主题部分（一个网页只有一个main）

<footer></footer>	表示网页的底部

<nav></nav>			导航   ---- navigate

<aside></aside>		和主体相关的其他内容（侧边栏）

<article></article>	表示一个独立的文章

<section></section>	表示一个独立的区块，上边的标签都不能表示的时候使用section  ---中文:部分，章节

<div></div>			没有语义，就是用来表示一个区块，目前来讲div还是我们的主要布局元素

<span></span>		行内元素，没有语义，一般用于在网页中选中文字
```

### ID属性

```html
每一个标签都可以添加一个id属性，他是元素的唯一标识，我们同一个页面中不可以出现重复的ID，这里它的属性值是区分大小写的

规范
	-id都是字母开头，不要搞些数字开头

```



### 超链接

```html
<a href="指定跳转的地方"> content </a>    --- 多个<a>标签不会换行，不会独占一行，他也是一个行内标签，有点特殊<a>标签中可以嵌套任何元素，除他自身外（对照前面的inline element不可以嵌套block element一样）， 它也是一个行内标签
    
example
    
    <a href="https://www.baidu.com">超链接</a>
    
属性href --- 指定跳转的目标路径
    
    - 值可以是一个外部网站地址
    	- <a href="https://www.baidu.com">超链接</a>
    - 也可以是一个内部页面地址
    	- <a href="./demo3.html">超链接</a>
    - # 针对滚动条，我们可以跳转回到顶部
    	- <a href='#'>跳转顶部</a>
    - javascript:;  占位符
    	- <a href='javascript:;'>占位符</a>
    - “#”+“id”  指定跳转到一个位置
    	- <a href="#id">指定跳转ID</a>
属性target
    他是一个可选参数(2个)，我们无法自定义
    _self :默认值，挑战连接在当天页面打开
    _blank:在新的空白页面打开
	
```

### 图片引入

```html
<img src='' alt=''>
属性src
	- 引入内部图片
		- 写入内部图片的相对位置

	- 引入外部图片
		- 将外部图片链接赋值给src

	- 通过base64字符引入图片,这样图片就可以在网页加载的时候直接加载进来,这个字符就是一个图片，没有它的原始路径，就存在与网页中
	
	使用python实现图片转换base64字符
	import base64
	f = open("C://Users//msi//Desktop//img.gif","rb")
	content = f.read()
	b64 = base64.b64encode(content)
	b64 = b64.decode("utf8")
	result = "data:img/git;base64,{0}".format(b64)

```

### 内联框架

```html
<iframe>src='' frameborder="0 or 1"</iframe>

内部框架。用于向当前页面中引入一个其他页面
	src 指定要引入的网页路径（可以链接，也可以是一个html文件）
	borderframe 可以选参数：0，1 分别表示是否有边框，一般情况下我们选择0
	width:和img里面不一样，单独修改的时候heigth不会等比缩放，单位px
	heigth：和img里面不一样，单独修改的时width不会等比缩放,单位px
```



### 音频标签

```html
<audio src="资源路径" controls loop muted autoplay preload="auto、metadata、none"></audio>

src 		资源路径
controls	控制组件（控制UI）
muted		规定视频输出应该被静音。
loop		循环播放
autoplay	如果出现该属性，则音频在就绪后马上播放。
preload		如果出现该属性，则音频在页面加载时进行加载，并预备播放。如果使用 "autoplay"，则忽略该属性。


开发中为了照顾compatibility 引入<source>src="" type</source>标签

<audio controls>
    Your browser does not support the audio element.
   <source src="horse.ogg" type="audio/ogg">
   <source src="horse.mp3" type="audio/mpeg">
 Your browser does not support the audio element.
</audio> 

执行过程分解
	1.首先浏览器如果不能识别audio标签，那么audio里面的内容都不会再去解析了
	2.当audio可以解析的时候，开始解析source标签，如果第一个就能解析播放，后面的source不会再解析
	3. Your browser does not support the audio element.当source无法被解析的时候显示出来


完美兼容例子
	<audio controls autoplay loop>
        <source src="./沙宝亮 - 完美世界.mp3" type="audio/mp3">
        <source src="./沙宝亮 - 完美世界.mp3" type="audio/mp3">
        <embed src="./沙宝亮 - 完美世界.mp3" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
```



### CSS引用标签

```html
<link rel="stylesheet" href="./关系型选择器.css">
```





## CSS

### CSS规范

* **内部样式表----建议使用外部样式表**

  ```html
  <!doctype html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>CSS演示教程</title>
      <style>
          p{
              color:red;
              font-size:50px;
          }
      </style>
  </head>
  ```

* **使用link标签进行外部样式引用**

  ```html
  <link href="main.css" rel="stylesheet">
  ```

  

* **style标签内部必须遵循CSS的语法规范**

* **CSS注释**

  ```css
  /*
  
  css中的注释
  
  */
  ```


* **class属性**

```
所有标签都可以有这个属性，跟ID属性一样
```



### CSS语法

#### 选择器

```CSS
1.	id选择器（id是唯一的只能有一个）
	作用：根据元素的id属性值选中一个元素
	语法:#id属性值{}

2.	class选择器  ----以后主要使用
	作用:根据元素的class属性值选中一组元素
	语法: .class属性值

3. 	复合选择器(seletor)
	作用:选中同时复合多个条件的元素
	语法：标签#id.class
special example:
	<style>
		.a.b.c{
            	color:red;
				}
	</style>
	<div class="red a b c">我是元素div</div>
一个元素可以有多个类名，书写格式class = "A B C"
4.	selector分组
	作用：同时选中多个选择器
	语法:标签1#id1.class1,标签2#id2.class2,标签3#id3.class3


5.	通配选择器
	作用：选择页面中的所用元素
	语法：*{}

6.	子元素选择器
	作用：选中父元素指定的子元素(所用子元素)
	语法：father > child  or  爷爷 > 老子 > 儿子
	表示：比father小一级目录的child标签

7.	后代元素选择器
	作用：选中指定元素的后代（这里不光只有子元素，它包括所有后代比如：孙子、曾孙）,对他的后代生效
	语法：祖先 后代
	表示：比祖先目录等级低的所以后代元素

8.	兄弟选择器
	作用：前一个的下一个
	语法：前一个 + 下一个
	注意：样式只对“下一个生效”
	注意：出现这种
		span + span 这种的两个相同元素相加，表示只要是存在两个span连续的元素，都被设定样式,同理A+B 只要满足的就生成样式，对“+”号后面的生效

9.	属性选择器(class 和 id 也是属性，但是他们有专门的标记了就排除)
	Syntax: [attr] [attr=value] [attr~=value] [attr|=value] [attr^=value] 						[attr$=value] [attr*=value]
	Example: [autoplay] will match all elements that have the autoplay attribute 				set (to any value).
	前面还可以加一个标签元素,反正就是灵活使用
	Syntax: div[attr] div[attr=value] div[attr~=value] div[attr|=value] 					div[attr^=value] div[attr$=value] [attr*=value]
前面不加div，相当于是*[value]

div[attr^=value ]  	---- 表示div中属性值以value开头的
div[attr$=value]	---- 表示div中属性值以value结尾的
[attr*=value]		---- 表示属性值中包含value的



$("div[dataId]");            //拥有属性dataId的div列表
$("div[dataId=test]");       //属性dataId为"test"的div列表
$("div[dataId!=test]");      //属性dataId不等于"test"或没有title属性的div列表
$("div[dataId^=test]");      //属性dataId以"test"开始的div列表
$("div[dataId$=test]");      //属性dataId以"test"结束的div列表
$("div[dataId*=test]");      //属性dataId含有"test"的div列表
$("div[dataId|=test]");      //属性dataId等于"test"或以"test-"开头的div列表
$("div[dataId~=test]");      //属性dataId用空格分割的值中包含test的div列表
$("div[id][dataId$=test]");  //包含属性id，同时属性title以"test"结束的div列表,不光指id其他属性也可以
example ----> img[src][alt='图片1']
											

```



### Pseudo Class

> ```HTML
> Pseudo Class（伪类有点多、伪元素就几个）  --- 可以和上面的CSS选中一起使用
> 	- 它是用来描述一个元素(即标签)的特殊状态的(所有前面必须要加一个元素，不然就是全局了，不管你是first还是last)
> 	比如：第一个子元素、被点击的元素、鼠标移入的元素
> 下面几个不适用于A+B这种选择器
> :first-child  				第一个子元素
> :last-child					最好一个子元素
> :nth-child(digital)			从头部计数开始，选中第n个子元素
> :nth-last-child(digital)	从尾部计数开始，选中第n个子元素
> 	digital = 2n or even	表示选中偶数个子元素
> 	digital = 2n+1 or odd 	表示奇数个子元素
> 
> 
> 以上这些伪类都是根据body里面所有的子元素进行排序的，它会将同级的全部纳入处理器中，然后依次匹配，符合规则的加以处理（这个有点抽象）
> 	<style>
>         li:nth-child(2n+1){
>             color:rgb(255,0,0)
>         }
>         
> 	</style>
> 	<ul>
>         <span>我是你爸爸</span>
>         <li>第一个</li>
>         <li>第二个</li>
>         <li>第三个</li>
>         <li>第四个</li>
>         <li>第五个</li>
>     </ul>
> 前面的选择器先进行定位，然后满足定位的的范围内，nth-child对级下的所有元素参与进行筛选
> 
> 
> 
> 
> 
> 
> 下面这几个就是同类型的了
> :fist-of-type
> :last-of-type
> :nth-of-type
> :nth-last-of-type()
> 
> 
> 
> 
> 
> :not()否定伪类
> 	- 将符合条件的元素从选择器中剔除
> 	li:nth-of-type(2n):not(:nth-child(5)){
>     color: red;
> 	}
> 
> 顺序：li:nth-of-type(2n) ,然后在这些满足条件的里面剔除li:nth-child(5)的这一个
> 
> 
> 注意：上面的当digital 等于"n"的时候表示所有
> 
> ```

### 超链接相关的伪类（不全是a专属哈）

```html
a:link{}  		--- 表示没有访问过的链接（正常链接）--a专属
a:visited{}		--- 表示访问过的链接，出于隐私考虑,它只能改颜色，font-size会无效 -- a专属
a:hover{}		--- 表示鼠标悬浮的样式，这个不限制a标签，其他标签也可以
a:active{}		--- 表示鼠标按下去后的样式
```



### 伪元素选择器

```html
You can use only one pseudo-element in a selector. It must appear after the simple selectors in the statement.
在选择器中只能使用一个伪元素。它还必须出现在一个语句中的简单选择器之后
Note: In contrast to pseudo-elements, pseudo-classes can be used to style an element based on its state.
注意：与伪类相反，伪元素可用于根据元素的状态来设置其样式

这样理解：伪类表示一个元素的特殊状态，伪元表示页面中一些特殊并不真实存在的元素（比如：特殊位置，首字母、第一行）,前面要加元素或者选择器，不然就是全局变量了

::first-letter	首字母
::first-line	首行
::selection		当鼠标选中以后的效果
::before		元素开始
::after			元素结束
	使用::before和::after ,必须结合content属性来使用
	通过content添加的内容你是无法选中的，因为他是通过CSS来添加的
	
```

### 继承

```html
一.并不是所以的元素都可以被继承
	1.背景相关CSS不会继承给后代 ---比如 background
	2.布局相关CSS的不会继承给后代
	3.等
```

### 选择器的权重

```html
选择器的权重：
二、权重计算规则

第一等：代表内联样式，如: style=””，权值为1000。
第二等：代表ID选择器，如：#content，权值为0100。
第三等：代表类，伪类和属性选择器，如.content，权值为0010。
第四等：代表元素选择器和伪元素选择器，如div,p，权值为0001。
通配符、子选择器、相邻选择器等的。如*、>、+,权值为0000。
继承的样式没有权值。
三、比较规则

1,0,0,0 > 0,99,99,99，也就是说从左往右逐个等级比较，前一等级相等才往后比

1，   0 ，     0，   0
0,   99 ，  99 ，  99
 

!important 的作用是提升优先级，加了这句的样式的优先级是最高的,可以放到样式声明的最后，用来无视本文重点说的权重等级。我觉得最好还是不要用这东西，首先IE6对它支持不好，要支持它需要把一个样式规则分开写，另，用多了会严重扰乱CSS的权重等级。
格式：
	div{
	color:blue !important;
}
```

## layout(布局)

### 文档流

```html
网页是一个多层结构
	-通过CSS可以分别为每一层来设置样式
	-作为用户来讲只能看到最顶上一层
	-这些层中，最底下的一层称为文档流，文档流是网页的基础
		我们所创建的元素默认都是在文档流中进行排列的
	-对于我们来说元素主要有两个状态
		在文档流中
		不在文档流中（脱离文档流）
```

```python
"""
元素在文档流中有什么特点
"""

	1.快元素
    	- 快元素会在页面中独占一行（无论多宽，多窄）（自上向下）
        - 默认宽度是夫元素多宽他就多宽
        - 默认高度是内容撑开（子元素撑开）
    2.行内元素
    	- 行内元素不会独占一行，只占自身的大小
        - 行内元素在页面中由左向右，水平排列
        - 如果一行之中不能容纳下所以的行内元素，则元素会换行到第二行，继续从左向右写（书写习惯一样）
        - 行内元素的默认高度和宽度都是被内容撑开
  
```

### 盒子模型

```html
--CSS将页面中的所有元素都设置为了一个矩形的盒子
--网页布局就是摆放盒子

每一个盒子都有以下几个部分组成
	-内容区  	content
    -内边距	padding(翻译:填充) -内容区和
    -边	框	border
    -外边距	margin(外部元素与元素之间的距离)


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>宇宙无敌</title>
    <style>

        .box1{
            /* 
            内容区（content），元素中所有子元素和文本内容都				在内容区中排列
            内容区的大小由width和height两个属性来设置
                    width 设置内容区的宽度
                    height 设置内容区的高度
            */
            width: 200px;
            height:200px;
            background-color: yellow;
            /* 
            边框(border)，边框属于盒子边缘，边框里边属于盒子内部，出了边框都是盒子的外部
            边框的大小会影响整个盒子的大小，里面的内容区(content)大小不会改变
            设置边框，至少需要设置三个样式
                边框的宽度 border-width（默认值是3px）
            	
                边框颜色    border-color
                边框的样式  border-style
            
            */ 

            border-width:10px;
            border-color:red;
            border-style:solid;
        }
    </style>
</head>
<body>

    <div class='box1'></div>
    
</body>
</html>
```

#### 边框

```html
border-width:10px 20px 30px 40px (顺时针)

四个值:	上	右	下	左 ----》顺时针
三个值:	上	左右	下
两个值:	上下	左右
一个值:	上下左右
不写的时候，默认3px


border-color:red yellow blue black
四个值:	上	右	下	左 ----》顺时针
三个值:	上	左右	下
两个值:	上下	左右
一个值:	上下左右
不写的时候他会去找color，color也没有的时候就是transparent

border-style:solid dotted dashed double;
四个值:	上	右	下	左 ----》顺时针
三个值:	上	左右	下
两个值:	上下	左右
一个值:	上下左右
solid 		-- 实线
dotted		-- 点虚线
dashed		-- 虚线
double		-- 双实线
不写时，默认值是 none

border-top-width:10px
border-bottom-width:10px
border-left-width:10px
border-right-width:10px


border-top-color:
border-bottom-color:
border-left-color:
border-right-color:


border-top-style:
border-bottom-style:
border-left-style:
border-right-style:

混合使用的时候，谁在下面运用谁的样式





上面的了解，下面才是最常用的
border简写属性，通过该属性可以同时设置边框所有的相关样式，并且没有顺序要求

example:
	borde:solid 10px orange;

出了border以外还有四个 border-xxx
border-top:
border-left:
border-bottom:
border-right:

example:
	border-top:10px solid yellow
```

#### color

```
color是一个浅景色，像什么“字体颜色”，“边框颜色”，如果你不特殊指定就用他了。
```

#### 内边距

```html
像素百分比好处：可以使子元素跟着父元素的改变而改变
```

![](D:\笔记\狂模型.png)

```html
元素的内边距在边框和内容区之间(border的内边和content的外边之间的距离，不指定padding,内边距就是0)。控制该区域最简单的属性是 padding 属性。
CSS padding 属性定义元素边框与元素内容之间的空白区域。

四个方向的内边距

	padding-top;
	padding-bottom;
	padding-left;
	padding-right;

注意点：
	1.内边距的设置会影响盒子的大小
	2.背景颜色会延伸到外边距
```

#### 外边距

移动元素的时候要注意：

 - 元素在页面中是按照自左向右的顺序排列的，

   所以默认情况下如果我们设置的左和上  边距则会移动元素自身

   而设置下和右边距会移动其他元素



#### 水平方向布局

元素在其父类当中水平方向的位置由以下几个属性共同决定

* margin-left
* border-left
* padding-left
* width
* padding-right
* border-right
* margin-right

一个元素在其父元素当中，水平布局必须要满足以下的等式

(margin-left) + (border-left) + (padding-left) + (width) +  (padding-right) +  (border-right) + (margin-right) ==  width（父元素--即父元素内容区宽度）



上面这个等式必须成立，如果相加等式不成立，则称为过度约束，等式会自动调整。

​	-- 调整情况

* 如果这七个值没有为auto的情况，则浏览器会自动调整margin-right值以使等式成立
* 上面7个值中有3个可以设置为auto
  - width
  - margin-left
  - margin-right
    - 如果某个值为auto，则会自动调整为auto的那个值，以使等式成立
* 如果将一个宽度和一个外边距设置为auto（不写也行，width不写默认是auto，其他两个不是的），宽度取最大，外边距为0
* 如果将三个值都设为auto，还是一样宽度最大，其他两个为0
* 如果将两个外边距设置为auto，宽度固定值，则会将外边距设置为相等的值
  * 所以我们经常利用这个特定来使一个元素在其父元素中水平居中





#### 垂直方向的布局

注意：

* 父元素的高度，不写，就是被父元素撑开，写上该是多少就是多少

* P标签自带了margin-top和margin-bottom值，div没有

* 父元素的高度固定，如果子元素的高度超过了父元素，则子元素会从父元素中overflow（一出），我们可以是用<strong style='color:red'>overflow</strong>属性来设置溢出的子元素;

  | 属性     | 参数    | 效果                                                 | 中文 |
  | -------- | ------- | :--------------------------------------------------- | ---- |
  | overflow | visible | 这是默认值，子元素会从父元素中溢出，在父元素外部显示 | 可见 |
  |          | hidden  | 溢出的部分会被裁剪掉，不会溢出                       | 隐藏 |
  |          | scroll  | 生成两个滚动条，通过滚动条来查看内容                 | 滚动 |
  |          | auto    | 根据需要生成滚动条                                   | 自动 |

  

#### 外边距的重叠 （垂直方向才有）

* 相邻的垂直方向外边距会发生重叠现象

  兄弟元素

  - 兄弟元素间的相邻垂直外边距会取两者之间的较大值--两者都是正值的时候（margin-bottom和margin-top谁大取谁）
  - 特殊情况（基本不会遇到）：
    - 相邻的外边距一正一负，则取两者的和
    - 如果相邻的外边距都是负值，取两者中绝对值较大的

  

  父子元素

  - 父子元素之间的相邻外边距，子元素的会传递给父元素（上外边距）
  - 父子外边距的折叠会影响到页面的布局，必须要进行处理
    - 可以灵活使用height 和padding来解决，但是要重新计算height，记住元素的高度被内容撑开这句话
    - 还要记住一句话：垂直外边距是，相邻元素到border的距离。

#### 行内元素的盒子模型

* 行内元素不支持设置width和height

* 行业元素可以设置padding，但是垂直方向的padding不会影响页面的布局（会盖住）

* 行业元素可以设置border，垂直方向的border不会影响页面的布局（会盖住）

* 行内元素可以设置margin，垂直方向的margin不会影响页面的布局（不会挤上下）

  | 属性       | 参数         | 效果                                                         | 中文     |
  | ---------- | ------------ | ------------------------------------------------------------ | -------- |
  | display    |              | 转换元素的类型                                               | 显示     |
  |            | inline       | 将元素设置为行内元素                                         | 行内元素 |
  |            | block        | 将元素设置为块元素                                           | 快       |
  |            | inline-block | 将元素设置为行内块元素，行业快，既可以设置高度和宽度又不会独占一行 | 行内块   |
  |            | table        | 将元素设置为一个表格                                         |          |
  |            | none         | 元素不在页面中显示，隐藏一个元素（没了就是没有）             |          |
  | visibility |              | 用来设置元素的显示状态                                       | 能见度   |
  |            | visible      | 默认值，元素在页面中正常使用                                 | 可见     |
  |            | hidden       | 元素在页面中隐藏，不显示，但是依然占据页面的位置             | 隐藏     |

  

#### 去除浏览器自带样式

```html
*{
	margin:0;
}
ul{
	list-style:none;
}
```

