'''
# @Title:
# @Time : 2021/9/15 10:34
# @File : tools_CheckApp.py
# @Software: PyCharm

'''
from airtest.core.api import *

auto_setup(__file__)
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


# 用于检测app是否正确启动
def check():
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    check_status = poco("android:id/content").offspring("我的，未选中状态").offspring("com.taobao.idlefish:id/tab_icon").exists()
    if check_status is True:
        return True
    else:
        return False