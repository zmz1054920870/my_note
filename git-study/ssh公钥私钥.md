### 前言

很多朋友在用github管理项目的时候，都是直接使用https url克隆到本地，当然也有有些人使用 SSH url 克隆到本地。然而，为什么绝大多数人会使用https url克隆呢？

这是因为，使用https url克隆对初学者来说会比较方便，复制https url 然后到 git Bash 里面直接用clone命令克隆到本地就好了。而使用 SSH url 克隆却需要在克隆之前先配置和添加好 SSH key 。

因此，如果你想要使用 SSH url 克隆的话，你必须是这个项目的拥有者。否则你是无法添加 SSH key 的。

### https 和 SSH 的区别：

1、前者可以随意克隆github上的项目，而不管是谁的；而后者则是你必须是你要克隆的项目的拥有者或管理员，且需要先添加 SSH key ，否则无法克隆。

2、https url 在push的时候是需要验证用户名和密码的；而 SSH 在push的时候，是不需要输入用户名的，如果配置SSH key的时候设置了密码，则需要输入密码的，否则直接是不需要输入密码的。

### 在 github 上添加 SSH key 的步骤：

##### 第一步、首先，检查下自己之前有没有已经生成：

在开始菜单中打开git下的git bash（当然，在其他目录下打开git bash也是一样的）：
然后执行

```
ls -al ~/.ssh 
1
```

##### 第二步、如果能进入到.ssh文件目录下 ，则证明，之前生成过.ssh秘钥，可以直接使用里面的秘钥。

如果不能进入到.ssh文件目录下，则：

检测下自己之前有没有配置：

```
git config user.name和git config user.email（直接分别输入这两个命令）
1
```

如果之前没有创建，则执行以下命令：

```
git config –global user.name ‘xxxxx’ 
git config –global user.email ‘xxx@xx.xxx’
12
```

生成秘钥

```
ssh-keygen -t rsa -C ‘上面的邮箱’
1
```

代码参数含义：

-t 指定密钥类型，默认是 rsa ，可以省略。
-C 设置注释文字，比如邮箱。
-f 指定密钥文件存储文件名。

接着按3个回车

```
[root@localhost ~]# ssh-keygen -t rsa       <== 建立密钥对，-t代表类型，有RSA和DSA两种
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa):   <==密钥文件默认存放位置，按Enter即可
Created directory '/root/.ssh'.
Enter passphrase (empty for no passphrase):     <== 输入密钥锁码，或直接按 Enter 留空
Enter same passphrase again:     <== 再输入一遍密钥锁码
Your identification has been saved in /root/.ssh/id_rsa.    <== 生成的私钥
Your public key has been saved in /root/.ssh/id_rsa.pub.    <== 生成的公钥
The key fingerprint is:
SHA256:K1qy928tkk1FUuzQtlZK+poeS67vIgPvHw9lQ+KNuZ4 root@localhost.localdomain
The key's randomart image is:
+---[RSA 2048]----+
|           +.    |
|          o * .  |
|        . .O +   |
|       . *. *    |
|        S =+     |
|    .    =...    |
|    .oo =+o+     |
|     ==o+B*o.    |
|    oo.=EXO.     |
+----[SHA256]-----+

1234567891011121314151617181920212223
```

最后在.ssh目录下(C盘用户文件夹下)得到了两个文件：id_rsa（私有秘钥）和id_rsa.pub（公有密钥）

##### 第三步、如果想登陆远端，则需要将rsa.pub里的秘钥添加到远端。

首先，去.ssh目录下找到id_rsa.pub这个文件夹打开复制全部内容。

接着：

1.登录GitHub，进入你的Settings
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019061921352777.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1NDk1MzM5,size_16,color_FFFFFF,t_70)
2.会看到左边这些目录，点击SSH and GPG keys
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190619213552339.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1NDk1MzM5,size_16,color_FFFFFF,t_70)
3.创建New SSH key
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190619213619807.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1NDk1MzM5,size_16,color_FFFFFF,t_70)
4.粘贴你的密钥到你key输入框中
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190619213715333.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1NDk1MzM5,size_16,color_FFFFFF,t_70)
5.点击Add SSH key
6.再弹出窗口，输入你的GitHub密码，点击确认按钮。
7.到此，就大功告成了。

##### 第四步 测试。

在git命令窗口上输入ssh -T git@github.com 按回车键，如看到以下信息，那么就完美了。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190619221201430.png)