### 一、主导航栏



1.File、Edit、View、Proxy、Tools、Window、Help

2.View栏

（1）structure视图是将网络请求按访问的域名分类；

（2）Sequence 视图是将网络请求按访问的时间排序



### 二、主界面介绍



![img](charles-01.png)

































1. 因为插件页面使用了咚咚客户端提供的接口，开发/测试时需要将本地前端文件代理到咚咚客户端插件访问的前端html地址，以达到本地调试/测试的需求
2. 要求windows环境
3. 安装[京麦客户端](https://jm.jd.com/index/index.html)，安装成功后打开安装目录下的dongdong文件夹

1. 将[devtools_resources.pak](https://cdn.xiaoduoai.com/dongdong/devtools_resources.pak)下载下来复制进去
2. 打开commonConfig.ini文件作如下修改（只需要修改下面两项）（注意⚠️：第一次安装需要打开咚咚客户端后才会有该文件，建议用notepad++来修改）



修改后如下所示（咚咚每个版本默认配置不一样，以下仅供参考）：

![](charles-02.png)





经过上面两步操作后才可以打开咚咚插件的调试窗口（F12）

1. 安装晓多客户端（找对应客户端开发同事要，要求关闭抓包工具检测，否则会导致晓多客户端与抓包工具冲突而无法打开晓多客户端）
2. 安装[charles](https://www.charlesproxy.com/)（范强后下载更快），安装后需要配置https证书（为抓取https包），SOCKS Proxy（为抓取websocket包），为后续代理调试作准备

![image-20210729113842364](charles-03.png)        

​                  ![](charles-04.png)  

​        ![](charles-05.png)

​        ![](charles-06.png)

​                 ![](charles-07.png)        

​                 ![](charles-08.png)        

​                 ![](charles-09.png)        

​                 ![](charles-10.png)

 ![](charles-11.png)       

​                 ![](charles-12.png)        

![](charles-13.png)



在可以抓https包了😄                        

​                

![](charles-14.png)





![](charles-15.png)



![](charles-16.png)



​        

现在可以抓websocket包了😄！

基本配置完成✅，如果觉得charles因为没有Register使用半小时就会自动关闭的话，可以在网上搜索激活码，很容易搜到哦😁

1. 上面所有准备完毕后，打开京麦咚咚，再在咚咚右侧应用中心里打开晓多机器人（即插件），再打开charles和晓多客户端（客户端必须和插件配置为同一环境）

![](charles-17.png)

再用charles将线上html文件请求代理到前端打包后dist文件夹里的index.html文件

​                 

![](charles-18.png)        

![](charles-19.png)





代理后再刷新插件页面，然后用同样的操作将其它文件（如.js、.css、图片等）代理到本地

大功告成！这样就实现了在咚咚客户端里面访问本地前端文件了😁