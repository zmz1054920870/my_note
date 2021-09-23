#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : find_element.py
import selenium
import random
import datetime
import hashlib
import uuid
import time
from local_lib.common.webdriver.command import *
from config.globalparams import log
from local_lib.common.webdriver.kernel.kernel_driver_up import RunJs
# from selenium.webdriver.remote.command import Command
from local_lib.common.webdriver.command import Command
from local_lib.common.webdriver.by import By
from local_lib.common.webdriver.execute_element import ExecuteElement
from local_lib.common.webdriver.exceptions import *

class FindElement(object):

    def __init__(self, title):
        """
        :param title: page name  ， 必须传，不然不知道操作哪一个操作哪一个页面

        """
        self.title = title
        self.session_id = random.randint(1, 10000000) #整个玩意主要是模拟selenium，其实完全没必要

    def __repr__(self):
        return '<{0.__module__}.{0.__name__}__at_{1} (session="{2}")>'.format(
            type(self), self.title, self.session_id)

    def __find(self, value):
        """

        selenium 如果元素没有找到会报错，我模仿的是selenium
        :param value:
        :return:
        """
        object_id = 'js' + uuid.uuid1().hex + str(random.randint(1, 1000000))
        command_js = Command.FIND_ELEMENT_XPATH.format(element=object_id, xpath=value)
        command_js = switch_js(command_js)
        log.error('evaluate_js\t' + command_js)
        js_executor = RunJs()
        xpath_result = js_executor.run_js(self.title, command_js)

        log.error('xpath_result\t' + str(xpath_result))

        if xpath_result['code'] == False:
            raise NotFoundRemoteUrlException('远程的url调试端口没打开,或者WS已经失效或者断开, 执行JS失败')
        else:
            command_len = Command.XPATH_ELEMENT_LEN.format(element=object_id)
            length_result = js_executor.run_js(self.title, command_len)

            log.error('length_result\t' + str(length_result))

            if length_result['code'] == False:
                raise NotFoundRemoteUrlException('远程的url调试端口没打开,或者WS已经失效或者断开, 执行JS失败')
            else:
                element_len = length_result['result']['result']['result']['value']
                if element_len == 0:
                    raise NotFoundElementException('没有找到元素')
                else:
                    return [ExecuteElement(self.title, object_id, index=i) for i in range(element_len)]


    def find_elements(self, by, value):
        """
            这里可以写一个正则表达式判断一下，传入得格式是不是Xpath格式，不是给他报个错
            我懒得写了,狗头保命。。。。。^ - ^
            #todo

        """
        if by == By.XPATH:
            by = Command.FIND_ELEMENT_XPATH
        return self.__find(value)

    def find_element_by_xpath(self, value):
        return self.find_elements(by=By.XPATH, value=value)


def switch_js(js):
    str_list = []
    quota_index = []
    for i in range(len(js)):
        str_list.append(i)
        if i == '\'':
            quota_index.append(i)
    if len(quota_index) > 2:
        for index in quota_index[1: -1]:
            str_list[index] = "\""
    else:
        return js
    return ''.join(str_list)

def create_session_id():
    pass

if __name__ == '__main__':

    a = FindElement('在线客服')
    # b = a.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/pre')
    # b[0].innerText("我是超人")
    # c = FindElement('在线客服')
    # d = c.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/pre')
    # d[0].innerText('测试一下')
    # d[0].click()
    #
    # print(d[0].text)
    # # e = c.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[3]/div/div')
    # # e[0].click()
    # print(d[0].getattribute('name'))
    print(a)