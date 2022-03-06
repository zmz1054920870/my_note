# 一、`.gitignore` 文件忽略规则:

开头的/并不是标识文件夹的要表明仅忽略文件夹需要在名称后面添加 /，而不是前面.

要想忽略某文件夹，但其下部分文件不能忽略。则需要添加通配符*，然后在后面添加！开头的规则，来指出不忽略的文件或文件夹。

只要写了路径，即/左右两边都有字符，那么就是指的“绝对路径”(相对仓库的，仓库.git文件夹所在目录为根目录)，但可以用*来指定层级，指定第几层子目录下的某个文件夹。

空格不匹配任意文件，可作为分隔符，可用反斜杠转义

#开头的模式标识注释，可以使用反斜杠进行转义

! 开头的模式标识否定，该文件将会再次被包含，如果排除了该文件的父级目录，则使用 ! 也不会再次被包含。可以使用反斜杠进行转义

/ 结束的模式只匹配文件夹以及在该文件夹路径下的内容，但是不匹配该文件

/ 开始的模式匹配项目跟目录
如果一个模式不包含斜杠，则它匹配相对于当前 .gitignore 文件路径的内容，如果该模式不在 .gitignore 文件中，则相对于项目根目录

**匹配多级目录，可在开始，中间，结束

?通用匹配单个字符

[]通用匹配单个字符列表

# 二、常用匹配示例：

- `bin/`: 忽略所有路径下的bin文件夹，该文件夹下的所有内容都会被忽略，不忽略 bin 文件，最后以/结尾的表示文件夹

- `/bin`: 忽略根目录下的bin文件

- `/*.c`: 忽略根目录下的 cat.c文件，不忽略 build/cat.c
- `debug/*`.obj: 忽略 debug/io.obj，不忽略 debug/common/io.obj 和 tools/debug/io.obj
- `**/foo`: 忽略/foo, a/foo, a/b/foo等
- `a/**/b`: 忽略a/b, a/x/b, a/x/y/b等
- `!/bin/run.sh`: 不忽略 bin 目录下的 run.sh 文件
- `*.log`: 忽略所有 .log 文件(当*和非/字符连用的话，表示匹配任意多个字符，所以可以匹配所有路径)
- `config.php`: 忽略所有路径下的 config.php 文件



*前面啥也没有得话，表示匹配所有字符，所以可以代表多级目录



🔺Git不会忽略空目录。 它忽略所有目录。 在Git中，目录仅通过其内容隐式存在。 空目录没有内容，因此不存在。

# 三、 关于.gitignore规则不生效的问题

.gitignore只能忽略那些原来没有被track的文件，如果某些文件已经被纳入了版本管理中，则修改.gitignore是无效的。

解决方法就是先把本地缓存删除（改变成未track状态），然后再提交:

```bash
git rm -r --cached .
git add .
git commit -m 'update .gitignore'
```





定义Git全局的 .gitignore 文件
除了可以在项目中定义 .gitignore 文件外，还可以设置全局的 git .gitignore 文件来管理所有Git项目的行为。这种方式在不同的项目开发者之间是不共享的，是属于项目之上Git应用级别的行为。

这种方式也需要创建相应的 .gitignore 文件，可以放在C:/Users/用户名/目录下。然后在使用以下命令配置Git：

```bash
git config --global core.excludesfile ~/.gitignore
```

##### 自用的全局 .ignore 文件:

```bash


### IntelliJ IDEA ###
.idea
*.iws
*.iml
*.ipr
modules.xml

target/

**/.idea
**/*.iws
**/*.iml
**/*.ipr
**/modules.xml


**/mvnw
**/mvnw.cmd
**/.mvn
**/target/
**/.gitignore

### Maven ###
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar

### Java ###
# Compiled class file
*.class

```





# 四、Git忽略规则的优先级

在 .gitingore 文件中，每一行指定一个忽略规则，Git 检查忽略规则的时候有多个来源，它的优先级如下（由高到低）：

从命令行中读取可用的忽略规则

当前目录定义的规则

父级目录定义的规则，依次递推

$GIT_DIR/info/exclude 文件中定义的规则

core.excludesfile中定义的全局规则

Git 忽略规则匹配语法