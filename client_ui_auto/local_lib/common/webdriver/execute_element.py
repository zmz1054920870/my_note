#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : execute_element.py

from local_lib.common.webdriver.command import Command
from local_lib.common.webdriver.kernel.kernel_driver_up import RunJs
from config.globalparams import log


class ExecuteElement(object):

    def __new__(cls, title, object_id, index=0, *args, **kwargs):
        cls.object_id = object_id
        cls.title = title
        cls.index = index
        return super(ExecuteElement, cls).__new__(cls)

    @classmethod
    def __execute(self, js):
        js_executor = RunJs()
        res = js_executor.run_js(self.title, js)
        log.error("ExecuteElement.__execute\t" + str(res))
        if res['code'] == False:
            return 'JS没有执行成功'
        if res['result']['result'].get('exceptionDetails'):
            return 'WebConsole 执行JS的时候发生错误 '

        try:
            res = res['result']['result']['result'].get('value', 'undefined')
            return res
        except Exception as e:
            return e

    @classmethod
    def click(cls):
        js = Command.ELEMENT_CLICK.format(element=cls.object_id, index=cls.index)
        log.error('click\t' + js)
        return cls.__execute(js)

    @property
    def text(cls):
        js = Command.ELEMENT_TEXT.format(element=cls.object_id, index=cls.index)
        log.error('text\t' + js)
        return cls.__execute(js)

    @classmethod
    def innerText(cls, text):
        js = Command.ELEMENT_INNERTEXT.format(element=cls.object_id, index=cls.index, text=text)
        log.error('innerText\t' + js)
        return cls.__execute(js)

    @classmethod
    def mouse_click(cls):
        pass

    @classmethod
    def hasattribute(cls, text):
        js = Command.ELEMENT_HAS_ATTRIBUTE.format(element=cls.object_id, index=cls.index, attribute=text)
        log.error('hasattribute\t' + js)
        return cls.__execute(js)

    @classmethod
    def getattribute(cls, text):
        js = Command.ELEMENT_GET_ATTRIBUTE.format(element=cls.object_id, index=cls.index, attribute=text)
        log.info('getattribute\t' + js)
        return cls.__execute(js)


class demp(list):

    def __init__(self):
        self.a = [1, 2, 3, 4]

    @classmethod
    def click(cls):
        print(222)


if __name__ == '__main__':
    a = demp()
    a.click()
