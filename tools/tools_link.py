'''
# @Title:
# @Time : 2021/9/14 15:30
# @File : tools_link.py
# @Software: PyCharm

'''
from airtest.core.android import Android
from airtest.core.api import *
auto_setup(__file__)

def connectDevice(deviceCode, httpServer):
    connect_device("android://" + httpServer + "/" + deviceCode + "?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=MINITOUCH")
    init_device()

def initServer(deviceCode, package, httpServer):
    connectDevice(deviceCode, httpServer)
    android = Android(deviceCode)
    # 如果屏幕没亮，则唤醒屏幕
    if not android.is_screenon():
        android.wake()
    # 如果锁屏了，则解锁
    if android.is_locked():
        android.unlock()
    # 关闭对应app
    stop_app(package)
    sleep(5)
    # 启动对应app
    start_app(package)
    sleep(10)