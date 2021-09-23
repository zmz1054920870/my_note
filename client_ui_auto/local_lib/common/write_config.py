#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : write_config.py
from configparser import ConfigParser


class WriteConfig(object):

    def __init__(self, filename):
        self.filename = filename

    def set_config(self, sec, opt, val):
        try:
            config = ConfigParser()
            config.read(self.filename, encoding='UTF-8')
            if sec not in config.sections():
                config.add_section(sec)
            config.set(sec, opt, val)
            with open(self.filename, 'w') as f:
                config.write(f)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    from config.globalparams import write_config
    write_config.set_config()

