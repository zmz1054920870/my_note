## 设置



#### 开关

```
file -- Capture Traffic  ✔选上以后才可以抓包（capture traffic :捕获流量）
```



#### 证书

```
1.fiddler默认是这可以转http请求的，所以我们要安装证书
2. Tools -- Options -- https(里面的全部打勾) -- Acations -- yes
	capture HTTPS connects:捕获HTTPS链接
	Decrypt HTTPS traffic:解密HTTPs
	Ignore server certificate err（unsafe）：忽略服务器证书错误（不安全）
	check for certificate revocation:
	
```



#### 简单过滤

```
Rules -- 	Hide Image request（隐藏图片请求）
			Hide CONNECTS（隐藏链接）
```



#### 快捷操作

```
1.在请求和响应中，点击‘Raw’ -- ‘View in notepad’ 在记事本中显示
```

