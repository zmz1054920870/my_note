#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : kernel_driver_up.py
import websocket
import requests
import time
import json
from config.globalparams import log
from websocket import WebSocketException

"""

代码错误 -- {'result': {'id': 1, 'result': {'result': {'type': 'object', 'subtype': 'error', 'className': 'DOMException', ' , 'preview': {'type': 'object', 'subtype': 'error', 'description': 'DOMException: Failed to execute \'evaluate\' on \'Document\': The string \'//pr"e[@name="sendBox"]\' is not a valid XPath expression.\n    at <anonymous>:1:22', 'overflow': False, 'properties': [{'name': 'stack', 'type': 'accessor'}, {'name': 'code', 'type': 'number', 'value': '12'}, {'name': 'name', 'type': 'string', 'value': 'SyntaxError'}, {'name': 'message', 'type': 'string', 'value': 'Failed to execute \'evaluate\' on \'Document\': The st…name="sendBox"]\' is not a valid XPath expression.'}]}}, 'exceptionDetails': {'exceptionId': 33, 'text': 'Uncaught', 'lineNumber': 0, 'columnNumber': 21, 'scriptId': '1113', 'stackTrace': {'callFrames': [{'functionName': '', 'scriptId': '1113', 'url': '', 'lineNumber': 0, 'columnNumber': 21}]}, 'exception': {'type': 'object', 'subtype': 'error', 'className': 'DOMException', 'description': 'DOMException: Failed to execute \'evaluate\' on \'Document\': The string \'//pr"e[@name="sendBox"]\' is not a valid XPath expression.\n    at <anonymous>:1:22', 'objectId': '2639001961805784748.2.2', 'preview': {'type': 'object', 'subtype': 'error', 'description': 'DOMException: Failed to execute \'evaluate\' on \'Document\': The string \'//pr"e[@name="sendBox"]\' is not a valid XPath expression.\n    at <anonymous>:1:22', 'overflow': False, 'properties': [{'name': 'stack', 'type': 'accessor'}, {'name': 'code', 'type': 'number', 'value': '12'}, {'name': 'name', 'type': 'string', 'value': 'SyntaxError'}, {'name': 'message', 'type': 'string', 'value': 'Failed to execute \'evaluate\' on \'Document\': The st…name="sendBox"]\' is not a valid XPath expression.'}]}}}}}}
index = 1 -- {'id': 1, 'result': {'result': {'type': 'object', 'subtype': 'node', 'className': 'HTMLDivElement', 'description': 'div.main', 'objectId': '2639001961805784748.2.1'}}}
index = 300 -- {'reslut': {'id': 1, 'result': {'result': {'type': 'object', 'subtype': 'null', 'value': None}}}}

"""



class RunJs(object):
    """
    单例模式， 单例以后，才能共享self.__ws_dict,不然每生成一个新的实例__ws_dict就会被重置

    """

    __instance = None
    __ws_dict = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(RunJs, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__invalid_ws_url = "ws://127.0.0.1:9222/devtools/page/ERROR"
        self.__error_ws_result = {"id": 0, "result": {"result": {"type": "undefined", "value": 'JS没有执行成功', "description": "0"}}}


    def get_url(self, title):
        """
            :param title: 页面title名字
            :return: ws://127.0.0.1:9222/devtools/page/ERROR

        """
        ws_url = self.__invalid_ws_url

        chrome_remote_url = 'http://127.0.0.1:9222/json'
        page = requests.get(url=chrome_remote_url).json()
        for i in page:
            if i['title'] == title:
                ws_url = i['webSocketDebuggerUrl']
        return ws_url

    def connect_ws(self, ws_url):
        """

        :param ws_url: get from get_url
        :return:None or object
        """
        count = 1
        while count < 4:
            try:
                ws = websocket.create_connection(ws_url)
                break
            except WebSocketException as e:  # 这里是防止，page突然打开了，然后又断开了，这个时候前面拿到的ws_url就无效了，就是防止失效
                log.warning('建立websocket失败,尝试{count}次'.format(count=count) + str(e))
                time.sleep(2)
                ws = None
            finally:
                count += 1
        return ws

    def try_run(self, title, js):
        ws_url = self.get_url(title)
        if ws_url == self.__invalid_ws_url:
            self.__ws_dict[title] = None
            return {'code': False, 'reason': '没有获取到ws_url', 'result': self.__error_ws_result}
        ws = websocket.create_connection(url=ws_url)
        if ws is None:
            self.__ws_dict[title] = None
            return {'code': False, 'reason': '创建ws的时候，ws_url已无效', 'result': self.__error_ws_result}
        payload = {
            'id': 1,
            'method': 'Runtime.evaluate',
            'params': {'expression': js}
        }
        try:
            data = json.dumps(payload)
            ws.send(data)
            res = ws.recv()
        except ConnectionAbortedError as e:
            self.__ws_dict[title] = None
            return {'code': False, 'reason': 'send(data)的时候ws断开或者无效', 'result': self.__error_ws_result}
        msg = json.loads(res)
        self.__ws_dict[title] = ws
        return {'code': True, 'reason': 'success', 'result': msg}

    def run_js(self, title, js):
        """
        :return: {"id":1,"result":{"result":{"type":"number","value":100,"description":"100"}}}
        """
        ws = self.__ws_dict.get(title, None)
        # log.error(self.__ws_dict)
        if ws is None:
            result = self.try_run(title, js)
            return result
        payload = {
            'id': 1,
            'method': 'Runtime.evaluate',
            'params': {'expression': js}
        }
        try:
            data = json.dumps(payload)
            # log.info(data)
            ws.send(data)
            result = ws.recv()
            msg = json.loads(result)
            result = {'code': True, 'reason': 'success', 'result': msg}
            return result
        except ConnectionAbortedError as e:
            result = self.try_run(title, js)
            return result


if __name__ == '__main__':
    temp = RunJs()
    js = """var a = document.evaluate('//pre[@name="sendBox"]',document.documentElement, null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)"""
    # js2 = "a.snapshotItem(0).getAttribute('class')"
    js2 = "a.snapshotItem(0).innerHTML='防止转接,自动发送'"
    js3 = """var b = document.evaluate('//div[@class="jimi-btn input-field--send-btn panda"]',document.documentElement, null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)"""
    js4 = "b.snapshotItem(0).click()"
    temp.run_js('在线客服', js)
    temp.run_js("在线客服", js2)
    temp.run_js("在线客服", js3)
    temp.run_js("在线客服", js4)
    while True:
        time.sleep(2)
        temp.run_js("在线客服", js2)
        temp.run_js("在线客服", js4)


    # res2 = temp.run_js('百度一下，你就知道', js2)
    # print(res2)
    #
    # res3 = temp.run_js('百度一下，你就知道', js3)
    # print(res3)
































    # baidu_command = "document.querySelector('#kw').value=1"
    # baidu_command2 = "document.querySelector('#kw').value=2"
    # baidu_command3 = "document.querySelector('#kw').value=3"
    # # online_command = "document.querySelector('.send-textarea')"
    # online_command = "var {element} = document.evaluate('{xpath}',document.documentElement, null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)"
    # # online_command = "document.querySelector('.send-textarea')"
    #
    # online_command2 = "document.querySelector('.send-textarea').innerText = 2"
    # online_command3 = "document.querySelector('.send-textarea').innerText = 3"
    # # def quotation_switch(js):
    # #     str_list = []
    # #     quota_res = []
    # #     for i in range(len(js)):
    # #         str_list.append(js[i])
    # #         if js[i] == "\'":
    # #             quota_res.append(i)
    # #     if len(quota_res) > 2:
    # #         for index in quota_res[1:-1]:
    # #             str_list[index] = "\""
    # #     else:
    # #         return js
    #
    # data = online_command.format(element='a', xpath = '//div')
    # # data = 'for i in rang'
    # res = temp.run_js('在线客服', data)
    # print(res)
    #
    # res = temp.run_js('在线客服', "a.snapshotLength")
    # print(res)
    #
    # res = temp.run_js('在线客服', 'b.innerText=200')
    # print(res)
    # # print(data)
    # # data = quotation_switch(data)
    # # print(data)
    # # print('---------', data)
    #
    #
    # # online_command2 = """var {element} = document.evaluate('{xpath}',document.documentElement, null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)"""
    # #
    # # data = online_command2.format(element="a", xpath="//pre[@name='sendBox']")
    # #
    # # res = temp.run_js('在线客服',data)
    # # print(res)
    #
    #
    # #     return ''.join(str_list)
    # # b = quotation_switch(data)
    # # print(b)
    # # js = "var a = document.evaluate('//pre[@name='sendBox']',document.documentElement, null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)"
    # # print(type(js))
    # #
    # # a = temp.run_js('在线客服', js)
    # # b = temp.run_js('在线客服', "a.")
    # # print(a)
    # # print(temp._RunJs__ws_dict)
    # # time.sleep(1)
    # # a = temp.run_js('百度一下，你就知道', baidu_command)
    # # print(temp._RunJs__ws_dict)
    # # time.sleep(1)
    # # a = temp.run_js('在线客服', online_command2)
    # # print(temp._RunJs__ws_dict)
    # # time.sleep(10)
    #
    # # temp2 = RunJs()
    # # a = temp2.run_js('百度一下，你就知道', baidu_command2)
    # # print(temp2._RunJs__ws_dict)
    # # time.sleep(1)
    # # a = temp2.run_js('在线客服', online_command3)
    # # print(temp2._RunJs__ws_dict)
