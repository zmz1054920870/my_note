## JS基础



[TOC]



```
alter()	  输出一个弹窗(警示框)
document.write('在body中输出一个内容')
consloe.log


```



#### 浏览器

浏览器分为两部分， 渲染引擎和JS引擎

1. 渲染引擎：用来解析HTML与CSS，俗称内核
2. JS引擎: 也称JS解释器，读取网页中的JS， 比如chrome的V8（最快的JS引擎）



![](D:\笔记\JS组成.png)

![](D:\笔记\DOM.png)

![](D:\笔记\BOM.png)

#### 巧用定位

```js
元素：<span data-value="7">7</span>

定位：//span[@data-value and text()=7] -- 比xpath好，这样可以避免动态生成的

上面的//    第一个/ 表示根目标   第二个/ 表示根目录下


```



```HTML
<span class="icon_title_2zyJg">开通会员</span>

//span[@class='icon_title_2zyJg' and text()='开通会员']  定位上面的元素
```





#### //和/的区别

###### // 示例

![](D:\笔记\双斜杠.png)



解释：它会将//div[@class=" a-view index__table___2n0X3"]作为根目录， 然后它下面的所以div，🔺包括儿子div，孙子div，曾孙子div



###### /示例

![](D:\笔记\单斜杠.png)

解释：它会将//div[@class=" a-view index__table___2n0X3"]作为根目录，然后它下面的🔺所有儿子div





```JS
var obj = document.querySelector(".interaction-button");
var count = 100;
while (count-- > 0) {
	if(document.all){
        obj.click();
    }else{
        var e = document.createEvent('MouseEvents');
        e.initEvent('click', true, true);
        obj.dispatchEvent(e);
    }
}
```







#### JS的编写位置

```
内嵌式的JS 		---- <head> javascript</head>
行内式			----	
```





#### JS的数据类型

![](D:\笔记\数据类型.png)

1. 跟python很像， 比如python中 a = 1，不提前定义a的类型，根据后面的赋值来定义，JS也是这样。

2. JS中 定义变量， 不使用var a; 那他就是个全局变量了





###### 普通数据类型

1. 整形

2. 字符型
3. 布尔型 false true   --- 跟python有点不一样，python是大写
4. Undefined  未定义类型  python没有，python变量必须赋值不然报错， 数字与undefined相加  ==  NaN， 函数没返回的时候，返回undefined
5. 空值 null      python中是None, JS中null当成0 来使用
6. object



#### 特性

###### 强制字符串拼接

```
拼接前会将与字符串相加的任何类型转成字符串，再拼接成一个新的字符串  '1' + 1 == '11'

数字型字符串 除以(/) 整形 强制转换成 数字     '10' / 2 == 5
```



###### = ， ==， ===， != , !==

```
一个等号， 是赋值
两个等号， 是数值相等
三个等号， 必须数值类型相同

!= 不等于， 不关心类型
!== 不等于 ， 要判断类型
```





![](D:\笔记\转义字符.png)

#### 内置BIF

```JS
isNaN(object)   --- return false or true  翻译：is no a number
```



```JS
var int = 1111
var str = 'abc'
console.log(typeof(int))	--- 输入类型
console.log(typeof(str))	--- 输入类型
>>> number
>>> string
```



#### 属性

###### 检查字符串的长度

```js
var str = 'my name is andy';
console.log(str.length);
```







#### 方法

###### 转换成字符串

1. 转成字符串： object.toString()    

2. 强制转换成字符串: String(object)

3. 加号拼接      number + " "

我们最常用第三种



###### 转换成数字

1. parseInt('1234abc')  ---> 1234  提取出字符串中的数字（第一个字符必须是数字）
2. parseInt(123.123)   ----> 123   浮点型转成整形
3. parseFloat('12314.12314abc') --->12314.12314
4. parseInt('abc1234')  ----> NaN
5. Number(数字字符串)   跟python的一样 ， 这个更有意义

第一个字符必须是数字， 其实里面也可以是数字，但是这样没有





#### if-else语句

```js
var age
if (age >= 18){
    alter('我想带你去网吧偷耳机')
}else{
    alter('滚回家做作业')
}
```





#### if(条件) - else if(条件) - else

```js
var age = prompt('请输入你的年龄');
        if (age >= 90){
            console.log('我想带你去网吧偷耳机')
        }else if(age >=80){
            console.log('我相带你去网吧偷鼠标')
        }else{
            console.log('滚回家去')
        }
```



#### switch(条件) - case value  -- default (用于固定值选择)

```JS
			
例子1：
			var age = prompt('请输入你的年龄:')
            age = Number(age)
            switch (age > 18){
                case age < 30:
                    console.log('大于30岁')
                    break
                case age < 60:
                    consloe.log('大于60岁')
                default:
                    console.log('好几把打')
                    break

            }


🔺例2：
			for (var i = 0; i <= 100; i++) {
            switch (i > 50) {
                case true:
                    console.log(i)
                    break
                case false:
                    console.log(i)
                    break

            	}
        	}

例3：
for (var i = 0; i <= 100; i++) {
            switch (i > 2) {  //i > 2 得到值有两种可能 true 和 false
                case 0:		 //  0只能全等于0 ,不能全等于false,python中可以
                    console.log(i)
                    break
                case 1:      // 1也同样
                    console.log(i)
                    break

            }
        }
一个都不会打印

"""
1. switch 的条件必须加括号， case 里面可以不加,也可以加
2. 第二种方式的时候 必须全等
3. 如果命中的 case 中没有break,  他会执行下一个case ，直到遇见break或执行完
4. if  是判断是否为真就执行， case是判断是否全等， switch只有传值功能，传的是他表达式最终的结果给case， case进行全等比较，如果全等就通过，  注意却别，case 不是判断真假
5. break  只会退出 switch 不会退出 外部的循环
"""
```





#### for 循环

```
for (var i=1; i<=100; i+=2)
```





#### while 循环

```js
var count = 100
while (count) {
    console.log(count)
    count -= 1
}

"""
跟python的很像
"""

```





#### do  while 循环

```js
该循环会先执行一次循环体， 然后对条件表达式进行判断，如果条件为真，就会重复执行循环体，否则退出循环体

do {
    //循环体
} while (条件)
```





#### 数据结构之 -- 数组 

```
1. JS 是没有多维数组的， python有， 可以去看 python的array BIF 和 numpy
2. 一维数组， 就是python的列表（list）
3. python的元组是tuple
```



###### 创建一个数组

```JS
var 数组名 = new Array()

------------------------------

var arr = []
```



######  其他操作(索引)

```JS
var arr = ['1', 'a', 3， [1, 2, 3]]
arr[0] = '王八蛋'
console.log(arr)
console.log(arr[3][0])
>>> ['王八蛋'， 'a', 3， [1, 2, 3]]
>>> 1
```





###### 遍历数组

```JS
var arr = ['1', 'a', 3, [1, 2, 3]]
for (var i=0; i < arr.length; i++) {
            console.log(arr[i])
        }
```



###### 排序

```JS
		var num = [20, 1, 21, 22, 32, 55, 2, 88, 7, 4, 5]
        var sor_num = []

        for (var j=0; j<num.length; j++) {
            var max = 0
            var count = 0
            for (var i=0; i<num.length; i++) {
                if (num[i]==undefined) {
                    continue
                }
                else if (num[i] > max) {
                    max = num[i]
                    count = i
                }
            }
            sor_num[j] = num[count]  // 这个的j 可以改成sor_num.length
            num[count] = undefined
        }
        console.log(sor_num)


>>> [88, 55, 32, 22, 21, 20, 7, 5, 4, 2, 1]



----------------------------------------------------------
        var num = [20, 1, 21, 22, 32, 55, 2, 88, 7, 4, 5]
        var sor_num = []

        while (num.length > sor_num.length) {
            var max = 0
            var count = 0
            for (var i=0; i<num.length; i++) {
                if (num[i]==undefined) {
                    continue
                }
                else if (num[i] > max) {
                    max = num[i]
                    count = i
                }
            }
            sor_num[sor_num.length] = num[count]
            num[count] = undefined
        }
        console.log(sor_num)

>>> [88, 55, 32, 22, 21, 20, 7, 5, 4, 2, 1]


-------------------------------------------------------
  //冒泡排序
  var num = [20, 1, 21, 22, 32, 55, 2, 88, 7, 4, 5]
            var temp;
            for (var j=0; j<num.length; j++) {
                for (var i=0; i<num.length; i++) {
                    if (num[i] > num[i+1]) {
                        temp = num[i]
                        num[i] = num[i+1]
                        num[i+1] = temp

                    }
                }
            }
            console.log(num)


>>> [1, 2, 4, 5, 7, 20, 21, 22, 32, 55, 88]
```





###### 数组扩容(改变长度扩容) 用empty填充，也可以直接添加

```JS
var ar = ['green', 'red', 'blue']
ar.length = 5
console.log(ar)
console.log(ar[4], typeof(ar[4]))
>>>["green", "red", "blue", empty × 2]
>>>undefined "undefined"

解释：typeof()  ---  返回的是一个字符穿
-----------------------------------------------------------------
    
var ar = ['green', 'red', 'blue']
ar[3] = "yellow"
console.log(ar)

>>> ['green', 'red', 'blue', 'yellow']
```



###### 数组缩容

```JS
var ar = ['green', 'red', 'blue']
ar.length = 2
console.log(ar)

>>> 
```





###### 数组的常用方法

```JS
push  	入栈  同python的append, python没有返回值，js有，返回长度
pop		出栈	同python的pop

array.slice(start,end)  同python的 [start:end]不改变原数组

sort()		同python的sort
reverse()	同python的reverse
indexOf(要查询的字符)

和splice()配合删除 ，指定的字符
var ar = ['a', 'b', 'c', 'd']
ar.splice(a.indexOf('b'), 1)
console.log(ar)
>>> ["a", "b", "c"]


```







###### 

#### 函数

###### 函数的两种申明方式

```js
function fn() {
    函数体
}
fn(参数)


var 变量名 = function(){
    函数体
}

这时候调用就只能是： 变量名(参数)
感觉是js的作用域的问题
```







###### return

没有返回值时，返回undefined





###### arguments 的使用

```js
"""
首先：arguments 是JS函数内置的一个接收参数的对象，不需要在函数中申明， 跟python不一样，python需要自己申明，比如*args
"""

// 是一个伪数组
//1. 具有数组的length属性
//2. 按照索引的方式进行存储
//3. 他没有真正数组的一些方法 pop(), push()等等
//4. 传入的不管是1,2,3,4 这样的参数 还是a=1,b=2,c=3,d=4这样的， 都会按传入的顺序解析成[1,2,3,4]
```





#### 作用域 （区别于python）

###### python

函数中只能调用外面的全局变量，但不能修改



###### JS

函数内部可以调用，也可以修改，但是你如果在函数内部重新申明了一个同名的局部变量，那么你的操作就不会影响外部的同名变量了



```JS
           	var a = 10
            function func () {
                var a = 20
            }
            func()
            console.log(a)

>>> 10
----------------------------------------------
			var a = 10
            function func () {
                a = a + 10
                
            }
            func()
            console.log(a)
>>> 20



-----------------------------------------------
            var a = 10
            function func () {
                var a = a + 10  // a = undefined + 10
                /*
                等价于：
                var a;
                a = a + 10 
                
                */
                
                console.log(a)
            }
            func()
            console.log(a)

 >>> NaN
>>>10
这也可以理解为什么python会报错在这里，因为python是严格的走作用域模式(undifined+10)当然会报错啊


-------------------------------------------------------
 🔺
function fn(num) {
    num = 20
    console.log('fn', num)
}

var num = 10
fn(num)
console.log(num)
>>>fn 20
>>>10
"""
函数内部不是改变了num的值？ 而且num没有进行变量申明， 那他不变成了全局了？

"""
解释：
首选当我们传参的时候， 其实函数内部是申明的，申明如下

function fn(num) {
    var num
    num = 20
    console.log('fn', num)
}
所以当我们传入的参数名和函数内部的变量名同名的时候， 其实他就已经是局部变量了
```







#### js代码预解析



###### js引擎运行JS 分两步： 预解析  代码执行

​	1.	预解析：JS引擎会把JS里面的所有var 还有 function 提升到当前作用域的最前面, var提升，但不赋值， function提升但不调用。。 先提生变量 再提升function

​	2.	代码执行： 按照代码书写顺序从上往下执行



```javascript
console.log(num)
var num = 10;

>>> undefined

// 首先将变量提升，就变成下面的样子了
//var num
//console.log(num)
//num = 10
```





#### 对象



###### 创建对象的 三种方法



第一种

```JS
var obj={
    username:"张三丰",
    sex:"男"
    
}


console.log(obj.username)
console.log(obj["username"])

```



第二种

```js
var obj = new Object()
//   添加属性和方法
obj.username = "张三丰"
obj["sex"] = "男"
obj['func'] = function() {
    
}
```



第三种： 利用构造函数创建对象

```js
function  构造函数名() {
    this.属性 = 值;
    this.方法 = function() {}
}
var a = new 构造函数名()

例子：
				function func(name, sex, age) {
                    this.name = name
                    this.sex = sex
                    this.age = age
                }

                var a = new func("张三丰", "男", 18)

                console.log(a.name)

>>> 张三丰

----------------------------------------------------
比较一下 Array
				var b = new Array('土豆', "玉米", "黄瓜")
                console.log(b)

>>> ["土豆", "玉米", "黄瓜"]

其实他们是一样的


--------------------------------------------------------
升级版, 手动实现劣质版本 Array的push方法
				function func(name, sex, age) {
                    this.name = name
                    this.sex = sex
                    this.age = age
                    this.list = function () {
                        console.log([this.name, this.sex, this.age])
                    }

                    this.push = function (temp) {
                        this.temp = temp
                    }
                }
```





###### 调用(不就是python的字典嘛)

```js
 				var obj = {
                    username: "张山峰",
                    sex: "男",
                    func: function() {
                        this.username = "王八蛋"
                        console.log(this.username)
                    }
                }

                a = obj['func']()   // 这样调用
                obj.func()          // 还可以这样调用
                console.log(obj)
>>>王八蛋
>>>王八蛋
>>>{username: "王八蛋", sex: "男", func: ƒ}
```





#### 对象的变量

首先我们要明确：前面学习的Array也是对象



###### 遍历Array元组(返回的是下标)

```js
var name_list = ['张三', '李四', '王麻子']

for (var k in name_list) {
console.log(k)
}
>>>0
>>>1
>>>2


--------------------------------------
var name_list =  ['张三', '李四', '王麻子']
for (var k in name_list) {
    console.log(name_list[k])
}
```





###### 遍历对象（字符串、[], {}都可以遍历）

```js
var obj = new Object()
obj.a = 1
obj.b = 2
obj.c =3
for (var k in obj) {
    console.log(obj[k])
}
-------------------------------------
var str = 'andy'
for (var k in str) {
    console.log(str[k])
}
```





#### 基本包装类型

###### 解释： 将普通数据类型包装成复杂数据类型 如String、Number、Boolean

string 类型也可以根据索引号取值

###### 例子：

```js
var str = 'andy'
// 解释器自动包装，包装如下：
var temp = new String('andy')
var str = temp
temp = null // 删除临时变量temp
console.log(str.length) //所有  上面的简单类型就是复杂数据类型了
```



###### 同样也有遍历方法

```js
var str = 'andy'
for (var k in str) {
    console.log(str[k])
}
```



######  方法

```js
length 属性

--------
方法：
indexOf(需要查询的字符， num)  -- num 从查询到的第几个字符开始返回，不写，默认从左到右第一个字符放回索引



-----------
replace(old, new)   ---- 替换一个字符

split('分隔符')      ---- 将字符转化为数组

join()				----- 将数组转换为字符串（这是数组的方法）

------------
 var str = 'a,b,c,d'
 var str1 = str.split(',')
 console.log(str1)
 str2 = str1.join()
 console.log(str2)
>>> ['a','b','c','d']
>>> a,b,c,d
```





#### 栈堆

###### 解释

简单数据类型是存放在栈里面， 里面直接开辟一个空间存放的是值

复杂数据类型 首先在栈里面存放地址(十六进制)， 这个地址指向堆里面的复杂数据类型

![](D:\笔记\栈和堆.png)



###### python的栈堆

栈区：存储运行函数的基础数据，方法的形参、局部变量、返回值。由系统自动分配和回收。

堆区：new一个对象的引用或地址存储在栈区，指向该对象存储在堆区中的真实数据。

简而言之一句话：栈放变量，堆放对象





## DOM



###### ------------------------document----------------------------



#### 获取元素

###### getElementById

```js
var element = document.getElementById(id);
console.log(element)
>>> <div id='time'>2019-9-9</div>
```

```
返回一个匹配到 ID 的 的DOM 元素对象
```



###### getElementsByTagName

```js
var element = document.getElementsById('li')
console.log(element)

>>>HTMLCollection [li]

// 不管找到几个元素， 都是返回一个伪数组， 都要用索引的形式去获取
// 如果元素不存在，但是会返回一个空的伪数组
```



###### element.getElementsByTagName('标签名')

```js
// 获取某个元素(父元素)内部所有指定标签名的子元素
<ul>
    <li>1</li>
	<li>2</li>
</ul>
<ol>
    <li>a</li>
	<li>b</li>
</ol>
var ol = document.getElementsByTagName('ol')
var li = ol[0].getElementsByTagName('li') 
console.log(li)
>>>HTMLCollection(2) [li, li]
```





###### getElementsByClassName   //根据类名获取元素集合

```js
<div class='box'>盒子</div>

var boxs = document.getElementsByClassName('box')
>>>HTMLCollection [div.box]   //也是返回一个伪数组
```



###### querySelector('选择器')     //根据指定选择器返回满足条件的第一个元素对象

```js
注意： querySlector不能获取动态生成的元素
<input type="text" value="输入内容">
选择器语法  ---->  
var input = document.querySelector('input[value=输入内容]')
属性值可以加引号也可以不加， 建议不加

```



###### querySelectorAll('选择器') //返回一个伪数组





###### document.body    // 不加括号，获取body元素对象 ,这是一个属性





###### document.documentElement  // 不加括号，返回html元素对象，这是一个属性





#### 事件触发

```js
// 1. 事件触发有三个部分  事件源	事件类型	事件处理程序

<div id='btn'>唐伯虎</button>

//(1) 事件源  事件被触发的对象	谁:按钮
var div = document.getElementByID('btn')
//(2)事件类型	如何触发  什么事情  比如鼠标点击(onclick) 还是键盘按下
//(3)事件处理程序	 通过一个函数赋值的方式 完成
btn.onclick = function() {
    alter('点秋香')
}
```



#### 常见的鼠标事件

![](D:\笔记\常见的鼠标事件.png)

#### 改变元素的内容



###### element.innerText = '修改的内容'     // 不赋值，就是直接获取他的内容

```js
// 1. 事件触发有三个部分  事件源	事件类型	事件处理程序

<div id='btn'>唐伯虎</button>
<div id='div1'>点击唐伯虎显示事件</div>

//(1) 事件源  事件被触发的对象	谁:按钮
var div = document.getElementByID('btn')
//(2)事件类型	如何触发  什么事情  比如鼠标点击(onclick) 还是键盘按下
//(3)事件处理程序	 通过一个函数赋值的方式 完成
btn.onclick = function() {
    var a = document.getElementById('div1')
    a.innerText = '2021-03-21'
}
```

```js
注意： innerText修改的内容不会识别里面的HTML标签
<div id='div1'>今天是个好日子</div>
var div = document.getElementById('div1')
div.innerText = '<strong>草</strong>' //内容加粗

>>> <div id='div1'><strong>草</strong></div> //不识别HTML标签
    
注意二：
innerText : 读取标签的时候，他会去除掉HTML标签并去除换行和空格
<p>
    我是你爹
	<span>123</span>
</p>
上面的HTML 显示效果为： 我是你爹 123  //有空格
var p = document.querySelector('p')
console.log(p.innerText)
>>>我是你爹123 //没有空格没有span标签

```





###### element.innerHTML  = '内容'    //同innerText一样， 但是他是标准的，可以识别HTML标签，上面的注意点，他都没有





#### 属性修改 - 元素对象.属性名 = 其他属性值     (轮播图基础)

```js
<img src='images/刘德华.jpg' alt=''>
 
 var img = document.querySelector('img')
img.src = 'images/张学友.jpg'
----------------------------------------
绑定事件操作
var img = document.querySelector('img')
img.onclick = function () {
    img.src = 'images/张学友.jpg'
}


```







#### this的灵活运用

```JS
<button>按钮</button>
<input type="text" value="输入内容">

var btn = document.querySelector('button')
var input = document.querySelector('input[value=输入内容]')
btn.onclick = function() {
    input.value = '被点击了'
    this.disabled = true
}    

// this指向的是函数调用者btn
//这样可以使用到多个调用者，不用每次就去指定调用者

```





#### 一个元素的样式属性  style

```js
<input type="text" value="输入内容">
<div>人生不止眼前的苟且，还有诗和远方的田野</div>


var div = document.querySelector('input+div')
div.style.background = 'pink'
也可以这样，但是要写完整
div.style = 'background-color: red'
```



#### 注意:元素的class属性，由于js把他当成了一个保留关键字来使用，我们不能直接使用element.class来修改，js给我们提供了另外一个className

```js
<div class='demo'>人生不止眼前的苟且</div>

var div = document.querySelector('div')
div.class = 'demo2' // 这样修改是不行的，避免冲突
div.className = 'demo3' //这样更好，JS提供了一个关键字给我们使用

```







#### 🔺element.属性名  和 element.getAttribute('属性名')

###### element.属性名:  只能获取那些JS给我我们定义好的属性名(内置属性)，比如style、id、className ,如果我们自定义个属性，再采用这样获取的话，就会给你返回undefined或者赋值的时候报错



###### element.getAttribute('属性名'): 可以获取自定义的属性值，如果属性不存在也不会报错，会给你返回一个null



#### element.setAttribute('属性名', '属性值) 设置属性

###### 同理设置属性element.setAttribute('属性名', '属性值')， 当我们用这个来修改类属性(class)的时候， 就可以直接使用class这个关键字了



#### element.removeAttribute('属性名')  移除属性





#### 🔺H5给了我们一个建立，来规范定义自定义属性

###### data-属性名，  这只是给你说要这样做， 你到底做不做那就看你了

###### 如果我们按照H5的标准进行命名的话， H5给我们提供了一个获取自定义属性的一个方法：  element.dataset.自定义属性名  || element.dataset['自定义属性名']，  这个玩意啊 IE 11才开始支持



###### dataset里面存放了所用以data开头的自定属性的一个集合

```js

```





### 节点



#### 获取元素的两种方式

###### 1. 利用DOM提供的方法获取元素

###### 2. 利用节点的层级关系获取元素

​	a. 利用父子兄节点关系获取元素

​	b. HTML DOM树中的所有节点均可以通过javascript进行访问,所有HTML元素(节点)均可被修改,也可以创建或删除

​	c. 节点至少拥有nodeType(节点类型) ,nodeName(节点名称)和 nodeValue(节点值)这三个基本属性



###### 3. nodeType

​	nodeType : 1     	元素节点

​	nodeType : 2		 属性节点

​	nodeType : 3		文本节点	(包括文字 , 空格, 换行)

```HTML
<ul>
    <li>1</li>
    <li>2</li>
    <li>3</li>
</ul>

 // 这里ul的子节点有7个 ,换行也是节点
var ul = document.querySelector('ui')
console.log(ul.childNodes)
>>> NodeList(7) [text, li, text, li, text, li, text]
```





#### 父节点

#### parentNode

###### 定义: 父节点 -- 包裹你的首个元素就是你的爸爸节点  

```js
var div = document.querySelector('div')
console.log(div.parentNode)

----------------------------------------
<div>
	<li>你好</li>    
</div>
这里<li>的父节点是<div>, 不是空格
文本节点"你好"的父节点是<li>
```



#### 子节点

##### node.children  / childNodes

```
children 只返回nodeType为1的元素节点
childNodes 返回所有类型的子节点
```





##### node.firstChild  (不管是文本节点还是元素节点)

```
第一个子节点 --  找不到不到返回null
```







##### node.firstElementChild (忽略文本节点,然后找第一个元素节点)

```
第一个元素子节点 -- 在不到返回null
```





##### node.lastElementChild

```
返回最后一个子元素节点,找不到返回null
```





#### 兄弟节点

##### node.nextSibling

```
返回当前元素的下一个兄弟节点,找不到返回null,同样返回所有节点
```



##### node.nextElementSibling

```
得到下一个兄弟元素节点
```



##### node.previousSibling

```
返回元素上一个兄弟节点,找不到返回null. 同样,也是包含所有的节点
```

###### 有什么用呢?

```js
<div class='demo' style='color:green' index-data='tudou'>
    人生不止眼前的苟且，还有诗和远方的田野
    <span>1</span>
    <span>2</span>
</div>

问题:我们要返回<div>里面文本文字
var div = document.querySelector('div[class=demo]')
console.log(div.innerText);
>>> 人生不止眼前的苟且，还有诗和远方的田野 1 2

解决:
var span = document.querySelector('span')
span.previousSibling.innerHTML
```



##### node.previousElementSiblingha











#### 🔺document.evaluate

```js
document.evaluate(xpathText, contextNode, namespaceURLMapper, resultType, result)
```

https://www.w3school.com.cn/xmldom/dom_xpathresult.asp

##### evaluate的参数和返回值

| 参数               | 经常使用参数 | 解释                                                         |
| ------------------ | ---------- | ------------------------------------------------------------ |
| xpathTexT          | xpath | 表示要计算的Xpath表达式的字符串                              |
| contextNode        | document.documentHTML表示整个HTML标签，document.body表示body标签页 | 文档中，对应要计算的表达式的节点。 |
| namespaceURLMapper | null（我们使用就用null吧） | 把一个命名空间前缀映射为一个全称命名空间 URL 的函数。如果不需要这样的映射，就为 null。namespace resolver 函数的引用, 它只有在工作在 application/xhtml+xml 类型的页面上的用户脚本中是有效的。即使您对它不是很了解也没有关系，因为那种类型的页面不是很多，您可能一次也遇不到。 如果您很想知道它是如何使用的，请参考 Mozilla XPath documentation (http://www-jcsu.jesus.cam.ac.uk/~jg307/mozilla/xpath-tutorial.html)，那里解释了它的用法。 |
| resultType         | https://www.w3school.com.cn/xmldom/dom_xpathresult.asp     **ORDERED_NODE_SNAPSHOT_TYPE**                                 这个结果是一个随机访问的节点列表，就像 UNORDERED_NODE_SNAPSHOT_TYPE，只不过这个列表是按照文档中的顺序排列的。 | 指定了期待作为结果的对象的类型，使用 XPath 转换来强制结果类型。类型的可能的值是 XPathResult 对象所定义的常量。就是返回结果的类型， 有两种一种顺序的，一种无序的 |
| result             | null | 一个复用的 XPathResult 对象；如果你要创建一个新的 XPathResult 对象，则为 null。 |
| **返回值** | | XPathResult对象 |



##### XPathResult对象的属性和方法

注意： XPathResult返回对象的属性跟他的 resultType挂钩



###### 属性

```
snapshotLength
```

当 resultType 为 UNORDERED_NODE_SNAPSHOT_TYPE 或 ORDERED_NODE_ITERATOR_TYPE 时，指定返回的节点数。和 snapshotItem() 方法联合使用这一属性。

还有8种resultType：**ANY_TYPE**， **NUMBER_TYPE**， **STRING_TYPE**， 



###### 方法

| [snapshotItem()](https://www.w3school.com.cn/xmldom/met_snapshotitem.asp) | 返回结果节点列表中指定下标的节点。这个方法只有在 resultType 是 UNORDERED_NODE_SNAPSHOT_TYPE 或 ORDERED_NODE_SNAPSHOT_TYPE 的时候才能使用。snapshotLength 属性和这个方法一起使用。 |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
|                                                              |                                                              |



例子：

![](D:\笔记\XPathResult.png)

resultType

使用 XPath 查询返回何种结果。它的值是前面列出等常量之一， 总共10个常量，这里选用的是第七个，七代表ORDERED_NODE_SNAPSHOT_TYPE。这个属性告诉我们只能使用他绑定的方法