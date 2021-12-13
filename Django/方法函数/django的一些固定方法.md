

#### 一、重定向

```python
from django.shortcuts import redirect
```



源码一下：

```python
def redirect(to, *args, permanent=False, **kwargs):
    """
    将 HttpResponseRedirect 返回到传递的参数的适当 URL。
    这个参数可以是
        一个模块：这个模块的`get_absolute_url()` 函数将被调用。
        视图名称，可能带有参数：`urls.reverse()` 将用于反向解析名称。
        一个 URL，将按原样用于重定向位置。
    默认情况下发出临时重定向；
    通过 Permanent=True 发出永久重定向
    """
    redirect_class = HttpResponsePermanentRedirect if permanent else HttpResponseRedirect
    return redirect_class(resolve_url(to, *args, **kwargs))
```

- ```python
	return redirect(to='/')				# 临时重定向到127.0.0.1：8080/,y
	```

- ```
	return redirect(to='/news/xxx')		# 重定向到其他地方，根据url
	```

	



**301: 临时重定向**： 主机域名没有发生改变

**302：永久重定向**：主机域名都发送了改变