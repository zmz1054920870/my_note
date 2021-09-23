#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : test_3.py
import pytest


# @pytest.fixture(scope='class', params=['zhangsan', 'lisi'], ids=['xxx', 'yyy'], autouse=True)
# def input_user(request):
#     print(1111111111111111111111111)
#     return request.param

def setup_module():
    print('\033[1;35m setup_module setup_module setup_module setup_module setup_module \033[0m')


def teardown_module():
    print('\033[1;35m teardown_module teardown_module teardown_module teardown_module \033[0m')


class TestCase3(object):

    def setup_class(self):
        print('\033[1;35m ------------------------------------------------- \033[0m')

    def teardown_class(self):
        print('\033[1;35m ================================================== \033[0m')

    def test_case_3_one_true(self, input_user):
        # print('\033[1;35m test_inter_two_sub_three \033[0m')
        # print('\033[1;36m %s : %s \033[0m' % (input_user, input_pwd))
        print('\033[1;32m test_case_3_one_true %s \n \033[0m' % input_user)

    def test_case_3_three_true(self):
        print('\033[1;32m test_case_3_two_true\n \033[0m')

    def test_case_3_two_true(self, input_user):
        # print('\033[1;35m test_inter_two_sub_three \033[0m')
        # print('\033[1;36m %s : %s \033[0m' % (input_user, input_pwd))
        print('\033[1;32m test_case_3_two_true %s \n \033[0m' % input_user)




def test_case_3_four_true(input_user):
    print('\033[1;32m test_case_3_four_true %s \n \033[0m' % input_user)


if __name__ == '__main__':
    pytest.main(['-s'])
    # pytest.main(['-s', '--collect-only'])