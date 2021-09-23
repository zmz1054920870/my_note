#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : demo.py
import pprint
import requests

# class func(object):
#
#     def __init__(self, data):
#         self.name = data['name']
#         self.sex = data['sex']
#
#
#     @classmethod
#     def judge(cls, data):
#         if 'name' in data and 'sex' in data:
#             return True
#
#
# data = {'name': 'Andy', 'sex': 'boy'}
# data1 = {'name1': 'Andy', 'sex': 'boy'}
# data2 = {'name': 'Andy', 'sex2': 'boy'}
#
# if func.judge(data):
#     a = func(data)
#     print(a.name, a.sex)
# if func.judge(data1):
#     a = func(data1)
#     print(a.name, a.sex)
#
# if func.judge(data):
#     a = func(data)
#     print(a.name, a.sex)

class MyExceptions(Exception):

    def __init__(self, msg=None, screen=None, stacktrace=None):
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __repr__(self):
        exception_msg = "Message: %s\n" % self.msg
        if self.screen is not None:
            exception_msg += "Screenshot: available via screen\n"
        if self.stacktrace is not None:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg


class More(MyExceptions):
    pass


class Demo(object):

    def __str__(self):
        return 1111


class Cat:
    """定义一个猫类"""

    def __init__(self, new_name, new_age):
        """在创建完对象之后 会自动调用, 它完成对象的初始化的功能"""
        # self.name = "汤姆"
        # self.age = 20
        self.name = new_name
        self.age = new_age  # 它是一个对象中的属性,在对象中存储,即只要这个对象还存在,那么这个变量就可以使用
        # num = 100  # 它是一个局部变量,当这个函数执行完之后,这个变量的空间就没有了,因此其他方法不能使用这个变量

    # def __repr__(self):
    #     """返回一个对象的描述信息"""
    #     # print(num)
    #     return "名字是:%s , 年龄是:%d" % (self.name, self.age)

    def eat(self):
        print("%s在吃鱼...." % self.name)
        self.introduce()

    def drink(self):
        print("%s在喝可乐..." % self.name)

    def introduce(self):
        # print("名字是:%s, 年龄是:%d" % (汤姆的名字, 汤姆的年龄))
        # print("名字是:%s, 年龄是:%d" % (tom.name, tom.age))
        print("名字是:%s, 年龄是:%d" % (self.name, self.age))

# 创建了一个对象

# tom = Cat("汤姆", 30)
# # raise Exception
# tom.eat()

# import websocket
# import time
# import json
# js = "document.querySelector('#kw').value=100"
# payload = {
#             'id': 1,
#             'method': 'Runtime.evaluate',
#             'params': {'expression': js}
#         }
# data = json.dumps(payload)
# a = websocket.create_connection(url="ws://127.0.0.1:9222/devtools/page/D42B4A432B7ED1CEAF442F35E6EE9C1E")
# res1 = a.recv()
# print(111)
# a.send(data)
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




#
# online_command2 = """var {element} = document.evaluate("{xpath}",document.documentElement, null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)"""
#
# data = online_command2.format(element = "a", xpath = "//pre[@name='sendBox' and text()='土豆']")
#
# # a = "sdfdsfsdf'fdsfsdf'"
# b = quotation_switch(data)
# print(b)
#
# #
# # a = "dfsfsd'dsfdsfsdfsdf'fsdfsdf"
# # b = 'sdfsdfds"sfdsfdsfds"fsdfsdfsdfdsfsdfsdf'
# # c = a + b
# # d = c
# a = 'A"BCD"E"FG"H'
# b = "A'BCD'E'FG'H"
# c = a + b
# print(c)
# m = 'A"BCD"E"FG"HA'BCD'E'FG'H'
# online_command = 'var {element} = document.evaluate(\'{xpath}\''
# c = online_command.format(element="a", xpath='//pre[@name="sendBox" and text()="土豆"]')
# b = c
# print(b)
import random

class FindElement(object):

    def __init__(self, title):
        self.title = title
        self.session_id = random.randint(1, 10000000)
    def __repr__(self):
        return '<{0.__module__}.{0.__name__} (session="{1}")>'.format(
            type(self), self.session_id)

    def list(self):
        a = 2


# from selenium import webdriver
#
# driver = webdriver.Chrome()
# driver.get('http://www.baidu.com')
# a = driver.find_element_by_tag_name('div')
# print(a)
# b = driver.find_element_by_tag_name('span')
# print(b)
# a = FindElement('在线客服')
# b = FindElement('百度于以下')
# print(a)
# print(b)
import random
class demo12(object):

    a = {}

    def __init__(self):
        pass

    def func(self):
        self.a['tele']= random.randint(1,1000)

b = demo12()
b.func()
print(b.a)
demo12.a = {}
c = demo12()
print(c.a)