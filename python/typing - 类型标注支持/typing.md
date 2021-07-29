# [`typing`](https://docs.python.org/zh-cn/3.7/library/typing.html#module-typing)- 类型标注支持

**源码：** [Lib/typing.py](https://github.com/python/cpython/tree/3.7/Lib/typing.py)

```
注解  Python 运行时并不强制标注函数和变量类型。类型标注可被用于第三方工具，比如类型检查器、集成开发环境、静态检查器等。
```



**备注：这是源码库中我截取的特殊的且常用的**

```python
__all__ = [
    # Super-special typing primitives.
    'Any',
    'Callable',
    'ClassVar',
    'ForwardRef',
    'Generic',
    'Optional',
    'Tuple',
    'Type',
    'TypeVar',
    'Union',
    ....
    ]
```

## 一、取别名

**备注：类型别名是通过将类型赋值给别名来定义。在这个例子中， `Vector` 和 `List[float]` 将被视为可互换的同义词**

```python
from typing import List
Vector = List[float]

def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]

# typechecks; a list of floats qualifies as a Vector.
new_vector = scale(2.0, [1.0, -4.2, 5.4])
```





## 二、语法格式



#### 2.1	List

**正确格式**

```python
from typing import List
List[float]
```

**错误格式**

```python
from typing import List
List[float, float]
```

**正确格式**

```python
from typing import List
List[Union[str，List[float]]
```



#### 2.2	Tuple

**例子**

```python
from typing import Tuplie
Tuple[float, str] or Tuple[float]
```





#### 2.3	Callable

期望回调函数返回类型，可以使用 `Callable[[Arg1Type, Arg2Type], ReturnType]`。

例如

```python
from typing import Callable

def func(x):
    return str(x)
    

def feeder(get_next_item: Callable[[int], str]) -> None:	# Callable期望传入的回调函数返回字符串, 
    # Body
    pass

    
feeder(get_next_item=func)
```

通过用文字省略号替换类型提示中的参数列表： `Callable[...，ReturnType]`，可以声明可调用的返回类型，而无需指定调用签名。





#### 2.4 Union

联合类型； `Union[X, Y]` 意味着：要不是 X，要不是 Y。

使用形如 `Union[int, str]` 的形式来定义一个联合类型。细节如下:

- 参数必须是类型，而且必须至少有一个参数。

- 联合类型的联合类型会被展开打平，比如:

	```
	Union[Union[int, str], float] == Union[int, str, float]
	```

- 仅有一个参数的联合类型会坍缩成参数自身，比如:

	```
	Union[int] == int  # The constructor actually returns int
	```

- 多余的参数会被跳过，比如:

	```
	Union[int, str, int] == Union[int, str]
	```

- 在比较联合类型的时候，参数顺序会被忽略，比如:

	```
	Union[int, str] == Union[str, int]
	```



#### 2.5 可选类型

```
typing.``Optional
```

可选类型。

 `Optional[X]` 等价于 `Union[X, None]` 。

请注意，这与可选参数并非相同的概念。可选参数是一个具有默认值的参数。可选参数的类型注解并不因为它是可选的就需要 `Optional` 限定符。例如：

```python
def foo(arg: int = 0) -> None:
    ...
```

另一方面，如果允许显式地传递值 `None` ， 使用 `Optional` 也是正当的，无论该参数是否是可选的。例如：

```python
def foo(arg: Optional[int] = None) -> None:
    ...
```





## 三、自定义类型 - `NewType`

**备注：使用 [`NewType()`](https://docs.python.org/zh-cn/3.7/library/typing.html#typing.NewType)建不同的类型:**







## 四、