# 终极无敌下载链接

```python
下载包
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn aircv==1.4.6

生成requirements.txt文件
pip freeze > ./requirements.txt

下载安装requirements.txt里面的全部包
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

# PIP升级

```python
python -m pip install --upgrade pip -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
```



# 生成requirement.txt文件

Pyhon项目中，一般都会有一个 `requirements.txt` 文件，这个文件主要是用于记录当前项目下的所有依赖包及其精确的版本号，以方便在一个新环境下更快的进行部署。

## 使用 pip freeze 生成

一般情况，我们可以直接使用Python下的 `pip` 包管理工具，来生成 requirements.txt 文件，命令如下：

```
点我复制pip freeze > D:\pycharm\requirements.txt
```

其中，`D:\pycharm\requirements.txt` 为生成的 requirements.txt 文件的具体路径。通过这个 `pip freeze` 方式生成时，会把整个Python环境下的所有包都列出生成，比较适用于Python项目为虚拟环境的情况。

## 使用 pipreqs 生成

我们还可以通过第三方库 `pipreqs` 来生成 requirements.txt 文件，这个方式有一个好处，那就是它可以只生成我们当前Python项目中所用到的依赖包及其版本号，而不是像 `pip freeze` 方式一样把所有包全部列出生成。

- **安装pipreqs**

可以直接通过 `pip` 来安装 `pipreqs`，安装命令：

```
点我复制pip install pipreqs
```

安装后通过 `pip show pipreqs` 查看，我这里安装的版本是 `0.4.10`。

```
点我复制D:\>pip3 show pipreqs
Name: pipreqs
Version: 0.4.10
Summary: Pip requirements.txt generator based on imports in project
Home-page: https://github.com/bndr/pipreqs
Author: Vadim Kravcenko
Author-email: vadim.kravcenko@gmail.com
License: Apache License
Location: d:\python\installation\lib\site-packages
Requires: yarg, docopt
Required-by:
```

- **使用pipreqs**

`pipreqs` 使用起来也很容易，命令使用方式为：`pipreqs 当前Python项目的根目录`。

```
点我复制D:\>pipreqs D:\pycharm\Code\flaskDemo
Traceback (most recent call last):
  File "d:\python\installation\lib\runpy.py", line 193, in _run_module_as_main
    "__main__", mod_spec)
  File "d:\python\installation\lib\runpy.py", line 85, in _run_code
    exec(code, run_globals)
  File "D:\Python\installation\Scripts\pipreqs.exe\__main__.py", line 9, in <module>
  File "d:\python\installation\lib\site-packages\pipreqs\pipreqs.py", line 470, in main
    init(args)
  File "d:\python\installation\lib\site-packages\pipreqs\pipreqs.py", line 409, in init
    follow_links=follow_links)
  File "d:\python\installation\lib\site-packages\pipreqs\pipreqs.py", line 122, in get_all_imports
    contents = f.read()
UnicodeDecodeError: 'gbk' codec can't decode byte 0x84 in position 100: illegal multibyte sequence
```

在执行时，可能会出现上面提示编码方式不对的情况，为解决这个问题，我们可以在执行命令中指定编码方式为 `utf-8` ，如下：

```
点我复制D:\>pipreqs D:\pycharm\Code\flaskDemo --encoding=utf8
INFO: Successfully saved requirements file in D:\pycharm\Code\flaskDemo\requirements.txt
```

如果我们Python项目的根目录中已存在 `requirements.txt` ，那么使用上面命令就会出现警告：

```
点我复制D:\>pipreqs D:\pycharm\Code\flaskDemo --encoding=utf-8
WARNING: Requirements.txt already exists, use --force to overwrite it
```

警告信息中的提示，告诉我们可以使用参数 `--force` 来覆盖重新生成 `requirements.txt` ，如下：

```
点我复制pipreqs D:\pycharm\Code\flaskDemo --encoding=utf-8 --force
```

## 执行requirement.txt

生成 `requirement.txt` 后，我们查看其发现是这样的格式：

```
点我复制PyMySQL==0.9.3
Flask==1.0.3
redis==3.4.1
```

那么，对于 requirement.txt 中列出的第三方库，应该如何去执行并安装呢？安装方式很简单，我们通过 `pip` 工具，执行命令：`pip install -r requirements.txt` ，该命令会把 `requirements.txt` 文件中列出的库依次进行安装，最后等待安装完成即可。

