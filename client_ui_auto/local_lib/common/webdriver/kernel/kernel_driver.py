#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : kernel_driver.py=

import websocket
import requests
import os
import time
import json
import sys
from config.globalparams import log, read_config

default_title = read_config.get_config('projectConfig', 'title')


class RunJs(object):
    """
    防止创建多个实例
    API_FORMAT:content = [title: xxx, payload: {id:1, 'method': 'Runtime.evaluate', 'params': {'expression': 'js'}}]
    ['page_name', ws, 'page_name2': ws2]
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(RunJs, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.ws_dict = {}

    def get_ws(self, title):
        chrome_remote_url = 'http://127.0.0.1:9222/json'
        log.debug(chrome_remote_url)
        page = requests.get(url=chrome_remote_url).json()
        try:
            for i in page:
                if i['title'] == title:
                    ws_url = i['webSocketDebuggerUrl']
            ws = websocket.create_connection(url=ws_url)
        except Exception as e:
            log.error(e)
            return {'code': 'fail', 'ws': None}
        print(11111111111111111111111111)
        return {'code': 'success', 'ws': ws}

    def run_js(self, title, js):
        """
        :return: {"id":1,"result":{"result":{"type":"number","value":100,"description":"100"}}}
        """
        self.ws_dict.setdefault(title, self.get_ws(title))
        log.debug(self.ws_dict)
        payload = {
            'id': 1,
            'method': 'Runtime.evaluate',
            'params': {'expression': js}
        }
        ws = self.ws_dict.get(title)['ws']
        ws.send(json.dumps(payload))
        try:
            res = ws.recv()
        except ConnectionAbortedError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            log.error((exc_type, fname, exc_tb.tb_lineno))
            res = None
        finally:
            log.info(res)
            return res


if __name__ == '__main__':
    temp = RunJs()
    baidu_command = "document.querySelector('#kw').value=100"
    baidu_command2 = "document.querySelector('#kw').value='你好'"
    online_command = "document.querySelector('.send-textarea').innerText = 100"
    online_command2 = "document.querySelector('.send-textarea').innerText = '你好'"
    temp.run_js('在线客服', online_command)
    time.sleep(1)
    temp.run_js('百度一下，你就知道', baidu_command)
    time.sleep(1)
    temp.run_js('在线客服', online_command2)
    time.sleep(10)
    temp.run_js('百度一下，你就知道', baidu_command2)
    time.sleep(1)
    temp.run_js('在线客服', online_command)



    #ConnectionAbortedError: [WinError 10053] 你的主机中的软件中止了一个已建立的连接。


    # import requests
    #
    # while True:
    #     page = requests.get('http://127.0.0.1:9222/json').json()
    #     for i in page:
    #         if i['title'] == 'AutoTest商品4 红色【图片 价格 品牌 报价】-京东':
    #             print(1111)
