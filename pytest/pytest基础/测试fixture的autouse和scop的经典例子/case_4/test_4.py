#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : test_4.py

# import pytest
#
# user_list = ['admin1', 'admin2']
# user_pwd = ['123456', '654321']
#
#
# @pytest.fixture(scope="function", params=user_list)
# def user(request):
#     print('user')
#     return request.param
#
#
# @pytest.fixture(scope="function", params=user_pwd)
# def pwd(request):
#     print('pwd')
#     return request.param
#
#
# @pytest.fixture(scope='module')
# def login(user, pwd):
#     print('第一组账号', user, pwd)
#     yield (user, pwd)
#     print('结束战斗')
#
#
# def test_demo_one(login):
#     print('test_demo_one', login)
#
#
# if __name__ == '__main__':
#     pytest.main(['-s'])