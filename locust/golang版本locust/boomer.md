## 背景

很早之前，考虑单机执行能力，使用locust做过公司短信网关的压测工作，后来发现了一个golang版本的locust，性能是python版本的5到10倍以上，但是一直没有机会使用。

最近公司想做一个性能测试平台，技术选型要求和开发的语言一致，即golang，所以我想到了boomer，本文为boomer的使用记录。

## 环境安装

|   开发环境    |              安装               |
| :-----------: | :-----------------------------: |
|  Python 3.7   |               略                |
| locust 0.11.0 |      pip install locustio       |
|    golang     |               略                |
|    boomer     | go get github.com/myzhan/boomer |

> **注**：最新版本的boomer兼容了goczmq，需要将locust升级到较高版本才能完成兼容。

## 脚本编写

#### master

这部分的代码不重要，只要能启动就行。

```python
from locust import Locust, TaskSet, task


class MyTaskSet(TaskSet):
    @task(20)
    def hello(self):
        pass


class Dummy(Locust):
    task_set = MyTaskSet
```

#### slave节点（golang/boomer）

```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"

	"github.com/myzhan/boomer"
)

func getDemo() {
	start := time.Now()
	resp, err := http.Get("http://httpbin.org/get?name=Detector")

	if err != nil {
		log.Println(err)
		return
	}
	defer resp.Body.Close()
	fmt.Println(resp.Status)
	elapsed := time.Since(start)
	if resp.Status == "200 OK" {
		boomer.RecordSuccess("http", "sostreq", elapsed.Nanoseconds()/int64(time.Millisecond), int64(10))
	} else {
		boomer.RecordFailure("http", "sostreq", elapsed.Nanoseconds()/int64(time.Millisecond), "sostreq not equal")
	}
}

func postDemo() {
	start := time.Now()

	info := make(map[string]interface{})
	info["name"] = "Detector"
	info["age"] = 15
	info["loc"] = "深圳"
	// 将map解析未[]byte类型
	bytesData, _ := json.Marshal(info)
	// 将解析之后的数据转为*Reader类型
	reader := bytes.NewReader(bytesData)
	resp, _ := http.Post("http://httpbin.org/post",
		"application/json",
		reader)
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(body))
	elapsed := time.Since(start)
	if resp.Status == "200 OK" {
		boomer.RecordSuccess("http", "sostreq", elapsed.Nanoseconds()/int64(time.Millisecond), int64(10))
	} else {
		boomer.RecordFailure("http", "sostreq", elapsed.Nanoseconds()/int64(time.Millisecond), "sostreq not equal")
	}
}

func main() {
	task1 := &boomer.Task{
		Name: "sostreq",
		// The weight is used to distribute goroutines over multiple tasks.
		Weight: 20,
		Fn:     getDemo,
	}

	task2 := &boomer.Task{
		Name: "sostreq",
		// The weight is used to distribute goroutines over multiple tasks.
		Weight: 10,
		Fn:     postDemo,
	}
	boomer.Run(task1, task2)
}
```