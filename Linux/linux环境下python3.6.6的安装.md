### 1.官网下载py包

```
wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz
```



### 2.解压

```
tar -zxvf Python-3.6.6.tgz -C /usr/local
```



### 3.安装必要组件

```
第一个：yum install -y gcc
```

不装的话会报错：
安装gcc在./configure时会error,configure: error: no acceptable C compiler found in $PATH

```
第二个：	yum install openssl-devel
```

```
不装的话会报错：
会忽略pip安装失败,pip command not found ，但是没有error,
```

### 4.安装

```
cd Python-3.6.6
./configure --prefix=/usr/local/python3
make && make install
```



### 5.搞个软件节

```
ln -s /usr/local/python3/bin/python3.6 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```

