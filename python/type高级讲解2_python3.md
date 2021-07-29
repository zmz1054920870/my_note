# 类作为对象

在理解元类之前，您需要掌握Python的类。Python从Smalltalk语言中借用了一个非常特殊的类概念。

在大多数语言中，类只是描述如何产生对象的代码段。在Python中也是如此：

```python
>>> class ObjectCreator(object):
...       pass
...

>>> my_object = ObjectCreator()
>>> print(my_object)
<__main__.ObjectCreator object at 0x8974f2c>
```

但是类比Python中的更多。类也是对象。

是的，对象。

一旦使用关键字`class`，Python就会执行它并创建一个对象。指令

```python
>>> class ObjectCreator(object):
...       pass
...
```

在内存中创建一个名称为“ ObjectCreator”的对象。

**这个对象（类）本身具有创建对象（实例）的能力，这就是为什么它是一个类**。

但是，它仍然是一个对象，因此：

- 您可以将其分配给变量
- 你可以复制它
- 您可以为其添加属性
- 您可以将其作为函数参数传递

例如：

```python
>>> print(ObjectCreator) # you can print a class because it's an object
<class '__main__.ObjectCreator'>
>>> def echo(o):
...       print(o)
...
>>> echo(ObjectCreator) # you can pass a class as a parameter
<class '__main__.ObjectCreator'>
>>> print(hasattr(ObjectCreator, 'new_attribute'))
False
>>> ObjectCreator.new_attribute = 'foo' # you can add attributes to a class
>>> print(hasattr(ObjectCreator, 'new_attribute'))
True
>>> print(ObjectCreator.new_attribute)
foo
>>> ObjectCreatorMirror = ObjectCreator # you can assign a class to a variable
>>> print(ObjectCreatorMirror.new_attribute)
foo
>>> print(ObjectCreatorMirror())
<__main__.ObjectCreator object at 0x8997b4c>
```

# 动态创建类

由于类是对象，因此您可以像创建任何对象一样动态地创建它们。

首先，您可以使用`class`以下方法在函数中创建一个类：

```python
>>> def choose_class(name):
...     if name == 'foo':
...         class Foo(object):
...             pass
...         return Foo # return the class, not an instance
...     else:
...         class Bar(object):
...             pass
...         return Bar
...
>>> MyClass = choose_class('foo')
>>> print(MyClass) # the function returns a class, not an instance
<class '__main__.Foo'>
>>> print(MyClass()) # you can create an object from this class
<__main__.Foo object at 0x89c6d4c>
```

但这并不是那么动态，因为您仍然必须自己编写整个类。

由于类是对象，因此它们必须由某种东西生成。

当您使用`class`关键字时，Python会自动创建此对象。但是，与Python中的大多数事情一样，它为您提供了一种手动进行操作的方法。

还记得功能`type`吗？一个非常强大的一个函数：

```python
>>> print(type(1))
<type 'int'>
>>> print(type("1"))
<type 'str'>
>>> print(type(ObjectCreator))
<type 'type'>
>>> print(type(ObjectCreator()))
<class '__main__.ObjectCreator'>
```

嗯，[`type`](http://docs.python.org/2/library/functions.html#type)具有完全不同的能力，它也可以动态创建类。`type`可以将一个类的描述作为参数，并返回一个类。

（我知道，根据传递给它的参数，同一个函数可以有两种完全不同的用法是很愚蠢的。由于Python中的向后兼容性，这是一个问题）

`type` 这样工作：

```python
type(name, bases, attrs)
```

在哪里：

- **`name`**：类名称
- **`bases`**：父类的元组（对于继承，可以为空）
- **`attrs`**：包含属性名称和值的字典

例如：

```python
>>> class MyShinyClass(object):
...       pass
```

可以通过以下方式手动创建：

```python
>>> MyShinyClass = type('MyShinyClass', (), {}) # returns a class object
>>> print(MyShinyClass)
<class '__main__.MyShinyClass'>
>>> print(MyShinyClass()) # create an instance with the class
<__main__.MyShinyClass object at 0x8997cec>
```

您会注意到，我们使用“ MyShinyClass”作为类的名称和变量来保存类引用。它们可以不同，但是没有理由使事情复杂化。

`type`接受字典来定义类的属性。所以：

```python
>>> class Foo(object):
...       bar = True
```

可以翻译为：

```python
>>> Foo = type('Foo', (), {'bar':True})
```

并用作普通类：

```python
>>> print(Foo)
<class '__main__.Foo'>
>>> print(Foo.bar)
True
>>> f = Foo()
>>> print(f)
<__main__.Foo object at 0x8a9b84c>
>>> print(f.bar)
True
```

当然，您可以从中继承，因此：

```python
>>>   class FooChild(Foo):
...         pass
```

将会：

```python
>>> FooChild = type('FooChild', (Foo,), {})
>>> print(FooChild)
<class '__main__.FooChild'>
>>> print(FooChild.bar) # bar is inherited from Foo
True
```

最终，您需要向类中添加方法。只需定义具有适当签名的函数并将其分配为属性即可。

```python
>>> def echo_bar(self):
...       print(self.bar)
...
>>> FooChild = type('FooChild', (Foo,), {'echo_bar': echo_bar})
>>> hasattr(Foo, 'echo_bar')
False
>>> hasattr(FooChild, 'echo_bar')
True
>>> my_foo = FooChild()
>>> my_foo.echo_bar()
True
```

在动态创建类之后，您可以添加更多方法，就像将方法添加到正常创建的类对象中一样。

```python
>>> def echo_bar_more(self):
...       print('yet another method')
...
>>> FooChild.echo_bar_more = echo_bar_more
>>> hasattr(FooChild, 'echo_bar_more')
True
```

您会看到我们研究的方向：在Python中，类是对象，您可以动态动态地创建一个类。

这就是Python在使用关键字`class`时所做的事情，并且通过使用元类来做到这一点。

# 什么是元类（最终）

元类是创建类的“东西”。

您定义类是为了创建对象，对吗？

但是我们了解到Python类是对象。

好吧，元类是创建这些对象的东西。它们是类的类，您可以通过以下方式对其进行描绘：

```python
MyClass = MetaClass()
my_object = MyClass()
```

您已经看到，`type`您可以执行以下操作：

```python
MyClass = type('MyClass', (), {})
```

这是因为该函数`type`实际上是一个元类。`type`是Python用于在幕后创建所有类的元类。

现在，您想知道为什么用小写而不是小写`Type`？

好吧，我想这与`str`，创建字符串对象`int`的类和创建整数对象的类的一致性有关。`type`只是创建类对象的类。

您可以通过检查`__class__`属性来看到。

一切，我的意思是一切，都是Python中的对象。其中包括整数，字符串，函数和类。它们都是对象。所有这些都是从一个类创建的：

```python
>>> age = 35
>>> age.__class__
<type 'int'>
>>> name = 'bob'
>>> name.__class__
<type 'str'>
>>> def foo(): pass
>>> foo.__class__
<type 'function'>
>>> class Bar(object): pass
>>> b = Bar()
>>> b.__class__
<class '__main__.Bar'>
```

现在，什么是`__class__`任何`__class__`？

```python
>>> age.__class__.__class__
<type 'type'>
>>> name.__class__.__class__
<type 'type'>
>>> foo.__class__.__class__
<type 'type'>
>>> b.__class__.__class__
<type 'type'>
```

因此，元类只是创建类对象的东西。

如果愿意，可以将其称为“；类工厂”。

`type` 是Python使用的内置元类，但是您当然可以创建自己的元类。

# 该[`__metaclass__`](http://docs.python.org/2/reference/datamodel.html?highlight=__metaclass__#__metaclass__)属性

在Python 2中，您可以`__metaclass__`在编写类时添加属性（有关Python 3语法，请参见下一部分）：

```python
class Foo(object):
    __metaclass__ = something...
    [...]
```

如果这样做，Python将使用元类来创建class `Foo`。

小心点，这很棘手。

您`class Foo(object)`先编写，但`Foo`尚未在内存中创建类对象。

Python将`__metaclass__`在类定义中查找。如果找到它，它将使用它来创建对象类`Foo`。如果没有，它将 `type`用于创建类。

读几次。

当您这样做时：

```python
class Foo(Bar):
    pass
```

Python执行以下操作：

`Foo`中有`__metaclass__`属性`Foo`吗？

如果是的话，在内存中创建一个类对象（我说的是类对象，请跟紧我思路），`Foo`使用是什么`__metaclass__`。

如果Python找不到`__metaclass__`，它将`__metaclass__`在MODULE级别查找a ，然后尝试执行相同的操作（但仅适用于不继承任何内容的类，基本上是旧式类）。

然后，如果根本找不到任何对象`__metaclass__`，它将使用`Bar`的（第一个父对象）自己的元类（可能是默认的`type`）创建类对象。

请注意，该`__metaclass__`属性将不会被继承，父（`Bar.__class__`）的元类将被继承。如果`Bar`使用的`__metaclass__`是创建的属性`Bar`与`type()`（不是`type.__new__()`），子类不会继承该行为。

现在的问题就是，你可以在__metaclass__中放置些什么代码呢？答案就是：可以创建一个类的东西。那么什么可以用来创建一个类呢？type，或者任何使用到type或者子类化type的东东都可以。

# Python 3中的元类

设置元类的语法在Python 3中已更改：

```python
class Foo(object, metaclass=something):
    ...
```

即`__metaclass__`不再使用该属性，而在基类列表中使用关键字参数。

但是，元类的行为[基本](https://www.python.org/dev/peps/pep-3115/)保持[不变](https://www.python.org/dev/peps/pep-3115/)。

在Python 3中，您还可以将属性作为关键字参数传递给元类，如下所示：

```python
class Foo(object, metaclass=something, kwarg1=value1, kwarg2=value2):
    ...
```

阅读以下部分以了解python如何处理此问题。

# 自定义元类

元类的主要目的是在创建类时自动更改它。

通常，您要对API进行此操作，在API中要创建与当前上下文匹配的类。

想象一个愚蠢的示例，在该示例中，您决定模块中的所有类的属性都应以大写形式编写。有几种方法可以执行此操作，但是一种方法是`__metaclass__`在模块级别进行设置。

这样，将使用此元类创建该模块的所有类，而我们只需要告诉元类将所有属性都转换为大写即可。

幸运的是，`__metaclass__`实际上可以是任何可调用的，它不需要是正式的类（我知道，名称中带有“ class”的东西不必是类，请弄清楚……但这很有用）。

因此，我们将从使用函数的简单示例开始。

```python
# the metaclass will automatically get passed the same argument
# that you usually pass to `type`
def upper_attr(future_class_name, future_class_parents, future_class_attrs):
    """
      Return a class object, with the list of its attribute turned
      into uppercase.
    """
    # pick up any attribute that doesn't start with '__' and uppercase it
    uppercase_attrs = {
        attr if attr.startswith("__") else attr.upper(): v
        for attr, v in future_class_attrs.items()
    }

    # let `type` do the class creation
    return type(future_class_name, future_class_parents, uppercase_attrs)

__metaclass__ = upper_attr # this will affect all classes in the module

class Foo(): # global __metaclass__ won't work with "object" though
    # but we can define __metaclass__ here instead to affect only this class
    # and this will work with "object" children
    bar = 'bip'
```

让我们检查：

```python
>>> hasattr(Foo, 'bar')
False
>>> hasattr(Foo, 'BAR')
True
>>> Foo.BAR
'bip'
```

现在，让我们做完全一样的事情，但是对元类使用真实的类：

```python
# remember that `type` is actually a class like `str` and `int`
# so you can inherit from it
class UpperAttrMetaclass(type):
    # __new__ is the method called before __init__
    # it's the method that creates the object and returns it
    # while __init__ just initializes the object passed as parameter
    # you rarely use __new__, except when you want to control how the object
    # is created.
    # here the created object is the class, and we want to customize it
    # so we override __new__
    # you can do some stuff in __init__ too if you wish
    # some advanced use involves overriding __call__ as well, but we won't
    # see this
    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attrs):
        uppercase_attrs = {
            attr if attr.startswith("__") else attr.upper(): v
            for attr, v in future_class_attrs.items()
        }
        return type(future_class_name, future_class_parents, uppercase_attrs)
```

让我们重写上面的内容，但是现在有了更短，更实际的变量名，我们知道它们的含义了：

```python
class UpperAttrMetaclass(type):
    def __new__(cls, clsname, bases, attrs):
        uppercase_attrs = {
            attr if attr.startswith("__") else attr.upper(): v
            for attr, v in attrs.items()
        }
        return type(clsname, bases, uppercase_attrs)
```

您可能已经注意到了额外的争论`cls`。它没有什么特别的：`__new__`始终将其定义的类作为第一个参数。就像您`self`将接收实例作为第一个参数的普通方法或类方法的定义类一样。

但这不是适当的OOP。我们正在`type`直接致电，而不是覆盖或致电父母的`__new__`。让我们改为这样做：

```python
class UpperAttrMetaclass(type):
    def __new__(cls, clsname, bases, attrs):
        uppercase_attrs = {
            attr if attr.startswith("__") else attr.upper(): v
            for attr, v in attrs.items()
        }
        return type.__new__(cls, clsname, bases, uppercase_attrs)
```

通过使用`super`，我们可以使其更加整洁，这将简化继承（因为是的，您可以具有元类，从元类继承，从类型继承）：

```python
class UpperAttrMetaclass(type):
    def __new__(cls, clsname, bases, attrs):
        uppercase_attrs = {
            attr if attr.startswith("__") else attr.upper(): v
            for attr, v in attrs.items()
        }
        return super(UpperAttrMetaclass, cls).__new__(
            cls, clsname, bases, uppercase_attrs)
```

哦，在python 3中，如果您使用关键字参数进行此调用，如下所示：

```python
class Foo(object, metaclass=MyMetaclass, kwarg1=value1):
    ...
```

它将在元类中转换为使用它：

```python
class MyMetaclass(type):
    def __new__(cls, clsname, bases, dct, kwargs1=default):
        ...
```

就是这样。实际上，关于元类的更多信息了。

使用元类的代码之所以复杂，其原因不是因为元类，而是因为您通常使用元类依靠自省，操纵继承和var等变量来扭曲事物`__dict__`。

确实，元类对于做黑魔法特别有用，因此也很复杂。但就其本身而言，它们很简单：

- 拦截类的创建
- 修改班级
- 返回修改后的类

# 为什么要使用元类类而不是函数？

既然`__metaclass__`可以接受任何可调用对象，那么为什么要使用一个类，因为它显然更复杂？

这样做有几个原因：

- 意图很明确。当您阅读时`UpperAttrMetaclass(type)`，您会知道接下来会发生什么
- 您可以使用OOP。元类可以继承元类，重写父方法。元类甚至可以使用元类。
- 如果您指定了元类类，但没有元类函数，则该类的子类将是其元类的实例。
- 您可以更好地构建代码。绝对不要像上面的示例那样使用元类来处理一些琐碎的事情。通常用于复杂的事情。能够制作几种方法并将它们分组在一个类中的能力对于使代码更易于阅读非常有用。
- 您可以勾上`__new__`，`__init__`和`__call__`。这将使您可以做不同的事情，即使通常您可以全部完成所有工作`__new__`，有些人还是更乐于使用`__init__`。
- 这些被称为元类，该死！它一定意味着什么！

# 为什么要使用元类？

现在是个大问题。为什么要使用一些晦涩的易错功能？

好吧，通常您不会：

> 元类是更深层的魔术，99％的用户永远不必担心它。如果您想知道是否需要它们，则不需要（实际上需要他们的人可以肯定地知道他们需要它们，并且不需要解释原因）。

*Python大师Tim Peters*

元类的主要用例是创建一个API。一个典型的例子是Django ORM。它允许您定义如下内容：

```python
class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
```

但是，如果您这样做：

```python
person = Person(name='bob', age='35')
print(person.age)
```

它不会返回`IntegerField`对象。它将返回一个`int`，甚至可以直接从数据库中获取它。

这是可能的，因为`models.Model`define`__metaclass__`并使用了一些魔术，这些魔术将使`Person`您使用简单的语句定义的对象变成对数据库字段的复杂钩子。

Django通过公开一个简单的API并使用元类，从该API重新创建代码来完成幕后的实际工作，从而使看起来复杂的事情变得简单。

# 最后一个字

首先，您知道类是可以创建实例的对象。

好吧，实际上，类本身就是实例。元类。

```python
>>> class Foo(object): pass
>>> id(Foo)
142630324
```

一切都是Python中的对象，它们都是类的实例或元类的实例。

除了`type`。

`type`实际上是它自己的元类。这不是您可以在纯Python中复制的东西，而是通过在实现级别上作弊来完成的。

其次，元类很复杂。您可能不希望将它们用于非常简单的类更改。您可以使用两种不同的技术来更改类：