#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : globalparams.py
import pprint
import os
from local_lib.common.write_config import WriteConfig
from local_lib.common.read_config import ReadConfig
from local_lib.common.log import Log

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_name = os.path.join(project_path, 'config', 'config.ini')
log_path = os.path.join(project_path, 'log')
# print(project_path)
# print(config_name)



write_config = WriteConfig(config_name)
read_config = ReadConfig(config_name)
log = Log(log_path)




