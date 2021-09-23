#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : __init__.py.py


class TestCase(object):

    def setup(self):
        print('\033[1;33m 类中每个方法测试用例执行之前 \033[0m')

    def teardown(self):
        print('\033[1;33m 类中每个方法测试用例执行之后 \033[0m')

    def test_one_true(self, input_user, input_pwd):
        # print('\033[1;35m test_inter_two_sub_three \033[0m')
        # print('\033[1;36m %s : %s \033[0m' % (input_user, input_pwd))
        print('\033[1;32m %s : %s\n \033[0m' % (input_user, input_pwd))

    def test_two_true(self, input_user, input_pwd):
        # print('\033[1;35m test_inter_two_sub_three \033[0m')
        # print('\033[1;36m %s : %s \033[0m' % (input_user, input_pwd))
        print('\033[1;32m %s : %s\n \033[0m' % (input_user, input_pwd))