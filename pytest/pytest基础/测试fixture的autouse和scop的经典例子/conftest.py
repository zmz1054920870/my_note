#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : conftest.py
import pytest


def pytest_configure(config):
    marker_list = ['critical', 'normal', 'minor', 'slow']
    for markers in marker_list:
        config.addinivalue_line('markers', markers)


@pytest.fixture(scope='module', params=['zhangsan', 'lisi', '王麻子'], ids=['xxx', 'yyy', 'zzz'], autouse=True)
def input_user(request):
    print('\033[1;35;44m mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm \033[0m')
    return request.param
#
#
# @pytest.fixture(scope='function', params=['123456', '654321'], ids=['uuu', 'iii'], autouse=True)
# def input_pwd(request):
#     print(222222222222222222222222222)
#     return request.param