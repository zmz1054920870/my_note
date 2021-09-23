#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : command.py

class Command(object):

    #获取元素
    FIND_ELEMENT_QUERY = "var {element} = document.querySelector('{css}')"
    FIND_ELEMENT_XPATH = "var {element} = document.evaluate('{xpath}',document.documentElement, null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)"
    XPATH_ELEMENT_LEN = "{element}.snapshotLength"



    #执行事件
    ELEMENT_CLICK = '{element}.snapshotItem({index}).click()'
    ELEMENT_TEXT = '{element}.snapshotItem({index}).innerText'
    ELEMENT_INNERTEXT = "{element}.snapshotItem({index}).innerText='{text}'"
    ELEMENT_VALUE = "{element}.snapshotItem({index}).value='{text}'"
    ELEMENT_GET_ATTRIBUTE = "{element}.snapshotItem({index}).getAttribute('{attribute}')"
    ELEMENT_HAS_ATTRIBUTE = "{element}.snapshotItem({index}).hasAttribute('{attribute}')"


if __name__ == '__main__':
    #
    # a = Command()
    # c = a.FIND_ELEMENT_ID.format(element='a', id="#kw")
    # print(c)
    pass