#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : exceptions.py
# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


class WebDriverException(Exception):
    """
    Base webdriver exception.
    """

    def __init__(self, msg=None, screen=None, stacktrace=None):
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        if self.screen is not None:
            exception_msg += "Screenshot: available via screen\n"
        if self.stacktrace is not None:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg


class MoreThanOneWebElementException(WebDriverException):
    """
    使用单元素查找方法但结果有多个元素时抛出
    """
    pass


class NotFoundRemoteUrlException(WebDriverException):
    """
    远程的url调试端口没打开,或者WS已经失效或者断开
    """
    pass


class NotFoundElementException(WebDriverException):
    """
    所写的JS不存在
    """
    pass


if __name__ == '__main__':
    # raise MoreThanOneWebElementException('土匪')
    raise AssertionError
