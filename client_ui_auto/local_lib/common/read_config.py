#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : read_config.py
from configparser import ConfigParser


class ReadConfig(object):

    def __init__(self, filename):
        self.filename = filename

    def get_config(self, sec, opt):
        config = ConfigParser()
        config.read(self.filename, encoding='UTF-8')
        try:
            value = config.get(sec, opt)
            return value
        except Exception as e:
            print(e)

if __name__ == '__main__':
    from config.globalparams import read_config
    number = read_config.get_config('projectConfig', 'chrome_remote_port')
    print(number, type(number))