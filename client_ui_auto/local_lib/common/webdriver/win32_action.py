#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# @Time    : 2021/3/25 23:53
# @Author  : 超级无敌张铁柱
# @File    : win32_action.py

import timer
import time
import win32event, win32gui, win32api, win32con
import re
from config.globalparams import read_config


class glork:

    def __init__(self, delay=1000, max=10):
        self.x = 0
        self.max = max
        self.id = timer.set_timer(delay, self.increment)
        # Could use the threading module, but this is
        # a win32 extension test after all! :-)
        self.event = win32event.CreateEvent(None, 0, 0, None)

    def increment(self, id, time):
        print('x = %d' % self.x)
        self.x = self.x + 1
        # if we've reached the max count,
        # kill off the timer.
        if self.x > self.max:
            # we could have used 'self.id' here, too
            timer.kill_timer(id)
            win32event.SetEvent(self.event)


# create a counter that will count from '1' thru '10', incrementing
# once a second, and then stop.

def demo(delay=1000, stop=10):
    g = glork(delay, stop)
    # Timers are message based - so we need
    # To run a message loop while waiting for our timers
    # to expire.
    start_time = time.time()
    while 1:
        # We can't simply give a timeout of 30 seconds, as
        # we may continouusly be recieving other input messages,
        # and therefore never expire.
        rc = win32event.MsgWaitForMultipleObjects(
            (g.event,),  # list of objects
            0,  # wait all
            500,  # timeout
            win32event.QS_ALLEVENTS,  # type of input
        )
        if rc == win32event.WAIT_OBJECT_0:
            # Event signalled.
            break
        elif rc == win32event.WAIT_OBJECT_0 + 1:
            # Message waiting.
            if win32gui.PumpWaitingMessages():
                raise RuntimeError("We got an unexpected WM_QUIT message!")
        else:
            # This wait timed-out.
            if time.time() - start_time > 30:
                raise RuntimeError("We timed out waiting for the timers to expire!")


class Win32Action(object):
    __instance = None
    __page_handle = None  # 用于存放浏览器窗口句柄

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__page_handle = get_web_handle()
            cls.__instance = super(Win32Action, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        pass

    def __repr__(self):
        return '<{0.__module__}.{0.__name__}>'.format(type(self))

    def move_to_element(self, x, y):
        print(self.__page_handle)
        rect = win32gui.GetWindowRect(self.__page_handle)
        position_x = rect[0] + x
        position_y = rect[1] + y
        win32api.SetCursorPos((position_x, position_y))

    def mouse_click(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 200, 200, 0, 0)
        win32api.mouse_event(win32con.MUOSEEVENTF_LEFTUP, 200, 200, 0, 0)


def get_web_handle():
    windows_handle = win32gui.GetDesktopWindow()

    hwndChildList = []

    handle1 = win32gui.EnumChildWindows(windows_handle, lambda hwnd, param: param.append(hwnd), hwndChildList)

    for i in hwndChildList:
        # 获取类名
        class_name = win32gui.GetClassName(i)
        if class_name == 'Chrome_WidgetWin_1':
            # 获取窗口标题
            wind_name = win32gui.GetWindowText(i)
            pattern = ' - Google Chrome'
            if re.search(pattern, wind_name):
                handle = win32gui.FindWindowEx(i, 0, 'Chrome_RenderWidgetHostHWND', 'Chrome Legacy Window')
                if handle != 0:
                    print('%x' % handle)
                    return handle
    return None

if __name__ == '__main__':

    # print('%x' % a, a)
    #
    # # win32gui.ShowWindow(3408958, win32con.SW_SHOWMAXIMIZED)
    # hwnd=win32gui.GetParent(a)
    # print('%x' % hwnd, hwnd)
    # # win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    # win32gui.MoveWindow(hwnd, 44, 44, 750, 500, 1)

    # a = Win32Action()

    # rect = win32api.GetCursorPos()
    # win32api.SetCursorPos((300, 300))
    # hw = win32gui.WindowFromPoint(win32api.GetCursorPos())
    # print(hw)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 200, 200, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 200, 0, 0)