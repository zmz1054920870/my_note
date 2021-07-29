```python
import os
import time
import json
from locust import (TaskSet, task, events, Locust)
import websocket


def send_websocket_request_(ws, req_type, req_para=None):
    if req_type == 'elevate':
        data = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": req_para,
                "objectGroup": "console",
                "includeCommandLineAPI": True,
                "doNotPauseOnExceptions": False,
                "returnByValue": True
            }
        }
        ws.send(json.dumps(data))


class WsClient(object):
    """重写self.client"""

    def __init__(self):
        ws_path = "ws://localhost:33229/devtools/page/E2BCA803-1715-4151-A019-BC2CDD2D9EBC"
        self.ws = websocket.create_connection(ws_path)

    def send_js(self):
        req_para = ("ROM.on('ali-gateway-test','{\"path\": \"test\",\"res_time\": \"15\",\"res_size\": \"30\"}');")
        send_websocket_request_(self.ws, 'elevate', req_para)
        result = self.ws.recv()
        return result

    def connect(self):
        """grpc实例"""
        # 记录开始时间
        start_time = int(time.time())
        try:
            # 参数实例
            self.send_js()
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(
                request_type='grpc',
                name=r'/generateSnowid',
                response_time=total_time,
                response_length=0
            )
        except Exception as e:
            print(e)
            print(e.args)
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type='grpc',
                name='/generateSnowid',
                response_time=total_time,
                exception=e
            )


class GrpcLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(GrpcLocust, self).__init__(*args, **kwargs)
        self.client = WsClient()


class WsTask(TaskSet):
    """压测任务"""

    @task
    def generateSnowid(self):
        self.client.connect()


class WebsiteUser(GrpcLocust):
    task_set = WsTask
    min_wait = 10
    max_wait = 20


if __name__ == '__main__':
    os.system("locust -f rongheban.py --host=http://127.0.0.1")
```

