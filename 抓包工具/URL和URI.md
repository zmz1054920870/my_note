## 一、URL和URI的关系和区别

#### 1.1	区别如下

```python
1.URL:Uniform Resource Locator   统一资源定位符
  通过URL就可以找到服务器上的特定资源
  例如：http：//192.168.55.55:8080/logonDemo/logonServlet
       服务器ID是192.168.55.55 服务软件端口号8080

2.URI：Uniform Resource Identifier 统一资源标识符
  URI描述的是服务端上服务软件上某项目地址
  例如：/logonDemo/logonServlet

3.Path：路径
  描述的是项目或者模块中资源绝对路径（不是相对路径）
  例如：/logonServlet

4.idea中web项目tomcat配置（  request.getContextPath（） ）：
  http：//192.168.55.55:8080/logonDemo


综上： 1.URL  --->>>   http：//192.168.55.55:8080/logonDemo/logonServlet
      2.URI  --->>>   /logonDemo/logonServlet
      3.PATH  --->>>  /logonServlet		# 这里有一点争议
      4.request.getContextPath（） ---->>> http：//192.168.55.55:8080/logonDemo
```



#### 1.2	实例

**现有有个接口如下：**

```markdown
http://pdd.myjjing.com/robot/report_client?a=7090b53b5a3837da296402a0f39078b7c4ab855ff236308199556e710da8bbde78d410e904c515926a80339f25c88f0a&pin=cnpdd3906448625&platform=pdd&msg_time=1625563992&state=1&service_status=7&spin=cnpdd%E8%8B%97%E8%8B%97miao%3A%E6%99%93%E5%A4%9A%E6%B5%8B%E8%AF%95de%E6%9D%8E%E9%BE%99&send_msg_from=0
```



> **协议 = `http://`**

> **域名 =`pdd.myjjing.com`**

> **一级域名 = `pdd`**

> **二级域名 = `myjjing`**

> **域名扩展 = `com`**

> **域名 = `pdd.myjjing.com`**

> **url: **
>
> ```html
> http://pdd.myjjing.com/robot/report_client?a=7090b53b5a3837da296402a0f39078b7c4ab855ff236308199556e710da8bbde78d410e904c515926a80339f25c88f0a&pin=cnpdd3906448625&platform=pdd&msg_time=1625563992&state=1&service_status=7&spin=cnpdd%E8%8B%97%E8%8B%97miao%3A%E6%99%93%E5%A4%9A%E6%B5%8B%E8%AF%95de%E6%9D%8E%E9%BE%99&send_msg_from=0
> ```

> **full_uri = `等于url`**

> **uri: **
>
> ```html
> /robot/report_client?a=7090b53b5a3837da296402a0f39078b7c4ab855ff236308199556e710da8bbde78d410e904c515926a80339f25c88f0a&pin=cnpdd3906448625&platform=pdd&msg_time=1625563992&state=1&service_status=7&spin=cnpdd%E8%8B%97%E8%8B%97miao%3A%E6%99%93%E5%A4%9A%E6%B5%8B%E8%AF%95de%E6%9D%8E%E9%BE%99&send_msg_from=0
> ```

> **uri.path = `/robot/report_client`**

