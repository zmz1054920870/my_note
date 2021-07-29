<strong>前言</strong>：如果你想引入别人的项目，但是引入的项目可能与自己原先装的模块的版本产生冲突，那最好的办法就是在虚拟环境中引入，这样就可以以一个独立的环境引入别人的项目，需要什么模块在虚拟环境下进行下载即可，就不会破坏自己本地的环境。



<strong>步骤</strong>

*  如果别人的环境中，存在venv，你可以先把venv给删除了
* file—>settings—>Project Interpreter—>Add Local…
*  后续就和新建虚拟环境一样了（比如我的虚拟环境是建立在D:\client-test中的）
   * 可以建立在当前项目文件中也可以在其他地方建立
   * 虚拟环境建立好以后，D:\client-test中生成你的虚拟环境和依赖包，同时在D:\client-test\Scripts中会生成一个activate.bat文件，这个就是虚拟机的bash界面


#### 怎么给虚拟环境中安装包

* 首先在pycharm的Terminal中执行，cd D:\client-test\Scripts 进入Script文件夹
* 然后输入activate.bat 这个文件名（必须这样不能cd D:\client-test\Scripts\activate.bat，这样是不能进入的）
* 下载我们的依赖包 pip install -i 模块名 http://pypi.douban.com/simple/



#### 怎么退出虚拟环境

* 首先，cd D:\client-test\Scripts
* 然后，deactivate



```
aircv==1.4.6
```



#### 如何找到我们的python安装路径

* CMD
* import sys
* sys.path